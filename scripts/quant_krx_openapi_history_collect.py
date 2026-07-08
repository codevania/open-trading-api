"""Collect KRX OpenAPI raws from a historical collection plan.

The collector reads the JSON plan produced by quant_krx_openapi_history_plan.py
and saves official KRX OpenAPI raw responses. It redacts the auth key in all
tracked outputs and keeps the result as market-data evidence only.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

try:
    from quant_io import write_text_lf
except ModuleNotFoundError:  # pragma: no cover - used when imported as scripts.* in tests.
    from scripts.quant_io import write_text_lf

try:
    from quant_krx_openapi_collect import SERVICES, _collect_one, _decode_json, _raw_output_path, _resolve_auth_key, _row_info
except ModuleNotFoundError:  # pragma: no cover - used when imported as scripts.* in tests.
    from scripts.quant_krx_openapi_collect import SERVICES, _collect_one, _decode_json, _raw_output_path, _resolve_auth_key, _row_info


@dataclass(frozen=True)
class PlannedCollectionRequest:
    bas_dd: str
    service_id: str


Collector = Callable[[str, str], dict[str, Any]]
ExistingRawReader = Callable[[str, str], dict[str, Any] | None]


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _planned_requests(plan: dict[str, Any]) -> list[PlannedCollectionRequest]:
    if plan.get("plan_type") != "krx_openapi_history_missing_raw":
        raise ValueError("plan_type must be krx_openapi_history_missing_raw")
    requests: list[PlannedCollectionRequest] = []
    for date_row in plan.get("dates", []):
        bas_dd = str(date_row.get("bas_dd", "")).strip()
        for item in date_row.get("requests", []):
            service_id = str(item.get("service_id", "")).strip()
            if not bas_dd or not service_id:
                raise ValueError("plan contains a request without bas_dd or service_id")
            if service_id not in SERVICES:
                raise ValueError(f"unsupported service id in plan: {service_id}")
            requests.append(PlannedCollectionRequest(bas_dd=bas_dd, service_id=service_id))
    return requests


def _existing_requests(plan: dict[str, Any]) -> list[PlannedCollectionRequest]:
    if plan.get("plan_type") != "krx_openapi_history_missing_raw":
        raise ValueError("plan_type must be krx_openapi_history_missing_raw")
    requests: list[PlannedCollectionRequest] = []
    for date_row in plan.get("dates", []):
        bas_dd = str(date_row.get("bas_dd", "")).strip()
        for service_id_value in date_row.get("existing_services", []):
            service_id = str(service_id_value).strip()
            if not bas_dd or not service_id:
                raise ValueError("plan contains an existing service without bas_dd or service_id")
            if service_id not in SERVICES:
                raise ValueError(f"unsupported existing service id in plan: {service_id}")
            requests.append(PlannedCollectionRequest(bas_dd=bas_dd, service_id=service_id))
    return requests


def _result_row(request: PlannedCollectionRequest, meta: dict[str, Any], result_source: str) -> dict[str, Any]:
    return {
        "result_source": result_source,
        "bas_dd": request.bas_dd,
        "service_id": request.service_id,
        "status_code": meta.get("status_code"),
        "row_count": meta.get("row_count"),
        "raw_output": meta.get("raw_output"),
    }


def collect_from_plan(
    *,
    plan: dict[str, Any],
    collector: Collector,
    existing_reader: ExistingRawReader | None = None,
    limit: int | None = None,
) -> dict[str, Any]:
    planned = _planned_requests(plan)
    existing = _existing_requests(plan)
    if limit is not None:
        if limit <= 0:
            raise ValueError("limit must be positive")
        planned = planned[:limit]

    results: list[dict[str, Any]] = []
    failures: list[dict[str, str]] = []
    existing_results: list[dict[str, Any]] = []
    existing_failures: list[dict[str, str]] = []
    if existing_reader is not None:
        for request in existing:
            try:
                meta = existing_reader(request.bas_dd, request.service_id)
            except Exception as exc:  # pragma: no cover - CLI keeps resumability evidence on local read failures.
                existing_failures.append(
                    {"bas_dd": request.bas_dd, "service_id": request.service_id, "error": str(exc)}
                )
                continue
            if meta is None:
                existing_failures.append(
                    {
                        "bas_dd": request.bas_dd,
                        "service_id": request.service_id,
                        "error": "existing raw file referenced by plan was not found",
                    }
                )
                continue
            existing_results.append(_result_row(request, meta, "existing"))

    for request in planned:
        try:
            meta = collector(request.bas_dd, request.service_id)
        except Exception as exc:  # pragma: no cover - CLI keeps partial evidence on external failures.
            failures.append({"bas_dd": request.bas_dd, "service_id": request.service_id, "error": str(exc)})
            continue
        results.append(_result_row(request, meta, "collected"))

    available_results = sorted(
        [*existing_results, *results],
        key=lambda item: (str(item.get("bas_dd", "")), str(item.get("service_id", "")), str(item.get("result_source", ""))),
    )

    return {
        "plan_type": plan.get("plan_type"),
        "capture_date": plan.get("capture_date"),
        "start": plan.get("start"),
        "end": plan.get("end"),
        "planned_requests": len(_planned_requests(plan)),
        "planned_existing_requests": len(existing),
        "attempted_requests": len(planned),
        "successful_requests": len(results),
        "verified_existing_requests": len(existing_results),
        "unverified_existing_requests": len(existing_failures),
        "available_raw_requests": len(available_results),
        "failed_requests": len(failures),
        "results": results,
        "existing_results": existing_results,
        "available_results": available_results,
        "failures": failures,
        "existing_failures": existing_failures,
        "guardrails": {
            "auth_key_redacted": True,
            "backtest_readiness": "hold",
            "live_trading_readiness": "blocked",
        },
    }


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def _read_existing_raw(raw_root: Path, capture_date: str, bas_dd: str, service_id: str) -> dict[str, Any] | None:
    output = _raw_output_path(raw_root, capture_date, service_id, bas_dd)
    if not output.exists():
        return None

    meta_path = output.with_name(f"{output.name}.meta.json")
    if meta_path.exists():
        meta = _read_json(meta_path)
        return {
            "status_code": meta.get("status_code"),
            "row_count": meta.get("row_count"),
            "raw_output": meta.get("raw_output") or output.as_posix(),
        }

    payload = _decode_json(output.read_bytes())
    row_count, _row_keys = _row_info(payload)
    return {"status_code": None, "row_count": row_count, "raw_output": output.as_posix()}


def _wikilink(path: Path) -> str:
    rendered = path.as_posix()
    return f"[[{rendered}|{rendered}]]"


def _render_report(summary: dict[str, Any], plan_path: Path, output_json: Path | None) -> str:
    lines = [
        "# KRX OpenAPI Historical Collection Result",
        "",
        f"- Plan: {_wikilink(plan_path)}",
        f"- Date range: `{summary['start']}` to `{summary['end']}`",
        f"- Capture date: `{summary['capture_date']}`",
        "- Interpretation: official raw market-data collection only, not a `Point-in-Time Universe` or `Backtest` result",
        "- AUTH_KEY stored in report: `false`",
        "- Backtest readiness: `hold`",
        "- Live trading readiness: `blocked`",
    ]
    if output_json:
        lines.append(f"- Machine-readable result: {_wikilink(output_json)}")

    lines.extend(
        [
            "",
            "## Totals",
            "",
            "| Metric | Value |",
            "| --- | ---: |",
            f"| Missing requests in plan | {summary['planned_requests']} |",
            f"| Attempted missing requests | {summary['attempted_requests']} |",
            f"| Newly successful requests | {summary['successful_requests']} |",
            f"| Existing raw requests in plan | {summary.get('planned_existing_requests', 0)} |",
            f"| Verified existing raw requests | {summary.get('verified_existing_requests', 0)} |",
            f"| Unverified existing raw requests | {summary.get('unverified_existing_requests', 0)} |",
            f"| Available raw requests | {summary.get('available_raw_requests', summary['successful_requests'])} |",
            f"| Failed new requests | {summary['failed_requests']} |",
            "",
            "## Row Counts",
            "",
            "| Source | bas_dd | Service | HTTP | Rows | Raw output |",
            "| --- | --- | --- | ---: | ---: | --- |",
        ]
    )
    row_count_items = summary.get("available_results", summary["results"])
    for item in row_count_items:
        raw_output = item.get("raw_output") or ""
        lines.append(
            f"| `{item.get('result_source', 'collected')}` | `{item['bas_dd']}` | `{item['service_id']}` | {item.get('status_code', '')} | "
            f"{item.get('row_count', '')} | {_wikilink(Path(raw_output)) if raw_output else ''} |"
        )
    if not row_count_items:
        lines.append("| `none` | `none` | `none` |  |  |  |")

    lines.extend(["", "## Failures", "", "| Source | bas_dd | Service | Error |", "| --- | --- | --- | --- |"])
    for item in summary["failures"]:
        lines.append(f"| `collected` | `{item['bas_dd']}` | `{item['service_id']}` | {item['error']} |")
    for item in summary.get("existing_failures", []):
        lines.append(f"| `existing` | `{item['bas_dd']}` | `{item['service_id']}` | {item['error']} |")
    if not summary["failures"] and not summary.get("existing_failures", []):
        lines.append("| `none` | `none` | `none` |  |")

    lines.extend(
        [
            "",
            "## Guardrails",
            "",
            "- This collector stores raw KRX OpenAPI responses and redacted metadata only.",
            "- This does not solve historical managed issue, trading halt, or delisting status coverage.",
            "- Backtest readiness remains `hold` until status coverage, cost model, benchmark, OOS, and Bias Control pass.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect KRX OpenAPI raws from a historical collection plan.")
    parser.add_argument("--plan", required=True, type=Path)
    parser.add_argument("--raw-root", type=Path, default=Path("_report/raw"))
    parser.add_argument("--env-file", type=Path, default=Path(".env.krx"))
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--report-output", type=Path)
    args = parser.parse_args()

    try:
        plan = _read_json(args.plan)
        capture_date = str(plan.get("capture_date", "")).strip()
        if not capture_date:
            raise ValueError("plan is missing capture_date")
        auth_key = _resolve_auth_key(args.env_file)

        def collector(bas_dd: str, service_id: str) -> dict[str, Any]:
            return _collect_one(SERVICES[service_id], bas_dd, args.raw_root, capture_date, auth_key, args.timeout)

        def existing_reader(bas_dd: str, service_id: str) -> dict[str, Any] | None:
            return _read_existing_raw(args.raw_root, capture_date, bas_dd, service_id)

        summary = collect_from_plan(plan=plan, collector=collector, existing_reader=existing_reader, limit=args.limit)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc

    if args.output:
        _write_json(args.output, summary)
    report = _render_report(summary, args.plan, args.output)
    if args.report_output:
        write_text_lf(args.report_output, report)
    else:
        print(report, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
