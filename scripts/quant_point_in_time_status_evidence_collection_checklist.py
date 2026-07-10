"""Render an operator checklist from Point-in-Time status evidence batches.

This helper is local planning only. It does not fetch KRX/KIND data, does not
validate source coverage, does not promote Backtest readiness, and never
creates order intents.
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path
from typing import Any

from quant_io import write_text_lf


REQUIRED_QUEUE_COLUMNS = {
    "batch_id",
    "priority",
    "blocker_type",
    "status_type",
    "suggested_source",
    "manifest_source",
    "collection_status",
    "market_scope",
    "row_count",
    "code_count",
    "code_sample",
    "required_evidence",
    "source_plan_rows",
    "order_intent_generated",
    "notes",
}


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


def _int_value(value: str) -> int:
    try:
        return int(float(str(value or "0").strip()))
    except ValueError:
        return 0


def _batch_sort_key(row: dict[str, str]) -> tuple[int, str]:
    return (_int_value(row.get("priority", "")), row.get("batch_id", ""))


def _wikilink(path: Path | None) -> str:
    if path is None:
        return "`not_supplied`"
    rendered = path.as_posix()
    if path.suffix == ".md":
        return f"[[{rendered[:-len(path.suffix)]}|{rendered}]]"
    return f"[[{rendered}|{rendered}]]"


def _raw_path_suggestion(batch_id: str) -> str:
    safe_batch = batch_id.lower() or "unknown-batch"
    return f"_report/raw/quant/status-evidence/{safe_batch}/"


def _priority_section(priority: str, blocker_type: str) -> str:
    if priority == "1":
        return "P1 Source Manifest Evidence"
    if priority == "2":
        return "P2 Release/Resume Evidence"
    if priority == "3":
        return "P3 Market Label Evidence"
    return f"P{priority or 'unknown'} {blocker_type or 'Evidence'}"


def _next_validation(blocker_type: str) -> str:
    if blocker_type == "source_manifest_evidence":
        return "Fill the P1 source-manifest packet, then run fill-progress, materialize, validate, and coverage audit."
    if blocker_type == "release_resume_evidence":
        return "Extract dated release/resume or cleared-state events, then validate and replay the expanded status events."
    if blocker_type == "market_label_resolution":
        return "Resolve market labels only with official evidence or deterministic local joins, then rerun market enrichment."
    return "Capture evidence, keep it under _report/raw/**, and rerun the relevant status validation."


def build_evidence_collection_checklist(queue_path: Path) -> tuple[list[dict[str, str]], dict[str, Any]]:
    fields, rows = _read_csv(queue_path, "evidence collection queue")
    _require_columns(fields, REQUIRED_QUEUE_COLUMNS, "evidence collection queue")
    bad_orders = [row.get("batch_id", "") for row in rows if row.get("order_intent_generated", "") != "false"]
    if bad_orders:
        raise ValueError("evidence queue contains order intent rows: " + ", ".join(bad_orders))

    checklist_rows: list[dict[str, str]] = []
    for row in sorted(rows, key=_batch_sort_key):
        checklist_rows.append(
            {
                "batch_id": row.get("batch_id", ""),
                "priority": row.get("priority", ""),
                "blocker_type": row.get("blocker_type", ""),
                "status_type": row.get("status_type", ""),
                "suggested_source": row.get("suggested_source", ""),
                "manifest_source": row.get("manifest_source", ""),
                "collection_status": row.get("collection_status", ""),
                "market_scope": row.get("market_scope", ""),
                "row_count": row.get("row_count", "0"),
                "code_count": row.get("code_count", "0"),
                "code_sample": row.get("code_sample", ""),
                "required_evidence": row.get("required_evidence", ""),
                "source_plan_rows": row.get("source_plan_rows", ""),
                "raw_path_suggestion": _raw_path_suggestion(row.get("batch_id", "")),
                "section": _priority_section(row.get("priority", ""), row.get("blocker_type", "")),
                "next_validation": _next_validation(row.get("blocker_type", "")),
            }
        )

    priority_counts = Counter(row["priority"] for row in checklist_rows)
    blocker_counts = Counter(row["blocker_type"] for row in checklist_rows)
    status_counts = Counter(row["status_type"] for row in checklist_rows)
    collection_status_counts = Counter(row["collection_status"] for row in checklist_rows)
    market_counts = Counter(row["market_scope"] for row in checklist_rows)
    pending_batches = sum(1 for row in checklist_rows if row["collection_status"].startswith("pending"))
    summary = {
        "queue_path": queue_path,
        "checklist_batches": len(checklist_rows),
        "queued_source_rows": sum(_int_value(row["row_count"]) for row in checklist_rows),
        "queued_codes": sum(_int_value(row["code_count"]) for row in checklist_rows),
        "pending_batches": pending_batches,
        "priority_counts": dict(sorted(priority_counts.items())),
        "blocker_counts": dict(sorted(blocker_counts.items())),
        "status_counts": dict(sorted(status_counts.items())),
        "collection_status_counts": dict(sorted(collection_status_counts.items())),
        "market_counts": dict(sorted(market_counts.items())),
    }
    return checklist_rows, summary


def _render_counter(counter: dict[str, int]) -> list[str]:
    if not counter:
        return ["| `none` | 0 |"]
    return [f"| `{key or 'blank'}` | {value} |" for key, value in counter.items()]


def _render_summary(summary: dict[str, Any]) -> list[str]:
    return [
        "## Summary",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| Checklist batches | {summary['checklist_batches']} |",
        f"| Pending batches | {summary['pending_batches']} |",
        f"| Queued source rows | {summary['queued_source_rows']} |",
        f"| Queued code references | {summary['queued_codes']} |",
        "",
        "## Priority Counts",
        "",
        "| Priority | Batches |",
        "| --- | ---: |",
        *_render_counter(summary["priority_counts"]),
        "",
        "## Blocker Counts",
        "",
        "| Blocker | Batches |",
        "| --- | ---: |",
        *_render_counter(summary["blocker_counts"]),
        "",
        "## Status Type Counts",
        "",
        "| Status type | Batches |",
        "| --- | ---: |",
        *_render_counter(summary["status_counts"]),
        "",
        "## Collection Status Counts",
        "",
        "| Collection status | Batches |",
        "| --- | ---: |",
        *_render_counter(summary["collection_status_counts"]),
        "",
        "## Market Scope Counts",
        "",
        "| Market scope | Batches |",
        "| --- | ---: |",
        *_render_counter(summary["market_counts"]),
        "",
    ]


def _render_batch(row: dict[str, str]) -> list[str]:
    return [
        f"### {row['batch_id']} `{row['blocker_type']}` / `{row['status_type']}`",
        "",
        f"- Collection status: `{row['collection_status'] or 'blank'}`",
        f"- Market scope: `{row['market_scope'] or 'blank'}`",
        f"- Source rows: `{row['row_count']}`",
        f"- Code references: `{row['code_count']}`",
        f"- Code sample: `{row['code_sample'] or 'blank'}`",
        f"- Suggested source: `{row['suggested_source'] or 'blank'}`",
        f"- Manifest source: `{row['manifest_source'] or 'blank'}`",
        f"- Required evidence: `{row['required_evidence'] or 'blank'}`",
        f"- Source plan rows: `{row['source_plan_rows'] or 'blank'}`",
        f"- Raw path suggestion: `{row['raw_path_suggestion']}`",
        "- [ ] Open the suggested official source or deterministic local evidence path.",
        "- [ ] Capture the raw response, downloaded file, screenshot metadata, or deterministic join evidence under the suggested raw directory.",
        "- [ ] Record source URL, raw path, confidence, capture date, and extraction notes in the follow-up evidence artifact before promotion.",
        f"- [ ] Next validation: {row['next_validation']}",
        "",
    ]


def render_report(*, rows: list[dict[str, str]], summary: dict[str, Any]) -> str:
    lines = [
        "# Point-in-Time Status Evidence Collection Checklist",
        "",
        f"- Evidence queue rows: {_wikilink(summary['queue_path'])}",
        "- KIS/KRX API call: `false`",
        "- Order intent generated: `false`",
        "- Backtest readiness impact: `hold`",
        "- Interpretation: operator checklist only, not source coverage evidence",
        "",
        *_render_summary(summary),
        "## Execution Order",
        "",
        "1. Complete `P1-*` source manifest evidence first.",
        "2. Complete `P2-*` release/resume evidence after the matching official source coverage is available.",
        "3. Complete `P3-*` market-label evidence only where official evidence or deterministic joins support the label.",
        "",
        "## Checklist Batches",
        "",
    ]

    current_section = ""
    for row in rows:
        if row["section"] != current_section:
            current_section = row["section"]
            lines.extend([f"## {current_section}", ""])
        lines.extend(_render_batch(row))

    lines.extend(
        [
            "## Guardrails",
            "",
            "- This checklist is not a source coverage manifest.",
            "- Do not pass checklist or queue rows to the coverage audit as evidence.",
            "- Keep `Backtest readiness` at `hold` until official raw capture, manifest validation, coverage audit, lifecycle coverage, costs, OOS, and Bias Control pass.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Render a Point-in-Time status evidence collection checklist.")
    parser.add_argument("--queue", required=True, type=Path)
    parser.add_argument("--report-output", type=Path)
    args = parser.parse_args()

    try:
        rows, summary = build_evidence_collection_checklist(args.queue)
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
