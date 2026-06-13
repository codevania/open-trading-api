"""Extract current KRX managed issues into a Universe exclusion report.

This script reads an already-downloaded KRX managed-issues CSV. It does not
download KRX data and does not create a Point-in-Time Universe. The output is a
current-snapshot exclusion evidence report for Quant Universe work.
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Any


CSV_ENCODINGS = ("utf-8-sig", "utf-8", "cp949", "euc-kr")
REQUIRED_COLUMNS = ("종목코드", "종목명", "지정일자")


@dataclass(frozen=True)
class ManagedIssue:
    code: str
    name: str
    designation_date: str
    instrument_note: str


def _read_csv_dicts(path: Path) -> tuple[list[dict[str, Any]], str]:
    last_error: Exception | None = None
    for encoding in CSV_ENCODINGS:
        try:
            with path.open("r", encoding=encoding, newline="") as handle:
                reader = csv.DictReader(handle)
                rows = list(reader)
                return rows, encoding
        except Exception as exc:  # pragma: no cover - fallback diagnostics
            last_error = exc
    raise ValueError(f"could not read CSV: {last_error}")


def _normalize_code(value: Any) -> str:
    code = str(value or "").strip()
    if code.endswith(".0"):
        code = code[:-2]
    return code.zfill(6)


def _instrument_note(name: str) -> str:
    if "스팩" in name or "SPAC" in name.upper():
        return "SPAC"
    if "리츠" in name or "REIT" in name.upper():
        return "REIT"
    return "common-stock-or-unclassified"


def parse_managed_issues(path: Path) -> tuple[list[ManagedIssue], str]:
    rows, encoding = _read_csv_dicts(path)
    if not rows:
        raise ValueError("managed issues CSV has no data rows")

    columns = set(rows[0].keys())
    missing = [column for column in REQUIRED_COLUMNS if column not in columns]
    if missing:
        raise ValueError(f"missing required columns: {', '.join(missing)}")

    issues = []
    for row in rows:
        code = _normalize_code(row.get("종목코드"))
        name = str(row.get("종목명") or "").strip()
        designation_date = str(row.get("지정일자") or "").strip()
        if not code or not name:
            raise ValueError(f"invalid managed issue row: {row}")
        issues.append(ManagedIssue(code, name, designation_date, _instrument_note(name)))

    issues.sort(key=lambda issue: (issue.designation_date, issue.code), reverse=True)
    return issues, encoding


def _render_markdown(issues: list[ManagedIssue], raw_path: Path, encoding: str, as_of_date: str) -> str:
    common_or_unknown = sum(1 for issue in issues if issue.instrument_note == "common-stock-or-unclassified")
    spac = sum(1 for issue in issues if issue.instrument_note == "SPAC")
    reit = sum(1 for issue in issues if issue.instrument_note == "REIT")

    lines = [
        "# KRX Managed Issues Current Exclusions",
        "",
        f"- As-of date: `{as_of_date}`",
        f"- Source raw: `{raw_path.as_posix()}`",
        f"- Detected encoding: `{encoding}`",
        f"- Row count: `{len(issues)}`",
        "- Interpretation: `current snapshot Universe exclusion evidence`, `not Point-in-Time Universe`",
        "- Exclusion Rule: exclude every listed code from the current investable Universe snapshot.",
        "- Bias Control judgment: `hold` until reproducible Point-in-Time snapshots exist.",
        "",
        "## Instrument Notes",
        "",
        f"- common-stock-or-unclassified: `{common_or_unknown}`",
        f"- SPAC: `{spac}`",
        f"- REIT: `{reit}`",
        "",
        "## Exclusion Rows",
        "",
        "| Code | Company | Designation Date | Instrument Note |",
        "| --- | --- | --- | --- |",
    ]
    for issue in issues:
        lines.append(
            f"| `{issue.code}` | {issue.name} | `{issue.designation_date}` | `{issue.instrument_note}` |"
        )
    lines.extend(
        [
            "",
            "## Guardrails",
            "",
            "- This output is derived from one current KRX snapshot.",
            "- It can exclude currently managed issues from a paper/smoke Universe snapshot.",
            "- It cannot prove historical membership for past Rebalance dates.",
            "- Do not upgrade Strategy or Backtest interpretation above `hold` from this artifact alone.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract current KRX managed issues into a markdown exclusion report.")
    parser.add_argument("--raw", required=True, type=Path)
    parser.add_argument("--as-of-date", required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    if not args.raw.exists():
        raise SystemExit(f"raw CSV not found: {args.raw}")

    issues, encoding = parse_managed_issues(args.raw)
    report = _render_markdown(issues, args.raw, encoding, args.as_of_date)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(report, encoding="utf-8")
    else:
        print(report, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
