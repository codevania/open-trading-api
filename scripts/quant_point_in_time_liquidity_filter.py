"""Apply a date-scoped Liquidity Filter to Point-in-Time Universe smoke rows.

The input is expected to be a status-replayed Point-in-Time Universe CSV with
one row per date/code and a same-date trading value. This script does not call
external APIs and should be treated as a smoke/scaffold until the date coverage
is long enough for the production lookback.
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict, deque
from dataclasses import dataclass
from pathlib import Path
from typing import Any


DEFAULT_LOOKBACK = 20
DEFAULT_MIN_AVG_TRADING_VALUE_KRW = 1_000_000_000


@dataclass(frozen=True)
class PitLiquidityRow:
    source: dict[str, str]
    final_status: str
    final_reasons: str
    liquidity_status: str
    liquidity_reason: str
    avg_trading_value_krw: float | None
    rows_used: int


def _read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise ValueError(f"Point-in-Time Universe CSV not found: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ValueError(f"Point-in-Time Universe CSV has no rows: {path}")
    required = {"date", "code", "trading_value_krw", "pit_universe_status"}
    missing = required - set(rows[0])
    if missing:
        raise ValueError(f"Point-in-Time Universe CSV missing required columns: {', '.join(sorted(missing))}")
    return rows


def _parse_trading_value(value: str) -> float | None:
    text = str(value or "").replace(",", "").strip()
    if not text:
        return None
    try:
        parsed = float(text)
    except ValueError:
        return None
    if parsed < 0:
        return None
    return parsed


def _append_reason(existing: str, reason: str) -> str:
    if not existing:
        return reason
    if reason in existing.split(";"):
        return existing
    return f"{existing};{reason}"


def apply_point_in_time_liquidity_filter(
    source_rows: list[dict[str, str]],
    lookback: int = DEFAULT_LOOKBACK,
    min_avg_trading_value_krw: float = DEFAULT_MIN_AVG_TRADING_VALUE_KRW,
) -> list[PitLiquidityRow]:
    if lookback <= 0:
        raise ValueError("lookback must be positive")
    if min_avg_trading_value_krw <= 0:
        raise ValueError("min_avg_trading_value_krw must be positive")

    ordered = sorted(source_rows, key=lambda row: (row.get("code", ""), row.get("date", "")))
    windows: dict[str, deque[float]] = defaultdict(lambda: deque(maxlen=lookback))
    output: list[PitLiquidityRow] = []

    for row in ordered:
        code = row.get("code", "").strip().upper()
        base_status = row.get("pit_universe_status", "")
        base_reasons = row.get("pit_universe_exclude_reasons", "")
        trading_value = _parse_trading_value(row.get("trading_value_krw", ""))

        if base_status != "include":
            output.append(
                PitLiquidityRow(
                    source=row,
                    final_status=base_status or "exclude",
                    final_reasons=base_reasons or "pre_liquidity_exclude",
                    liquidity_status="not_evaluated_preexisting_exclude",
                    liquidity_reason="pre_liquidity_exclude",
                    avg_trading_value_krw=None,
                    rows_used=0,
                )
            )
            if trading_value is not None:
                windows[code].append(trading_value)
            continue

        if trading_value is None:
            output.append(
                PitLiquidityRow(
                    source=row,
                    final_status="exclude",
                    final_reasons=_append_reason(base_reasons, "liquidity_trading_value_missing_or_invalid"),
                    liquidity_status="data_invalid",
                    liquidity_reason="liquidity_trading_value_missing_or_invalid",
                    avg_trading_value_krw=None,
                    rows_used=len(windows[code]),
                )
            )
            continue

        windows[code].append(trading_value)
        window = windows[code]
        rows_used = len(window)
        if rows_used < lookback:
            output.append(
                PitLiquidityRow(
                    source=row,
                    final_status="exclude",
                    final_reasons=_append_reason(base_reasons, "liquidity_history_insufficient"),
                    liquidity_status="data_insufficient",
                    liquidity_reason="liquidity_history_insufficient",
                    avg_trading_value_krw=None,
                    rows_used=rows_used,
                )
            )
            continue

        avg_value = sum(window) / rows_used
        if avg_value < min_avg_trading_value_krw:
            output.append(
                PitLiquidityRow(
                    source=row,
                    final_status="exclude",
                    final_reasons=_append_reason(base_reasons, "liquidity_value_below_threshold"),
                    liquidity_status="fail",
                    liquidity_reason="liquidity_value_below_threshold",
                    avg_trading_value_krw=avg_value,
                    rows_used=rows_used,
                )
            )
        else:
            output.append(
                PitLiquidityRow(
                    source=row,
                    final_status="include",
                    final_reasons=base_reasons,
                    liquidity_status="pass",
                    liquidity_reason="liquidity_value_pass",
                    avg_trading_value_krw=avg_value,
                    rows_used=rows_used,
                )
            )

    output.sort(key=lambda result: (result.source.get("date", ""), result.source.get("code", "")))
    return output


def _format_number(value: float | None) -> str:
    if value is None:
        return ""
    return f"{value:.0f}"


def _counts(rows: list[PitLiquidityRow], attr: str) -> dict[str, int]:
    counter: Counter[str] = Counter()
    for row in rows:
        counter[str(getattr(row, attr) or "missing")] += 1
    return dict(sorted(counter.items()))


def _reason_counts(rows: list[PitLiquidityRow]) -> dict[str, int]:
    counter: Counter[str] = Counter()
    for row in rows:
        if row.final_status != "exclude":
            continue
        for reason in row.final_reasons.split(";"):
            if reason:
                counter[reason] += 1
    return dict(sorted(counter.items()))


def write_csv(rows: list[PitLiquidityRow], path: Path, lookback: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    base_fields = list(rows[0].source.keys()) if rows else []
    extra_fields = [
        "pit_liquidity_final_status",
        "pit_liquidity_final_reasons",
        f"avg_trading_value_{lookback}d_krw",
        "pit_liquidity_status",
        "pit_liquidity_reason",
        "pit_liquidity_rows_used",
    ]
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=base_fields + extra_fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    **row.source,
                    "pit_liquidity_final_status": row.final_status,
                    "pit_liquidity_final_reasons": row.final_reasons,
                    f"avg_trading_value_{lookback}d_krw": _format_number(row.avg_trading_value_krw),
                    "pit_liquidity_status": row.liquidity_status,
                    "pit_liquidity_reason": row.liquidity_reason,
                    "pit_liquidity_rows_used": str(row.rows_used),
                }
            )


def _wikilink(path: Path) -> str:
    rendered = path.as_posix()
    return f"[[{rendered}|{rendered}]]"


def render_report(
    rows: list[PitLiquidityRow],
    input_path: Path,
    as_of_range: str,
    lookback: int,
    min_avg_trading_value_krw: float,
    csv_output: Path | None,
) -> str:
    base_includes = sum(1 for row in rows if row.source.get("pit_universe_status") == "include")
    final_includes = sum(1 for row in rows if row.final_status == "include")
    dates = sorted({row.source.get("date", "") for row in rows if row.source.get("date", "")})
    evaluated = [row for row in rows if row.liquidity_status in {"pass", "fail"}]

    lines = [
        "# Point-in-Time Liquidity Filter Smoke",
        "",
        f"- Input: {_wikilink(input_path)}",
        f"- Date range: `{as_of_range}`",
        "- Mode: `point_in_time_liquidity_smoke`",
        "- KIS API call: `false`",
        "- Backtest readiness: `hold`",
        "- Live trading readiness: `blocked`",
        f"- Liquidity Filter rule: `avg_trading_value_{lookback}d_krw >= {min_avg_trading_value_krw:,.0f}`",
    ]
    if csv_output is not None:
        lines.append(f"- Machine-readable rows: {_wikilink(csv_output)}")

    lines.extend(
        [
            "",
            "## Summary",
            "",
            f"- Input rows: `{len(rows)}`",
            f"- Dates: `{len(dates)}`",
            f"- Base `Point-in-Time Universe` include rows: `{base_includes}`",
            f"- Include rows after Liquidity Filter: `{final_includes}`",
            f"- Exclude rows after Liquidity Filter: `{len(rows) - final_includes}`",
            f"- Rows with full lookback evaluated: `{len(evaluated)}`",
            "",
            "## Liquidity Status Counts",
            "",
            "| Status | Count |",
            "| --- | ---: |",
        ]
    )
    for status, count in _counts(rows, "liquidity_status").items():
        lines.append(f"| `{status}` | {count} |")

    lines.extend(["", "## Final Status Counts", "", "| Status | Count |", "| --- | ---: |"])
    for status, count in _counts(rows, "final_status").items():
        lines.append(f"| `{status}` | {count} |")

    lines.extend(["", "## Exclusion Reason Counts", "", "| Reason | Count |", "| --- | ---: |"])
    for reason, count in _reason_counts(rows).items():
        lines.append(f"| `{reason}` | {count} |")

    lines.extend(
        [
            "",
            "## Evaluated Sample",
            "",
            "| Date | Code | Company | Final Status | Avg Trading Value KRW | Liquidity Status |",
            "| --- | --- | --- | --- | ---: | --- |",
        ]
    )
    for row in evaluated[:20]:
        lines.append(
            f"| `{row.source.get('date', '')}` | `{row.source.get('code', '')}` | {row.source.get('stock_name', '')} | "
            f"{row.final_status} | {_format_number(row.avg_trading_value_krw)} | {row.liquidity_status} |"
        )

    lines.extend(
        [
            "",
            "## Limitations",
            "",
            "- This is still a smoke artifact because the current input covers only a bounded 17-date window.",
            "- The first `lookback - 1` rows per code are excluded as `liquidity_history_insufficient` by design.",
            "- Historical status coverage is still incomplete, so this output is not a Backtest input yet.",
            "- Keep `Backtest readiness` at `hold` until full `Point-in-Time` status and Liquidity Filter coverage are available.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Apply date-scoped Liquidity Filter to Point-in-Time Universe rows.")
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--as-of-range", required=True)
    parser.add_argument("--lookback", default=DEFAULT_LOOKBACK, type=int)
    parser.add_argument("--min-avg-trading-value-krw", default=DEFAULT_MIN_AVG_TRADING_VALUE_KRW, type=float)
    parser.add_argument("--csv-output", type=Path)
    parser.add_argument("--report-output", type=Path)
    args = parser.parse_args()

    try:
        source_rows = _read_rows(args.input)
        results = apply_point_in_time_liquidity_filter(source_rows, args.lookback, args.min_avg_trading_value_krw)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc

    if args.csv_output:
        write_csv(results, args.csv_output, args.lookback)
    report = render_report(
        results,
        args.input,
        args.as_of_range,
        args.lookback,
        args.min_avg_trading_value_krw,
        args.csv_output,
    )
    if args.report_output:
        args.report_output.parent.mkdir(parents=True, exist_ok=True)
        args.report_output.write_text(report, encoding="utf-8")
    else:
        print(report, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
