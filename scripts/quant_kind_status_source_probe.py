"""Probe KIND public status downloads for Point-in-Time source wiring.

This script is read-only. It does not require or accept account credentials.
It preserves current KIND status download evidence as raw files and a small
manifest so later normalization can be built from verified official sources.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.parse import unquote
from zoneinfo import ZoneInfo

import requests

from quant_io import write_json_lf, write_text_lf


KST = ZoneInfo("Asia/Seoul")
KIND_BASE_URL = "https://kind.krx.co.kr"
CAPTURE_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
INPUT_RE = re.compile(r"<input\b(?P<attrs>[^>]*)>", re.IGNORECASE)
ATTR_RE = re.compile(r"(?P<key>[A-Za-z_:][-A-Za-z0-9_:.]*)\s*=\s*[\"'](?P<value>.*?)[\"']", re.IGNORECASE)
OPTION_RE = re.compile(r"<option\b(?P<attrs>[^>]*)>", re.IGNORECASE)
SELECT_RE = re.compile(r"<select\b(?P<attrs>[^>]*)>(?P<body>.*?)</select>", re.IGNORECASE | re.DOTALL)
SEARCH_FORM_RE = re.compile(
    r"<form\b(?P<attrs>[^>]*(?:id|name)\s*=\s*[\"']searchForm[\"'][^>]*)>(?P<body>.*?)</form>",
    re.IGNORECASE | re.DOTALL,
)
FN_DOWNLOAD_START_RE = re.compile(r"function\s+fnDownload\s*\(\)\s*\{", re.IGNORECASE)
ACTION_RE = re.compile(r"attr\(\s*['\"]action['\"]\s*,\s*['\"](?P<action>[^'\"]+)['\"]\s*\)", re.IGNORECASE)
JQUERY_VALUE_RE = re.compile(r"#(?P<name>method|forward)[\"']\)\.val\([\"'](?P<value>[^\"']+)[\"']\)", re.IGNORECASE)
TABLE_RE = re.compile(r"<table\b", re.IGNORECASE)
TR_RE = re.compile(r"<tr\b", re.IGNORECASE)


@dataclass(frozen=True)
class KindStatusSpec:
    slug: str
    label: str
    status_type_hint: str
    page_path: str
    post_path: str
    download_method: str
    download_forward: str
    extra_fields: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class DownloadDefinition:
    action: str
    methods: list[str]
    forwards: list[str]


@dataclass(frozen=True)
class KindProbeResult:
    slug: str
    label: str
    status_type_hint: str
    page_url: str
    post_url: str
    download_method: str
    download_forward: str
    discovered_action: str
    discovered_methods: list[str]
    discovered_forwards: list[str]
    response_status_code: int
    response_content_type: str
    response_content_disposition: str
    filename: str
    byte_count: int
    table_count: int
    table_tr_count: int
    classification: str
    message: str
    raw_path: str


DEFAULT_SPECS = (
    KindStatusSpec(
        slug="managed_issue",
        label="Managed issue",
        status_type_hint="managed_issue",
        page_path="/investwarn/adminissue.do?method=searchAdminIssueList",
        post_path="/investwarn/adminissue.do",
        download_method="searchAdminIssueSub",
        download_forward="adminissue_down",
    ),
    KindStatusSpec(
        slug="watchlist_issue",
        label="KOSDAQ watchlist issue",
        status_type_hint="managed_issue",
        page_path="/investwarn/hwangiissue.do?method=searchHwangiIssueMain",
        post_path="/investwarn/hwangiissue.do",
        download_method="searchHwangiIssueSub",
        download_forward="hwangiissue_down",
    ),
    KindStatusSpec(
        slug="trading_halt",
        label="Trading halt",
        status_type_hint="trading_halt",
        page_path="/investwarn/tradinghaltissue.do?method=searchTradingHaltIssueMain",
        post_path="/investwarn/tradinghaltissue.do",
        download_method="searchTradingHaltIssueSub",
        download_forward="tradinghaltissue_down",
    ),
    KindStatusSpec(
        slug="delisted_company",
        label="Delisted company",
        status_type_hint="delisting",
        page_path="/investwarn/delcompany.do?method=searchDelCompanyMain",
        post_path="/investwarn/delcompany.do",
        download_method="searchDelCompanySub",
        download_forward="delcompany_down",
    ),
    KindStatusSpec(
        slug="market_alert_caution",
        label="Market alert caution",
        status_type_hint="market_alert",
        page_path="/investwarn/investattentwarnrisky.do?method=investattentwarnriskyMain",
        post_path="/investwarn/investattentwarnrisky.do",
        download_method="investattentwarnriskySub",
        download_forward="invstcautnisu_down",
        extra_fields={"menuIndex": "1"},
    ),
    KindStatusSpec(
        slug="market_alert_warning",
        label="Market alert warning",
        status_type_hint="market_alert",
        page_path="/investwarn/investattentwarnrisky.do?method=investattentwarnriskyMain",
        post_path="/investwarn/investattentwarnrisky.do",
        download_method="investattentwarnriskySub",
        download_forward="invstwarnisu_down",
        extra_fields={"menuIndex": "2"},
    ),
    KindStatusSpec(
        slug="market_alert_risk",
        label="Market alert risk",
        status_type_hint="market_alert",
        page_path="/investwarn/investattentwarnrisky.do?method=investattentwarnriskyMain",
        post_path="/investwarn/investattentwarnrisky.do",
        download_method="investattentwarnriskySub",
        download_forward="invstriskisu_down",
        extra_fields={"menuIndex": "3"},
    ),
)


def _now_kst() -> datetime:
    return datetime.now(KST).replace(microsecond=0)


def _validate_capture_date(value: str) -> str:
    if not CAPTURE_DATE_RE.match(value):
        raise argparse.ArgumentTypeError("capture-date must be YYYY-MM-DD")
    return value


def _abs_url(path_or_url: str) -> str:
    if path_or_url.startswith("http://") or path_or_url.startswith("https://"):
        return path_or_url
    return f"{KIND_BASE_URL}{path_or_url}"


def _parse_attrs(raw_attrs: str) -> dict[str, str]:
    return {match.group("key").lower(): match.group("value") for match in ATTR_RE.finditer(raw_attrs)}


def _search_form_html(html: str) -> str:
    match = SEARCH_FORM_RE.search(html)
    if not match:
        return html
    return match.group("body")


def extract_form_defaults(html: str, capture_date: str | None = None) -> dict[str, str]:
    form_html = _search_form_html(html)
    defaults: dict[str, str] = {}
    pending_radios: dict[str, str] = {}

    for input_match in INPUT_RE.finditer(form_html):
        raw_attrs = input_match.group("attrs")
        attrs = _parse_attrs(raw_attrs)
        name = attrs.get("name", "")
        value = attrs.get("value", "")
        if not name:
            continue
        input_type = attrs.get("type", "").lower()
        if input_type == "radio":
            pending_radios.setdefault(name, value)
            if re.search(r"\bchecked\b", raw_attrs, re.IGNORECASE):
                defaults[name] = value
        elif input_type == "checkbox":
            if re.search(r"\bchecked\b", raw_attrs, re.IGNORECASE):
                defaults[name] = value
        elif input_type in {"hidden", "text", ""}:
            defaults[name] = value

    for name, first_value in pending_radios.items():
        defaults.setdefault(name, first_value)

    for select_match in SELECT_RE.finditer(form_html):
        select_attrs = _parse_attrs(select_match.group("attrs"))
        name = select_attrs.get("name") or select_attrs.get("id") or ""
        if not name:
            continue
        selected = ""
        first = ""
        for option_match in OPTION_RE.finditer(select_match.group("body")):
            raw_attrs = option_match.group("attrs")
            option_attrs = _parse_attrs(raw_attrs)
            value = option_attrs.get("value", "")
            if not first:
                first = value
            if re.search(r"\bselected\b", raw_attrs, re.IGNORECASE):
                selected = value
                break
        defaults.setdefault(name, selected or first)

    if capture_date and "startDate" in defaults:
        defaults["startDate"] = capture_date
        defaults["endDate"] = capture_date
    elif defaults.get("searchFromDate") and not defaults.get("startDate"):
        defaults["startDate"] = defaults["searchFromDate"]
        defaults["endDate"] = defaults["searchFromDate"]

    return defaults


def extract_download_definition(html: str) -> DownloadDefinition:
    body = _extract_function_body(html, FN_DOWNLOAD_START_RE)
    if body is None:
        return DownloadDefinition(action="", methods=[], forwards=[])

    action_match = ACTION_RE.search(body)
    methods: list[str] = []
    forwards: list[str] = []
    for value_match in JQUERY_VALUE_RE.finditer(body):
        name = value_match.group("name").lower()
        value = value_match.group("value")
        if name == "method":
            methods.append(value)
        elif name == "forward":
            forwards.append(value)

    return DownloadDefinition(
        action=action_match.group("action") if action_match else "",
        methods=list(dict.fromkeys(methods)),
        forwards=list(dict.fromkeys(forwards)),
    )


def _extract_function_body(html: str, start_re: re.Pattern[str]) -> str | None:
    match = start_re.search(html)
    if not match:
        return None

    index = match.end()
    depth = 1
    in_string = ""
    escaped = False
    while index < len(html):
        char = html[index]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == in_string:
                in_string = ""
        elif char in {"'", '"'}:
            in_string = char
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return html[match.end() : index]
        index += 1
    return None


def build_download_payload(spec: KindStatusSpec, html: str, capture_date: str) -> dict[str, str]:
    payload = extract_form_defaults(html, capture_date=capture_date)
    payload.update(
        {
            "method": spec.download_method,
            "forward": spec.download_forward,
            "currentPageSize": "3000",
            "pageIndex": "1",
        }
    )
    payload.update(spec.extra_fields)
    if "searchCorpNameTmp" in payload:
        payload["searchCorpName"] = payload.get("searchCorpNameTmp", "")
    return payload


def _decode_content(content: bytes, content_type: str) -> str:
    lowered = content_type.lower()
    encodings = ["euc-kr", "utf-8", "cp949"] if "euc-kr" in lowered else ["utf-8", "euc-kr", "cp949"]
    for encoding in encodings:
        try:
            return content.decode(encoding)
        except UnicodeDecodeError:
            continue
    return content.decode("utf-8", errors="replace")


def _filename_from_disposition(content_disposition: str) -> str:
    match = re.search(r"filename\*?=(?:UTF-8''|\"?)(?P<filename>[^\";]+)", content_disposition, re.IGNORECASE)
    if not match:
        return ""
    return unquote(match.group("filename").strip('"'))


def classify_download_response(
    status_code: int,
    content_type: str,
    content_disposition: str,
    content: bytes,
) -> dict[str, Any]:
    text = _decode_content(content, content_type)
    table_count = len(TABLE_RE.findall(text))
    table_tr_count = len(TR_RE.findall(text))
    filename = _filename_from_disposition(content_disposition)

    if status_code in {401, 403}:
        classification = "auth_required"
        message = f"HTTP {status_code}"
    elif status_code >= 400:
        classification = "http_error"
        message = f"HTTP {status_code}"
    elif table_count:
        classification = "ok_table_download"
        message = f"{table_count} table(s), {table_tr_count} tr tag(s)"
    elif "application/vnd.ms-excel" in content_type.lower() and content:
        classification = "excel_without_html_table"
        message = "Excel-like response did not expose an HTML table."
    elif "<html" in text.lower():
        classification = "html_without_table"
        message = "HTML response did not expose a table."
    elif content:
        classification = "non_empty_response_without_table"
        message = content_type or "unknown content-type"
    else:
        classification = "empty_response"
        message = "No response body."

    return {
        "classification": classification,
        "message": message,
        "filename": filename,
        "table_count": table_count,
        "table_tr_count": table_tr_count,
    }


def _raw_extension(classification: str, content_type: str) -> str:
    if "excel" in classification or "application/vnd.ms-excel" in content_type.lower():
        return ".xls"
    if "html" in classification:
        return ".html"
    return ".bin"


def probe_kind_status_sources(
    *,
    capture_date: str,
    raw_root: Path,
    timeout: float,
    specs: tuple[KindStatusSpec, ...] = DEFAULT_SPECS,
) -> tuple[list[KindProbeResult], Path]:
    session = requests.Session()
    raw_base = raw_root / capture_date[:4] / capture_date / "kind"
    snapshot_dir = raw_base / "status-source-probe"
    snapshot_dir.mkdir(parents=True, exist_ok=True)

    results: list[KindProbeResult] = []
    for spec in specs:
        page_url = _abs_url(spec.page_path)
        post_url = _abs_url(spec.post_path)
        page_response = session.get(page_url, timeout=timeout)
        page_response.raise_for_status()
        html = page_response.text
        definition = extract_download_definition(html)
        payload = build_download_payload(spec, html, capture_date)

        response = session.post(post_url, data=payload, timeout=timeout)
        response_content_type = response.headers.get("content-type", "")
        response_content_disposition = response.headers.get("content-disposition", "")
        classified = classify_download_response(
            response.status_code,
            response_content_type,
            response_content_disposition,
            response.content,
        )
        raw_path = snapshot_dir / f"{spec.slug}{_raw_extension(classified['classification'], response_content_type)}"
        raw_path.write_bytes(response.content)

        results.append(
            KindProbeResult(
                slug=spec.slug,
                label=spec.label,
                status_type_hint=spec.status_type_hint,
                page_url=page_url,
                post_url=post_url,
                download_method=spec.download_method,
                download_forward=spec.download_forward,
                discovered_action=definition.action,
                discovered_methods=definition.methods,
                discovered_forwards=definition.forwards,
                response_status_code=response.status_code,
                response_content_type=response_content_type,
                response_content_disposition=response_content_disposition,
                filename=str(classified["filename"]),
                byte_count=len(response.content),
                table_count=int(classified["table_count"]),
                table_tr_count=int(classified["table_tr_count"]),
                classification=str(classified["classification"]),
                message=str(classified["message"]),
                raw_path=raw_path.as_posix(),
            )
        )

    manifest_path = raw_base / "status-source-probe.raw.json"
    write_json_lf(
        manifest_path,
        {
            "capture_date": capture_date,
            "captured_at": _now_kst().isoformat(),
            "source": "kind",
            "source_base_url": KIND_BASE_URL,
            "results": [asdict(result) for result in results],
        },
    )
    return results, manifest_path


def _wikilink(path: Path | str) -> str:
    rendered = Path(path).as_posix() if isinstance(path, Path) else str(path).replace("\\", "/")
    return f"[[{rendered}|{rendered}]]"


def render_report(capture_date: str, results: list[KindProbeResult], manifest_path: Path) -> str:
    ok_count = sum(1 for result in results if result.classification == "ok_table_download")
    lines = [
        "# KIND Status Source Probe",
        "",
        f"- Capture date: `{capture_date}`",
        "- Source: `KIND` public status pages",
        f"- Raw manifest: {_wikilink(manifest_path)}",
        f"- OK table downloads: `{ok_count}/{len(results)}`",
        "- Interpretation: official current/status download evidence; not historical Point-in-Time coverage by itself",
        "- Backtest readiness: `hold`",
        "",
        "## Results",
        "",
        "| Status source | Hint | Method | Forward | Classification | Filename | Bytes | Tables | TR tags | Raw |",
        "| --- | --- | --- | --- | --- | --- | ---: | ---: | ---: | --- |",
    ]
    for result in results:
        lines.append(
            "| "
            f"{result.label} | "
            f"`{result.status_type_hint}` | "
            f"`{result.download_method}` | "
            f"`{result.download_forward}` | "
            f"`{result.classification}` | "
            f"`{result.filename}` | "
            f"{result.byte_count} | "
            f"{result.table_count} | "
            f"{result.table_tr_count} | "
            f"{_wikilink(result.raw_path)} |"
        )

    lines.extend(
        [
            "",
            "## Guardrails",
            "",
            "- Treat these as source-availability probes until normalized event rows pass validation.",
            "- `TR tags` are raw HTML table row tags, not confirmed investable-code event rows.",
            "- Historical `Backtest` remains blocked until the selected date range has reproducible status coverage.",
            "- If a source returns `html_without_table`, inspect the raw file before using it for normalization.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    today = _now_kst().date().isoformat()
    parser = argparse.ArgumentParser(description="Probe KIND public status downloads for Quant Point-in-Time work.")
    parser.add_argument("--capture-date", default=today, type=_validate_capture_date)
    parser.add_argument("--raw-root", default=Path("_report/raw"), type=Path)
    parser.add_argument("--report-output", type=Path)
    parser.add_argument("--timeout", default=20.0, type=float)
    args = parser.parse_args()

    results, manifest_path = probe_kind_status_sources(
        capture_date=args.capture_date,
        raw_root=args.raw_root,
        timeout=args.timeout,
    )
    report = render_report(args.capture_date, results, manifest_path)
    if args.report_output:
        write_text_lf(args.report_output, report)
    else:
        print(report, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
