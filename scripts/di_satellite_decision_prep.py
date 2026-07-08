"""Prepare DI satellite equity candidates before writing decision notes."""

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
DEFAULT_RESEARCH_ROOT = Path("_report/di/research")

REQUIRED_RESEARCH_FILES = ("financials.md", "thesis.md", "valuation.md")
OPTIONAL_STAGE_FILES = ("decision.md",)
MIN_MEANINGFUL_LINES = {
    "financials.md": 10,
    "thesis.md": 6,
    "valuation.md": 8,
    "decision.md": 4,
}
MANUAL_DECISION_INPUTS = {
    "latest_price_checked": "latest_price",
    "valuation_range_checked": "valuation_range",
    "reverse_dcf_checked": "reverse_dcf_or_scenario",
    "etf_overlap_checked": "etf_overlap",
    "tax_account_route": "tax_account_route",
    "max_position_size": "max_position_size",
    "add_trim_rule": "add_trim_rule",
    "source_freshness_checked": "source_freshness",
}
UNCHECKED_TOKENS = ("todo", "verify", "check", "needs_", "null", "pending")
FILE_UNCHECKED_TOKENS = ("todo", "verify", "needs_", "null", "pending")


@dataclass(frozen=True)
class SatelliteDecisionPrep:
    queue: str
    symbol: str
    name: str
    status: str
    research_state: str
    required_inputs: tuple[str, ...]
    safe_next_action: str


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
    if isinstance(value, list):
        return ", ".join(_text(item) for item in value)
    return str(value).strip()


def _is_filled(value: Any) -> bool:
    text = _text(value).lower()
    if not text:
        return False
    return not any(token in text for token in UNCHECKED_TOKENS)


def _meaningful_lines(path: Path) -> list[str]:
    if not path.exists():
        return []
    lines: list[str] = []
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        lowered = line.lower()
        if not line or line.startswith("#"):
            continue
        if line in {"-", "*"}:
            continue
        if any(token in lowered for token in FILE_UNCHECKED_TOKENS):
            continue
        lines.append(line)
    return lines


def _has_invalidation_rule(path: Path) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8").lower()
    return any(token in text for token in ("invalidation", "invalidated", "\ubb34\ud6a8\ud654"))


def _research_file_present(symbol: str, research_root: Path, filename: str) -> bool:
    path = research_root / symbol / filename
    return len(_meaningful_lines(path)) >= MIN_MEANINGFUL_LINES[filename]


def _research_state(symbol: str, research_root: Path) -> str:
    present: list[str] = []
    missing: list[str] = []
    for filename in (*REQUIRED_RESEARCH_FILES, *OPTIONAL_STAGE_FILES):
        if _research_file_present(symbol, research_root, filename):
            present.append(filename)
        else:
            missing.append(filename)
    present_text = "+".join(present) if present else "none"
    missing_text = "+".join(missing) if missing else "none"
    return f"present: {present_text}; pending: {missing_text}"


def _missing_inputs(row: dict[str, Any], symbol: str, research_root: Path) -> list[str]:
    missing: list[str] = []
    for filename in REQUIRED_RESEARCH_FILES:
        if not _research_file_present(symbol, research_root, filename):
            missing.append(filename)
    thesis_path = research_root / symbol / "thesis.md"
    if not _has_invalidation_rule(thesis_path):
        missing.append("invalidation_rule")
    for field, label in MANUAL_DECISION_INPUTS.items():
        if not _is_filled(row.get(field)):
            missing.append(label)
    return missing


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


