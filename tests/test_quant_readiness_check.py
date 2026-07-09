from __future__ import annotations

import csv
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from scripts.quant_readiness_check import evaluate_readiness, main


def _liquidity_rows(date_count: int = 20) -> list[dict[str, str]]:
    return [
        {
            "date": f"2025-01-{day:02d}",
            "code": "005930",
            "pit_liquidity_final_status": "include",
            "pit_liquidity_rows_used": "20",
        }
        for day in range(1, date_count + 1)
    ]


def _signal_rows() -> list[dict[str, str]]:
    return [
        {"date": "2025-01-20", "code": "005930", "signal_state": "BUY candidate"},
        {"date": "2025-01-20", "code": "000660", "signal_state": "SELL candidate"},
    ]


def _forward_rows() -> list[dict[str, str]]:
    return [
        {"date": "2025-01-20", "code": "005930", "horizon_trading_days": "1", "evaluation_status": "complete"},
        {"date": "2025-01-20", "code": "000660", "horizon_trading_days": "5", "evaluation_status": "missing_forward_price"},
    ]


def _portfolio_target_rows() -> list[dict[str, str]]:
    return [
        {
            "date": "2025-01-20",
            "code": "005930",
            "target_weight": "0.050000",
            "target_mode": "paper_portfolio_target_smoke_only",
            "order_intent_generated": "false",
        },
        {
            "date": "2025-01-20",
            "code": "000660",
            "target_weight": "0.050000",
            "target_mode": "paper_portfolio_target_smoke_only",
            "order_intent_generated": "false",
        },
    ]


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


