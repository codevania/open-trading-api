from __future__ import annotations

import csv
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from scripts.quant_backtest_attribution_smoke import build_attribution_rows, main, render_report


PNL_FIELDS = (
    "date",
    "code",
    "stock_name",
    "market",
    "horizon_trading_days",
    "evaluation_status",
    "forward_date",
    "target_side",
    "target_weight",
    "raw_forward_return_pct",
    "weighted_return_contribution_pct",
    "benchmark_label",
    "benchmark_join_status",
    "benchmark_return_pct",
    "excess_return_pct",
    "weighted_excess_return_contribution_pct",
    "source_signal_state",
    "target_mode",
    "pnl_mode",
    "order_intent_generated",
)


def _assumptions() -> dict[str, object]:
    return {
        "cost_model": {
            "currency": "KRW",
            "commission_bps_per_side": {"baseline": 1.5, "stress": 5.0, "needs_broker_override": True},
            "markets": {
                "KOSPI": {"baseline_round_trip_bps": 33.0, "stress_round_trip_bps": 70.0},
                "KOSDAQ": {"baseline_round_trip_bps": 33.0, "stress_round_trip_bps": 70.0},
            },
        },
        "benchmark": {"primary": "KOSPI", "required_for_backtest": True},
    }


def _pnl_row(
    code: str,
    *,
    market: str = "KOSPI",
    target_weight: str = "0.500000",
    contribution: str = "5.0000",
    status: str = "complete",
    benchmark_status: str = "complete",
) -> dict[str, str]:
    return {
        "date": "2025-02-05",
        "code": code,
        "stock_name": "Fixture",
        "market": market,
        "horizon_trading_days": "1",
        "evaluation_status": status,
        "forward_date": "2025-02-06" if status == "complete" else "",
        "target_side": "LONG",
        "target_weight": target_weight,
        "raw_forward_return_pct": "10.0000" if status == "complete" else "",
        "weighted_return_contribution_pct": contribution if status == "complete" else "",
        "benchmark_label": "KOSPI",
        "benchmark_join_status": benchmark_status,
        "benchmark_return_pct": "2.0000" if benchmark_status == "complete" else "",
        "excess_return_pct": "8.0000" if status == "complete" and benchmark_status == "complete" else "",
        "weighted_excess_return_contribution_pct": "4.0000"
        if status == "complete" and benchmark_status == "complete"
        else "",
        "source_signal_state": "BUY candidate",
        "target_mode": "paper_portfolio_target_smoke_only",
        "pnl_mode": "paper_backtest_pnl_smoke_only",
        "order_intent_generated": "false",
    }


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=PNL_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _write_yaml(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")


class QuantBacktestAttributionSmokeTest(unittest.TestCase):
    def test_aggregates_cost_net_and_active_return_without_readiness_upgrade(self) -> None:
        pnl_rows = [
            _pnl_row("005930", target_weight="0.500000", contribution="5.0000"),
            _pnl_row("000660", target_weight="0.250000", contribution="1.0000"),
        ]

        rows, summary = build_attribution_rows(pnl_rows=pnl_rows, assumptions=_assumptions())

        self.assertEqual(summary["attribution_status"], "pass_smoke_assumption_only")
        self.assertEqual(summary["backtest_readiness"], "hold")
        self.assertEqual(summary["live_trading_readiness"], "blocked")
        self.assertEqual(len(rows), 1)
        row = rows[0]
        self.assertAlmostEqual(row.gross_target_weight, 0.75)
        self.assertAlmostEqual(row.cash_weight, 0.25)
        self.assertAlmostEqual(row.gross_return_pct, 6.0)
        self.assertAlmostEqual(row.baseline_cost_pct, 0.2475)
        self.assertAlmostEqual(row.baseline_net_return_pct, 5.7525)
        self.assertAlmostEqual(row.benchmark_return_pct or 0, 2.0)
        self.assertAlmostEqual(row.baseline_active_return_pct or 0, 3.7525)
        self.assertAlmostEqual(row.cash_drag_vs_benchmark_pct or 0, -0.5)
        self.assertIn("broker_fee_override_required", row.notes)

    def test_missing_cost_assumption_holds_row(self) -> None:
        pnl_rows = [_pnl_row("005930", market="KONEX")]

        rows, summary = build_attribution_rows(pnl_rows=pnl_rows, assumptions=_assumptions())

        self.assertEqual(summary["attribution_status"], "hold")
        self.assertEqual(rows[0].attribution_status, "hold")
        self.assertIn("missing_market_cost_assumptions:KONEX", rows[0].notes)

    def test_rejects_order_intents_and_unexpected_pnl_mode(self) -> None:
        rows = [_pnl_row("005930")]
        rows[0]["order_intent_generated"] = "true"
        with self.assertRaisesRegex(ValueError, "must not contain order intents"):
            build_attribution_rows(pnl_rows=rows, assumptions=_assumptions())

        rows = [_pnl_row("005930")]
        rows[0]["pnl_mode"] = "unexpected"
        with self.assertRaisesRegex(ValueError, "unexpected PnL modes"):
            build_attribution_rows(pnl_rows=rows, assumptions=_assumptions())

    def test_report_keeps_smoke_guardrails(self) -> None:
        rows, summary = build_attribution_rows(pnl_rows=[_pnl_row("005930")], assumptions=_assumptions())
        report = render_report(
            rows=rows,
            summary=summary,
            pnl_input=Path("_report/quant/research/pnl.rows.csv"),
            assumptions_input=Path("_report/quant/data/backtest_cost_benchmark_assumptions.yaml"),
            csv_output=Path("_report/quant/research/attribution.rows.csv"),
        )

        self.assertIn("- Attribution status: `pass_smoke_assumption_only`", report)
        self.assertIn("- Backtest readiness: `hold`", report)
        self.assertIn("not a production `Backtest` result", report)
        self.assertIn("broker_fee_override_required=true", report)

    def test_cli_writes_lf_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            pnl = root / "pnl.rows.csv"
            assumptions = root / "assumptions.yaml"
            rows_output = root / "attribution.rows.csv"
            report_output = root / "attribution.md"
            _write_csv(pnl, [_pnl_row("005930")])
            _write_yaml(assumptions, _assumptions())

            with patch(
                "sys.argv",
                [
                    "quant_backtest_attribution_smoke.py",
                    "--pnl-input",
                    str(pnl),
                    "--assumptions",
                    str(assumptions),
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

        self.assertIn("# Backtest Attribution Smoke", report_text)
        self.assertIn("baseline_net_return_pct", rows_text)
        self.assertIn("paper_backtest_attribution_smoke_assumption_only", rows_text)
        self.assertNotIn(b"\r\n", report_bytes)
        self.assertNotIn(b"\r\n", rows_bytes)


if __name__ == "__main__":
    unittest.main()
