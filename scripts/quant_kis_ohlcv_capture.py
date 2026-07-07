"""Execute a small KIS OHLCV request queue and save raw JSON responses.

This script is intentionally queue-based and resumable. It reads JSONL rows
created by `quant_kis_ohlcv_batch_plan.py`, calls the read-only KIS daily OHLCV
endpoint, and writes raw responses under `_report/raw/**`.

The default `--dry-run` mode does not import KIS auth code or call the network.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from quant_io import write_json_lf, write_text_lf


API_TYPE = "inquire_daily_itemchartprice"
API_PATH = "/uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice"
TR_ID = "FHKST03010100"
REQUIRED_PARAMS = (
    "env_dv",
    "fid_cond_mrkt_div_code",
    "fid_input_iscd",
    "fid_input_date_1",
    "fid_input_date_2",
    "fid_period_div_code",
    "fid_org_adj_prc",
)
KIS_PARAM_MAP = {
    "fid_cond_mrkt_div_code": "FID_COND_MRKT_DIV_CODE",
    "fid_input_iscd": "FID_INPUT_ISCD",
    "fid_input_date_1": "FID_INPUT_DATE_1",
    "fid_input_date_2": "FID_INPUT_DATE_2",
    "fid_period_div_code": "FID_PERIOD_DIV_CODE",
    "fid_org_adj_prc": "FID_ORG_ADJ_PRC",
}


@dataclass(frozen=True)
class CaptureResult:
    code: str
    name: str
    status: str
    output_file: str
    message: str


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _read_queue(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            text = line.strip()
            if not text:
                continue
            try:
                row = json.loads(text)
            except json.JSONDecodeError as exc:
                raise ValueError(f"invalid JSONL at line {line_number}: {exc}") from exc
            rows.append(row)
    if not rows:
        raise ValueError(f"request queue has no rows: {path}")
    return rows


def _validate_queue_row(row: dict[str, Any]) -> None:
    if row.get("tool") != "domestic_stock":
        raise ValueError(f"unsupported tool for code {row.get('code')}: {row.get('tool')}")
    if row.get("api_type") != API_TYPE:
        raise ValueError(f"unsupported api_type for code {row.get('code')}: {row.get('api_type')}")
    params = row.get("params")
    if not isinstance(params, dict):
        raise ValueError(f"missing params for code {row.get('code')}")
    missing = [name for name in REQUIRED_PARAMS if not params.get(name)]
    if missing:
        raise ValueError(f"missing required params for code {row.get('code')}: {', '.join(missing)}")


def _select_rows(rows: list[dict[str, Any]], offset: int, limit: int | None) -> list[dict[str, Any]]:
    if offset < 0:
        raise ValueError("offset must be zero or greater")
    if limit is not None and limit < 0:
        raise ValueError("limit must be zero or greater")
    return rows[offset : None if limit is None else offset + limit]


def _load_kis_auth(repo_root: Path) -> Any:
    examples_dir = repo_root / "examples_llm"
    if str(examples_dir) not in sys.path:
        sys.path.insert(0, str(examples_dir))
    import kis_auth as ka  # type: ignore

    return ka


def _kis_params(params: dict[str, str]) -> dict[str, str]:
    return {target: str(params[source]) for source, target in KIS_PARAM_MAP.items()}


def _response_json(response: Any) -> dict[str, Any]:
    if hasattr(response, "getResponse"):
        raw_response = response.getResponse()
        if hasattr(raw_response, "json"):
            return raw_response.json()
    body = response.getBody()
    if hasattr(body, "_asdict"):
        return dict(body._asdict())
    raise ValueError("could not extract JSON from KIS response")


def _yaml_scalar(value: str | int | float | bool | None) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    return json.dumps(value, ensure_ascii=False)


def _write_manifest(
    raw_dir: Path,
    queue_path: Path,
    results: list[CaptureResult],
    started_at: str,
    finished_at: str,
    dry_run: bool,
) -> None:
    status_counts: dict[str, int] = {}
    for result in results:
        status_counts[result.status] = status_counts.get(result.status, 0) + 1

    lines = [
        "schema_version: 1",
        "purpose: quant_universe_ohlcv_batch_capture",
        "source: kis_openapi_direct_queue_capture",
        "api_type: inquire_daily_itemchartprice",
        "tool_group: domestic_stock",
        "preflight: local_api_detail_from_MCP_Kis_Trading_MCP_configs_domestic_stock_json",
        f"dry_run: {_yaml_scalar(dry_run)}",
        f"started_at_utc: {_yaml_scalar(started_at)}",
        f"finished_at_utc: {_yaml_scalar(finished_at)}",
        f"queue_path: {_yaml_scalar(queue_path.as_posix())}",
        f"raw_dir: {_yaml_scalar(raw_dir.as_posix())}",
        "status_counts:",
    ]
    for status, count in sorted(status_counts.items()):
        lines.append(f"  {status}: {count}")
    lines.append("files:")
    for result in results:
        lines.extend(
            [
                f"  - code: {_yaml_scalar(result.code)}",
                f"    name: {_yaml_scalar(result.name)}",
                f"    status: {_yaml_scalar(result.status)}",
                f"    output_file: {_yaml_scalar(result.output_file)}",
                f"    message: {_yaml_scalar(result.message)}",
            ]
        )
    write_text_lf(raw_dir / "manifest.yaml", "\n".join(lines) + "\n")


def execute_capture(
    queue_rows: list[dict[str, Any]],
    queue_path: Path,
    raw_dir: Path,
    dry_run: bool,
    skip_existing: bool,
    sleep_seconds: float,
    stop_on_error: bool,
) -> list[CaptureResult]:
    raw_dir.mkdir(parents=True, exist_ok=True)
    started_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    results: list[CaptureResult] = []
    ka = None if dry_run else _load_kis_auth(_repo_root())
    authenticated_env: str | None = None

    for row in queue_rows:
        _validate_queue_row(row)
        code = str(row["code"])
        name = str(row.get("name", ""))
        output_file = str(row.get("output_file") or f"{code}.daily.raw.json")
        output_path = raw_dir / output_file

        if skip_existing and output_path.exists():
            results.append(CaptureResult(code, name, "skipped_existing", output_file, "raw file already exists"))
            continue

        params = row["params"]
        env_dv = str(params["env_dv"])
        if dry_run:
            results.append(CaptureResult(code, name, "dry_run", output_file, "validated queue row only"))
            continue

        try:
            if authenticated_env != env_dv:
                ka.auth("vps" if env_dv == "demo" else "prod")
                authenticated_env = env_dv
            response = ka._url_fetch(API_PATH, TR_ID, "", _kis_params(params))
            payload = _response_json(response)
            write_json_lf(output_path, payload, sort_keys=True)
            if response.isOK():
                results.append(CaptureResult(code, name, "saved", output_file, "ok"))
            else:
                message = f"{response.getErrorCode()} {response.getErrorMessage()}".strip()
                results.append(CaptureResult(code, name, "api_error_saved", output_file, message))
                if stop_on_error:
                    break
        except Exception as exc:
            results.append(CaptureResult(code, name, "error", output_file, str(exc)))
            if stop_on_error:
                break
        if sleep_seconds > 0:
            time.sleep(sleep_seconds)

    finished_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    _write_manifest(raw_dir, queue_path, results, started_at, finished_at, dry_run)
    return results


def render_markdown(results: list[CaptureResult], queue_path: Path, raw_dir: Path, dry_run: bool) -> str:
    counts: dict[str, int] = {}
    for result in results:
        counts[result.status] = counts.get(result.status, 0) + 1

    lines = [
        "# KIS OHLCV Queue Capture Result",
        "",
        f"- Request queue: `{queue_path.as_posix()}`",
        f"- Raw directory: `{raw_dir.as_posix()}`",
        f"- Dry run: `{'true' if dry_run else 'false'}`",
        "- API type: `inquire_daily_itemchartprice`",
        "- Tool group: `domestic_stock`",
        "- MCP preflight status: `tool_unavailable_in_current_codex_app_surface`",
        "- Local API detail fallback: `MCP/Kis Trading MCP/configs/domestic_stock.json` + `examples_llm` sample",
        "- Execution path: `direct_kis_openapi_sample_auth` / read-only quotation endpoint",
        "- Interpretation: `current_snapshot` / `paper-smoke`; not Backtest evidence",
        "",
        "## Status Counts",
        "",
        "| Status | Count |",
        "| --- | ---: |",
    ]
    for status, count in sorted(counts.items()):
        lines.append(f"| `{status}` | {count} |")

    lines.extend(
        [
            "",
            "## Rows",
            "",
            "| Code | Company | Status | Output File | Message |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for result in results:
        lines.append(
            f"| `{result.code}` | {result.name} | `{result.status}` | `{result.output_file}` | {result.message} |"
        )

    lines.extend(
        [
            "",
            "## Guardrails",
            "",
            "- Raw responses are stored under `_report/raw/**` and should not be committed.",
            "- Re-run `scripts/quant_liquidity_filter.py` only after non-dry-run raw files are saved.",
            "- `api_error_saved` means the raw error response was preserved for diagnosis, not that the stock failed the Liquidity Filter.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Execute a KIS OHLCV JSONL request queue and save raw responses.")
    parser.add_argument("--queue", required=True, type=Path)
    parser.add_argument("--raw-dir", required=True, type=Path)
    parser.add_argument("--offset", default=0, type=int)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--skip-existing", action="store_true")
    parser.add_argument("--sleep-seconds", default=0.2, type=float)
    parser.add_argument("--stop-on-error", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    if not args.queue.exists():
        raise SystemExit(f"request queue not found: {args.queue}")
    try:
        rows = _select_rows(_read_queue(args.queue), args.offset, args.limit)
        results = execute_capture(
            rows,
            args.queue,
            args.raw_dir,
            args.dry_run,
            args.skip_existing,
            args.sleep_seconds,
            args.stop_on_error,
        )
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc

    report = render_markdown(results, args.queue, args.raw_dir, args.dry_run)
    if args.output:
        write_text_lf(args.output, report)
    else:
        print(report, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
