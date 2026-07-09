"""Report DI private-input completeness without printing private values."""

from __future__ import annotations

import argparse
from collections import Counter
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
DEFAULT_ETF_INPUT_FILE = Path("_report/private/di/etf-overlap-inputs.yaml")
DEFAULT_DECISION_INPUT_FILE = Path("_report/private/di/satellite-decision-inputs.yaml")

DECISION_INPUT_FIELDS = {
    "latest_price_checked": "record latest price, currency, timestamp, and source",
    "valuation_range_checked": "record base, bear, and bull valuation range",
    "reverse_dcf_checked": "record scenario or reverse-DCF assumptions",
    "etf_overlap_checked": "record core/satellite ETF overlap summary",
    "tax_account_route": "record taxable, ISA, pension, or IRP route",
    "max_position_size": "record maximum single-name weight",
    "add_trim_rule": "record add, trim, and stop-adding rule",
    "source_freshness_checked": "record filing, price, holdings, and tax check dates",
}
UNCHECKED_TOKENS = ("todo", "verify", "needs_", "pending", "null", "none", "tbd", "unknown")


@dataclass(frozen=True)
class PrivateInputStatus:
    area: str
    symbol: str
    field: str
    status: str
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


def _lookup_case_insensitive(mapping: dict[str, Any], key: str) -> Any:
    for candidate in (key, key.upper(), key.lower()):
        if candidate in mapping:
            return mapping[candidate]
    return None


def _expected_etfs(candidate_payload: dict[str, Any], etf_input_payload: dict[str, Any]) -> tuple[str, ...]:
    symbols: list[str] = []
    for section in ("core_etfs", "satellite_etfs_to_verify"):
        for row in _as_list(candidate_payload.get(section)):
            if not isinstance(row, dict):
                raise ValueError(f"{section}: expected candidate objects")
            symbol = _text(row.get("symbol")).upper()
            if symbol and symbol not in symbols:
                symbols.append(symbol)

    holdings = etf_input_payload.get("etf_holdings") or {}
    if holdings and not isinstance(holdings, dict):
        raise ValueError("ETF input file: expected etf_holdings object")
    for symbol in holdings:
        normalized = _text(symbol).upper()
        if normalized and normalized not in symbols:
            symbols.append(normalized)
    return tuple(symbols)


def _candidate_symbols(candidate_payload: dict[str, Any], queue: str) -> tuple[str, ...]:
    satellite = candidate_payload.get("satellite_equities") or {}
    if not isinstance(satellite, dict):
        raise ValueError("satellite_equities: expected object")
    queues = ("primary_queue", "secondary_queue") if queue == "all" else (queue,)
    symbols: list[str] = []
    for queue_name in queues:
        for row in _as_list(satellite.get(queue_name)):
            if not isinstance(row, dict):
                raise ValueError(f"satellite_equities.{queue_name}: expected candidate objects")
            symbol = _text(row.get("symbol")).upper()
            if not symbol:
                raise ValueError(f"satellite_equities.{queue_name}: missing symbol")
            if symbol not in symbols:
                symbols.append(symbol)
    return tuple(symbols)


def _etf_row(etf_input_payload: dict[str, Any], etf_symbol: str) -> dict[str, Any]:
    holdings_root = etf_input_payload.get("etf_holdings") or {}
    if holdings_root and not isinstance(holdings_root, dict):
        raise ValueError("ETF input file: expected etf_holdings object")
    row = _lookup_case_insensitive(holdings_root, etf_symbol) or {}
    if not isinstance(row, dict):
        raise ValueError(f"etf_holdings.{etf_symbol}: expected object")
    return row


def _status(is_filled: bool) -> str:
    return "filled" if is_filled else "missing"


def _status_row(area: str, symbol: str, field: str, is_filled: bool, action: str) -> PrivateInputStatus:
    return PrivateInputStatus(
        area=area,
        symbol=symbol,
        field=field,
        status=_status(is_filled),
        safe_next_action="no action; value is present but masked" if is_filled else action,
    )


def evaluate_private_input_status(
    candidate_payload: dict[str, Any],
    *,
    etf_input_payload: dict[str, Any],
    decision_input_payload: dict[str, Any],
    queue: str,
) -> list[PrivateInputStatus]:
    rows: list[PrivateInputStatus] = []
    etfs = _expected_etfs(candidate_payload, etf_input_payload)
    symbols = _candidate_symbols(candidate_payload, queue)

    weights = etf_input_payload.get("portfolio_etf_weights") or etf_input_payload.get("portfolio_weights") or {}
    if weights and not isinstance(weights, dict):
        raise ValueError("ETF input file: expected portfolio_etf_weights object")

    for etf in etfs:
        rows.append(
            _status_row(
                "ETF portfolio weight",
                etf,
                f"portfolio_etf_weights.{etf}",
                _is_filled(_lookup_case_insensitive(weights, etf)),
                "fill private ETF portfolio percent, or 0 if deliberately not held",
            )
        )

        etf_row = _etf_row(etf_input_payload, etf)
        rows.append(
            _status_row(
                "ETF source meta",
                etf,
                f"etf_holdings.{etf}.source_meta",
                all(_is_filled(etf_row.get(key)) for key in ("as_of", "source_url", "coverage")),
                "record official holdings as_of, source_url, and coverage",
            )
        )

        holdings = etf_row.get("holdings") or {}
        if holdings and not isinstance(holdings, dict):
            raise ValueError(f"etf_holdings.{etf}.holdings: expected object")
        for symbol in symbols:
            rows.append(
                _status_row(
                    "ETF holding weight",
                    f"{etf}:{symbol}",
                    f"etf_holdings.{etf}.holdings.{symbol}",
                    _is_filled(_lookup_case_insensitive(holdings, symbol)),
                    "collect official ETF holding weight for this satellite candidate",
                )
            )

    inputs = decision_input_payload.get("inputs") or decision_input_payload.get("symbols") or {}
    if inputs and not isinstance(inputs, dict):
        raise ValueError("Decision input file: expected inputs object")
    for symbol in symbols:
        symbol_inputs = _lookup_case_insensitive(inputs, symbol) or {}
        if symbol_inputs and not isinstance(symbol_inputs, dict):
            raise ValueError(f"Decision input file: expected object for {symbol}")
        for field, action in DECISION_INPUT_FIELDS.items():
            rows.append(
                _status_row(
                    "Satellite decision input",
                    symbol,
                    f"inputs.{symbol}.{field}",
                    _is_filled(symbol_inputs.get(field)),
                    action,
                )
            )

    return rows


