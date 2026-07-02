"""Audit continuity of normalized KRX OpenAPI tables.

This script reads normalized CSV outputs and produces row-count continuity
evidence. It does not create a tradable Universe or upgrade Backtest readiness.
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


TABLE_FILES = {
    "stock_daily": "stock_daily.csv",
    "issue_base": "issue_base.csv",
    "index_daily": "index_daily.csv",
}

AUDIT_FIELDS = (
    "date",
    "stock_daily_rows",
    "issue_base_rows",
    "index_daily_rows",
    "stock_kospi_rows",
    "stock_kosdaq_rows",
    "issue_kospi_rows",
    "issue_kosdaq_rows",
    "duplicate_stock_keys",
    "duplicate_issue_keys",
    "missing_issue_for_stock",
    "missing_stock_for_issue",
    "stock_daily_delta_prev",
    "issue_base_delta_prev",
    "row_count_alert",
)


def _read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise ValueError(f"missing normalized table: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def _rows_by_date(rows: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    by_date: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        by_date[row.get("date", "")].append(row)
    by_date.pop("", None)
    return dict(by_date)


def _market_count(rows: list[dict[str, str]], market: str) -> int:
    return sum(1 for row in rows if row.get("market") == market)


def _duplicate_key_count(rows: list[dict[str, str]], fields: tuple[str, ...]) -> int:
    keys = Counter(tuple(row.get(field, "") for field in fields) for row in rows)
    return sum(1 for count in keys.values() if count > 1)


def _code_set(rows: list[dict[str, str]]) -> set[str]:
    return {row.get("code", "") for row in rows if row.get("code")}


def audit_normalized_dir(normalized_dir: Path, max_row_delta: int) -> list[dict[str, Any]]:
    stock_rows = _read_csv(normalized_dir / TABLE_FILES["stock_daily"])
    issue_rows = _read_csv(normalized_dir / TABLE_FILES["issue_base"])
    index_rows = _read_csv(normalized_dir / TABLE_FILES["index_daily"])

    stock_by_date = _rows_by_date(stock_rows)
    issue_by_date = _rows_by_date(issue_rows)
    index_by_date = _rows_by_date(index_rows)
    dates = sorted(set(stock_by_date) | set(issue_by_date) | set(index_by_date))

    audit_rows: list[dict[str, Any]] = []
    previous_stock_count: int | None = None
    previous_issue_count: int | None = None
    for date in dates:
        day_stock = stock_by_date.get(date, [])
        day_issue = issue_by_date.get(date, [])
        day_index = index_by_date.get(date, [])
        stock_count = len(day_stock)
        issue_count = len(day_issue)
        stock_delta = "" if previous_stock_count is None else stock_count - previous_stock_count
        issue_delta = "" if previous_issue_count is None else issue_count - previous_issue_count
        row_count_alert = False
        if isinstance(stock_delta, int) and abs(stock_delta) > max_row_delta:
            row_count_alert = True
        if isinstance(issue_delta, int) and abs(issue_delta) > max_row_delta:
            row_count_alert = True

        stock_codes = _code_set(day_stock)
        issue_codes = _code_set(day_issue)
        audit_rows.append(
            {
                "date": date,
                "stock_daily_rows": stock_count,
                "issue_base_rows": issue_count,
                "index_daily_rows": len(day_index),
                "stock_kospi_rows": _market_count(day_stock, "KOSPI"),
                "stock_kosdaq_rows": _market_count(day_stock, "KOSDAQ"),
                "issue_kospi_rows": _market_count(day_issue, "KOSPI"),
                "issue_kosdaq_rows": _market_count(day_issue, "KOSDAQ"),
                "duplicate_stock_keys": _duplicate_key_count(day_stock, ("date", "code")),
                "duplicate_issue_keys": _duplicate_key_count(day_issue, ("date", "code")),
                "missing_issue_for_stock": len(stock_codes - issue_codes),
                "missing_stock_for_issue": len(issue_codes - stock_codes),
                "stock_daily_delta_prev": stock_delta,
                "issue_base_delta_prev": issue_delta,
                "row_count_alert": str(row_count_alert).lower(),
            }
        )
        previous_stock_count = stock_count
        previous_issue_count = issue_count
    return audit_rows


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=AUDIT_FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def _wikilink(path: Path) -> str:
    rendered = path.as_posix()
    return f"[[{rendered}|{rendered}]]"


def _render_markdown(rows: list[dict[str, Any]], normalized_dir: Path, rows_output: Path | None) -> str:
    alert_count = sum(1 for row in rows if row["row_count_alert"] == "true")
    duplicate_count = sum(int(row["duplicate_stock_keys"]) + int(row["duplicate_issue_keys"]) for row in rows)
    missing_pair_count = sum(int(row["missing_issue_for_stock"]) + int(row["missing_stock_for_issue"]) for row in rows)
    lines = [
        "# KRX OpenAPI Continuity Audit",
        "",
        f"- Source normalized dir: {_wikilink(normalized_dir)}",
        "- Interpretation: normalized row-count continuity audit, not a `Point-in-Time Universe` or `Backtest` result",
        "- Bias Control judgment: `hold`",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| Audited dates | {len(rows)} |",
        f"| Row-count alerts | {alert_count} |",
        f"| Duplicate date/code keys | {duplicate_count} |",
        f"| Stock/issue code mismatches | {missing_pair_count} |",
        "",
    ]
    if rows_output is not None:
        lines.extend(["## Row Output", "", f"- {_wikilink(rows_output)}", ""])

    lines.extend(
        [
            "## Date Rows",
            "",
            "| Date | Stock Rows | Issue Rows | Index Rows | Stock Delta | Issue Delta | Alert | Missing Pair Count |",
            "| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: |",
        ]
    )
    for row in rows:
        missing_pair = int(row["missing_issue_for_stock"]) + int(row["missing_stock_for_issue"])
        stock_delta = "-" if row["stock_daily_delta_prev"] == "" else row["stock_daily_delta_prev"]
        issue_delta = "-" if row["issue_base_delta_prev"] == "" else row["issue_base_delta_prev"]
        lines.append(
            f"| `{row['date']}` | {row['stock_daily_rows']} | {row['issue_base_rows']} | {row['index_daily_rows']} | "
            f"{stock_delta} | {issue_delta} | `{row['row_count_alert']}` | {missing_pair} |"
        )

    lines.extend(
        [
            "",
            "## Guardrails",
            "",
            "- Small row-count deltas can be legitimate listing or delisting changes, but they still require event-source validation before Backtest use.",
            "- Zero duplicate keys and zero stock/issue mismatches only validate normalized table consistency for this window.",
            "- Backtest readiness remains `hold` until `Point-in-Time` status replay and broader historical coverage are validated.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit continuity of normalized KRX OpenAPI tables.")
    parser.add_argument("--normalized-dir", required=True, type=Path)
    parser.add_argument("--max-row-delta", type=int, default=10)
    parser.add_argument("--rows-output", type=Path)
    parser.add_argument("--report-output", type=Path)
    args = parser.parse_args()

    try:
        rows = audit_normalized_dir(args.normalized_dir, args.max_row_delta)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc

    if args.rows_output:
        _write_csv(args.rows_output, rows)
    report = _render_markdown(rows, args.normalized_dir, args.rows_output)
    if args.report_output:
        args.report_output.parent.mkdir(parents=True, exist_ok=True)
        args.report_output.write_text(report, encoding="utf-8")
    else:
        print(report, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
