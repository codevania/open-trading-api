"""Validate Backtest cost and benchmark assumptions.

This is an input-contract check for local Quant research. It does not run a
Backtest, fetch market data, or approve live trading.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

try:
    from quant_io import write_text_lf
except ModuleNotFoundError:  # pragma: no cover - used when imported as scripts.* in tests.
    from scripts.quant_io import write_text_lf


DEFAULT_ASSUMPTIONS = Path("_report/quant/data/backtest_cost_benchmark_assumptions.yaml")


@dataclass(frozen=True)
class AssumptionCheck:
    name: str
    status: str
    evidence: str


def _load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise ValueError(f"missing assumptions YAML: {path}")
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("assumptions YAML root must be a mapping")
    return payload


def _number(value: Any, field: str) -> float:
    try:
        parsed = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field} must be numeric") from exc
    if parsed < 0:
        raise ValueError(f"{field} must be non-negative")
    return parsed


def _check_required_sections(config: dict[str, Any]) -> AssumptionCheck:
    missing = [key for key in ("cost_model", "benchmark") if not isinstance(config.get(key), dict)]
    if missing:
        return AssumptionCheck("required_sections", "hold", "missing sections: " + ",".join(missing))
    return AssumptionCheck("required_sections", "pass", "cost_model and benchmark sections are present")


def _check_cost_model(config: dict[str, Any]) -> AssumptionCheck:
    cost_model = config.get("cost_model", {}) or {}
    commission = cost_model.get("commission_bps_per_side", {}) or {}
    slippage = cost_model.get("slippage_bps_per_side", {}) or {}
    markets = cost_model.get("markets", {}) or {}
    if not isinstance(markets, dict) or not markets:
        return AssumptionCheck("cost_model", "hold", "no market cost assumptions supplied")

    commission_baseline = _number(commission.get("baseline"), "commission_bps_per_side.baseline")
    commission_stress = _number(commission.get("stress"), "commission_bps_per_side.stress")
    slippage_baseline = _number(slippage.get("baseline"), "slippage_bps_per_side.baseline")
    slippage_stress = _number(slippage.get("stress"), "slippage_bps_per_side.stress")
    if commission_stress < commission_baseline or slippage_stress < slippage_baseline:
        return AssumptionCheck("cost_model", "hold", "stress assumptions must be greater than or equal to baseline")

    errors: list[str] = []
    for market, values in markets.items():
        if not isinstance(values, dict):
            errors.append(f"{market}: market assumptions must be a mapping")
            continue
        tax = _number(values.get("sell_tax_bps"), f"{market}.sell_tax_bps")
        expected_baseline = (2 * commission_baseline) + (2 * slippage_baseline) + tax
        expected_stress = (2 * commission_stress) + (2 * slippage_stress) + tax
        baseline = _number(values.get("baseline_round_trip_bps"), f"{market}.baseline_round_trip_bps")
        stress = _number(values.get("stress_round_trip_bps"), f"{market}.stress_round_trip_bps")
        if abs(baseline - expected_baseline) > 1e-9:
            errors.append(f"{market}: baseline_round_trip_bps expected {expected_baseline:g}, got {baseline:g}")
        if abs(stress - expected_stress) > 1e-9:
            errors.append(f"{market}: stress_round_trip_bps expected {expected_stress:g}, got {stress:g}")

    if errors:
        return AssumptionCheck("cost_model", "hold", "; ".join(errors))
    return AssumptionCheck("cost_model", "pass_assumption_only", f"{len(markets)} market cost assumptions reconcile")


def _check_benchmark(config: dict[str, Any]) -> AssumptionCheck:
    benchmark = config.get("benchmark", {}) or {}
    primary = str(benchmark.get("primary", "")).strip()
    source = str(benchmark.get("source", "")).strip()
    if not primary:
        return AssumptionCheck("benchmark", "hold", "primary benchmark is missing")
    if not source:
        return AssumptionCheck("benchmark", "hold", "benchmark source is missing")
    if not benchmark.get("required_for_backtest", False):
        return AssumptionCheck("benchmark", "hold", "benchmark is not marked required_for_backtest")
    return AssumptionCheck("benchmark", "pass_assumption_only", f"primary={primary}; source={source}")


def validate_assumptions(path: Path = DEFAULT_ASSUMPTIONS) -> tuple[list[AssumptionCheck], dict[str, Any]]:
    config = _load_yaml(path)
    checks = [_check_required_sections(config)]
    if checks[0].status == "pass":
        checks.extend([_check_cost_model(config), _check_benchmark(config)])
    assumption_status = "pass_assumption_only" if all(check.status != "hold" for check in checks) else "hold"
    summary = {
        "assumptions_path": path,
        "assumption_status": assumption_status,
        "backtest_readiness": "hold",
        "live_trading_readiness": "blocked",
        "check_count": len(checks),
        "hold_count": sum(1 for check in checks if check.status == "hold"),
    }
    return checks, summary


def _wikilink(path: Path) -> str:
    rendered = path.as_posix()
    return f"[[{rendered}|{rendered}]]"


def render_report(*, checks: list[AssumptionCheck], summary: dict[str, Any]) -> str:
    lines = [
        "# Backtest Cost Benchmark Assumptions Validation",
        "",
        f"- Assumptions: {_wikilink(summary['assumptions_path'])}",
        f"- Assumption status: `{summary['assumption_status']}`",
        f"- Backtest readiness: `{summary['backtest_readiness']}`",
        f"- Live trading readiness: `{summary['live_trading_readiness']}`",
        "- KIS/KRX API call: `false`",
        "- Order intent generated: `false`",
        "- Interpretation: local assumption contract only, not a `Backtest` result",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| Checks | {summary['check_count']} |",
        f"| Hold checks | {summary['hold_count']} |",
        "",
        "## Checks",
        "",
        "| Check | Status | Evidence |",
        "| --- | --- | --- |",
    ]
    for check in checks:
        lines.append(f"| `{check.name}` | `{check.status}` | {check.evidence} |")
    lines.extend(
        [
            "",
            "## Guardrails",
            "",
            "- `pass_assumption_only` means the local assumptions reconcile; it is not Backtest readiness.",
            "- Replace placeholder commission with the actual KIS account/channel fee schedule before production Backtest.",
            "- Benchmark return rows still need to be joined into the Backtest engine separately.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Backtest cost and benchmark assumptions.")
    parser.add_argument("--assumptions", default=DEFAULT_ASSUMPTIONS, type=Path)
    parser.add_argument("--report-output", type=Path)
    args = parser.parse_args()

    try:
        checks, summary = validate_assumptions(args.assumptions)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
    report = render_report(checks=checks, summary=summary)
    if args.report_output:
        write_text_lf(args.report_output, report)
    else:
        print(report, end="")
    return 0 if summary["assumption_status"] == "pass_assumption_only" else 1


if __name__ == "__main__":
    raise SystemExit(main())
