"""Summarize Quant Backtest and live-trading readiness gates.

The checker reads already-generated local research artifacts. It does not call
KIS, KRX, or any broker API, and it never upgrades readiness on its own.
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Any


DEFAULT_MIN_MARKET_DATES = 20
DEFAULT_MIN_LIQUIDITY_LOOKBACK = 20


@dataclass(frozen=True)
class Gate:
    name: str
    status: str
    evidence: str
    next_action: str


def _read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise ValueError(f"missing CSV: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [{key: (value or "").strip() for key, value in row.items()} for row in csv.DictReader(handle)]


def _date_count(rows: list[dict[str, str]]) -> int:
    return len({row.get("date", "") for row in rows if row.get("date", "")})


def _count(rows: list[dict[str, str]], column: str, value: str) -> int:
    return sum(1 for row in rows if row.get(column, "") == value)


def _int_value(row: dict[str, str], column: str) -> int:
    text = row.get(column, "").strip()
    if not text:
        return 0
    try:
        return int(float(text))
    except ValueError:
        return 0


def _sorted_numeric_strings(values: set[str]) -> list[str]:
    def key(value: str) -> tuple[int, float | str]:
        try:
            return (0, float(value))
        except ValueError:
            return (1, value)

    return sorted(values, key=key)


def _float_value(row: dict[str, str], column: str) -> float:
    text = row.get(column, "").strip()
    if not text:
        return 0.0
    try:
        return float(text)
    except ValueError:
        return 0.0


def _read_text(path: Path | None) -> str:
    if path is None or not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def _kis_preflight_gate(path: Path | None) -> Gate:
    text = _read_text(path)
    if not text:
        return Gate(
            "kis_demo_account",
            "blocked",
            "no local KIS demo account preflight report supplied",
            "fill local demo account config and rerun account preflight",
        )
    if "Ready for read-only demo account calls: `true`" in text:
        return Gate(
            "kis_demo_account",
            "pass_read_only_only",
            "local demo account preflight reports read-only readiness true",
            "add buying-power and sellable-quantity checks before any order executor",
        )
    if "KIS_PAPER_STOCK" in text and "fail" in text:
        evidence = "local demo account preflight reports KIS_PAPER_STOCK missing or invalid"
    else:
        evidence = "local demo account preflight is not ready"
    return Gate("kis_demo_account", "blocked", evidence, "fill KIS_PAPER_STOCK locally and rerun account preflight")


def _backtest_contract_gate(path: Path | None) -> Gate | None:
    if path is None:
        return None
    text = _read_text(path)
    if not text:
        return Gate(
            "backtest_input_contract",
            "hold",
            "no local Backtest input contract report supplied",
            "run quant_backtest_input_contract_validate.py on current smoke artifacts",
        )
    if "Contract status: `pass_smoke`" in text and "Order intent generated: `false`" in text:
        return Gate(
            "backtest_input_contract",
            "pass_smoke",
            "local contract report is pass_smoke and reports no order intents",
            "keep contract validation aligned whenever smoke inputs change",
        )
    return Gate(
        "backtest_input_contract",
        "hold",
        "local contract report is not pass_smoke",
        "repair contract failures before wiring a Backtest engine",
    )


def evaluate_readiness(
    *,
    liquidity_rows: list[dict[str, str]],
    signal_rows: list[dict[str, str]],
    forward_return_rows: list[dict[str, str]] | None = None,
    portfolio_target_rows: list[dict[str, str]] | None = None,
    backtest_contract_report: Path | None = None,
    kis_preflight_report: Path | None,
    min_market_dates: int = DEFAULT_MIN_MARKET_DATES,
    min_liquidity_lookback: int = DEFAULT_MIN_LIQUIDITY_LOOKBACK,
    status_coverage: str = "current_snapshot_smoke",
) -> tuple[list[Gate], dict[str, Any]]:
    if min_market_dates <= 0:
        raise ValueError("min_market_dates must be positive")
    if min_liquidity_lookback <= 0:
        raise ValueError("min_liquidity_lookback must be positive")

    date_count = _date_count(liquidity_rows)
    include_rows = _count(liquidity_rows, "pit_liquidity_final_status", "include")
    full_lookback_rows = sum(1 for row in liquidity_rows if _int_value(row, "pit_liquidity_rows_used") >= min_liquidity_lookback)
    signal_date_count = _date_count(signal_rows)
    buy_candidates = _count(signal_rows, "signal_state", "BUY candidate")
    sell_candidates = _count(signal_rows, "signal_state", "SELL candidate")
    forward_rows = forward_return_rows or []
    forward_complete_rows = _count(forward_rows, "evaluation_status", "complete")
    forward_horizons = _sorted_numeric_strings(
        {row.get("horizon_trading_days", "") for row in forward_rows if row.get("horizon_trading_days", "")}
    )
    portfolio_rows = portfolio_target_rows or []
    portfolio_date_count = _date_count(portfolio_rows)
    portfolio_order_intents = sum(1 for row in portfolio_rows if row.get("order_intent_generated", "").lower() != "false")
    portfolio_modes = {row.get("target_mode", "") for row in portfolio_rows if row.get("target_mode", "")}
    portfolio_gross_by_date: dict[str, float] = {}
    for row in portfolio_rows:
        date = row.get("date", "")
        if not date:
            continue
        portfolio_gross_by_date[date] = portfolio_gross_by_date.get(date, 0.0) + _float_value(row, "target_weight")

    gates = [
        Gate(
            "market_data_window",
            "pass" if date_count >= min_market_dates else "hold",
            f"{date_count} market-data dates available; minimum configured gate is {min_market_dates}",
            "extend KRX OpenAPI market-data collection" if date_count < min_market_dates else "keep extending for production strategy lookbacks",
        ),
        Gate(
            "liquidity_filter",
            "pass_smoke" if full_lookback_rows > 0 and include_rows > 0 else "hold",
            f"{include_rows} include rows; {full_lookback_rows} rows evaluated with at least {min_liquidity_lookback}-day lookback",
            "keep 20-day Liquidity Filter aligned with expanded status/date windows",
        ),
        Gate(
            "signal_candidates",
            "pass_smoke" if signal_rows else "hold",
            f"{len(signal_rows)} candidates across {signal_date_count} dates; BUY={buy_candidates}, SELL={sell_candidates}",
            "keep candidates paper-only until Backtest/OOS/Bias Control pass",
        ),
    ]
    if forward_return_rows is not None:
        gates.append(
            Gate(
                "forward_return_smoke",
                "pass_smoke" if forward_complete_rows > 0 else "hold",
                f"{forward_complete_rows}/{len(forward_rows)} forward-return rows complete across horizons {','.join(forward_horizons) or 'none'}",
                "extend market-data window so forward-return coverage reaches production horizons",
            )
        )
    if portfolio_target_rows is not None:
        portfolio_is_smoke_only = bool(portfolio_rows) and portfolio_order_intents == 0 and portfolio_modes == {
            "paper_portfolio_target_smoke_only"
        }
        gates.append(
            Gate(
                "portfolio_targets_smoke",
                "pass_smoke" if portfolio_is_smoke_only else "hold",
                f"{len(portfolio_rows)} target rows across {portfolio_date_count} dates; order-intent rows={portfolio_order_intents}",
                "keep target weights diagnostic-only until Backtest cost/benchmark/OOS gates are wired",
            )
        )

    contract_gate = _backtest_contract_gate(backtest_contract_report)
    if contract_gate is not None:
        gates.append(contract_gate)

    status_ready = status_coverage == "historical_complete"
    gates.append(
        Gate(
            "point_in_time_status_coverage",
            "pass" if status_ready else "hold",
            f"status coverage mode is {status_coverage}",
            "replace current-snapshot smoke with historical status-event coverage by rebalance date",
        )
    )
    gates.extend(
        [
            Gate(
                "backtest_engine",
                "hold",
                "Backtest engine is not wired to Point-in-Time Universe, costs, benchmark, OOS, and Bias Control",
                "build Backtest only after Point-in-Time status coverage is acceptable for the selected scope",
            ),
            Gate(
                "live_trading_controls",
                "blocked",
                "no order executor, kill switch, explicit confirmation gate, status/cancel flow, or read-only account checks are complete",
                "finish demo read-only account gates before any order executor",
            ),
            _kis_preflight_gate(kis_preflight_report),
        ]
    )
    summary = {
        "market_data_dates": date_count,
        "liquidity_include_rows": include_rows,
        "liquidity_full_lookback_rows": full_lookback_rows,
        "signal_rows": len(signal_rows),
        "signal_dates": signal_date_count,
        "buy_candidates": buy_candidates,
        "sell_candidates": sell_candidates,
        "forward_return_rows": len(forward_rows) if forward_return_rows is not None else None,
        "forward_return_complete_rows": forward_complete_rows if forward_return_rows is not None else None,
        "forward_return_horizons": ",".join(forward_horizons) if forward_return_rows is not None else None,
        "portfolio_target_rows": len(portfolio_rows) if portfolio_target_rows is not None else None,
        "portfolio_target_dates": portfolio_date_count if portfolio_target_rows is not None else None,
        "portfolio_target_max_gross_weight": max(portfolio_gross_by_date.values(), default=0.0)
        if portfolio_target_rows is not None
        else None,
        "backtest_contract_report_supplied": backtest_contract_report is not None,
        "backtest_readiness": "hold",
        "live_trading_readiness": "blocked",
    }
    return gates, summary


def _wikilink(path: Path) -> str:
    rendered = path.as_posix()
    return f"[[{rendered}|{rendered}]]"


def _render_report(
    *,
    gates: list[Gate],
    summary: dict[str, Any],
    liquidity_input: Path,
    signals_input: Path,
    forward_returns_input: Path | None,
    portfolio_targets_input: Path | None,
    backtest_contract_report: Path | None,
    kis_preflight_report: Path | None,
    status_coverage: str,
) -> str:
    lines = [
        "# Quant Readiness Check",
        "",
        f"- Liquidity input: {_wikilink(liquidity_input)}",
        f"- Signal input: {_wikilink(signals_input)}",
        f"- Forward-return input: {_wikilink(forward_returns_input) if forward_returns_input else '`not_supplied`'}",
        f"- Portfolio-target input: {_wikilink(portfolio_targets_input) if portfolio_targets_input else '`not_supplied`'}",
        f"- Backtest contract report: {_wikilink(backtest_contract_report) if backtest_contract_report else '`not_supplied`'}",
        f"- KIS preflight report: {_wikilink(kis_preflight_report) if kis_preflight_report else '`not_supplied`'}",
        f"- Status coverage mode: `{status_coverage}`",
        "- KIS API call: `false`",
        "- Order intent generated: `false`",
        f"- Backtest readiness: `{summary['backtest_readiness']}`",
        f"- Live trading readiness: `{summary['live_trading_readiness']}`",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| Market-data dates | {summary['market_data_dates']} |",
        f"| Liquidity include rows | {summary['liquidity_include_rows']} |",
        f"| Liquidity full-lookback rows | {summary['liquidity_full_lookback_rows']} |",
        f"| Signal rows | {summary['signal_rows']} |",
        f"| Signal dates | {summary['signal_dates']} |",
        f"| BUY candidates | {summary['buy_candidates']} |",
        f"| SELL candidates | {summary['sell_candidates']} |",
    ]
    if summary.get("forward_return_rows") is not None:
        lines.extend(
            [
                f"| Forward-return rows | {summary['forward_return_rows']} |",
                f"| Forward-return complete rows | {summary['forward_return_complete_rows']} |",
            ]
        )
        if summary.get("forward_return_horizons"):
            lines.append(f"| Forward-return horizons | {summary['forward_return_horizons']} |")
    if summary.get("portfolio_target_rows") is not None:
        lines.extend(
            [
                f"| Portfolio target rows | {summary['portfolio_target_rows']} |",
                f"| Portfolio target dates | {summary['portfolio_target_dates']} |",
                f"| Portfolio max gross target weight | {summary['portfolio_target_max_gross_weight']:.4f} |",
            ]
        )

    lines.extend(
        [
            "",
            "## Gates",
            "",
            "| Gate | Status | Evidence | Next action |",
            "| --- | --- | --- | --- |",
        ]
    )
    for gate in gates:
        lines.append(f"| `{gate.name}` | `{gate.status}` | {gate.evidence} | {gate.next_action} |")

    lines.extend(
        [
            "",
            "## Guardrails",
            "",
            "- Passing smoke gates does not make the strategy Backtest-ready.",
            "- Do not create KIS order intents from Signal Candidate rows.",
            "- Keep raw credentials and account values out of tracked reports.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize Quant Backtest and live-trading readiness gates.")
    parser.add_argument("--liquidity-input", required=True, type=Path)
    parser.add_argument("--signals-input", required=True, type=Path)
    parser.add_argument("--forward-returns-input", type=Path)
    parser.add_argument("--portfolio-targets-input", type=Path)
    parser.add_argument("--backtest-contract-report", type=Path)
    parser.add_argument("--kis-preflight-report", type=Path)
    parser.add_argument("--status-coverage", default="current_snapshot_smoke")
    parser.add_argument("--min-market-dates", default=DEFAULT_MIN_MARKET_DATES, type=int)
    parser.add_argument("--min-liquidity-lookback", default=DEFAULT_MIN_LIQUIDITY_LOOKBACK, type=int)
    parser.add_argument("--report-output", type=Path)
    args = parser.parse_args()

    try:
        liquidity_rows = _read_csv(args.liquidity_input)
        signal_rows = _read_csv(args.signals_input)
        forward_return_rows = _read_csv(args.forward_returns_input) if args.forward_returns_input else None
        portfolio_target_rows = _read_csv(args.portfolio_targets_input) if args.portfolio_targets_input else None
        gates, summary = evaluate_readiness(
            liquidity_rows=liquidity_rows,
            signal_rows=signal_rows,
            forward_return_rows=forward_return_rows,
            portfolio_target_rows=portfolio_target_rows,
            backtest_contract_report=args.backtest_contract_report,
            kis_preflight_report=args.kis_preflight_report,
            min_market_dates=args.min_market_dates,
            min_liquidity_lookback=args.min_liquidity_lookback,
            status_coverage=args.status_coverage,
        )
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc

    report = _render_report(
        gates=gates,
        summary=summary,
        liquidity_input=args.liquidity_input,
        signals_input=args.signals_input,
        forward_returns_input=args.forward_returns_input,
        portfolio_targets_input=args.portfolio_targets_input,
        backtest_contract_report=args.backtest_contract_report,
        kis_preflight_report=args.kis_preflight_report,
        status_coverage=args.status_coverage,
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
