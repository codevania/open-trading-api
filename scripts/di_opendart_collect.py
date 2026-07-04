"""Collect OpenDART raw filings and financial statements for DI research."""

from __future__ import annotations

import argparse
import io
import json
import os
import re
import zipfile
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from xml.etree import ElementTree
from zoneinfo import ZoneInfo


try:
    KST = ZoneInfo("Asia/Seoul")
except Exception:
    KST = timezone(timedelta(hours=9), "KST")
DART_BASE = "https://opendart.fss.or.kr/api"
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
STOCK_CODE_RE = re.compile(r"^\d{6}$")
CORP_CODE_RE = re.compile(r"^\d{8}$")

REPORT_CODES = {
    "annual": "11011",
    "half": "11012",
    "q1": "11013",
    "q3": "11014",
}


def _now_kst() -> datetime:
    return datetime.now(KST).replace(microsecond=0)


def _load_env_file(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}

    values: dict[str, str] = {}
    for line_no, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            raise ValueError(f"{path}:{line_no}: expected KEY=VALUE")
        key, value = line.split("=", 1)
        key = key.strip()
        if not key:
            raise ValueError(f"{path}:{line_no}: empty key")
        values[key] = value.strip().strip('"').strip("'")
    return values


def _resolve_dart_key(env_file: Path) -> str:
    file_values = _load_env_file(env_file)
    key = (
        os.environ.get("OPENDART_API_KEY")
        or os.environ.get("DART_API_KEY")
        or file_values.get("OPENDART_API_KEY")
        or file_values.get("DART_API_KEY")
    )
    if not key:
        raise ValueError("OpenDART API key is missing. Set OPENDART_API_KEY in .env.dart or the process environment.")
    return key


def _validate_ymd(value: str) -> str:
    if not DATE_RE.match(value):
        raise argparse.ArgumentTypeError("date must be YYYY-MM-DD")
    return value


def _validate_stock_code(value: str) -> str:
    if not STOCK_CODE_RE.match(value):
        raise argparse.ArgumentTypeError("stock-code must be a 6 digit KRX code")
    return value


