"""Estimate ETF overlap for DI satellite equity candidates."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
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
DEFAULT_INPUT_FILE = Path("_report/private/di/etf-overlap-inputs.yaml")
UNCHECKED_TOKENS = ("todo", "verify", "check", "needs_", "null", "pending", "none")


@dataclass(frozen=True)
class OverlapRow:
    queue: str
    symbol: str
    name: str
    status: str
    etf_weights: tuple[str, ...]
    portfolio_overlap: str
    missing_inputs: tuple[str, ...]
    safe_next_action: str


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


def _parse_percent(value: Any, *, field: str) -> float | None:
    if not _is_filled(value):
        return None
    if isinstance(value, int | float):
        return float(value)
    text = _text(value).replace("%", "").strip()
    try:
        return float(text)
    except ValueError as exc:
        raise ValueError(f"{field}: expected numeric percent, got {value!r}") from exc


def _lookup_case_insensitive(mapping: dict[str, Any], key: str) -> Any:
    for candidate in (key, key.upper(), key.lower()):
        if candidate in mapping:
            return mapping[candidate]
    return None


def _candidate_rows(payload: dict[str, Any], queue: str) -> list[tuple[str, dict[str, Any]]]:
    satellite = payload.get("satellite_equities") or {}
    if not isinstance(satellite, dict):
        raise ValueError("satellite_equities: expected object")
    queues = ("primary_queue", "secondary_queue") if queue == "all" else (queue,)
    rows: list[tuple[str, dict[str, Any]]] = []
    for queue_name in queues:
        for row in _as_list(satellite.get(queue_name)):
            if not isinstance(row, dict):
                raise ValueError(f"satellite_equities.{queue_name}: expected candidate objects")
            rows.append((queue_name, row))
    return rows


def _expected_etfs(candidate_payload: dict[str, Any], input_payload: dict[str, Any]) -> tuple[str, ...]:
    symbols: list[str] = []
    for section in ("core_etfs", "satellite_etfs_to_verify"):
        for row in _as_list(candidate_payload.get(section)):
            if not isinstance(row, dict):
                raise ValueError(f"{section}: expected candidate objects")
            symbol = _text(row.get("symbol")).upper()
            if symbol and symbol not in symbols:
                symbols.append(symbol)

    holdings = input_payload.get("etf_holdings") or {}
    if holdings and not isinstance(holdings, dict):
        raise ValueError("etf_overlap input: expected etf_holdings object")
    for symbol in holdings:
        normalized = _text(symbol).upper()
        if normalized and normalized not in symbols:
            symbols.append(normalized)
    return tuple(symbols)


def _holding_map(input_payload: dict[str, Any], etf_symbol: str) -> dict[str, Any]:
    holdings_root = input_payload.get("etf_holdings") or {}
    row = _lookup_case_insensitive(holdings_root, etf_symbol) or {}
    if not isinstance(row, dict):
        raise ValueError(f"etf_holdings.{etf_symbol}: expected object")
    holdings = row.get("holdings") or {}
    if not isinstance(holdings, dict):
        raise ValueError(f"etf_holdings.{etf_symbol}.holdings: expected object")
    return {str(key).upper(): value for key, value in holdings.items()}


def _has_source_meta(input_payload: dict[str, Any], etf_symbol: str) -> bool:
    holdings_root = input_payload.get("etf_holdings") or {}
    row = _lookup_case_insensitive(holdings_root, etf_symbol) or {}
    if not isinstance(row, dict):
        return False
    return all(_is_filled(row.get(key)) for key in ("as_of", "source_url", "coverage"))


def _portfolio_weight(input_payload: dict[str, Any], etf_symbol: str) -> float | None:
    weights = input_payload.get("portfolio_etf_weights") or input_payload.get("portfolio_weights") or {}
    if weights and not isinstance(weights, dict):
        raise ValueError("etf_overlap input: expected portfolio_etf_weights object")
    value = _lookup_case_insensitive(weights, etf_symbol)
    return _parse_percent(value, field=f"portfolio_etf_weights.{etf_symbol}")


def _format_percent(value: float) -> str:
    return f"{value:.2f}%"


def _format_pp(value: float) -> str:
    return f"{value:.2f}pp"


def evaluate_overlap(
    candidate_payload: dict[str, Any],
    *,
    input_payload: dict[str, Any],
    queue: str,
) -> list[OverlapRow]:
    etfs = _expected_etfs(candidate_payload, input_payload)
    results: list[OverlapRow] = []

    for queue_name, row in _candidate_rows(candidate_payload, queue):
        symbol = _text(row.get("symbol")).upper()
        if not symbol:
            raise ValueError(f"satellite_equities.{queue_name}: missing symbol")

        missing: list[str] = []
        etf_weights: list[str] = []
        overlap_pp = 0.0
        overlap_ready = True

        for etf in etfs:
            if not _has_source_meta(input_payload, etf):
                missing.append(f"{etf}:source_meta")
                overlap_ready = False

            holdings = _holding_map(input_payload, etf)
            holding_weight = _parse_percent(holdings.get(symbol), field=f"etf_holdings.{etf}.holdings.{symbol}")
            if holding_weight is None:
                missing.append(f"{etf}:{symbol}_weight")
                overlap_ready = False
                etf_weights.append(f"{etf}=needs_weight")
            else:
                etf_weights.append(f"{etf}={_format_percent(holding_weight)}")

            portfolio_weight = _portfolio_weight(input_payload, etf)
            if portfolio_weight is None:
                missing.append(f"{etf}:portfolio_weight")
                overlap_ready = False
            elif holding_weight is not None:
                overlap_pp += portfolio_weight * holding_weight / 100.0

        status = "ready_for_private_decision_input" if overlap_ready else "needs_overlap_inputs"
        results.append(
            OverlapRow(
                queue=queue_name,
                symbol=symbol,
                name=_text(row.get("name")),
                status=status,
                etf_weights=tuple(etf_weights),
                portfolio_overlap=_format_pp(overlap_pp) if overlap_ready else "needs_input",
                missing_inputs=tuple(missing),
                safe_next_action=(
                    "copy overlap summary into private satellite-decision-inputs.yaml"
                    if overlap_ready
                    else "fill official ETF holding weights, source dates, and private ETF portfolio weights"
                ),
            )
        )
    return results


def _render_list(values: tuple[str, ...]) -> str:
    return ", ".join(f"`{value}`" for value in values) if values else "-"


def _cell(value: str) -> str:
    return value.replace("|", "\\|")


def render_report(
    rows: list[OverlapRow],
    *,
    candidate_file: Path,
    input_file: Path | None,
    run_date: str,
    queue: str,
) -> str:
    ready = sum(1 for row in rows if row.status == "ready_for_private_decision_input")
    lines = [
        "# DI ETF Overlap Check",
        "",
        f"- Run date: `{run_date}`",
        f"- Candidate manifest: `{candidate_file.as_posix()}`",
        f"- ETF overlap input file: `{input_file.as_posix() if input_file else 'not configured'}`",
        f"- Queue scope: `{queue}`",
        "- Interpretation: overlap-prep only; no buy, sell, hold, or order intent is generated",
        "- Order intent generated: `false`",
        "- Formula: `portfolio ETF weight * ETF holding weight / 100 = portfolio overlap percentage points`",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| Candidates checked | {len(rows)} |",
        f"| Ready for private decision input | {ready} |",
        f"| Needs overlap inputs | {len(rows) - ready} |",
        "",
        "## Candidate Overlap State",
        "",
        "| Queue | Symbol | Name | Status | ETF holding weights | Portfolio overlap estimate | Missing before etf_overlap_checked | Safe next action |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{row.queue}`",
                    f"`{row.symbol}`",
                    _cell(row.name),
                    f"`{row.status}`",
                    _render_list(row.etf_weights),
                    f"`{row.portfolio_overlap}`",
                    _render_list(row.missing_inputs),
                    _cell(row.safe_next_action),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Input Rules",
            "",
            "- Use official issuer holdings or factsheet data and record `as_of`, `source_url`, and `coverage` for every ETF checked.",
            "- Put personal ETF portfolio weights only in the gitignored private input file.",
            "- Use `0` for an ETF that is deliberately not held, rather than leaving the field blank.",
            "- For `GOOGL`, confirm whether the ETF source separates `GOOGL` and `GOOG` share classes before copying the result into a decision input.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Estimate ETF overlap for DI satellite equity candidates.")
    parser.add_argument("--candidate-file", type=Path, default=DEFAULT_CANDIDATE_FILE)
    parser.add_argument("--input-file", type=Path, default=DEFAULT_INPUT_FILE)
    parser.add_argument("--queue", choices=("primary_queue", "secondary_queue", "all"), default="primary_queue")
    parser.add_argument("--run-date", default=_now_kst().date().isoformat())
    parser.add_argument("--output", type=Path, help="Markdown report output path. Prints to stdout when omitted.")
    args = parser.parse_args()

    try:
        candidate_payload = _load_yaml(args.candidate_file)
        input_payload = _load_optional_yaml(args.input_file)
        rows = evaluate_overlap(candidate_payload, input_payload=input_payload, queue=args.queue)
        report = render_report(
            rows,
            candidate_file=args.candidate_file,
            input_file=args.input_file,
            run_date=args.run_date,
            queue=args.queue,
        )
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(report, encoding="utf-8")
    else:
        print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
