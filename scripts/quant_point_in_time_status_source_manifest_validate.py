"""Validate Point-in-Time status source coverage manifests.

This validates local manifest evidence only. It does not fetch KRX/KIND data,
does not normalize status events, and does not promote any Backtest gate.
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml

from quant_io import write_text_lf


DEFAULT_POLICY_PATH = Path("_report/quant/data/point_in_time_status_sources.yaml")
DEFAULT_REQUIRED_STATUS_TYPES = ("managed_issue", "trading_halt", "market_alert", "delisting")
REQUIRED_FIELDS = {
    "status_type",
    "coverage_start",
    "coverage_end",
    "source",
    "source_url",
    "raw_path",
    "confidence",
    "notes",
}
VALID_CONFIDENCE = {"high", "medium", "low"}
CHECK_FIELDS = (
    "row_number",
    "status_type",
    "coverage_start",
    "coverage_end",
    "source",
    "source_url",
    "raw_path",
    "status",
    "message",
)


@dataclass
class ManifestRowCheck:
    row_number: int
    status_type: str
    coverage_start: str
    coverage_end: str
    source: str
    source_url: str
    raw_path: str
    status: str
    message: str


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


def _market_window_from_rows(rows: list[dict[str, str]]) -> tuple[str, str]:
    dates = [_iso_date(row.get("date", ""), "date") for row in rows]
    return min(dates), max(dates)


def _resolve_market_window(
    *,
    market_data_path: Path | None,
    market_start: str | None,
    market_end: str | None,
) -> tuple[str, str]:
    if market_data_path is not None:
        fields, rows = _read_csv(market_data_path, "market-data")
        _require_columns(fields, {"date"}, "market-data")
        inferred_start, inferred_end = _market_window_from_rows(rows)
        if market_start is not None and _iso_date(market_start, "market_start") != inferred_start:
            raise ValueError("market_start does not match market-data window")
        if market_end is not None and _iso_date(market_end, "market_end") != inferred_end:
            raise ValueError("market_end does not match market-data window")
        return inferred_start, inferred_end
    if market_start is None or market_end is None:
        raise ValueError("provide --market-data or both --market-start and --market-end")
    start = _iso_date(market_start, "market_start")
    end = _iso_date(market_end, "market_end")
    if start > end:
        raise ValueError("market_start must be on or before market_end")
    return start, end


def _source_url_allowed(source_url: str, allowed_prefixes: list[str]) -> bool:
    return any(source_url.startswith(prefix) for prefix in allowed_prefixes)


def _check_row(
    *,
    row_number: int,
    row: dict[str, str],
    policy: dict[str, Any],
    repo_root: Path,
    required_status_types: tuple[str, ...],
) -> ManifestRowCheck:
    status_type = row.get("status_type", "")
    coverage_start = row.get("coverage_start", "")
    coverage_end = row.get("coverage_end", "")
    source = row.get("source", "")
    source_url = row.get("source_url", "")
    raw_path = row.get("raw_path", "").replace("\\", "/")
    messages: list[str] = []
    scope_note = ""

    if status_type not in required_status_types:
        scope_note = "status_type is outside required coverage scope"
    try:
        start = _iso_date(coverage_start, f"row {row_number} coverage_start")
        end = _iso_date(coverage_end, f"row {row_number} coverage_end")
        if start > end:
            messages.append("coverage_start is after coverage_end")
    except ValueError as exc:
        messages.append(str(exc))

    sources = policy["sources"]
    source_policy = sources.get(source)
    if not isinstance(source_policy, dict):
        messages.append("source is not listed in source policy")
        allowed_prefixes: list[str] = []
    else:
        allowed_prefixes = [str(prefix) for prefix in source_policy.get("allowed_url_prefixes", []) or []]

    if not source_url:
        messages.append("source_url is empty")
    elif allowed_prefixes and not _source_url_allowed(source_url, allowed_prefixes):
        messages.append("source_url does not match allowed source prefixes")

    if not raw_path:
        messages.append("raw_path is empty")
    elif not raw_path.startswith("_report/raw/"):
        messages.append("raw_path must be under _report/raw/")
    elif not (repo_root / raw_path).exists():
        messages.append("raw_path does not exist")

    confidence = row.get("confidence", "")
    if confidence not in VALID_CONFIDENCE:
        messages.append("confidence must be high, medium, or low")

    status = "pass" if not messages else "fail"
    return ManifestRowCheck(
        row_number=row_number,
        status_type=status_type,
        coverage_start=coverage_start,
        coverage_end=coverage_end,
        source=source,
        source_url=source_url,
        raw_path=raw_path,
        status=status,
        message="; ".join(messages) if messages else scope_note or "ok",
    )


def _missing_coverage_types(
    rows: list[dict[str, str]],
    required_status_types: tuple[str, ...],
    market_start: str,
    market_end: str,
) -> list[str]:
    covered: set[str] = set()
    for row in rows:
        status_type = row.get("status_type", "")
        if status_type not in required_status_types:
            continue
        if row.get("coverage_start", "") <= market_start and row.get("coverage_end", "") >= market_end:
            covered.add(status_type)
    return sorted(set(required_status_types) - covered)


def validate_manifest(
    *,
    manifest_path: Path,
    policy_path: Path,
    market_data_path: Path | None = None,
    market_start: str | None = None,
    market_end: str | None = None,
    required_status_types: tuple[str, ...] = DEFAULT_REQUIRED_STATUS_TYPES,
    repo_root: Path | None = None,
) -> tuple[list[ManifestRowCheck], dict[str, Any]]:
    repo_root = repo_root or Path.cwd()
    fields, rows = _read_csv(manifest_path, "source coverage manifest")
    _require_columns(fields, REQUIRED_FIELDS, "source coverage manifest")
    policy = _read_policy(policy_path)
    resolved_start, resolved_end = _resolve_market_window(
        market_data_path=market_data_path,
        market_start=market_start,
        market_end=market_end,
    )

    checks = [
        _check_row(
            row_number=index,
            row=row,
            policy=policy,
            repo_root=repo_root,
            required_status_types=required_status_types,
        )
        for index, row in enumerate(rows, start=2)
    ]
    row_failures = sum(1 for check in checks if check.status != "pass")
    missing_types = _missing_coverage_types(rows, required_status_types, resolved_start, resolved_end)
    overall_status = "pass" if row_failures == 0 and not missing_types else "fail"
    summary = {
        "manifest_path": manifest_path,
        "policy_path": policy_path,
        "market_data_path": market_data_path,
        "market_start": resolved_start,
        "market_end": resolved_end,
        "required_status_types": required_status_types,
        "manifest_rows": len(rows),
        "row_failures": row_failures,
        "missing_coverage_status_types": missing_types,
        "overall_status": overall_status,
    }
    return checks, summary


def _wikilink(path: Path | None) -> str:
    if path is None:
        return "`not_supplied`"
    rendered = path.as_posix()
    return f"[[{rendered}|{rendered}]]"


def _write_check_rows(path: Path, checks: list[ManifestRowCheck]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CHECK_FIELDS, lineterminator="\n")
        writer.writeheader()
        for check in checks:
            writer.writerow(
                {
                    "row_number": check.row_number,
                    "status_type": check.status_type,
                    "coverage_start": check.coverage_start,
                    "coverage_end": check.coverage_end,
                    "source": check.source,
                    "source_url": check.source_url,
                    "raw_path": check.raw_path,
                    "status": check.status,
                    "message": check.message,
                }
            )


def _render_report(checks: list[ManifestRowCheck], summary: dict[str, Any], rows_output: Path | None) -> str:
    lines = [
        "# Point-in-Time Status Source Coverage Manifest Validate",
        "",
        f"- Manifest: {_wikilink(summary['manifest_path'])}",
        f"- Source policy: {_wikilink(summary['policy_path'])}",
        f"- Market-data input: {_wikilink(summary['market_data_path'])}",
        f"- Market window: `{summary['market_start']}..{summary['market_end']}`",
        f"- Required status types: `{','.join(summary['required_status_types'])}`",
        f"- Overall status: `{summary['overall_status']}`",
        "- KIS/KRX API call: `false`",
        "- Order intent generated: `false`",
        "- Interpretation: source manifest validation only, not a `Backtest` result",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| Manifest rows | {summary['manifest_rows']} |",
        f"| Row failures | {summary['row_failures']} |",
        f"| Missing coverage status types | `{','.join(summary['missing_coverage_status_types']) or 'none'}` |",
        "",
    ]
    if rows_output is not None:
        lines.extend(["## Row Output", "", f"- {_wikilink(rows_output)}", ""])

    lines.extend(
        [
            "## Row Checks",
            "",
            "| Row | Status type | Coverage | Source | Raw path | Status | Message |",
            "| ---: | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for check in checks:
        lines.append(
            f"| {check.row_number} | `{check.status_type}` | "
            f"`{check.coverage_start}..{check.coverage_end}` | `{check.source}` | "
            f"`{check.raw_path}` | `{check.status}` | {check.message} |"
        )
    lines.extend(
        [
            "",
            "## Guardrails",
            "",
            "- This validator does not prove that normalized status-event rows are complete.",
            "- A passing manifest only proves the source coverage rows are locally usable by the coverage audit gate.",
            "- Keep `Backtest readiness` at `hold` until status events, replay, costs, OOS, and Bias Control pass.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a Point-in-Time status source coverage manifest.")
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--policy", default=DEFAULT_POLICY_PATH, type=Path)
    parser.add_argument("--market-data", type=Path)
    parser.add_argument("--market-start")
    parser.add_argument("--market-end")
    parser.add_argument("--required-status-types", default=",".join(DEFAULT_REQUIRED_STATUS_TYPES))
    parser.add_argument("--repo-root", type=Path)
    parser.add_argument("--rows-output", type=Path)
    parser.add_argument("--report-output", type=Path)
    args = parser.parse_args()

    try:
        checks, summary = validate_manifest(
            manifest_path=args.manifest,
            policy_path=args.policy,
            market_data_path=args.market_data,
            market_start=args.market_start,
            market_end=args.market_end,
            required_status_types=_split_required_status_types(args.required_status_types),
            repo_root=args.repo_root or Path.cwd(),
        )
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc

    if args.rows_output:
        _write_check_rows(args.rows_output, checks)
    report = _render_report(checks, summary, args.rows_output)
    if args.report_output:
        write_text_lf(args.report_output, report)
    else:
        print(report, end="")
    return 0 if summary["overall_status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
