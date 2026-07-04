"""Validate smoke artifacts before they are treated as Backtest inputs.

This contract validator is local-only. It checks that the current
Point-in-Time Liquidity, Signal Candidate, forward-return, and portfolio target
artifacts can be joined consistently, while keeping Backtest readiness at hold.
It does not call KIS, KRX, or any broker API, and it never creates order intents.
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable


LIQUIDITY_REQUIRED = {
    "date",
    "code",
    "close",
    "pit_status_replay_status",
    "pit_universe_status",
    "pit_liquidity_final_status",
}
SIGNAL_REQUIRED = {
    "date",
    "code",
    "close",
    "signal_state",
    "signal_mode",
    "rank_in_date_state",
    "source_strategy",
    "pit_liquidity_final_status",
}
FORWARD_RETURN_REQUIRED = {
    "date",
    "code",
    "signal_state",
    "horizon_trading_days",
    "evaluation_status",
    "evaluation_mode",
}
PORTFOLIO_TARGET_REQUIRED = {
    "date",
    "code",
    "target_side",
    "target_weight",
    "rank_in_portfolio",
    "source_signal_state",
    "portfolio_mode",
    "target_mode",
    "order_intent_generated",
}

ALLOWED_SIGNAL_STATES = {"BUY candidate", "SELL candidate"}
ALLOWED_FORWARD_STATUSES = {"complete", "missing_signal_price", "missing_forward_price"}
SIGNAL_MODE = "paper_signal_candidate_only"
FORWARD_MODE = "paper_forward_return_smoke_only"
PORTFOLIO_MODE = "long_only"
TARGET_MODE = "paper_portfolio_target_smoke_only"
DEFAULT_EXPECTED_HORIZONS = (1, 5)
DEFAULT_MAX_POSITION_WEIGHT = 0.10
DEFAULT_MAX_GROSS_EXPOSURE = 1.0
WEIGHT_TOLERANCE = 0.000001


@dataclass(frozen=True)
class ContractCheck:
    name: str
    status: str
    evidence: str
    next_action: str


def _read_csv(path: Path, label: str) -> list[dict[str, str]]:
    if not path.exists():
        raise ValueError(f"{label} CSV not found: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = [{key: (value or "").strip() for key, value in row.items()} for row in csv.DictReader(handle)]
    if not rows:
        raise ValueError(f"{label} CSV has no rows: {path}")
    return rows


def _columns(rows: list[dict[str, str]]) -> set[str]:
    return set(rows[0]) if rows else set()


def _missing_columns(rows: list[dict[str, str]], required: set[str]) -> set[str]:
    return required - _columns(rows)


def _key(row: dict[str, str], *columns: str) -> tuple[str, ...]:
    return tuple(row.get(column, "").strip().upper() if column == "code" else row.get(column, "").strip() for column in columns)


def _duplicate_count(rows: list[dict[str, str]], columns: tuple[str, ...]) -> int:
    counts = Counter(_key(row, *columns) for row in rows)
    return sum(count - 1 for key, count in counts.items() if all(key) and count > 1)


def _date_is_iso(value: str) -> bool:
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        return False
    return len(value) == 10


def _bad_date_or_code_count(rows: list[dict[str, str]]) -> int:
    return sum(1 for row in rows if not _date_is_iso(row.get("date", "")) or not row.get("code", "").strip())


def _parse_float(value: str) -> float | None:
    text = str(value or "").replace(",", "").strip()
    if not text:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def _parse_int(value: str) -> int | None:
    try:
        parsed = int(float(str(value or "").strip()))
    except ValueError:
        return None
    return parsed


def _parse_horizons(value: str) -> tuple[int, ...]:
    horizons: list[int] = []
    for token in value.split(","):
        text = token.strip()
        if not text:
            continue
        parsed = _parse_int(text)
        if parsed is None or parsed <= 0:
            raise ValueError(f"invalid expected horizon: {text}")
        horizons.append(parsed)
    if not horizons:
        raise ValueError("at least one expected horizon is required")
    return tuple(dict.fromkeys(horizons))


def _status_from_failures(failures: int) -> str:
    return "pass" if failures == 0 else "hold"


def _set_status(values: Iterable[str], expected: set[str]) -> tuple[int, str]:
    unexpected = sorted({value for value in values if value and value not in expected})
    return len(unexpected), ", ".join(unexpected)


def validate_contract(
    *,
    liquidity_rows: list[dict[str, str]],
    signal_rows: list[dict[str, str]],
    forward_return_rows: list[dict[str, str]],
    portfolio_target_rows: list[dict[str, str]],
    expected_horizons: tuple[int, ...] = DEFAULT_EXPECTED_HORIZONS,
    max_position_weight: float = DEFAULT_MAX_POSITION_WEIGHT,
    max_gross_exposure: float = DEFAULT_MAX_GROSS_EXPOSURE,
) -> tuple[list[ContractCheck], dict[str, object]]:
    if not expected_horizons:
        raise ValueError("at least one expected horizon is required")
    if any(horizon <= 0 for horizon in expected_horizons):
        raise ValueError("expected horizons must be positive")
    if max_position_weight <= 0 or max_position_weight > 1:
        raise ValueError("max_position_weight must be in (0, 1]")
    if max_gross_exposure <= 0 or max_gross_exposure > 1:
        raise ValueError("max_gross_exposure must be in (0, 1]")

    checks: list[ContractCheck] = []

    missing = {
        "liquidity": _missing_columns(liquidity_rows, LIQUIDITY_REQUIRED),
        "signals": _missing_columns(signal_rows, SIGNAL_REQUIRED),
        "forward_returns": _missing_columns(forward_return_rows, FORWARD_RETURN_REQUIRED),
        "portfolio_targets": _missing_columns(portfolio_target_rows, PORTFOLIO_TARGET_REQUIRED),
    }
    missing_total = sum(len(values) for values in missing.values())
    checks.append(
        ContractCheck(
            "required_columns",
            _status_from_failures(missing_total),
            "; ".join(f"{label} missing={','.join(sorted(values)) or 'none'}" for label, values in missing.items()),
            "regenerate the affected smoke artifact with the current script" if missing_total else "keep schema contract stable",
        )
    )

    duplicate_counts = {
        "liquidity": _duplicate_count(liquidity_rows, ("date", "code")),
        "signals": _duplicate_count(signal_rows, ("date", "code", "signal_state")),
        "forward_returns": _duplicate_count(forward_return_rows, ("date", "code", "horizon_trading_days")),
        "portfolio_targets": _duplicate_count(portfolio_target_rows, ("date", "code")),
    }
    duplicate_total = sum(duplicate_counts.values())
    checks.append(
        ContractCheck(
            "key_uniqueness",
            _status_from_failures(duplicate_total),
            "; ".join(f"{label} duplicate_keys={count}" for label, count in duplicate_counts.items()),
            "deduplicate or rebuild the affected artifact" if duplicate_total else "use these keys for Backtest preflight joins",
        )
    )

    bad_integrity = {
        "liquidity": _bad_date_or_code_count(liquidity_rows),
        "signals": _bad_date_or_code_count(signal_rows),
        "forward_returns": _bad_date_or_code_count(forward_return_rows),
        "portfolio_targets": _bad_date_or_code_count(portfolio_target_rows),
    }
    bad_integrity_total = sum(bad_integrity.values())
    checks.append(
        ContractCheck(
            "date_code_integrity",
            _status_from_failures(bad_integrity_total),
            "; ".join(f"{label} bad_date_or_code={count}" for label, count in bad_integrity.items()),
            "fix date format to YYYY-MM-DD and preserve KRX short codes" if bad_integrity_total else "date/code fields are joinable",
        )
    )

    liquidity_include_keys = {
        _key(row, "date", "code")
        for row in liquidity_rows
        if row.get("pit_liquidity_final_status") == "include" and row.get("pit_universe_status") == "include"
    }
    signal_keys = {_key(row, "date", "code") for row in signal_rows}
    signal_not_liquid = len(signal_keys - liquidity_include_keys)
    unexpected_signal_states, signal_state_text = _set_status((row.get("signal_state", "") for row in signal_rows), ALLOWED_SIGNAL_STATES)
    non_paper_signal_modes = sum(1 for row in signal_rows if row.get("signal_mode", "") != SIGNAL_MODE)
    signal_failures = signal_not_liquid + unexpected_signal_states + non_paper_signal_modes
    checks.append(
        ContractCheck(
            "signal_liquidity_contract",
            _status_from_failures(signal_failures),
            (
                f"signals_not_in_liquid_universe={signal_not_liquid}; "
                f"unexpected_signal_states={signal_state_text or 'none'}; non_paper_signal_modes={non_paper_signal_modes}"
            ),
            "rebuild Signal Candidate rows from the current Liquidity Filter output" if signal_failures else "signals are liquidity-backed and paper-only",
        )
    )

    expected_horizon_set = {str(horizon) for horizon in expected_horizons}
    forward_signal_keys = {_key(row, "date", "code") for row in forward_return_rows}
    forward_without_signal = len(forward_signal_keys - signal_keys)
    unexpected_forward_statuses, forward_status_text = _set_status(
        (row.get("evaluation_status", "") for row in forward_return_rows), ALLOWED_FORWARD_STATUSES
    )
    non_paper_forward_modes = sum(1 for row in forward_return_rows if row.get("evaluation_mode", "") != FORWARD_MODE)
    bad_forward_horizons = sum(1 for row in forward_return_rows if row.get("horizon_trading_days", "") not in expected_horizon_set)
    expected_forward_keys = {(date, code, str(horizon)) for date, code in signal_keys for horizon in expected_horizons}
    observed_forward_keys = {_key(row, "date", "code", "horizon_trading_days") for row in forward_return_rows}
    missing_forward_keys = len(expected_forward_keys - observed_forward_keys)
    forward_failures = (
        forward_without_signal
        + unexpected_forward_statuses
        + non_paper_forward_modes
        + bad_forward_horizons
        + missing_forward_keys
    )
    checks.append(
        ContractCheck(
            "forward_return_contract",
            _status_from_failures(forward_failures),
            (
                f"forward_rows_without_signal={forward_without_signal}; "
                f"unexpected_statuses={forward_status_text or 'none'}; non_paper_modes={non_paper_forward_modes}; "
                f"bad_horizons={bad_forward_horizons}; missing_signal_horizon_keys={missing_forward_keys}"
            ),
            "rerun forward-return smoke with the expected horizons" if forward_failures else "forward-return rows cover every signal/horizon key",
        )
    )

    buy_signal_keys = {_key(row, "date", "code") for row in signal_rows if row.get("signal_state") == "BUY candidate"}
    portfolio_keys = {_key(row, "date", "code") for row in portfolio_target_rows}
    targets_without_buy_signal = len(portfolio_keys - buy_signal_keys)
    target_rows_with_order_intent = sum(1 for row in portfolio_target_rows if row.get("order_intent_generated", "").lower() != "false")
    non_long_targets = sum(1 for row in portfolio_target_rows if row.get("target_side", "") != "LONG")
    non_long_only_modes = sum(1 for row in portfolio_target_rows if row.get("portfolio_mode", "") != PORTFOLIO_MODE)
    non_paper_target_modes = sum(1 for row in portfolio_target_rows if row.get("target_mode", "") != TARGET_MODE)
    target_contract_failures = (
        targets_without_buy_signal
        + target_rows_with_order_intent
        + non_long_targets
        + non_long_only_modes
        + non_paper_target_modes
    )
    checks.append(
        ContractCheck(
            "portfolio_target_contract",
            _status_from_failures(target_contract_failures),
            (
                f"targets_without_buy_signal={targets_without_buy_signal}; order_intent_rows={target_rows_with_order_intent}; "
                f"non_long_targets={non_long_targets}; non_long_only_modes={non_long_only_modes}; "
                f"non_paper_target_modes={non_paper_target_modes}"
            ),
            "rerun portfolio target smoke from BUY candidates only" if target_contract_failures else "portfolio targets are long-only and diagnostic-only",
        )
    )

    gross_by_date: dict[str, float] = defaultdict(float)
    bad_weight_rows = 0
    overweight_rows = 0
    for row in portfolio_target_rows:
        weight = _parse_float(row.get("target_weight", ""))
        if weight is None or weight <= 0:
            bad_weight_rows += 1
            continue
        if weight > max_position_weight + WEIGHT_TOLERANCE:
            overweight_rows += 1
        gross_by_date[row.get("date", "")] += weight
    gross_exposure_violations = sum(1 for value in gross_by_date.values() if value > max_gross_exposure + WEIGHT_TOLERANCE)
    weight_failures = bad_weight_rows + overweight_rows + gross_exposure_violations
    checks.append(
        ContractCheck(
            "portfolio_weight_bounds",
            _status_from_failures(weight_failures),
            (
                f"bad_weight_rows={bad_weight_rows}; overweight_rows={overweight_rows}; "
                f"gross_exposure_violations={gross_exposure_violations}; max_gross_observed={max(gross_by_date.values(), default=0.0):.6f}"
            ),
            "fix target weight generation or risk limits" if weight_failures else "portfolio weights stay inside configured bounds",
        )
    )

    row_counts = {
        "liquidity_rows": len(liquidity_rows),
        "signal_rows": len(signal_rows),
        "forward_return_rows": len(forward_return_rows),
        "portfolio_target_rows": len(portfolio_target_rows),
    }
    date_counts = {
        "liquidity_dates": len({_key(row, "date")[0] for row in liquidity_rows if row.get("date")}),
        "signal_dates": len({_key(row, "date")[0] for row in signal_rows if row.get("date")}),
        "portfolio_target_dates": len({_key(row, "date")[0] for row in portfolio_target_rows if row.get("date")}),
    }
    hold_count = sum(1 for check in checks if check.status != "pass")
    summary: dict[str, object] = {
        **row_counts,
        **date_counts,
        "expected_horizons": ",".join(str(horizon) for horizon in expected_horizons),
        "contract_status": "pass_smoke" if hold_count == 0 else "hold",
        "hold_checks": hold_count,
        "max_gross_observed": max(gross_by_date.values(), default=0.0),
        "backtest_readiness": "hold",
        "live_trading_readiness": "blocked",
    }
    return checks, summary


def _wikilink(path: Path) -> str:
    rendered = path.as_posix()
    return f"[[{rendered}|{rendered}]]"


def render_report(
    *,
    checks: list[ContractCheck],
    summary: dict[str, object],
    liquidity_input: Path,
    signals_input: Path,
    forward_returns_input: Path,
    portfolio_targets_input: Path,
    expected_horizons: tuple[int, ...],
    max_position_weight: float,
    max_gross_exposure: float,
) -> str:
    lines = [
        "# Backtest Input Contract Validate",
        "",
        f"- Liquidity input: {_wikilink(liquidity_input)}",
        f"- Signal input: {_wikilink(signals_input)}",
        f"- Forward-return input: {_wikilink(forward_returns_input)}",
        f"- Portfolio-target input: {_wikilink(portfolio_targets_input)}",
        f"- Expected horizons: `{','.join(str(horizon) for horizon in expected_horizons)}`",
        f"- Max position weight: `{max_position_weight:.2%}`",
        f"- Max gross exposure: `{max_gross_exposure:.2%}`",
        "- KIS API call: `false`",
        "- KRX API call: `false`",
        "- Order intent generated: `false`",
        f"- Contract status: `{summary['contract_status']}`",
        f"- Backtest readiness: `{summary['backtest_readiness']}`",
        f"- Live trading readiness: `{summary['live_trading_readiness']}`",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| Liquidity rows | {summary['liquidity_rows']} |",
        f"| Signal rows | {summary['signal_rows']} |",
        f"| Forward-return rows | {summary['forward_return_rows']} |",
        f"| Portfolio target rows | {summary['portfolio_target_rows']} |",
        f"| Liquidity dates | {summary['liquidity_dates']} |",
        f"| Signal dates | {summary['signal_dates']} |",
        f"| Portfolio target dates | {summary['portfolio_target_dates']} |",
        f"| Hold checks | {summary['hold_checks']} |",
        f"| Max gross observed | {float(summary['max_gross_observed']):.6f} |",
        "",
        "## Checks",
        "",
        "| Check | Status | Evidence | Next action |",
        "| --- | --- | --- | --- |",
    ]
    for check in checks:
        lines.append(f"| `{check.name}` | `{check.status}` | {check.evidence} | {check.next_action} |")

    lines.extend(
        [
            "",
            "## Guardrails",
            "",
            "- Passing this contract means the smoke artifacts are internally joinable; it is not a Backtest result.",
            "- This does not model transaction costs, slippage, taxes, benchmark returns, cash drag, or execution constraints.",
            "- Keep `Backtest readiness` at `hold` until historical `Point-in-Time` status coverage, cost model, benchmark, OOS, and Bias Control pass.",
            "- Keep `Live trading readiness` at `blocked` until demo account, buying-power, sellable-quantity, order status/cancel, kill switch, and explicit confirmation gates are implemented.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate smoke artifacts before Backtest input wiring.")
    parser.add_argument("--liquidity-input", required=True, type=Path)
    parser.add_argument("--signals-input", required=True, type=Path)
    parser.add_argument("--forward-returns-input", required=True, type=Path)
    parser.add_argument("--portfolio-targets-input", required=True, type=Path)
    parser.add_argument("--expected-horizons", default=",".join(str(value) for value in DEFAULT_EXPECTED_HORIZONS))
    parser.add_argument("--max-position-weight", default=DEFAULT_MAX_POSITION_WEIGHT, type=float)
    parser.add_argument("--max-gross-exposure", default=DEFAULT_MAX_GROSS_EXPOSURE, type=float)
    parser.add_argument("--report-output", type=Path)
    args = parser.parse_args()

    try:
        expected_horizons = _parse_horizons(args.expected_horizons)
        liquidity_rows = _read_csv(args.liquidity_input, "Liquidity")
        signal_rows = _read_csv(args.signals_input, "Signal Candidate")
        forward_return_rows = _read_csv(args.forward_returns_input, "Forward-return")
        portfolio_target_rows = _read_csv(args.portfolio_targets_input, "Portfolio target")
        checks, summary = validate_contract(
            liquidity_rows=liquidity_rows,
            signal_rows=signal_rows,
            forward_return_rows=forward_return_rows,
            portfolio_target_rows=portfolio_target_rows,
            expected_horizons=expected_horizons,
            max_position_weight=args.max_position_weight,
            max_gross_exposure=args.max_gross_exposure,
        )
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc

    report = render_report(
        checks=checks,
        summary=summary,
        liquidity_input=args.liquidity_input,
        signals_input=args.signals_input,
        forward_returns_input=args.forward_returns_input,
        portfolio_targets_input=args.portfolio_targets_input,
        expected_horizons=expected_horizons,
        max_position_weight=args.max_position_weight,
        max_gross_exposure=args.max_gross_exposure,
    )
    if args.report_output:
        args.report_output.parent.mkdir(parents=True, exist_ok=True)
        with args.report_output.open("w", encoding="utf-8", newline="\n") as handle:
            handle.write(report)
    else:
        print(report, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
