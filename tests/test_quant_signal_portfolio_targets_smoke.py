from __future__ import annotations

import csv
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.quant_signal_portfolio_targets_smoke import generate_portfolio_targets, main, render_report, summarize


def _signal_rows() -> list[dict[str, str]]:
    return [
        {
            "date": "2025-02-05",
            "code": "005930",
            "stock_name": "Samsung Electronics",
            "market": "KOSPI",
            "close": "70000",
            "signal_state": "BUY candidate",
            "roc_pct": "10.0",
            "rank_in_date_state": "2",
            "source_strategy": "001-strategy-universe-momentum",
            "signal_mode": "paper_signal_candidate_only",
        },
        {
            "date": "2025-02-05",
            "code": "000660",
            "stock_name": "SK hynix",
            "market": "KOSPI",
            "close": "120000",
            "signal_state": "BUY candidate",
            "roc_pct": "15.0",
            "rank_in_date_state": "1",
            "source_strategy": "001-strategy-universe-momentum",
            "signal_mode": "paper_signal_candidate_only",
        },
        {
            "date": "2025-02-05",
            "code": "035420",
            "stock_name": "NAVER",
            "market": "KOSPI",
            "close": "200000",
            "signal_state": "SELL candidate",
            "roc_pct": "-5.0",
            "rank_in_date_state": "1",
            "source_strategy": "001-strategy-universe-momentum",
            "signal_mode": "paper_signal_candidate_only",
        },
        {
            "date": "2025-02-06",
            "code": "005930",
            "stock_name": "Samsung Electronics",
            "market": "KOSPI",
            "close": "71000",
            "signal_state": "BUY candidate",
            "roc_pct": "8.0",
            "rank_in_date_state": "1",
            "source_strategy": "001-strategy-universe-momentum",
            "signal_mode": "paper_signal_candidate_only",
        },
    ]


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


class QuantSignalPortfolioTargetsSmokeTest(unittest.TestCase):
    def test_long_only_targets_use_buy_candidates_only(self) -> None:
        targets, diagnostics = generate_portfolio_targets(
            _signal_rows(),
            max_positions=10,
            max_position_weight=0.25,
            target_gross_exposure=1.0,
        )

        self.assertEqual([target.source["code"] for target in targets[:2]], ["000660", "005930"])
        self.assertNotIn("035420", [target.source["code"] for target in targets])
        self.assertTrue(all(target.target_side == "LONG" for target in targets))
        self.assertEqual(targets[0].target_weight, 0.25)
        self.assertEqual(diagnostics[0].selected_positions, 2)
        self.assertAlmostEqual(diagnostics[0].gross_target_weight, 0.5)
        self.assertAlmostEqual(diagnostics[0].cash_reserve_weight, 0.5)

    def test_turnover_weight_change_is_computed_between_dates(self) -> None:
        targets, diagnostics = generate_portfolio_targets(
            _signal_rows(),
            max_positions=10,
            max_position_weight=0.5,
            target_gross_exposure=1.0,
        )

        self.assertEqual(len(targets), 3)
        self.assertAlmostEqual(diagnostics[0].turnover_weight_change, 1.0)
        self.assertAlmostEqual(diagnostics[1].turnover_weight_change, 0.5)

    def test_report_keeps_order_and_backtest_guardrails(self) -> None:
        targets, diagnostics = generate_portfolio_targets(_signal_rows(), max_position_weight=0.25)
        report = render_report(
            targets=targets,
            diagnostics=diagnostics,
            summary=summarize(targets, diagnostics),
            input_path=Path("_report/quant/research/signals.rows.csv"),
            csv_output=Path("_report/quant/research/targets.rows.csv"),
            max_positions=20,
            max_position_weight=0.25,
            target_gross_exposure=1.0,
        )

        self.assertIn("- Order intent generated: `false`", report)
        self.assertIn("- Backtest readiness: `hold`", report)
        self.assertIn("- Live trading readiness: `blocked`", report)
        self.assertIn("`SELL candidate` rows are excluded in `long_only` mode", report)

    def test_invalid_thresholds_are_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "max_positions must be positive"):
            generate_portfolio_targets(_signal_rows(), max_positions=0)
        with self.assertRaisesRegex(ValueError, "max_position_weight must be in"):
            generate_portfolio_targets(_signal_rows(), max_position_weight=0)
        with self.assertRaisesRegex(ValueError, "target_gross_exposure must be in"):
            generate_portfolio_targets(_signal_rows(), target_gross_exposure=2)

    def test_cli_writes_report_and_rows(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            signals = root / "signals.rows.csv"
            rows_output = root / "targets.rows.csv"
            report_output = root / "targets.md"
            _write_csv(signals, _signal_rows())

            with patch(
                "sys.argv",
                [
                    "quant_signal_portfolio_targets_smoke.py",
                    "--signals-input",
                    str(signals),
                    "--max-position-weight",
                    "0.25",
                    "--csv-output",
                    str(rows_output),
                    "--report-output",
                    str(report_output),
                ],
            ):
                self.assertEqual(main(), 0)

            rows = rows_output.read_text(encoding="utf-8-sig")
            report = report_output.read_text(encoding="utf-8")
            rows_bytes = rows_output.read_bytes()
            report_bytes = report_output.read_bytes()

        self.assertIn("order_intent_generated", rows)
        self.assertIn("false", rows)
        self.assertIn("# Signal Portfolio Targets Smoke", report)
        self.assertIn("| Target rows | 3 |", report)
        self.assertNotIn(b"\r\n", rows_bytes)
        self.assertNotIn(b"\r\n", report_bytes)


if __name__ == "__main__":
    unittest.main()