def evaluate_satellite_decision_prep(
    payload: dict[str, Any],
    *,
    research_root: Path,
    queue: str,
) -> list[SatelliteDecisionPrep]:
    results: list[SatelliteDecisionPrep] = []
    for queue_name, row in _candidate_rows(payload, queue):
        symbol = _text(row.get("symbol")).upper()
        if not symbol:
            raise ValueError(f"satellite_equities.{queue_name}: missing symbol")
        required_inputs = tuple(_missing_inputs(row, symbol, research_root))
        status = "ready_for_checked_decision" if not required_inputs else "needs_decision_inputs"
        results.append(
            SatelliteDecisionPrep(
                queue=queue_name,
                symbol=symbol,
                name=_text(row.get("name")),
                status=status,
                research_state=_research_state(symbol, research_root),
                required_inputs=required_inputs,
                safe_next_action=(
                    "write checked decision.md with no order intent"
                    if status == "ready_for_checked_decision"
                    else "fill valuation, overlap, tax/account, sizing, and freshness inputs before decision.md"
                ),
            )
        )
    return results


def _render_list(values: tuple[str, ...]) -> str:
    return ", ".join(f"`{value}`" for value in values) if values else "-"


def _cell(value: str) -> str:
    return value.replace("|", "\\|")


def render_report(
    rows: list[SatelliteDecisionPrep],
    *,
    candidate_file: Path,
    research_root: Path,
    run_date: str,
    queue: str,
) -> str:
    ready = sum(1 for row in rows if row.status == "ready_for_checked_decision")
    lines = [
        "# DI Satellite Equity Decision Prep",
        "",
        f"- Run date: `{run_date}`",
        f"- Candidate manifest: `{candidate_file.as_posix()}`",
        f"- Research root: `{research_root.as_posix()}`",
        f"- Queue scope: `{queue}`",
        "- Interpretation: pre-decision checklist only; no buy, sell, hold, or order intent is generated",
        "- Order intent generated: `false`",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| Candidates checked | {len(rows)} |",
        f"| Ready for checked decision | {ready} |",
        f"| Needs prep | {len(rows) - ready} |",
        "",
        "## Candidate Prep State",
        "",
        "| Queue | Symbol | Name | Status | Research state | Required before decision.md | Safe next action |",
        "| --- | --- | --- | --- | --- | --- | --- |",
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
                    _cell(row.research_state),
                    _render_list(row.required_inputs),
                    _cell(row.safe_next_action),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Manual Inputs Required Before decision.md",
            "",
            "- `latest_price`: latest market price, currency, and timestamp.",
            "- `valuation_range`: base/bull/bear range or comparable multiple range tied to current price.",
            "- `reverse_dcf_or_scenario`: explicit assumptions needed to justify the current price.",
            "- `etf_overlap`: overlap with core ETF and satellite ETF holdings so single-name exposure is not double-counted.",
            "- `tax_account_route`: taxable account, ISA, pension, or IRP route and the expected tax/reporting treatment.",
            "- `max_position_size`: maximum single-name weight before adding the first lot.",
            "- `add_trim_rule`: written rule for adding, trimming, or stopping additional buys.",
            "- `source_freshness`: date of latest filing, facts, price, holdings, and tax/account checks.",
            "",
            "## Promotion Boundary",
            "",
            "- This report does not create or update `decision.md`.",
            "- A candidate remains blocked until required inputs are recorded and a checked decision note is written.",
            "- A ready status means process readiness to write a decision note, not a recommendation to buy.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare DI satellite equities before writing decision notes.")
    parser.add_argument("--candidate-file", type=Path, default=DEFAULT_CANDIDATE_FILE)
    parser.add_argument("--research-root", type=Path, default=DEFAULT_RESEARCH_ROOT)
    parser.add_argument("--queue", choices=("primary_queue", "secondary_queue", "all"), default="primary_queue")
    parser.add_argument("--run-date", default=_now_kst().date().isoformat())
    parser.add_argument("--output", type=Path, help="Markdown report output path. Prints to stdout when omitted.")
    args = parser.parse_args()

    try:
        payload = _load_yaml(args.candidate_file)
        rows = evaluate_satellite_decision_prep(payload, research_root=args.research_root, queue=args.queue)
        report = render_report(
            rows,
            candidate_file=args.candidate_file,
            research_root=args.research_root,
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
