"""Materialize a filled source-manifest packet into a coverage manifest.

This helper is the bridge after official raw KRX/KIND evidence has been
captured. It requires filled source URL, raw path, confidence, and a non-pending
capture status. It does not fetch data, validate raw files, promote Backtest
readiness, or create order intents.
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
    "evidence_capture_status",
    "source_url_to_fill",
    "raw_path_to_fill",
    "confidence_to_fill",
    "order_intent_generated",
    "manifest_notes",
    "queue_notes",
}
MANIFEST_FIELDS = (
    "status_type",
    "coverage_start",
    "coverage_end",
    "source",
    "source_url",
    "raw_path",
    "confidence",
    "notes",
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


def _row_failures(row_number: int, row: dict[str, str]) -> list[str]:
    failures: list[str] = []
    if row.get("order_intent_generated") != "false":
        failures.append("order_intent_generated must be false")
    if not row.get("source_url_to_fill", ""):
        failures.append("source_url_to_fill is empty")
    if not row.get("raw_path_to_fill", ""):
        failures.append("raw_path_to_fill is empty")
    confidence = row.get("confidence_to_fill", "")
    if confidence not in VALID_CONFIDENCE:
        failures.append("confidence_to_fill must be high, medium, or low")
    capture_status = row.get("evidence_capture_status", "")
    if not capture_status:
        failures.append("evidence_capture_status is empty")
    elif capture_status.startswith("pending"):
        failures.append("evidence_capture_status is still pending")
    if not row.get("status_type", ""):
        failures.append("status_type is empty")
    if not row.get("source", ""):
        failures.append("source is empty")
    if not row.get("coverage_start", ""):
        failures.append("coverage_start is empty")
    if not row.get("coverage_end", ""):
        failures.append("coverage_end is empty")
    return [f"row {row_number}: {failure}" for failure in failures]


def _notes(row: dict[str, str]) -> str:
    parts = [
        f"batch_id={row.get('batch_id', '')}",
        f"evidence_capture_status={row.get('evidence_capture_status', '')}",
        row.get("manifest_notes", ""),
        row.get("queue_notes", ""),
    ]
    return ";".join(dict.fromkeys(part for part in parts if part))


def materialize_source_manifest(
    *,
    fill_packet_path: Path,
) -> tuple[list[dict[str, str]], dict[str, Any]]:
    fields, rows = _read_csv(fill_packet_path, "source manifest fill packet")
    _require_columns(fields, REQUIRED_FILL_PACKET_COLUMNS, "source manifest fill packet")

    failures: list[str] = []
    for row_number, row in enumerate(rows, start=2):
        failures.extend(_row_failures(row_number, row))
    if failures:
        raise ValueError("source manifest fill packet is not materializable: " + "; ".join(failures))

    manifest_rows = [
        {
            "status_type": row["status_type"],
            "coverage_start": row["coverage_start"],
            "coverage_end": row["coverage_end"],
            "source": row["source"],
            "source_url": row["source_url_to_fill"],
            "raw_path": _normalize_path(row["raw_path_to_fill"]),
            "confidence": row["confidence_to_fill"],
            "notes": _notes(row),
        }
        for row in rows
    ]
    status_counts = Counter(row["status_type"] for row in manifest_rows)
    source_counts = Counter(row["source"] for row in manifest_rows)
    coverage_windows = sorted(
        {
            f"{row['coverage_start']}..{row['coverage_end']}"
            for row in manifest_rows
            if row.get("coverage_start") and row.get("coverage_end")
        }
    )
    summary = {
        "fill_packet_path": fill_packet_path,
        "manifest_rows": len(manifest_rows),
        "coverage_windows": coverage_windows,
        "status_counts": dict(sorted(status_counts.items())),
        "source_counts": dict(sorted(source_counts.items())),
    }
    return manifest_rows, summary


def _write_manifest(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=MANIFEST_FIELDS, lineterminator="\n")
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
    lines = [
        "# Point-in-Time Status Source Manifest Materialize",
        "",
        f"- Fill packet: {_wikilink(summary['fill_packet_path'])}",
        f"- Manifest output: {_wikilink(output_path)}",
        f"- Coverage windows: `{','.join(summary['coverage_windows']) or 'unknown'}`",
        "- KIS/KRX API call: `false`",
        "- Order intent generated: `false`",
        "- Backtest readiness impact: `hold`",
        "- Interpretation: manifest materialization only, not source coverage validation",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| Manifest rows | {summary['manifest_rows']} |",
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
        "## Next Validation",
        "",
        "1. Run `scripts/quant_point_in_time_status_source_manifest_validate.py` on the manifest output.",
        "2. Re-run the status coverage audit with the validated manifest only after row validation passes.",
        "",
        "## Guardrails",
        "",
        "- This materializer refuses blank or pending fill-packet rows.",
        "- This materializer does not check that raw files exist or that coverage is complete.",
        "- Keep `Backtest readiness` at `hold` until manifest validation, coverage audit, lifecycle coverage, costs, OOS, and Bias Control pass.",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Materialize a filled Point-in-Time source manifest packet.")
    parser.add_argument("--fill-packet", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--report-output", type=Path)
    args = parser.parse_args()

    try:
        rows, summary = materialize_source_manifest(fill_packet_path=args.fill_packet)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc

    _write_manifest(args.output, rows)
    report = _render_report(summary, args.output)
    if args.report_output:
        write_text_lf(args.report_output, report)
    else:
        print(report, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
