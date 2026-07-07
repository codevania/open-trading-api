"""Create a KIS OHLCV batch request plan from current Universe rows.

This script does not call KIS. It creates a deterministic request queue for
`domestic_stock.inquire_daily_itemchartprice` so a separate MCP/manual capture
step can execute the requests after API-detail preflight.
"""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from quant_io import write_text_lf


API_TYPE = "inquire_daily_itemchartprice"
DEFAULT_API_CONFIG = Path("MCP/Kis Trading MCP/configs/domestic_stock.json")
DEFAULT_ENV_DV = "real"
DEFAULT_MARKET_CODE = "J"
DEFAULT_PERIOD_DIV_CODE = "D"
DEFAULT_ORG_ADJ_PRC = "0"
REQUIRED_PARAMS = (
    "env_dv",
    "fid_cond_mrkt_div_code",
    "fid_input_iscd",
    "fid_input_date_1",
    "fid_input_date_2",
    "fid_period_div_code",
    "fid_org_adj_prc",
)


@dataclass(frozen=True)
class UniverseIssue:
    code: str
    name: str
    market: str
    status: str
    reason: str


@dataclass(frozen=True)
class BatchRequest:
    sequence: int
    code: str
    name: str
    market: str
    api_type: str
    params: dict[str, str]
    output_file: str


def _read_universe(path: Path) -> list[UniverseIssue]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ValueError(f"universe CSV has no rows: {path}")
    required = {"code", "name", "market", "status", "reason"}
    missing = required - set(rows[0])
    if missing:
        raise ValueError(f"universe CSV missing required columns: {', '.join(sorted(missing))}")
    return [
        UniverseIssue(
            str(row.get("code", "")).strip().upper(),
            str(row.get("name", "")).strip(),
            str(row.get("market", "")).strip(),
            str(row.get("status", "")).strip(),
            str(row.get("reason", "")).strip(),
        )
        for row in rows
    ]


def _load_api_detail(config_path: Path) -> dict[str, Any]:
    config = json.loads(config_path.read_text(encoding="utf-8"))
    try:
        detail = config["apis"][API_TYPE]
    except KeyError as exc:
        raise ValueError(f"{API_TYPE} not found in API config: {config_path}") from exc
    params = detail.get("params") or {}
    missing = [name for name in REQUIRED_PARAMS if name not in params]
    if missing:
        raise ValueError(f"{API_TYPE} API detail missing params: {', '.join(missing)}")
    return detail


def _existing_raw_codes(raw_dir: Path) -> set[str]:
    if not raw_dir.exists():
        return set()
    codes: set[str] = set()
    for path in raw_dir.glob("*.daily.raw.json"):
        codes.add(path.name[: -len(".daily.raw.json")].upper())
    for path in raw_dir.glob("*/inquire_daily_itemchartprice.json"):
        codes.add(path.parent.name.upper())
    return codes


def build_requests(
    issues: list[UniverseIssue],
    raw_dir: Path,
    start_date: str,
    end_date: str,
    env_dv: str,
    market_code: str,
    period_div_code: str,
    org_adj_prc: str,
    offset: int,
    limit: int | None,
    skip_existing: bool,
) -> tuple[list[BatchRequest], dict[str, int]]:
    if offset < 0:
        raise ValueError("offset must be zero or greater")
    if limit is not None and limit < 0:
        raise ValueError("limit must be zero or greater")

    included = [issue for issue in issues if issue.status == "include"]
    existing_codes = _existing_raw_codes(raw_dir) if skip_existing else set()
    eligible = [issue for issue in included if issue.code not in existing_codes]
    selected = eligible[offset : None if limit is None else offset + limit]

    requests: list[BatchRequest] = []
    for sequence, issue in enumerate(selected, start=1):
        params = {
            "env_dv": env_dv,
            "fid_cond_mrkt_div_code": market_code,
            "fid_input_iscd": issue.code,
            "fid_input_date_1": start_date,
            "fid_input_date_2": end_date,
            "fid_period_div_code": period_div_code,
            "fid_org_adj_prc": org_adj_prc,
        }
        requests.append(
            BatchRequest(
                sequence=sequence,
                code=issue.code,
                name=issue.name,
                market=issue.market,
                api_type=API_TYPE,
                params=params,
                output_file=f"{issue.code}.daily.raw.json",
            )
        )

    counts = {
        "total_rows": len(issues),
        "base_included_rows": len(included),
        "preexisting_excluded_rows": len(issues) - len(included),
        "existing_raw_skipped": sum(1 for issue in included if issue.code in existing_codes),
        "eligible_after_skip": len(eligible),
        "selected_requests": len(requests),
    }
    return requests, counts


