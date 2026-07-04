from __future__ import annotations

import csv
import tempfile
import unittest
from pathlib import Path

from scripts.quant_point_in_time_liquidity_filter import apply_point_in_time_liquidity_filter, render_report, write_csv


def _row(date: str, code: str, value: str, status: str = "include", reasons: str = "") -> dict[str, str]:
    return {
        "date": date,
        "code": code,
        "stock_name": f"Name{code}",
        "market": "KOSPI",
        "trading_value_krw": value,
        "pit_universe_status": status,
        "pit_universe_exclude_reasons": reasons,
    }


class QuantPointInTimeLiquidityFilterTest(unittest.TestCase):
    def test_applies_trailing_date_scoped_liquidity_filter(self) -> None:
        rows = [
            _row("2025-01-02", "005930", "1000000000"),
            _row("2025-01-03", "005930", "2000000000"),
            _row("2025-01-06", "005930", "3000000000"),
            _row("2025-01-02", "000020", "100000000"),
            _row("2025-01-03", "000020", "200000000"),
            _row("2025-01-06", "000020", "300000000"),
            _row("2025-01-02", "000040", "999999999", status="exclude", reasons="status_event:managed_issue_active"),
            _row("2025-01-02", "000050", ""),
        ]

        result = apply_point_in_time_liquidity_filter(rows, lookback=3, min_avg_trading_value_krw=1_000_000_000)
        by_key = {(row.source["date"], row.source["code"]): row for row in result}

        self.assertEqual(by_key[("2025-01-02", "005930")].liquidity_status, "data_insufficient")
        self.assertEqual(by_key[("2025-01-06", "005930")].final_status, "include")
        self.assertEqual(by_key[("2025-01-06", "005930")].avg_trading_value_krw, 2_000_000_000)
        self.assertEqual(by_key[("2025-01-06", "000020")].final_status, "exclude")
        self.assertEqual(by_key[("2025-01-06", "000020")].liquidity_status, "fail")
        self.assertEqual(by_key[("2025-01-02", "000040")].liquidity_status, "not_evaluated_preexisting_exclude")
        self.assertEqual(by_key[("2025-01-02", "000050")].liquidity_status, "data_invalid")

    def test_writes_csv_and_report_without_requiring_external_data(self) -> None:
        rows = [
            _row("2025-01-02", "005930", "1000000000"),
            _row("2025-01-03", "005930", "2000000000"),
        ]
        result = apply_point_in_time_liquidity_filter(rows, lookback=2, min_avg_trading_value_krw=1_000_000_000)
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "rows.csv"
            write_csv(result, output, lookback=2)
            with output.open("r", encoding="utf-8-sig", newline="") as handle:
                written = list(csv.DictReader(handle))
            report = render_report(result, Path("input.csv"), "20250102-20250103", 2, 1_000_000_000, output)

        self.assertEqual(written[-1]["pit_liquidity_final_status"], "include")
        self.assertEqual(written[-1]["avg_trading_value_2d_krw"], "1500000000")
        self.assertIn("- KIS API call: `false`", report)
        self.assertIn("- Include rows after Liquidity Filter: `1`", report)


if __name__ == "__main__":
    unittest.main()
