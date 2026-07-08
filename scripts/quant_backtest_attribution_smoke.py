"""Compute paper-only Backtest attribution smoke diagnostics.

This aggregates local Backtest PnL smoke rows into date/horizon portfolio
return, cost, and benchmark-active diagnostics. It does not fetch data, does
not create orders, and does not promote Backtest readiness.
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from statistics import mean
from typing import Any

import yaml

try:
    from quant_io import write_text_lf
except ModuleNotFoundError:  # pragma: no cover - used when imported as scripts.* in tests.
    from scripts.quant_io import write_text_lf


PNL_MODE = "paper_backtest_pnl_smoke_only"
ATTRIBUTION_MODE = "paper_backtest_attribution_smoke_assumption_only"
DEFAULT_ASSUMPTIONS = Path("_report/quant/data/backtest_cost_benchmark_assumptions.yaml")
REQUIRED_PNL_FIELDS = {
    "date",
    "code",
    "market",
    "horizon_trading_days",
    "evaluation_status",
    "target_side",
    "target_weight",
    "weighted_return_contribution_pct",
    "benchmark_label",
    "benchmark_join_status",
    "benchmark_return_pct",
    "pnl_mode",
    "order_intent_generated",
}
OUTPUT_FIELDS = (
    "date",
    "horizon_trading_days",
    "benchmark_label",
    "attribution_status",
    "target_rows",
    "complete_rows",
    "benchmark_joined_rows",
    "cost_covered_rows",
    "gross_target_weight",
    "covered_gross_weight",
    "missing_gross_weight",
    "cash_weight",
    "gross_return_pct",
    "baseline_cost_pct",
    "stress_cost_pct",
    "baseline_net_return_pct",
    "stress_net_return_pct",
    "benchmark_return_pct",
    "baseline_active_return_pct",
    "stress_active_return_pct",
    "cash_drag_vs_benchmark_pct",
    "baseline_round_trip_bps_weighted_avg",
    "stress_round_trip_bps_weighted_avg",
    "markets",
    "broker_fee_override_required",
    "attribution_mode",
    "order_intent_generated",
    "notes",
)


@dataclass(frozen=True)
class MarketCost:
    baseline_round_trip_bps: float
    stress_round_trip_bps: float


@dataclass(frozen=True)
class AttributionRow:
    date: str
    horizon: int
    benchmark_label: str
    attribution_status: str
    target_rows: int
    complete_rows: int
    benchmark_joined_rows: int
    cost_covered_rows: int
    gross_target_weight: float
    covered_gross_weight: float
    missing_gross_weight: float
    cash_weight: float
    gross_return_pct: float
    baseline_cost_pct: float
    stress_cost_pct: float
    baseline_net_return_pct: float
    stress_net_return_pct: float
    benchmark_return_pct: float | None
    baseline_active_return_pct: float | None
    stress_active_return_pct: float | None
    cash_drag_vs_benchmark_pct: float | None
    baseline_round_trip_bps_weighted_avg: float | None
    stress_round_trip_bps_weighted_avg: float | None
    markets: tuple[str, ...]
    broker_fee_override_required: bool
    notes: tuple[str, ...]


def _read_csv(path: Path, label: str) -> tuple[list[str], list[dict[str, str]]]:
    if not path.exists():
        raise ValueError(f"{label} CSV not found: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = list(reader.fieldnames or [])
        rows = [{key: (value or "").strip() for key, value in row.items()} for row in reader]
    if not rows:
        raise ValueError(f"{label} CSV has no rows: {path}")
    return fields, rows


def _require_columns(fields: list[str], required: set[str], label: str) -> None:
    missing = required - set(fields)
    if missing:
        raise ValueError(f"{label} CSV missing required columns: {', '.join(sorted(missing))}")


def _parse_float(value: Any) -> float | None:
    text = str(value or "").replace(",", "").strip()
    if not text:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def _parse_int(value: Any) -> int | None:
    parsed = _parse_float(value)
    if parsed is None:
        return None
    return int(parsed)


def _format_float(value: float | None) -> str:
    if value is None:
        return ""
    return f"{value:.4f}"


def _format_weight(value: float) -> str:
    return f"{value:.6f}"


def _load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise ValueError(f"missing assumptions YAML: {path}")
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("assumptions YAML root must be a mapping")
    return payload


def _number(value: Any, field_name: str) -> float:
    parsed = _parse_float(value)
    if parsed is None:
        raise ValueError(f"{field_name} must be numeric")
    if parsed < 0:
        raise ValueError(f"{field_name} must be non-negative")
    return parsed


def _market_costs(config: dict[str, Any]) -> tuple[dict[str, MarketCost], bool, str]:
    cost_model = config.get("cost_model", {}) or {}
    if not isinstance(cost_model, dict):
        raise ValueError("assumptions cost_model must be a mapping")
    markets = cost_model.get("markets", {}) or {}
    if not isinstance(markets, dict) or not markets:
        raise ValueError("assumptions cost_model.markets must be a non-empty mapping")
    commission = cost_model.get("commission_bps_per_side", {}) or {}
    broker_fee_override_required = bool(commission.get("needs_broker_override", False))
    currency = str(cost_model.get("currency", "KRW") or "KRW")

    parsed: dict[str, MarketCost] = {}
    for market, values in markets.items():
        if not isinstance(values, dict):
            raise ValueError(f"{market} cost assumption must be a mapping")
        parsed[str(market).strip().upper()] = MarketCost(
            baseline_round_trip_bps=_number(values.get("baseline_round_trip_bps"), f"{market}.baseline_round_trip_bps"),
            stress_round_trip_bps=_number(values.get("stress_round_trip_bps"), f"{market}.stress_round_trip_bps"),
        )
    return parsed, broker_fee_override_required, currency


def _benchmark_primary(config: dict[str, Any]) -> str:
    benchmark = config.get("benchmark", {}) or {}
    if not isinstance(benchmark, dict):
        raise ValueError("assumptions benchmark must be a mapping")
    primary = str(benchmark.get("primary", "")).strip().upper()
    if not primary:
        raise ValueError("assumptions benchmark.primary is required")
    return primary


def _validate_pnl_rows(rows: list[dict[str, str]]) -> None:
    bad_orders = sum(1 for row in rows if row.get("order_intent_generated", "").lower() != "false")
    if bad_orders:
        raise ValueError("PnL rows must not contain order intents")
    non_long = sum(1 for row in rows if row.get("target_side", "") != "LONG")
    if non_long:
        raise ValueError("PnL attribution smoke currently supports LONG-only rows")
    bad_modes = sorted({row.get("pnl_mode", "") for row in rows if row.get("pnl_mode", "") != PNL_MODE})
    if bad_modes:
        raise ValueError(f"unexpected PnL modes: {', '.join(bad_modes)}")


def _group_key(row: dict[str, str]) -> tuple[str, int]:
    horizon = _parse_int(row.get("horizon_trading_days", ""))
    if horizon is None or horizon <= 0:
        raise ValueError("horizon_trading_days must be positive")
    return row.get("date", ""), horizon


def _market(row: dict[str, str]) -> str:
    return row.get("market", "").strip().upper()


def build_attribution_rows(
    *,
    pnl_rows: list[dict[str, str]],
    assumptions: dict[str, Any],
) -> tuple[list[AttributionRow], dict[str, Any]]:
    _validate_pnl_rows(pnl_rows)
    market_costs, broker_fee_override_required, currency = _market_costs(assumptions)
    primary_benchmark = _benchmark_primary(assumptions)
    grouped: dict[tuple[str, int], list[dict[str, str]]] = defaultdict(list)
    for row in pnl_rows:
        grouped[_group_key(row)].append(row)

    rows: list[AttributionRow] = []
    for (date, horizon), group in sorted(grouped.items()):
        target_rows = len(group)
        complete = [row for row in group if row.get("evaluation_status", "") == "complete"]
        benchmark_joined = [row for row in group if row.get("benchmark_join_status", "") == "complete"]
        gross_target_weight = sum(_parse_float(row.get("target_weight", "")) or 0.0 for row in group)
        covered_gross_weight = sum(_parse_float(row.get("target_weight", "")) or 0.0 for row in complete)
        missing_gross_weight = max(0.0, gross_target_weight - covered_gross_weight)
        cash_weight = max(0.0, 1.0 - gross_target_weight)
        gross_return = sum(_parse_float(row.get("weighted_return_contribution_pct", "")) or 0.0 for row in complete)

        baseline_cost = 0.0
        stress_cost = 0.0
        cost_weight = 0.0
        cost_covered_rows = 0
        missing_cost_markets: set[str] = set()
        markets: set[str] = set()
        for row in group:
            market = _market(row)
            if market:
                markets.add(market)
            cost = market_costs.get(market)
            target_weight = _parse_float(row.get("target_weight", "")) or 0.0
            if cost is None:
                missing_cost_markets.add(market or "blank")
                continue
            cost_covered_rows += 1
            cost_weight += target_weight
            baseline_cost += target_weight * (cost.baseline_round_trip_bps / 100.0)
            stress_cost += target_weight * (cost.stress_round_trip_bps / 100.0)

        benchmark_values = [
            value
            for value in (_parse_float(row.get("benchmark_return_pct", "")) for row in benchmark_joined)
            if value is not None
        ]
        benchmark_return = mean(benchmark_values) if benchmark_values else None
        baseline_net = gross_return - baseline_cost
        stress_net = gross_return - stress_cost
        baseline_active = baseline_net - benchmark_return if benchmark_return is not None else None
        stress_active = stress_net - benchmark_return if benchmark_return is not None else None
        cash_drag = -(cash_weight * benchmark_return) if benchmark_return is not None else None

        notes: list[str] = []
        if broker_fee_override_required:
            notes.append("broker_fee_override_required")
        if missing_gross_weight > 1e-12:
            notes.append("missing_forward_return_weight")
        if missing_cost_markets:
            notes.append("missing_market_cost_assumptions:" + ";".join(sorted(missing_cost_markets)))
        if len(benchmark_joined) != target_rows:
            notes.append("benchmark_join_incomplete")
        if primary_benchmark not in {row.get("benchmark_label", "").strip().upper() for row in group}:
            notes.append("primary_benchmark_not_joined")

        attribution_status = (
            "pass_smoke_assumption_only"
            if target_rows
            and len(complete) == target_rows
            and len(benchmark_joined) == target_rows
            and not missing_cost_markets
            else "hold"
        )
        rows.append(
            AttributionRow(
                date=date,
                horizon=horizon,
                benchmark_label=primary_benchmark,
                attribution_status=attribution_status,
                target_rows=target_rows,
                complete_rows=len(complete),
                benchmark_joined_rows=len(benchmark_joined),
                cost_covered_rows=cost_covered_rows,
                gross_target_weight=gross_target_weight,
                covered_gross_weight=covered_gross_weight,
                missing_gross_weight=missing_gross_weight,
                cash_weight=cash_weight,
                gross_return_pct=gross_return,
                baseline_cost_pct=baseline_cost,
                stress_cost_pct=stress_cost,
                baseline_net_return_pct=baseline_net,
                stress_net_return_pct=stress_net,
                benchmark_return_pct=benchmark_return,
                baseline_active_return_pct=baseline_active,
                stress_active_return_pct=stress_active,
                cash_drag_vs_benchmark_pct=cash_drag,
                baseline_round_trip_bps_weighted_avg=(baseline_cost / cost_weight) * 100.0 if cost_weight else None,
                stress_round_trip_bps_weighted_avg=(stress_cost / cost_weight) * 100.0 if cost_weight else None,
                markets=tuple(sorted(markets)),
                broker_fee_override_required=broker_fee_override_required,
                notes=tuple(notes),
            )
        )

    status_counts = Counter(row.attribution_status for row in rows)
    summary = {
        "attribution_status": "pass_smoke_assumption_only" if rows and not status_counts.get("hold") else "hold",
        "rows": len(rows),
        "pnl_rows": len(pnl_rows),
        "date_count": len({row.date for row in rows}),
        "horizon_count": len({row.horizon for row in rows}),
        "status_counts": dict(sorted(status_counts.items())),
        "avg_gross_return_pct": mean([row.gross_return_pct for row in rows]) if rows else 0.0,
        "avg_baseline_net_return_pct": mean([row.baseline_net_return_pct for row in rows]) if rows else 0.0,
        "avg_stress_net_return_pct": mean([row.stress_net_return_pct for row in rows]) if rows else 0.0,
        "avg_baseline_active_return_pct": mean(
            [row.baseline_active_return_pct for row in rows if row.baseline_active_return_pct is not None]
        )
        if any(row.baseline_active_return_pct is not None for row in rows)
        else None,
        "currency": currency,
        "broker_fee_override_required": broker_fee_override_required,
        "backtest_readiness": "hold",
        "live_trading_readiness": "blocked",
    }
    return rows, summary


def write_csv(rows: list[AttributionRow], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "date": row.date,
                    "horizon_trading_days": str(row.horizon),
                    "benchmark_label": row.benchmark_label,
                    "attribution_status": row.attribution_status,
                    "target_rows": str(row.target_rows),
                    "complete_rows": str(row.complete_rows),
                    "benchmark_joined_rows": str(row.benchmark_joined_rows),
                    "cost_covered_rows": str(row.cost_covered_rows),
                    "gross_target_weight": _format_weight(row.gross_target_weight),
                    "covered_gross_weight": _format_weight(row.covered_gross_weight),
                    "missing_gross_weight": _format_weight(row.missing_gross_weight),
                    "cash_weight": _format_weight(row.cash_weight),
                    "gross_return_pct": _format_float(row.gross_return_pct),
                    "baseline_cost_pct": _format_float(row.baseline_cost_pct),
                    "stress_cost_pct": _format_float(row.stress_cost_pct),
                    "baseline_net_return_pct": _format_float(row.baseline_net_return_pct),
                    "stress_net_return_pct": _format_float(row.stress_net_return_pct),
                    "benchmark_return_pct": _format_float(row.benchmark_return_pct),
                    "baseline_active_return_pct": _format_float(row.baseline_active_return_pct),
                    "stress_active_return_pct": _format_float(row.stress_active_return_pct),
                    "cash_drag_vs_benchmark_pct": _format_float(row.cash_drag_vs_benchmark_pct),
                    "baseline_round_trip_bps_weighted_avg": _format_float(row.baseline_round_trip_bps_weighted_avg),
                    "stress_round_trip_bps_weighted_avg": _format_float(row.stress_round_trip_bps_weighted_avg),
                    "markets": ";".join(row.markets),
                    "broker_fee_override_required": str(row.broker_fee_override_required).lower(),
                    "attribution_mode": ATTRIBUTION_MODE,
                    "order_intent_generated": "false",
                    "notes": ";".join(row.notes),
                }
            )


def _wikilink(path: Path) -> str:
    rendered = path.as_posix()
    return f"[[{rendered}|{rendered}]]"


def render_report(
    *,
    rows: list[AttributionRow],
    summary: dict[str, Any],
    pnl_input: Path,
    assumptions_input: Path,
    csv_output: Path | None,
) -> str:
    lines = [
        "# Backtest Attribution Smoke",
        "",
        f"- PnL smoke input: {_wikilink(pnl_input)}",
        f"- Assumptions input: {_wikilink(assumptions_input)}",
        f"- Attribution mode: `{ATTRIBUTION_MODE}`",
        f"- Attribution status: `{summary['attribution_status']}`",
        f"- Backtest readiness: `{summary['backtest_readiness']}`",
        f"- Live trading readiness: `{summary['live_trading_readiness']}`",
        "- KIS API call: `false`",
        "- KRX API call: `false`",
        "- Order intent generated: `false`",
        "- Interpretation: cost and benchmark attribution smoke only, not a production `Backtest` result",
    ]
    if csv_output is not None:
        lines.append(f"- Machine-readable rows: {_wikilink(csv_output)}")

    lines.extend(
        [
            "",
            "## Summary",
            "",
            "| Metric | Value |",
            "| --- | ---: |",
            f"| Attribution rows | {summary['rows']} |",
            f"| PnL rows | {summary['pnl_rows']} |",
            f"| Dates | {summary['date_count']} |",
            f"| Horizons | {summary['horizon_count']} |",
            f"| Broker fee override required | `{str(summary['broker_fee_override_required']).lower()}` |",
            f"| Avg gross return % | {_format_float(summary['avg_gross_return_pct'])} |",
            f"| Avg baseline net return % | {_format_float(summary['avg_baseline_net_return_pct'])} |",
            f"| Avg stress net return % | {_format_float(summary['avg_stress_net_return_pct'])} |",
            f"| Avg baseline active return % | {_format_float(summary['avg_baseline_active_return_pct'])} |",
            "",
            "## Attribution Status Counts",
            "",
            "| Status | Count |",
            "| --- | ---: |",
        ]
    )
    for status, count in summary["status_counts"].items():
        lines.append(f"| `{status}` | {count} |")
    if not summary["status_counts"]:
        lines.append("| `none` | 0 |")

    lines.extend(
        [
            "",
            "## Date-Horizon Attribution",
            "",
            "| Date | Horizon | Status | Gross % | Baseline cost % | Baseline net % | Benchmark % | Baseline active % | Cash weight | Notes |",
            "| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
        ]
    )
    for row in rows:
        lines.append(
            f"| {row.date} | {row.horizon} | `{row.attribution_status}` | {_format_float(row.gross_return_pct)} | "
            f"{_format_float(row.baseline_cost_pct)} | {_format_float(row.baseline_net_return_pct)} | "
            f"{_format_float(row.benchmark_return_pct)} | {_format_float(row.baseline_active_return_pct)} | "
            f"{_format_weight(row.cash_weight)} | {';'.join(row.notes)} |"
        )

    lines.extend(
        [
            "",
            "## Guardrails",
            "",
            "- Costs use local assumption rows only; `broker_fee_override_required=true` means actual KIS account/channel fees are still missing.",
            "- Baseline and stress cost estimates are date/horizon diagnostics, not execution fills.",
            "- Benchmark-active return uses local benchmark smoke rows already joined into PnL smoke; it is not production benchmark attribution.",
            "- Cash return is assumed to be zero for this smoke, and cash drag is reported only as a diagnostic.",
            "- This still does not model rebalance execution timing, taxes beyond round-trip assumptions, delisting/event timing, OOS, or Bias Control.",
            "- Keep `Backtest readiness` at `hold` until historical `Point-in-Time` status coverage, actual costs, production benchmark attribution, OOS, and Bias Control pass.",
            "- Keep `Live trading readiness` at `blocked`; this script never creates order intents.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Compute paper-only Backtest attribution smoke diagnostics.")
    parser.add_argument("--pnl-input", required=True, type=Path)
    parser.add_argument("--assumptions", default=DEFAULT_ASSUMPTIONS, type=Path)
    parser.add_argument("--csv-output", type=Path)
    parser.add_argument("--report-output", type=Path)
    args = parser.parse_args()

    try:
        fields, pnl_rows = _read_csv(args.pnl_input, "PnL smoke")
        _require_columns(fields, REQUIRED_PNL_FIELDS, "PnL smoke")
        assumptions = _load_yaml(args.assumptions)
        rows, summary = build_attribution_rows(pnl_rows=pnl_rows, assumptions=assumptions)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc

    if args.csv_output:
        write_csv(rows, args.csv_output)
    report = render_report(
        rows=rows,
        summary=summary,
        pnl_input=args.pnl_input,
        assumptions_input=args.assumptions,
        csv_output=args.csv_output,
    )
    if args.report_output:
        write_text_lf(args.report_output, report)
    else:
        print(report, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
