"""Draft Point-in-Time status source coverage manifest collection rows.

This is a local planning helper. It does not fetch KRX/KIND data, does not
claim source coverage, and intentionally leaves evidence fields blank until
raw official files are captured.
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml

from quant_io import write_text_lf


DEFAULT_SOURCE_POLICY_PATH = Path("_report/quant/data/point_in_time_status_sources.yaml")
DEFAULT_REQUIRED_STATUS_TYPES = ("managed_issue", "trading_halt", "market_alert", "delisting")
REQUIRED_LIFECYCLE_COLUMNS = {
    "code",
    "market",
    "status_type",
    "lifecycle_gap_status",
    "market_start",
    "market_end",
}
OUTPUT_FIELDS = (
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
)
STATUS_TYPE_TERMS = {
    "managed_issue": ("managed", "designated"),
    "trading_halt": ("trading halt", "trading suspension", "resumption", "resume"),
    "market_alert": ("market alert", "alert"),
    "delisting": ("delisting",),
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


def _iso_date(value: str, field_name: str) -> str:
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError as exc:
        raise ValueError(f"{field_name} must be YYYY-MM-DD: {value}") from exc
    return value


def _split_required_status_types(value: str) -> tuple[str, ...]:
    parsed = tuple(dict.fromkeys(token.strip() for token in value.split(",") if token.strip()))
    if not parsed:
        raise ValueError("at least one required status type is required")
    return parsed


def _read_policy(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise ValueError(f"source policy not found: {path}")
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("source policy root must be a mapping")
    sources = payload.get("sources")
    if not isinstance(sources, dict) or not sources:
        raise ValueError("source policy must contain a non-empty sources mapping")
    return payload


def _split_semicolon(value: str) -> list[str]:
    return [item.strip() for item in str(value or "").split(";") if item.strip()]


def _source_haystack(source: str, source_policy: dict[str, Any]) -> str:
    parts: list[str] = [source]
    for key in ("display_name", "source_kind"):
        value = source_policy.get(key)
        if value:
            parts.append(str(value))
    for key in ("candidate_tables", "notes"):
        values = source_policy.get(key, []) or []
        if isinstance(values, list):
            parts.extend(str(value) for value in values)
    return " ".join(parts).lower()


def _candidate_sources(policy: dict[str, Any], status_type: str) -> list[str]:
    sources: dict[str, Any] = policy["sources"]
    terms = STATUS_TYPE_TERMS.get(status_type, (status_type.replace("_", " "),))
    candidates: list[str] = []
    fallback: list[str] = []
    for source, source_policy in sources.items():
        if not isinstance(source_policy, dict):
            continue
        if source == "manual_snapshot":
            fallback.append(source)
            continue
        haystack = _source_haystack(source, source_policy)
        if any(term in haystack for term in terms):
            candidates.append(source)
    candidates.extend(source for source in fallback if source not in candidates)
    return candidates or list(sources)


def _coverage_window(
    rows: list[dict[str, str]],
    market_start: str | None,
    market_end: str | None,
) -> tuple[str, str]:
    starts = [_iso_date(row["market_start"], "market_start") for row in rows if row.get("market_start")]
    ends = [_iso_date(row["market_end"], "market_end") for row in rows if row.get("market_end")]
    start = _iso_date(market_start, "market_start") if market_start is not None else (min(starts) if starts else "")
    end = _iso_date(market_end, "market_end") if market_end is not None else (max(ends) if ends else "")
    if not start or not end:
        raise ValueError("provide --market-start and --market-end when lifecycle rows do not contain a market window")
    if start > end:
        raise ValueError("market_start must be on or before market_end")
    return start, end


def _source_policy_list(source_policy: dict[str, Any], key: str) -> str:
    values = source_policy.get(key, []) or []
    if not isinstance(values, list):
        return ""
    return ";".join(str(value) for value in values if str(value))


def _target_rows_for_type(rows: list[dict[str, str]], status_type: str) -> list[dict[str, str]]:
    return [
        row
        for row in rows
        if row.get("status_type", "") == status_type
        and row.get("lifecycle_gap_status", "") == "missing_release_resume_evidence"
    ]


def build_source_manifest_draft(
    *,
    lifecycle_gaps_path: Path,
    policy_path: Path = DEFAULT_SOURCE_POLICY_PATH,
    market_start: str | None = None,
    market_end: str | None = None,
    required_status_types: tuple[str, ...] = DEFAULT_REQUIRED_STATUS_TYPES,
) -> tuple[list[dict[str, str]], dict[str, Any]]:
    fields, lifecycle_rows = _read_csv(lifecycle_gaps_path, "lifecycle gaps")
    _require_columns(fields, REQUIRED_LIFECYCLE_COLUMNS, "lifecycle gaps")
    policy = _read_policy(policy_path)
    coverage_start, coverage_end = _coverage_window(lifecycle_rows, market_start, market_end)
    sources: dict[str, Any] = policy["sources"]

    draft_rows: list[dict[str, str]] = []
    target_counts: dict[str, int] = {}
    target_code_counts: dict[str, int] = {}
    for status_type in required_status_types:
        target_rows = _target_rows_for_type(lifecycle_rows, status_type)
        target_codes = sorted({row["code"] for row in target_rows if row.get("code")})
        markets = sorted(
            {
                market
                for row in target_rows
                for market in _split_semicolon(row.get("market", ""))
                if market and market != "UNKNOWN"
            }
        )
        target_counts[status_type] = len(target_rows)
        target_code_counts[status_type] = len(target_codes)
        notes = [
            "draft_only",
            "fill_source_url_raw_path_confidence_before_validation",
        ]
        if target_rows:
            notes.append("lifecycle_release_resume_collection_targets_present")
        else:
            notes.append("required_manifest_coverage_no_lifecycle_gap_rows")

        for source in _candidate_sources(policy, status_type):
            source_policy = sources.get(source, {})
            if not isinstance(source_policy, dict):
                source_policy = {}
            draft_rows.append(
                {
                    "status_type": status_type,
                    "coverage_start": coverage_start,
                    "coverage_end": coverage_end,
                    "source": source,
                    "source_url": "",
                    "raw_path": "",
                    "confidence": "",
                    "lifecycle_target_groups": str(len(target_rows)),
                    "lifecycle_target_codes": str(len(target_codes)),
                    "market_labels": ";".join(markets),
                    "candidate_tables": _source_policy_list(source_policy, "candidate_tables"),
                    "allowed_url_prefixes": _source_policy_list(source_policy, "allowed_url_prefixes"),
                    "draft_status": "pending_raw_evidence",
                    "notes": ";".join(notes),
                }
            )

    source_counts = Counter(row["source"] for row in draft_rows)
    summary = {
        "lifecycle_gaps_path": lifecycle_gaps_path,
        "policy_path": policy_path,
        "required_status_types": list(required_status_types),
        "coverage_start": coverage_start,
        "coverage_end": coverage_end,
        "lifecycle_gap_rows": len(lifecycle_rows),
        "draft_rows": len(draft_rows),
        "target_counts": target_counts,
        "target_code_counts": target_code_counts,
        "source_counts": dict(sorted(source_counts.items())),
    }
    return draft_rows, summary


def _write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _wikilink(path: Path) -> str:
    rendered = path.as_posix()
    return f"[[{rendered}|{rendered}]]"


def _render_target_counts(summary: dict[str, Any]) -> list[str]:
    lines: list[str] = []
    for status_type in summary["required_status_types"]:
        lines.append(
            f"| `{status_type}` | {summary['target_counts'].get(status_type, 0)} | "
            f"{summary['target_code_counts'].get(status_type, 0)} |"
        )
    return lines


def _render_source_counts(source_counts: dict[str, int]) -> list[str]:
    if not source_counts:
        return ["| `none` | 0 |"]
    return [f"| `{source}` | {count} |" for source, count in source_counts.items()]


def _render_report(summary: dict[str, Any], output_path: Path) -> str:
    lines = [
        "# Point-in-Time Status Source Manifest Draft",
        "",
        f"- Lifecycle gaps: {_wikilink(summary['lifecycle_gaps_path'])}",
        f"- Source policy: {_wikilink(summary['policy_path'])}",
        f"- Output: {_wikilink(output_path)}",
        f"- Coverage window: `{summary['coverage_start']}..{summary['coverage_end']}`",
        f"- Required status types: `{','.join(summary['required_status_types'])}`",
        "- Draft status: `pending_raw_evidence`",
        "- KIS/KRX API call: `false`",
        "- Order intent generated: `false`",
        "- Backtest readiness impact: `hold`",
        "- Interpretation: collection planning only, not source coverage evidence",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| Lifecycle gap rows | {summary['lifecycle_gap_rows']} |",
        f"| Draft manifest rows | {summary['draft_rows']} |",
        "",
        "## Lifecycle Targets By Status Type",
        "",
        "| Status type | Target groups | Target codes |",
        "| --- | ---: | ---: |",
        *_render_target_counts(summary),
        "",
        "## Candidate Sources",
        "",
        "| Source | Draft rows |",
        "| --- | ---: |",
        *_render_source_counts(summary["source_counts"]),
        "",
        "## Guardrails",
        "",
        "- `source_url`, `raw_path`, and `confidence` are intentionally blank in the draft.",
        "- Do not pass this draft as source evidence until official raw files are saved and those fields are filled.",
        "- A valid source manifest still does not promote `Backtest readiness`; normalized status events, replay, costs, OOS, and Bias Control must also pass.",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Draft Point-in-Time status source coverage manifest rows.")
    parser.add_argument("--lifecycle-gaps", required=True, type=Path)
    parser.add_argument("--policy", default=DEFAULT_SOURCE_POLICY_PATH, type=Path)
    parser.add_argument("--market-start")
    parser.add_argument("--market-end")
    parser.add_argument("--required-status-types", default=",".join(DEFAULT_REQUIRED_STATUS_TYPES))
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--report-output", type=Path)
    args = parser.parse_args()

    try:
        rows, summary = build_source_manifest_draft(
            lifecycle_gaps_path=args.lifecycle_gaps,
            policy_path=args.policy,
            market_start=args.market_start,
            market_end=args.market_end,
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
