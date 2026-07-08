from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from scripts.quant_bias_control_preflight import build_bias_checks, main, render_report


def _readiness_report() -> str:
    return "\n".join(
        [
            "- Backtest readiness: `hold`",
            "- Live trading readiness: `blocked`",
            "- Order intent generated: `false`",
            "| Gate | Status | Evidence | Next action |",
            "| --- | --- | --- | --- |",
            "| `forward_return_smoke` | `pass_smoke` | 2/2 forward-return rows complete | next |",
            "| `benchmark_returns_smoke` | `pass_smoke` | local benchmark return smoke report is diagnostic-only | next |",
            "| `backtest_attribution_smoke` | `pass_smoke_assumption_only` | local attribution smoke links costs; broker fee override still required | next |",
            "| `oos_walk_forward_preflight` | `pass_smoke_plumbing_only` | local OOS/Walk-Forward temporal fold plumbing exists | next |",
            "| `point_in_time_status_coverage` | `hold` | source manifest validation=not_supplied | next |",
            "| `backtest_engine` | `hold` | Backtest engine is not wired | next |",
            "| `live_trading_controls` | `blocked` | no order executor | next |",
            "| `kis_demo_account` | `blocked` | KIS_PAPER_STOCK missing | next |",
        ]
    )


def _oos_report() -> str:
    return "\n".join(
        [
            "- OOS/WF preflight status: `pass_smoke_plumbing_only`",
            "- OOS readiness: `hold`",
            "- Backtest readiness: `hold`",
            "- Order intent generated: `false`",
            "- It inherits assumption-only costs; `broker_fee_override_required=true` still blocks production interpretation.",
        ]
    )


class QuantBiasControlPreflightTest(unittest.TestCase):
    def test_builds_bias_hold_from_latest_smoke_gates(self) -> None:
        rows, summary = build_bias_checks(
            readiness_text=_readiness_report(),
            oos_text=_oos_report(),
            strategy_bias_texts=["Current Judgment: hold"],
        )
        by_id = {row.check_id: row for row in rows}

        self.assertEqual(summary["bias_control_status"], "hold")
        self.assertEqual(summary["backtest_readiness"], "hold")
        self.assertEqual(summary["live_trading_readiness"], "blocked")
        self.assertTrue(summary["broker_fee_override_required"])
        self.assertEqual(by_id["survivorship_bias"].status, "hold")
        self.assertEqual(by_id["lookahead_bias"].status, "pass_smoke")
        self.assertEqual(by_id["data_snooping"].status, "pass_smoke_plumbing_only")
        self.assertEqual(by_id["overfitting"].status, "hold")
        self.assertEqual(by_id["cost_bias"].status, "hold")
        self.assertEqual(by_id["execution_bias"].status, "blocked")
        self.assertEqual(by_id["strategy_bias_docs"].status, "hold")

    def test_rejects_reports_with_order_intents(self) -> None:
        with self.assertRaisesRegex(ValueError, "refuses reports with generated order intents"):
            build_bias_checks(readiness_text=_readiness_report().replace("`false`", "`true`", 1))

    def test_report_keeps_preflight_guardrails(self) -> None:
        rows, summary = build_bias_checks(readiness_text=_readiness_report(), oos_text=_oos_report())
        report = render_report(
            rows=rows,
            summary=summary,
            readiness_report=Path("_report/quant/research/readiness.md"),
            oos_report=Path("_report/quant/research/oos.md"),
            status_coverage_report=Path("_report/quant/research/status.md"),
            strategy_bias_reports=[Path("_report/quant/strategies/001-strategy-universe-momentum.bias-control.md")],
            csv_output=Path("_report/quant/research/bias.rows.csv"),
        )

        self.assertIn("- Bias Control status: `hold`", report)
        self.assertIn("- Backtest readiness: `hold`", report)
        self.assertIn("Bias Control preflight only", report)
        self.assertIn("| `survivorship_bias` |", report)

    def test_cli_writes_lf_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            readiness = root / "readiness.md"
            oos = root / "oos.md"
            strategy = root / "strategy.bias-control.md"
            rows_output = root / "bias.rows.csv"
            report_output = root / "bias.md"
            readiness.write_text(_readiness_report(), encoding="utf-8")
            oos.write_text(_oos_report(), encoding="utf-8")
            strategy.write_text("Current Judgment: hold\n", encoding="utf-8")

            with patch(
                "sys.argv",
                [
                    "quant_bias_control_preflight.py",
                    "--readiness-report",
                    str(readiness),
                    "--oos-walk-forward-report",
                    str(oos),
                    "--strategy-bias-report",
                    str(strategy),
                    "--csv-output",
                    str(rows_output),
                    "--report-output",
                    str(report_output),
                ],
            ):
                self.assertEqual(main(), 0)

            report_text = report_output.read_text(encoding="utf-8")
            rows_text = rows_output.read_text(encoding="utf-8-sig")
            report_bytes = report_output.read_bytes()
            rows_bytes = rows_output.read_bytes()

        self.assertIn("# Bias Control Preflight", report_text)
        self.assertIn("paper_bias_control_preflight_only", rows_text)
        self.assertIn("order_intent_generated", rows_text)
        self.assertNotIn(b"\r\n", report_bytes)
        self.assertNotIn(b"\r\n", rows_bytes)


if __name__ == "__main__":
    unittest.main()
