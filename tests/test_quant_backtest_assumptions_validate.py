from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import yaml

from scripts.quant_backtest_assumptions_validate import main, render_report, validate_assumptions


def _config() -> dict[str, object]:
    return {
        "version": "1.0",
        "scope": "unit-test",
        "cost_model": {
            "currency": "KRW",
            "commission_bps_per_side": {"baseline": 1.5, "stress": 5.0},
            "slippage_bps_per_side": {"baseline": 5.0, "stress": 20.0},
            "markets": {
                "KOSPI": {"sell_tax_bps": 20.0, "baseline_round_trip_bps": 33.0, "stress_round_trip_bps": 70.0},
                "KOSDAQ": {"sell_tax_bps": 20.0, "baseline_round_trip_bps": 33.0, "stress_round_trip_bps": 70.0},
            },
        },
        "benchmark": {
            "primary": "KOSPI",
            "secondary": ["KOSDAQ", "KOSPI200"],
            "source": "krx_openapi_index_daily",
            "required_for_backtest": True,
        },
    }


def _write_yaml(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")


class QuantBacktestAssumptionsValidateTest(unittest.TestCase):
    def test_valid_assumptions_pass_as_assumption_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "assumptions.yaml"
            _write_yaml(path, _config())

            checks, summary = validate_assumptions(path)

        self.assertEqual(summary["assumption_status"], "pass_assumption_only")
        self.assertEqual(summary["backtest_readiness"], "hold")
        self.assertEqual({check.name: check for check in checks}["cost_model"].status, "pass_assumption_only")
        self.assertEqual({check.name: check for check in checks}["benchmark"].status, "pass_assumption_only")

    def test_round_trip_costs_must_reconcile(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "assumptions.yaml"
            payload = _config()
            cost_model = payload["cost_model"]  # type: ignore[index]
            markets = cost_model["markets"]  # type: ignore[index]
            markets["KOSPI"]["baseline_round_trip_bps"] = 30.0  # type: ignore[index]
            _write_yaml(path, payload)

            checks, summary = validate_assumptions(path)

        self.assertEqual(summary["assumption_status"], "hold")
        self.assertIn("expected 33", {check.name: check for check in checks}["cost_model"].evidence)

    def test_benchmark_primary_is_required(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "assumptions.yaml"
            payload = _config()
            benchmark = payload["benchmark"]  # type: ignore[index]
            benchmark["primary"] = ""  # type: ignore[index]
            _write_yaml(path, payload)

            checks, summary = validate_assumptions(path)

        self.assertEqual(summary["assumption_status"], "hold")
        self.assertEqual({check.name: check for check in checks}["benchmark"].status, "hold")

    def test_cli_writes_lf_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "assumptions.yaml"
            output = root / "report.md"
            _write_yaml(path, _config())

            with patch(
                "sys.argv",
                [
                    "quant_backtest_assumptions_validate.py",
                    "--assumptions",
                    str(path),
                    "--report-output",
                    str(output),
                ],
            ):
                self.assertEqual(main(), 0)

            report = output.read_text(encoding="utf-8")
            report_bytes = output.read_bytes()

        self.assertIn("- Assumption status: `pass_assumption_only`", report)
        self.assertIn("- Backtest readiness: `hold`", report)
        self.assertIn("| `cost_model` | `pass_assumption_only` |", report)
        self.assertNotIn(b"\r\n", report_bytes)

    def test_report_keeps_assumptions_out_of_backtest_readiness(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "assumptions.yaml"
            _write_yaml(path, _config())
            checks, summary = validate_assumptions(path)
            report = render_report(checks=checks, summary=summary)

        self.assertIn("not Backtest readiness", report)
        self.assertIn("Benchmark return rows still need to be joined", report)


if __name__ == "__main__":
    unittest.main()
