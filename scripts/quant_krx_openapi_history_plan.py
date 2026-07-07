"""Plan missing KRX OpenAPI raw collection across a date range.

The planner is local-only. It does not call KRX, read auth keys, or create a
Point-in-Time Universe. Its job is to turn a bounded date range into missing
collector requests, skipping already-saved raw files.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from quant_io import write_json_lf, write_text_lf
from quant_krx_openapi_collect import CORE_SERVICES, SERVICES, _now_kst, _raw_output_path, _validate_bas_dd, _validate_capture_date


@dataclass(frozen=True)
class PlannedRequest:
    bas_dd: str
    service_id: str
    raw_output: Path


def _parse_bas_dd(value: str) -> datetime:
    _validate_bas_dd(value)
    return datetime.strptime(value, "%Y%m%d")


def _date_range(start: str, end: str, include_weekends: bool) -> list[str]:
    start_dt = _parse_bas_dd(start)
    end_dt = _parse_bas_dd(end)
    if start_dt > end_dt:
        raise ValueError("start must be on or before end")

    dates: list[str] = []
    current = start_dt
    while current <= end_dt:
        if include_weekends or current.weekday() < 5:
            dates.append(current.strftime("%Y%m%d"))
        current += timedelta(days=1)
    return dates


def _selected_services(values: list[str]) -> list[str]:
    return values or list(CORE_SERVICES)


def _weekday_name(bas_dd: str) -> str:
    return _parse_bas_dd(bas_dd).strftime("%A")


def _request_for(raw_root: Path, capture_date: str, service_id: str, bas_dd: str) -> PlannedRequest:
    return PlannedRequest(
        bas_dd=bas_dd,
        service_id=service_id,
        raw_output=_raw_output_path(raw_root, capture_date, service_id, bas_dd),
    )


def build_plan(
    *,
    start: str,
    end: str,
    capture_date: str,
    raw_root: Path,
    services: list[str],
    include_weekends: bool = False,
) -> dict[str, Any]:
    selected_services = _selected_services(services)
    for service_id in selected_services:
        if service_id not in SERVICES:
            raise ValueError(f"unsupported service id: {service_id}")

    date_rows: list[dict[str, Any]] = []
    existing_raw_files = 0
    missing_requests: list[PlannedRequest] = []

    for bas_dd in _date_range(start, end, include_weekends):
        existing_services: list[str] = []
        missing_services: list[str] = []
        requests: list[PlannedRequest] = []
        for service_id in selected_services:
            request = _request_for(raw_root, capture_date, service_id, bas_dd)
            if request.raw_output.exists():
                existing_services.append(service_id)
                existing_raw_files += 1
            else:
                missing_services.append(service_id)
                requests.append(request)
                missing_requests.append(request)

        date_rows.append(
            {
                "bas_dd": bas_dd,
                "weekday": _weekday_name(bas_dd),
                "complete": not missing_services,
                "existing_services": existing_services,
                "missing_services": missing_services,
                "requests": [
                    {
                        "service_id": request.service_id,
                        "raw_output": request.raw_output.as_posix(),
                    }
                    for request in requests
                ],
            }
        )

    return {
        "plan_type": "krx_openapi_history_missing_raw",
        "capture_date": capture_date,
        "start": start,
        "end": end,
        "include_weekends": include_weekends,
        "services": selected_services,
        "totals": {
            "candidate_dates": len(date_rows),
            "complete_dates": sum(1 for row in date_rows if row["complete"]),
            "existing_raw_files": existing_raw_files,
            "missing_requests": len(missing_requests),
        },
        "dates": date_rows,
    }


def _write_json(path: Path, payload: Any) -> None:
    write_json_lf(path, payload)


def _wikilink(path: str | Path) -> str:
    rendered = path.as_posix() if isinstance(path, Path) else path
    return f"[[{rendered}|{rendered}]]"


def _render_markdown(plan: dict[str, Any], output_json: Path | None) -> str:
    totals = plan["totals"]
    lines = [
        "# KRX OpenAPI Historical Collection Plan",
        "",
        "- Plan type: `krx_openapi_history_missing_raw`",
        f"- Date range: `{plan['start']}` to `{plan['end']}`",
        f"- Capture date: `{plan['capture_date']}`",
        f"- Include weekends: `{str(plan['include_weekends']).lower()}`",
        "- Interpretation: local missing-raw plan only, not a `Point-in-Time Universe` or `Backtest` result",
        "",
        "## Totals",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| Candidate dates | {totals['candidate_dates']} |",
        f"| Complete dates | {totals['complete_dates']} |",
        f"| Existing raw files | {totals['existing_raw_files']} |",
        f"| Missing requests | {totals['missing_requests']} |",
        "",
    ]
    if output_json is not None:
        lines.extend(["## JSON Plan", "", f"- {_wikilink(output_json)}", ""])

    lines.extend(
        [
            "## Date Plan",
            "",
            "| bas_dd | Weekday | Complete | Missing services |",
            "| --- | --- | --- | --- |",
        ]
    )
    for row in plan["dates"]:
        missing = ", ".join(f"`{service_id}`" for service_id in row["missing_services"]) or "-"
        lines.append(f"| `{row['bas_dd']}` | {row['weekday']} | `{str(row['complete']).lower()}` | {missing} |")

    lines.extend(
        [
            "",
            "## Guardrails",
            "",
            "- Weekend filtering is not a KRX trading-calendar guarantee; holidays can still produce zero-row raws.",
            "- The collector should still save raw responses and metadata for every attempted date.",
            "- Backtest readiness remains `hold` until `Point-in-Time` status replay and historical coverage are validated.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Plan missing KRX OpenAPI raw collection across a date range.")
    parser.add_argument("--start", required=True, type=_validate_bas_dd, help="Start date in YYYYMMDD form.")
    parser.add_argument("--end", required=True, type=_validate_bas_dd, help="End date in YYYYMMDD form.")
    parser.add_argument("--service", action="append", choices=tuple(SERVICES), default=[], help="Service id to plan. Repeatable. Defaults to core 6 services.")
    parser.add_argument("--raw-root", type=Path, default=Path("_report/raw"))
    parser.add_argument("--capture-date", type=_validate_capture_date, default=_now_kst().date().isoformat())
    parser.add_argument("--include-weekends", action="store_true")
    parser.add_argument("--output", type=Path, help="Optional JSON output path.")
    parser.add_argument("--report-output", type=Path, help="Optional Markdown report output path.")
    args = parser.parse_args()

    try:
        plan = build_plan(
            start=args.start,
            end=args.end,
            capture_date=args.capture_date,
            raw_root=args.raw_root,
            services=args.service,
            include_weekends=args.include_weekends,
        )
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc

    if args.output:
        _write_json(args.output, plan)
    if args.report_output:
        write_text_lf(args.report_output, _render_markdown(plan, args.output))
    if not args.output and not args.report_output:
        print(json.dumps(plan, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
