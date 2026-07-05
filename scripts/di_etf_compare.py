"""Render DI core ETF and satellite candidate comparison from YAML."""

from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import yaml


try:
    KST = ZoneInfo("Asia/Seoul")
except Exception:
    KST = timezone(timedelta(hours=9), "KST")

DEFAULT_CANDIDATE_FILE = Path("_report/di/candidates/core-satellite-candidates.yaml")


def _now_kst() -> datetime:
    return datetime.now(KST).replace(microsecond=0)


def _load_yaml(path: Path) -> dict[str, Any]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path}: expected YAML object")
    return payload


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def _display(value: Any) -> str:
    if value is None:
        return "TODO"
    if isinstance(value, bool):
        return "yes" if value else "no"
    if isinstance(value, list):
        return ", ".join(_display(item) for item in value) or "-"
    text = str(value).strip()
    return text if text else "TODO"


def _validate_candidate(row: Any, section: str, index: int, required: tuple[str, ...]) -> dict[str, Any]:
    if not isinstance(row, dict):
        raise ValueError(f"{section}[{index}]: expected object")
    missing = [key for key in required if not row.get(key)]
    if missing:
        raise ValueError(f"{section}[{index}]: missing {', '.join(missing)}")
    return row


def _validate_manifest(payload: dict[str, Any]) -> None:
    for index, row in enumerate(_as_list(payload.get("core_etfs"))):
        _validate_candidate(row, "core_etfs", index, ("symbol", "name", "listing", "benchmark", "status"))
    for index, row in enumerate(_as_list(payload.get("korea_listed_etfs_to_verify"))):
        _validate_candidate(row, "korea_listed_etfs_to_verify", index, ("symbol", "name", "listing", "benchmark", "status"))
    for index, row in enumerate(_as_list(payload.get("satellite_etfs_to_verify"))):
        _validate_candidate(row, "satellite_etfs_to_verify", index, ("symbol", "name", "listing", "benchmark", "status"))
    satellite = payload.get("satellite_equities") or {}
    if not isinstance(satellite, dict):
        raise ValueError("satellite_equities: expected object")
    for queue_name in ("primary_queue", "secondary_queue"):
        for index, row in enumerate(_as_list(satellite.get(queue_name))):
            _validate_candidate(row, f"satellite_equities.{queue_name}", index, ("symbol", "name", "market", "status"))


def _table(headers: list[str], rows: list[list[Any]]) -> list[str]:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(_display(value).replace("\n", " ") for value in row) + " |")
    return lines


def _render_policy(payload: dict[str, Any]) -> list[str]:
    frame = payload.get("portfolio_frame") or {}
    guardrails = frame.get("guardrails") or {}
    priority = _as_list(frame.get("priority_order"))
    lines = [
        "## Portfolio Frame",
        "",
        f"- Strategy: `{_display(frame.get('name'))}`",
        f"- Horizon: `{_display(frame.get('horizon'))}`",
        "- Status: research queue only, not a buy list",
        "",
        "### Priority Order",
        "",
    ]
    lines.extend(f"{idx}. {_display(item)}" for idx, item in enumerate(priority, start=1))
    lines.extend(
        [
            "",
            "### Guardrails",
            "",
            *[
                f"- {key}: `{_display(value)}`"
                for key, value in guardrails.items()
                if key != "exclude_from_long_term_core"
            ],
        ]
    )
    excluded = _as_list(guardrails.get("exclude_from_long_term_core"))
    if excluded:
        lines.extend(["", "Excluded from long-term core:"])
        lines.extend(f"- {_display(item)}" for item in excluded)
    return lines