def _cell(value: str) -> str:
    return value.replace("|", "\\|")


def _render_summary(rows: list[PrivateInputStatus]) -> list[str]:
    by_area: Counter[str] = Counter(row.area for row in rows)
    filled_by_area: Counter[str] = Counter(row.area for row in rows if row.status == "filled")
    lines = [
        "| Area | Filled | Missing | Total |",
        "| --- | ---: | ---: | ---: |",
    ]
    for area in sorted(by_area):
        total = by_area[area]
        filled = filled_by_area[area]
        lines.append(f"| {_cell(area)} | {filled} | {total - filled} | {total} |")
    return lines


def render_report(
    rows: list[PrivateInputStatus],
    *,
    candidate_file: Path,
    etf_input_file: Path | None,
    decision_input_file: Path | None,
    run_date: str,
    queue: str,
    row_filter: str = "all",
) -> str:
    filled = sum(1 for row in rows if row.status == "filled")
    lines = [
        "# DI Private Input Status",
        "",
        f"- Run date: `{run_date}`",
        f"- Candidate manifest: `{candidate_file.as_posix()}`",
        f"- ETF overlap input file: `{etf_input_file.as_posix() if etf_input_file else 'not configured'}`",
        f"- Satellite decision input file: `{decision_input_file.as_posix() if decision_input_file else 'not configured'}`",
        f"- Queue scope: `{queue}`",
        f"- Row filter: `{row_filter}`",
        "- Interpretation: private input completeness only; values are masked.",
        "- Sensitive values printed: `false`",
        "- Order intent generated: `false`",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| Fields checked | {len(rows)} |",
        f"| Filled fields | {filled} |",
        f"| Missing fields | {len(rows) - filled} |",
        "",
        "## Summary By Area",
        "",
        *_render_summary(rows),
        "",
        "## Field Status",
        "",
        "| Area | Symbol | Field | Status | Safe next action |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    _cell(row.area),
                    f"`{row.symbol}`",
                    f"`{row.field}`",
                    f"`{row.status}`",
                    _cell(row.safe_next_action),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Privacy Boundary",
            "",
            "- This report must show only `filled` or `missing`, never private weights, account routes, account names, or position limits.",
            "- Keep `_report/private/di/` gitignored. Commit this status report only because the values are masked.",
            "- Use this report to decide which private fields to fill before running overlap and decision-prep gates.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Report DI private-input completeness without printing private values.")
    parser.add_argument("--candidate-file", type=Path, default=DEFAULT_CANDIDATE_FILE)
    parser.add_argument("--etf-input-file", type=Path, default=DEFAULT_ETF_INPUT_FILE)
    parser.add_argument("--decision-input-file", type=Path, default=DEFAULT_DECISION_INPUT_FILE)
    parser.add_argument("--queue", choices=("primary_queue", "secondary_queue", "all"), default="primary_queue")
    parser.add_argument("--run-date", default=_now_kst().date().isoformat())
    parser.add_argument("--only-missing", action="store_true", help="Show only missing private-input fields.")
    parser.add_argument(
        "--fail-on-missing",
        action="store_true",
        help="Return exit code 2 when any checked private-input field is missing.",
    )
    parser.add_argument("--output", type=Path, help="Markdown report output path. Prints to stdout when omitted.")
    args = parser.parse_args()

    try:
        candidate_payload = _load_yaml(args.candidate_file)
        etf_input_payload = _load_optional_yaml(args.etf_input_file)
        decision_input_payload = _load_optional_yaml(args.decision_input_file)
        rows = evaluate_private_input_status(
            candidate_payload,
            etf_input_payload=etf_input_payload,
            decision_input_payload=decision_input_payload,
            queue=args.queue,
        )
        visible_rows = [row for row in rows if row.status == "missing"] if args.only_missing else rows
        report = render_report(
            visible_rows,
            candidate_file=args.candidate_file,
            etf_input_file=args.etf_input_file,
            decision_input_file=args.decision_input_file,
            run_date=args.run_date,
            queue=args.queue,
            row_filter="missing_only" if args.only_missing else "all",
        )
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(report, encoding="utf-8")
    else:
        print(report)
    if args.fail_on_missing and any(row.status == "missing" for row in rows):
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
