"""Compute paper-only Backtest PnL smoke diagnostics.

This joins local portfolio target rows to local forward-return rows. It is a
diagnostic bridge between Signal Candidate plumbing and a real Backtest engine:
no broker/API calls, no order intents, and no costs. Benchmark returns can be
joined as an optional diagnostic comparison, but this is still not a Backtest.
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from statistics import mean

try:
    from quant_io import write_text_lf
except ModuleNotFoundError:  # pragma: no cover - used when imported as scripts.* in tests.
    from scripts.quant_io import write_text_lf


DEFAULT_HORIZONS = (1,)
TARGET_MODE = "paper_portfolio_target_smoke_only"
FORWARD_MODE = "paper_forward_return_smoke_only"
PNL_MODE = "paper_backtest_pnl_smoke_only"
BENCHMARK_MODE = "paper_benchmark_return_smoke_only"


@dataclass(frozen=True)
class PnlSmokeRow:
    target: dict[str, str]
    horizon: int
    evaluation_status: str
    target_weight: float
    forward_date: str = ""
    raw_forward_return_pct: float | None = None
    weighted_return_contribution_pct: float | None = None
    benchmark_label: str = ""
    benchmark_join_status: str = "not_supplied"
    benchmark_return_pct: float | None = None
    excess_return_pct: float | None = None
    weighted_excess_return_contribution_pct: float | None = None


@dataclass(frozen=True)
class DateHorizonDiagnostic:
    date: str
    horizon: int
    target_rows: int
    complete_rows: int
    gross_target_weight: float
    covered_gross_weight: float
    missing_gross_weight: float
    weighted_return_pct: float


def _read_csv(path: Path, required: set[str], label: str) -> list[dict[str, str]]:
    if not path.exists():
        raise ValueError(f"{label} CSV not found: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = [{key: (value or "").strip() for key, value in row.items()} for row in csv.DictReader(handle)]
    if not rows:
        raise ValueError(f"{label} CSV has no rows: {path}")
    missing = required - set(rows[0])
    if missing:
        raise ValueError(f"{label} CSV missing required columns: {', '.join(sorted(missing))}")
    return rows


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
        return int(float(str(value or "").strip()))
    except ValueError:
        return None


def _parse_horizons(value: str) -> tuple[int, ...]:
    horizons: list[int] = []
    for token in value.split(","):
        text = token.strip()
        if not text:
            continue
        parsed = _parse_int(text)
        if parsed is None or parsed <= 0:
            raise ValueError(f"invalid horizon: {text}")
        horizons.append(parsed)
    if not horizons:
        raise ValueError("at least one horizon is required")
    return tuple(dict.fromkeys(horizons))


def _target_key(row: dict[str, str]) -> tuple[str, str]:
    return (row.get("date", "").strip(), row.get("code", "").strip().upper())


def _forward_key(row: dict[str, str]) -> tuple[str, str, int]:
    horizon = _parse_int(row.get("horizon_trading_days", ""))
    return (row.get("date", "").strip(), row.get("code", "").strip().upper(), horizon or 0)


def _benchmark_key(row: dict[str, str]) -> tuple[str, str, int]:
    horizon = _parse_int(row.get("horizon_trading_days", ""))
    return (row.get("date", "").strip(), row.get("benchmark", "").strip().upper(), horizon or 0)


def _validate_targets(target_rows: list[dict[str, str]]) -> None:
    bad_order_intents = sum(1 for row in target_rows if row.get("order_intent_generated", "").lower() != "false")
    if bad_order_intents:
        raise ValueError("portfolio target rows must not contain order intents")
    non_long = sum(1 for row in target_rows if row.get("target_side", "") != "LONG")
    if non_long:
        raise ValueError("portfolio target rows must be LONG-only for this smoke")
    bad_modes = sorted({row.get("target_mode", "") for row in target_rows if row.get("target_mode", "") != TARGET_MODE})
    if bad_modes:
        raise ValueError(f"unexpected target modes: {', '.join(bad_modes)}")


def _forward_index(forward_rows: list[dict[str, str]]) -> dict[tuple[str, str, int], dict[str, str]]:
    index: dict[tuple[str, str, int], dict[str, str]] = {}
    counts = Counter(_forward_key(row) for row in forward_rows)
    duplicates = [key for key, count in counts.items() if key[0] and key[1] and key[2] and count > 1]
    if duplicates:
        raise ValueError("forward-return rows contain duplicate date/code/horizon keys")
    for row in forward_rows:
        key = _forward_key(row)
        if key[0] and key[1] and key[2]:
            index[key] = row
    return index


def _benchmark_index(benchmark_rows: list[dict[str, str]]) -> dict[tuple[str, str, int], dict[str, str]]:
    index: dict[tuple[str, str, int], dict[str, str]] = {}
    counts = Counter(_benchmark_key(row) for row in benchmark_rows)
    duplicates = [key for key, count in counts.items() if key[0] and key[1] and key[2] and count > 1]
    if duplicates:
        raise ValueError("benchmark-return rows contain duplicate date/benchmark/horizon keys")
    for row in benchmark_rows:
        key = _benchmark_key(row)
        if key[0] and key[1] and key[2]:
            index[key] = row
    return index


def compute_pnl_smoke(
    target_rows: list[dict[str, str]],
    forward_rows: list[dict[str, str]],
    horizons: tuple[int, ...] = DEFAULT_HORIZONS,
    benchmark_rows: list[dict[str, str]] | None = None,
    benchmark_label: str = "KOSPI",
) -> tuple[list[PnlSmokeRow], list[DateHorizonDiagnostic]]:
    if not horizons:
        raise ValueError("at least one horizon is required")
    if any(horizon <= 0 for horizon in horizons):
        raise ValueError("horizons must be positive")
    _validate_targets(target_rows)
    forward_by_key = _forward_index(forward_rows)
    benchmark_label = benchmark_label.strip().upper()
    benchmark_by_key = _benchmark_index(benchmark_rows or []) if benchmark_rows is not None else {}

    rows: list[PnlSmokeRow] = []
    for target in target_rows:
        date, code = _target_key(target)
        target_weight = _parse_float(target.get("target_weight", "")) or 0.0
        for horizon in horizons:
            forward = forward_by_key.get((date, code, horizon))
            if forward is None:
                rows.append(PnlSmokeRow(target, horizon, "missing_forward_row", target_weight, benchmark_label=benchmark_label))
                continue
            status = forward.get("evaluation_status", "")
            if forward.get("evaluation_mode", "") and forward.get("evaluation_mode", "") != FORWARD_MODE:
                status = "unexpected_forward_mode"
            raw_return = _parse_float(forward.get("raw_forward_return_pct", ""))
            if status == "complete" and raw_return is None:
                status = "bad_forward_return"
            contribution = target_weight * raw_return if status == "complete" and raw_return is not None else None
            benchmark_join_status = "not_supplied"
            benchmark_return = None
            excess_return = None
            weighted_excess = None
            if benchmark_rows is not None:
                benchmark = benchmark_by_key.get((date, benchmark_label, horizon))
                if benchmark is None:
                    benchmark_join_status = "missing_benchmark_return"
                elif benchmark.get("evaluation_mode", "") and benchmark.get("evaluation_mode", "") != BENCHMARK_MODE:
                    benchmark_join_status = "unexpected_benchmark_mode"
                else:
                    benchmark_join_status = benchmark.get("evaluation_status", "") or "missing_benchmark_status"
                    benchmark_return = _parse_float(benchmark.get("benchmark_return_pct", ""))
                    if benchmark_join_status == "complete" and benchmark_return is None:
                        benchmark_join_status = "bad_benchmark_return"
                    if status == "complete" and raw_return is not None and benchmark_join_status == "complete" and benchmark_return is not None:
                        excess_return = raw_return - benchmark_return
                        weighted_excess = target_weight * excess_return
            rows.append(
                PnlSmokeRow(
                    target=target,
                    horizon=horizon,
                    evaluation_status=status or "missing_forward_status",
                    target_weight=target_weight,
                    forward_date=forward.get("forward_date", ""),
                    raw_forward_return_pct=raw_return,
                    weighted_return_contribution_pct=contribution,
                    benchmark_label=benchmark_label,
                    benchmark_join_status=benchmark_join_status,
                    benchmark_return_pct=benchmark_return,
                    excess_return_pct=excess_return,
                    weighted_excess_return_contribution_pct=weighted_excess,
                )
            )

    return rows, _date_horizon_diagnostics(rows)


def _date_horizon_diagnostics(rows: list[PnlSmokeRow]) -> list[DateHorizonDiagnostic]:
    grouped: dict[tuple[str, int], list[PnlSmokeRow]] = defaultdict(list)
    for row in rows:
        grouped[(row.target.get("date", ""), row.horizon)].append(row)

    diagnostics: list[DateHorizonDiagnostic] = []
    for (date, horizon), group in sorted(grouped.items()):
        gross = sum(row.target_weight for row in group)
        complete = [row for row in group if row.evaluation_status == "complete"]
        covered = sum(row.target_weight for row in complete)
        contribution = sum(row.weighted_return_contribution_pct or 0.0 for row in complete)
        diagnostics.append(
            DateHorizonDiagnostic(
                date=date,
                horizon=horizon,
                target_rows=len(group),
                complete_rows=len(complete),
                gross_target_weight=gross,
                covered_gross_weight=covered,
                missing_gross_weight=max(0.0, gross - covered),
                weighted_return_pct=contribution,
            )
        )
    return diagnostics


def _format_float(value: float | None) -> str:
    if value is None:
        return ""
    return f"{value:.4f}"


def _format_weight(value: float) -> str:
    return f"{value:.6f}"


def write_csv(rows: list[PnlSmokeRow], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = (
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
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            target = row.target
            writer.writerow(
                {
                    "date": target.get("date", ""),
                    "code": target.get("code", ""),
                    "stock_name": target.get("stock_name", ""),
                    "market": target.get("market", ""),
                    "horizon_trading_days": str(row.horizon),
                    "evaluation_status": row.evaluation_status,
                    "forward_date": row.forward_date,
                    "target_side": target.get("target_side", ""),
                    "target_weight": _format_weight(row.target_weight),
                    "raw_forward_return_pct": _format_float(row.raw_forward_return_pct),
                    "weighted_return_contribution_pct": _format_float(row.weighted_return_contribution_pct),
                    "benchmark_label": row.benchmark_label,
                    "benchmark_join_status": row.benchmark_join_status,
                    "benchmark_return_pct": _format_float(row.benchmark_return_pct),
                    "excess_return_pct": _format_float(row.excess_return_pct),
                    "weighted_excess_return_contribution_pct": _format_float(row.weighted_excess_return_contribution_pct),
                    "source_signal_state": target.get("source_signal_state", ""),
                    "target_mode": target.get("target_mode", ""),
                    "pnl_mode": PNL_MODE,
                    "order_intent_generated": "false",
                }
            )


def summarize(rows: list[PnlSmokeRow], diagnostics: list[DateHorizonDiagnostic]) -> dict[str, object]:
    status_counts = Counter(row.evaluation_status for row in rows)
    benchmark_status_counts = Counter(row.benchmark_join_status for row in rows)
    horizon_counts = Counter(str(row.horizon) for row in rows)
    by_horizon: dict[str, list[float]] = defaultdict(list)
    covered_by_horizon: dict[str, list[float]] = defaultdict(list)
    excess_by_horizon: dict[str, list[float]] = defaultdict(list)
    for diagnostic in diagnostics:
        key = str(diagnostic.horizon)
        by_horizon[key].append(diagnostic.weighted_return_pct)
        covered_by_horizon[key].append(diagnostic.covered_gross_weight)
    for row in rows:
        if row.weighted_excess_return_contribution_pct is not None:
            excess_by_horizon[str(row.horizon)].append(row.weighted_excess_return_contribution_pct)
    complete_rows = status_counts.get("complete", 0)
    return {
        "pnl_smoke_status": "pass_smoke" if rows and complete_rows > 0 else "hold",
        "rows": len(rows),
        "target_dates": len({row.target.get("date", "") for row in rows if row.target.get("date", "")}),
        "status_counts": dict(sorted(status_counts.items())),
        "benchmark_join_status_counts": dict(sorted(benchmark_status_counts.items())),
        "benchmark_joined_rows": benchmark_status_counts.get("complete", 0),
        "horizon_counts": dict(sorted(horizon_counts.items())),
        "complete_rows": complete_rows,
        "date_horizon_rows": len(diagnostics),
        "avg_weighted_return_by_horizon": {key: mean(values) for key, values in sorted(by_horizon.items()) if values},
        "avg_covered_gross_by_horizon": {key: mean(values) for key, values in sorted(covered_by_horizon.items()) if values},
        "avg_weighted_excess_by_horizon": {key: mean(values) for key, values in sorted(excess_by_horizon.items()) if values},
    }


def _wikilink(path: Path) -> str:
    rendered = path.as_posix()
    return f"[[{rendered}|{rendered}]]"


def render_report(
    *,
    rows: list[PnlSmokeRow],
    diagnostics: list[DateHorizonDiagnostic],
    summary: dict[str, object],
    targets_input: Path,
    forward_returns_input: Path,
    benchmark_returns_input: Path | None,
    benchmark_label: str,
    horizons: tuple[int, ...],
    csv_output: Path | None,
) -> str:
    lines = [
        "# Backtest PnL Smoke",
        "",
        f"- Portfolio-target input: {_wikilink(targets_input)}",
        f"- Forward-return input: {_wikilink(forward_returns_input)}",
        f"- Benchmark-return input: {_wikilink(benchmark_returns_input) if benchmark_returns_input else '`not_supplied`'}",
        f"- Benchmark label: `{benchmark_label}`",
        f"- Horizons: `{','.join(str(horizon) for horizon in horizons)}` trading days",
        f"- Mode: `{PNL_MODE}`",
        "- KIS API call: `false`",
        "- KRX API call: `false`",
        "- Order intent generated: `false`",
        f"- PnL smoke status: `{summary['pnl_smoke_status']}`",
        "- Backtest readiness: `hold`",
        "- Live trading readiness: `blocked`",
    ]
    if csv_output:
        lines.append(f"- Machine-readable rows: {_wikilink(csv_output)}")

    lines.extend(
        [
            "",
            "## Summary",
            "",
            "| Metric | Value |",
            "| --- | ---: |",
            f"| PnL rows | {summary['rows']} |",
            f"| Complete rows | {summary['complete_rows']} |",
            f"| Benchmark joined rows | {summary['benchmark_joined_rows']} |",
            f"| Target dates | {summary['target_dates']} |",
            f"| Date-horizon rows | {summary['date_horizon_rows']} |",
            "",
            "## Status Counts",
            "",
            "| Status | Count |",
            "| --- | ---: |",
        ]
    )
    for status, count in dict(summary["status_counts"]).items():
        lines.append(f"| `{status}` | {count} |")
    if not summary["status_counts"]:
        lines.append("| `none` | 0 |")

    lines.extend(
        [
            "",
            "## Benchmark Join Status Counts",
            "",
            "| Status | Count |",
            "| --- | ---: |",
        ]
    )
    for status, count in dict(summary["benchmark_join_status_counts"]).items():
        lines.append(f"| `{status}` | {count} |")
    if not summary["benchmark_join_status_counts"]:
        lines.append("| `none` | 0 |")

    lines.extend(
        [
            "",
            "## Horizon Diagnostics",
            "",
            "| Horizon | Avg weighted return % | Avg weighted excess vs benchmark % | Avg covered gross weight |",
            "| ---: | ---: | ---: | ---: |",
        ]
    )
    returns = dict(summary["avg_weighted_return_by_horizon"])
    covered = dict(summary["avg_covered_gross_by_horizon"])
    excess = dict(summary["avg_weighted_excess_by_horizon"])
    for horizon in sorted({*returns.keys(), *covered.keys(), *excess.keys()}, key=int):
        lines.append(
            f"| {horizon} | {_format_float(returns.get(horizon))} | {_format_float(excess.get(horizon))} | "
            f"{_format_weight(float(covered.get(horizon, 0.0)))} |"
        )
    if not returns and not covered and not excess:
        lines.append("| `none` |  |  |  |")

    lines.extend(
        [
            "",
            "## Date-Horizon Diagnostics",
            "",
            "| Date | Horizon | Target rows | Complete rows | Gross target weight | Covered weight | Missing weight | Weighted return % |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for item in diagnostics:
        lines.append(
            f"| {item.date} | {item.horizon} | {item.target_rows} | {item.complete_rows} | "
            f"{_format_weight(item.gross_target_weight)} | {_format_weight(item.covered_gross_weight)} | "
            f"{_format_weight(item.missing_gross_weight)} | {_format_float(item.weighted_return_pct)} |"
        )

    complete_sample = [row for row in rows if row.evaluation_status == "complete"][-30:]
    lines.extend(
        [
            "",
            "## Complete Row Sample",
            "",
            "| Signal date | Horizon | Forward date | Code | Company | Weight | Raw return % | Benchmark % | Excess % | Contribution % | Excess contribution % |",
            "| --- | ---: | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in complete_sample:
        target = row.target
        lines.append(
            f"| {target.get('date', '')} | {row.horizon} | {row.forward_date} | `{target.get('code', '')}` | "
            f"{target.get('stock_name', '')} | {_format_weight(row.target_weight)} | "
            f"{_format_float(row.raw_forward_return_pct)} | {_format_float(row.benchmark_return_pct)} | "
            f"{_format_float(row.excess_return_pct)} | {_format_float(row.weighted_return_contribution_pct)} | "
            f"{_format_float(row.weighted_excess_return_contribution_pct)} |"
        )

    lines.extend(
        [
            "",
            "## Guardrails",
            "",
            "- This is a PnL smoke diagnostic, not a production Backtest result.",
            "- Weighted return uses target weight multiplied by raw forward return; missing forward rows are not filled as zero.",
            "- Benchmark excess return is optional diagnostic math, not a production benchmark attribution engine.",
            "- This does not model transaction costs, slippage, taxes, cash drag, rebalance execution, or delisting/event timing.",
            "- Keep `Backtest readiness` at `hold` until historical `Point-in-Time` status coverage, cost model, benchmark attribution, OOS, and Bias Control pass.",
            "- Keep `Live trading readiness` at `blocked`; this script never creates order intents.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Compute paper-only Backtest PnL smoke diagnostics.")
    parser.add_argument("--targets-input", required=True, type=Path)
    parser.add_argument("--forward-returns-input", required=True, type=Path)
    parser.add_argument("--benchmark-returns-input", type=Path)
    parser.add_argument("--benchmark-label", default="KOSPI")
    parser.add_argument("--horizons", default=",".join(str(value) for value in DEFAULT_HORIZONS))
    parser.add_argument("--csv-output", type=Path)
    parser.add_argument("--report-output", type=Path)
    args = parser.parse_args()

    try:
        horizons = _parse_horizons(args.horizons)
        target_rows = _read_csv(
            args.targets_input,
            {
                "date",
                "code",
                "stock_name",
                "target_side",
                "target_weight",
                "target_mode",
                "order_intent_generated",
            },
            "Portfolio target",
        )
        forward_rows = _read_csv(
            args.forward_returns_input,
            {
                "date",
                "code",
                "horizon_trading_days",
                "evaluation_status",
                "raw_forward_return_pct",
                "evaluation_mode",
            },
            "Forward-return",
        )
        benchmark_rows = (
            _read_csv(
                args.benchmark_returns_input,
                {
                    "date",
                    "benchmark",
                    "horizon_trading_days",
                    "evaluation_status",
                    "benchmark_return_pct",
                    "evaluation_mode",
                },
                "Benchmark-return",
            )
            if args.benchmark_returns_input
            else None
        )
        rows, diagnostics = compute_pnl_smoke(target_rows, forward_rows, horizons, benchmark_rows, args.benchmark_label)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc

    if args.csv_output:
        write_csv(rows, args.csv_output)
    report = render_report(
        rows=rows,
        diagnostics=diagnostics,
        summary=summarize(rows, diagnostics),
        targets_input=args.targets_input,
        forward_returns_input=args.forward_returns_input,
        benchmark_returns_input=args.benchmark_returns_input,
        benchmark_label=args.benchmark_label.strip().upper(),
        horizons=horizons,
        csv_output=args.csv_output,
    )
    if args.report_output:
        write_text_lf(args.report_output, report)
    else:
        print(report, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
