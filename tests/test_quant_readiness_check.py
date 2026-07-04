from __future__ import annotations

import csv
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

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
            output = root / "readiness.md"
            _write_csv(liquidity, _liquidity_rows())
            _write_csv(signals, _signal_rows())
            _write_csv(forward_returns, _forward_rows())
            _write_csv(portfolio_targets, _portfolio_target_rows())

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
