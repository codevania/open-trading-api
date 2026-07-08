from __future__ import annotations

import csv
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.quant_backtest_pnl_smoke import compute_pnl_smoke, main, render_report, summarize


def _target_rows() -> list[dict[str, str]]:
    return [
        {
            "date": "2025-02-05",
            "code": "005930",
            "stock_name": "Samsung Electronics",
            "market": "KOSPI",
            "target_side": "LONG",
            "target_weight": "0.500000",
            "source_signal_state": "BUY candidate",
            "target_mode": "paper_portfolio_target_smoke_only",
            "order_intent_generated": "false",
        },
        {
            "date": "2025-02-05",
            "code": "000660",
            "stock_name": "SK hynix",
            "market": "KOSPI",
            "target_side": "LONG",
            "target_weight": "0.250000",
            "source_signal_state": "BUY candidate",
            "target_mode": "paper_portfolio_target_smoke_only",
            "order_intent_generated": "false",
        },
    ]


def _forward_rows() -> list[dict[str, str]]:
    return [
        {
            "date": "2025-02-05",
            "code": "005930",
            "horizon_trading_days": "1",
            "evaluation_status": "complete",
            "forward_date": "2025-02-06",
            "raw_forward_return_pct": "10.0000",
            "evaluation_mode": "paper_forward_return_smoke_only",
        },
        {
            "date": "2025-02-05",
            "code": "000660",
            "horizon_trading_days": "1",
            "evaluation_status": "missing_forward_price",
            "forward_date": "",
            "raw_forward_return_pct": "",
            "evaluation_mode": "paper_forward_return_smoke_only",
        },
    ]


def _benchmark_rows() -> list[dict[str, str]]:
    return [
        {
            "date": "2025-02-05",
            "benchmark": "KOSPI",
            "horizon_trading_days": "1",
            "evaluation_status": "complete",
            "forward_date": "2025-02-06",
            "benchmark_return_pct": "2.0000",
            "evaluation_mode": "paper_benchmark_return_smoke_only",
        }
    ]


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


class QuantBacktestPnlSmokeTest(unittest.TestCase):
    def test_computes_weighted_pnl_contribution_without_readiness_upgrade(self) -> None:
        rows, diagnostics = compute_pnl_smoke(_target_rows(), _forward_rows(), horizons=(1,))
        summary = summarize(rows, diagnostics)

        self.assertEqual(summary["pnl_smoke_status"], "pass_smoke")
        self.assertEqual(summary["complete_rows"], 1)
        self.assertAlmostEqual(rows[0].weighted_return_contribution_pct or 0, 5.0)
        self.assertEqual(rows[1].evaluation_status, "missing_forward_price")
        self.assertAlmostEqual(diagnostics[0].gross_target_weight, 0.75)
        self.assertAlmostEqual(diagnostics[0].covered_gross_weight, 0.5)
        self.assertAlmostEqual(diagnostics[0].missing_gross_weight, 0.25)
        self.assertAlmostEqual(diagnostics[0].weighted_return_pct, 5.0)

    def test_optional_benchmark_join_computes_weighted_excess(self) -> None:
        rows, diagnostics = compute_pnl_smoke(_target_rows(), _forward_rows(), horizons=(1,), benchmark_rows=_benchmark_rows())
        summary = summarize(rows, diagnostics)

        complete = [row for row in rows if row.evaluation_status == "complete"][0]

        self.assertEqual(summary["benchmark_joined_rows"], 2)
        self.assertEqual(dict(summary["benchmark_join_status_counts"]), {"complete": 2})
        self.assertAlmostEqual(complete.benchmark_return_pct or 0, 2.0)
        self.assertAlmostEqual(complete.excess_return_pct or 0, 8.0)
        self.assertAlmostEqual(complete.weighted_excess_return_contribution_pct or 0, 4.0)
        self.assertAlmostEqual(dict(summary["avg_weighted_excess_by_horizon"])["1"], 4.0)

    def test_missing_forward_rows_are_reported_not_filled_as_zero(self) -> None:
        rows, diagnostics = compute_pnl_smoke(_target_rows(), _forward_rows(), horizons=(5,))
        summary = summarize(rows, diagnostics)

        self.assertEqual(summary["pnl_smoke_status"], "hold")
        self.assertEqual({row.evaluation_status for row in rows}, {"missing_forward_row"})
        self.assertAlmostEqual(diagnostics[0].missing_gross_weight, 0.75)

    def test_rejects_order_intents_and_non_long_targets(self) -> None:
        rows = [dict(row) for row in _target_rows()]
        rows[0]["order_intent_generated"] = "true"
        with self.assertRaisesRegex(ValueError, "must not contain order intents"):
            compute_pnl_smoke(rows, _forward_rows(), horizons=(1,))

        rows = [dict(row) for row in _target_rows()]
        rows[0]["target_side"] = "SHORT"
        with self.assertRaisesRegex(ValueError, "LONG-only"):
            compute_pnl_smoke(rows, _forward_rows(), horizons=(1,))

    def test_report_keeps_backtest_and_live_guardrails(self) -> None:
        rows, diagnostics = compute_pnl_smoke(_target_rows(), _forward_rows(), horizons=(1,))
        report = render_report(
            rows=rows,
            diagnostics=diagnostics,
            summary=summarize(rows, diagnostics),
            targets_input=Path("_report/quant/research/targets.rows.csv"),
            forward_returns_input=Path("_report/quant/research/forward.rows.csv"),
            benchmark_returns_input=None,
            benchmark_label="KOSPI",
            horizons=(1,),
            csv_output=Path("_report/quant/research/pnl.rows.csv"),
        )

        self.assertIn("- PnL smoke status: `pass_smoke`", report)
        self.assertIn("- Backtest readiness: `hold`", report)
        self.assertIn("- Live trading readiness: `blocked`", report)
        self.assertIn("not a production Backtest result", report)

    def test_cli_writes_report_and_rows_without_crlf(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            targets = root / "targets.rows.csv"
            forward_returns = root / "forward.rows.csv"
            rows_output = root / "pnl.rows.csv"
            report_output = root / "pnl.md"
            _write_csv(targets, _target_rows())
            _write_csv(forward_returns, _forward_rows())
            benchmark_returns = root / "benchmark.rows.csv"
            _write_csv(benchmark_returns, _benchmark_rows())

            with patch(
                "sys.argv",
                [
                    "quant_backtest_pnl_smoke.py",
                    "--targets-input",
                    str(targets),
                    "--forward-returns-input",
                    str(forward_returns),
                    "--benchmark-returns-input",
                    str(benchmark_returns),
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
            rows_text = rows_output.read_text(encoding="utf-8-sig")
            report_bytes = report_output.read_bytes()
            rows_bytes = rows_output.read_bytes()

        self.assertIn("# Backtest PnL Smoke", report)
        self.assertIn("weighted_return_contribution_pct", rows_text)
        self.assertIn("weighted_excess_return_contribution_pct", rows_text)
        self.assertIn("- Benchmark-return input: [[", report)
        self.assertIn("paper_backtest_pnl_smoke_only", rows_text)
        self.assertNotIn(b"\r\n", report_bytes)
        self.assertNotIn(b"\r\n", rows_bytes)


if __name__ == "__main__":
    unittest.main()
