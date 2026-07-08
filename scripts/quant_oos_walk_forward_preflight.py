"""Build paper-only OOS/Walk-Forward preflight diagnostics.

This script reads already-generated Backtest attribution smoke rows and checks
whether they can be segmented into deterministic temporal folds. It does not
fetch data, optimize parameters, create orders, or promote OOS readiness.
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from statistics import mean
from typing import Any

try:
    from quant_io import write_text_lf
except ModuleNotFoundError:  # pragma: no cover - used when imported as scripts.* in tests.
    from scripts.quant_io import write_text_lf


ATTRIBUTION_MODE = "paper_backtest_attribution_smoke_assumption_only"
OOS_MODE = "paper_oos_walk_forward_preflight_smoke_only"
PASS_STATUS = "pass_smoke_plumbing_only"
REQUIRED_ATTRIBUTION_FIELDS = {
    "date",
    "horizon_trading_days",
    "attribution_status",
    "baseline_net_return_pct",
    "stress_net_return_pct",
    "baseline_active_return_pct",
    "broker_fee_override_required",
    "attribution_mode",
    "order_intent_generated",
}
OUTPUT_FIELDS = (
    "fold_id",
    "horizon_trading_days",
    "fold_status",
    "train_start_date",
    "train_end_date",
    "test_start_date",
    "test_end_date",
    "train_dates",
    "test_dates",
    "train_rows",
    "test_rows",
    "train_avg_baseline_net_return_pct",
    "test_avg_baseline_net_return_pct",
    "test_avg_stress_net_return_pct",
    "test_avg_baseline_active_return_pct",
    "test_positive_baseline_net_dates",
    "test_positive_baseline_net_rate",
    "broker_fee_override_required",
    "oos_mode",
    "order_intent_generated",
    "notes",
)


@dataclass(frozen=True)
class FoldRow:
    fold_id: str
    horizon: int
    fold_status: str
    train_start_date: str
    train_end_date: str
    test_start_date: str
    test_end_date: str
    train_dates: int
    test_dates: int
    train_rows: int
    test_rows: int
    train_avg_baseline_net_return_pct: float | None
    test_avg_baseline_net_return_pct: float | None
    test_avg_stress_net_return_pct: float | None
    test_avg_baseline_active_return_pct: float | None
    test_positive_baseline_net_dates: int
    test_positive_baseline_net_rate: float | None
    broker_fee_override_required: bool
    notes: tuple[str, ...]


def _read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path.exists():
        raise ValueError(f"attribution CSV not found: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = list(reader.fieldnames or [])
        rows = [{key: (value or "").strip() for key, value in row.items()} for row in reader]
    if not rows:
        raise ValueError(f"attribution CSV has no rows: {path}")
    return fields, rows


def _require_columns(fields: list[str]) -> None:
    missing = REQUIRED_ATTRIBUTION_FIELDS - set(fields)
    if missing:
        raise ValueError(f"attribution CSV missing required columns: {', '.join(sorted(missing))}")


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


def _parse_bool(value: Any) -> bool:
    return str(value or "").strip().lower() == "true"


def _format_float(value: float | None) -> str:
    if value is None:
        return ""
    return f"{value:.4f}"


def _valid_date(value: str) -> str:
    try:
        date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"invalid ISO date: {value}") from exc
    return value


def _validate_rows(rows: list[dict[str, str]]) -> None:
    bad_orders = sum(1 for row in rows if row.get("order_intent_generated", "").lower() != "false")
    if bad_orders:
        raise ValueError("attribution rows must not contain order intents")
    bad_modes = sorted({row.get("attribution_mode", "") for row in rows if row.get("attribution_mode", "") != ATTRIBUTION_MODE})
    if bad_modes:
        raise ValueError(f"unexpected attribution modes: {', '.join(bad_modes)}")
    for row in rows:
        _valid_date(row.get("date", ""))
        horizon = _parse_int(row.get("horizon_trading_days", ""))
        if horizon is None or horizon <= 0:
            raise ValueError("horizon_trading_days must be positive")


def _numeric_values(rows: list[dict[str, str]], column: str) -> list[float]:
    return [value for value in (_parse_float(row.get(column, "")) for row in rows) if value is not None]


def _avg(rows: list[dict[str, str]], column: str) -> float | None:
    values = _numeric_values(rows, column)
    return mean(values) if values else None


def build_walk_forward_rows(
    *,
    attribution_rows: list[dict[str, str]],
    min_train_dates: int = 20,
    test_dates: int = 10,
    fold_count: int = 3,
) -> tuple[list[FoldRow], dict[str, Any]]:
    if min_train_dates <= 0:
        raise ValueError("min_train_dates must be positive")
    if test_dates <= 0:
        raise ValueError("test_dates must be positive")
    if fold_count <= 0:
        raise ValueError("fold_count must be positive")

    _validate_rows(attribution_rows)
    grouped: dict[int, list[dict[str, str]]] = {}
    for row in attribution_rows:
        horizon = _parse_int(row.get("horizon_trading_days", ""))
        assert horizon is not None
        grouped.setdefault(horizon, []).append(row)

    fold_rows: list[FoldRow] = []
    hold_reasons: list[str] = []
    for horizon, rows in sorted(grouped.items()):
        dates = sorted({row["date"] for row in rows if row.get("date")})
        required_dates = min_train_dates + test_dates
        if len(dates) < required_dates:
            hold_reasons.append(f"horizon_{horizon}:not_enough_dates:{len(dates)}<{required_dates}")
            continue

        rows_by_date: dict[str, list[dict[str, str]]] = {}
        for row in rows:
            rows_by_date.setdefault(row["date"], []).append(row)

        produced = 0
        for index in range(fold_count):
            train_end_index = min_train_dates + (index * test_dates)
            test_start_index = train_end_index
            test_end_index = test_start_index + test_dates
            if test_end_index > len(dates):
                hold_reasons.append(f"horizon_{horizon}:fold_{index + 1}:insufficient_tail_dates")
                break

            train_window = dates[:train_end_index]
            test_window = dates[test_start_index:test_end_index]
            train_rows = [row for day in train_window for row in rows_by_date.get(day, [])]
            test_rows = [row for day in test_window for row in rows_by_date.get(day, [])]
            all_window_rows = train_rows + test_rows
            non_pass_rows = sum(1 for row in all_window_rows if row.get("attribution_status", "") != "pass_smoke_assumption_only")
            broker_fee_required = any(_parse_bool(row.get("broker_fee_override_required", "")) for row in all_window_rows)
            notes: list[str] = []
            if non_pass_rows:
                notes.append(f"attribution_rows_not_pass:{non_pass_rows}")
            if broker_fee_required:
                notes.append("broker_fee_override_required")
            notes.append("point_in_time_status_coverage_not_historical_complete")
            notes.append("production_backtest_not_wired")

            test_baseline_values = _numeric_values(test_rows, "baseline_net_return_pct")
            positive_dates = sum(1 for value in test_baseline_values if value > 0)
            fold_status = PASS_STATUS if train_rows and test_rows and non_pass_rows == 0 else "hold"
            fold_rows.append(
                FoldRow(
                    fold_id=f"wf_{index + 1:02d}",
                    horizon=horizon,
                    fold_status=fold_status,
                    train_start_date=train_window[0],
                    train_end_date=train_window[-1],
                    test_start_date=test_window[0],
                    test_end_date=test_window[-1],
                    train_dates=len(train_window),
                    test_dates=len(test_window),
                    train_rows=len(train_rows),
                    test_rows=len(test_rows),
                    train_avg_baseline_net_return_pct=_avg(train_rows, "baseline_net_return_pct"),
                    test_avg_baseline_net_return_pct=_avg(test_rows, "baseline_net_return_pct"),
                    test_avg_stress_net_return_pct=_avg(test_rows, "stress_net_return_pct"),
                    test_avg_baseline_active_return_pct=_avg(test_rows, "baseline_active_return_pct"),
                    test_positive_baseline_net_dates=positive_dates,
                    test_positive_baseline_net_rate=(positive_dates / len(test_baseline_values)) if test_baseline_values else None,
                    broker_fee_override_required=broker_fee_required,
                    notes=tuple(notes),
                )
            )
            produced += 1

        if produced < fold_count:
            hold_reasons.append(f"horizon_{horizon}:folds_produced:{produced}<{fold_count}")

    status_counts = Counter(row.fold_status for row in fold_rows)
    overall_status = PASS_STATUS if fold_rows and not status_counts.get("hold") else "hold"
    broker_fee_override_required = any(_parse_bool(row.get("broker_fee_override_required", "")) for row in attribution_rows)
    test_baseline_averages = [
        row.test_avg_baseline_net_return_pct for row in fold_rows if row.test_avg_baseline_net_return_pct is not None
    ]
    test_active_averages = [
        row.test_avg_baseline_active_return_pct for row in fold_rows if row.test_avg_baseline_active_return_pct is not None
    ]
    summary = {
        "oos_walk_forward_status": overall_status,
        "oos_readiness": "hold",
        "backtest_readiness": "hold",
        "live_trading_readiness": "blocked",
        "fold_rows": len(fold_rows),
        "attribution_rows": len(attribution_rows),
        "date_count": len({row.get("date", "") for row in attribution_rows if row.get("date", "")}),
        "horizon_count": len(grouped),
        "status_counts": dict(sorted(status_counts.items())),
        "min_train_dates": min_train_dates,
        "test_dates": test_dates,
        "requested_fold_count": fold_count,
        "avg_test_baseline_net_return_pct": mean(test_baseline_averages) if test_baseline_averages else None,
        "avg_test_baseline_active_return_pct": mean(test_active_averages) if test_active_averages else None,
        "broker_fee_override_required": broker_fee_override_required,
        "hold_reasons": sorted(set(hold_reasons)),
    }
    return fold_rows, summary


def write_csv(rows: list[FoldRow], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "fold_id": row.fold_id,
                    "horizon_trading_days": str(row.horizon),
                    "fold_status": row.fold_status,
                    "train_start_date": row.train_start_date,
                    "train_end_date": row.train_end_date,
                    "test_start_date": row.test_start_date,
                    "test_end_date": row.test_end_date,
                    "train_dates": str(row.train_dates),
                    "test_dates": str(row.test_dates),
                    "train_rows": str(row.train_rows),
                    "test_rows": str(row.test_rows),
                    "train_avg_baseline_net_return_pct": _format_float(row.train_avg_baseline_net_return_pct),
                    "test_avg_baseline_net_return_pct": _format_float(row.test_avg_baseline_net_return_pct),
                    "test_avg_stress_net_return_pct": _format_float(row.test_avg_stress_net_return_pct),
                    "test_avg_baseline_active_return_pct": _format_float(row.test_avg_baseline_active_return_pct),
                    "test_positive_baseline_net_dates": str(row.test_positive_baseline_net_dates),
                    "test_positive_baseline_net_rate": _format_float(row.test_positive_baseline_net_rate),
                    "broker_fee_override_required": str(row.broker_fee_override_required).lower(),
                    "oos_mode": OOS_MODE,
                    "order_intent_generated": "false",
                    "notes": ";".join(row.notes),
                }
            )


def _wikilink(path: Path) -> str:
    rendered = path.as_posix()
    return f"[[{rendered}|{rendered}]]"


def render_report(
    *,
    rows: list[FoldRow],
    summary: dict[str, Any],
    attribution_input: Path,
    csv_output: Path | None,
) -> str:
    lines = [
        "# OOS Walk-Forward Preflight",
        "",
        f"- Attribution input: {_wikilink(attribution_input)}",
        f"- Preflight mode: `{OOS_MODE}`",
        f"- OOS/WF preflight status: `{summary['oos_walk_forward_status']}`",
        f"- OOS readiness: `{summary['oos_readiness']}`",
        f"- Backtest readiness: `{summary['backtest_readiness']}`",
        f"- Live trading readiness: `{summary['live_trading_readiness']}`",
        "- KIS API call: `false`",
        "- KRX API call: `false`",
        "- Order intent generated: `false`",
        "- Interpretation: temporal fold plumbing smoke only, not an OOS or production `Backtest` result",
    ]
    if csv_output is not None:
        lines.append(f"- Machine-readable folds: {_wikilink(csv_output)}")

    lines.extend(
        [
            "",
            "## Summary",
            "",
            "| Metric | Value |",
            "| --- | ---: |",
            f"| Attribution rows | {summary['attribution_rows']} |",
            f"| Fold rows | {summary['fold_rows']} |",
            f"| Dates | {summary['date_count']} |",
            f"| Horizons | {summary['horizon_count']} |",
            f"| Min train dates | {summary['min_train_dates']} |",
            f"| Test dates per fold | {summary['test_dates']} |",
            f"| Requested folds | {summary['requested_fold_count']} |",
            f"| Broker fee override required | `{str(summary['broker_fee_override_required']).lower()}` |",
            f"| Avg test baseline net return % | {_format_float(summary['avg_test_baseline_net_return_pct'])} |",
            f"| Avg test baseline active return % | {_format_float(summary['avg_test_baseline_active_return_pct'])} |",
            "",
            "## Fold Status Counts",
            "",
            "| Status | Count |",
            "| --- | ---: |",
        ]
    )
    for status, count in summary["status_counts"].items():
        lines.append(f"| `{status}` | {count} |")
    if not summary["status_counts"]:
        lines.append("| `none` | 0 |")

    if summary["hold_reasons"]:
        lines.extend(["", "## Hold Reasons", ""])
        for reason in summary["hold_reasons"]:
            lines.append(f"- `{reason}`")

    lines.extend(
        [
            "",
            "## Walk-Forward Folds",
            "",
            "| Fold | Horizon | Status | Train | Test | Train avg net % | Test avg net % | Test avg active % | Test positive rate | Notes |",
            "| --- | ---: | --- | --- | --- | ---: | ---: | ---: | ---: | --- |",
        ]
    )
    for row in rows:
        train_window = f"{row.train_start_date}..{row.train_end_date}"
        test_window = f"{row.test_start_date}..{row.test_end_date}"
        lines.append(
            f"| `{row.fold_id}` | {row.horizon} | `{row.fold_status}` | {train_window} | {test_window} | "
            f"{_format_float(row.train_avg_baseline_net_return_pct)} | "
            f"{_format_float(row.test_avg_baseline_net_return_pct)} | "
            f"{_format_float(row.test_avg_baseline_active_return_pct)} | "
            f"{_format_float(row.test_positive_baseline_net_rate)} | {';'.join(row.notes)} |"
        )

    lines.extend(
        [
            "",
            "## Guardrails",
            "",
            "- This preflight only checks deterministic temporal segmentation of attribution smoke rows.",
            "- It does not optimize parameters, choose a strategy, or validate production OOS performance.",
            "- It inherits assumption-only costs; `broker_fee_override_required=true` still blocks production interpretation.",
            "- It inherits the current `Point-in-Time` status coverage gap and therefore keeps OOS readiness at `hold`.",
            "- Keep `Backtest readiness` at `hold` until historical `Point-in-Time` status coverage, actual costs, production benchmark attribution, OOS, and Bias Control pass.",
            "- Keep `Live trading readiness` at `blocked`; this script never creates order intents.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Build paper-only OOS/Walk-Forward preflight diagnostics.")
    parser.add_argument("--attribution-input", required=True, type=Path)
    parser.add_argument("--csv-output", type=Path)
    parser.add_argument("--report-output", type=Path)
    parser.add_argument("--min-train-dates", default=20, type=int)
    parser.add_argument("--test-dates", default=10, type=int)
    parser.add_argument("--fold-count", default=3, type=int)
    args = parser.parse_args()

    try:
        fields, attribution_rows = _read_csv(args.attribution_input)
        _require_columns(fields)
        rows, summary = build_walk_forward_rows(
            attribution_rows=attribution_rows,
            min_train_dates=args.min_train_dates,
            test_dates=args.test_dates,
            fold_count=args.fold_count,
        )
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc

    if args.csv_output:
        write_csv(rows, args.csv_output)
    report = render_report(
        rows=rows,
        summary=summary,
        attribution_input=args.attribution_input,
        csv_output=args.csv_output,
    )
    if args.report_output:
        write_text_lf(args.report_output, report)
    else:
        print(report, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
