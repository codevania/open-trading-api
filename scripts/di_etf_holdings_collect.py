"""Collect official ETF holdings evidence for DI overlap checks."""

from __future__ import annotations

import argparse
import json
import os
import re
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import requests
import yaml


try:
    KST = ZoneInfo("Asia/Seoul")
except Exception:
    KST = timezone(timedelta(hours=9), "KST")

DEFAULT_CANDIDATE_FILE = Path("_report/di/candidates/core-satellite-candidates.yaml")
DEFAULT_RAW_ROOT = Path("_report/raw")
DEFAULT_SECTIONS = ("core_etfs", "satellite_etfs_to_verify")
DEFAULT_EQUITY_QUEUE = "primary_queue"
DEFAULT_USER_AGENT = "open-trading-api-di-research/1.0 (personal ETF holdings snapshot)"
SAFE_SYMBOL_PATTERN = re.compile(r"[^A-Za-z0-9._-]+")
EMPTY_SOURCE_URL_TOKENS = {"", "null", "none", "todo", "verify"}
INVESCO_QQQ_HOLDINGS_URL = (
    "https://dng-api.invesco.com/cache/v1/accounts/en_US/shareclasses/QQQ/holdings/fund"
    "?idType=ticker&interval=monthly&productType=ETF"
)
INVESCO_QQQ_SOURCE_URL = "https://www.invesco.com/qqq-etf/en/about.html"


@dataclass(frozen=True)
class EtfHoldingSource:
    section: str
    symbol: str
    name: str
    provider: str
    source_url: str
    holdings_url: str
    source_state: str
    notes: str


def _now_kst() -> datetime:
    return datetime.now(KST).replace(microsecond=0)


def _load_yaml(path: Path) -> dict[str, Any]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path}: expected YAML object")
    return payload


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def _text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _safe_symbol(symbol: str) -> str:
    safe = SAFE_SYMBOL_PATTERN.sub("_", symbol.upper()).strip("._-")
    if not safe:
        raise ValueError("symbol resolves to an empty path segment")
    return safe


def _collection_root(raw_root: Path, run_date: str) -> Path:
    return raw_root / run_date[:4] / run_date / "di" / "etf-holdings"


def _holding_dir(raw_root: Path, run_date: str, symbol: str) -> Path:
    return _collection_root(raw_root, run_date) / _safe_symbol(symbol)


def _provider_for(symbol: str, source_url: str) -> tuple[str, str, str, str]:
    normalized = symbol.upper()
    url_lower = source_url.lower()
    if normalized == "QQQ" and "invesco.com" in url_lower:
        return (
            "invesco",
            INVESCO_QQQ_HOLDINGS_URL,
            "confirmed_api",
            "official page exposes data-holding-api for QQQ holdings",
        )
    if "investor.vanguard.com" in url_lower:
        return (
            "vanguard",
            "",
            "manual_official_source_required",
            "official profile page exists, but a stable holdings API was not confirmed",
        )
    if not source_url:
        return ("unknown", "", "missing_source_url", "candidate manifest has no source_url")
    return (
        "manual",
        "",
        "manual_official_source_required",
        "record official issuer holdings before using this ETF in overlap inputs",
    )


def iter_holding_sources(
    payload: dict[str, Any],
    *,
    sections: tuple[str, ...],
    symbols: tuple[str, ...],
) -> list[EtfHoldingSource]:
    filters = {symbol.upper() for symbol in symbols}
    sources: list[EtfHoldingSource] = []
    for section in sections:
        for index, row in enumerate(_as_list(payload.get(section))):
            if not isinstance(row, dict):
                raise ValueError(f"{section}[{index}]: expected candidate object")
            symbol = _text(row.get("symbol")).upper()
            if not symbol:
                raise ValueError(f"{section}[{index}]: missing symbol")
            if filters and symbol not in filters:
                continue
            source_url = _text(row.get("source_url"))
            if source_url.lower() in EMPTY_SOURCE_URL_TOKENS:
                source_url = ""
            provider, holdings_url, source_state, notes = _provider_for(symbol, source_url)
            sources.append(
                EtfHoldingSource(
                    section=section,
                    symbol=symbol,
                    name=_text(row.get("name")),
                    provider=provider,
                    source_url=source_url,
                    holdings_url=holdings_url,
                    source_state=source_state,
                    notes=notes,
                )
            )
    return sources


