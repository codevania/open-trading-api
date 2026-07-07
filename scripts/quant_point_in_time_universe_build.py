"""Build a Point-in-Time Universe eligibility smoke table.

This script consumes already-replayed market-data rows. It does not collect raw
data and does not prove historical status coverage beyond the supplied replay.
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path
from typing import Any

from quant_io import write_text_lf


ALLOWED_MARKETS = {"KOSPI", "KOSDAQ"}
COMMON_SECURITY_GROUP = "주권"
COMMON_STOCK_CERTIFICATE_TYPE = "보통주"
REQUIRED_COLUMNS = (
    "date",
    "code",
    "stock_name",
    "market",
    "listing_date",
    "security_group",
    "stock_certificate_type",
    "close",
    "volume",
    "trading_value_krw",
    "market_cap_krw",
    "pit_status_replay_status",
    "pit_status_exclude_reasons",
)
OUTPUT_COLUMNS = (
    "date",
    "code",
    "stock_name",
    "market",
    "listing_date",
    "security_group",
    "stock_certificate_type",
    "close",
    "volume",
    "trading_value_krw",
    "market_cap_krw",
    "pit_status_replay_status",
    "pit_status_exclude_reasons",
    "pit_universe_status",
    "pit_universe_exclude_reasons",
    "pit_universe_mode",
)


def _read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path.exists():
        raise ValueError(f"missing replayed market-data CSV: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or [])
        rows = [{key: (value or "").strip() for key, value in row.items()} for row in reader]
    return fieldnames, rows


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_COLUMNS, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def _require_columns(fieldnames: list[str]) -> None:
    missing = [column for column in REQUIRED_COLUMNS if column not in fieldnames]
    if missing:
        raise ValueError(f"replayed market-data CSV missing required columns: {', '.join(missing)}")


def _exclude_reasons(row: dict[str, str]) -> list[str]:
    reasons: list[str] = []
    if row.get("market", "") not in ALLOWED_MARKETS:
        reasons.append("market_not_allowed")
    if row.get("security_group", "") != COMMON_SECURITY_GROUP:
        reasons.append("security_group_not_plain_equity")
    if row.get("stock_certificate_type", "") != COMMON_STOCK_CERTIFICATE_TYPE:
        reasons.append("stock_certificate_not_common")
    if row.get("pit_status_replay_status") == "exclude_by_status_event":
        status_reasons = row.get("pit_status_exclude_reasons", "")
        if status_reasons:
            for reason in status_reasons.split(";"):
                if reason:
                    reasons.append(f"status_event:{reason}")
        else:
            reasons.append("status_event:unspecified")
    return reasons


def build_point_in_time_universe(
    replayed_market_data_path: Path,
    mode: str = "status_replay_smoke",
) -> tuple[list[dict[str, str]], dict[str, Any]]:
    fieldnames, input_rows = _read_csv(replayed_market_data_path)
    _require_columns(fieldnames)

    output_rows: list[dict[str, str]] = []
    reason_counts: Counter[str] = Counter()
    date_counts: Counter[str] = Counter()
    include_by_date: Counter[str] = Counter()
    exclude_by_date: Counter[str] = Counter()

    for row in input_rows:
        reasons = _exclude_reasons(row)
        status = "exclude" if reasons else "include"
        date = row["date"]
        date_counts[date] += 1
        if status == "include":
            include_by_date[date] += 1
        else:
            exclude_by_date[date] += 1
            reason_counts.update(reasons)

        output_rows.append(
            {
                "date": row["date"],
                "code": row["code"],
                "stock_name": row["stock_name"],
                "market": row["market"],
                "listing_date": row["listing_date"],
                "security_group": row["security_group"],
                "stock_certificate_type": row["stock_certificate_type"],
                "close": row["close"],
                "volume": row["volume"],
                "trading_value_krw": row["trading_value_krw"],
                "market_cap_krw": row["market_cap_krw"],
                "pit_status_replay_status": row["pit_status_replay_status"],
                "pit_status_exclude_reasons": row["pit_status_exclude_reasons"],
                "pit_universe_status": status,
                "pit_universe_exclude_reasons": ";".join(reasons),
                "pit_universe_mode": mode,
            }
        )

    summary = {
        "replayed_market_data_path": replayed_market_data_path,
        "input_rows": len(input_rows),
        "output_rows": len(output_rows),
        "include_rows": sum(1 for row in output_rows if row["pit_universe_status"] == "include"),
        "exclude_rows": sum(1 for row in output_rows if row["pit_universe_status"] == "exclude"),
        "date_count": len(date_counts),
        "reason_counts": dict(sorted(reason_counts.items())),
        "include_by_date": dict(sorted(include_by_date.items())),
        "exclude_by_date": dict(sorted(exclude_by_date.items())),
        "mode": mode,
    }
    return output_rows, summary


def _wikilink(path: Path) -> str:
    rendered = path.as_posix()
    return f"[[{rendered}|{rendered}]]"


def _render_report(summary: dict[str, Any], output_path: Path) -> str:
    lines = [
        "# Point-in-Time Universe Smoke",
        "",
        f"- Replayed market-data input: {_wikilink(summary['replayed_market_data_path'])}",
        f"- Output: {_wikilink(output_path)}",
        f"- Mode: `{summary['mode']}`",
        "- Interpretation: Universe eligibility smoke only, not a full historical Backtest input",
        "- Backtest readiness: `hold`",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| Input rows | {summary['input_rows']} |",
        f"| Output rows | {summary['output_rows']} |",
        f"| Dates | {summary['date_count']} |",
        f"| Include rows | {summary['include_rows']} |",
        f"| Exclude rows | {summary['exclude_rows']} |",
        "",
        "## Exclusion Reason Counts",
        "",
        "| Reason | Rows |",
        "| --- | ---: |",
    ]
    if summary["reason_counts"]:
        for reason, count in summary["reason_counts"].items():
            lines.append(f"| `{reason}` | {count} |")
    else:
        lines.append("| `none` | 0 |")

    lines.extend(
        [
            "",
            "## Date Counts",
            "",
            "| Date | Include | Exclude |",
            "| --- | ---: | ---: |",
        ]
    )
    for date in sorted(set(summary["include_by_date"]) | set(summary["exclude_by_date"])):
        lines.append(f"| `{date}` | {summary['include_by_date'].get(date, 0)} | {summary['exclude_by_date'].get(date, 0)} |")

    lines.extend(
        [
            "",
            "## Guardrails",
            "",
            "- This consumes supplied status replay rows; it does not prove status-source completeness.",
            "- `include` means the row passed the local instrument/status filters in this smoke input.",
            "- Do not treat this as Backtest-ready until historical status coverage, Liquidity Filter, and strategy/OOS gates are complete.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a Point-in-Time Universe eligibility smoke table.")
    parser.add_argument("--replayed-market-data", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--report-output", type=Path)
    parser.add_argument("--mode", default="status_replay_smoke")
    args = parser.parse_args()

    try:
        rows, summary = build_point_in_time_universe(args.replayed_market_data, args.mode)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc

    _write_csv(args.output, rows)
    report = _render_report(summary, args.output)
    if args.report_output:
        write_text_lf(args.report_output, report)
    else:
        print(report, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