def write_jsonl(requests: list[BatchRequest], path: Path, raw_dir: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for request in requests:
            payload = {
                "sequence": request.sequence,
                "code": request.code,
                "name": request.name,
                "market": request.market,
                "tool": "domestic_stock",
                "api_type": request.api_type,
                "params": request.params,
                "raw_dir": raw_dir.as_posix(),
                "output_file": request.output_file,
            }
            handle.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")


def render_markdown(
    requests: list[BatchRequest],
    counts: dict[str, int],
    api_detail: dict[str, Any],
    universe_csv: Path,
    api_config: Path,
    raw_dir: Path,
    jsonl_output: Path | None,
    as_of_date: str,
    offset: int,
    limit: int | None,
    skip_existing: bool,
) -> str:
    lines = [
        "# KRX Current Universe v0 OHLCV Batch Plan",
        "",
        f"- As-of date: `{as_of_date}`",
        f"- Source Universe rows: `{universe_csv.as_posix()}`",
        f"- API detail source: `{api_config.as_posix()}`",
        "- MCP preflight status: `tool_unavailable_in_current_codex_app_surface`",
        "- Local API detail preflight: `pass`",
        "- Tool group: `domestic_stock`",
        f"- API type: `{API_TYPE}`",
        f"- API path: `{api_detail.get('api_path', '')}`",
        "- API note: one call returns up to `100` daily rows according to local KIS config/example docs.",
        f"- Raw output directory target: `{raw_dir.as_posix()}`",
        f"- Offset: `{offset}`",
        f"- Limit: `{'all' if limit is None else limit}`",
        f"- Skip existing raw: `{'true' if skip_existing else 'false'}`",
    ]
    if jsonl_output:
        lines.append(f"- Request queue JSONL: `{jsonl_output.as_posix()}`")

    lines.extend(
        [
            "",
            "## Required Params",
            "",
            "| Param | Description |",
            "| --- | --- |",
        ]
    )
    params = api_detail.get("params") or {}
    for name in REQUIRED_PARAMS:
        description = str((params.get(name) or {}).get("description", "")).replace("\n", " ")
        lines.append(f"| `{name}` | {description} |")

    lines.extend(
        [
            "",
            "## Summary",
            "",
            f"- Total Universe rows: `{counts['total_rows']}`",
            f"- Base included rows: `{counts['base_included_rows']}`",
            f"- Preexisting excluded rows: `{counts['preexisting_excluded_rows']}`",
            f"- Existing raw skipped: `{counts['existing_raw_skipped']}`",
            f"- Eligible after skip: `{counts['eligible_after_skip']}`",
            f"- Selected requests: `{counts['selected_requests']}`",
            "",
            "## Request Sample",
            "",
            "| Seq | Code | Company | Market | Start | End | Output File |",
            "| ---: | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for request in requests[:20]:
        lines.append(
            f"| {request.sequence} | `{request.code}` | {request.name} | {request.market} | "
            f"{request.params['fid_input_date_1']} | {request.params['fid_input_date_2']} | "
            f"`{request.output_file}` |"
        )

    lines.extend(
        [
            "",
            "## Guardrails",
            "",
            "- This plan does not call KIS and does not place orders.",
            "- Before live MCP execution, run `domestic_stock.find_api_detail` for `inquire_daily_itemchartprice` in a surface where the MCP tool is available.",
            "- Save raw responses under `_report/raw/**`; do not commit raw response files.",
            "- Use `--limit`, `--offset`, and `--skip-existing` for small resumable batches.",
            "- This is still `current_snapshot` / paper-smoke work, not a Point-in-Time Universe or Backtest.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a KIS OHLCV batch request plan from current Universe rows.")
    parser.add_argument("--universe-csv", required=True, type=Path)
    parser.add_argument("--api-config", default=DEFAULT_API_CONFIG, type=Path)
    parser.add_argument("--raw-dir", required=True, type=Path)
    parser.add_argument("--as-of-date", required=True)
    parser.add_argument("--start-date", required=True)
    parser.add_argument("--end-date", required=True)
    parser.add_argument("--env-dv", default=DEFAULT_ENV_DV)
    parser.add_argument("--market-code", default=DEFAULT_MARKET_CODE)
    parser.add_argument("--period-div-code", default=DEFAULT_PERIOD_DIV_CODE)
    parser.add_argument("--org-adj-prc", default=DEFAULT_ORG_ADJ_PRC)
    parser.add_argument("--offset", default=0, type=int)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--skip-existing", action="store_true")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--jsonl-output", type=Path)
    args = parser.parse_args()

    if not args.universe_csv.exists():
        raise SystemExit(f"universe CSV not found: {args.universe_csv}")
    if not args.api_config.exists():
        raise SystemExit(f"API config not found: {args.api_config}")

    try:
        issues = _read_universe(args.universe_csv)
        api_detail = _load_api_detail(args.api_config)
        requests, counts = build_requests(
            issues,
            args.raw_dir,
            args.start_date,
            args.end_date,
            args.env_dv,
            args.market_code,
            args.period_div_code,
            args.org_adj_prc,
            args.offset,
            args.limit,
            args.skip_existing,
        )
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc

    if args.jsonl_output:
        write_jsonl(requests, args.jsonl_output, args.raw_dir)

    report = render_markdown(
        requests,
        counts,
        api_detail,
        args.universe_csv,
        args.api_config,
        args.raw_dir,
        args.jsonl_output,
        args.as_of_date,
        args.offset,
        args.limit,
        args.skip_existing,
    )
    if args.output:
        write_text_lf(args.output, report)
    else:
        print(report, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
