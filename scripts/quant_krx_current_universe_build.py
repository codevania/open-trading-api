"""Build a current KRX Universe snapshot from official manual CSV files.

This script reads already-downloaded KRX CSV files. It does not download data
and does not create a historical Point-in-Time Universe. The output is a
current-snapshot Universe for paper/smoke work only.
"""

from __future__ import annotations

import argparse
import csv
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from quant_krx_managed_issues_extract import CSV_ENCODINGS, parse_managed_issues


CODE_COLUMNS = ("종목코드", "단축코드", "표준코드")
NAME_COLUMNS = ("종목명", "한글 종목약명", "한글종목명", "한글명")
MARKET_COLUMNS = ("시장구분", "시장구분명", "시장")
TYPE_COLUMNS = ("주식종류", "증권구분", "종목구분", "상품구분")
ALLOWED_MARKETS = ("KOSPI", "KOSDAQ", "유가증권", "코스피", "코스닥")
EXCLUDED_TYPE_TOKENS = ("ETF", "ETN", "ELW", "스팩", "리츠", "REIT", "우선주")
PREFERRED_NAME_RE = re.compile(r"(?:\d+우B?|우B?|우선주)$")


@dataclass(frozen=True)
class ListedIssue:
    code: str
    name: str
    market: str
    security_type: str


@dataclass(frozen=True)
class UniverseRow:
    code: str
    name: str
    market: str
    security_type: str
    status: str
    reason: str


def _read_csv_dicts(path: Path) -> tuple[list[dict[str, Any]], str]:
    last_error: Exception | None = None
    for encoding in CSV_ENCODINGS:
        try:
            with path.open("r", encoding=encoding, newline="") as handle:
                reader = csv.DictReader(handle)
                return list(reader), encoding
        except Exception as exc:  # pragma: no cover - fallback diagnostics
            last_error = exc
    raise ValueError(f"could not read CSV: {last_error}")


def _first_present(row: dict[str, Any], candidates: tuple[str, ...]) -> str:
    for key in candidates:
        value = row.get(key)
        if value not in (None, ""):
            return str(value).strip()
    return ""


def _normalize_code(value: Any) -> str:
    code = str(value or "").strip().strip('"').upper()
    if code.startswith("KR") and len(code) >= 9:
        return code[3:9]
    if code.endswith(".0") and code[:-2].isdigit():
        code = code[:-2]
    if code.isdigit() and len(code) < 6:
        return code.zfill(6)
    return code


def _require_any_column(rows: list[dict[str, Any]], candidates: tuple[str, ...], label: str) -> None:
    if not rows:
        raise ValueError("listed issues CSV has no data rows")
    columns = set(rows[0].keys())
    if not any(column in columns for column in candidates):
        raise ValueError(f"missing {label} column; accepted aliases: {', '.join(candidates)}")


def parse_listed_issues(path: Path) -> tuple[list[ListedIssue], str]:
    rows, encoding = _read_csv_dicts(path)
    _require_any_column(rows, CODE_COLUMNS, "code")
    _require_any_column(rows, NAME_COLUMNS, "name")

    issues: list[ListedIssue] = []
    for row in rows:
        code = _normalize_code(_first_present(row, CODE_COLUMNS))
        name = _first_present(row, NAME_COLUMNS)
        market = _first_present(row, MARKET_COLUMNS)
        security_type = _first_present(row, TYPE_COLUMNS)
        if not code or not name:
            raise ValueError(f"invalid listed issue row: {row}")
        issues.append(ListedIssue(code, name, market, security_type))
    issues.sort(key=lambda issue: issue.code)
    return issues, encoding


def _is_allowed_market(market: str) -> bool:
    if not market:
        return True
    normalized = market.upper()
    return any(token.upper() in normalized for token in ALLOWED_MARKETS)


def _instrument_exclusion_reason(issue: ListedIssue) -> str | None:
    type_text = issue.security_type.upper()
    name_text = issue.name.upper()
    if any(token.upper() in type_text for token in EXCLUDED_TYPE_TOKENS):
        return "instrument_type_excluded"
    if any(token.upper() in name_text for token in ("ETF", "ETN", "ELW", "스팩", "리츠", "REIT")):
        return "instrument_name_excluded"
    if PREFERRED_NAME_RE.search(issue.name):
        return "preferred_share_name"
    return None


