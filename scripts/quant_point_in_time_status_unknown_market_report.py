"""Report status-event rows that still lack deterministic market labels.

This is a local collection-target diagnostic. It does not fetch KRX/KIND data,
change event state, promote status coverage, or create order intents.
"""

from __future__ import annotations

import argparse
import csv
import re
from collections import Counter
from pathlib import Path
from typing import Any

from quant_io import write_text_lf


UNKNOWN_MARKET_VALUES = {"", "UNKNOWN"}
REQUIRED_COLUMNS = (
    "event_date",
    "code",
    "market",
    "status_type",
    "status_value",
    "source",
    "source_url",
    "raw_path",
    "confidence",
    "notes",
)
OUTPUT_FIELDS = (
    "code",
    "status_type",
    "status_value",
    "event_date",
    "source",
    "confidence",
    "source_url",
    "current_market",
    "raw_path_count",
    "raw_capture_dates",
    "raw_paths",
    "collection_target",
    "notes",
)
RAW_CAPTURE_DATE_RE = re.compile(r"_report/raw/\d{4}/(\d{4}-\d{2}-\d{2})/")


def _read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path.exists():
        raise ValueError(f"events CSV not found: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = list(reader.fieldnames or [])
        rows = [{key: (value or "").strip() for key, value in row.items()} for row in reader]
    if not rows:
        raise ValueError(f"events CSV has no rows: {path}")
    return fields, rows


def _require_columns(fields: list[str]) -> None:
    missing = [column for column in REQUIRED_COLUMNS if column not in fields]
    if missing:
        raise ValueError(f"events CSV missing required columns: {', '.join(missing)}")


def _split_paths(value: str) -> list[str]:
    return [part.strip() for part in value.split(";") if part.strip()]


def _raw_capture_dates(paths: list[str]) -> list[str]:
    dates: set[str] = set()
    for path in paths:
        match = RAW_CAPTURE_DATE_RE.search(path)
        if match:
            dates.add(match.group(1))
    return sorted(dates)


def _is_unknown_market(value: str) -> bool:
    return value.strip().upper() in UNKNOWN_MARKET_VALUES


def build_unknown_market_rows(events_path: Path) -> tuple[list[dict[str, str]], dict[str, Any]]:
    fields, event_rows = _read_csv(events_path)
    _require_columns(fields)

    output_rows: list[dict[str, str]] = []
    status_type_counts: Counter[str] = Counter()
    source_counts: Counter[str] = Counter()
    raw_capture_dates: set[str] = set()

    for row in event_rows:
        market = row.get("market", "")
        if not _is_unknown_market(market):
            continue

        raw_paths = _split_paths(row.get("raw_path", ""))
        capture_dates = _raw_capture_dates(raw_paths)
        raw_capture_dates.update(capture_dates)
        status_type_counts[row.get("status_type", "")] += 1
        source_counts[row.get("source", "")] += 1
        output_rows.append(
            {
                "code": row.get("code", ""),
                "status_type": row.get("status_type", ""),
                "status_value": row.get("status_value", ""),
                "event_date": row.get("event_date", ""),
                "source": row.get("source", ""),
                "confidence": row.get("confidence", ""),
                "source_url": row.get("source_url", ""),
                "current_market": market or "UNKNOWN",
                "raw_path_count": str(len(raw_paths)),
                "raw_capture_dates": ";".join(capture_dates),
                "raw_paths": ";".join(raw_paths),
                "collection_target": "resolve_market_label",
                "notes": row.get("notes", ""),
            }
        )

    output_rows.sort(key=lambda item: (item["code"], item["status_type"], item["status_value"], item["event_date"]))
    summary = {
        "events_path": events_path,
        "event_rows": len(event_rows),
        "unknown_market_rows": len(output_rows),
        "unknown_market_codes": len({row["code"] for row in output_rows}),
        "raw_capture_dates": sorted(raw_capture_dates),
        "status_type_counts": dict(sorted(status_type_counts.items())),
        "source_counts": dict(sorted(source_counts.items())),
    }
    return output_rows, summary


def _write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _wikilink(path: Path) -> str:
    rendered = path.as_posix()
    return f"[[{rendered}|{rendered}]]"


def _render_counter(counter: dict[str, int]) -> list[str]:
    if not counter:
        return ["| `none` | 0 |"]
    return [f"| `{key or 'blank'}` | {value} |" for key, value in counter.items()]


def _render_capture_window(dates: list[str]) -> str:
    if not dates:
        return "unknown"
    if len(dates) == 1:
        return dates[0]
    return f"{dates[0]}..{dates[-1]}"


def _render_report(summary: dict[str, Any], output: Path) -> str:
    lines = [
        "# Point-in-Time Status Unknown Market Targets",
        "",
        f"- Events: {_wikilink(summary['events_path'])}",
        f"- Output: {_wikilink(output)}",
        "- KIS/KRX API call: `false`",
        "- Order intent generated: `false`",
        "- Backtest readiness impact: `none`",
        "- Interpretation: market-label collection targets only, not status transition evidence",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| Event rows | {summary['event_rows']} |",
        f"| Unknown market rows | {summary['unknown_market_rows']} |",
        f"| Unknown market codes | {summary['unknown_market_codes']} |",
        f"| Raw capture dates | {len(summary['raw_capture_dates'])} |",
        f"| Raw capture date window | `{_render_capture_window(summary['raw_capture_dates'])}` |",
        "",
        "## Status Type Counts",
        "",
        "| Status type | Rows |",
        "| --- | ---: |",
        *_render_counter(summary["status_type_counts"]),
        "",
        "## Source Counts",
        "",
        "| Source | Rows |",
        "| --- | ---: |",
        *_render_counter(summary["source_counts"]),
        "",
        "## Guardrails",
        "",
        "- Resolving these rows may improve market labels, but it does not solve release/resume lifecycle coverage.",
        "- Keep `Backtest readiness` at `hold` until historical status transition evidence and source coverage manifest validation pass.",
        "- Do not infer market labels without official evidence or deterministic local market-data joins.",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Report Point-in-Time status-event rows with UNKNOWN market labels.")
    parser.add_argument("--events", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--report-output", type=Path)
    args = parser.parse_args()

    try:
        rows, summary = build_unknown_market_rows(args.events)
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