def _validate_corp_code(value: str) -> str:
    if not CORP_CODE_RE.match(value):
        raise argparse.ArgumentTypeError("corp-code must be an 8 digit OpenDART corp code")
    return value


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _write_bytes(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(payload)


def _redacted_request(endpoint: str, params: dict[str, Any]) -> dict[str, Any]:
    redacted_params = dict(params)
    redacted_params["crtfc_key"] = "***"
    return {
        "method": "GET",
        "url": f"{DART_BASE}/{endpoint}",
        "params": redacted_params,
    }


def _raw_dir(raw_root: Path, run_date: str, symbol: str) -> Path:
    return raw_root / run_date[:4] / run_date / "dart" / symbol


def _raw_json_path(base_dir: Path, stem: str) -> Path:
    return base_dir / f"{stem}.raw.json"


def _meta_path(raw_path: Path) -> Path:
    return raw_path.with_name(f"{raw_path.name}.meta.json")


def _extract_corp_code_xml(zip_bytes: bytes) -> bytes:
    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as archive:
        names = archive.namelist()
        if not names:
            raise ValueError("OpenDART corpCode.xml zip was empty")
        with archive.open(names[0]) as handle:
            return handle.read()


def _parse_corp_codes(xml_bytes: bytes) -> list[dict[str, str]]:
    root = ElementTree.fromstring(xml_bytes)
    rows: list[dict[str, str]] = []
    for item in root.findall("list"):
        rows.append(
            {
                "corp_code": (item.findtext("corp_code") or "").strip(),
                "corp_name": (item.findtext("corp_name") or "").strip(),
                "stock_code": (item.findtext("stock_code") or "").strip(),
                "modify_date": (item.findtext("modify_date") or "").strip(),
            }
        )
    return rows


def _select_corp(rows: list[dict[str, str]], stock_code: str | None, corp_code: str | None) -> dict[str, str]:
    if corp_code:
        matches = [row for row in rows if row["corp_code"] == corp_code]
    elif stock_code:
        matches = [row for row in rows if row["stock_code"] == stock_code]
    else:
        raise ValueError("Either stock_code or corp_code is required")

    if not matches:
        target = corp_code or stock_code
        raise ValueError(f"OpenDART corporation not found for {target}")
    if len(matches) > 1:
        return sorted(matches, key=lambda row: row.get("modify_date", ""), reverse=True)[0]
    return matches[0]


def _get_json(session: Any, endpoint: str, params: dict[str, Any], timeout: float) -> tuple[dict[str, Any], Any]:
    response = session.get(f"{DART_BASE}/{endpoint}", params=params, timeout=timeout)
    response.raise_for_status()
    payload = response.json()
    if not isinstance(payload, dict):
        raise ValueError(f"OpenDART {endpoint} returned non-object JSON")
    return payload, response


def _write_meta(path: Path, request: dict[str, Any], response: Any, payload: dict[str, Any]) -> None:
    _write_json(
        path,
        {
            "captured_at_kst": _now_kst().isoformat(),
            "request": request,
            "status_code": response.status_code,
            "content_type": response.headers.get("content-type", ""),
            "dart_status": payload.get("status"),
            "dart_message": payload.get("message"),
            "top_keys": list(payload.keys()),
        },
    )


def _dry_run_plan(args: argparse.Namespace, symbol: str, run_date: str, start_ymd: str, end_ymd: str) -> dict[str, Any]:
    base_dir = _raw_dir(args.raw_root, run_date, symbol)
    report_code_names = args.report_code or ["annual"]
    report_codes = [REPORT_CODES[value] for value in report_code_names]
    return {
        "source": "OpenDART",
        "symbol": symbol,
        "run_date": run_date,
        "raw_dir": base_dir.as_posix(),
        "requests": [
            {
                "id": "corpCode",
                "request": _redacted_request("corpCode.xml", {"crtfc_key": "***"}),
                "raw_output": (base_dir / "corpCode.raw.zip").as_posix(),
            },
            {
                "id": "disclosure_list",
                "request": _redacted_request(
                    "list.json",
                    {
                        "crtfc_key": "***",
                        "corp_code": args.corp_code or "<resolved>",
                        "bgn_de": start_ymd,
                        "end_de": end_ymd,
                        "page_no": 1,
                        "page_count": args.page_count,
                    },
                ),
                "raw_output": _raw_json_path(base_dir, "disclosure_list").as_posix(),
            },
            {
                "id": "company",
                "request": _redacted_request("company.json", {"crtfc_key": "***", "corp_code": args.corp_code or "<resolved>"}),
                "raw_output": _raw_json_path(base_dir, "company").as_posix(),
            },
            *[
                {
                    "id": f"financials_{args.business_year}_{code}_{args.fs_div}",
                    "request": _redacted_request(
                        "fnlttSinglAcntAll.json",
                        {
                            "crtfc_key": "***",
                            "corp_code": args.corp_code or "<resolved>",
                            "bsns_year": args.business_year,
                            "reprt_code": code,
                            "fs_div": args.fs_div,
                        },
                    ),
                    "raw_output": _raw_json_path(base_dir, f"financials_{args.business_year}_{code}_{args.fs_div}").as_posix(),
                }
                for code in report_codes
            ],
        ],
    }


def collect(args: argparse.Namespace) -> dict[str, Any]:
    run_date = args.run_date or _now_kst().date().isoformat()
    parsed_run_date = date.fromisoformat(run_date)
    start_ymd = args.start_date or (parsed_run_date - timedelta(days=args.lookback_days)).strftime("%Y%m%d")
    end_ymd = args.end_date or parsed_run_date.strftime("%Y%m%d")
    symbol = args.stock_code or args.corp_code
    if args.dry_run:
        return _dry_run_plan(args, symbol, run_date, start_ymd, end_ymd)

    dart_key = _resolve_dart_key(args.env_file)
    import requests

    base_dir = _raw_dir(args.raw_root, run_date, symbol)
    session = requests.Session()

    corp_params = {"crtfc_key": dart_key}
    corp_response = session.get(f"{DART_BASE}/corpCode.xml", params=corp_params, timeout=args.timeout)
    corp_response.raise_for_status()
    _write_bytes(base_dir / "corpCode.raw.zip", corp_response.content)
    corp_xml = _extract_corp_code_xml(corp_response.content)
    _write_bytes(base_dir / "corpCode.raw.xml", corp_xml)
    corp_rows = _parse_corp_codes(corp_xml)
    selected_corp = _select_corp(corp_rows, args.stock_code, args.corp_code)
    _write_json(base_dir / "corp_lookup.json", selected_corp)

    summary: dict[str, Any] = {
        "source": "OpenDART",
        "run_date": run_date,
        "symbol": symbol,
        "corp": selected_corp,
        "raw_dir": base_dir.as_posix(),
        "calls": {},
    }

    list_params = {
        "crtfc_key": dart_key,
        "corp_code": selected_corp["corp_code"],
        "bgn_de": start_ymd,
        "end_de": end_ymd,
        "page_no": 1,
        "page_count": args.page_count,
    }
    disclosure_list, response = _get_json(session, "list.json", list_params, args.timeout)
    disclosure_path = _raw_json_path(base_dir, "disclosure_list")
    _write_json(disclosure_path, disclosure_list)
    _write_meta(_meta_path(disclosure_path), _redacted_request("list.json", list_params), response, disclosure_list)
    summary["calls"]["disclosure_list"] = {
        "status": disclosure_list.get("status"),
        "message": disclosure_list.get("message"),
        "rows": len(disclosure_list.get("list") or []),
        "raw_output": disclosure_path.as_posix(),
    }

    company_params = {"crtfc_key": dart_key, "corp_code": selected_corp["corp_code"]}
    company, response = _get_json(session, "company.json", company_params, args.timeout)
    company_path = _raw_json_path(base_dir, "company")
    _write_json(company_path, company)
    _write_meta(_meta_path(company_path), _redacted_request("company.json", company_params), response, company)
    summary["calls"]["company"] = {
        "status": company.get("status"),
        "message": company.get("message"),
        "raw_output": company_path.as_posix(),
    }

    summary["calls"]["financials"] = []
    for report_code_name in args.report_code or ["annual"]:
        report_code = REPORT_CODES[report_code_name]
        financial_params = {
            "crtfc_key": dart_key,
            "corp_code": selected_corp["corp_code"],
            "bsns_year": args.business_year,
            "reprt_code": report_code,
            "fs_div": args.fs_div,
        }
        financials, response = _get_json(session, "fnlttSinglAcntAll.json", financial_params, args.timeout)
        financial_path = _raw_json_path(base_dir, f"financials_{args.business_year}_{report_code}_{args.fs_div}")
        _write_json(financial_path, financials)
        _write_meta(
            _meta_path(financial_path),
            _redacted_request("fnlttSinglAcntAll.json", financial_params),
            response,
            financials,
        )
        summary["calls"]["financials"].append(
            {
                "report_code_name": report_code_name,
                "report_code": report_code,
                "status": financials.get("status"),
                "message": financials.get("message"),
                "rows": len(financials.get("list") or []),
                "raw_output": financial_path.as_posix(),
            }
        )

    _write_json(base_dir / "collection_summary.json", summary)
    return summary


def main() -> int:
    default_run_date = _now_kst().date().isoformat()
    parser = argparse.ArgumentParser(description="Collect OpenDART raw evidence for DI company research.")
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("--stock-code", type=_validate_stock_code, help="6 digit KRX stock code, e.g. 005930.")
    target.add_argument("--corp-code", type=_validate_corp_code, help="8 digit OpenDART corp code.")
    parser.add_argument("--business-year", default=str(date.fromisoformat(default_run_date).year - 1))
    parser.add_argument("--report-code", action="append", choices=tuple(REPORT_CODES), default=None)
    parser.add_argument("--fs-div", choices=("CFS", "OFS"), default="CFS")
    parser.add_argument("--run-date", type=_validate_ymd, default=default_run_date)
    parser.add_argument("--start-date", help="Disclosure search start date in YYYYMMDD. Defaults to run date minus lookback days.")
    parser.add_argument("--end-date", help="Disclosure search end date in YYYYMMDD. Defaults to run date.")
    parser.add_argument("--lookback-days", type=int, default=365)
    parser.add_argument("--page-count", type=int, default=100)
    parser.add_argument("--raw-root", type=Path, default=Path("_report/raw"))
    parser.add_argument("--env-file", type=Path, default=Path(".env.dart"))
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    print(json.dumps(collect(args), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