def _render_etfs(payload: dict[str, Any]) -> list[str]:
    rows = []
    for row in _as_list(payload.get("core_etfs")):
        rows.append(
            [
                row.get("symbol"),
                row.get("name"),
                row.get("listing"),
                row.get("role"),
                row.get("benchmark"),
                row.get("currency_hedge"),
                row.get("distribution_policy"),
                row.get("expense_ratio"),
                row.get("status"),
            ]
        )
    lines = ["## Core ETF Candidates", ""]
    lines.extend(
        _table(
            ["Symbol", "Name", "Listing", "Role", "Benchmark", "FX hedge", "Distribution", "Expense", "Status"],
            rows,
        )
    )
    lines.extend(["", "## Korea-Listed ETF Verification Queue", ""])
    domestic_rows = []
    for row in _as_list(payload.get("korea_listed_etfs_to_verify")):
        domestic_rows.append(
            [
                row.get("symbol"),
                row.get("name"),
                row.get("benchmark"),
                row.get("currency_hedge"),
                row.get("distribution_policy"),
                row.get("tax_account_fit"),
                row.get("status"),
            ]
        )
    lines.extend(
        _table(
            ["Code", "Name", "Benchmark", "FX hedge", "Distribution", "Tax/account check", "Status"],
            domestic_rows,
        )
    )
    lines.extend(["", "## Satellite ETF Verification Queue", ""])
    satellite_rows = []
    for row in _as_list(payload.get("satellite_etfs_to_verify")):
        satellite_rows.append(
            [
                row.get("symbol"),
                row.get("name"),
                row.get("listing"),
                row.get("role"),
                row.get("benchmark"),
                row.get("tax_account_fit"),
                row.get("status"),
            ]
        )
    lines.extend(
        _table(
            ["Symbol", "Name", "Listing", "Role", "Benchmark", "Tax/account check", "Status"],
            satellite_rows,
        )
    )
    return lines


def _render_satellites(payload: dict[str, Any]) -> list[str]:
    satellite = payload.get("satellite_equities") or {}
    lines = ["## Satellite Equity Queue", ""]
    for queue_name, title in (("primary_queue", "Primary Queue"), ("secondary_queue", "Secondary Queue")):
        rows = []
        for row in _as_list(satellite.get(queue_name)):
            rows.append(
                [
                    row.get("symbol"),
                    row.get("name"),
                    row.get("market"),
                    row.get("role"),
                    row.get("filings_to_read"),
                    row.get("status"),
                    row.get("notes"),
                ]
            )
        lines.extend([f"### {title}", ""])
        lines.extend(_table(["Symbol", "Name", "Market", "Role", "Filings", "Status", "First read"], rows))
        lines.append("")
    return lines


def _render_manual_checks(payload: dict[str, Any]) -> list[str]:
    checks = payload.get("manual_checks_before_buy") or {}
    lines = ["## Manual Checks Before Buy", ""]
    for section in ("etf", "stock"):
        values = _as_list(checks.get(section))
        lines.extend([f"### {section.upper()}", ""])
        lines.extend(f"- {_display(item)}" for item in values)
        lines.append("")
    return lines


def render_report(payload: dict[str, Any], *, candidate_file: Path, run_date: str) -> str:
    _validate_manifest(payload)
    lines = [
        "# DI Core ETF and Satellite Candidate Comparison",
        "",
        f"- Run date: `{run_date}`",
        f"- Candidate manifest: `{candidate_file.as_posix()}`",
        f"- Manifest version: `{_display(payload.get('version'))}`",
        "- Interpretation: candidate screening aid only; final buy decisions require a written thesis and tax/account verification",
        "",
    ]
    for block in (_render_policy(payload), _render_etfs(payload), _render_satellites(payload), _render_manual_checks(payload)):
        lines.extend(block)
        lines.append("")
    lines.extend(
        [
            "## Next Actions",
            "",
            "1. Fill issuer page, factsheet, expense, AUM, spread, NAV gap, and distribution fields for each ETF.",
            "2. Compare domestic-listed S&P 500 ETFs against US-direct VOO/VTI/VT using the same tax assumptions.",
            "3. For each satellite stock, run SEC EDGAR collection before writing thesis/valuation/decision notes.",
            "4. Move only approved candidates into `_report/di/watchlist.yaml` after a decision note exists.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Render DI ETF and satellite candidate comparison from YAML.")
    parser.add_argument("--candidate-file", type=Path, default=DEFAULT_CANDIDATE_FILE)
    parser.add_argument("--run-date", default=_now_kst().date().isoformat())
    parser.add_argument("--output", type=Path, help="Markdown report output path. Prints to stdout when omitted.")
    args = parser.parse_args()

    try:
        payload = _load_yaml(args.candidate_file)
        report = render_report(payload, candidate_file=args.candidate_file, run_date=args.run_date)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(report, encoding="utf-8")
    else:
        print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
