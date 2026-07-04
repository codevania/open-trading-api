"""Generate paper/smoke Signal Candidate rows from Point-in-Time liquidity rows.

This is a signal-only research scaffold. It does not call broker APIs and does
not create order intents.
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict, deque
from dataclasses import dataclass
from pathlib import Path
from typing import Any


DEFAULT_LOOKBACK = 5
DEFAULT_THRESHOLD_PCT = 0.0
DEFAULT_TOP_N_PER_STATE = 20
STRATEGY_ID = "001-strategy-universe-momentum"


@dataclass(frozen=True)
class SignalCandidate:
    source: dict[str, str]
    signal_state: str
    roc_pct: float
    lookback: int
    rank_in_date_state: int = 0


def _read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise ValueError(f"Point-in-Time liquidity CSV not found: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ValueError(f"Point-in-Time liquidity CSV has no rows: {path}")
    required = {"date", "code", "stock_name", "close", "pit_liquidity_final_status"}
    missing = required - set(rows[0])
    if missing:
        raise ValueError(f"Point-in-Time liquidity CSV missing required columns: {', '.join(sorted(missing))}")
    return rows


def _parse_float(value: str) -> float | None:
    text = str(value or "").replace(",", "").strip()
    if not text:
        return None
    try:
        parsed = float(text)
    except ValueError:
        return None
    if parsed <= 0:
        return None
    return parsed


def _state_for_roc(roc_pct: float, threshold_pct: float) -> str:
    if roc_pct > threshold_pct:
        return "BUY candidate"
    if roc_pct < 0:
        return "SELL candidate"
    return "HOLD"


def generate_signal_candidates(
    rows: list[dict[str, str]],
    lookback: int = DEFAULT_LOOKBACK,
    threshold_pct: float = DEFAULT_THRESHOLD_PCT,
    top_n_per_state: int = DEFAULT_TOP_N_PER_STATE,
) -> list[SignalCandidate]:
    if lookback <= 0:
        raise ValueError("lookback must be positive")
    if top_n_per_state <= 0:
        raise ValueError("top_n_per_state must be positive")

    histories: dict[str, deque[float]] = defaultdict(lambda: deque(maxlen=lookback))
    all_candidates: list[SignalCandidate] = []
    for row in sorted(rows, key=lambda item: (item.get("code", ""), item.get("date", ""))):
        code = row.get("code", "").strip().upper()
        close = _parse_float(row.get("close", ""))
        history = histories[code]
        if close is None:
            continue

        if len(history) >= lookback and row.get("pit_liquidity_final_status") == "include":
            base_close = history[0]
            roc_pct = ((close / base_close) - 1.0) * 100.0
            state = _state_for_roc(roc_pct, threshold_pct)
            if state != "HOLD":
                all_candidates.append(SignalCandidate(row, state, roc_pct, lookback))
        history.append(close)

    grouped: dict[tuple[str, str], list[SignalCandidate]] = defaultdict(list)
    for candidate in all_candidates:
        grouped[(candidate.source.get("date", ""), candidate.signal_state)].append(candidate)

    ranked: list[SignalCandidate] = []
    for (_date, state), group in grouped.items():
        reverse = state == "BUY candidate"
        ordered = sorted(group, key=lambda candidate: candidate.roc_pct, reverse=reverse)[:top_n_per_state]
        for rank, candidate in enumerate(ordered, start=1):
            ranked.append(
                SignalCandidate(
                    source=candidate.source,
                    signal_state=candidate.signal_state,
                    roc_pct=candidate.roc_pct,
                    lookback=candidate.lookback,
                    rank_in_date_state=rank,
                )
            )
    ranked.sort(key=lambda candidate: (candidate.source.get("date", ""), candidate.signal_state, candidate.rank_in_date_state))
    return ranked


def _format_pct(value: float) -> str:
    return f"{value:.4f}"


def write_csv(candidates: list[SignalCandidate], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = (
        "date",
        "code",
        "stock_name",
        "market",
        "close",
        "signal_state",
        "roc_pct",
        "lookback",
        "rank_in_date_state",
        "source_strategy",
        "signal_mode",
        "pit_liquidity_final_status",
    )
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for candidate in candidates:
            row = candidate.source
            writer.writerow(
                {
                    "date": row.get("date", ""),
                    "code": row.get("code", ""),
                    "stock_name": row.get("stock_name", ""),
                    "market": row.get("market", ""),
                    "close": row.get("close", ""),
                    "signal_state": candidate.signal_state,
                    "roc_pct": _format_pct(candidate.roc_pct),
                    "lookback": str(candidate.lookback),
                    "rank_in_date_state": str(candidate.rank_in_date_state),
                    "source_strategy": STRATEGY_ID,
                    "signal_mode": "paper_signal_candidate_only",
                    "pit_liquidity_final_status": row.get("pit_liquidity_final_status", ""),
                }
            )


def _wikilink(path: Path) -> str:
    rendered = path.as_posix()
    return f"[[{rendered}|{rendered}]]"


def render_report(
    candidates: list[SignalCandidate],
    input_path: Path,
    as_of_range: str,
    lookback: int,
    threshold_pct: float,
    top_n_per_state: int,
    csv_output: Path | None,
) -> str:
    dates = sorted({candidate.source.get("date", "") for candidate in candidates if candidate.source.get("date", "")})
    state_counts = Counter(candidate.signal_state for candidate in candidates)
    latest_date = dates[-1] if dates else ""
    latest = [candidate for candidate in candidates if candidate.source.get("date", "") == latest_date]

    lines = [
        "# Point-in-Time Momentum Signal Candidates Smoke",
        "",
        f"- Input: {_wikilink(input_path)}",
        f"- Date range: `{as_of_range}`",
        f"- Strategy: `{STRATEGY_ID}`",
        "- Mode: `paper_signal_candidate_only`",
        "- KIS API call: `false`",
        "- Order intent generated: `false`",
        "- Backtest readiness: `hold`",
        "- Live trading readiness: `blocked`",
        f"- Rule: `{lookback}d ROC > {threshold_pct:.2f}%` for BUY candidates; `{lookback}d ROC < 0` for SELL candidates",
        f"- Top N per date/state: `{top_n_per_state}`",
    ]
    if csv_output:
        lines.append(f"- Machine-readable rows: {_wikilink(csv_output)}")

    lines.extend(["", "## Summary", "", f"- Candidate rows: `{len(candidates)}`", f"- Candidate dates: `{len(dates)}`"])
    if latest_date:
        lines.append(f"- Latest candidate date: `{latest_date}`")

    lines.extend(["", "## State Counts", "", "| State | Count |", "| --- | ---: |"])
    for state, count in sorted(state_counts.items()):
        lines.append(f"| `{state}` | {count} |")
    if not state_counts:
        lines.append("| `none` | 0 |")

    lines.extend(
        [
            "",
            "## Latest Date Sample",
            "",
            "| State | Rank | Code | Company | ROC % | Close |",
            "| --- | ---: | --- | --- | ---: | ---: |",
        ]
    )
    for candidate in latest[:40]:
        row = candidate.source
        lines.append(
            f"| {candidate.signal_state} | {candidate.rank_in_date_state} | `{row.get('code', '')}` | "
            f"{row.get('stock_name', '')} | {_format_pct(candidate.roc_pct)} | {row.get('close', '')} |"
        )

    lines.extend(
        [
            "",
            "## Guardrails",
            "",
            "- These rows are `Signal Candidate` tracking rows only, not trade instructions.",
            "- The source `Point-in-Time` and Liquidity Filter inputs are still smoke artifacts.",
            "- Do not generate orders from this file.",
            "- Keep `Backtest readiness` at `hold` until full historical status, production Liquidity Filter, cost model, OOS, and Bias Control pass.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate paper/smoke Momentum Signal Candidate rows.")
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--as-of-range", required=True)
    parser.add_argument("--lookback", default=DEFAULT_LOOKBACK, type=int)
    parser.add_argument("--threshold-pct", default=DEFAULT_THRESHOLD_PCT, type=float)
    parser.add_argument("--top-n-per-state", default=DEFAULT_TOP_N_PER_STATE, type=int)
    parser.add_argument("--csv-output", type=Path)
    parser.add_argument("--report-output", type=Path)
    args = parser.parse_args()

    try:
        rows = _read_rows(args.input)
        candidates = generate_signal_candidates(rows, args.lookback, args.threshold_pct, args.top_n_per_state)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc

    if args.csv_output:
        write_csv(candidates, args.csv_output)
    report = render_report(
        candidates,
        args.input,
        args.as_of_range,
        args.lookback,
        args.threshold_pct,
        args.top_n_per_state,
        args.csv_output,
    )
    if args.report_output:
        args.report_output.parent.mkdir(parents=True, exist_ok=True)
        args.report_output.write_text(report, encoding="utf-8")
    else:
        print(report, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
