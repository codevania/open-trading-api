"""Compute paper-only benchmark return smoke diagnostics.

This joins local Signal Candidate dates to local KRX OpenAPI index daily rows.
It is not a Backtest, does not call KRX/KIS, and does not approve trading.
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


DEFAULT_HORIZONS = (1, 5)
DEFAULT_BENCHMARKS = "KOSPI=KOSPI:코스피,KOSDAQ=KOSDAQ:코스닥,KOSPI200=KOSPI:코스피 200"
EVALUATION_MODE = "paper_benchmark_return_smoke_only"


@dataclass(frozen=True)
class BenchmarkSpec:
    label: str
    index_class: str
    index_name: str


@dataclass(frozen=True)
class BenchmarkReturnRow:
    signal_date: str
    benchmark: BenchmarkSpec
    horizon: int
    evaluation_status: str
    forward_date: str = ""
    signal_close: float | None = None
    forward_close: float | None = None
    benchmark_return_pct: float | None = None


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
        parsed = float(text)
    except ValueError:
        return None
    if parsed <= 0:
        return None
    return parsed


def _parse_horizons(value: str) -> tuple[int, ...]:
    horizons: list[int] = []
    for token in value.split(","):
        text = token.strip()
        if not text:
            continue
        try:
            horizon = int(text)
        except ValueError as exc:
            raise ValueError(f"invalid horizon: {text}") from exc
        if horizon <= 0:
            raise ValueError("horizons must be positive")
        horizons.append(horizon)
    if not horizons:
        raise ValueError("at least one horizon is required")
    return tuple(dict.fromkeys(horizons))


def _parse_benchmarks(value: str) -> tuple[BenchmarkSpec, ...]:
    specs: list[BenchmarkSpec] = []
    for token in value.split(","):
        text = token.strip()
        if not text:
            continue
        if "=" not in text or ":" not in text:
            raise ValueError(f"invalid benchmark mapping: {text}")
        label, rest = text.split("=", 1)
        index_class, index_name = rest.split(":", 1)
        label = label.strip().upper()
        index_class = index_class.strip().upper()
        index_name = index_name.strip()
        if not label or not index_class or not index_name:
            raise ValueError(f"invalid benchmark mapping: {text}")
        specs.append(BenchmarkSpec(label, index_class, index_name))
    if not specs:
        raise ValueError("at least one benchmark mapping is required")
    labels = [spec.label for spec in specs]
    duplicates = sorted(label for label, count in Counter(labels).items() if count > 1)
    if duplicates:
        raise ValueError("duplicate benchmark labels: " + ", ".join(duplicates))
    return tuple(specs)


def _signal_dates(signal_rows: list[dict[str, str]]) -> list[str]:
    return sorted({row.get("date", "").strip() for row in signal_rows if row.get("date", "").strip()})


def _index_series(
    index_rows: list[dict[str, str]],
    benchmarks: tuple[BenchmarkSpec, ...],
) -> dict[str, list[tuple[str, float]]]:
    by_lookup = {(spec.index_class, spec.index_name): spec for spec in benchmarks}
    values: dict[str, dict[str, float]] = {spec.label: {} for spec in benchmarks}
    for row in index_rows:
        key = (row.get("index_class", "").strip().upper(), row.get("index_name", "").strip())
        spec = by_lookup.get(key)
        if spec is None:
            continue
        date = row.get("date", "").strip()
        close = _parse_float(row.get("close", ""))
        if not date or close is None:
            continue
        if date in values[spec.label]:
            raise ValueError(f"duplicate benchmark date: {spec.label}/{date}")
        values[spec.label][date] = close
    return {label: sorted(rows.items()) for label, rows in values.items()}


def evaluate_benchmark_returns(
    signal_rows: list[dict[str, str]],
    index_rows: list[dict[str, str]],
    benchmarks: tuple[BenchmarkSpec, ...],
    horizons: tuple[int, ...] = DEFAULT_HORIZONS,
) -> list[BenchmarkReturnRow]:
    if not horizons:
        raise ValueError("at least one horizon is required")
    if any(horizon <= 0 for horizon in horizons):
        raise ValueError("horizons must be positive")

    dates = _signal_dates(signal_rows)
    series_by_label = _index_series(index_rows, benchmarks)
    results: list[BenchmarkReturnRow] = []

    for signal_date in dates:
        for spec in benchmarks:
            series = series_by_label.get(spec.label, [])
            date_to_index = {date: index for index, (date, _close) in enumerate(series)}
            signal_index = date_to_index.get(signal_date)
            signal_close = series[signal_index][1] if signal_index is not None else None
            for horizon in horizons:
                if not series:
                    results.append(BenchmarkReturnRow(signal_date, spec, horizon, "missing_benchmark_series"))
                    continue
                if signal_index is None or signal_close is None:
                    results.append(BenchmarkReturnRow(signal_date, spec, horizon, "missing_signal_index"))
                    continue
                forward_index = signal_index + horizon
                if forward_index >= len(series):
                    results.append(BenchmarkReturnRow(signal_date, spec, horizon, "missing_forward_index", signal_close=signal_close))
                    continue
                forward_date, forward_close = series[forward_index]
                benchmark_return = ((forward_close / signal_close) - 1.0) * 100.0
                results.append(
                    BenchmarkReturnRow(
                        signal_date=signal_date,
                        benchmark=spec,
                        horizon=horizon,
                        evaluation_status="complete",
                        forward_date=forward_date,
                        signal_close=signal_close,
                        forward_close=forward_close,
                        benchmark_return_pct=benchmark_return,
                    )
                )
    return results


def _format_float(value: float | None) -> str:
    if value is None:
        return ""
    return f"{value:.4f}"


def write_csv(rows: list[BenchmarkReturnRow], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = (
        "date",
        "benchmark",
        "index_class",
        "index_name",
        "horizon_trading_days",
        "evaluation_status",
        "forward_date",
        "signal_close",
        "forward_close",
        "benchmark_return_pct",
        "evaluation_mode",
    )
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "date": row.signal_date,
                    "benchmark": row.benchmark.label,
                    "index_class": row.benchmark.index_class,
                    "index_name": row.benchmark.index_name,
                    "horizon_trading_days": str(row.horizon),
                    "evaluation_status": row.evaluation_status,
                    "forward_date": row.forward_date,
                    "signal_close": _format_float(row.signal_close),
                    "forward_close": _format_float(row.forward_close),
                    "benchmark_return_pct": _format_float(row.benchmark_return_pct),
                    "evaluation_mode": EVALUATION_MODE,
                }
            )


def summarize(rows: list[BenchmarkReturnRow]) -> dict[str, object]:
    status_counts = Counter(row.evaluation_status for row in rows)
    benchmark_counts = Counter(row.benchmark.label for row in rows)
    horizon_counts = Counter(str(row.horizon) for row in rows)
    complete_by_benchmark_horizon: dict[tuple[str, str], list[float]] = defaultdict(list)
    for row in rows:
        if row.evaluation_status == "complete" and row.benchmark_return_pct is not None:
            complete_by_benchmark_horizon[(row.benchmark.label, str(row.horizon))].append(row.benchmark_return_pct)
    return {
        "rows": len(rows),
        "signal_dates": len({row.signal_date for row in rows}),
        "status_counts": dict(sorted(status_counts.items())),
        "benchmark_counts": dict(sorted(benchmark_counts.items())),
        "horizon_counts": dict(sorted(horizon_counts.items())),
        "complete_rows": status_counts.get("complete", 0),
        "avg_return_by_benchmark_horizon": {
            f"{benchmark}/{horizon}": mean(values) for (benchmark, horizon), values in sorted(complete_by_benchmark_horizon.items()) if values
        },
    }


def _wikilink(path: Path) -> str:
    rendered = path.as_posix()
    return f"[[{rendered}|{rendered}]]"


def render_report(
    *,
    rows: list[BenchmarkReturnRow],
    summary: dict[str, object],
    signals_input: Path,
    index_inputs: list[Path],
    benchmarks: tuple[BenchmarkSpec, ...],
    horizons: tuple[int, ...],
    csv_output: Path | None,
) -> str:
    lines = [
        "# Benchmark Return Smoke",
        "",
        f"- Signal input: {_wikilink(signals_input)}",
        f"- Index inputs: `{len(index_inputs)}`",
        f"- Benchmarks: `{','.join(spec.label for spec in benchmarks)}`",
        f"- Horizons: `{','.join(str(horizon) for horizon in horizons)}` trading days",
        f"- Mode: `{EVALUATION_MODE}`",
        "- KIS API call: `false`",
        "- KRX API call: `false`",
        "- Order intent generated: `false`",
        "- Backtest readiness: `hold`",
        "- Live trading readiness: `blocked`",
    ]
    if csv_output:
        lines.append(f"- Machine-readable rows: {_wikilink(csv_output)}")

    lines.extend(["", "## Index Inputs", "", "| Input |", "| --- |"])
    for path in index_inputs:
        lines.append(f"| {_wikilink(path)} |")

    lines.extend(["", "## Benchmark Mapping", "", "| Benchmark | Index class | Index name |", "| --- | --- | --- |"])
    for spec in benchmarks:
        lines.append(f"| `{spec.label}` | `{spec.index_class}` | {spec.index_name} |")

    lines.extend(
        [
            "",
            "## Summary",
            "",
            f"- Evaluation rows: `{summary['rows']}`",
            f"- Signal dates: `{summary['signal_dates']}`",
            f"- Complete rows: `{summary['complete_rows']}`",
            "",
            "## Status Counts",
            "",
            "| Status | Count |",
            "| --- | ---: |",
        ]
    )
    for status, count in dict(summary["status_counts"]).items():
        lines.append(f"| `{status}` | {count} |")

    lines.extend(["", "## Average Complete Benchmark Returns", "", "| Benchmark / Horizon | Avg return % |", "| --- | ---: |"])
    averages = dict(summary["avg_return_by_benchmark_horizon"])
    for key, value in averages.items():
        lines.append(f"| `{key}` | {_format_float(value)} |")
    if not averages:
        lines.append("| `none` |  |")

    latest_complete = [row for row in rows if row.evaluation_status == "complete"][-30:]
    lines.extend(
        [
            "",
            "## Complete Row Sample",
            "",
            "| Signal date | Horizon | Forward date | Benchmark | Index name | Return % |",
            "| --- | ---: | --- | --- | --- | ---: |",
        ]
    )
    for row in latest_complete:
        lines.append(
            f"| {row.signal_date} | {row.horizon} | {row.forward_date} | `{row.benchmark.label}` | "
            f"{row.benchmark.index_name} | {_format_float(row.benchmark_return_pct)} |"
        )

    lines.extend(
        [
            "",
            "## Guardrails",
            "",
            "- This is benchmark-return coverage/diagnostic smoke, not a Backtest.",
            "- Benchmark rows are not joined to strategy PnL yet.",
            "- Missing forward index rows usually mean the current smoke window ends too soon after a signal date.",
            "- Keep Backtest readiness `hold` until Point-in-Time status coverage, actual costs, benchmark join, OOS, and Bias Control pass.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Compute paper-only benchmark return smoke diagnostics.")
    parser.add_argument("--signals-input", required=True, type=Path)
    parser.add_argument("--index-input", action="append", required=True, type=Path, help="Normalized KRX index_daily.csv. Repeatable.")
    parser.add_argument("--benchmarks", default=DEFAULT_BENCHMARKS)
    parser.add_argument("--horizons", default=",".join(str(value) for value in DEFAULT_HORIZONS))
    parser.add_argument("--csv-output", type=Path)
    parser.add_argument("--report-output", type=Path)
    args = parser.parse_args()

    try:
        horizons = _parse_horizons(args.horizons)
        benchmarks = _parse_benchmarks(args.benchmarks)
        signal_rows = _read_csv(args.signals_input, {"date"}, "Signal Candidate")
        index_rows: list[dict[str, str]] = []
        for path in args.index_input:
            index_rows.extend(_read_csv(path, {"date", "index_class", "index_name", "close"}, "Index daily"))
        rows = evaluate_benchmark_returns(signal_rows, index_rows, benchmarks, horizons)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc

    if args.csv_output:
        write_csv(rows, args.csv_output)
    report = render_report(
        rows=rows,
        summary=summarize(rows),
        signals_input=args.signals_input,
        index_inputs=args.index_input,
        benchmarks=benchmarks,
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
