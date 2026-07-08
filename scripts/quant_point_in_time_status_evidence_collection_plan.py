"""Build a Point-in-Time status evidence collection plan.

This local helper consolidates already-generated status blocker artifacts into
actionable collection rows. It does not fetch KRX/KIND data, does not validate
source evidence, does not promote Backtest readiness, and never creates order
intents.
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from quant_io import write_text_lf


REQUIRED_LIFECYCLE_COLUMNS = {
    "code",
    "market",
    "status_type",
    "lifecycle_gap_status",
    "active_like_rows",
    "release_like_rows",
    "first_active_event_date",
    "latest_active_event_date",
    "raw_paths",
    "notes",
}
REQUIRED_MANIFEST_COLUMNS = {
    "status_type",
    "coverage_start",
    "coverage_end",
    "source",
    "source_url",
    "raw_path",
    "confidence",
    "lifecycle_target_groups",
    "lifecycle_target_codes",
    "market_labels",
    "candidate_tables",
    "allowed_url_prefixes",
    "draft_status",
    "notes",
}
REQUIRED_UNKNOWN_MARKET_COLUMNS = {
    "code",
    "status_type",
    "status_value",
    "event_date",
    "source",
    "confidence",
    "source_url",
    "current_market",
    "raw_paths",
    "collection_target",
    "notes",
}
OUTPUT_FIELDS = (
    "priority",
    "blocker_type",
    "status_type",
    "code",
    "market",
    "lifecycle_gap_status",
    "target_groups",
    "active_like_rows",
    "release_like_rows",
    "manifest_source",
    "manifest_status",
    "unknown_market_target",
    "suggested_source",
    "required_evidence",
    "collection_status",
    "order_intent_generated",
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


def _split_semicolon(value: str) -> list[str]:
    return [item.strip() for item in str(value or "").split(";") if item.strip()]


def _int_value(value: str) -> int:
    try:
        return int(float(str(value or "0").strip()))
    except ValueError:
        return 0


def _join_unique(values: list[str]) -> str:
    return ";".join(dict.fromkeys(value for value in values if value))


def _manifest_by_status(rows: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    indexed: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        indexed[row.get("status_type", "")].append(row)
    return indexed


def _status_sources(manifest_rows: dict[str, list[dict[str, str]]], status_type: str) -> str:
    sources = [row.get("source", "") for row in manifest_rows.get(status_type, [])]
    return _join_unique(sources) or "not_in_manifest_draft"


def _source_summary(row: dict[str, str]) -> str:
    source = row.get("source", "")
    tables = row.get("candidate_tables", "")
    if tables:
        return f"{source}:{tables}"
    return source


def _manifest_plan_rows(manifest_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    plan_rows: list[dict[str, str]] = []
    for row in manifest_rows:
        plan_rows.append(
            {
                "priority": "1",
                "blocker_type": "source_manifest_evidence",
                "status_type": row.get("status_type", ""),
                "code": "",
                "market": row.get("market_labels", ""),
                "lifecycle_gap_status": "",
                "target_groups": row.get("lifecycle_target_groups", "0"),
                "active_like_rows": "",
                "release_like_rows": "",
                "manifest_source": row.get("source", ""),
                "manifest_status": row.get("draft_status", ""),
                "unknown_market_target": "false",
                "suggested_source": _source_summary(row),
                "required_evidence": (
                    "fill source_url, raw_path, and confidence with official raw evidence "
                    "covering the market-data window"
                ),
                "collection_status": "pending_raw_evidence",
                "order_intent_generated": "false",
                "notes": row.get("notes", ""),
            }
        )
    return plan_rows


def _lifecycle_plan_rows(
    lifecycle_rows: list[dict[str, str]],
    manifest_rows_by_status: dict[str, list[dict[str, str]]],
) -> list[dict[str, str]]:
    plan_rows: list[dict[str, str]] = []
    for row in lifecycle_rows:
        if row.get("lifecycle_gap_status", "") != "missing_release_resume_evidence":
            continue
        status_type = row.get("status_type", "")
        plan_rows.append(
            {
                "priority": "2",
                "blocker_type": "release_resume_evidence",
                "status_type": status_type,
                "code": row.get("code", ""),
                "market": row.get("market", ""),
                "lifecycle_gap_status": row.get("lifecycle_gap_status", ""),
                "target_groups": "1",
                "active_like_rows": row.get("active_like_rows", ""),
                "release_like_rows": row.get("release_like_rows", ""),
                "manifest_source": _status_sources(manifest_rows_by_status, status_type),
                "manifest_status": "requires_filled_manifest",
                "unknown_market_target": "false",
                "suggested_source": _status_sources(manifest_rows_by_status, status_type),
                "required_evidence": (
                    "official release/resume, cleared, delisting withdrawal, or other dated "
                    "inactive-state evidence for this code/status group"
                ),
                "collection_status": "pending_release_resume_evidence",
                "order_intent_generated": "false",
                "notes": row.get("notes", ""),
            }
        )
    return plan_rows


def _unknown_market_plan_rows(
    unknown_market_rows: list[dict[str, str]],
    manifest_rows_by_status: dict[str, list[dict[str, str]]],
) -> list[dict[str, str]]:
    plan_rows: list[dict[str, str]] = []
    for row in unknown_market_rows:
        status_type = row.get("status_type", "")
        plan_rows.append(
            {
                "priority": "3",
                "blocker_type": "market_label_resolution",
                "status_type": status_type,
                "code": row.get("code", ""),
                "market": row.get("current_market", "UNKNOWN") or "UNKNOWN",
                "lifecycle_gap_status": "",
                "target_groups": "1",
                "active_like_rows": "",
                "release_like_rows": "",
                "manifest_source": _status_sources(manifest_rows_by_status, status_type),
                "manifest_status": "requires_market_label_evidence",
                "unknown_market_target": "true",
                "suggested_source": row.get("source", "") or _status_sources(manifest_rows_by_status, status_type),
                "required_evidence": (
                    "official market label, listing status, or deterministic local market-data "
                    "join evidence for this code"
                ),
                "collection_status": "pending_market_label_evidence",
                "order_intent_generated": "false",
                "notes": row.get("notes", ""),
            }
        )
    return plan_rows


def build_evidence_collection_plan(
    *,
    lifecycle_gaps_path: Path,
    source_manifest_draft_path: Path,
    unknown_market_targets_path: Path | None = None,
) -> tuple[list[dict[str, str]], dict[str, Any]]:
    lifecycle_fields, lifecycle_rows = _read_csv(lifecycle_gaps_path, "lifecycle gaps")
    _require_columns(lifecycle_fields, REQUIRED_LIFECYCLE_COLUMNS, "lifecycle gaps")
    manifest_fields, manifest_rows = _read_csv(source_manifest_draft_path, "source manifest draft")
    _require_columns(manifest_fields, REQUIRED_MANIFEST_COLUMNS, "source manifest draft")

    unknown_rows: list[dict[str, str]] = []
    if unknown_market_targets_path is not None:
        unknown_fields, unknown_rows = _read_csv(unknown_market_targets_path, "unknown market targets")
        _require_columns(unknown_fields, REQUIRED_UNKNOWN_MARKET_COLUMNS, "unknown market targets")

    manifest_rows_by_status = _manifest_by_status(manifest_rows)
    plan_rows = [
        *_manifest_plan_rows(manifest_rows),
        *_lifecycle_plan_rows(lifecycle_rows, manifest_rows_by_status),
        *_unknown_market_plan_rows(unknown_rows, manifest_rows_by_status),
    ]
    plan_rows.sort(
        key=lambda row: (
            _int_value(row["priority"]),
            row["blocker_type"],
            row["status_type"],
            row["code"],
            row["manifest_source"],
        )
    )

    priority_counts = Counter(row["priority"] for row in plan_rows)
    blocker_counts = Counter(row["blocker_type"] for row in plan_rows)
    status_type_counts = Counter(row["status_type"] for row in plan_rows)
    collection_status_counts = Counter(row["collection_status"] for row in plan_rows)
    summary = {
        "lifecycle_gaps_path": lifecycle_gaps_path,
        "source_manifest_draft_path": source_manifest_draft_path,
        "unknown_market_targets_path": unknown_market_targets_path,
        "lifecycle_gap_rows": len(lifecycle_rows),
        "manifest_draft_rows": len(manifest_rows),
        "unknown_market_rows": len(unknown_rows),
        "plan_rows": len(plan_rows),
        "priority_counts": dict(sorted(priority_counts.items())),
        "blocker_counts": dict(sorted(blocker_counts.items())),
        "status_type_counts": dict(sorted(status_type_counts.items())),
        "collection_status_counts": dict(sorted(collection_status_counts.items())),
    }
    return plan_rows, summary


def _write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS, lineterminator="\n")
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
    return [f"| `{key or 'blank'}` | {value} |" for key, value in counter.items()]


def _render_report(summary: dict[str, Any], output_path: Path) -> str:
    lines = [
        "# Point-in-Time Status Evidence Collection Plan",
        "",
        f"- Lifecycle gaps: {_wikilink(summary['lifecycle_gaps_path'])}",
        f"- Source manifest draft: {_wikilink(summary['source_manifest_draft_path'])}",
        f"- Unknown market targets: {_wikilink(summary['unknown_market_targets_path'])}",
        f"- Output: {_wikilink(output_path)}",
        "- KIS/KRX API call: `false`",
        "- Order intent generated: `false`",
        "- Backtest readiness impact: `hold`",
        "- Interpretation: collection plan only, not source coverage evidence",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| Lifecycle gap rows | {summary['lifecycle_gap_rows']} |",
        f"| Manifest draft rows | {summary['manifest_draft_rows']} |",
        f"| Unknown market rows | {summary['unknown_market_rows']} |",
        f"| Collection plan rows | {summary['plan_rows']} |",
        "",
        "## Priority Counts",
        "",
        "| Priority | Rows |",
        "| --- | ---: |",
        *_render_counter(summary["priority_counts"]),
        "",
        "## Blocker Counts",
        "",
        "| Blocker | Rows |",
        "| --- | ---: |",
        *_render_counter(summary["blocker_counts"]),
        "",
        "## Status Type Counts",
        "",
        "| Status type | Rows |",
        "| --- | ---: |",
        *_render_counter(summary["status_type_counts"]),
        "",
        "## Collection Status Counts",
        "",
        "| Collection status | Rows |",
        "| --- | ---: |",
        *_render_counter(summary["collection_status_counts"]),
        "",
        "## Execution Order",
        "",
        "1. Fill source manifest evidence rows from official raw KRX/KIND files.",
        "2. Collect release/resume or inactive-state evidence for lifecycle gap rows.",
        "3. Resolve UNKNOWN market labels only with official evidence or deterministic local joins.",
        "",
        "## Guardrails",
        "",
        "- This plan is not a filled source coverage manifest.",
        "- Do not pass this plan to the coverage audit as evidence.",
        "- Keep `Backtest readiness` at `hold` until filled manifest validation, lifecycle coverage, costs, OOS, and Bias Control pass.",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a Point-in-Time status evidence collection plan.")
    parser.add_argument("--lifecycle-gaps", required=True, type=Path)
    parser.add_argument("--source-manifest-draft", required=True, type=Path)
    parser.add_argument("--unknown-market-targets", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--report-output", type=Path)
    args = parser.parse_args()

    try:
        rows, summary = build_evidence_collection_plan(
            lifecycle_gaps_path=args.lifecycle_gaps,
            source_manifest_draft_path=args.source_manifest_draft,
            unknown_market_targets_path=args.unknown_market_targets,
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
