"""Merge normalized Point-in-Time status-event CSVs.

The merge is evidence-preserving: identical logical events are kept as one
event row, while raw capture paths and notes from each observation are retained
so coverage audits can see multiple source capture dates.
"""

from __future__ import annotations

import argparse
import csv
import re
from collections import Counter
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from quant_io import write_text_lf
except ModuleNotFoundError:  # pragma: no cover - used when imported as scripts.* in tests.
    from scripts.quant_io import write_text_lf


EVENT_FIELDS = (
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
LOGICAL_KEY_FIELDS = ("event_date", "code", "status_type", "status_value", "source", "source_url")
CONFIDENCE_ORDER = {"low": 0, "medium": 1, "high": 2}
RAW_CAPTURE_DATE_RE = re.compile(r"(?:^|[\\/])raw[\\/]\d{4}[\\/](\d{4}-\d{2}-\d{2})(?:[\\/]|$)")


@dataclass(frozen=True)
class MergeInput:
    path: Path
    rows: list[dict[str, str]]


def _read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path.exists():
        raise ValueError(f"status-event CSV not found: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = list(reader.fieldnames or [])
        rows = [{key: (value or "").strip() for key, value in row.items()} for row in reader]
    missing = set(EVENT_FIELDS) - set(fields)
    if missing:
        raise ValueError(f"{path} missing required columns: {', '.join(sorted(missing))}")
    return fields, rows


def _logical_key(row: dict[str, str]) -> tuple[str, ...]:
    return tuple(row.get(field, "") for field in LOGICAL_KEY_FIELDS)


def _split_evidence(value: str) -> list[str]:
    parts = re.split(r"\s*[;|]\s*", value or "")
    return [part for part in parts if part]


def _raw_capture_dates(raw_paths: list[str]) -> list[str]:
    dates: set[str] = set()
    for raw_path in raw_paths:
        for match in RAW_CAPTURE_DATE_RE.finditer(raw_path):
            value = match.group(1)
            try:
                datetime.strptime(value, "%Y-%m-%d")
            except ValueError:
                continue
            dates.add(value)
    return sorted(dates)


def _choose_market(rows: list[dict[str, str]]) -> tuple[str, list[str]]:
    markets = [row.get("market", "") or "UNKNOWN" for row in rows]
    non_unknown = sorted({market for market in markets if market != "UNKNOWN"})
    if len(non_unknown) == 1:
        return non_unknown[0], []
    if len(non_unknown) > 1:
        return non_unknown[0], [f"market_conflict={','.join(non_unknown)}"]
    return "UNKNOWN", []


def _choose_confidence(rows: list[dict[str, str]], extra_notes: list[str]) -> str:
    confidences = [row.get("confidence", "") for row in rows if row.get("confidence", "") in CONFIDENCE_ORDER]
    if not confidences:
        return ""
    if extra_notes:
        return "low"
    return min(confidences, key=lambda value: CONFIDENCE_ORDER[value])


def _merge_rows(rows: list[dict[str, str]]) -> dict[str, str]:
    base = dict(rows[0])
    market, extra_notes = _choose_market(rows)
    raw_paths = sorted({part for row in rows for part in _split_evidence(row.get("raw_path", ""))})
    source_notes = sorted({row.get("notes", "") for row in rows if row.get("notes", "")})
    capture_dates = _raw_capture_dates(raw_paths)
    notes = list(source_notes)
    if len(rows) > 1:
        notes.append(f"merged_observations={len(rows)}")
    if capture_dates:
        notes.append(f"raw_capture_dates={','.join(capture_dates)}")
    notes.extend(extra_notes)
    base.update(
        {
            "market": market,
            "raw_path": ";".join(raw_paths),
            "confidence": _choose_confidence(rows, extra_notes),
            "notes": " | ".join(dict.fromkeys(note for note in notes if note)),
        }
    )
    return {field: base.get(field, "") for field in EVENT_FIELDS}


def merge_status_event_files(paths: list[Path]) -> tuple[list[dict[str, str]], dict[str, Any]]:
    if len(paths) < 2:
        raise ValueError("at least two status-event CSV inputs are required")
    inputs: list[MergeInput] = []
    grouped: dict[tuple[str, ...], list[dict[str, str]]] = {}
    input_rows = 0
    for path in paths:
        _fields, rows = _read_csv(path)
        inputs.append(MergeInput(path=path, rows=rows))
        input_rows += len(rows)
        for row in rows:
            grouped.setdefault(_logical_key(row), []).append(row)

    merged_rows = [_merge_rows(rows) for rows in grouped.values()]
    merged_rows.sort(key=lambda row: (row["event_date"], row["code"], row["status_type"], row["status_value"]))
    raw_paths = [part for row in merged_rows for part in _split_evidence(row.get("raw_path", ""))]
    status_type_counts = Counter(row["status_type"] for row in merged_rows)
    summary = {
        "inputs": paths,
        "input_rows": input_rows,
        "output_rows": len(merged_rows),
        "merged_duplicate_rows": input_rows - len(merged_rows),
        "logical_event_keys": len(grouped),
        "raw_path_count": len(set(raw_paths)),
        "raw_capture_dates": _raw_capture_dates(raw_paths),
        "status_type_counts": dict(sorted(status_type_counts.items())),
    }
    return merged_rows, summary


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=EVENT_FIELDS, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def _wikilink(path: Path) -> str:
    rendered = path.as_posix()
    return f"[[{rendered}|{rendered}]]"


def _render_report(summary: dict[str, Any], output: Path) -> str:
    lines = [
        "# Point-in-Time Status Events Merge",
        "",
        f"- Output: {_wikilink(output)}",
        "- Interpretation: local evidence merge only, not historical-complete status coverage",
        "- Backtest readiness: `hold`",
        "",
        "## Inputs",
        "",
    ]
    for path in summary["inputs"]:
        lines.append(f"- {_wikilink(path)}")
    lines.extend(
        [
            "",
            "## Summary",
            "",
            "| Metric | Value |",
            "| --- | ---: |",
            f"| Input rows | {summary['input_rows']} |",
            f"| Output rows | {summary['output_rows']} |",
            f"| Merged duplicate rows | {summary['merged_duplicate_rows']} |",
            f"| Logical event keys | {summary['logical_event_keys']} |",
            f"| Raw source paths | {summary['raw_path_count']} |",
            f"| Raw capture dates | {len(summary['raw_capture_dates'])} |",
            "",
            "## Raw Capture Dates",
            "",
        ]
    )
    for capture_date in summary["raw_capture_dates"]:
        lines.append(f"- `{capture_date}`")
    if not summary["raw_capture_dates"]:
        lines.append("- `none`")
    lines.extend(["", "## Status Type Counts", "", "| Status type | Rows |", "| --- | ---: |"])
    for status_type, count in summary["status_type_counts"].items():
        lines.append(f"| `{status_type}` | {count} |")
    lines.extend(
        [
            "",
            "## Guardrails",
            "",
            "- Logical duplicates are merged by event date, code, status type/value, source, and source URL.",
            "- Raw paths from duplicate observations are retained so coverage audits can see capture-date evidence.",
            "- This does not create release/resume events and does not make `Backtest` ready.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Merge normalized Point-in-Time status-event CSVs.")
    parser.add_argument("--events", action="append", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--report-output", type=Path)
    args = parser.parse_args()

    try:
        rows, summary = merge_status_event_files(args.events)
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
