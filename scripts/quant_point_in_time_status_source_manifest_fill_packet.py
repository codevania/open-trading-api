"""Build a source-manifest fill packet from P1 evidence queue batches.

This helper prepares the manual/official source capture step. It does not fetch
KRX/KIND data, does not validate source coverage, does not promote Backtest
readiness, and never creates order intents.
"""

from __future__ import annotations

import argparse
import csv
import re
from collections import Counter
from pathlib import Path
from typing import Any

from quant_io import write_text_lf


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
OUTPUT_FIELDS = (
    "batch_id",
    "manifest_draft_row_number",
    "status_type",
    "source",
    "coverage_start",
    "coverage_end",
    "market_labels",
    "lifecycle_target_groups",
    "lifecycle_target_codes",
    "candidate_tables",
    "allowed_url_prefixes",
    "source_url_hint",
    "raw_path_suggestion",
    "suggested_source",
    "required_evidence",
    "collection_status",
    "evidence_capture_status",
    "source_url_to_fill",
    "raw_path_to_fill",
    "confidence_to_fill",
    "order_intent_generated",
    "manifest_notes",
    "queue_notes",
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


def _join_unique(values: list[str], *, default: str = "") -> str:
    rendered = ";".join(dict.fromkeys(value for value in values if value))
    return rendered or default


def _manifest_key(row: dict[str, str]) -> tuple[str, str]:
    return row.get("status_type", ""), row.get("source", "")


def _queue_key(row: dict[str, str]) -> tuple[str, str]:
    return row.get("status_type", ""), row.get("manifest_source", "")


def _slug(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.strip().lower()).strip("-")
    return slug or "unknown"


def _source_url_hint(row: dict[str, str]) -> str:
    if row.get("source_url", ""):
        return row["source_url"]
    prefixes = [part.strip() for part in row.get("allowed_url_prefixes", "").split(";") if part.strip()]
    return prefixes[0] if prefixes else ""


def _raw_path_suggestion(*, queue_row: dict[str, str], manifest_row: dict[str, str]) -> str:
    start = manifest_row.get("coverage_start", "").replace("-", "") or "unknown-start"
    end = manifest_row.get("coverage_end", "").replace("-", "") or "unknown-end"
    file_name = "-".join(
        [
            _slug(queue_row.get("batch_id", "")),
            _slug(manifest_row.get("status_type", "")),
            _slug(manifest_row.get("source", "")),
        ]
    )
    return f"_report/raw/quant/status-source-manifest/{start}-{end}/{file_name}.json"


def _p1_queue_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    filtered = [
        row
        for row in rows
        if row.get("priority") == "1" and row.get("blocker_type") == "source_manifest_evidence"
    ]
    if not filtered:
        raise ValueError("evidence queue has no P1 source_manifest_evidence rows")
    for row in filtered:
        if row.get("order_intent_generated") != "false":
            raise ValueError("P1 evidence queue contains an order intent row")
    return sorted(filtered, key=lambda row: row.get("batch_id", ""))


def _index_manifest(rows: list[dict[str, str]]) -> dict[tuple[str, str], tuple[int, dict[str, str]]]:
    indexed: dict[tuple[str, str], tuple[int, dict[str, str]]] = {}
    for row_number, row in enumerate(rows, start=2):
        key = _manifest_key(row)
        if key in indexed:
            raise ValueError(f"source manifest draft has duplicate status/source row: {key[0]}/{key[1]}")
        indexed[key] = row_number, row
    return indexed


def _build_packet_row(
    *,
    queue_row: dict[str, str],
    manifest_row_number: int,
    manifest_row: dict[str, str],
) -> dict[str, str]:
    return {
        "batch_id": queue_row["batch_id"],
        "manifest_draft_row_number": str(manifest_row_number),
        "status_type": manifest_row["status_type"],
        "source": manifest_row["source"],
        "coverage_start": manifest_row["coverage_start"],
        "coverage_end": manifest_row["coverage_end"],
        "market_labels": manifest_row["market_labels"],
        "lifecycle_target_groups": manifest_row["lifecycle_target_groups"],
        "lifecycle_target_codes": manifest_row["lifecycle_target_codes"],
        "candidate_tables": manifest_row["candidate_tables"],
        "allowed_url_prefixes": manifest_row["allowed_url_prefixes"],
        "source_url_hint": _source_url_hint(manifest_row),
        "raw_path_suggestion": _raw_path_suggestion(queue_row=queue_row, manifest_row=manifest_row),
        "suggested_source": queue_row["suggested_source"],
        "required_evidence": queue_row["required_evidence"],
        "collection_status": queue_row["collection_status"],
        "evidence_capture_status": "pending_official_raw_capture",
        "source_url_to_fill": manifest_row["source_url"],
        "raw_path_to_fill": manifest_row["raw_path"],
        "confidence_to_fill": manifest_row["confidence"],
        "order_intent_generated": "false",
        "manifest_notes": manifest_row["notes"],
        "queue_notes": queue_row["notes"],
    }


def build_source_manifest_fill_packet(
    *,
    source_manifest_draft_path: Path,
    evidence_queue_path: Path,
) -> tuple[list[dict[str, str]], dict[str, Any]]:
    manifest_fields, manifest_rows = _read_csv(source_manifest_draft_path, "source manifest draft")
    _require_columns(manifest_fields, REQUIRED_MANIFEST_COLUMNS, "source manifest draft")
    queue_fields, queue_rows = _read_csv(evidence_queue_path, "evidence queue")
    _require_columns(queue_fields, REQUIRED_QUEUE_COLUMNS, "evidence queue")

    manifest_index = _index_manifest(manifest_rows)
    p1_rows = _p1_queue_rows(queue_rows)
    packet_rows: list[dict[str, str]] = []
    for queue_row in p1_rows:
        key = _queue_key(queue_row)
        manifest_match = manifest_index.get(key)
        if manifest_match is None:
            raise ValueError(f"P1 queue row has no matching manifest draft row: {key[0]}/{key[1]}")
        manifest_row_number, manifest_row = manifest_match
        packet_rows.append(
            _build_packet_row(
                queue_row=queue_row,
                manifest_row_number=manifest_row_number,
                manifest_row=manifest_row,
            )
        )

    packet_keys = {_queue_key(row) for row in p1_rows}
    unmatched_manifest_rows = [
        f"{row.get('status_type', '')}/{row.get('source', '')}"
        for row in manifest_rows
        if _manifest_key(row) not in packet_keys
    ]
    status_counts = Counter(row["status_type"] for row in packet_rows)
    source_counts = Counter(row["source"] for row in packet_rows)
    coverage_windows = sorted(
        {
            f"{row['coverage_start']}..{row['coverage_end']}"
            for row in packet_rows
            if row.get("coverage_start") and row.get("coverage_end")
        }
    )
    summary = {
        "source_manifest_draft_path": source_manifest_draft_path,
        "evidence_queue_path": evidence_queue_path,
        "manifest_draft_rows": len(manifest_rows),
        "p1_queue_batches": len(p1_rows),
        "packet_rows": len(packet_rows),
        "unmatched_manifest_rows": unmatched_manifest_rows,
        "coverage_windows": coverage_windows,
        "status_counts": dict(sorted(status_counts.items())),
        "source_counts": dict(sorted(source_counts.items())),
    }
    return packet_rows, summary


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
    if path.suffix == ".md":
        target = rendered[: -len(path.suffix)]
        return f"[[{target}|{rendered}]]"
    return f"[[{rendered}|{rendered}]]"


def _render_counter(counter: dict[str, int]) -> list[str]:
    if not counter:
        return ["| `none` | 0 |"]
    return [f"| `{key or 'blank'}` | {value} |" for key, value in counter.items()]


def _render_report(summary: dict[str, Any], output_path: Path) -> str:
    unmatched = ";".join(summary["unmatched_manifest_rows"]) or "none"
    lines = [
        "# Point-in-Time Status Source Manifest Fill Packet",
        "",
        f"- Source manifest draft: {_wikilink(summary['source_manifest_draft_path'])}",
        f"- Evidence queue: {_wikilink(summary['evidence_queue_path'])}",
        f"- Fill packet rows: {_wikilink(output_path)}",
        f"- Coverage windows: `{','.join(summary['coverage_windows']) or 'unknown'}`",
        "- KIS/KRX API call: `false`",
        "- Order intent generated: `false`",
        "- Backtest readiness impact: `hold`",
        "- Interpretation: fill checklist only, not source coverage evidence",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| Manifest draft rows | {summary['manifest_draft_rows']} |",
        f"| P1 queue batches | {summary['p1_queue_batches']} |",
        f"| Fill packet rows | {summary['packet_rows']} |",
        f"| Unmatched manifest rows | `{unmatched}` |",
        "",
        "## Status Type Counts",
        "",
        "| Status type | Rows |",
        "| --- | ---: |",
        *_render_counter(summary["status_counts"]),
        "",
        "## Source Counts",
        "",
        "| Source | Rows |",
        "| --- | ---: |",
        *_render_counter(summary["source_counts"]),
        "",
        "## Fill Instructions",
        "",
        "1. Use each `batch_id` to capture an official raw file from the listed source and candidate table.",
        "2. Use `source_url_hint` and `raw_path_suggestion` as capture aids only; adjust the final path extension if the official export is not JSON.",
        "3. Fill `source_url_to_fill`, `raw_path_to_fill`, and `confidence_to_fill` only after the raw file is saved under `_report/raw/**`.",
        "4. Convert filled packet evidence into a source coverage manifest, then run the manifest validator and coverage audit.",
        "",
        "## Guardrails",
        "",
        "- This packet is not a valid source coverage manifest while fill fields are blank.",
        "- Do not pass this packet to the coverage audit as evidence.",
        "- Keep `Backtest readiness` at `hold` until filled manifest validation, lifecycle coverage, costs, OOS, and Bias Control pass.",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a Point-in-Time source-manifest fill packet from P1 queue rows.")
    parser.add_argument("--source-manifest-draft", required=True, type=Path)
    parser.add_argument("--evidence-queue", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--report-output", type=Path)
    args = parser.parse_args()

    try:
        rows, summary = build_source_manifest_fill_packet(
            source_manifest_draft_path=args.source_manifest_draft,
            evidence_queue_path=args.evidence_queue,
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
