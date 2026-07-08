from __future__ import annotations

import csv
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.quant_benchmark_return_smoke import (
    BenchmarkSpec,
    evaluate_benchmark_returns,
    main,
    summarize,
)


def _signal(date: str) -> dict[str, str]:
    return {"date": date, "code": "005930", "signal_state": "BUY candidate"}


def _index(date: str, index_class: str, index_name: str, close: str) -> dict[str, str]:
    return {"date": date, "index_class": index_class, "index_name": index_name, "close": close}


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


class QuantBenchmarkReturnSmokeTest(unittest.TestCase):
    def test_computes_benchmark_forward_returns(self) -> None:
        spec = BenchmarkSpec("KOSPI", "KOSPI", "코스피")
        rows = evaluate_benchmark_returns(
            [_signal("2025-01-02")],
            [
                _index("2025-01-02", "KOSPI", "코스피", "100"),
                _index("2025-01-03", "KOSPI", "코스피", "110"),
            ],
            (spec,),
            horizons=(1,),
        )

        self.assertEqual(rows[0].evaluation_status, "complete")
        self.assertEqual(rows[0].forward_date, "2025-01-03")
        self.assertAlmostEqual(rows[0].benchmark_return_pct or 0, 10.0)

    def test_marks_missing_forward_index_by_horizon(self) -> None:
        spec = BenchmarkSpec("KOSDAQ", "KOSDAQ", "코스닥")
        rows = evaluate_benchmark_returns(
            [_signal("2025-01-02")],
            [
                _index("2025-01-02", "KOSDAQ", "코스닥", "100"),
                _index("2025-01-03", "KOSDAQ", "코스닥", "101"),
            ],
            (spec,),
            horizons=(1, 5),
        )
        by_horizon = {row.horizon: row for row in rows}

        self.assertEqual(by_horizon[1].evaluation_status, "complete")
        self.assertEqual(by_horizon[5].evaluation_status, "missing_forward_index")

    def test_summary_groups_by_benchmark_horizon(self) -> None:
        spec = BenchmarkSpec("KOSPI200", "KOSPI", "코스피 200")
        summary = summarize(
            evaluate_benchmark_returns(
                [_signal("2025-01-02")],
                [
                    _index("2025-01-02", "KOSPI", "코스피 200", "200"),
                    _index("2025-01-03", "KOSPI", "코스피 200", "220"),
                ],
                (spec,),
                horizons=(1,),
            )
        )

        self.assertEqual(summary["complete_rows"], 1)
        self.assertAlmostEqual(dict(summary["avg_return_by_benchmark_horizon"])["KOSPI200/1"], 10.0)

    def test_rejects_duplicate_benchmark_dates(self) -> None:
        spec = BenchmarkSpec("KOSPI", "KOSPI", "코스피")

        with self.assertRaisesRegex(ValueError, "duplicate benchmark date"):
            evaluate_benchmark_returns(
                [_signal("2025-01-02")],
                [
                    _index("2025-01-02", "KOSPI", "코스피", "100"),
                    _index("2025-01-02", "KOSPI", "코스피", "101"),
                ],
                (spec,),
                horizons=(1,),
            )

    def test_cli_writes_report_and_csv_without_order_intents(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            signals = root / "signals.csv"
            index_input = root / "index_daily.csv"
            rows_output = root / "benchmark.rows.csv"
            report_output = root / "benchmark.md"
            _write_csv(signals, [_signal("2025-01-02")])
            _write_csv(
                index_input,
                [
                    _index("2025-01-02", "KOSPI", "코스피", "100"),
                    _index("2025-01-03", "KOSPI", "코스피", "105"),
                ],
            )

            with patch(
                "sys.argv",
                [
                    "quant_benchmark_return_smoke.py",
                    "--signals-input",
                    str(signals),
                    "--index-input",
                    str(index_input),
                    "--benchmarks",
                    "KOSPI=KOSPI:코스피",
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
            report_bytes = report_output.read_bytes()
            rows_bytes = rows_output.read_bytes()
            with rows_output.open("r", encoding="utf-8-sig", newline="") as handle:
                written = list(csv.DictReader(handle))

        self.assertEqual(written[0]["evaluation_status"], "complete")
        self.assertEqual(written[0]["evaluation_mode"], "paper_benchmark_return_smoke_only")
        self.assertIn("- KIS API call: `false`", report)
        self.assertIn("- KRX API call: `false`", report)
        self.assertIn("- Order intent generated: `false`", report)
        self.assertIn("- Backtest readiness: `hold`", report)
        self.assertNotIn(b"\r\n", report_bytes)
        self.assertNotIn(b"\r\n", rows_bytes)


if __name__ == "__main__":
    unittest.main()