def build_universe(listed: list[ListedIssue], managed_codes: set[str]) -> list[UniverseRow]:
    rows: list[UniverseRow] = []
    for issue in listed:
        reasons = []
        if not _is_allowed_market(issue.market):
            reasons.append("market_not_allowed")
        instrument_reason = _instrument_exclusion_reason(issue)
        if instrument_reason:
            reasons.append(instrument_reason)
        if issue.code in managed_codes:
            reasons.append("managed_issue_current")

        status = "exclude" if reasons else "include"
        rows.append(
            UniverseRow(
                issue.code,
                issue.name,
                issue.market,
                issue.security_type,
                status,
                ";".join(reasons) if reasons else "eligible_current_snapshot",
            )
        )
    rows.sort(key=lambda row: (row.status, row.code))
    return rows


def _write_csv(rows: list[UniverseRow], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=("code", "name", "market", "security_type", "status", "reason"))
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "code": row.code,
                    "name": row.name,
                    "market": row.market,
                    "security_type": row.security_type,
                    "status": row.status,
                    "reason": row.reason,
                }
            )


def _render_markdown(
    rows: list[UniverseRow],
    listed_raw: Path,
    listed_encoding: str,
    managed_raw: Path,
    as_of_date: str,
    csv_output: Path | None,
) -> str:
    include_count = sum(1 for row in rows if row.status == "include")
    exclude_count = len(rows) - include_count
    reason_counts: dict[str, int] = {}
    for row in rows:
        if row.status == "exclude":
            for reason in row.reason.split(";"):
                reason_counts[reason] = reason_counts.get(reason, 0) + 1

    lines = [
        "# KRX Current Universe v0",
        "",
        f"- As-of date: `{as_of_date}`",
        f"- Listed issues raw: `{listed_raw.as_posix()}`",
        f"- Listed issues encoding: `{listed_encoding}`",
        f"- Managed issues raw: `{managed_raw.as_posix()}`",
        "- Universe mode: `current_snapshot`",
        "- Interpretation: `paper/smoke Universe only`, `not Point-in-Time Universe`",
        "- Bias Control judgment: `hold`",
    ]
    if csv_output:
        lines.append(f"- Machine-readable rows: `{csv_output.as_posix()}`")
    lines.extend(
        [
            "",
            "## Summary",
            "",
            f"- Total listed rows: `{len(rows)}`",
            f"- Included rows: `{include_count}`",
            f"- Excluded rows: `{exclude_count}`",
            "",
            "## Exclusion Reason Counts",
            "",
            "| Reason | Count |",
            "| --- | ---: |",
        ]
    )
    for reason, count in sorted(reason_counts.items()):
        lines.append(f"| `{reason}` | {count} |")

    lines.extend(
        [
            "",
            "## Included Sample",
            "",
            "| Code | Company | Market | Security Type |",
            "| --- | --- | --- | --- |",
        ]
    )
    for row in [row for row in rows if row.status == "include"][:20]:
        lines.append(f"| `{row.code}` | {row.name} | {row.market} | {row.security_type} |")

    lines.extend(
        [
            "",
            "## Guardrails",
            "",
            "- This Universe uses current KRX listed issues and current managed-issue exclusions only.",
            "- Listing Age, Liquidity Filter, trading suspension, market-alert, and delisting history are not solved here.",
            "- This artifact can drive paper/smoke validation but not a performance Backtest claim.",
            "- Do not upgrade Strategy interpretation above `hold` until reproducible Point-in-Time snapshots exist.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a current KRX Universe v0 from local manual CSV snapshots.")
    parser.add_argument("--listed-raw", required=True, type=Path)
    parser.add_argument("--managed-raw", required=True, type=Path)
    parser.add_argument("--as-of-date", required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--csv-output", type=Path)
    args = parser.parse_args()

    if not args.listed_raw.exists():
        raise SystemExit(f"listed raw CSV not found: {args.listed_raw}")
    if not args.managed_raw.exists():
        raise SystemExit(f"managed raw CSV not found: {args.managed_raw}")

    listed, listed_encoding = parse_listed_issues(args.listed_raw)
    managed, _managed_encoding = parse_managed_issues(args.managed_raw)
    rows = build_universe(listed, {issue.code for issue in managed})

    if args.csv_output:
        _write_csv(rows, args.csv_output)

    report = _render_markdown(
        rows,
        args.listed_raw,
        listed_encoding,
        args.managed_raw,
        args.as_of_date,
        args.csv_output,
    )
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(report, encoding="utf-8")
    else:
        print(report, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
