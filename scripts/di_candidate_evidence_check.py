"""Check DI candidate evidence before watchlist promotion."""

from __future__ import annotations

import argparse
import re
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

UNCHECKED_TOKENS = ("todo", "verify", "check", "must be checked", "needs_", "null")
FILE_UNCHECKED_TOKENS = ("todo", "verify", "must be checked", "needs_", "null", "pending")
MIN_RESEARCH_LINES = {
    "sec-filing-summary.md": 6,
    "sec-filing-documents.md": 6,
    "sec-filing-sections.md": 6,
    "financials.md": 10,
    "thesis.md": 6,
    "valuation.md": 8,
    "decision.md": 4,
}
PLACEHOLDER_LINE_PATTERNS = (
    re.compile(r"^-+$"),
    re.compile(r"^\d+\.$"),
    re.compile(r"^[-*]\s*$"),
    re.compile(r"^[-*]\s+\[\s\]\s+\S+"),
    re.compile(r"^[-*]\s+[^:]+:\s*$"),
    re.compile(r"^\|\s*[-:|\s]+\|$"),
    re.compile(r"^\|\s*(?:[^|]*\|\s*)+$"),
)


@dataclass(frozen=True)
class CandidateGate:
    section: str
    symbol: str
    name: str
    status: str
    missing: tuple[str, ...]
    next_action: str


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


def _missing_fields(row: dict[str, Any], fields: tuple[str, ...]) -> list[str]:
    return [field for field in fields if not _is_filled(row.get(field))]


def _is_checked_decision_line(line: str) -> bool:
    return bool(re.match(r"^[-*]\s+\[[xX]\]\s+\S+", line))


def _meaningful_lines(text: str) -> list[str]:
    lines: list[str] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        lowered = line.lower()
        if not line or line.startswith("#"):
            continue
        if any(pattern.match(line) for pattern in PLACEHOLDER_LINE_PATTERNS):
            if not _is_checked_decision_line(line):
                continue
        if any(token in lowered for token in FILE_UNCHECKED_TOKENS):
            continue
        lines.append(line)
    return lines


def _research_file_status(symbol: str, research_root: Path, filename: str) -> str | None:
    path = research_root / symbol.upper() / filename
    if not path.exists():
        return f"research {filename}"
    lines = _meaningful_lines(path.read_text(encoding="utf-8"))
    if len(lines) < MIN_RESEARCH_LINES[filename]:
        return f"research {filename} content"
    if filename == "decision.md" and not any(_is_checked_decision_line(line) for line in lines):
        return "research decision.md checked decision"
    return None


def _etf_gate(section: str, row: dict[str, Any]) -> CandidateGate:
    required = (
        "source_url",
        "benchmark",
        "currency_hedge",
        "distribution_policy",
        "tax_account_fit",
        "expense_ratio",
    )
    missing = _missing_fields(row, required)
    status = "ready_for_decision_note" if not missing else "hold"
    return CandidateGate(
        section=section,
        symbol=_text(row.get("symbol")),
        name=_text(row.get("name")),
        status=status,
        missing=tuple(missing),
        next_action="write ETF decision note" if status != "hold" else "fill issuer, fee, NAV, distribution, tax, and account evidence",
    )


def _stock_gate(section: str, row: dict[str, Any], research_root: Path) -> CandidateGate:
    missing = _missing_fields(row, ("filings_to_read",))
    symbol = _text(row.get("symbol")).upper()
    market = _text(row.get("market")).upper()
    if market in {"NASDAQ", "NYSE"}:
        for filename in ("sec-filing-summary.md", "sec-filing-documents.md", "sec-filing-sections.md"):
            file_status = _research_file_status(symbol, research_root, filename)
            if file_status:
                missing.append(file_status)
    for filename in ("financials.md", "thesis.md", "valuation.md", "decision.md"):
        file_status = _research_file_status(symbol, research_root, filename)
        if file_status:
            missing.append(file_status)
    status = "ready_for_watchlist_review" if not missing else "hold"
    return CandidateGate(
        section=section,
        symbol=symbol,
        name=_text(row.get("name")),
        status=status,
        missing=tuple(missing),
        next_action="review position size and watchlist promotion" if status != "hold" else "collect filings and write thesis/valuation/decision notes",
    )


