from __future__ import annotations

import csv
import tempfile
import unittest
from pathlib import Path

from scripts.quant_point_in_time_signal_candidates import generate_signal_candidates, render_report, write_csv


def _row(date: str, code: str, close: str, status: str = "include") -> dict[str, str]:
    return {
        "date": date,
        "code": code,
        "stock_name": f"Name{code}",
        "market": "KOSPI",
        "close": close,
        "pit_liquidity_final_status": status,
    }


class QuantPointInTimeSignalCandidatesTest(unittest.TestCase):
    def test_generates_ranked_momentum_candidates_only_for_liquid_rows(self) -> None:
        rows = [
            _row("2025-01-02", "005930", "100"),
            _row("2025-01-03", "005930", "110"),
            _row("2025-01-06", "005930", "121"),
            _row("2025-01-02", "000020", "100"),
            _row("2025-01-03", "000020", "90"),
            _row("2025-01-06", "000020", "81"),
            _row("2025-01-02", "000040", "100"),
            _row("2025-01-03", "000040", "200"),
            _row("2025-01-06", "000040", "300", status="exclude"),
        ]

        candidates = generate_signal_candidates(rows, lookback=2, threshold_pct=0, top_n_per_state=10)
        by_code = {candidate.source["code"]: candidate for candidate in candidates}

        self.assertEqual(by_code["005930"].signal_state, "BUY candidate")
        self.assertAlmostEqual(by_code["005930"].roc_pct, 21.0)
        self.assertEqual(by_code["000020"].signal_state, "SELL candidate")
        self.assertAlmostEqual(by_code["000020"].roc_pct, -19.0)
        self.assertNotIn("000040", by_code)

    def test_writes_csv_and_report(self) -> None:
        rows = [
            _row("2025-01-02", "005930", "100"),
            _row("2025-01-03", "005930", "110"),
        ]
        candidates = generate_signal_candidates(rows, lookback=1, threshold_pct=0, top_n_per_state=5)
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "signals.csv"
            write_csv(candidates, output)
            with output.open("r", encoding="utf-8-sig", newline="") as handle:
                written = list(csv.DictReader(handle))
            report = render_report(candidates, Path("input.csv"), "20250102-20250103", 1, 0, 5, output)

        self.assertEqual(written[0]["signal_state"], "BUY candidate")
        self.assertEqual(written[0]["source_strategy"], "001-strategy-universe-momentum")
        self.assertIn("- Order intent generated: `false`", report)
        self.assertIn("Signal Candidate", report)


if __name__ == "__main__":
    unittest.main()
