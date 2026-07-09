"""Build a batch queue from Point-in-Time status evidence plan rows.

This helper is local planning only. It does not fetch KRX/KIND data, does not
validate official source coverage, does not promote Backtest readiness, and
never creates order intents.
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from quant_io import write_text_lf


REQUIRED_PLAN_COLUMNS = {
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
}
OUTPUT_FIELDS = (
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
)


def _read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path.exists():
        raise ValueError(f"evidence plan CSV not found: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = list(reader.fieldnames or [])
        rows = [{key: (value or "").strip() for key, value in row.items()} for row in reader]
    if not rows:
        raise ValueError(f"evidence plan CSV has no rows: {path}")
    return fields, rows


def _require_columns(fields: list[str]) -> None:
    missing = REQUIRED_PLAN_COLUMNS - set(fields)
    if missing:
        raise ValueError(f"evidence plan CSV missing required columns: {', '.join(sorted(missing))}")


def _int_value(value: str) -> int:
    try:
        return int(float(str(value or "0").strip()))
    except ValueError:
        return 0


def _join_unique(values: list[str], *, default: str = "") -> str:
    rendered = ";".join(dict.fromkeys(value for value in values if value))
    return rendered or default


def _market_scope(row: dict[str, str]) -> str:
    market = row.get("market", "").strip()
    if market:
        return market
    if row.get("blocker_type") == "source_manifest_evidence":
        return "required_manifest_scope"
    if row.get("unknown_market_target") == "true":
        return "UNKNOWN"
    return "blank"


def _group_key(row: dict[str, str]) -> tuple[str, ...]:
    base = (
        row["priority"],
        row["blocker_type"],
        row["status_type"],
        row["suggested_source"],
        row["manifest_source"],
        row["collection_status"],
        row["required_evidence"],
    )
    if row["blocker_type"] == "source_manifest_evidence":
        return (*base, "source_manifest_scope")
    return (*base, _market_scope(row))


def _chunks(rows: list[dict[str, str]], batch_size: int) -> list[list[dict[str, str]]]:
    return [rows[index : index + batch_size] for index in range(0, len(rows), batch_size)]


def _source_plan_row(row: dict[str, str]) -> str:
    return str(row.get("_source_plan_row", ""))


def _build_batch_row(batch_id: str, rows: list[dict[str, str]]) -> dict[str, str]:
    first = rows[0]
    codes = [row.get("code", "") for row in rows if row.get("code", "")]
    source_plan_rows = [_source_plan_row(row) for row in rows]
    notes = [row.get("notes", "") for row in rows]
    notes.append("plan_only_not_source_coverage")
    return {
        "batch_id": batch_id,
        "priority": first["priority"],
        "blocker_type": first["blocker_type"],
        "status_type": first["status_type"],
        "suggested_source": first["suggested_source"],
        "manifest_source": first["manifest_source"],
        "collection_status": first["collection_status"],
        "market_scope": _join_unique([_market_scope(row) for row in rows], default="blank"),
        "row_count": str(len(rows)),
        "code_count": str(len(dict.fromkeys(codes))),
        "code_sample": _join_unique(codes[:5], default="not_applicable"),
        "required_evidence": first["required_evidence"],
        "source_plan_rows": _join_unique(source_plan_rows),
        "order_intent_generated": "false",
        "notes": _join_unique(notes),
    }


def build_evidence_collection_queue(
    *,
    evidence_plan_path: Path,
    batch_size: int = 25,
) -> tuple[list[dict[str, str]], dict[str, Any]]:
    if batch_size < 1:
        raise ValueError("batch_size must be >= 1")

    fields, plan_rows = _read_csv(evidence_plan_path)
    _require_columns(fields)
    for index, row in enumerate(plan_rows, start=1):
        row["_source_plan_row"] = str(index)

    grouped: dict[tuple[str, ...], list[dict[str, str]]] = defaultdict(list)
    for row in plan_rows:
        if row.get("order_intent_generated") != "false":
            raise ValueError("evidence plan contains order_intent_generated rows that are not false")
        grouped[_group_key(row)].append(row)

    batch_rows: list[dict[str, str]] = []
    priority_sequence: Counter[str] = Counter()
    for key in sorted(grouped, key=lambda item: (_int_value(item[0]), item[1], item[2], item[3], item[-1])):
        group_rows = sorted(
            grouped[key],
            key=lambda row: (_int_value(_source_plan_row(row)), row.get("code", ""), row.get("notes", "")),
        )
        for chunk in _chunks(group_rows, batch_size):
            priority = chunk[0]["priority"]
            priority_sequence[priority] += 1
            batch_id = f"P{priority}-{priority_sequence[priority]:03d}"
            batch_rows.append(_build_batch_row(batch_id, chunk))

    priority_counts = Counter(row["priority"] for row in batch_rows)
    blocker_counts = Counter(row["blocker_type"] for row in batch_rows)
    status_type_counts = Counter(row["status_type"] for row in batch_rows)
    source_counts = Counter(row["suggested_source"] for row in batch_rows)
    collection_status_counts = Counter(row["collection_status"] for row in batch_rows)
    input_code_count = len({row.get("code", "") for row in plan_rows if row.get("code", "")})
    summary = {
        "evidence_plan_path": evidence_plan_path,
        "batch_size": batch_size,
        "input_rows": len(plan_rows),
        "input_code_count": input_code_count,
        "queue_batches": len(batch_rows),
        "queued_rows": sum(int(row["row_count"]) for row in batch_rows),
        "priority_counts": dict(sorted(priority_counts.items())),
        "blocker_counts": dict(sorted(blocker_counts.items())),
        "status_type_counts": dict(sorted(status_type_counts.items())),
        "source_counts": dict(sorted(source_counts.items())),
        "collection_status_counts": dict(sorted(collection_status_counts.items())),
    }
    return batch_rows, summary


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
    lines = [
        "# Point-in-Time Status Evidence Collection Queue",
        "",
        f"- Evidence plan: {_wikilink(summary['evidence_plan_path'])}",
        f"- Queue rows: {_wikilink(output_path)}",
        f"- Batch size: `{summary['batch_size']}`",
        "- KIS/KRX API call: `false`",
        "- Order intent generated: `false`",
        "- Backtest readiness impact: `hold`",
        "- Interpretation: execution queue only, not source coverage evidence",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| Evidence plan rows | {summary['input_rows']} |",
        f"| Unique codes in plan | {summary['input_code_count']} |",
        f"| Queue batches | {summary['queue_batches']} |",
        f"| Queued source rows | {summary['queued_rows']} |",
        "",
        "## Priority Batch Counts",
        "",
        "| Priority | Batches |",
        "| --- | ---: |",
        *_render_counter(summary["priority_counts"]),
        "",
        "## Blocker Batch Counts",
        "",
        "| Blocker | Batches |",
        "| --- | ---: |",
        *_render_counter(summary["blocker_counts"]),
        "",
        "## Status Type Batch Counts",
        "",
        "| Status type | Batches |",
        "| --- | ---: |",
        *_render_counter(summary["status_type_counts"]),
        "",
        "## Suggested Source Batch Counts",
        "",
        "| Suggested source | Batches |",
        "| --- | ---: |",
        *_render_counter(summary["source_counts"]),
        "",
        "## Collection Status Batch Counts",
        "",
        "| Collection status | Batches |",
        "| --- | ---: |",
        *_render_counter(summary["collection_status_counts"]),
        "",
        "## Execution Order",
        "",
        "1. Execute `P1-*` source manifest batches first and fill official `source_url`, `raw_path`, and `confidence` evidence.",
        "2. Execute `P2-*` release/resume batches only after the matching source manifest evidence is filled.",
        "3. Execute `P3-*` UNKNOWN market label batches with official evidence or deterministic local joins only.",
        "",
        "## Guardrails",
        "",
        "- This queue is derived from the plan and is not a filled source coverage manifest.",
        "- Do not pass queue rows to the coverage audit as evidence.",
        "- Keep `Backtest readiness` at `hold` until filled manifest validation, lifecycle coverage, costs, OOS, and Bias Control pass.",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a Point-in-Time status evidence collection batch queue.")
    parser.add_argument("--evidence-plan", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--report-output", type=Path)
    parser.add_argument("--batch-size", type=int, default=25)
    args = parser.parse_args()

    try:
        rows, summary = build_evidence_collection_queue(
            evidence_plan_path=args.evidence_plan,
            batch_size=args.batch_size,
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
