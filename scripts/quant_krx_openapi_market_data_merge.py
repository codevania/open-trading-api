"""Merge KRX OpenAPI market-data join CSVs into one date/code table.

This script reads already-joined market-data CSV files. It does not call KRX
and keeps duplicate date/code keys as a hard failure.
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path
from typing import Any

from quant_io import write_text_lf


def _read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path.exists():
        raise ValueError(f"missing market-data CSV: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = list(reader.fieldnames or [])
        rows = [{key: (value or "").strip() for key, value in row.items()} for row in reader]
    if not fields:
        raise ValueError(f"market-data CSV has no header: {path}")
    if "date" not in fields or "code" not in fields:
        raise ValueError(f"market-data CSV missing date/code columns: {path}")
    return fields, rows


def _key(row: dict[str, str]) -> tuple[str, str]:
    return row.get("date", ""), row.get("code", "")


def merge_market_data(inputs: list[Path]) -> tuple[list[str], list[dict[str, str]], dict[str, Any]]:
    if not inputs:
        raise ValueError("at least one --input is required")

    base_fields: list[str] | None = None
    merged_rows: list[dict[str, str]] = []
    input_counts: list[dict[str, Any]] = []
    for path in inputs:
        fields, rows = _read_csv(path)
        if base_fields is None:
            base_fields = fields
        elif fields != base_fields:
            raise ValueError(f"market-data CSV schema mismatch: {path}")
        merged_rows.extend(rows)
        input_counts.append({"path": path, "rows": len(rows)})

    duplicate_keys = [key for key, count in Counter(_key(row) for row in merged_rows).items() if key != ("", "") and count > 1]
    if duplicate_keys:
        sample = ", ".join(f"{date}/{code}" for date, code in sorted(duplicate_keys)[:5])
        raise ValueError(f"duplicate date/code keys across inputs: {sample}")

    merged_rows = sorted(merged_rows, key=lambda row: (row.get("date", ""), row.get("market", ""), row.get("code", "")))
    by_date = Counter(row.get("date", "") for row in merged_rows if row.get("date", ""))
    by_market = Counter(row.get("market", "") for row in merged_rows if row.get("market", ""))
    summary = {
        "inputs": input_counts,
        "merged_rows": len(merged_rows),
        "date_count": len(by_date),
        "by_date": dict(sorted(by_date.items())),
        "by_market": dict(sorted(by_market.items())),
    }
    return list(base_fields or []), merged_rows, summary


def _write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def _wikilink(path: Path) -> str:
    rendered = path.as_posix()
    return f"[[{rendered}|{rendered}]]"


def _render_report(summary: dict[str, Any], output: Path) -> str:
    lines = [
        "# KRX OpenAPI Market Data Merge Result",
        "",
        f"- Output: {_wikilink(output)}",
        "- Interpretation: joined market-data merge, not a `Point-in-Time Universe` or `Backtest` result",
        "- Bias Control judgment: `hold`",
        "",
        "## Inputs",
        "",
        "| Input | Rows |",
        "| --- | ---: |",
    ]
    for item in summary["inputs"]:
        lines.append(f"| {_wikilink(item['path'])} | {item['rows']} |")

    lines.extend(
        [
            "",
            "## Summary",
            "",
            "| Metric | Value |",
            "| --- | ---: |",
            f"| Merged rows | {summary['merged_rows']} |",
            f"| Date count | {summary['date_count']} |",
            "",
            "## Market Counts",
            "",
            "| Market | Rows |",
            "| --- | ---: |",
        ]
    )
    for market, count in summary["by_market"].items():
        lines.append(f"| `{market}` | {count} |")

    lines.extend(["", "## Date Counts", "", "| Date | Rows |", "| --- | ---: |"])
    for date, count in summary["by_date"].items():
        lines.append(f"| `{date}` | {count} |")

    lines.extend(
        [
            "",
            "## Guardrails",
            "",
            "- Duplicate date/code keys across inputs are a hard failure.",
            "- This output still lacks complete historical status coverage by itself.",
            "- Backtest readiness remains `hold` until `Point-in-Time` status replay and broader historical coverage are validated.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Merge KRX OpenAPI market-data join CSV files.")
    parser.add_argument("--input", action="append", required=True, type=Path, help="Joined market-data CSV. Repeatable.")
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--report-output", type=Path)
    args = parser.parse_args()

    try:
        fields, rows, summary = merge_market_data(args.input)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc

    _write_csv(args.output, fields, rows)
    report = _render_report(summary, args.output)
    if args.report_output:
        write_text_lf(args.report_output, report)
    else:
        print(report, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