class QuantReadinessCheckTest(unittest.TestCase):
    def test_smoke_artifacts_do_not_upgrade_backtest_or_live_readiness(self) -> None:
        gates, summary = evaluate_readiness(
            liquidity_rows=_liquidity_rows(),
            signal_rows=_signal_rows(),
            kis_preflight_report=None,
            status_coverage="current_snapshot_smoke",
        )
        by_name = {gate.name: gate for gate in gates}

        self.assertEqual(summary["backtest_readiness"], "hold")
        self.assertEqual(summary["live_trading_readiness"], "blocked")
        self.assertEqual(by_name["market_data_window"].status, "pass")
        self.assertEqual(by_name["liquidity_filter"].status, "pass_smoke")
        self.assertEqual(by_name["signal_candidates"].status, "pass_smoke")
        self.assertEqual(by_name["point_in_time_status_coverage"].status, "hold")
        self.assertEqual(by_name["backtest_engine"].status, "hold")
        self.assertEqual(by_name["live_trading_controls"].status, "blocked")
        self.assertEqual(by_name["kis_demo_account"].status, "blocked")

    def test_forward_return_smoke_is_a_diagnostic_gate_only(self) -> None:
        gates, summary = evaluate_readiness(
            liquidity_rows=_liquidity_rows(),
            signal_rows=_signal_rows(),
            forward_return_rows=_forward_rows(),
            kis_preflight_report=None,
            status_coverage="current_snapshot_smoke",
        )
        by_name = {gate.name: gate for gate in gates}

        self.assertEqual(by_name["forward_return_smoke"].status, "pass_smoke")
        self.assertEqual(summary["forward_return_rows"], 2)
        self.assertEqual(summary["forward_return_complete_rows"], 1)
        self.assertEqual(summary["backtest_readiness"], "hold")
        self.assertEqual(summary["live_trading_readiness"], "blocked")

    def test_portfolio_targets_smoke_is_diagnostic_only(self) -> None:
        gates, summary = evaluate_readiness(
            liquidity_rows=_liquidity_rows(),
            signal_rows=_signal_rows(),
            forward_return_rows=_forward_rows(),
            portfolio_target_rows=_portfolio_target_rows(),
            kis_preflight_report=None,
            status_coverage="current_snapshot_smoke",
        )
        by_name = {gate.name: gate for gate in gates}

        self.assertEqual(by_name["portfolio_targets_smoke"].status, "pass_smoke")
        self.assertEqual(summary["portfolio_target_rows"], 2)
        self.assertEqual(summary["portfolio_target_dates"], 1)
        self.assertEqual(summary["portfolio_target_max_gross_weight"], 0.1)
        self.assertEqual(summary["backtest_readiness"], "hold")
        self.assertEqual(summary["live_trading_readiness"], "blocked")

    def test_portfolio_targets_with_order_intents_do_not_pass(self) -> None:
        rows = [dict(row) for row in _portfolio_target_rows()]
        rows[0]["order_intent_generated"] = "true"

        gates, _summary = evaluate_readiness(
            liquidity_rows=_liquidity_rows(),
            signal_rows=_signal_rows(),
            portfolio_target_rows=rows,
            kis_preflight_report=None,
            status_coverage="current_snapshot_smoke",
        )

        self.assertEqual({gate.name: gate for gate in gates}["portfolio_targets_smoke"].status, "hold")

    def test_backtest_contract_report_is_smoke_gate_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            report = Path(tmp) / "contract.md"
            report.write_text(
                "\n".join(
                    [
                        "- Contract status: `pass_smoke`",
                        "- Order intent generated: `false`",
                    ]
                ),
                encoding="utf-8",
            )
            gates, summary = evaluate_readiness(
                liquidity_rows=_liquidity_rows(),
                signal_rows=_signal_rows(),
                portfolio_target_rows=_portfolio_target_rows(),
                backtest_contract_report=report,
                kis_preflight_report=None,
                status_coverage="current_snapshot_smoke",
            )
        by_name = {gate.name: gate for gate in gates}

        self.assertEqual(by_name["backtest_input_contract"].status, "pass_smoke")
        self.assertTrue(summary["backtest_contract_report_supplied"])
        self.assertEqual(summary["backtest_readiness"], "hold")
        self.assertEqual(summary["live_trading_readiness"], "blocked")

    def test_backtest_contract_report_hold_when_not_pass_smoke(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            report = Path(tmp) / "contract.md"
            report.write_text("- Contract status: `hold`\n", encoding="utf-8")
            gates, _summary = evaluate_readiness(
                liquidity_rows=_liquidity_rows(),
                signal_rows=_signal_rows(),
                backtest_contract_report=report,
                kis_preflight_report=None,
            )

        self.assertEqual({gate.name: gate for gate in gates}["backtest_input_contract"].status, "hold")

    def test_backtest_pnl_smoke_report_is_diagnostic_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            report = Path(tmp) / "pnl.md"
            report.write_text(
                "\n".join(
                    [
                        "- PnL smoke status: `pass_smoke`",
                        "- Order intent generated: `false`",
                    ]
                ),
                encoding="utf-8",
            )
            gates, summary = evaluate_readiness(
                liquidity_rows=_liquidity_rows(),
                signal_rows=_signal_rows(),
                portfolio_target_rows=_portfolio_target_rows(),
                backtest_pnl_report=report,
                kis_preflight_report=None,
                status_coverage="current_snapshot_smoke",
            )
        by_name = {gate.name: gate for gate in gates}

        self.assertEqual(by_name["backtest_pnl_smoke"].status, "pass_smoke")
        self.assertTrue(summary["backtest_pnl_report_supplied"])
        self.assertEqual(summary["backtest_readiness"], "hold")
        self.assertEqual(summary["live_trading_readiness"], "blocked")

    def test_backtest_assumptions_report_is_assumption_only_gate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            report = Path(tmp) / "assumptions.md"
            report.write_text(
                "\n".join(
                    [
                        "- Assumption status: `pass_assumption_only`",
                        "- Order intent generated: `false`",
                    ]
                ),
                encoding="utf-8",
            )
            gates, summary = evaluate_readiness(
                liquidity_rows=_liquidity_rows(),
                signal_rows=_signal_rows(),
                backtest_assumptions_report=report,
                kis_preflight_report=None,
                status_coverage="current_snapshot_smoke",
            )
        by_name = {gate.name: gate for gate in gates}

        self.assertEqual(by_name["backtest_assumptions"].status, "pass_assumption_only")
        self.assertTrue(summary["backtest_assumptions_report_supplied"])
        self.assertEqual(summary["backtest_readiness"], "hold")
        self.assertEqual(summary["live_trading_readiness"], "blocked")

    def test_benchmark_returns_report_is_smoke_gate_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            report = Path(tmp) / "benchmark.md"
            report.write_text(
                "\n".join(
                    [
                        "- Mode: `paper_benchmark_return_smoke_only`",
                        "- Order intent generated: `false`",
                        "- Backtest readiness: `hold`",
                    ]
                ),
                encoding="utf-8",
            )
            gates, summary = evaluate_readiness(
                liquidity_rows=_liquidity_rows(),
                signal_rows=_signal_rows(),
                benchmark_returns_report=report,
                kis_preflight_report=None,
                status_coverage="current_snapshot_smoke",
            )
        by_name = {gate.name: gate for gate in gates}

        self.assertEqual(by_name["benchmark_returns_smoke"].status, "pass_smoke")
        self.assertTrue(summary["benchmark_returns_report_supplied"])
        self.assertEqual(summary["backtest_readiness"], "hold")
        self.assertEqual(summary["live_trading_readiness"], "blocked")

    def test_backtest_attribution_report_is_assumption_only_gate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            report = Path(tmp) / "attribution.md"
            report.write_text(
                "\n".join(
                    [
                        "- Attribution status: `pass_smoke_assumption_only`",
                        "- Backtest readiness: `hold`",
                        "- Order intent generated: `false`",
                        "- Costs use local assumption rows only; `broker_fee_override_required=true` means actual KIS account/channel fees are still missing.",
                    ]
                ),
                encoding="utf-8",
            )
            gates, summary = evaluate_readiness(
                liquidity_rows=_liquidity_rows(),
                signal_rows=_signal_rows(),
                backtest_attribution_report=report,
                kis_preflight_report=None,
                status_coverage="current_snapshot_smoke",
            )
        by_name = {gate.name: gate for gate in gates}

        self.assertEqual(by_name["backtest_attribution_smoke"].status, "pass_smoke_assumption_only")
        self.assertIn("broker fee override still required", by_name["backtest_attribution_smoke"].evidence)
        self.assertTrue(summary["backtest_attribution_report_supplied"])
        self.assertEqual(summary["backtest_readiness"], "hold")
        self.assertEqual(summary["live_trading_readiness"], "blocked")

    def test_oos_walk_forward_report_is_preflight_only_gate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            report = Path(tmp) / "oos.md"
            report.write_text(
                "\n".join(
                    [
                        "- OOS/WF preflight status: `pass_smoke_plumbing_only`",
                        "- OOS readiness: `hold`",
                        "- Backtest readiness: `hold`",
                        "- Order intent generated: `false`",
                        "- It inherits assumption-only costs; `broker_fee_override_required=true` still blocks production interpretation.",
                    ]
                ),
                encoding="utf-8",
            )
            gates, summary = evaluate_readiness(
                liquidity_rows=_liquidity_rows(),
                signal_rows=_signal_rows(),
                oos_walk_forward_report=report,
                kis_preflight_report=None,
                status_coverage="current_snapshot_smoke",
            )
        by_name = {gate.name: gate for gate in gates}

        self.assertEqual(by_name["oos_walk_forward_preflight"].status, "pass_smoke_plumbing_only")
        self.assertIn("broker fee override still required", by_name["oos_walk_forward_preflight"].evidence)
        self.assertTrue(summary["oos_walk_forward_report_supplied"])
        self.assertEqual(summary["backtest_readiness"], "hold")
        self.assertEqual(summary["live_trading_readiness"], "blocked")

    def test_bias_control_report_keeps_readiness_hold(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            report = Path(tmp) / "bias.md"
            report.write_text(
                "\n".join(
                    [
                        "- Bias Control status: `hold`",
                        "- Backtest readiness: `hold`",
                        "- Order intent generated: `false`",
                    ]
                ),
                encoding="utf-8",
            )
            gates, summary = evaluate_readiness(
                liquidity_rows=_liquidity_rows(),
                signal_rows=_signal_rows(),
                bias_control_report=report,
                kis_preflight_report=None,
                status_coverage="current_snapshot_smoke",
            )
        by_name = {gate.name: gate for gate in gates}

        self.assertEqual(by_name["bias_control_preflight"].status, "hold")
        self.assertIn("correctly keeps Bias Control at hold", by_name["bias_control_preflight"].evidence)
        self.assertTrue(summary["bias_control_report_supplied"])
        self.assertEqual(summary["backtest_readiness"], "hold")
        self.assertEqual(summary["live_trading_readiness"], "blocked")

    def test_status_evidence_collection_plan_is_plan_only_gate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            report = Path(tmp) / "status-evidence-plan.md"
            report.write_text(
                "\n".join(
                    [
                        "# Point-in-Time Status Evidence Collection Plan",
                        "- Order intent generated: `false`",
                        "- Backtest readiness impact: `hold`",
                        "| Metric | Value |",
                        "| --- | ---: |",
                        "| Collection plan rows | 361 |",
                        "| Blocker | Count |",
                        "| --- | ---: |",
                        "| `source_manifest_evidence` | 10 |",
                        "| `release_resume_evidence` | 304 |",
                        "| `market_label_resolution` | 47 |",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            gates, summary = evaluate_readiness(
                liquidity_rows=_liquidity_rows(),
                signal_rows=_signal_rows(),
                status_evidence_collection_plan_report=report,
                kis_preflight_report=None,
                status_coverage="current_snapshot_smoke",
            )
        by_name = {gate.name: gate for gate in gates}

        self.assertEqual(by_name["point_in_time_status_evidence_collection_plan"].status, "plan_only")
        self.assertIn("361 pending evidence rows", by_name["point_in_time_status_evidence_collection_plan"].evidence)
        self.assertIn("release_resume_evidence=304", by_name["point_in_time_status_evidence_collection_plan"].evidence)
        self.assertTrue(summary["status_evidence_collection_plan_report_supplied"])
        self.assertEqual(summary["backtest_readiness"], "hold")
        self.assertEqual(summary["live_trading_readiness"], "blocked")

    def test_status_evidence_collection_queue_is_plan_only_gate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            report = Path(tmp) / "status-evidence-queue.md"
            report.write_text(
                "\n".join(
                    [
                        "# Point-in-Time Status Evidence Collection Queue",
                        "- Order intent generated: `false`",
                        "- Backtest readiness impact: `hold`",
                        "| Metric | Value |",
                        "| --- | ---: |",
                        "| Queue batches | 33 |",
                        "| Queued source rows | 385 |",
                        "| Priority | Batches |",
                        "| --- | ---: |",
                        "| `1` | 10 |",
                        "| `2` | 18 |",
                        "| `3` | 5 |",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            gates, summary = evaluate_readiness(
                liquidity_rows=_liquidity_rows(),
                signal_rows=_signal_rows(),
                status_evidence_collection_queue_report=report,
                kis_preflight_report=None,
                status_coverage="current_snapshot_smoke",
            )
        by_name = {gate.name: gate for gate in gates}

        self.assertEqual(by_name["point_in_time_status_evidence_collection_queue"].status, "plan_only")
        self.assertIn("33 batches", by_name["point_in_time_status_evidence_collection_queue"].evidence)
        self.assertIn("385 queued source rows", by_name["point_in_time_status_evidence_collection_queue"].evidence)
        self.assertIn("P2=18", by_name["point_in_time_status_evidence_collection_queue"].evidence)
        self.assertTrue(summary["status_evidence_collection_queue_report_supplied"])
        self.assertEqual(summary["backtest_readiness"], "hold")
        self.assertEqual(summary["live_trading_readiness"], "blocked")

    def test_historical_status_gate_still_does_not_authorize_trading(self) -> None:
        gates, summary = evaluate_readiness(
            liquidity_rows=_liquidity_rows(),
            signal_rows=_signal_rows(),
            kis_preflight_report=None,
            status_coverage="historical_complete",
        )
        by_name = {gate.name: gate for gate in gates}

        self.assertEqual(by_name["point_in_time_status_coverage"].status, "pass")
        self.assertEqual(summary["backtest_readiness"], "hold")
        self.assertEqual(summary["live_trading_readiness"], "blocked")

    def test_status_coverage_audit_report_can_hold_gate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            report = Path(tmp) / "status-coverage.md"
            lifecycle_report = Path(tmp) / "status-lifecycle-gaps.md"
            report.write_text(
                "\n".join(
                    [
                        "- Coverage status: `hold`",
                        "| Source coverage manifest validation | `not_supplied` |",
                        "| Source coverage missing status types | `managed_issue,trading_halt` |",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            lifecycle_report.write_text(
                "\n".join(
                    [
                        "| Missing release/resume groups | 3 |",
                        "| Status type | Missing release/resume | Active after latest release | Has release/resume | Release without active |",
                        "| --- | ---: | ---: | ---: | ---: |",
                        "| `managed_issue` | 2 | 0 | 0 | 0 |",
                        "| `trading_halt` | 1 | 0 | 0 | 0 |",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            gates, summary = evaluate_readiness(
                liquidity_rows=_liquidity_rows(),
                signal_rows=_signal_rows(),
                status_coverage_report=report,
                status_lifecycle_gap_report=lifecycle_report,
                kis_preflight_report=None,
                status_coverage="current_snapshot_smoke",
            )
        by_name = {gate.name: gate for gate in gates}

        self.assertEqual(by_name["point_in_time_status_coverage"].status, "hold")
        self.assertIn("coverage audit reports hold", by_name["point_in_time_status_coverage"].evidence)
        self.assertIn("source manifest validation=not_supplied", by_name["point_in_time_status_coverage"].evidence)
        self.assertIn("missing source coverage=managed_issue,trading_halt", by_name["point_in_time_status_coverage"].evidence)
        self.assertIn("lifecycle missing release/resume groups=3", by_name["point_in_time_status_coverage"].evidence)
        self.assertIn("lifecycle missing by status=managed_issue=2,trading_halt=1", by_name["point_in_time_status_coverage"].evidence)
        self.assertTrue(summary["status_coverage_report_supplied"])
        self.assertTrue(summary["status_lifecycle_gap_report_supplied"])

    def test_kis_paper_stock_gap_is_reported_without_account_value(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            preflight = Path(tmp) / "kis-preflight.md"
            preflight.write_text(
                "\n".join(
                    [
                        "- Ready for read-only demo account calls: `false`",
                        "| `demo_stock_account` | `fail` | `KIS_PAPER_STOCK` | configured value is empty |",
                    ]
                ),
                encoding="utf-8",
            )
            gates, _summary = evaluate_readiness(
                liquidity_rows=_liquidity_rows(),
                signal_rows=_signal_rows(),
                kis_preflight_report=preflight,
            )

        gate = {gate.name: gate for gate in gates}["kis_demo_account"]
        self.assertEqual(gate.status, "blocked")
        self.assertIn("KIS_PAPER_STOCK", gate.evidence)
        self.assertIn("fill KIS_PAPER_STOCK", gate.next_action)

    def test_cli_writes_markdown_report_from_local_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            liquidity = root / "liquidity.rows.csv"
            signals = root / "signals.rows.csv"
            forward_returns = root / "forward.rows.csv"
            portfolio_targets = root / "portfolio-targets.rows.csv"
            contract_report = root / "contract.md"
            pnl_report = root / "pnl.md"
            assumptions_report = root / "assumptions.md"
            benchmark_report = root / "benchmark.md"
            attribution_report = root / "attribution.md"
            oos_report = root / "oos.md"
            bias_report = root / "bias.md"
            status_coverage_report = root / "status-coverage.md"
            status_lifecycle_gap_report = root / "status-lifecycle-gaps.md"
            status_evidence_collection_plan_report = root / "status-evidence-plan.md"
            status_evidence_collection_queue_report = root / "status-evidence-queue.md"
            output = root / "readiness.md"
            _write_csv(liquidity, _liquidity_rows())
            _write_csv(signals, _signal_rows())
            _write_csv(forward_returns, _forward_rows())
            _write_csv(portfolio_targets, _portfolio_target_rows())
            contract_report.write_text(
                "- Contract status: `pass_smoke`\n- Order intent generated: `false`\n",
                encoding="utf-8",
            )
            pnl_report.write_text(
                "- PnL smoke status: `pass_smoke`\n- Order intent generated: `false`\n",
                encoding="utf-8",
            )
            assumptions_report.write_text(
                "- Assumption status: `pass_assumption_only`\n- Order intent generated: `false`\n",
                encoding="utf-8",
            )
            benchmark_report.write_text(
                "- Mode: `paper_benchmark_return_smoke_only`\n- Order intent generated: `false`\n- Backtest readiness: `hold`\n",
                encoding="utf-8",
            )
            attribution_report.write_text(
                "- Attribution status: `pass_smoke_assumption_only`\n- Order intent generated: `false`\n- Backtest readiness: `hold`\n",
                encoding="utf-8",
            )
            oos_report.write_text(
                "- OOS/WF preflight status: `pass_smoke_plumbing_only`\n- OOS readiness: `hold`\n- Order intent generated: `false`\n- Backtest readiness: `hold`\n",
                encoding="utf-8",
            )
            bias_report.write_text(
                "- Bias Control status: `hold`\n- Backtest readiness: `hold`\n- Order intent generated: `false`\n",
                encoding="utf-8",
            )
            status_coverage_report.write_text("- Coverage status: `hold`\n", encoding="utf-8")
            status_lifecycle_gap_report.write_text("| Missing release/resume groups | 3 |\n", encoding="utf-8")
            status_evidence_collection_plan_report.write_text(
                "# Point-in-Time Status Evidence Collection Plan\n"
                "- Order intent generated: `false`\n"
                "- Backtest readiness impact: `hold`\n"
                "| Collection plan rows | 361 |\n",
                encoding="utf-8",
            )
            status_evidence_collection_queue_report.write_text(
                "# Point-in-Time Status Evidence Collection Queue\n"
                "- Order intent generated: `false`\n"
                "- Backtest readiness impact: `hold`\n"
                "| Queue batches | 33 |\n"
                "| Queued source rows | 361 |\n",
                encoding="utf-8",
            )

            with patch(
                "sys.argv",
                [
                    "quant_readiness_check.py",
                    "--liquidity-input",
                    str(liquidity),
                    "--signals-input",
                    str(signals),
                    "--forward-returns-input",
                    str(forward_returns),
                    "--portfolio-targets-input",
                    str(portfolio_targets),
                    "--backtest-contract-report",
                    str(contract_report),
                    "--backtest-pnl-report",
                    str(pnl_report),
                    "--backtest-assumptions-report",
                    str(assumptions_report),
                    "--benchmark-returns-report",
                    str(benchmark_report),
                    "--backtest-attribution-report",
                    str(attribution_report),
                    "--oos-walk-forward-report",
                    str(oos_report),
                    "--bias-control-report",
                    str(bias_report),
                    "--status-coverage-report",
                    str(status_coverage_report),
                    "--status-lifecycle-gap-report",
                    str(status_lifecycle_gap_report),
                    "--status-evidence-collection-plan-report",
                    str(status_evidence_collection_plan_report),
                    "--status-evidence-collection-queue-report",
                    str(status_evidence_collection_queue_report),
                    "--report-output",
                    str(output),
                ],
            ):
                self.assertEqual(main(), 0)

            report = output.read_text(encoding="utf-8")
            report_bytes = output.read_bytes()

        self.assertIn("- KIS API call: `false`", report)
        self.assertIn("- Order intent generated: `false`", report)
        self.assertIn("- Backtest readiness: `hold`", report)
        self.assertIn("- Live trading readiness: `blocked`", report)
        self.assertIn("| `signal_candidates` | `pass_smoke` |", report)
        self.assertIn("| `forward_return_smoke` | `pass_smoke` |", report)
        self.assertIn("| `portfolio_targets_smoke` | `pass_smoke` |", report)
        self.assertIn("| `backtest_input_contract` | `pass_smoke` |", report)
        self.assertIn("| `backtest_pnl_smoke` | `pass_smoke` |", report)
        self.assertIn("| `backtest_assumptions` | `pass_assumption_only` |", report)
        self.assertIn("| `benchmark_returns_smoke` | `pass_smoke` |", report)
        self.assertIn("| `backtest_attribution_smoke` | `pass_smoke_assumption_only` |", report)
        self.assertIn("| `oos_walk_forward_preflight` | `pass_smoke_plumbing_only` |", report)
        self.assertIn("| `bias_control_preflight` | `hold` |", report)
        self.assertIn("| `point_in_time_status_evidence_collection_plan` | `plan_only` |", report)
        self.assertIn("| `point_in_time_status_evidence_collection_queue` | `plan_only` |", report)
        self.assertIn("| `point_in_time_status_coverage` | `hold` |", report)
        self.assertIn("- Backtest assumptions report: [[", report)
        self.assertIn("- Benchmark returns report: [[", report)
        self.assertIn("- Backtest attribution smoke report: [[", report)
        self.assertIn("- OOS/Walk-Forward preflight report: [[", report)
        self.assertIn("- Bias Control preflight report: [[", report)
        self.assertIn("- Status coverage audit report: [[", report)
        self.assertIn("- Status lifecycle gap report: [[", report)
        self.assertIn("- Status evidence collection plan report: [[", report)
        self.assertIn("- Status evidence collection queue report: [[", report)
        self.assertIn("lifecycle missing release/resume groups=3", report)
        self.assertIn("| Forward-return complete rows | 1 |", report)
        self.assertIn("| Portfolio target rows | 2 |", report)
        self.assertNotIn(b"\r\n", report_bytes)

    def test_positive_thresholds_are_required(self) -> None:
        with self.assertRaisesRegex(ValueError, "min_market_dates must be positive"):
            evaluate_readiness(
                liquidity_rows=_liquidity_rows(),
                signal_rows=_signal_rows(),
                kis_preflight_report=None,
                min_market_dates=0,
            )
        with self.assertRaisesRegex(ValueError, "min_liquidity_lookback must be positive"):
            evaluate_readiness(
                liquidity_rows=_liquidity_rows(),
                signal_rows=_signal_rows(),
                kis_preflight_report=None,
                min_liquidity_lookback=0,
            )


if __name__ == "__main__":
    unittest.main()
