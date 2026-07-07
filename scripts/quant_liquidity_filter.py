"""Apply a paper/smoke Liquidity Filter to current KRX Universe rows.

This script reads an already-built Universe CSV and already-saved KIS daily
raw JSON files. It does not call KIS, place orders, or create a historical
Point-in-Time Universe.
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from quant_io import write_text_lf
from quant_smoke_validate import _as_float, _extract_rows, _load_json, _symbol_from_path


DEFAULT_LOOKBACK = 20
DEFAULT_MIN_AVG_TRADING_VALUE_KRW = 1_000_000_000


@dataclass(frozen=True)
class LiquidityMetric:
    status: str
    reason: str
    avg_trading_value_20d_krw: float | None
    rows_available: int
    rows_used: int
    latest_date: str | None
    raw_path: Path | None


@dataclass(frozen=True)
class LiquidityRow:
    source: dict[str, str]
    base_status: str
    base_reason: str
    status: str
    reason: str
    metric: LiquidityMetric


def _normalize_code(value: Any) -> str:
    return str(value or "").strip().upper()


def _read_universe_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ValueError(f"universe CSV has no rows: {path}")
    required = {"code", "name", "status", "reason"}
    missing = required - set(rows[0])
    if missing:
        raise ValueError(f"universe CSV missing required columns: {', '.join(sorted(missing))}")
    return rows


def _find_raw_files(raw_dirs: list[Path]) -> dict[str, Path]:
    files: dict[str, Path] = {}
    for raw_dir in raw_dirs:
        if not raw_dir.exists():
            raise ValueError(f"raw dir not found: {raw_dir}")
        candidates = sorted(raw_dir.glob("*.daily.raw.json"))
        candidates.extend(sorted(raw_dir.glob("**/inquire_daily_itemchartprice.json")))
        for path in candidates:
            files[_normalize_code(_symbol_from_path(path))] = path
    return files


def calculate_liquidity_metric(path: Path, lookback: int) -> LiquidityMetric:
    payload = _load_json(path)
    rows = _extract_rows(payload)
    if not rows:
        return LiquidityMetric("data_insufficient", "liquidity_no_daily_rows", None, 0, 0, None, path)

    try:
        ordered = sorted(rows, key=lambda row: str(row["stck_bsop_date"]))
    except KeyError:
        return LiquidityMetric("data_insufficient", "liquidity_date_missing", None, len(rows), 0, None, path)

    latest_date = str(ordered[-1].get("stck_bsop_date", ""))
    if len(ordered) < lookback:
        return LiquidityMetric(
            "data_insufficient",
            "liquidity_trading_value_history_insufficient",
            None,
            len(ordered),
            0,
            latest_date,
            path,
        )

    recent = ordered[-lookback:]
    try:
        values = [_as_float(row["acml_tr_pbmn"]) for row in recent]
    except (KeyError, ValueError):
        return LiquidityMetric(
            "data_insufficient",
            "liquidity_trading_value_missing_or_invalid",
            None,
            len(ordered),
            0,
            latest_date,
            path,
        )

    return LiquidityMetric(
        "calculated",
        "ok",
        sum(values) / len(values),
        len(ordered),
        len(values),
        latest_date,
        path,
    )


def apply_liquidity_filter(
    universe_rows: list[dict[str, str]],
    raw_files: dict[str, Path],
    lookback: int,
    min_avg_trading_value_krw: float,
) -> list[LiquidityRow]:
    rows: list[LiquidityRow] = []
    for source in universe_rows:
        code = _normalize_code(source.get("code"))
        base_status = source.get("status", "")
        base_reason = source.get("reason", "")

        if base_status != "include":
            metric = LiquidityMetric(
                "not_evaluated_preexisting_exclude",
                "pre_liquidity_exclude",
                None,
                0,
                0,
                None,
                None,
            )
            rows.append(LiquidityRow(source, base_status, base_reason, base_status, base_reason, metric))
            continue

        raw_path = raw_files.get(code)
        if raw_path is None:
            metric = LiquidityMetric("data_missing", "liquidity_raw_missing", None, 0, 0, None, None)
            rows.append(LiquidityRow(source, base_status, base_reason, "exclude", metric.reason, metric))
            continue

        metric = calculate_liquidity_metric(raw_path, lookback)
        if metric.avg_trading_value_20d_krw is None:
            rows.append(LiquidityRow(source, base_status, base_reason, "exclude", metric.reason, metric))
        elif metric.avg_trading_value_20d_krw < min_avg_trading_value_krw:
            metric = LiquidityMetric(
                "fail",
                "liquidity_value_below_threshold",
                metric.avg_trading_value_20d_krw,
                metric.rows_available,
                metric.rows_used,
                metric.latest_date,
                metric.raw_path,
            )
            rows.append(LiquidityRow(source, base_status, base_reason, "exclude", metric.reason, metric))
        else:
            metric = LiquidityMetric(
                "pass",
                "liquidity_value_pass",
                metric.avg_trading_value_20d_krw,
                metric.rows_available,
                metric.rows_used,
                metric.latest_date,
                metric.raw_path,
            )
            rows.append(LiquidityRow(source, base_status, base_reason, "include", base_reason, metric))
    rows.sort(key=lambda row: (row.status, row.source.get("code", "")))
    return rows


def _reason_counts(rows: list[LiquidityRow]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in rows:
        if row.status != "exclude":
            continue
        for reason in row.reason.split(";"):
            if reason:
                counts[reason] = counts.get(reason, 0) + 1
    return counts


def _metric_counts(rows: list[LiquidityRow]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in rows:
        counts[row.metric.status] = counts.get(row.metric.status, 0) + 1
    return counts


def _format_number(value: float | None) -> str:
    if value is None:
        return ""
    return f"{value:.0f}"


def write_csv(rows: list[LiquidityRow], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = (
        "code",
        "name",
        "market",
        "security_type",
        "listing_date",
        "listing_age_calendar_days",
        "base_status",
        "base_reason",
        "status",
        "reason",
        "avg_trading_value_20d_krw",
        "liquidity_filter_status",
        "liquidity_filter_reason",
        "liquidity_rows_available",
        "liquidity_rows_used",
        "liquidity_latest_date",
        "liquidity_raw_path",
    )
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            source = row.source
            writer.writerow(
                {
                    "code": source.get("code", ""),
                    "name": source.get("name", ""),
                    "market": source.get("market", ""),
                    "security_type": source.get("security_type", ""),
                    "listing_date": source.get("listing_date", ""),
                    "listing_age_calendar_days": source.get("listing_age_calendar_days", ""),
                    "base_status": row.base_status,
                    "base_reason": row.base_reason,
                    "status": row.status,
                    "reason": row.reason,
                    "avg_trading_value_20d_krw": _format_number(row.metric.avg_trading_value_20d_krw),
                    "liquidity_filter_status": row.metric.status,
                    "liquidity_filter_reason": row.metric.reason,
                    "liquidity_rows_available": row.metric.rows_available,
                    "liquidity_rows_used": row.metric.rows_used,
                    "liquidity_latest_date": row.metric.latest_date or "",
                    "liquidity_raw_path": "" if row.metric.raw_path is None else row.metric.raw_path.as_posix(),
                }
            )


def render_markdown(
    rows: list[LiquidityRow],
    universe_csv: Path,
    raw_dirs: list[Path],
    as_of_date: str,
    lookback: int,
    min_avg_trading_value_krw: float,
    csv_output: Path | None,
) -> str:
    base_include = sum(1 for row in rows if row.base_status == "include")
    include_count = sum(1 for row in rows if row.status == "include")
    exclude_count = len(rows) - include_count
    metric_counts = _metric_counts(rows)
    reason_counts = _reason_counts(rows)
    evaluated = [row for row in rows if row.metric.status in {"pass", "fail"}]

    lines = [
        "# KRX Current Universe v0 Liquidity Filter Smoke",
        "",
        f"- As-of date: `{as_of_date}`",
        f"- Source Universe rows: `{universe_csv.as_posix()}`",
        "- Source raw directories:",
    ]
    for raw_dir in raw_dirs:
        lines.append(f"  - `{raw_dir.as_posix()}`")
    lines.extend(
        [
            "- Filter mode: `current_snapshot_liquidity_smoke`",
            "- Interpretation: `paper/smoke Universe only`, `not Point-in-Time Universe`",
            "- Bias Control judgment: `hold`",
            f"- Liquidity Filter rule: `avg_trading_value_{lookback}d_krw >= {min_avg_trading_value_krw:,.0f}`",
        ]
    )
    if csv_output:
        lines.append(f"- Machine-readable rows: `{csv_output.as_posix()}`")

    lines.extend(
        [
            "",
            "## Summary",
            "",
            f"- Total rows: `{len(rows)}`",
            f"- Base included rows before Liquidity Filter: `{base_include}`",
            f"- Included rows after Liquidity Filter: `{include_count}`",
            f"- Excluded rows after Liquidity Filter: `{exclude_count}`",
            f"- Rows with raw OHLCV evaluated: `{len(evaluated)}`",
            "",
            "## Liquidity Filter Status Counts",
            "",
            "| Status | Count |",
            "| --- | ---: |",
        ]
    )
    for status, count in sorted(metric_counts.items()):
        lines.append(f"| `{status}` | {count} |")

    lines.extend(
        [
            "",
            "## Exclusion Reason Counts",
            "",
            "| Reason | Count |",
            "| --- | ---: |",
        ]
    )
    for reason, count in sorted(reason_counts.items()):
        lines.append(f"| `{reason}` | {count} |")

    lines.extend(
        [
            "",
            "## Evaluated Sample",
            "",
            "| Code | Company | Final Status | Avg Trading Value 20D KRW | Liquidity Status | Latest Date |",
            "| --- | --- | --- | ---: | --- | --- |",
        ]
    )
    for row in evaluated[:20]:
        source = row.source
        lines.append(
            f"| `{source.get('code', '')}` | {source.get('name', '')} | {row.status} | "
            f"{_format_number(row.metric.avg_trading_value_20d_krw)} | {row.metric.status} | "
            f"{row.metric.latest_date or ''} |"
        )

    lines.extend(
        [
            "",
            "## Limitations",
            "",
            "- This is a derived smoke artifact from the current snapshot Universe, not a Point-in-Time Universe.",
            "- Missing raw OHLCV is marked as `liquidity_raw_missing`; it is a data-coverage blocker, not evidence that the stock is illiquid.",
            "- The derived final `status` excludes rows that cannot prove the Liquidity Filter from saved raw data.",
            "- KIS batch collection for the full generated Universe remains required before this can represent the full current Universe.",
            "- Backtest, OOS, Walk-Forward, and Bias Control interpretation remain `hold`.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Apply a Liquidity Filter to current KRX Universe rows using saved KIS daily raw files.")
    parser.add_argument("--universe-csv", required=True, type=Path)
    parser.add_argument("--raw-dir", required=True, action="append", type=Path)
    parser.add_argument("--as-of-date", required=True)
    parser.add_argument("--lookback", default=DEFAULT_LOOKBACK, type=int)
    parser.add_argument("--min-avg-trading-value-krw", default=DEFAULT_MIN_AVG_TRADING_VALUE_KRW, type=float)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--csv-output", type=Path)
    args = parser.parse_args()

    if args.lookback <= 0:
        raise SystemExit("--lookback must be positive")
    if args.min_avg_trading_value_krw <= 0:
        raise SystemExit("--min-avg-trading-value-krw must be positive")
    if not args.universe_csv.exists():
        raise SystemExit(f"universe CSV not found: {args.universe_csv}")

    try:
        universe_rows = _read_universe_rows(args.universe_csv)
        raw_files = _find_raw_files(args.raw_dir)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc

    rows = apply_liquidity_filter(universe_rows, raw_files, args.lookback, args.min_avg_trading_value_krw)
    if args.csv_output:
        write_csv(rows, args.csv_output)

    report = render_markdown(
        rows,
        args.universe_csv,
        args.raw_dir,
        args.as_of_date,
        args.lookback,
        args.min_avg_trading_value_krw,
        args.csv_output,
    )
    if args.output:
        write_text_lf(args.output, report)
    else:
        print(report, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
