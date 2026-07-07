"""Render a compact SEC EDGAR filing summary from DI raw JSON."""

from __future__ import annotations

import argparse
import json
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
DEFAULT_FORMS = ("10-K", "10-Q", "8-K")
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


def _read_json(path: Path) -> Any:
    if not path.exists():
        raise ValueError(f"{path}: file not found")
    return json.loads(path.read_text(encoding="utf-8"))


def _display(value: Any) -> str:
    if value is None:
        return "-"
    text = str(value).strip()
    return text if text else "-"


def _format_number(value: Any) -> str:
    if isinstance(value, bool):
        return str(value)
    if isinstance(value, int):
        return f"{value:,}"
    if isinstance(value, float):
        return f"{value:,.2f}"
    return _display(value)


def _safe_symbol(symbol: str) -> str:
    cleaned = symbol.strip().upper()
    if not cleaned:
        raise ValueError("symbol is required")
    return cleaned


def _raw_dir(raw_root: Path, run_date: str, symbol: str) -> Path:
    return raw_root / run_date[:4] / run_date / "sec" / _safe_symbol(symbol)


def _output_path(research_root: Path, symbol: str) -> Path:
    return research_root / _safe_symbol(symbol) / "sec-filing-summary.md"


def _cik_for_archive(submissions: dict[str, Any]) -> str:
    cik = str(submissions.get("cik") or "").strip()
    if not cik:
        return ""
    return cik.lstrip("0") or "0"


def _filing_url(submissions: dict[str, Any], accession: str, primary_document: str) -> str:
    cik = _cik_for_archive(submissions)
    accession_no_dash = accession.replace("-", "")
    if not cik or not accession_no_dash:
        return "-"
    base = f"https://www.sec.gov/Archives/edgar/data/{cik}/{accession_no_dash}"
    return f"{base}/{primary_document}" if primary_document else base


def _recent_rows(submissions: dict[str, Any]) -> list[dict[str, Any]]:
    recent = ((submissions.get("filings") or {}).get("recent") or {})
    forms = recent.get("form") or []
    rows: list[dict[str, Any]] = []
    for index, form in enumerate(forms):
        rows.append(
            {
                "form": form,
                "filing_date": _value_at(recent.get("filingDate"), index),
                "report_date": _value_at(recent.get("reportDate"), index),
                "accession": _value_at(recent.get("accessionNumber"), index),
                "primary_document": _value_at(recent.get("primaryDocument"), index),
            }
        )
    return rows


def _value_at(values: Any, index: int) -> Any:
    if isinstance(values, list) and index < len(values):
        return values[index]
    return None


def _select_filings(submissions: dict[str, Any], *, forms: tuple[str, ...], limit_per_form: int) -> list[dict[str, Any]]:
    counts = {form: 0 for form in forms}
    selected: list[dict[str, Any]] = []
    for row in _recent_rows(submissions):
        form = str(row.get("form") or "")
        if form not in counts or counts[form] >= limit_per_form:
            continue
        counts[form] += 1
        selected.append(
            {
                **row,
                "url": _filing_url(submissions, str(row.get("accession") or ""), str(row.get("primary_document") or "")),
            }
        )
    return selected


def _latest_fact(concept_payload: dict[str, Any]) -> dict[str, Any] | None:
    units = concept_payload.get("units") or {}
    if not isinstance(units, dict):
        return None
    unit_name = "USD" if isinstance(units.get("USD"), list) else next((key for key, value in units.items() if isinstance(value, list)), "")
    facts = units.get(unit_name) if unit_name else []
    if not isinstance(facts, list) or not facts:
        return None
    candidates = [fact for fact in facts if isinstance(fact, dict) and fact.get("val") is not None]
    if not candidates:
        return None
    candidates.sort(key=lambda item: (_display(item.get("filed")), _display(item.get("end")), _display(item.get("fy")), _display(item.get("fp"))))
    latest = candidates[-1]
    return {
        "unit": unit_name,
        "value": latest.get("val"),
        "end": latest.get("end"),
        "filed": latest.get("filed"),
        "fy": latest.get("fy"),
        "fp": latest.get("fp"),
        "form": latest.get("form"),
    }


def _latest_financial_filing_date(filings: list[dict[str, Any]]) -> str:
    dates = [
        str(row.get("filing_date") or "")
        for row in filings
        if row.get("form") in {"10-K", "10-Q"} and row.get("filing_date")
    ]
    return max(dates) if dates else ""


def _concept_status(fact: dict[str, Any] | None, latest_financial_filing_date: str) -> str:
    if not fact:
        return "no_fact"
    filed = str(fact.get("filed") or "")
    if latest_financial_filing_date and filed and filed < latest_financial_filing_date:
        return "stale"
    return "ok"


