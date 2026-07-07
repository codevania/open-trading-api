"""Collect SEC EDGAR primary filing documents for DI research."""

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

DEFAULT_RAW_ROOT = Path("_report/raw")
DEFAULT_RESEARCH_ROOT = Path("_report/di/research")
DEFAULT_FORMS = ("10-K", "10-Q")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SYMBOL_RE = re.compile(r"^[A-Za-z][A-Za-z0-9.\-]{0,14}$")
SAFE_NAME_RE = re.compile(r"[^A-Za-z0-9._-]+")


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


def _validate_symbol(value: str) -> str:
    if not SYMBOL_RE.match(value):
        raise argparse.ArgumentTypeError("symbol must start with a letter and contain only letters, digits, dot, or hyphen")
    return value.upper()


def _safe_filename(value: str) -> str:
    cleaned = SAFE_NAME_RE.sub("_", value.strip())
    return cleaned.strip("._") or "document"


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


def _read_json(path: Path) -> Any:
    if not path.exists():
        raise ValueError(f"{path}: file not found")
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _raw_dir(raw_root: Path, run_date: str, symbol: str) -> Path:
    return raw_root / run_date[:4] / run_date / "sec" / symbol.upper()


def _research_output_path(research_root: Path, symbol: str) -> Path:
    return research_root / symbol.upper() / "sec-filing-documents.md"


def _cik_for_archive(submissions: dict[str, Any]) -> str:
    cik = str(submissions.get("cik") or "").strip()
    if not cik:
        return ""
    return cik.lstrip("0") or "0"


def _archive_url(submissions: dict[str, Any], accession: str, primary_document: str) -> str:
    cik = _cik_for_archive(submissions)
    accession_no_dash = accession.replace("-", "")
    if not cik or not accession_no_dash or not primary_document:
        return ""
    return f"https://www.sec.gov/Archives/edgar/data/{cik}/{accession_no_dash}/{primary_document}"


def _value_at(values: Any, index: int) -> Any:
    if isinstance(values, list) and index < len(values):
        return values[index]
    return None


def _recent_rows(submissions: dict[str, Any]) -> list[dict[str, Any]]:
    recent = ((submissions.get("filings") or {}).get("recent") or {})
    forms = recent.get("form") or []
    rows: list[dict[str, Any]] = []
    for index, form in enumerate(forms):
        accession = str(_value_at(recent.get("accessionNumber"), index) or "")
        primary_document = str(_value_at(recent.get("primaryDocument"), index) or "")
        rows.append(
            {
                "form": str(form),
                "filing_date": _value_at(recent.get("filingDate"), index),
                "report_date": _value_at(recent.get("reportDate"), index),
                "accession": accession,
                "primary_document": primary_document,
                "url": _archive_url(submissions, accession, primary_document),
            }
        )
    return rows


def _select_filings(submissions: dict[str, Any], forms: tuple[str, ...], limit_per_form: int) -> list[dict[str, Any]]:
    counts = {form: 0 for form in forms}
    selected: list[dict[str, Any]] = []
    for row in _recent_rows(submissions):
        form = str(row.get("form") or "")
        if form not in counts or counts[form] >= limit_per_form:
            continue
        if not row.get("url"):
            continue
        counts[form] += 1
        selected.append(row)
    return selected


def _document_path(base_dir: Path, row: dict[str, Any]) -> Path:
    form = _safe_filename(str(row.get("form") or "FORM"))
    filing_date = _safe_filename(str(row.get("filing_date") or "undated"))
    accession = _safe_filename(str(row.get("accession") or "unknown").replace("-", ""))
    primary_document = _safe_filename(str(row.get("primary_document") or "primary.htm"))
    return base_dir / "filings" / f"{form}_{filing_date}_{accession}_{primary_document}.raw.html"


def _meta_path(raw_path: Path) -> Path:
    return raw_path.with_name(f"{raw_path.name}.meta.json")


def _write_meta(path: Path, url: str, response: Any) -> None:
    _write_json(
        path,
        {
            "captured_at_kst": _now_kst().isoformat(),
            "request": _redacted_request(url),
            "status_code": response.status_code,
            "content_type": response.headers.get("content-type", ""),
            "content_length": len(response.text),
        },
    )