def candidate_equity_symbols(payload: dict[str, Any], *, equity_queue: str) -> tuple[str, ...]:
    satellite = payload.get("satellite_equities") or {}
    if not isinstance(satellite, dict):
        raise ValueError("satellite_equities: expected object")
    queue_names = ("primary_queue", "secondary_queue") if equity_queue == "all" else (equity_queue,)
    symbols: list[str] = []
    for queue_name in queue_names:
        for index, row in enumerate(_as_list(satellite.get(queue_name))):
            if not isinstance(row, dict):
                raise ValueError(f"satellite_equities.{queue_name}[{index}]: expected candidate object")
            symbol = _text(row.get("symbol")).upper()
            if symbol and symbol not in symbols:
                symbols.append(symbol)
    return tuple(symbols)


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _invesco_headers(user_agent: str) -> dict[str, str]:
    return {
        "Accept": "application/json",
        "User-Agent": user_agent,
        "Origin": "https://www.invesco.com",
        "Referer": INVESCO_QQQ_SOURCE_URL,
        "X-Requested-With": "XMLHttpRequest",
    }


def _parse_float(value: Any) -> float | None:
    if value is None:
        return None
    if isinstance(value, int | float):
        return float(value)
    text = _text(value).replace("%", "")
    if not text:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def normalize_invesco_holdings(payload: dict[str, Any], candidate_symbols: tuple[str, ...]) -> dict[str, Any]:
    holdings = payload.get("holdings")
    if not isinstance(holdings, list):
        raise ValueError("Invesco holdings payload: expected holdings list")

    rows: list[dict[str, Any]] = []
    weights: dict[str, float] = {}
    for index, holding in enumerate(holdings):
        if not isinstance(holding, dict):
            raise ValueError(f"Invesco holdings payload: holdings[{index}] expected object")
        ticker = _text(holding.get("ticker")).upper()
        weight = _parse_float(holding.get("percentageOfTotalNetAssets"))
        if ticker and weight is not None:
            weights[ticker] = weight
        rows.append(
            {
                "ticker": ticker or None,
                "issuer_name": _text(holding.get("issuerName")) or None,
                "weight_pct": weight,
                "security_type": _text(holding.get("securityTypeName")) or None,
                "currency": _text(holding.get("currency")) or None,
                "cusip": _text(holding.get("cusip")) or None,
            }
        )

    candidate_weights = {symbol: weights.get(symbol) for symbol in candidate_symbols}
    share_class_notes: dict[str, str] = {}
    if "GOOGL" in candidate_symbols and weights.get("GOOG") is not None:
        share_class_notes["GOOGL"] = (
            f"GOOG is reported separately at {weights['GOOG']:.6f}%; "
            "decide whether to combine Alphabet classes in the private overlap input."
        )

    return {
        "provider": "invesco",
        "as_of": _text(payload.get("effectiveBusinessDate")) or _text(payload.get("effectiveDate")),
        "effective_date": _text(payload.get("effectiveDate")),
        "total_number_of_holdings": payload.get("totalNumberOfHoldings"),
        "coverage": "full" if len(rows) == payload.get("totalNumberOfHoldings") else "reported_holdings",
        "candidate_holdings": candidate_weights,
        "share_class_notes": share_class_notes,
        "holdings": rows,
    }


