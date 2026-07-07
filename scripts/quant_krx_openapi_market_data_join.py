"""Join normalized KRX stock daily and issue base tables by date/code.

This produces a date-scoped market-data input for later Universe plumbing. It
does not add Point-in-Time status replay and does not make Backtest ready.
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from quant_io import write_text_lf

OUTPUT_FIELDS = (
    "date",
    "code",
    "standard_code",
    "stock_name",
    "issue_name",
    "short_name",
    "english_name",
    "market",
    "section",
    "listing_date",
    "security_group",
    "stock_certificate_type",
    "par_value_krw",
    "listed_shares_issue",
    "listed_shares_stock",
    "close",
    "change",
    "return_pct",
    "open",
    "high",
    "low",
    "volume",
    "trading_value_krw",
    "market_cap_krw",
    "source_stock_service",
    "source_issue_service",
    "source_stock_path",
    "source_issue_path",
)


def _read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise ValueError(f"missing normalized table: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def _key(row: dict[str, str]) -> tuple[str, str]:
    return row.get("date", ""), row.get("code", "")


def _duplicate_keys(rows: list[dict[str, str]]) -> list[tuple[str, str]]:
    counts = Counter(_key(row) for row in rows)
    return [key for key, count in counts.items() if key != ("", "") and count > 1]


def _index_by_date_code(rows: list[dict[str, str]], label: str) -> dict[tuple[str, str], dict[str, str]]:
    duplicates = _duplicate_keys(rows)
    if duplicates:
        sample = ", ".join(f"{date}/{code}" for date, code in duplicates[:5])
        raise ValueError(f"{label}: duplicate date/code keys: {sample}")
    return {_key(row): row for row in rows if _key(row) != ("", "")}


def _join_row(stock: dict[str, str], issue: dict[str, str]) -> dict[str, str]:
    return {
        "date": stock.get("date", ""),
        "code": stock.get("code", ""),
        "standard_code": issue.get("standard_code", ""),
        "stock_name": stock.get("name", ""),
        "issue_name": issue.get("name", ""),
        "short_name": issue.get("short_name", ""),
        "english_name": issue.get("english_name", ""),
        "market": stock.get("market", "") or issue.get("market", ""),
        "section": stock.get("section", "") or issue.get("section", ""),
        "listing_date": issue.get("listing_date", ""),
        "security_group": issue.get("security_group", ""),
        "stock_certificate_type": issue.get("stock_certificate_type", ""),
        "par_value_krw": issue.get("par_value_krw", ""),
        "listed_shares_issue": issue.get("listed_shares", ""),
        "listed_shares_stock": stock.get("listed_shares", ""),
        "close": stock.get("close", ""),
        "change": stock.get("change", ""),
        "return_pct": stock.get("return_pct", ""),
        "open": stock.get("open", ""),
        "high": stock.get("high", ""),
        "low": stock.get("low", ""),
        "volume": stock.get("volume", ""),
        "trading_value_krw": stock.get("trading_value_krw", ""),
        "market_cap_krw": stock.get("market_cap_krw", ""),
        "source_stock_service": stock.get("source_service", ""),
        "source_issue_service": issue.get("source_service", ""),
        "source_stock_path": stock.get("source_path", ""),
        "source_issue_path": issue.get("source_path", ""),
    }


def _date_set(rows: list[dict[str, str]]) -> set[str]:
    return {row.get("date", "") for row in rows if row.get("date")}


def _drop_issue_only_dates(
    stock_rows: list[dict[str, str]],
    issue_rows: list[dict[str, str]],
) -> tuple[list[dict[str, str]], dict[str, Any]]:
    stock_dates = _date_set(stock_rows)
    issue_dates = _date_set(issue_rows)
    issue_only_dates = sorted(issue_dates - stock_dates)
    if not issue_only_dates:
        return issue_rows, {"dropped_issue_only_dates": [], "dropped_issue_only_rows": 0}

    dropped = [row for row in issue_rows if row.get("date", "") in issue_only_dates]
    kept = [row for row in issue_rows if row.get("date", "") not in issue_only_dates]
    return kept, {"dropped_issue_only_dates": issue_only_dates, "dropped_issue_only_rows": len(dropped)}


def join_market_data(
    normalized_dir: Path,
    drop_issue_only_dates: bool = False,
) -> tuple[list[dict[str, str]], dict[str, Any]]:
    stock_rows = _read_csv(normalized_dir / "stock_daily.csv")
    issue_rows = _read_csv(normalized_dir / "issue_base.csv")
    dropped_summary: dict[str, Any] = {"dropped_issue_only_dates": [], "dropped_issue_only_rows": 0}
    if drop_issue_only_dates:
        issue_rows, dropped_summary = _drop_issue_only_dates(stock_rows, issue_rows)

    stock_by_key = _index_by_date_code(stock_rows, "stock_daily")
    issue_by_key = _index_by_date_code(issue_rows, "issue_base")

    stock_keys = set(stock_by_key)
    issue_keys = set(issue_by_key)
    missing_issue = sorted(stock_keys - issue_keys)
    missing_stock = sorted(issue_keys - stock_keys)
    if missing_issue:
        sample = ", ".join(f"{date}/{code}" for date, code in missing_issue[:5])
        raise ValueError(f"stock rows without issue rows: {sample}")
    if missing_stock:
        sample = ", ".join(f"{date}/{code}" for date, code in missing_stock[:5])
        raise ValueError(f"issue rows without stock rows: {sample}")

    rows = [_join_row(stock_by_key[key], issue_by_key[key]) for key in sorted(stock_keys)]
    by_date: dict[str, int] = defaultdict(int)
    by_market: dict[str, int] = defaultdict(int)
    for row in rows:
        by_date[row["date"]] += 1
        by_market[row["market"]] += 1

    summary = {
        "joined_rows": len(rows),
        "date_count": len(by_date),
        "by_date": dict(sorted(by_date.items())),
        "by_market": dict(sorted(by_market.items())),
        "missing_issue_for_stock": len(missing_issue),
        "missing_stock_for_issue": len(missing_stock),
        **dropped_summary,
    }
    return rows, summary


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def _wikilink(path: Path) -> str:
    rendered = path.as_posix()
    return f"[[{rendered}|{rendered}]]"


def _render_markdown(summary: dict[str, Any], normalized_dir: Path, output: Path) -> str:
    lines = [
        "# KRX OpenAPI Market Data Join Result",
        "",
        f"- Source normalized dir: {_wikilink(normalized_dir)}",
        f"- Output: {_wikilink(output)}",
        "- Interpretation: date-scoped market-data input, not a `Point-in-Time Universe` or `Backtest` result",
        "- Bias Control judgment: `hold`",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| Joined rows | {summary['joined_rows']} |",
        f"| Date count | {summary['date_count']} |",
        f"| Missing issue rows for stock rows | {summary['missing_issue_for_stock']} |",
        f"| Missing stock rows for issue rows | {summary['missing_stock_for_issue']} |",
        f"| Dropped issue-only dates | {len(summary.get('dropped_issue_only_dates', []))} |",
        f"| Dropped issue-only rows | {summary.get('dropped_issue_only_rows', 0)} |",
        "",
        "## Market Counts",
        "",
        "| Market | Rows |",
        "| --- | ---: |",
    ]
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
            "- This join validates table alignment for stock daily and issue base rows only.",
            "- If issue-only dates were dropped, those dates had issue-base rows but no stock-daily rows and are treated as non-trading-date evidence, not joined market data.",
            "- It does not replay historical managed issue, trading halt, market alert, or delisting status.",
            "- Backtest readiness remains `hold` until `Point-in-Time` status replay and broader historical coverage are validated.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Join normalized KRX stock daily and issue base tables by date/code.")
    parser.add_argument("--normalized-dir", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--report-output", type=Path)
    parser.add_argument(
        "--drop-issue-only-dates",
        action="store_true",
        help="Drop dates that have issue-base rows but no stock-daily rows before strict date/code joining.",
    )
    args = parser.parse_args()

    try:
        rows, summary = join_market_data(args.normalized_dir, args.drop_issue_only_dates)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc

    _write_csv(args.output, rows)
    report = _render_markdown(summary, args.normalized_dir, args.output)
    if args.report_output:
        write_text_lf(args.report_output, report)
    else:
        print(report, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