def _source_map_lines(
    *,
    symbol: str,
    run_date: str,
    raw_dir: Path,
    selected: list[dict[str, Any]],
    generated_at: str,
) -> list[str]:
    lines = [
        f"# {symbol.upper()} SEC Filing Documents",
        "",
        f"- Run date: `{run_date}`",
        f"- Generated at: `{generated_at}`",
        f"- Raw dir: `{raw_dir.as_posix()}`",
        "- Source: SEC EDGAR primary filing documents collected for DI research",
        "- Interpretation: source map only; no buy or order intent is generated",
        "- Order intent generated: `false`",
        "",
        "## Documents",
        "",
        "| Form | Filing date | Report date | Accession | Primary document | SEC URL | Local raw path |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    if not selected:
        lines.append("| - | - | - | - | - | - | - |")
    for row in selected:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{row.get('form') or '-'}`",
                    str(row.get("filing_date") or "-"),
                    str(row.get("report_date") or "-"),
                    f"`{row.get('accession') or '-'}`",
                    str(row.get("primary_document") or "-"),
                    str(row.get("url") or "-"),
                    f"`{row.get('raw_output') or '-'}`",
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Reading Checklist",
            "",
            "1. Read the latest 10-K Business, Risk Factors, and MD&A sections before writing `thesis.md`.",
            "2. Read the latest 10-Q for recent trend changes, margin pressure, capex, balance sheet changes, and management wording.",
            "3. Use 8-K documents only when they contain earnings, guidance, financing, acquisition, litigation, or other thesis-changing events.",
            "4. Keep the candidate on `hold` until `thesis.md` and `decision.md` are filled from primary-source evidence.",
            "",
        ]
    )
    return lines


def build_dry_run(args: argparse.Namespace) -> dict[str, Any]:
    raw_dir = args.raw_dir or _raw_dir(args.raw_root, args.run_date, args.symbol)
    submissions = _read_json(raw_dir / "submissions.raw.json")
    if not isinstance(submissions, dict):
        raise ValueError(f"{raw_dir / 'submissions.raw.json'}: expected JSON object")
    selected = _select_filings(submissions, tuple(args.forms), args.limit_per_form)
    for row in selected:
        row["raw_output"] = _document_path(raw_dir, row).as_posix()
    return {
        "source": "SEC EDGAR",
        "run_date": args.run_date,
        "symbol": args.symbol,
        "raw_dir": raw_dir.as_posix(),
        "requests": [
            {
                "form": row.get("form"),
                "filing_date": row.get("filing_date"),
                "accession": row.get("accession"),
                "request": _redacted_request(str(row.get("url") or "")),
                "raw_output": row.get("raw_output"),
            }
            for row in selected
        ],
    }


def collect(args: argparse.Namespace) -> dict[str, Any]:
    raw_dir = args.raw_dir or _raw_dir(args.raw_root, args.run_date, args.symbol)
    output = args.output or _research_output_path(args.research_root, args.symbol)
    submissions = _read_json(raw_dir / "submissions.raw.json")
    if not isinstance(submissions, dict):
        raise ValueError(f"{raw_dir / 'submissions.raw.json'}: expected JSON object")
    selected = _select_filings(submissions, tuple(args.forms), args.limit_per_form)
    for row in selected:
        row["raw_output"] = _document_path(raw_dir, row).as_posix()

    if args.dry_run:
        return build_dry_run(args)

    user_agent = _resolve_user_agent(args.env_file)
    import requests

    session = requests.Session()
    calls: list[dict[str, Any]] = []
    for row in selected:
        url = str(row.get("url") or "")
        response = session.get(url, headers=_request_headers(user_agent), timeout=args.timeout)
        raw_path = Path(str(row["raw_output"]))
        _write_text(raw_path, response.text)
        _write_meta(_meta_path(raw_path), url, response)
        calls.append(
            {
                "form": row.get("form"),
                "filing_date": row.get("filing_date"),
                "accession": row.get("accession"),
                "status_code": response.status_code,
                "ok": 200 <= response.status_code < 300,
                "raw_output": raw_path.as_posix(),
            }
        )
        if args.require_success:
            response.raise_for_status()

    generated_at = _now_kst().isoformat()
    report = "\n".join(
        _source_map_lines(
            symbol=args.symbol,
            run_date=args.run_date,
            raw_dir=raw_dir,
            selected=selected,
            generated_at=generated_at,
        )
    )
    _write_text(output, report)
    summary = {
        "source": "SEC EDGAR",
        "run_date": args.run_date,
        "symbol": args.symbol,
        "raw_dir": raw_dir.as_posix(),
        "research_output": output.as_posix(),
        "calls": calls,
    }
    _write_json(raw_dir / "filing_documents_summary.json", summary)
    return summary


def main() -> int:
    default_run_date = _now_kst().date().isoformat()
    parser = argparse.ArgumentParser(description="Collect SEC EDGAR primary filing documents for DI research.")
    parser.add_argument("--symbol", required=True, type=_validate_symbol)
    parser.add_argument("--run-date", type=_validate_ymd, default=default_run_date)
    parser.add_argument("--raw-root", type=Path, default=DEFAULT_RAW_ROOT)
    parser.add_argument("--raw-dir", type=Path)
    parser.add_argument("--research-root", type=Path, default=DEFAULT_RESEARCH_ROOT)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--env-file", type=Path, default=Path(".env.sec"))
    parser.add_argument("--form", action="append", dest="forms", default=None)
    parser.add_argument("--limit-per-form", type=int, default=1)
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--require-success", action="store_true")
    args = parser.parse_args()
    args.forms = args.forms or list(DEFAULT_FORMS)

    try:
        payload = collect(args)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc

    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
