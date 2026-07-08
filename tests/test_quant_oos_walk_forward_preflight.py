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

from scripts.quant_oos_walk_forward_preflight import build_walk_forward_rows, main, render_report


ATTRIBUTION_FIELDS = (
    "date",
    "horizon_trading_days",
    "attribution_status",
    "baseline_net_return_pct",
    "stress_net_return_pct",
    "baseline_active_return_pct",
    "broker_fee_override_required",
    "attribution_mode",
    "order_intent_generated",
)


def _attribution_row(day: int, *, baseline: float | None = None) -> dict[str, str]:
    value = float(day if baseline is None else baseline)
    return {
        "date": f"2025-01-{day:02d}",
        "horizon_trading_days": "1",
        "attribution_status": "pass_smoke_assumption_only",
        "baseline_net_return_pct": f"{value:.4f}",
        "stress_net_return_pct": f"{value - 0.5:.4f}",
        "baseline_active_return_pct": f"{value - 1.0:.4f}",
        "broker_fee_override_required": "true",
        "attribution_mode": "paper_backtest_attribution_smoke_assumption_only",
        "order_intent_generated": "false",
    }


def _rows(count: int) -> list[dict[str, str]]:
    return [_attribution_row(day) for day in range(1, count + 1)]


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=ATTRIBUTION_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


class QuantOosWalkForwardPreflightTest(unittest.TestCase):
    def test_builds_expanding_walk_forward_folds_without_readiness_upgrade(self) -> None:
        fold_rows, summary = build_walk_forward_rows(
            attribution_rows=_rows(30),
            min_train_dates=10,
            test_dates=5,
            fold_count=3,
        )

        self.assertEqual(summary["oos_walk_forward_status"], "pass_smoke_plumbing_only")
        self.assertEqual(summary["oos_readiness"], "hold")
        self.assertEqual(summary["backtest_readiness"], "hold")
        self.assertEqual(summary["live_trading_readiness"], "blocked")
        self.assertEqual(len(fold_rows), 3)
        self.assertEqual(fold_rows[0].fold_id, "wf_01")
        self.assertEqual(fold_rows[0].train_start_date, "2025-01-01")
        self.assertEqual(fold_rows[0].train_end_date, "2025-01-10")
        self.assertEqual(fold_rows[0].test_start_date, "2025-01-11")
        self.assertEqual(fold_rows[0].test_end_date, "2025-01-15")
        self.assertAlmostEqual(fold_rows[0].train_avg_baseline_net_return_pct or 0, 5.5)
        self.assertAlmostEqual(fold_rows[0].test_avg_baseline_net_return_pct or 0, 13.0)
        self.assertIn("broker_fee_override_required", fold_rows[0].notes)
        self.assertIn("production_backtest_not_wired", fold_rows[0].notes)

    def test_not_enough_dates_keeps_preflight_hold(self) -> None:
        fold_rows, summary = build_walk_forward_rows(
            attribution_rows=_rows(12),
            min_train_dates=10,
            test_dates=5,
            fold_count=1,
        )

        self.assertEqual(fold_rows, [])
        self.assertEqual(summary["oos_walk_forward_status"], "hold")
        self.assertIn("horizon_1:not_enough_dates:12<15", summary["hold_reasons"])

    def test_rejects_order_intents_and_unexpected_attribution_mode(self) -> None:
        rows = _rows(20)
        rows[0]["order_intent_generated"] = "true"
        with self.assertRaisesRegex(ValueError, "must not contain order intents"):
            build_walk_forward_rows(attribution_rows=rows)

        rows = _rows(20)
        rows[0]["attribution_mode"] = "unexpected"
        with self.assertRaisesRegex(ValueError, "unexpected attribution modes"):
            build_walk_forward_rows(attribution_rows=rows)

    def test_report_keeps_preflight_guardrails(self) -> None:
        fold_rows, summary = build_walk_forward_rows(
            attribution_rows=_rows(20),
            min_train_dates=10,
            test_dates=5,
            fold_count=1,
        )
        report = render_report(
            rows=fold_rows,
            summary=summary,
            attribution_input=Path("_report/quant/research/attribution.rows.csv"),
            csv_output=Path("_report/quant/research/oos.folds.csv"),
        )

        self.assertIn("- OOS/WF preflight status: `pass_smoke_plumbing_only`", report)
        self.assertIn("- OOS readiness: `hold`", report)
        self.assertIn("not an OOS or production `Backtest` result", report)
        self.assertIn("broker_fee_override_required=true", report)

    def test_cli_writes_lf_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            attribution = root / "attribution.rows.csv"
            folds = root / "oos.folds.csv"
            report = root / "oos.md"
            _write_csv(attribution, _rows(20))

            with patch(
                "sys.argv",
                [
                    "quant_oos_walk_forward_preflight.py",
                    "--attribution-input",
                    str(attribution),
                    "--csv-output",
                    str(folds),
                    "--report-output",
                    str(report),
                    "--min-train-dates",
                    "10",
                    "--test-dates",
                    "5",
                    "--fold-count",
                    "1",
                ],
            ):
                self.assertEqual(main(), 0)

            report_text = report.read_text(encoding="utf-8")
            folds_text = folds.read_text(encoding="utf-8-sig")
            report_bytes = report.read_bytes()
            folds_bytes = folds.read_bytes()

        self.assertIn("# OOS Walk-Forward Preflight", report_text)
        self.assertIn("paper_oos_walk_forward_preflight_smoke_only", folds_text)
        self.assertIn("test_avg_baseline_net_return_pct", folds_text)
        self.assertNotIn(b"\r\n", report_bytes)
        self.assertNotIn(b"\r\n", folds_bytes)


if __name__ == "__main__":
    unittest.main()
