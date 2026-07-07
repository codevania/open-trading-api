"""Validate normalized Point-in-Time status-event rows.

This script checks local CSV rows against the schema/config scaffolding. It
does not fetch KRX/KIND data and does not make the pipeline Backtest-ready.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import yaml

from quant_io import write_text_lf


DEFAULT_SCHEMA = Path("_report/quant/data/schemas/point_in_time_status_events.schema.json")
DEFAULT_SOURCE_POLICY = Path("_report/quant/data/point_in_time_status_sources.yaml")

VALIDATION_FIELDS = (
    "row_number",
    "event_date",
    "code",
    "status_type",
    "status_value",
    "source",
    "valid",
    "errors",
)


@dataclass
class ValidationResult:
    row_number: int
    row: dict[str, str]
    errors: list[str]

    @property
    def valid(self) -> bool:
        return not self.errors


def _load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("schema root must be a mapping")
    return payload


def _load_yaml(path: Path) -> dict[str, Any]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("source policy root must be a mapping")
    return payload


def _read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path.exists():
        raise ValueError(f"missing status-event CSV: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = [field.strip() for field in (reader.fieldnames or [])]
        rows = [{key.strip(): (value or "").strip() for key, value in row.items()} for row in reader]
    return fieldnames, rows


def _is_iso_date(value: str) -> bool:
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        return False
    return True


def _is_valid_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme == "https" and bool(parsed.netloc)


def _source_url_prefixes(policy: dict[str, Any], source: str) -> list[str]:
    sources = policy.get("sources", {}) or {}
    config = sources.get(source, {}) or {}
    prefixes = config.get("allowed_url_prefixes", []) or []
    return [str(prefix) for prefix in prefixes if str(prefix)]


def _validate_raw_path(value: str, raw_root: str) -> str | None:
    normalized = value.replace("\\", "/")
    root = raw_root.replace("\\", "/").rstrip("/")
    if not normalized:
        return "raw_path is required"
    if Path(value).is_absolute():
        return "raw_path must be repo-relative"
    if ".." in normalized.split("/"):
        return "raw_path must not contain parent traversal"
    if not normalized.startswith(f"{root}/"):
        return f"raw_path must be under {root}/"
    return None


def _validate_row(
    row: dict[str, str],
    schema: dict[str, Any],
    source_policy: dict[str, Any],
    required_columns: list[str],
) -> list[str]:
    nullable = set(schema.get("nullable_columns", []) or [])
    allowed = schema.get("allowed_values", {}) or {}
    status_value_by_type = schema.get("status_value_by_type", {}) or {}
    raw_root = str(source_policy.get("raw_root", "_report/raw"))
    errors: list[str] = []

    for column in required_columns:
        if column in nullable:
            continue
        if not row.get(column, ""):
            errors.append(f"{column} is required")

    event_date = row.get("event_date", "")
    if event_date and not _is_iso_date(event_date):
        errors.append("event_date must be YYYY-MM-DD")

    code = row.get("code", "")
    code_pattern = str(schema.get("code_pattern", ""))
    if code and code_pattern and not re.fullmatch(code_pattern, code):
        errors.append("code does not match KRX short-code pattern")

    for column, values in allowed.items():
        value = row.get(column, "")
        if value and value not in values:
            errors.append(f"{column} has unsupported value: {value}")

    status_type = row.get("status_type", "")
    status_value = row.get("status_value", "")
    allowed_status_values = status_value_by_type.get(status_type)
    if status_type and status_value and allowed_status_values and status_value not in allowed_status_values:
        errors.append(f"status_value {status_value} is not valid for status_type {status_type}")

    raw_path_error = _validate_raw_path(row.get("raw_path", ""), raw_root)
    if raw_path_error:
        errors.append(raw_path_error)

    source = row.get("source", "")
    source_url = row.get("source_url", "")
    if source_url:
        if not _is_valid_url(source_url):
            errors.append("source_url must be an https URL")
        prefixes = _source_url_prefixes(source_policy, source)
        if prefixes and not any(source_url.startswith(prefix) for prefix in prefixes):
            errors.append(f"source_url does not match source policy for {source}")
    elif source != "manual_snapshot":
        errors.append("source_url is required for non-manual sources")

    return errors


def _event_key(row: dict[str, str], schema: dict[str, Any]) -> tuple[str, ...]:
    columns = schema.get("event_key_columns", []) or []
    return tuple(row.get(str(column), "") for column in columns)


def validate_events(
    events_path: Path,
    schema_path: Path = DEFAULT_SCHEMA,
    source_policy_path: Path = DEFAULT_SOURCE_POLICY,
) -> tuple[list[ValidationResult], dict[str, Any]]:
    schema = _load_json(schema_path)
    source_policy = _load_yaml(source_policy_path)
    fieldnames, rows = _read_csv(events_path)
    required_columns = [str(column) for column in schema.get("required_columns", []) or []]
    missing_columns = [column for column in required_columns if column not in fieldnames]

    results: list[ValidationResult] = []
    if missing_columns:
        results.append(
            ValidationResult(
                0,
                {},
                [f"missing required columns: {', '.join(missing_columns)}"],
            )
        )
    else:
        for index, row in enumerate(rows, start=1):
            results.append(ValidationResult(index, row, _validate_row(row, schema, source_policy, required_columns)))

        key_counts = Counter(_event_key(row, schema) for row in rows)
        duplicate_keys = {key for key, count in key_counts.items() if key and count > 1}
        if duplicate_keys:
            for result in results:
                if _event_key(result.row, schema) in duplicate_keys:
                    result.errors.append("duplicate event key")

    by_status_type: dict[str, int] = defaultdict(int)
    by_source: dict[str, int] = defaultdict(int)
    for row in rows:
        if row.get("status_type"):
            by_status_type[row["status_type"]] += 1
        if row.get("source"):
            by_source[row["source"]] += 1

    invalid_rows = sum(1 for result in results if not result.valid)
    summary = {
        "events_path": events_path,
        "schema_path": schema_path,
        "source_policy_path": source_policy_path,
        "input_rows": len(rows),
        "valid_rows": len(rows) - invalid_rows if not missing_columns else 0,
        "invalid_rows": invalid_rows,
        "missing_columns": missing_columns,
        "duplicate_event_keys": sum(1 for result in results if "duplicate event key" in result.errors),
        "by_status_type": dict(sorted(by_status_type.items())),
        "by_source": dict(sorted(by_source.items())),
    }
    return results, summary


def _write_validation_rows(path: Path, results: list[ValidationResult]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=VALIDATION_FIELDS, lineterminator="\n")
        writer.writeheader()
        for result in results:
            row = result.row
            writer.writerow(
                {
                    "row_number": result.row_number,
                    "event_date": row.get("event_date", ""),
                    "code": row.get("code", ""),
                    "status_type": row.get("status_type", ""),
                    "status_value": row.get("status_value", ""),
                    "source": row.get("source", ""),
                    "valid": str(result.valid).lower(),
                    "errors": ";".join(result.errors),
                }
            )


def _wikilink(path: Path) -> str:
    rendered = path.as_posix()
    return f"[[{rendered}|{rendered}]]"


def _render_report(summary: dict[str, Any], rows_output: Path | None) -> str:
    lines = [
        "# Point-in-Time Status Events Validation",
        "",
        f"- Events: {_wikilink(summary['events_path'])}",
        f"- Schema: {_wikilink(summary['schema_path'])}",
        f"- Source policy: {_wikilink(summary['source_policy_path'])}",
        "- Interpretation: schema validation only, not a `Point-in-Time Universe` or `Backtest` result",
        "- Backtest readiness: `hold`",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| Input rows | {summary['input_rows']} |",
        f"| Valid rows | {summary['valid_rows']} |",
        f"| Invalid rows | {summary['invalid_rows']} |",
        f"| Duplicate event keys | {summary['duplicate_event_keys']} |",
        "",
    ]
    if summary["missing_columns"]:
        lines.extend(["## Missing Columns", "", f"- `{', '.join(summary['missing_columns'])}`", ""])
    if rows_output is not None:
        lines.extend(["## Row Output", "", f"- {_wikilink(rows_output)}", ""])

    lines.extend(["## Status Type Counts", "", "| Status Type | Rows |", "| --- | ---: |"])
    for status_type, count in summary["by_status_type"].items():
        lines.append(f"| `{status_type}` | {count} |")
    if not summary["by_status_type"]:
        lines.append("| `none` | 0 |")

    lines.extend(["", "## Source Counts", "", "| Source | Rows |", "| --- | ---: |"])
    for source, count in summary["by_source"].items():
        lines.append(f"| `{source}` | {count} |")
    if not summary["by_source"]:
        lines.append("| `none` | 0 |")

    lines.extend(
        [
            "",
            "## Guardrails",
            "",
            "- Passing validation means normalized status-event rows match local schema/config only.",
            "- It does not prove raw KRX/KIND collection coverage.",
            "- Raw evidence must remain under `_report/raw/**` and stay out of commits.",
            "- `Backtest` readiness remains `hold` until historical status replay is validated for the selected test scope.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate normalized Point-in-Time status-event rows.")
    parser.add_argument("--events", required=True, type=Path)
    parser.add_argument("--schema", default=DEFAULT_SCHEMA, type=Path)
    parser.add_argument("--source-policy", default=DEFAULT_SOURCE_POLICY, type=Path)
    parser.add_argument("--rows-output", type=Path)
    parser.add_argument("--report-output", type=Path)
    args = parser.parse_args()

    try:
        results, summary = validate_events(args.events, args.schema, args.source_policy)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc

    if args.rows_output:
        _write_validation_rows(args.rows_output, results)
    report = _render_report(summary, args.rows_output)
    if args.report_output:
        write_text_lf(args.report_output, report)
    else:
        print(report, end="")
    return 0 if summary["invalid_rows"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