def evaluate_candidates(payload: dict[str, Any], *, research_root: Path) -> list[CandidateGate]:
    gates: list[CandidateGate] = []
    for section in ("core_etfs", "korea_listed_etfs_to_verify", "satellite_etfs_to_verify"):
        for row in _as_list(payload.get(section)):
            if not isinstance(row, dict):
                raise ValueError(f"{section}: expected candidate objects")
            gates.append(_etf_gate(section, row))

    satellite = payload.get("satellite_equities") or {}
    if not isinstance(satellite, dict):
        raise ValueError("satellite_equities: expected object")
    for section in ("primary_queue", "secondary_queue"):
        for row in _as_list(satellite.get(section)):
            if not isinstance(row, dict):
                raise ValueError(f"satellite_equities.{section}: expected candidate objects")
            gates.append(_stock_gate(f"satellite_equities.{section}", row, research_root))
    return gates


def _render_missing(missing: tuple[str, ...]) -> str:
    return ", ".join(f"`{item}`" for item in missing) if missing else "-"


def _repo_doc_ref(path: Path, *, label: str | None = None) -> str:
    if not path.is_absolute():
        normalized = path.as_posix()
        return f"[[{normalized}|{label or path.name}]]"
    try:
        relative_path = path.resolve().relative_to(Path.cwd().resolve())
    except ValueError:
        return f"`{path.as_posix()}`"
    return f"[[{relative_path.as_posix()}|{label or path.name}]]"


def render_report(
    gates: list[CandidateGate],
    *,
    candidate_file: Path,
    research_root: Path,
    run_date: str,
    row_filter: str = "all",
) -> str:
    ready = sum(1 for gate in gates if gate.status != "hold")
    lines = [
        "# DI Candidate Evidence Gate",
        "",
        f"- Run date: `{run_date}`",
        f"- Candidate manifest: {_repo_doc_ref(candidate_file)}",
        f"- Research root: `{research_root.as_posix()}`",
        f"- Row filter: `{row_filter}`",
        "- Interpretation: readiness gate only; no buy or order intent is generated",
        "- Order intent generated: `false`",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| Candidates checked | {len(gates)} |",
        f"| Ready for next review | {ready} |",
        f"| Hold | {len(gates) - ready} |",
        "",
        "## Gate Results",
        "",
        "| Section | Symbol | Name | Status | Missing evidence | Next action |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for gate in gates:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{gate.section}`",
                    f"`{gate.symbol}`",
                    gate.name,
                    f"`{gate.status}`",
                    _render_missing(gate.missing),
                    gate.next_action,
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Promotion Rules",
            "",
            "- ETF candidates stay out of [[_report/di/watchlist.yaml|_report/di/watchlist.yaml]] until issuer, cost, NAV/liquidity, distribution, tax, and account evidence are filled.",
            "- Stock candidates stay out of active position review until SEC/DART source evidence, primary filing document and section maps, `financials.md`, `thesis.md`, `valuation.md`, and `decision.md` exist.",
            "- A `ready_*` status means research process readiness only, not a recommendation to buy.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Check DI candidate evidence before watchlist promotion.")
    parser.add_argument("--candidate-file", type=Path, default=DEFAULT_CANDIDATE_FILE)
    parser.add_argument("--research-root", type=Path, default=DEFAULT_RESEARCH_ROOT)
    parser.add_argument("--run-date", default=_now_kst().date().isoformat())
    parser.add_argument("--only-hold", action="store_true", help="Show only candidates that remain on hold.")
    parser.add_argument(
        "--fail-on-hold",
        action="store_true",
        help="Return exit code 2 when any checked candidate remains on hold.",
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    try:
        payload = _load_yaml(args.candidate_file)
        gates = evaluate_candidates(payload, research_root=args.research_root)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc

    visible_gates = [gate for gate in gates if gate.status == "hold"] if args.only_hold else gates
    report = render_report(
        visible_gates,
        candidate_file=args.candidate_file,
        research_root=args.research_root,
        run_date=args.run_date,
        row_filter="hold_only" if args.only_hold else "all",
    )
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(report, encoding="utf-8")
    else:
        print(report)
    if args.fail_on_hold and any(gate.status == "hold" for gate in gates):
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