def build_summary(
    sources: list[EtfHoldingSource],
    *,
    candidate_symbols: tuple[str, ...],
    candidate_file: Path,
    raw_root: Path,
    run_date: str,
    dry_run: bool,
    results: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    return {
        "source": "DI ETF official holdings sources",
        "run_date": run_date,
        "generated_at_kst": _now_kst().isoformat(),
        "candidate_file": candidate_file.as_posix(),
        "raw_root": raw_root.as_posix(),
        "dry_run": dry_run,
        "order_intent_generated": False,
        "candidate_symbols": list(candidate_symbols),
        "source_count": len(sources),
        "sources": [
            {
                **asdict(source),
                "output_dir": _holding_dir(raw_root, run_date, source.symbol).as_posix(),
                "live_fetch_supported": bool(source.holdings_url and source.source_state == "confirmed_api"),
            }
            for source in sources
        ],
        "results": results or [],
    }


def collect_holdings(
    sources: list[EtfHoldingSource],
    *,
    candidate_symbols: tuple[str, ...],
    candidate_file: Path,
    raw_root: Path,
    run_date: str,
    timeout: float,
    user_agent: str,
) -> dict[str, Any]:
    session = requests.Session()
    results: list[dict[str, Any]] = []
    fetched_at = _now_kst().isoformat()

    for source in sources:
        output_dir = _holding_dir(raw_root, run_date, source.symbol)
        output_dir.mkdir(parents=True, exist_ok=True)
        if source.source_state != "confirmed_api" or not source.holdings_url:
            results.append(
                {
                    **asdict(source),
                    "status": "skipped_unresolved_source",
                    "fetched_at_kst": fetched_at,
                    "raw_path": "",
                    "normalized_path": "",
                }
            )
            continue

        raw_path = output_dir / "holdings.raw.json"
        meta_path = output_dir / "holdings.raw.json.meta.json"
        normalized_path = output_dir / "holdings.normalized.json"
        try:
            headers = _invesco_headers(user_agent) if source.provider == "invesco" else {"User-Agent": user_agent}
            response = session.get(source.holdings_url, headers=headers, timeout=timeout, allow_redirects=True)
            raw_path.write_bytes(response.content)
            response.raise_for_status()
            payload = response.json()
            if not isinstance(payload, dict):
                raise ValueError(f"{source.symbol}: holdings response expected JSON object")
            normalized = (
                normalize_invesco_holdings(payload, candidate_symbols)
                if source.provider == "invesco"
                else {"provider": source.provider, "candidate_holdings": {}}
            )
            _write_json(normalized_path, normalized)
            result = {
                **asdict(source),
                "status": "collected",
                "fetched_at_kst": fetched_at,
                "requested_url": source.holdings_url,
                "final_url": response.url,
                "status_code": response.status_code,
                "content_type": response.headers.get("content-type", ""),
                "bytes": len(response.content),
                "raw_path": raw_path.as_posix(),
                "normalized_path": normalized_path.as_posix(),
                "as_of": normalized.get("as_of"),
                "coverage": normalized.get("coverage"),
                "candidate_holdings": normalized.get("candidate_holdings", {}),
                "share_class_notes": normalized.get("share_class_notes", {}),
            }
        except (requests.RequestException, ValueError, json.JSONDecodeError) as exc:
            result = {
                **asdict(source),
                "status": "failed",
                "fetched_at_kst": fetched_at,
                "error_type": exc.__class__.__name__,
                "error": str(exc),
                "raw_path": raw_path.as_posix(),
                "normalized_path": normalized_path.as_posix(),
            }
        _write_json(meta_path, result)
        results.append(result)

    summary = build_summary(
        sources,
        candidate_symbols=candidate_symbols,
        candidate_file=candidate_file,
        raw_root=raw_root,
        run_date=run_date,
        dry_run=False,
        results=results,
    )
    _write_json(_collection_root(raw_root, run_date) / "collection_summary.json", summary)
    return summary


def _cell(value: Any) -> str:
    return _text(value).replace("|", "\\|") or "-"


def _repo_link(path_value: Any) -> str:
    path = _text(path_value).replace("\\", "/")
    if not path:
        return "-"
    label = Path(path).name or path
    return f"[[{path}|{label}]]"


def _holding_cell(result: dict[str, Any], symbol: str) -> str:
    holdings = result.get("candidate_holdings") or {}
    value = holdings.get(symbol)
    if isinstance(value, int | float):
        return f"{float(value):.4f}%"
    return "-"


def render_report(summary: dict[str, Any]) -> str:
    candidate_symbols = tuple(summary.get("candidate_symbols") or ())
    lines = [
        "# DI ETF Holdings Source Status",
        "",
        f"- Run date: `{summary['run_date']}`",
        f"- Candidate manifest: {_repo_link(summary['candidate_file'])}",
        f"- Raw root: `{summary['raw_root']}`",
        "- Interpretation: official holdings evidence only; no buy, sell, hold, or order intent is generated",
        f"- Order intent generated: `{str(summary['order_intent_generated']).lower()}`",
        "- Private portfolio ETF weights stay only in [[_report/private/di/etf-overlap-inputs.yaml|etf-overlap-inputs.yaml]].",
        "",
        "## Source Coverage",
        "",
        "| ETF | Provider | Source state | Live fetch | Official source | Holdings API | Notes |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for source in summary["sources"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{source['symbol']}`",
                    f"`{source['provider']}`",
                    f"`{source['source_state']}`",
                    "`yes`" if source.get("live_fetch_supported") else "`no`",
                    _cell(source.get("source_url")),
                    _cell(source.get("holdings_url")),
                    _cell(source.get("notes")),
                ]
            )
            + " |"
        )

    lines.extend(["", "## Collected Candidate Weights", ""])
    if summary.get("dry_run"):
        lines.append("- Dry run only; run without `--dry-run` to save ignored raw holdings evidence.")
    elif not summary.get("results"):
        lines.append("- No collection results were recorded.")
    else:
        header = ["ETF", "Status", "As of", "Coverage", *candidate_symbols, "Notes"]
        lines.append("| " + " | ".join(header) + " |")
        lines.append("| " + " | ".join(["---"] * len(header)) + " |")
        for result in summary["results"]:
            notes = "; ".join((result.get("share_class_notes") or {}).values()) or result.get("notes") or ""
            lines.append(
                "| "
                + " | ".join(
                    [
                        f"`{result.get('symbol', '')}`",
                        f"`{result.get('status', '')}`",
                        _cell(result.get("as_of")),
                        _cell(result.get("coverage")),
                        *[_holding_cell(result, symbol) for symbol in candidate_symbols],
                        _cell(notes),
                    ]
                )
                + " |"
            )

    lines.extend(
        [
            "",
            "## Next Use",
            "",
            "1. Copy only official holding weights into the gitignored overlap input file.",
            "2. Add private ETF portfolio weights there, not in this public report.",
            "3. Rerun [[scripts/di_etf_overlap_check.py|di_etf_overlap_check.py]] before marking `etf_overlap_checked`.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect official ETF holdings evidence for DI overlap checks.")
    parser.add_argument("--candidate-file", type=Path, default=DEFAULT_CANDIDATE_FILE)
    parser.add_argument("--raw-root", type=Path, default=DEFAULT_RAW_ROOT)
    parser.add_argument("--run-date", default=_now_kst().date().isoformat())
    parser.add_argument("--section", choices=DEFAULT_SECTIONS, action="append", dest="sections")
    parser.add_argument("--symbol", action="append", dest="symbols", default=[])
    parser.add_argument("--equity-queue", choices=("primary_queue", "secondary_queue", "all"), default=DEFAULT_EQUITY_QUEUE)
    parser.add_argument("--timeout", type=float, default=20.0)
    parser.add_argument("--user-agent", default=os.environ.get("ETF_USER_AGENT") or os.environ.get("SEC_USER_AGENT") or DEFAULT_USER_AGENT)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--output", type=Path, help="Markdown status report output path.")
    args = parser.parse_args()

    try:
        payload = _load_yaml(args.candidate_file)
        sections = tuple(args.sections or DEFAULT_SECTIONS)
        symbols = tuple(args.symbols or ())
        sources = iter_holding_sources(payload, sections=sections, symbols=symbols)
        candidate_symbols = candidate_equity_symbols(payload, equity_queue=args.equity_queue)
        if args.dry_run:
            summary = build_summary(
                sources,
                candidate_symbols=candidate_symbols,
                candidate_file=args.candidate_file,
                raw_root=args.raw_root,
                run_date=args.run_date,
                dry_run=True,
            )
        else:
            summary = collect_holdings(
                sources,
                candidate_symbols=candidate_symbols,
                candidate_file=args.candidate_file,
                raw_root=args.raw_root,
                run_date=args.run_date,
                timeout=args.timeout,
                user_agent=args.user_agent,
            )
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(render_report(summary), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