def _concept_rows(raw_dir: Path, concepts: tuple[str, ...], *, latest_financial_filing_date: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for concept in concepts:
        path = raw_dir / "concepts" / f"us-gaap_{concept}.raw.json"
        if not path.exists():
            rows.append({"concept": concept, "status": "missing", "path": path.as_posix()})
            continue
        payload = _read_json(path)
        fact = _latest_fact(payload) if isinstance(payload, dict) else None
        rows.append(
            {
                "concept": concept,
                "status": _concept_status(fact, latest_financial_filing_date),
                "path": path.as_posix(),
                **(fact or {}),
            }
        )
    return rows


def render_summary(
    *,
    raw_dir: Path,
    symbol: str,
    run_date: str,
    forms: tuple[str, ...],
    limit_per_form: int,
    concepts: tuple[str, ...],
) -> str:
    submissions = _read_json(raw_dir / "submissions.raw.json")
    companyfacts = _read_json(raw_dir / "companyfacts.raw.json")
    ticker_lookup_path = raw_dir / "ticker_lookup.json"
    ticker_lookup = _read_json(ticker_lookup_path) if ticker_lookup_path.exists() else {}
    if not isinstance(submissions, dict):
        raise ValueError(f"{raw_dir / 'submissions.raw.json'}: expected JSON object")
    if not isinstance(companyfacts, dict):
        raise ValueError(f"{raw_dir / 'companyfacts.raw.json'}: expected JSON object")
    if not isinstance(ticker_lookup, dict):
        ticker_lookup = {}

    filings = _select_filings(submissions, forms=forms, limit_per_form=limit_per_form)
    concept_rows = _concept_rows(raw_dir, concepts, latest_financial_filing_date=_latest_financial_filing_date(filings))
    taxonomies = ", ".join((companyfacts.get("facts") or {}).keys()) if isinstance(companyfacts.get("facts"), dict) else "-"
    lines = [
        f"# {symbol.upper()} SEC Filing Summary",
        "",
        f"- Run date: `{run_date}`",
        f"- Generated at: `{_now_kst().isoformat()}`",
        f"- Raw dir: `{raw_dir.as_posix()}`",
        f"- Source: SEC EDGAR raw JSON collected for DI research",
        "- Interpretation: source-readiness summary only; no buy or order intent is generated",
        "- Order intent generated: `false`",
        "",
        "## Entity",
        "",
        "| Field | Value |",
        "| --- | --- |",
        f"| Ticker | `{_display(ticker_lookup.get('ticker') or symbol.upper())}` |",
        f"| CIK | `{_display(submissions.get('cik') or ticker_lookup.get('cik_str'))}` |",
        f"| Company | {_display(submissions.get('name') or ticker_lookup.get('title'))} |",
        f"| Companyfacts entity | {_display(companyfacts.get('entityName'))} |",
        f"| Taxonomies | `{taxonomies}` |",
        "",
        "## Latest Core Filings",
        "",
        "| Form | Filing date | Report date | Accession | Primary document | SEC URL |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    if filings:
        for row in filings:
            lines.append(
                "| "
                + " | ".join(
                    [
                        f"`{_display(row.get('form'))}`",
                        _display(row.get("filing_date")),
                        _display(row.get("report_date")),
                        f"`{_display(row.get('accession'))}`",
                        _display(row.get("primary_document")),
                        _display(row.get("url")),
                    ]
                )
                + " |"
            )
    else:
        lines.append("| - | - | - | - | - | - |")
    lines.extend(
        [
            "",
            "## XBRL Concept Snapshot",
            "",
            "| Concept | Status | Latest value | Unit | FY | FP | Period end | Filed | Form |",
            "| --- | --- | ---: | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for row in concept_rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{row['concept']}`",
                    f"`{row['status']}`",
                    _format_number(row.get("value")),
                    _display(row.get("unit")),
                    _display(row.get("fy")),
                    _display(row.get("fp")),
                    _display(row.get("end")),
                    _display(row.get("filed")),
                    _display(row.get("form")),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Next Actions",
            "",
            "1. Read the latest 10-K Business, Risk Factors, and MD&A sections before writing `thesis.md`.",
            "2. Use the latest 10-Q and 8-K filings to check whether the thesis is stale.",
            "3. Convert XBRL facts into `financials.md` only after checking fiscal period alignment and units.",
            "4. Keep the candidate on `hold` until `thesis.md` and `decision.md` contain filled evidence and a checked decision.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    default_run_date = _now_kst().date().isoformat()
    parser = argparse.ArgumentParser(description="Render a compact SEC EDGAR filing summary from DI raw JSON.")
    parser.add_argument("--symbol", required=True)
    parser.add_argument("--run-date", default=default_run_date)
    parser.add_argument("--raw-root", type=Path, default=DEFAULT_RAW_ROOT)
    parser.add_argument("--raw-dir", type=Path)
    parser.add_argument("--research-root", type=Path, default=DEFAULT_RESEARCH_ROOT)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--form", action="append", dest="forms")
    parser.add_argument("--limit-per-form", type=int, default=2)
    parser.add_argument("--concept", action="append", dest="concepts")
    args = parser.parse_args()

    symbol = _safe_symbol(args.symbol)
    raw_dir = args.raw_dir or _raw_dir(args.raw_root, args.run_date, symbol)
    output = args.output or _output_path(args.research_root, symbol)
    forms = tuple(args.forms or DEFAULT_FORMS)
    concepts = tuple(args.concepts or DEFAULT_CONCEPTS)

    try:
        report = render_summary(
            raw_dir=raw_dir,
            symbol=symbol,
            run_date=args.run_date,
            forms=forms,
            limit_per_form=args.limit_per_form,
            concepts=concepts,
        )
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(report, encoding="utf-8")
    print(output.as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
