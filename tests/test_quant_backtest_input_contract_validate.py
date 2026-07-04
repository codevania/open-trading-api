from __future__ import annotations

import csv
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.quant_backtest_input_contract_validate import main, render_report, validate_contract


def _liquidity_rows() -> list[dict[str, str]]:
    return [
        {
            "date": "2025-02-05",
            "code": "005930",
            "stock_name": "Samsung Electronics",
            "close": "70000",
            "pit_status_replay_status": "include_by_status_event",
            "pit_universe_status": "include",
            "pit_liquidity_final_status": "include",
        },
        {
            "date": "2025-02-05",
            "code": "000660",
            "stock_name": "SK hynix",
            "close": "120000",
            "pit_status_replay_status": "include_by_status_event",
            "pit_universe_status": "include",
            "pit_liquidity_final_status": "include",
        },
    ]


def _signal_rows() -> list[dict[str, str]]:
    return [
        {
            "date": "2025-02-05",
            "code": "005930",
            "stock_name": "Samsung Electronics",
            "close": "70000",
            "signal_state": "BUY candidate",
            "signal_mode": "paper_signal_candidate_only",
            "rank_in_date_state": "1",
            "source_strategy": "001-strategy-universe-momentum",
            "pit_liquidity_final_status": "include",
        },
        {
            "date": "2025-02-05",
            "code": "000660",
            "stock_name": "SK hynix",
            "close": "120000",
            "signal_state": "SELL candidate",
            "signal_mode": "paper_signal_candidate_only",
            "rank_in_date_state": "1",
            "source_strategy": "001-strategy-universe-momentum",
            "pit_liquidity_final_status": "include",
        },
    ]


def _forward_return_rows() -> list[dict[str, str]]:
    return [
        {
            "date": "2025-02-05",
            "code": "005930",
            "signal_state": "BUY candidate",
            "horizon_trading_days": "1",
            "evaluation_status": "complete",
            "evaluation_mode": "paper_forward_return_smoke_only",
        },
        {
            "date": "2025-02-05",
            "code": "000660",
            "signal_state": "SELL candidate",
            "horizon_trading_days": "1",
            "evaluation_status": "missing_forward_price",
            "evaluation_mode": "paper_forward_return_smoke_only",
        },
    ]


def _portfolio_target_rows() -> list[dict[str, str]]:
    return [
        {
            "date": "2025-02-05",
            "code": "005930",
            "stock_name": "Samsung Electronics",
            "target_side": "LONG",
            "target_weight": "0.050000",
            "rank_in_portfolio": "1",
            "source_signal_state": "BUY candidate",
            "portfolio_mode": "long_only",
            "target_mode": "paper_portfolio_target_smoke_only",
            "order_intent_generated": "false",
        }
    ]


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


