"""Audit saved KIS daily OHLCV calendar coverage for Quant research.

This script is read-only. It does not call KIS, does not download KRX data, and
does not build a Point-in-Time Universe. It compares already-saved daily raw
files to catch symbol-level date coverage mismatches before Backtest work.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from quant_smoke_validate import _extract_rows, _find_raw_files, _load_json, _load_symbol_labels, _symbol_from_path


@dataclass
class CalendarResult:
    symbol: str
    rows: int
    unique_dates: int
    first_date: str
    last_date: str
    duplicate_dates: list[str]
    missing_dates: list[str]
    extra_dates: list[str]
    status: str


def _load_expected_dates(path: Path | None) -> list[str] | None:
    if path is None:
        return None
    dates = []
    for line in path.read_text(encoding="utf-8").splitlines():
        value = line.strip().split(",", 1)[0].strip()
        if value and value.lower() not in {"date", "stck_bsop_date"}:
            dates.append(value)
    return sorted(set(dates))


def _dates_from_file(path: Path) -> list[str]:
    rows = _extract_rows(_load_json(path))
    dates = [str(row.get("stck_bsop_date", "")).strip() for row in rows]
    return [date for date in dates if date]


def _audit_file(path: Path, expected_dates: list[str]) -> CalendarResult:
    symbol = _symbol_from_path(path)
    dates = _dates_from_file(path)
    unique = sorted(set(dates))
    counts = Counter(dates)
    duplicate_dates = sorted(date for date, count in counts.items() if count > 1)
    missing_dates = sorted(set(expected_dates) - set(unique))
    extra_dates = sorted(set(unique) - set(expected_dates))

    if not dates:
        status = "fail"
    elif duplicate_dates:
        status = "fail"
    elif missing_dates or extra_dates:
        status = "hold"
    else:
        status = "pass"

    return CalendarResult(
        symbol=symbol,
        rows=len(dates),
        unique_dates=len(unique),
        first_date=unique[0] if unique else "",
        last_date=unique[-1] if unique else "",
        duplicate_dates=duplicate_dates,
        missing_dates=missing_dates,
        extra_dates=extra_dates,
        status=status,
    )


def _overall_status(results: list[CalendarResult], has_external_calendar: bool) -> str:
    if any(result.status == "fail" for result in results):
        return "fail"
    if any(result.status == "hold" for result in results):
        return "hold"
    if not has_external_calendar:
        return "reference-only"
    return "pass"


def _short_dates(dates: list[str], limit: int = 8) -> str:
    if not dates:
        return ""
    shown = ", ".join(dates[:limit])
    if len(dates) > limit:
        return f"{shown}, ... (+{len(dates) - limit})"
    return shown


def render_markdown(raw_dir: Path, results: list[CalendarResult], expected_source: str) -> str:
    has_external_calendar = expected_source != "symbol-union"
    status = _overall_status(results, has_external_calendar)
    lines = [
        "# KIS OHLCV Calendar Audit Result",
        "",
        f"- Source raw directory: `{raw_dir.as_posix()}`",
        "- Auditor: `scripts/quant_calendar_audit.py`",
        f"- Expected calendar source: `{expected_source}`",
        f"- Overall status: `{status}`",
        "- Interpretation: `calendar coverage audit only`, `not Backtest ready`",
        "- Bias Control judgment: `hold`",
        "",
        "| Symbol | Status | Rows | Unique Dates | First Date | Last Date | Missing Dates | Extra Dates | Duplicate Dates |",
        "| --- | --- | ---: | ---: | --- | --- | --- | --- | --- |",
    ]
    for result in results:
        lines.append(
            f"| `{result.symbol}` | {result.status} | {result.rows} | {result.unique_dates} | "
            f"{result.first_date} | {result.last_date} | {_short_dates(result.missing_dates)} | "
            f"{_short_dates(result.extra_dates)} | {_short_dates(result.duplicate_dates)} |"
        )
    lines.extend(
        [
            "",
            "## Guardrails",
            "",
            "- This audit compares saved OHLCV dates only.",
            "- Without an external KRX/KIS trading calendar, a `pass` is not possible; symbol-union mode is `reference-only` at best.",
            "- Calendar coverage consistency does not solve Survivorship Bias or Point-in-Time Universe construction.",
            "- Keep Strategy interpretation at `hold` until official Universe snapshots, OOS, and Bias Control pass.",
        ]
    )
    return "\n".join(lines) + "\n"


def audit_raw_dir(raw_dir: Path, expected_calendar: Path | None = None) -> tuple[list[CalendarResult], str]:
    raw_files = _find_raw_files(raw_dir)
    if not raw_files:
        raise ValueError(f"no raw daily files found under: {raw_dir}")

    expected_dates = _load_expected_dates(expected_calendar)
    expected_source = expected_calendar.as_posix() if expected_calendar else "symbol-union"
    if expected_dates is None:
        all_dates = []
        for path in raw_files:
            all_dates.extend(_dates_from_file(path))
        expected_dates = sorted(set(all_dates))

    labels = _load_symbol_labels(raw_dir)
    results = [_audit_file(path, expected_dates) for path in raw_files]
    for result in results:
        result.symbol = labels.get(result.symbol, result.symbol)
    return results, expected_source


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit saved Quant OHLCV raw calendar coverage.")
    parser.add_argument("--raw-dir", required=True, type=Path)
    parser.add_argument("--expected-calendar", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    if not args.raw_dir.exists():
        raise SystemExit(f"raw dir not found: {args.raw_dir}")
    if args.expected_calendar and not args.expected_calendar.exists():
        raise SystemExit(f"expected calendar not found: {args.expected_calendar}")

    try:
        results, expected_source = audit_raw_dir(args.raw_dir, args.expected_calendar)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc

    report = render_markdown(args.raw_dir, results, expected_source)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(report, encoding="utf-8")
    else:
        print(report, end="")

    status = _overall_status(results, expected_source != "symbol-union")
    return 1 if status == "fail" else 0


if __name__ == "__main__":
    raise SystemExit(main())
