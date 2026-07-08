"""Report Point-in-Time status lifecycle gaps by code and status type.

This is a local diagnostic for collection planning. It does not fetch KRX/KIND
data, promote current snapshots to historical coverage, or create order intents.
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

from quant_io import write_text_lf


DEFAULT_REQUIRED_STATUS_TYPES = ("managed_issue", "trading_halt", "market_alert")
RELEASE_LIKE_STATUS_TYPES = {"trading_resume"}
RELEASE_LIKE_STATUS_VALUES = {"released", "resumed", "cleared", "normal", "delisting_withdrawn"}
GAP_ROW_FIELDS = (
    "code",
    "market",
    "status_type",
    "lifecycle_gap_status",
    "active_like_rows",
    "release_like_rows",
    "first_active_event_date",
    "latest_active_event_date",
    "first_release_like_event_date",
    "latest_release_like_event_date",
    "market_rows",
    "market_start",
    "market_end",
    "event_sources",
    "raw_paths",
    "notes",
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


def _split_required_status_types(value: str) -> tuple[str, ...]:
    parsed = tuple(dict.fromkeys(token.strip() for token in value.split(",") if token.strip()))
    if not parsed:
        raise ValueError("at least one required status type is required")
    return parsed


def _is_release_like(event: dict[str, str]) -> bool:
    return (
        event.get("status_type", "") in RELEASE_LIKE_STATUS_TYPES
        or event.get("status_value", "") in RELEASE_LIKE_STATUS_VALUES
    )


def _lifecycle_status_type(status_type: str) -> str:
    if status_type == "trading_resume":
        return "trading_halt"
    return status_type


def _join_sorted(values: set[str]) -> str:
    return ";".join(sorted(value for value in values if value))


def _market_index(rows: list[dict[str, str]] | None) -> dict[str, dict[str, Any]]:
    indexed: dict[str, dict[str, Any]] = {}
    if rows is None:
        return indexed
    for row in rows:
        date = _iso_date(row.get("date", ""), "date")
        code = _normalize_code(row.get("code", ""))
        if not code:
            raise ValueError("market-data row has empty code")
        current = indexed.setdefault(code, {"rows": 0, "dates": set(), "markets": set()})
        current["rows"] += 1
        current["dates"].add(date)
        if row.get("market"):
            current["markets"].add(row["market"])
    return indexed


def _blank_market_summary() -> dict[str, str]:
    return {"market_rows": "0", "market_start": "", "market_end": "", "market": ""}


def _market_summary(code: str, indexed_market: dict[str, dict[str, Any]]) -> dict[str, str]:
    item = indexed_market.get(code)
    if item is None:
        return _blank_market_summary()
    dates = sorted(item["dates"])
    markets = sorted(item["markets"])
    return {
        "market_rows": str(item["rows"]),
        "market_start": dates[0] if dates else "",
        "market_end": dates[-1] if dates else "",
        "market": ";".join(markets),
    }


def _gap_status(active_dates: list[str], release_dates: list[str]) -> str:
    if active_dates and not release_dates:
        return "missing_release_resume_evidence"
    if active_dates and release_dates:
        if max(active_dates) > max(release_dates):
            return "active_after_latest_release"
        return "has_release_resume_evidence"
    if release_dates:
        return "release_without_active_in_scope"
    return "no_lifecycle_events"


def build_lifecycle_gap_rows(
    *,
    events_path: Path,
    market_data_path: Path | None = None,
    required_status_types: tuple[str, ...] = DEFAULT_REQUIRED_STATUS_TYPES,
) -> tuple[list[dict[str, str]], dict[str, Any]]:
    event_fields, event_rows = _read_csv(events_path, "status-events")
    _require_columns(event_fields, {"event_date", "code", "status_type", "status_value", "source", "raw_path"}, "status-events")

    market_rows: list[dict[str, str]] | None = None
    market_fields: list[str] = []
    if market_data_path is not None:
        market_fields, market_rows = _read_csv(market_data_path, "market-data")
        _require_columns(market_fields, {"date", "code"}, "market-data")

    indexed_market = _market_index(market_rows)
    required = set(required_status_types)
    groups: dict[tuple[str, str], dict[str, Any]] = defaultdict(
        lambda: {
            "active_dates": [],
            "release_dates": [],
            "markets": set(),
            "sources": set(),
            "raw_paths": set(),
            "release_status_types": set(),
        }
    )
    status_type_counts: Counter[str] = Counter()
    status_value_counts: Counter[str] = Counter()
    skipped_status_type_counts: Counter[str] = Counter()

    for row in event_rows:
        event_date = _iso_date(row.get("event_date", ""), "event_date")
        code = _normalize_code(row.get("code", ""))
        if not code:
            raise ValueError("status-events row has empty code")
        status_type = row.get("status_type", "")
        status_value = row.get("status_value", "")
        status_type_counts[status_type] += 1
        status_value_counts[status_value] += 1

        lifecycle_type = _lifecycle_status_type(status_type)
        if lifecycle_type not in required:
            skipped_status_type_counts[status_type] += 1
            continue

        group = groups[(code, lifecycle_type)]
        if row.get("market"):
            group["markets"].add(row["market"])
        if row.get("source"):
            group["sources"].add(row["source"])
        if row.get("raw_path"):
            for raw_path in row["raw_path"].split(";"):
                group["raw_paths"].add(raw_path.strip())

        if _is_release_like(row):
            group["release_dates"].append(event_date)
            group["release_status_types"].add(status_type)
        else:
            group["active_dates"].append(event_date)

    gap_rows: list[dict[str, str]] = []
    for (code, status_type), group in sorted(groups.items()):
        active_dates = sorted(group["active_dates"])
        release_dates = sorted(group["release_dates"])
        market_summary = _market_summary(code, indexed_market)
        markets = set(group["markets"])
        if market_summary["market"]:
            markets.update(market_summary["market"].split(";"))
        notes: list[str] = []
        if market_data_path is not None and market_summary["market_rows"] == "0":
            notes.append("market_data_absent_for_code")
        if "trading_resume" in group["release_status_types"]:
            notes.append("trading_resume_mapped_to_trading_halt_release")
        if not release_dates:
            notes.append("release_resume_collection_target")
        gap_rows.append(
            {
                "code": code,
                "market": ";".join(sorted(markets)),
                "status_type": status_type,
                "lifecycle_gap_status": _gap_status(active_dates, release_dates),
                "active_like_rows": str(len(active_dates)),
                "release_like_rows": str(len(release_dates)),
                "first_active_event_date": active_dates[0] if active_dates else "",
                "latest_active_event_date": active_dates[-1] if active_dates else "",
                "first_release_like_event_date": release_dates[0] if release_dates else "",
                "latest_release_like_event_date": release_dates[-1] if release_dates else "",
                "market_rows": market_summary["market_rows"],
                "market_start": market_summary["market_start"],
                "market_end": market_summary["market_end"],
                "event_sources": _join_sorted(group["sources"]),
                "raw_paths": _join_sorted(group["raw_paths"]),
                "notes": ";".join(notes),
            }
        )

    gap_status_counts = Counter(row["lifecycle_gap_status"] for row in gap_rows)
    by_status_type_counts: dict[str, Counter[str]] = defaultdict(Counter)
    for row in gap_rows:
        by_status_type_counts[row["status_type"]][row["lifecycle_gap_status"]] += 1

    market_start = ""
    market_end = ""
    market_codes = 0
    if market_rows is not None:
        market_dates = sorted({row["date"] for row in market_rows})
        market_start = market_dates[0]
        market_end = market_dates[-1]
        market_codes = len({_normalize_code(row["code"]) for row in market_rows})

    summary = {
        "events_path": events_path,
        "market_data_path": market_data_path,
        "required_status_types": list(required_status_types),
        "event_rows": len(event_rows),
        "event_codes": len({_normalize_code(row["code"]) for row in event_rows}),
        "status_type_counts": dict(sorted(status_type_counts.items())),
        "status_value_counts": dict(sorted(status_value_counts.items())),
        "skipped_status_type_counts": dict(sorted(skipped_status_type_counts.items())),
        "market_rows": len(market_rows or []),
        "market_codes": market_codes,
        "market_start": market_start,
        "market_end": market_end,
        "lifecycle_groups": len(gap_rows),
        "gap_status_counts": dict(sorted(gap_status_counts.items())),
        "by_status_type_counts": {key: dict(sorted(value.items())) for key, value in sorted(by_status_type_counts.items())},
    }
    return gap_rows, summary


def _write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=GAP_ROW_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _wikilink(path: Path | None) -> str:
    if path is None:
        return "`not_supplied`"
    rendered = path.as_posix()
    return f"[[{rendered}|{rendered}]]"


def _render_counter(counter: dict[str, int]) -> list[str]:
    if not counter:
        return ["| `none` | 0 |"]
    return [f"| `{key}` | {value} |" for key, value in counter.items()]


def _render_status_type_counts(counts: dict[str, dict[str, int]]) -> list[str]:
    if not counts:
        return ["| `none` | 0 | 0 | 0 | 0 |"]
    lines: list[str] = []
    for status_type, row in counts.items():
        lines.append(
            "| `"
            + status_type
            + "` | "
            + str(row.get("missing_release_resume_evidence", 0))
            + " | "
            + str(row.get("active_after_latest_release", 0))
            + " | "
            + str(row.get("has_release_resume_evidence", 0))
            + " | "
            + str(row.get("release_without_active_in_scope", 0))
            + " |"
        )
    return lines


def _render_report(summary: dict[str, Any], output_path: Path) -> str:
    lines = [
        "# Point-in-Time Status Lifecycle Gap Report",
        "",
        f"- Status events: {_wikilink(summary['events_path'])}",
        f"- Market data: {_wikilink(summary['market_data_path'])}",
        f"- Output: {_wikilink(output_path)}",
        f"- Required lifecycle status types: `{','.join(summary['required_status_types'])}`",
        "- KIS/KRX API call: `false`",
        "- Order intent generated: `false`",
        "- Backtest readiness impact: `hold`",
        "- Interpretation: lifecycle collection-target diagnostic, not historical status truth",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| Status event rows | {summary['event_rows']} |",
        f"| Status event codes | {summary['event_codes']} |",
        f"| Market rows | {summary['market_rows']} |",
        f"| Market codes | {summary['market_codes']} |",
        f"| Market window | `{summary['market_start']}..{summary['market_end']}` |",
        f"| Lifecycle groups | {summary['lifecycle_groups']} |",
        f"| Missing release/resume groups | {summary['gap_status_counts'].get('missing_release_resume_evidence', 0)} |",
        f"| Active after latest release groups | {summary['gap_status_counts'].get('active_after_latest_release', 0)} |",
        f"| Has release/resume evidence groups | {summary['gap_status_counts'].get('has_release_resume_evidence', 0)} |",
        f"| Release without active groups | {summary['gap_status_counts'].get('release_without_active_in_scope', 0)} |",
        "",
        "## Lifecycle Gap Status Counts",
        "",
        "| Gap status | Groups |",
        "| --- | ---: |",
        *_render_counter(summary["gap_status_counts"]),
        "",
        "## Gap Counts By Status Type",
        "",
        "| Status type | Missing release/resume | Active after latest release | Has release/resume | Release without active |",
        "| --- | ---: | ---: | ---: | ---: |",
        *_render_status_type_counts(summary["by_status_type_counts"]),
        "",
        "## Input Status Type Counts",
        "",
        "| Status type | Rows |",
        "| --- | ---: |",
        *_render_counter(summary["status_type_counts"]),
        "",
        "## Guardrails",
        "",
        "- `trading_resume` rows are counted as release-like evidence for `trading_halt` lifecycle groups.",
        "- Rows with `missing_release_resume_evidence` are collection targets for official transition evidence.",
        "- This report does not prove historical completeness and must not promote `Backtest readiness`.",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Report local Point-in-Time status lifecycle gaps.")
    parser.add_argument("--events", required=True, type=Path)
    parser.add_argument("--market-data", type=Path)
    parser.add_argument("--required-status-types", default=",".join(DEFAULT_REQUIRED_STATUS_TYPES))
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--report-output", type=Path)
    args = parser.parse_args()

    try:
        rows, summary = build_lifecycle_gap_rows(
            events_path=args.events,
            market_data_path=args.market_data,
            required_status_types=_split_required_status_types(args.required_status_types),
        )
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc

    _write_rows(args.output, rows)
    report = _render_report(summary, args.output)
    if args.report_output:
        write_text_lf(args.report_output, report)
    else:
        print(report, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