class QuantBacktestInputContractValidateTest(unittest.TestCase):
    def test_passes_joinable_smoke_contract_without_upgrading_backtest(self) -> None:
        checks, summary = validate_contract(
            liquidity_rows=_liquidity_rows(),
            signal_rows=_signal_rows(),
            forward_return_rows=_forward_return_rows(),
            portfolio_target_rows=_portfolio_target_rows(),
            expected_horizons=(1,),
            max_position_weight=0.10,
            max_gross_exposure=1.0,
        )
        by_name = {check.name: check for check in checks}

        self.assertEqual(summary["contract_status"], "pass_smoke")
        self.assertEqual(summary["backtest_readiness"], "hold")
        self.assertEqual(summary["live_trading_readiness"], "blocked")
        self.assertEqual(by_name["signal_liquidity_contract"].status, "pass")
        self.assertEqual(by_name["forward_return_contract"].status, "pass")
        self.assertEqual(by_name["portfolio_target_contract"].status, "pass")
        self.assertEqual(by_name["portfolio_weight_bounds"].status, "pass")

    def test_holds_when_signal_is_not_liquidity_backed(self) -> None:
        signals = [dict(row) for row in _signal_rows()]
        signals[0]["code"] = "035420"

        checks, summary = validate_contract(
            liquidity_rows=_liquidity_rows(),
            signal_rows=signals,
            forward_return_rows=[
                {**row, "code": "035420" if row["code"] == "005930" else row["code"]} for row in _forward_return_rows()
            ],
            portfolio_target_rows=[
                {**row, "code": "035420" if row["code"] == "005930" else row["code"]} for row in _portfolio_target_rows()
            ],
            expected_horizons=(1,),
        )

        self.assertEqual(summary["contract_status"], "hold")
        self.assertEqual({check.name: check for check in checks}["signal_liquidity_contract"].status, "hold")

    def test_holds_when_portfolio_targets_have_order_intents_or_bad_weights(self) -> None:
        targets = [dict(row) for row in _portfolio_target_rows()]
        targets[0]["order_intent_generated"] = "true"
        targets[0]["target_weight"] = "1.50"

        checks, summary = validate_contract(
            liquidity_rows=_liquidity_rows(),
            signal_rows=_signal_rows(),
            forward_return_rows=_forward_return_rows(),
            portfolio_target_rows=targets,
            expected_horizons=(1,),
            max_position_weight=0.10,
            max_gross_exposure=1.0,
        )
        by_name = {check.name: check for check in checks}

        self.assertEqual(summary["contract_status"], "hold")
        self.assertEqual(by_name["portfolio_target_contract"].status, "hold")
        self.assertEqual(by_name["portfolio_weight_bounds"].status, "hold")

    def test_holds_when_expected_forward_horizon_is_missing(self) -> None:
        checks, summary = validate_contract(
            liquidity_rows=_liquidity_rows(),
            signal_rows=_signal_rows(),
            forward_return_rows=_forward_return_rows(),
            portfolio_target_rows=_portfolio_target_rows(),
            expected_horizons=(1, 5),
        )

        self.assertEqual(summary["contract_status"], "hold")
        self.assertIn("missing_signal_horizon_keys=2", {check.name: check for check in checks}["forward_return_contract"].evidence)

    def test_report_guardrails_keep_contract_separate_from_backtest(self) -> None:
        checks, summary = validate_contract(
            liquidity_rows=_liquidity_rows(),
            signal_rows=_signal_rows(),
            forward_return_rows=_forward_return_rows(),
            portfolio_target_rows=_portfolio_target_rows(),
            expected_horizons=(1,),
        )
        report = render_report(
            checks=checks,
            summary=summary,
            liquidity_input=Path("_report/quant/research/liquidity.rows.csv"),
            signals_input=Path("_report/quant/research/signals.rows.csv"),
            forward_returns_input=Path("_report/quant/research/forward.rows.csv"),
            portfolio_targets_input=Path("_report/quant/research/targets.rows.csv"),
            expected_horizons=(1,),
            max_position_weight=0.10,
            max_gross_exposure=1.0,
        )

        self.assertIn("- Contract status: `pass_smoke`", report)
        self.assertIn("- Backtest readiness: `hold`", report)
        self.assertIn("- Live trading readiness: `blocked`", report)
        self.assertIn("it is not a Backtest result", report)

    def test_cli_writes_lf_report_from_local_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            liquidity = root / "liquidity.rows.csv"
            signals = root / "signals.rows.csv"
            forward = root / "forward.rows.csv"
            targets = root / "targets.rows.csv"
            output = root / "contract.md"
            _write_csv(liquidity, _liquidity_rows())
            _write_csv(signals, _signal_rows())
            _write_csv(forward, _forward_return_rows())
            _write_csv(targets, _portfolio_target_rows())

            with patch(
                "sys.argv",
                [
                    "quant_backtest_input_contract_validate.py",
                    "--liquidity-input",
                    str(liquidity),
                    "--signals-input",
                    str(signals),
                    "--forward-returns-input",
                    str(forward),
                    "--portfolio-targets-input",
                    str(targets),
                    "--expected-horizons",
                    "1",
                    "--report-output",
                    str(output),
                ],
            ):
                self.assertEqual(main(), 0)
            report = output.read_text(encoding="utf-8")
            report_bytes = output.read_bytes()

        self.assertIn("| `portfolio_target_contract` | `pass` |", report)
        self.assertIn("- Contract status: `pass_smoke`", report)
        self.assertNotIn(b"\r\n", report_bytes)


if __name__ == "__main__":
    unittest.main()
