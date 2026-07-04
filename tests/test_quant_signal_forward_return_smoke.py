from __future__ import annotations

import csv
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.quant_signal_forward_return_smoke import evaluate_forward_returns, main, summarize


def _signal(date: str, code: str, close: str, state: str) -> dict[str, str]:
    return {
        "date": date,
        "code": code,
        "stock_name": f"Name{code}",
        "market": "KOSPI",
        "close": close,
        "signal_state": state,
        "source_strategy": "001-strategy-universe-momentum",
        "signal_mode": "paper_signal_candidate_only",
    }


def _price(date: str, code: str, close: str) -> dict[str, str]:
    return {"date": date, "code": code, "close": close}


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


class QuantSignalForwardReturnSmokeTest(unittest.TestCase):
    def test_computes_raw_and_directional_forward_returns(self) -> None:
        signals = [
            _signal("2025-01-02", "005930", "100", "BUY candidate"),
            _signal("2025-01-02", "000660", "100", "SELL candidate"),
        ]
        prices = [
            _price("2025-01-02", "005930", "100"),
            _price("2025-01-03", "005930", "110"),
            _price("2025-01-02", "000660", "100"),
            _price("2025-01-03", "000660", "90"),
        ]

        rows = evaluate_forward_returns(signals, prices, horizons=(1,))
        by_code = {row.signal["code"]: row for row in rows}

        self.assertEqual(by_code["005930"].evaluation_status, "complete")
        self.assertAlmostEqual(by_code["005930"].raw_forward_return_pct or 0, 10.0)
        self.assertAlmostEqual(by_code["005930"].directional_forward_score_pct or 0, 10.0)
        self.assertEqual(by_code["000660"].evaluation_status, "complete")
        self.assertAlmostEqual(by_code["000660"].raw_forward_return_pct or 0, -10.0)
        self.assertAlmostEqual(by_code["000660"].directional_forward_score_pct or 0, 10.0)

    def test_marks_missing_forward_prices_by_horizon(self) -> None:
        signals = [_signal("2025-01-02", "005930", "100", "BUY candidate")]
        prices = [_price("2025-01-02", "005930", "100"), _price("2025-01-03", "005930", "101")]

        rows = evaluate_forward_returns(signals, prices, horizons=(1, 5))
        by_horizon = {row.horizon: row for row in rows}

        self.assertEqual(by_horizon[1].evaluation_status, "complete")
        self.assertEqual(by_horizon[5].evaluation_status, "missing_forward_price")

    def test_summary_groups_complete_return_coverage(self) -> None:
        signals = [
            _signal("2025-01-02", "005930", "100", "BUY candidate"),
            _signal("2025-01-02", "000660", "100", "SELL candidate"),
        ]
        prices = [
            _price("2025-01-02", "005930", "100"),
            _price("2025-01-03", "005930", "110"),
            _price("2025-01-02", "000660", "100"),
            _price("2025-01-03", "000660", "90"),
        ]

        summary = summarize(evaluate_forward_returns(signals, prices, horizons=(1,)))

        self.assertEqual(summary["complete_rows"], 2)
        self.assertEqual(summary["status_counts"], {"complete": 2})
        self.assertAlmostEqual(summary["avg_directional_score_by_horizon"]["1"], 10.0)

    def test_cli_writes_report_and_csv_without_order_intents(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            signals = root / "signals.csv"
            prices = root / "prices.csv"
            rows_output = root / "forward.rows.csv"
            report_output = root / "forward.md"
            _write_csv(signals, [_signal("2025-01-02", "005930", "100", "BUY candidate")])
            _write_csv(prices, [_price("2025-01-02", "005930", "100"), _price("2025-01-03", "005930", "105")])

            with patch(
                "sys.argv",
                [
                    "quant_signal_forward_return_smoke.py",
                    "--signals-input",
                    str(signals),
                    "--price-input",
                    str(prices),
                    "--horizons",
                    "1",
                    "--csv-output",
                    str(rows_output),
                    "--report-output",
                    str(report_output),
                ],
            ):
                self.assertEqual(main(), 0)

            report = report_output.read_text(encoding="utf-8")
            with rows_output.open("r", encoding="utf-8-sig", newline="") as handle:
                written = list(csv.DictReader(handle))

        self.assertEqual(written[0]["evaluation_status"], "complete")
        self.assertEqual(written[0]["evaluation_mode"], "paper_forward_return_smoke_only")
        self.assertIn("- KIS API call: `false`", report)
        self.assertIn("- KRX API call: `false`", report)
        self.assertIn("- Order intent generated: `false`", report)
        self.assertIn("- Backtest readiness: `hold`", report)

    def test_rejects_non_positive_horizons(self) -> None:
        with self.assertRaisesRegex(ValueError, "horizons must be positive"):
            evaluate_forward_returns([], [], horizons=(0,))


if __name__ == "__main__":
    unittest.main()
