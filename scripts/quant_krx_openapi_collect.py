"""Collect approved KRX OpenAPI core Quant raw datasets.

The collector saves official KRX OpenAPI responses as raw evidence only. It
does not normalize the rows into an investable Universe and does not upgrade
Backtest readiness beyond hold.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import requests

from quant_krx_openapi_probe import _resolve_auth_key


KST = ZoneInfo("Asia/Seoul")
BAS_DD_RE = re.compile(r"^\d{8}$")
CAPTURE_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


@dataclass(frozen=True)
class KrxOpenApiService:
    service_id: str
    title: str
    category: str
    endpoint: str
    official_page: str


SERVICES: dict[str, KrxOpenApiService] = {
    "kospi_stock_daily": KrxOpenApiService(
        service_id="kospi_stock_daily",
        title="유가증권 일별매매정보",
        category="stock",
        endpoint="https://data-dbg.krx.co.kr/svc/apis/sto/stk_bydd_trd",
        official_page="https://openapi.krx.co.kr/contents/OPP/USES/service/OPPUSES002_S2.cmd?BO_ID=JvJFzlAENzZlPBDNGAWC",
    ),
    "kosdaq_stock_daily": KrxOpenApiService(
        service_id="kosdaq_stock_daily",
        title="코스닥 일별매매정보",
        category="stock",
        endpoint="https://data-dbg.krx.co.kr/svc/apis/sto/ksq_bydd_trd",
        official_page="https://openapi.krx.co.kr/contents/OPP/USES/service/OPPUSES002_S2.cmd?BO_ID=hZjGpkllgCBCWqeTsYFj",
    ),
    "kospi_issue_base": KrxOpenApiService(
        service_id="kospi_issue_base",
        title="유가증권 종목기본정보",
        category="stock",
        endpoint="https://data-dbg.krx.co.kr/svc/apis/sto/stk_isu_base_info",
        official_page="https://openapi.krx.co.kr/contents/OPP/USES/service/OPPUSES002_S2.cmd?BO_ID=PiwgMdTwmsenXhmqqxuj",
    ),
    "kosdaq_issue_base": KrxOpenApiService(
        service_id="kosdaq_issue_base",
        title="코스닥 종목기본정보",
        category="stock",
        endpoint="https://data-dbg.krx.co.kr/svc/apis/sto/ksq_isu_base_info",
        official_page="https://openapi.krx.co.kr/contents/OPP/USES/service/OPPUSES002_S2.cmd?BO_ID=CifLHplnUFMgpHIMMPXs",
    ),
    "kospi_index_daily": KrxOpenApiService(
        service_id="kospi_index_daily",
        title="KOSPI 시리즈 일별시세정보",
        category="index",
        endpoint="https://data-dbg.krx.co.kr/svc/apis/idx/kospi_dd_trd",
        official_page="https://openapi.krx.co.kr/contents/OPP/USES/service/OPPUSES001_S2.cmd?BO_ID=EREKZauXnMmxyIlqzeDN",
    ),
    "kosdaq_index_daily": KrxOpenApiService(
        service_id="kosdaq_index_daily",
        title="KOSDAQ 시리즈 일별시세정보",
        category="index",
        endpoint="https://data-dbg.krx.co.kr/svc/apis/idx/kosdaq_dd_trd",
        official_page="https://openapi.krx.co.kr/contents/OPP/USES/service/OPPUSES001_S2.cmd?BO_ID=nimebcamqFNIPNcRrHoO",
    ),
}

CORE_SERVICES = tuple(SERVICES)


def _now_kst() -> datetime:
    return datetime.now(KST).replace(microsecond=0)


def _validate_bas_dd(value: str) -> str:
    if not BAS_DD_RE.match(value):
        raise argparse.ArgumentTypeError("bas-dd must be YYYYMMDD")
    return value


def _validate_capture_date(value: str) -> str:
    if not CAPTURE_DATE_RE.match(value):
        raise argparse.ArgumentTypeError("capture-date must be YYYY-MM-DD")
    return value


def _selected_services(values: list[str]) -> list[KrxOpenApiService]:
    selected = values or list(CORE_SERVICES)
    return [SERVICES[value] for value in selected]


def _raw_output_path(raw_root: Path, capture_date: str, service_id: str, bas_dd: str) -> Path:
    year = capture_date[:4]
    return raw_root / year / capture_date / "krx" / "openapi" / f"{service_id}_{bas_dd}.raw.json"


def _row_info(payload: Any) -> tuple[int | None, list[str]]:
    if not isinstance(payload, dict):
        return None, []
    rows = payload.get("OutBlock_1")
    if not isinstance(rows, list):
        return None, []
    if not rows or not isinstance(rows[0], dict):
        return len(rows), []
    return len(rows), list(rows[0].keys())


def _decode_json(content: bytes) -> Any:
    return json.loads(content.decode("utf-8-sig"))


def _metadata(
    *,
    service: KrxOpenApiService,
    bas_dd: str,
    captured_at_kst: str,
    status_code: int,
    content_type: str,
    raw_output: Path,
    payload: Any,
) -> dict[str, Any]:
    row_count, row_keys = _row_info(payload)
    return {
        "captured_at_kst": captured_at_kst,
        "service": {
            "id": service.service_id,
            "title": service.title,
            "category": service.category,
            "official_page": service.official_page,
        },
        "request": {
            "method": "GET",
            "url": service.endpoint,
            "headers": {"AUTH_KEY": "***"},
            "params": {"basDd": bas_dd},
        },
        "status_code": status_code,
        "content_type": content_type,
        "raw_output": raw_output.as_posix(),
        "top_keys": list(payload.keys()) if isinstance(payload, dict) else [],
        "row_container": "OutBlock_1" if isinstance(payload, dict) and "OutBlock_1" in payload else None,
        "row_count": row_count,
        "row_keys": row_keys,
    }


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _dry_run_plan(services: list[KrxOpenApiService], bas_dd: str, raw_root: Path, capture_date: str) -> dict[str, Any]:
    return {
        "capture_date": capture_date,
        "bas_dd": bas_dd,
        "services": [
            {
                "id": service.service_id,
                "title": service.title,
                "request": {
                    "method": "GET",
                    "url": service.endpoint,
                    "headers": {"AUTH_KEY": "***"},
                    "params": {"basDd": bas_dd},
                },
                "raw_output": _raw_output_path(raw_root, capture_date, service.service_id, bas_dd).as_posix(),
            }
            for service in services
        ],
    }


def _collect_one(service: KrxOpenApiService, bas_dd: str, raw_root: Path, capture_date: str, auth_key: str, timeout: float) -> dict[str, Any]:
    captured_at_kst = _now_kst().isoformat()
    output = _raw_output_path(raw_root, capture_date, service.service_id, bas_dd)
    response = requests.get(
        service.endpoint,
        params={"basDd": bas_dd},
        headers={"AUTH_KEY": auth_key},
        timeout=timeout,
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(response.content)
    payload = _decode_json(response.content)
    meta = _metadata(
        service=service,
        bas_dd=bas_dd,
        captured_at_kst=captured_at_kst,
        status_code=response.status_code,
        content_type=response.headers.get("content-type", ""),
        raw_output=output,
        payload=payload,
    )
    _write_json(output.with_name(f"{output.name}.meta.json"), meta)
    response.raise_for_status()
    return meta


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect approved KRX OpenAPI core Quant raw datasets.")
    parser.add_argument("--bas-dd", required=True, type=_validate_bas_dd, help="KRX base date in YYYYMMDD form.")
    parser.add_argument("--service", action="append", choices=tuple(SERVICES), default=[], help="Service id to collect. Repeatable. Defaults to core 6 services.")
    parser.add_argument("--raw-root", type=Path, default=Path("_report/raw"))
    parser.add_argument("--capture-date", type=_validate_capture_date, default=_now_kst().date().isoformat())
    parser.add_argument("--env-file", type=Path, default=Path(".env.krx"))
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    services = _selected_services(args.service)
    if args.dry_run:
        print(json.dumps(_dry_run_plan(services, args.bas_dd, args.raw_root, args.capture_date), ensure_ascii=False, indent=2))
        return 0

    auth_key = _resolve_auth_key(args.env_file)
    summaries = [_collect_one(service, args.bas_dd, args.raw_root, args.capture_date, auth_key, args.timeout) for service in services]
    print(json.dumps({"bas_dd": args.bas_dd, "capture_date": args.capture_date, "services": summaries}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
