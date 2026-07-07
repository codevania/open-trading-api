"""Collect SEC EDGAR raw submissions and XBRL facts for DI research."""

from __future__ import annotations

import argparse
import json
import os
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo


try:
    KST = ZoneInfo("Asia/Seoul")
except Exception:
    KST = timezone(timedelta(hours=9), "KST")
SEC_DATA = "https://data.sec.gov"
SEC_WWW = "https://www.sec.gov"
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
TICKER_RE = re.compile(r"^[A-Za-z][A-Za-z0-9.\-]{0,14}$")
CIK_RE = re.compile(r"^\d{1,10}$")

DEFAULT_CONCEPTS = (
    "RevenueFromContractWithCustomerExcludingAssessedTax",
    "Revenues",
    "OperatingIncomeLoss",
    "NetIncomeLoss",
    "Assets",
    "Liabilities",
    "StockholdersEquity",
    "NetCashProvidedByUsedInOperatingActivities",
    "PaymentsToAcquirePropertyPlantAndEquipment",
)


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


def _resolve_user_agent(env_file: Path) -> str:
    file_values = _load_env_file(env_file)
    user_agent = os.environ.get("SEC_USER_AGENT") or file_values.get("SEC_USER_AGENT")
    if not user_agent:
        raise ValueError("SEC User-Agent is missing. Set SEC_USER_AGENT in .env.sec or the process environment.")
    return user_agent


def _validate_ymd(value: str) -> str:
    if not DATE_RE.match(value):
        raise argparse.ArgumentTypeError("date must be YYYY-MM-DD")
    return value


def _validate_ticker(value: str) -> str:
    if not TICKER_RE.match(value):
        raise argparse.ArgumentTypeError("ticker must start with a letter and contain only letters, digits, dot, or hyphen")
    return value.upper()


def _validate_cik(value: str) -> str:
    if not CIK_RE.match(value):
        raise argparse.ArgumentTypeError("cik must be 1 to 10 digits")
    return value


def _padded_cik(cik: int | str) -> str:
    return str(cik).strip().lstrip("0").zfill(10)


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _raw_dir(raw_root: Path, run_date: str, symbol: str) -> Path:
    return raw_root / run_date[:4] / run_date / "sec" / symbol.upper()


def _meta_path(raw_path: Path) -> Path:
    return raw_path.with_name(f"{raw_path.name}.meta.json")


def _request_headers(user_agent: str) -> dict[str, str]:
    return {
        "User-Agent": user_agent,
        "Accept-Encoding": "gzip, deflate",
    }


def _redacted_request(url: str) -> dict[str, Any]:
    return {
        "method": "GET",
        "url": url,
        "headers": {"User-Agent": "***", "Accept-Encoding": "gzip, deflate"},
    }


def _get_json(session: Any, url: str, user_agent: str, timeout: float, *, require_success: bool = True) -> tuple[Any, Any]:
    response = session.get(url, headers=_request_headers(user_agent), timeout=timeout)
    if require_success:
        response.raise_for_status()
    try:
        payload: Any = response.json()
    except ValueError:
        payload = {"ok": False, "error": "non-json response", "text_sample": response.text[:500]}
    return payload, response


def _write_meta(path: Path, url: str, response: Any, payload: Any) -> None:
    top_keys = list(payload.keys()) if isinstance(payload, dict) else []
    _write_json(
        path,
        {
            "captured_at_kst": _now_kst().isoformat(),
            "request": _redacted_request(url),
            "status_code": response.status_code,
            "content_type": response.headers.get("content-type", ""),
            "top_keys": top_keys,
        },
    )


def _ticker_map_url() -> str:
    return f"{SEC_WWW}/files/company_tickers.json"


def _submissions_url(cik10: str) -> str:
    return f"{SEC_DATA}/submissions/CIK{cik10}.json"


def _companyfacts_url(cik10: str) -> str:
    return f"{SEC_DATA}/api/xbrl/companyfacts/CIK{cik10}.json"


def _companyconcept_url(cik10: str, concept: str) -> str:
    return f"{SEC_DATA}/api/xbrl/companyconcept/CIK{cik10}/us-gaap/{concept}.json"


def _select_ticker(mapping: Any, ticker: str) -> dict[str, Any]:
    if not isinstance(mapping, dict):
        raise ValueError("SEC ticker mapping returned non-object JSON")
    for row in mapping.values():
        if isinstance(row, dict) and str(row.get("ticker", "")).upper() == ticker.upper():
            return row
    raise ValueError(f"SEC ticker mapping not found for {ticker}")


def _dry_run_plan(args: argparse.Namespace, symbol: str, run_date: str) -> dict[str, Any]:
    base_dir = _raw_dir(args.raw_root, run_date, symbol)
    cik10 = _padded_cik(args.cik) if args.cik else "<resolved>"
    concepts = args.concept or list(DEFAULT_CONCEPTS)
    concept_requests = [] if args.skip_concepts else [
        {
            "id": f"concept_{concept}",
            "request": _redacted_request(_companyconcept_url(cik10, concept)),
            "raw_output": (base_dir / "concepts" / f"us-gaap_{concept}.raw.json").as_posix(),
        }
        for concept in concepts
    ]
    return {
        "source": "SEC EDGAR",
        "symbol": symbol,
        "run_date": run_date,
        "raw_dir": base_dir.as_posix(),
        "requests": [
            {
                "id": "company_tickers",
                "request": _redacted_request(_ticker_map_url()),
                "raw_output": (base_dir / "company_tickers.raw.json").as_posix(),
            },
            {
                "id": "submissions",
                "request": _redacted_request(_submissions_url(cik10)),
                "raw_output": (base_dir / "submissions.raw.json").as_posix(),
            },
            {
                "id": "companyfacts",
                "request": _redacted_request(_companyfacts_url(cik10)),
                "raw_output": (base_dir / "companyfacts.raw.json").as_posix(),
            },
            *concept_requests,
        ],
    }


