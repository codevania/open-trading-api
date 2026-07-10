"""Render a human checklist for Point-in-Time status evidence capture.

This helper is an operator checklist only. It does not fetch KRX/KIND data,
does not validate or materialize source coverage, does not promote Backtest
readiness, and never creates order intents.
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path
from typing import Any

from quant_io import write_text_lf


REQUIRED_FILL_PACKET_COLUMNS = {
    "batch_id",
    "status_type",
    "source",
    "coverage_start",
    "coverage_end",
    "candidate_tables",
    "source_url_hint",
    "raw_path_suggestion",
    "evidence_capture_status",
    "source_url_to_fill",
    "raw_path_to_fill",
    "confidence_to_fill",
    "order_intent_generated",
}
VALID_CONFIDENCE = {"high", "medium", "low"}


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


def _wikilink(path: Path | None) -> str:
    if path is None:
        return "`not_supplied`"
    rendered = path.as_posix()
    if path.suffix == ".md":
        return f"[[{rendered[:-len(path.suffix)]}|{rendered}]]"
    return f"[[{rendered}|{rendered}]]"


def _is_ready(row: dict[str, str]) -> bool:
    capture_status = row.get("evidence_capture_status", "")
    return (
        bool(row.get("source_url_to_fill", ""))
        and bool(row.get("raw_path_to_fill", ""))
        and row.get("confidence_to_fill", "") in VALID_CONFIDENCE
        and bool(capture_status)
        and not capture_status.startswith("pending")
        and row.get("order_intent_generated", "") == "false"
    )


def build_capture_checklist(fill_packet_path: Path) -> tuple[list[dict[str, str]], dict[str, Any]]:
    fields, rows = _read_csv(fill_packet_path, "source manifest fill packet")
    _require_columns(fields, REQUIRED_FILL_PACKET_COLUMNS, "source manifest fill packet")
    bad_orders = [row.get("batch_id", "") for row in rows if row.get("order_intent_generated", "") != "false"]
    if bad_orders:
        raise ValueError("fill packet contains order intent rows: " + ", ".join(bad_orders))

    checklist_rows = []
    for row in sorted(rows, key=lambda item: item.get("batch_id", "")):
        ready = _is_ready(row)
        checklist_rows.append(
            {
                "batch_id": row.get("batch_id", ""),
                "status_type": row.get("status_type", ""),
                "source": row.get("source", ""),
                "coverage_window": f"{row.get('coverage_start', '')}..{row.get('coverage_end', '')}",
                "candidate_tables": row.get("candidate_tables", ""),
                "source_url_hint": row.get("source_url_hint", ""),
                "raw_path_suggestion": row.get("raw_path_suggestion", ""),
                "capture_state": "ready_for_materialization" if ready else "pending_official_capture",
            }
        )

    source_counts = Counter(row["source"] for row in checklist_rows)
    status_counts = Counter(row["status_type"] for row in checklist_rows)
    summary = {
        "fill_packet_path": fill_packet_path,
        "checklist_rows": len(checklist_rows),
        "pending_rows": sum(1 for row in checklist_rows if row["capture_state"] != "ready_for_materialization"),
        "ready_rows": sum(1 for row in checklist_rows if row["capture_state"] == "ready_for_materialization"),
        "source_counts": dict(sorted(source_counts.items())),
        "status_counts": dict(sorted(status_counts.items())),
    }
    return checklist_rows, summary


def _render_counter(counter: dict[str, int]) -> list[str]:
    if not counter:
        return ["| `none` | 0 |"]
    return [f"| `{key or 'blank'}` | {value} |" for key, value in counter.items()]


def render_report(*, rows: list[dict[str, str]], summary: dict[str, Any]) -> str:
    lines = [
        "# Point-in-Time Status P1 Official Capture Checklist",
        "",
        f"- Fill packet: {_wikilink(summary['fill_packet_path'])}",
        "- KIS/KRX API call: `false`",
        "- Order intent generated: `false`",
        "- Backtest readiness impact: `hold`",
        "- Interpretation: operator checklist only, not source coverage evidence",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| Checklist rows | {summary['checklist_rows']} |",
        f"| Pending rows | {summary['pending_rows']} |",
        f"| Ready rows | {summary['ready_rows']} |",
        "",
        "## Source Counts",
        "",
        "| Source | Rows |",
        "| --- | ---: |",
        *_render_counter(summary["source_counts"]),
        "",
        "## Status Type Counts",
        "",
        "| Status type | Rows |",
        "| --- | ---: |",
        *_render_counter(summary["status_counts"]),
        "",
        "## Capture Rows",
        "",
    ]
    for row in rows:
        lines.extend(
            [
                f"### {row['batch_id']} `{row['status_type']}` / `{row['source']}`",
                "",
                f"- Coverage window: `{row['coverage_window']}`",
                f"- Capture state: `{row['capture_state']}`",
                f"- Candidate tables: `{row['candidate_tables']}`",
                f"- Source URL hint: `{row['source_url_hint'] or 'blank'}`",
                f"- Raw path suggestion: `{row['raw_path_suggestion'] or 'blank'}`",
                "- [ ] Capture official raw evidence from the listed source.",
                "- [ ] Save the raw file under `_report/raw/**`, using the suggestion as a naming aid.",
                "- [ ] Fill `source_url_to_fill`, `raw_path_to_fill`, `confidence_to_fill`, and non-pending `evidence_capture_status` in the fill packet.",
                "",
            ]
        )
    lines.extend(
        [
            "## Next Validation",
            "",
            "1. Re-run [[scripts/quant_point_in_time_status_source_manifest_fill_progress.py|scripts/quant_point_in_time_status_source_manifest_fill_progress.py]].",
            "2. Run [[scripts/quant_point_in_time_status_source_manifest_materialize.py|scripts/quant_point_in_time_status_source_manifest_materialize.py]] only after every row is ready.",
            "3. Run [[scripts/quant_point_in_time_status_source_manifest_validate.py|scripts/quant_point_in_time_status_source_manifest_validate.py]] on the materialized manifest.",
            "",
            "## Guardrails",
            "",
            "- This checklist is not a source coverage manifest.",
            "- `source_url_hint` and `raw_path_suggestion` are aids only; do not copy them into evidence fields before capture.",
            "- Keep `Backtest readiness` at `hold` until official raw capture, manifest validation, coverage audit, lifecycle coverage, costs, OOS, and Bias Control pass.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Render a P1 official capture checklist.")
    parser.add_argument("--fill-packet", required=True, type=Path)
    parser.add_argument("--report-output", type=Path)
    args = parser.parse_args()

    try:
        rows, summary = build_capture_checklist(args.fill_packet)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc

    report = render_report(rows=rows, summary=summary)
    if args.report_output:
        write_text_lf(args.report_output, report)
    else:
        print(report, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
