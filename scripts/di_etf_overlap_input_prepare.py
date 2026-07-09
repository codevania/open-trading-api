"""Prepare gitignored ETF overlap inputs from official holdings evidence."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import yaml


try:
    KST = ZoneInfo("Asia/Seoul")
except Exception:
    KST = timezone(timedelta(hours=9), "KST")

DEFAULT_CANDIDATE_FILE = Path("_report/di/candidates/core-satellite-candidates.yaml")
DEFAULT_RAW_ROOT = Path("_report/raw")
DEFAULT_OUTPUT_FILE = Path("_report/private/di/etf-overlap-inputs.yaml")
DEFAULT_SECTIONS = ("core_etfs", "satellite_etfs_to_verify")
DEFAULT_EQUITY_QUEUE = "primary_queue"
TODO_PORTFOLIO_WEIGHT = "TODO - portfolio percent"
TODO_AS_OF = "TODO - official holdings date"
TODO_SOURCE_URL = "TODO - official issuer holdings or factsheet URL"
TODO_COVERAGE = "TODO - full, candidate_only, or top_n"
TODO_HOLDING_WEIGHT = "TODO - ETF holding percent"
STALE_MANUAL_NOTE = "manual official holdings still required"
UNCHECKED_TOKENS = ("todo", "verify", "check", "needs_", "null", "pending", "none")


def _now_kst() -> datetime:
    return datetime.now(KST).replace(microsecond=0)


def _load_yaml(path: Path) -> dict[str, Any]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path}: expected YAML object")
    return payload


def _load_optional_yaml(path: Path | None) -> dict[str, Any]:
    if path is None or not path.exists():
        return {}
    return _load_yaml(path)


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


def _is_filled(value: Any) -> bool:
    text = _text(value).lower()
    if not text:
        return False
    return not any(token in text for token in UNCHECKED_TOKENS)


def _lookup_case_insensitive(mapping: dict[str, Any], key: str) -> Any:
    for candidate in (key, key.upper(), key.lower()):
        if candidate in mapping:
            return mapping[candidate]
    return None


def _safe_value(existing: Any, fallback: Any, *, refresh: bool) -> Any:
    if refresh:
        return fallback
    return existing if _is_filled(existing) else fallback


def _candidate_etfs(payload: dict[str, Any], *, sections: tuple[str, ...]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for section in sections:
        for index, row in enumerate(_as_list(payload.get(section))):
            if not isinstance(row, dict):
                raise ValueError(f"{section}[{index}]: expected candidate object")
            symbol = _text(row.get("symbol")).upper()
            if not symbol:
                raise ValueError(f"{section}[{index}]: missing symbol")
            rows.append(
                {
                    "section": section,
                    "symbol": symbol,
                    "name": _text(row.get("name")),
                    "source_url": _text(row.get("source_url")),
                }
            )
    return rows


def _candidate_equity_symbols(payload: dict[str, Any], *, equity_queue: str) -> tuple[str, ...]:
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


def _holding_dir(raw_root: Path, run_date: str, symbol: str) -> Path:
    return raw_root / run_date[:4] / run_date / "di" / "etf-holdings" / symbol.upper()


def _normalized_path(raw_root: Path, run_date: str, symbol: str) -> Path:
    return _holding_dir(raw_root, run_date, symbol) / "holdings.normalized.json"


def _load_normalized(raw_root: Path, run_date: str, symbol: str) -> dict[str, Any] | None:
    path = _normalized_path(raw_root, run_date, symbol)
    if not path.exists():
        return None
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path}: expected JSON object")
    return payload


def _existing_etf_row(existing_payload: dict[str, Any], symbol: str) -> dict[str, Any]:
    holdings_root = existing_payload.get("etf_holdings") or {}
    if holdings_root and not isinstance(holdings_root, dict):
        raise ValueError("existing etf overlap input: expected etf_holdings object")
    row = _lookup_case_insensitive(holdings_root, symbol) or {}
    if not isinstance(row, dict):
        raise ValueError(f"existing etf_holdings.{symbol}: expected object")
    return row


def _existing_holdings(row: dict[str, Any], symbol: str) -> dict[str, Any]:
    holdings = row.get("holdings") or {}
    if holdings and not isinstance(holdings, dict):
        raise ValueError(f"existing etf_holdings.{symbol}.holdings: expected object")
    return {str(key).upper(): value for key, value in holdings.items()}


def _existing_portfolio_weight(existing_payload: dict[str, Any], symbol: str) -> Any:
    weights = existing_payload.get("portfolio_etf_weights") or existing_payload.get("portfolio_weights") or {}
    if weights and not isinstance(weights, dict):
        raise ValueError("existing etf overlap input: expected portfolio_etf_weights object")
    return _lookup_case_insensitive(weights, symbol)


def _holding_value(
    *,
    existing_holdings: dict[str, Any],
    normalized: dict[str, Any] | None,
    equity_symbol: str,
    refresh_official: bool,
) -> Any:
    existing = existing_holdings.get(equity_symbol)
    if normalized:
        candidate_holdings = normalized.get("candidate_holdings") or {}
        if not isinstance(candidate_holdings, dict):
            raise ValueError("normalized holdings: expected candidate_holdings object")
        normalized_value = _lookup_case_insensitive(candidate_holdings, equity_symbol)
        if normalized_value is not None:
            return _safe_value(existing, normalized_value, refresh=refresh_official)
    return existing if _is_filled(existing) else TODO_HOLDING_WEIGHT


def _notes(existing_row: dict[str, Any], normalized: dict[str, Any] | None) -> list[str]:
    notes: list[str] = []
    existing_notes = existing_row.get("notes")
    for value in _as_list(existing_notes):
        text = _text(value)
        if normalized and text == STALE_MANUAL_NOTE:
            continue
        if text and text not in notes:
            notes.append(text)
    if normalized:
        share_class_notes = normalized.get("share_class_notes") or {}
        if isinstance(share_class_notes, dict):
            for value in share_class_notes.values():
                text = _text(value)
                if text and text not in notes:
                    notes.append(text)
    if not notes:
        if normalized:
            notes.append("official holdings prefilled from normalized raw evidence")
        else:
            notes.append(STALE_MANUAL_NOTE)
    return notes


def prepare_inputs(
    candidate_payload: dict[str, Any],
    *,
    existing_payload: dict[str, Any],
    candidate_file: Path,
    raw_root: Path,
    run_date: str,
    sections: tuple[str, ...],
    equity_queue: str,
    refresh_official: bool,
) -> tuple[dict[str, Any], dict[str, Any]]:
    etfs = _candidate_etfs(candidate_payload, sections=sections)
    equity_symbols = _candidate_equity_symbols(candidate_payload, equity_queue=equity_queue)
    generated_at = _now_kst().isoformat()

    portfolio_weights: dict[str, Any] = {}
    etf_holdings: dict[str, Any] = {}
    autofilled: list[dict[str, Any]] = []
    manual_required: list[str] = []

    for etf in etfs:
        symbol = etf["symbol"]
        existing_row = _existing_etf_row(existing_payload, symbol)
        existing_holdings = _existing_holdings(existing_row, symbol)
        normalized = _load_normalized(raw_root, run_date, symbol)

        existing_weight = _existing_portfolio_weight(existing_payload, symbol)
        portfolio_weights[symbol] = existing_weight if _is_filled(existing_weight) else TODO_PORTFOLIO_WEIGHT

        as_of = _safe_value(existing_row.get("as_of"), normalized.get("as_of") if normalized else TODO_AS_OF, refresh=refresh_official)
        source_url_fallback = etf["source_url"] or TODO_SOURCE_URL
        source_url = _safe_value(existing_row.get("source_url"), source_url_fallback, refresh=refresh_official)
        coverage = _safe_value(
            existing_row.get("coverage"),
            normalized.get("coverage") if normalized else TODO_COVERAGE,
            refresh=refresh_official,
        )
        holdings = {
            equity_symbol: _holding_value(
                existing_holdings=existing_holdings,
                normalized=normalized,
                equity_symbol=equity_symbol,
                refresh_official=refresh_official,
            )
            for equity_symbol in equity_symbols
        }
        etf_holdings[symbol] = {
            "as_of": as_of,
            "source_url": source_url,
            "coverage": coverage,
            "holdings": holdings,
            "notes": _notes(existing_row, normalized),
        }

        if normalized:
            filled_symbols = [
                equity_symbol
                for equity_symbol, value in holdings.items()
                if _is_filled(value) and value != TODO_HOLDING_WEIGHT
            ]
            autofilled.append(
                {
                    "symbol": symbol,
                    "normalized_path": _normalized_path(raw_root, run_date, symbol).as_posix(),
                    "as_of": normalized.get("as_of"),
                    "coverage": normalized.get("coverage"),
                    "filled_candidate_symbols": filled_symbols,
                }
            )
        else:
            manual_required.append(symbol)

    prepared = {
        "version": 1,
        "purpose": (
            "Private ETF overlap input. Fill personal ETF portfolio weights manually; "
            "official holdings may be prefilled from ignored raw evidence."
        ),
        "source_inputs": {
            "candidate_file": candidate_file.as_posix(),
            "raw_root": raw_root.as_posix(),
            "run_date": run_date,
            "generated_at_kst": generated_at,
            "generated_by": "scripts/di_etf_overlap_input_prepare.py",
        },
        "notes": [
            "Keep this file under _report/private; it can contain private portfolio weights after editing.",
            "Use 0 for ETFs deliberately not held.",
            "For GOOGL, decide whether to combine GOOG when the official source reports share classes separately.",
        ],
        "portfolio_etf_weights": portfolio_weights,
        "etf_holdings": etf_holdings,
    }
    summary = {
        "run_date": run_date,
        "candidate_file": candidate_file.as_posix(),
        "raw_root": raw_root.as_posix(),
        "equity_queue": equity_queue,
        "candidate_symbols": list(equity_symbols),
        "etf_symbols": [etf["symbol"] for etf in etfs],
        "autofilled_etfs": autofilled,
        "manual_required_etfs": manual_required,
        "private_weight_fields": list(portfolio_weights),
        "order_intent_generated": False,
    }
    return prepared, summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare private ETF overlap inputs from official holdings evidence.")
    parser.add_argument("--candidate-file", type=Path, default=DEFAULT_CANDIDATE_FILE)
    parser.add_argument("--raw-root", type=Path, default=DEFAULT_RAW_ROOT)
    parser.add_argument("--run-date", default=_now_kst().date().isoformat())
    parser.add_argument("--section", choices=DEFAULT_SECTIONS, action="append", dest="sections")
    parser.add_argument("--equity-queue", choices=("primary_queue", "secondary_queue", "all"), default=DEFAULT_EQUITY_QUEUE)
    parser.add_argument("--input-file", type=Path, default=DEFAULT_OUTPUT_FILE, help="Existing private YAML to preserve.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_FILE, help="Prepared private YAML output path.")
    parser.add_argument("--refresh-official", action="store_true", help="Overwrite existing official ETF fields with normalized raw evidence.")
    parser.add_argument("--dry-run", action="store_true", help="Print summary without writing the private YAML.")
    args = parser.parse_args()

    try:
        candidate_payload = _load_yaml(args.candidate_file)
        existing_payload = _load_optional_yaml(args.input_file)
        prepared, summary = prepare_inputs(
            candidate_payload,
            existing_payload=existing_payload,
            candidate_file=args.candidate_file,
            raw_root=args.raw_root,
            run_date=args.run_date,
            sections=tuple(args.sections or DEFAULT_SECTIONS),
            equity_queue=args.equity_queue,
            refresh_official=args.refresh_official,
        )
    except (ValueError, json.JSONDecodeError) as exc:
        raise SystemExit(str(exc)) from exc

    summary["output"] = args.output.as_posix()
    summary["dry_run"] = args.dry_run
    if not args.dry_run:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(yaml.safe_dump(prepared, sort_keys=False, allow_unicode=True), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