def collect(args: argparse.Namespace) -> dict[str, Any]:
    run_date = args.run_date or _now_kst().date().isoformat()
    symbol = args.ticker or f"CIK{_padded_cik(args.cik)}"
    if args.dry_run:
        return _dry_run_plan(args, symbol, run_date)

    user_agent = _resolve_user_agent(args.env_file)
    import requests

    base_dir = _raw_dir(args.raw_root, run_date, symbol)
    session = requests.Session()

    summary: dict[str, Any] = {
        "source": "SEC EDGAR",
        "run_date": run_date,
        "symbol": symbol,
        "raw_dir": base_dir.as_posix(),
        "calls": {},
    }

    selected_ticker: dict[str, Any] | None = None
    if args.ticker:
        ticker_url = _ticker_map_url()
        ticker_mapping, response = _get_json(session, ticker_url, user_agent, args.timeout)
        ticker_path = base_dir / "company_tickers.raw.json"
        _write_json(ticker_path, ticker_mapping)
        _write_meta(_meta_path(ticker_path), ticker_url, response, ticker_mapping)
        selected_ticker = _select_ticker(ticker_mapping, args.ticker)
        _write_json(base_dir / "ticker_lookup.json", selected_ticker)
        cik10 = _padded_cik(selected_ticker["cik_str"])
        summary["calls"]["company_tickers"] = {
            "status_code": response.status_code,
            "raw_output": ticker_path.as_posix(),
        }
        summary["ticker_lookup"] = selected_ticker
    else:
        cik10 = _padded_cik(args.cik)
        summary["ticker_lookup"] = {"cik_str": int(cik10), "ticker": None, "title": None}

    submissions_url = _submissions_url(cik10)
    submissions, response = _get_json(session, submissions_url, user_agent, args.timeout)
    submissions_path = base_dir / "submissions.raw.json"
    _write_json(submissions_path, submissions)
    _write_meta(_meta_path(submissions_path), submissions_url, response, submissions)
    summary["calls"]["submissions"] = {
        "status_code": response.status_code,
        "name": submissions.get("name") if isinstance(submissions, dict) else None,
        "recent_forms": len(((submissions.get("filings") or {}).get("recent") or {}).get("form") or []) if isinstance(submissions, dict) else 0,
        "raw_output": submissions_path.as_posix(),
    }

    companyfacts_url = _companyfacts_url(cik10)
    companyfacts, response = _get_json(session, companyfacts_url, user_agent, args.timeout)
    companyfacts_path = base_dir / "companyfacts.raw.json"
    _write_json(companyfacts_path, companyfacts)
    _write_meta(_meta_path(companyfacts_path), companyfacts_url, response, companyfacts)
    summary["calls"]["companyfacts"] = {
        "status_code": response.status_code,
        "entity_name": companyfacts.get("entityName") if isinstance(companyfacts, dict) else None,
        "taxonomies": list((companyfacts.get("facts") or {}).keys()) if isinstance(companyfacts, dict) else [],
        "raw_output": companyfacts_path.as_posix(),
    }

    summary["calls"]["concepts"] = []
    if not args.skip_concepts:
        for concept in args.concept or list(DEFAULT_CONCEPTS):
            url = _companyconcept_url(cik10, concept)
            payload, response = _get_json(session, url, user_agent, args.timeout, require_success=False)
            concept_path = base_dir / "concepts" / f"us-gaap_{concept}.raw.json"
            _write_json(concept_path, payload)
            _write_meta(_meta_path(concept_path), url, response, payload)
            summary["calls"]["concepts"].append(
                {
                    "concept": concept,
                    "status_code": response.status_code,
                    "ok": 200 <= response.status_code < 300,
                    "raw_output": concept_path.as_posix(),
                }
            )

    _write_json(base_dir / "collection_summary.json", summary)
    return summary


def main() -> int:
    default_run_date = _now_kst().date().isoformat()
    parser = argparse.ArgumentParser(description="Collect SEC EDGAR raw evidence for DI company research.")
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("--ticker", type=_validate_ticker, help="US ticker, e.g. MSFT.")
    target.add_argument("--cik", type=_validate_cik, help="SEC CIK, 1 to 10 digits.")
    parser.add_argument("--concept", action="append", default=None, help="US GAAP concept to collect. Repeatable. Defaults to the standard DI concept set.")
    parser.add_argument("--skip-concepts", action="store_true", help="Only collect ticker map, submissions, and companyfacts.")
    parser.add_argument("--run-date", type=_validate_ymd, default=default_run_date)
    parser.add_argument("--raw-root", type=Path, default=Path("_report/raw"))
    parser.add_argument("--env-file", type=Path, default=Path(".env.sec"))
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    print(json.dumps(collect(args), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
