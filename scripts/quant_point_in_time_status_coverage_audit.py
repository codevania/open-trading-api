"""Audit Point-in-Time status coverage for local market-data rows.

This is a coverage/readiness diagnostic. It does not fetch KRX/KIND data and it
does not promote current-snapshot status replay into historical coverage.
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

from quant_io import write_text_lf


DEFAULT_REQUIRED_STATUS_TYPES = ("managed_issue", "trading_halt", "market_alert", "delisting")
RELEASE_LIKE_STATUS_TYPES = {"trading_resume"}
RELEASE_LIKE_STATUS_VALUES = {"released", "resumed", "cleared", "normal", "delisting_withdrawn"}
DATE_ROWS_FIELDS = (
    "date",
    "market_rows",
    "unique_codes",
    "event_codes_present",
    "rows_with_event_code",
    "rows_without_event_code",
    "rows_with_applied_status_event",
    "rows_excluded_by_status_event",
    "event_code_row_ratio",
    "applied_status_event_row_ratio",
    "status_exclusion_row_ratio",
    "coverage_status",
    "coverage_notes",
)


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


def _iso_date(value: str, field_name: str) -> str:
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError as exc:
        raise ValueError(f"{field_name} must be YYYY-MM-DD: {value}") from exc
    return value


def _normalize_code(value: str) -> str:
    return str(value or "").strip().upper()


def _parse_int(value: str) -> int:
    text = str(value or "").replace(",", "").strip()
    if not text:
        return 0
    try:
        return int(float(text))
    except ValueError:
        return 0


def _ratio(numerator: int, denominator: int) -> str:
    if denominator <= 0:
        return "0.000000"
    return f"{numerator / denominator:.6f}"


def _split_required_status_types(value: str) -> tuple[str, ...]:
    parsed = tuple(dict.fromkeys(token.strip() for token in value.split(",") if token.strip()))
    if not parsed:
        raise ValueError("at least one required status type is required")
    return parsed


def _is_release_like(event: dict[str, str]) -> bool:
    status_type = event.get("status_type", "")
    status_value = event.get("status_value", "")
    return status_type in RELEASE_LIKE_STATUS_TYPES or status_value in RELEASE_LIKE_STATUS_VALUES


def _replayed_index(rows: list[dict[str, str]]) -> dict[tuple[str, str], dict[str, str]]:
    indexed: dict[tuple[str, str], dict[str, str]] = {}
    for row in rows:
        key = (row.get("date", ""), _normalize_code(row.get("code", "")))
        if all(key) and key not in indexed:
            indexed[key] = row
    return indexed


def audit_status_coverage(
    *,
    market_data_path: Path,
    events_path: Path,
    replayed_market_data_path: Path | None = None,
    coverage_mode: str = "current_snapshot_smoke",
    required_status_types: tuple[str, ...] = DEFAULT_REQUIRED_STATUS_TYPES,
) -> tuple[list[dict[str, str]], dict[str, Any]]:
    market_fields, market_rows = _read_csv(market_data_path, "market-data")
    event_fields, event_rows = _read_csv(events_path, "status-events")
    _require_columns(market_fields, {"date", "code"}, "market-data")
    _require_columns(event_fields, {"event_date", "code", "status_type", "status_value", "source", "raw_path"}, "status-events")

    for row in market_rows:
        _iso_date(row.get("date", ""), "date")
        if not _normalize_code(row.get("code", "")):
            raise ValueError("market-data row has empty code")
    for row in event_rows:
        _iso_date(row.get("event_date", ""), "event_date")
        if not _normalize_code(row.get("code", "")):
            raise ValueError("status-events row has empty code")

    replayed_rows: list[dict[str, str]] = []
    replayed: dict[tuple[str, str], dict[str, str]] = {}
    if replayed_market_data_path is not None:
        replay_fields, replayed_rows = _read_csv(replayed_market_data_path, "replayed market-data")
        _require_columns(
            replay_fields,
            {"date", "code", "pit_applied_event_count", "pit_status_replay_status"},
            "replayed market-data",
        )
        replayed = _replayed_index(replayed_rows)

    event_codes = {_normalize_code(row["code"]) for row in event_rows}
    status_type_counts = Counter(row["status_type"] for row in event_rows)
    status_value_counts = Counter(row["status_value"] for row in event_rows)
    source_counts = Counter(row["source"] for row in event_rows)
    confidence_counts = Counter(row.get("confidence", "") or "blank" for row in event_rows)
    raw_path_counts = Counter(row["raw_path"] for row in event_rows)
    release_like_event_rows = sum(1 for row in event_rows if _is_release_like(row))
    missing_required_types = sorted(set(required_status_types) - set(status_type_counts))

    rows_by_date: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in market_rows:
        rows_by_date[row["date"]].append(row)

    replay_match_rows = 0
    replay_missing_rows = 0
    date_rows: list[dict[str, str]] = []
    for date in sorted(rows_by_date):
        rows = rows_by_date[date]
        row_count = len(rows)
        codes = {_normalize_code(row["code"]) for row in rows}
        event_codes_present = codes & event_codes
        rows_with_event_code = sum(1 for row in rows if _normalize_code(row["code"]) in event_codes)
        rows_with_applied = 0
        rows_excluded = 0
        for row in rows:
            key = (date, _normalize_code(row["code"]))
            replay_row = replayed.get(key)
            if replayed_market_data_path is not None and replay_row is None:
                replay_missing_rows += 1
                continue
            if replay_row is not None:
                replay_match_rows += 1
                if _parse_int(replay_row.get("pit_applied_event_count", "")) > 0:
                    rows_with_applied += 1
                if replay_row.get("pit_status_replay_status") == "exclude_by_status_event":
                    rows_excluded += 1

        notes: list[str] = []
        if coverage_mode != "historical_complete":
            notes.append("mode_not_historical_complete")
        if missing_required_types:
            notes.append("missing_required_status_types")
        if release_like_event_rows == 0:
            notes.append("no_release_like_events")
        if replayed_market_data_path is None:
            notes.append("replay_not_supplied")
        elif replay_missing_rows:
            notes.append("replay_missing_rows")

        date_rows.append(
            {
                "date": date,
                "market_rows": str(row_count),
                "unique_codes": str(len(codes)),
                "event_codes_present": str(len(event_codes_present)),
                "rows_with_event_code": str(rows_with_event_code),
                "rows_without_event_code": str(row_count - rows_with_event_code),
                "rows_with_applied_status_event": str(rows_with_applied),
                "rows_excluded_by_status_event": str(rows_excluded),
                "event_code_row_ratio": _ratio(rows_with_event_code, row_count),
                "applied_status_event_row_ratio": _ratio(rows_with_applied, row_count),
                "status_exclusion_row_ratio": _ratio(rows_excluded, row_count),
                "coverage_status": "hold",
                "coverage_notes": ";".join(dict.fromkeys(notes)),
            }
        )

    coverage_status = "pass" if (
        coverage_mode == "historical_complete"
        and not missing_required_types
        and release_like_event_rows > 0
        and replayed_market_data_path is not None
        and replay_missing_rows == 0
    ) else "hold"
    if coverage_status == "pass":
        for row in date_rows:
            row["coverage_status"] = "pass"
            row["coverage_notes"] = "historical_complete_inputs_supplied"

    summary = {
        "market_data_path": market_data_path,
        "events_path": events_path,
        "replayed_market_data_path": replayed_market_data_path,
        "coverage_mode": coverage_mode,
        "coverage_status": coverage_status,
        "market_rows": len(market_rows),
        "market_dates": len(rows_by_date),
        "market_codes": len({_normalize_code(row["code"]) for row in market_rows}),
        "market_start": min(row["date"] for row in market_rows),
        "market_end": max(row["date"] for row in market_rows),
        "event_rows": len(event_rows),
        "event_codes": len(event_codes),
        "event_start": min(row["event_date"] for row in event_rows),
        "event_end": max(row["event_date"] for row in event_rows),
        "status_type_counts": dict(sorted(status_type_counts.items())),
        "status_value_counts": dict(sorted(status_value_counts.items())),
        "source_counts": dict(sorted(source_counts.items())),
        "confidence_counts": dict(sorted(confidence_counts.items())),
        "raw_path_count": len(raw_path_counts),
        "release_like_event_rows": release_like_event_rows,
        "missing_required_status_types": missing_required_types,
        "replayed_rows": len(replayed_rows),
        "replay_match_rows": replay_match_rows,
        "replay_missing_rows": replay_missing_rows,
        "rows_with_any_status_event_code": sum(_parse_int(row["rows_with_event_code"]) for row in date_rows),
        "rows_with_applied_status_event": sum(_parse_int(row["rows_with_applied_status_event"]) for row in date_rows),
        "rows_excluded_by_status_event": sum(_parse_int(row["rows_excluded_by_status_event"]) for row in date_rows),
    }
    return date_rows, summary


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=DATE_ROWS_FIELDS, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def _wikilink(path: Path | None) -> str:
    if path is None:
        return "`not_supplied`"
    rendered = path.as_posix()
    return f"[[{rendered}|{rendered}]]"


def _render_counter(counter: dict[str, int]) -> list[str]:
    if not counter:
        return ["| `none` | 0 |"]
    return [f"| `{key}` | {count} |" for key, count in counter.items()]


def _render_report(summary: dict[str, Any], output_path: Path) -> str:
    hold_reasons: list[str] = []
    if summary["coverage_mode"] != "historical_complete":
        hold_reasons.append("coverage mode is not `historical_complete`")
    if summary["missing_required_status_types"]:
        hold_reasons.append(
            "missing required status types: `" + ",".join(summary["missing_required_status_types"]) + "`"
        )
    if summary["release_like_event_rows"] == 0:
        hold_reasons.append("no release/resume-like events are present, so active-state lifetimes are one-sided")
    if summary["replayed_market_data_path"] is None:
        hold_reasons.append("status replay rows were not supplied")
    elif summary["replay_missing_rows"]:
        hold_reasons.append(f"status replay is missing {summary['replay_missing_rows']} market rows")
    if not hold_reasons and summary["coverage_status"] == "pass":
        hold_reasons.append("none")

    lines = [
        "# Point-in-Time Status Coverage Audit",
        "",
        f"- Market data: {_wikilink(summary['market_data_path'])}",
        f"- Status events: {_wikilink(summary['events_path'])}",
        f"- Replayed market-data: {_wikilink(summary['replayed_market_data_path'])}",
        f"- Output: {_wikilink(output_path)}",
        f"- Coverage mode: `{summary['coverage_mode']}`",
        f"- Coverage status: `{summary['coverage_status']}`",
        "- KIS/KRX API call: `false`",
        "- Order intent generated: `false`",
        "- Interpretation: status coverage audit only, not a `Backtest` result",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| Market rows | {summary['market_rows']} |",
        f"| Market dates | {summary['market_dates']} |",
        f"| Market codes | {summary['market_codes']} |",
        f"| Market window | `{summary['market_start']}..{summary['market_end']}` |",
        f"| Status event rows | {summary['event_rows']} |",
        f"| Status event codes | {summary['event_codes']} |",
        f"| Event date window | `{summary['event_start']}..{summary['event_end']}` |",
        f"| Raw status source paths | {summary['raw_path_count']} |",
        f"| Release/resume-like event rows | {summary['release_like_event_rows']} |",
        f"| Replayed rows | {summary['replayed_rows']} |",
        f"| Replay matched market rows | {summary['replay_match_rows']} |",
        f"| Replay missing market rows | {summary['replay_missing_rows']} |",
        f"| Rows with any status-event code | {summary['rows_with_any_status_event_code']} |",
        f"| Rows with applied status event | {summary['rows_with_applied_status_event']} |",
        f"| Rows excluded by status event | {summary['rows_excluded_by_status_event']} |",
        "",
        "## Status Type Counts",
        "",
        "| Status type | Rows |",
        "| --- | ---: |",
        *_render_counter(summary["status_type_counts"]),
        "",
        "## Status Value Counts",
        "",
        "| Status value | Rows |",
        "| --- | ---: |",
        *_render_counter(summary["status_value_counts"]),
        "",
        "## Source Counts",
        "",
        "| Source | Rows |",
        "| --- | ---: |",
        *_render_counter(summary["source_counts"]),
        "",
        "## Hold Reasons",
        "",
    ]
    for reason in hold_reasons:
        lines.append(f"- {reason}")
    lines.extend(
        [
            "",
            "## Guardrails",
            "",
            "- Event-code ratios are diagnostic; a stock with no status event is not automatically a data gap.",
            "- Current snapshot events can exclude active issues, but they do not prove historical state transitions.",
            "- Keep `Backtest readiness` at `hold` until source coverage is reproducible for every rebalance date.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit local Point-in-Time status coverage.")
    parser.add_argument("--market-data", required=True, type=Path)
    parser.add_argument("--events", required=True, type=Path)
    parser.add_argument("--replayed-market-data", type=Path)
    parser.add_argument("--coverage-mode", default="current_snapshot_smoke")
    parser.add_argument("--required-status-types", default=",".join(DEFAULT_REQUIRED_STATUS_TYPES))
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--report-output", type=Path)
    args = parser.parse_args()

    try:
        rows, summary = audit_status_coverage(
            market_data_path=args.market_data,
            events_path=args.events,
            replayed_market_data_path=args.replayed_market_data,
            coverage_mode=args.coverage_mode,
            required_status_types=_split_required_status_types(args.required_status_types),
        )
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc

    _write_csv(args.output, rows)
    report = _render_report(summary, args.output)
    if args.report_output:
        write_text_lf(args.report_output, report)
    else:
        print(report, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
