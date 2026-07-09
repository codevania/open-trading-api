"""Report fill progress for a Point-in-Time source-manifest fill packet.

This helper is a non-promoting checklist audit. It does not fetch KRX/KIND
data, does not validate source coverage, does not materialize a manifest, and
does not create order intents.
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from quant_io import write_text_lf


REQUIRED_FILL_PACKET_COLUMNS = {
    "batch_id",
    "status_type",
    "source",
    "coverage_start",
    "coverage_end",
    "evidence_capture_status",
    "source_url_to_fill",
    "raw_path_to_fill",
    "confidence_to_fill",
    "order_intent_generated",
}
PROGRESS_FIELDS = (
    "row_number",
    "batch_id",
    "status_type",
    "source",
    "evidence_capture_status",
    "source_url_status",
    "raw_path_status",
    "raw_path_exists",
    "confidence_status",
    "order_intent_status",
    "materializable_status",
    "missing_fields",
)
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


def _normalize_path(value: str) -> str:
    return value.replace("\\", "/")


def _status(value: bool) -> str:
    return "pass" if value else "missing"


def _progress_row(*, row_number: int, row: dict[str, str], repo_root: Path) -> dict[str, str]:
    source_url_filled = bool(row.get("source_url_to_fill", ""))
    raw_path = _normalize_path(row.get("raw_path_to_fill", ""))
    raw_path_filled = bool(raw_path)
    raw_path_exists = raw_path_filled and (repo_root / raw_path).exists()
    confidence = row.get("confidence_to_fill", "")
    confidence_valid = confidence in VALID_CONFIDENCE
    capture_status = row.get("evidence_capture_status", "")
    capture_non_pending = bool(capture_status) and not capture_status.startswith("pending")
    order_intent_ok = row.get("order_intent_generated", "") == "false"

    missing_fields: list[str] = []
    if not source_url_filled:
        missing_fields.append("source_url_to_fill")
    if not raw_path_filled:
        missing_fields.append("raw_path_to_fill")
    if not confidence_valid:
        missing_fields.append("confidence_to_fill")
    if not capture_non_pending:
        missing_fields.append("evidence_capture_status")
    if not order_intent_ok:
        missing_fields.append("order_intent_generated")

    materializable = not missing_fields
    return {
        "row_number": str(row_number),
        "batch_id": row.get("batch_id", ""),
        "status_type": row.get("status_type", ""),
        "source": row.get("source", ""),
        "evidence_capture_status": capture_status,
        "source_url_status": _status(source_url_filled),
        "raw_path_status": _status(raw_path_filled),
        "raw_path_exists": "true" if raw_path_exists else "false",
        "confidence_status": "pass" if confidence_valid else "invalid_or_missing",
        "order_intent_status": "pass" if order_intent_ok else "fail",
        "materializable_status": "ready" if materializable else "blocked",
        "missing_fields": ";".join(missing_fields) or "none",
    }


def summarize_fill_progress(
    *,
    fill_packet_path: Path,
    repo_root: Path | None = None,
) -> tuple[list[dict[str, str]], dict[str, Any]]:
    repo_root = repo_root or Path.cwd()
    fields, rows = _read_csv(fill_packet_path, "source manifest fill packet")
    _require_columns(fields, REQUIRED_FILL_PACKET_COLUMNS, "source manifest fill packet")

    progress_rows = [
        _progress_row(row_number=index, row=row, repo_root=repo_root)
        for index, row in enumerate(rows, start=2)
    ]
    missing_counter: Counter[str] = Counter()
    for progress in progress_rows:
        for field in progress["missing_fields"].split(";"):
            if field and field != "none":
                missing_counter[field] += 1

    grouped: dict[tuple[str, str], dict[str, int]] = defaultdict(lambda: {"rows": 0, "ready": 0})
    for progress in progress_rows:
        key = (progress["status_type"], progress["source"])
        grouped[key]["rows"] += 1
        if progress["materializable_status"] == "ready":
            grouped[key]["ready"] += 1

    summary = {
        "fill_packet_path": fill_packet_path,
        "fill_packet_rows": len(progress_rows),
        "materializable_rows": sum(1 for row in progress_rows if row["materializable_status"] == "ready"),
        "blocked_rows": sum(1 for row in progress_rows if row["materializable_status"] != "ready"),
        "raw_path_exists_rows": sum(1 for row in progress_rows if row["raw_path_exists"] == "true"),
        "missing_counts": dict(sorted(missing_counter.items())),
        "grouped_counts": dict(sorted(grouped.items())),
    }
    return progress_rows, summary


def _write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=PROGRESS_FIELDS, lineterminator="\n")
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


def _render_missing_counts(missing_counts: dict[str, int]) -> list[str]:
    if not missing_counts:
        return ["| `none` | 0 |"]
    return [f"| `{field}` | {count} |" for field, count in missing_counts.items()]


def _render_grouped_counts(grouped_counts: dict[tuple[str, str], dict[str, int]]) -> list[str]:
    if not grouped_counts:
        return ["| `none` | `none` | 0 | 0 |"]
    return [
        f"| `{status_type}` | `{source}` | {counts['rows']} | {counts['ready']} |"
        for (status_type, source), counts in grouped_counts.items()
    ]


def _render_report(summary: dict[str, Any], rows_output: Path | None) -> str:
    lines = [
        "# Point-in-Time Status Source Manifest Fill Progress",
        "",
        f"- Fill packet: {_wikilink(summary['fill_packet_path'])}",
        f"- Progress rows: {_wikilink(rows_output) if rows_output else '`not_supplied`'}",
        "- KIS/KRX API call: `false`",
        "- Order intent generated: `false`",
        "- Backtest readiness impact: `hold`",
        "- Interpretation: fill progress only, not source coverage evidence",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| Fill packet rows | {summary['fill_packet_rows']} |",
        f"| Materializable rows | {summary['materializable_rows']} |",
        f"| Blocked rows | {summary['blocked_rows']} |",
        f"| Raw path exists rows | {summary['raw_path_exists_rows']} |",
        "",
        "## Missing Field Counts",
        "",
        "| Field | Rows |",
        "| --- | ---: |",
        *_render_missing_counts(summary["missing_counts"]),
        "",
        "## Status/Source Counts",
        "",
        "| Status type | Source | Rows | Materializable |",
        "| --- | --- | ---: | ---: |",
        *_render_grouped_counts(summary["grouped_counts"]),
        "",
        "## Next Action",
        "",
        "1. Capture official raw files for blocked rows.",
        "2. Fill `source_url_to_fill`, `raw_path_to_fill`, `confidence_to_fill`, and non-pending `evidence_capture_status`.",
        "3. Run [[scripts/quant_point_in_time_status_source_manifest_materialize.py|scripts/quant_point_in_time_status_source_manifest_materialize.py]] only after `Materializable rows` equals `Fill packet rows`.",
        "",
        "## Guardrails",
        "",
        "- This progress report does not validate source coverage.",
        "- Do not pass progress rows to the coverage audit.",
        "- Keep `Backtest readiness` at `hold` until manifest validation, coverage audit, lifecycle coverage, costs, OOS, and Bias Control pass.",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Report Point-in-Time source-manifest fill progress.")
    parser.add_argument("--fill-packet", required=True, type=Path)
    parser.add_argument("--rows-output", type=Path)
    parser.add_argument("--report-output", type=Path)
    parser.add_argument("--repo-root", type=Path)
    args = parser.parse_args()

    try:
        rows, summary = summarize_fill_progress(
            fill_packet_path=args.fill_packet,
            repo_root=args.repo_root or Path.cwd(),
        )
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc

    if args.rows_output:
        _write_rows(args.rows_output, rows)
    report = _render_report(summary, args.rows_output)
    if args.report_output:
        write_text_lf(args.report_output, report)
    else:
        print(report, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
