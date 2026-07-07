"""Probe KRX Data Marketplace status screens for Point-in-Time source wiring.

This script is read-only. It does not require or accept account credentials.
Its purpose is to preserve the official menu/screen/bld evidence needed before
building a Point-in-Time status collector. Some KRX status screens may return
``LOGOUT`` for their JSON endpoint; that is recorded as an access result rather
than treated as a successful status source.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.parse import quote
from zoneinfo import ZoneInfo

import requests

from quant_io import write_json_lf, write_text_lf


KST = ZoneInfo("Asia/Seoul")
KRX_BASE_URL = "https://data.krx.co.kr"
MENU_SEARCH_PATH = "/comm/util/SearchEngine/menuCore.cmd"
JSON_DATA_PATH = "/comm/bldAttendant/getJsonData.cmd"
CAPTURE_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
INPUT_RE = re.compile(r"<input\b(?P<attrs>[^>]*)>", re.IGNORECASE)
ATTR_RE = re.compile(r"(?P<key>[A-Za-z_:][-A-Za-z0-9_:.]*)\s*=\s*[\"'](?P<value>.*?)[\"']", re.IGNORECASE)
FORM_RE = re.compile(r"<form\b(?P<attrs>[^>]*)>", re.IGNORECASE)
GRID_BLD_RE = re.compile(r"bld\s*:\s*'(?P<bld>[^']+)'")
GRID_KEY_RE = re.compile(r"bldDataKey\s*:\s*'(?P<key>[^']+)'")

DEFAULT_KEYWORDS = (
    "전종목 지정내역",
    "관리종목 현황",
    "매매거래정지종목 현황",
    "상장폐지종목 현황",
    "정리매매종목 현황",
    "투자주의종목 현황",
    "투자경고종목 현황",
    "투자위험종목 현황",
)


@dataclass(frozen=True)
class MenuResult:
    keyword: str
    org_menu_name: str
    menu_name: str
    screen_no: str
    screen_url: str
    menu_id: str
    screen_id: str


@dataclass(frozen=True)
class ScreenDefinition:
    screen_url: str
    form_id: str
    form_name: str
    defaults: dict[str, str]
    blds: list[str]
    bld_data_keys: list[str]


def _now_kst() -> datetime:
    return datetime.now(KST).replace(microsecond=0)


def _validate_capture_date(value: str) -> str:
    if not CAPTURE_DATE_RE.match(value):
        raise argparse.ArgumentTypeError("capture-date must be YYYY-MM-DD")
    return value


def _abs_url(path_or_url: str) -> str:
    if path_or_url.startswith("http://") or path_or_url.startswith("https://"):
        return path_or_url
    return f"{KRX_BASE_URL}{path_or_url}"


def _one(value: Any) -> str:
    if isinstance(value, list):
        return str(value[0]) if value else ""
    if value is None:
        return ""
    return str(value)


def parse_menu_results(keyword: str, payload: dict[str, Any]) -> list[MenuResult]:
    rows = payload.get("result", [])
    if not isinstance(rows, list):
        return []

    results: list[MenuResult] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        results.append(
            MenuResult(
                keyword=keyword,
                org_menu_name=_one(row.get("org_menu_nm")),
                menu_name=_one(row.get("menu_nm")),
                screen_no=_one(row.get("scren_no")),
                screen_url=_one(row.get("scren_url")),
                menu_id=_one(row.get("menu_id")),
                screen_id=_one(row.get("scren_id")),
            )
        )
    return results


def _parse_attrs(raw_attrs: str) -> dict[str, str]:
    attrs = {match.group("key").lower(): match.group("value") for match in ATTR_RE.finditer(raw_attrs)}
    lowered = raw_attrs.lower()
    if " checked" in lowered or lowered.strip().endswith("checked"):
        attrs["checked"] = "checked"
    return attrs


def extract_screen_definition(screen_url: str, html: str) -> ScreenDefinition:
    form_id = ""
    form_name = ""
    form_match = FORM_RE.search(html)
    if form_match:
        attrs = _parse_attrs(form_match.group("attrs"))
        form_id = attrs.get("id", "")
        form_name = attrs.get("name", "")

    defaults: dict[str, str] = {}
    pending_radios: dict[str, str] = {}
    for input_match in INPUT_RE.finditer(html):
        attrs = _parse_attrs(input_match.group("attrs"))
        name = attrs.get("name", "")
        value = attrs.get("value", "")
        if not name:
            continue
        input_type = attrs.get("type", "").lower()
        if input_type == "radio":
            pending_radios.setdefault(name, value)
            if attrs.get("checked"):
                defaults[name] = value
        elif input_type in {"checkbox", "hidden", "text", ""}:
            defaults[name] = value

    for name, first_value in pending_radios.items():
        defaults.setdefault(name, first_value)

    blds = list(dict.fromkeys(match.group("bld") for match in GRID_BLD_RE.finditer(html)))
    bld_data_keys = list(dict.fromkeys(match.group("key") for match in GRID_KEY_RE.finditer(html)))

    return ScreenDefinition(
        screen_url=screen_url,
        form_id=form_id,
        form_name=form_name,
        defaults=defaults,
        blds=blds,
        bld_data_keys=bld_data_keys,
    )


def classify_json_response(
    status_code: int,
    content_type: str,
    text: str,
    payload: Any,
    row_keys: list[str] | None = None,
) -> dict[str, Any]:
    if status_code in {401, 403} or text.strip().upper() == "LOGOUT":
        return {"status": "auth_required", "row_count": None, "message": "KRX returned LOGOUT or an auth status."}
    if status_code >= 400:
        return {"status": "http_error", "row_count": None, "message": f"HTTP {status_code}"}
    if not isinstance(payload, dict):
        return {"status": "non_json_response", "row_count": None, "message": content_type}

    candidate_keys = row_keys or ["OutBlock_1", "output"]
    for key in candidate_keys:
        rows = payload.get(key)
        if isinstance(rows, list):
            return {"status": "ok", "row_count": len(rows), "message": f"{key} rows returned."}
    return {"status": "json_without_rows", "row_count": None, "message": "No configured row container is present."}


def _decode_json_response(response: requests.Response) -> tuple[Any, str]:
    text = response.text
    try:
        return response.json(), text
    except ValueError:
        return None, text


def _menu_search(session: requests.Session, keyword: str, timeout: float) -> dict[str, Any]:
    url = _abs_url(MENU_SEARCH_PATH)
    params = {
        "isAutoCom": "true",
        "type": "",
        "solrIsuType": "",
        "solrKeyword": keyword,
        "rows": "20",
        "start": "0",
    }
    response = session.get(url, params=params, timeout=timeout)
    response.raise_for_status()
    return response.json()


def _probe_json(
    session: requests.Session,
    *,
    screen_url: str,
    bld: str,
    row_keys: list[str],
    defaults: dict[str, str],
    timeout: float,
) -> dict[str, Any]:
    url = f"{_abs_url(JSON_DATA_PATH)}?bld={quote(bld, safe='/')}"
    headers = {
        "Referer": _abs_url(screen_url),
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0",
    }
    response = session.post(url, data=defaults, headers=headers, timeout=timeout)
    payload, text = _decode_json_response(response)
    classified = classify_json_response(
        response.status_code,
        response.headers.get("content-type", ""),
        text,
        payload,
        row_keys,
    )
    return {
        "request": {
            "method": "POST",
            "url": url,
            "headers": {"Referer": _abs_url(screen_url), "X-Requested-With": "XMLHttpRequest"},
            "form": defaults,
        },
        "status_code": response.status_code,
        "content_type": response.headers.get("content-type", ""),
        "classification": classified,
        "top_keys": list(payload.keys()) if isinstance(payload, dict) else [],
        "body_excerpt": text[:500],
    }


def _write_json(path: Path, payload: Any) -> None:
    write_json_lf(path, payload)


def _wikilink(path: str | Path) -> str:
    rendered = path.as_posix() if isinstance(path, Path) else path
    return f"[[{rendered}|{rendered}]]"


def _render_report(payload: dict[str, Any], raw_output: Path | None) -> str:
    lines = [
        "# KRX Data Marketplace Status Source Probe",
        "",
        f"- Captured at KST: `{payload['captured_at_kst']}`",
        "- Scope: official KRX Data Marketplace status screen endpoint discovery",
        "- Interpretation: source-access probe only, not a `Point-in-Time Universe` or `Backtest` result",
        "",
        "## Raw Evidence",
        "",
    ]
    if raw_output is not None:
        lines.append(f"- {_wikilink(raw_output)}")
    else:
        lines.append("- Not written; stdout only.")

    lines.extend(["", "## Probe Results", "", "| keyword | screen | bld | result | rows |", "| --- | --- | --- | --- | ---: |"])
    for keyword_result in payload["keywords"]:
        for screen in keyword_result["screens"]:
            screen_label = screen["menu"]["screen_id"] or screen["menu"]["screen_no"]
            blds = screen["definition"]["blds"] or ["-"]
            probes = screen["json_probes"] or []
            if probes:
                for probe in probes:
                    classification = probe["classification"]
                    lines.append(
                        f"| {keyword_result['keyword']} | `{screen_label}` | `{probe['bld']}` | "
                        f"`{classification['status']}` | {classification['row_count'] if classification['row_count'] is not None else '-'} |"
                    )
            else:
                for bld in blds:
                    lines.append(f"| {keyword_result['keyword']} | `{screen_label}` | `{bld}` | `not_probed` | - |")

    lines.extend(
        [
            "",
            "## Current Judgment",
            "",
            "- KRX official menu/search metadata can identify status candidate screens and their `bld` identifiers.",
            "- A `LOGOUT` classification means the endpoint is official but not usable as unattended raw input without an authenticated KRX session or manual official download.",
            "- `Backtest` readiness remains `hold` until at least one official status raw sample can be saved, normalized, validated, and replayed.",
        ]
    )
    return "\n".join(lines) + "\n"


def build_probe(
    *,
    keywords: list[str],
    timeout: float,
    max_screens_per_keyword: int,
    probe_json: bool,
) -> dict[str, Any]:
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0"})
    captured_at_kst = _now_kst().isoformat()
    results: list[dict[str, Any]] = []

    for keyword in keywords:
        menu_payload = _menu_search(session, keyword, timeout)
        menu_results = parse_menu_results(keyword, menu_payload)
        screens: list[dict[str, Any]] = []
        for menu in menu_results[:max_screens_per_keyword]:
            screen_url = _abs_url(menu.screen_url)
            screen_response = session.get(screen_url, timeout=timeout)
            definition = extract_screen_definition(menu.screen_url, screen_response.text)
            json_probes = []
            if probe_json:
                for bld in definition.blds:
                    json_probe = _probe_json(
                        session,
                        screen_url=menu.screen_url,
                        bld=bld,
                        row_keys=definition.bld_data_keys,
                        defaults=definition.defaults,
                        timeout=timeout,
                    )
                    json_probe["bld"] = bld
                    json_probes.append(json_probe)
            screens.append(
                {
                    "menu": asdict(menu),
                    "screen_fetch": {
                        "url": screen_url,
                        "status_code": screen_response.status_code,
                        "content_type": screen_response.headers.get("content-type", ""),
                    },
                    "definition": asdict(definition),
                    "json_probes": json_probes,
                }
            )
        results.append(
            {
                "keyword": keyword,
                "menu_result_count": len(menu_results),
                "screens": screens,
            }
        )

    return {
        "captured_at_kst": captured_at_kst,
        "source": {
            "name": "KRX Data Marketplace",
            "menu_search_url": _abs_url(MENU_SEARCH_PATH),
            "json_data_url": _abs_url(JSON_DATA_PATH),
        },
        "keywords": results,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Probe KRX Data Marketplace status screens for official source wiring.")
    parser.add_argument("--keyword", action="append", default=[], help="Status screen keyword. Repeatable. Defaults to core status candidates.")
    parser.add_argument("--capture-date", type=_validate_capture_date, default=_now_kst().date().isoformat())
    parser.add_argument("--raw-root", type=Path, default=Path("_report/raw"))
    parser.add_argument("--output", type=Path, help="Raw probe JSON output path.")
    parser.add_argument("--report-output", type=Path, help="Markdown report output path.")
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument("--max-screens-per-keyword", type=int, default=1)
    parser.add_argument("--skip-json-probe", action="store_true", help="Only resolve menu/JSP definitions; do not call JSON data endpoints.")
    args = parser.parse_args()

    keywords = args.keyword or list(DEFAULT_KEYWORDS)
    payload = build_probe(
        keywords=keywords,
        timeout=args.timeout,
        max_screens_per_keyword=args.max_screens_per_keyword,
        probe_json=not args.skip_json_probe,
    )

    output = args.output
    if output is None and args.report_output:
        year = args.capture_date[:4]
        output = args.raw_root / year / args.capture_date / "krx" / "data-marketplace" / "status-source-probe.raw.json"

    if output is not None:
        _write_json(output, payload)
    if args.report_output:
        write_text_lf(args.report_output, _render_report(payload, output))
    if output is None and args.report_output is None:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
