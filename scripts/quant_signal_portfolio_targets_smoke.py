"""Generate paper-only portfolio target rows from Signal Candidate rows.

This is a Backtest preflight artifact. It converts local Signal Candidate rows
into deterministic target-weight rows so portfolio construction assumptions can
be inspected before a Backtest engine exists. It does not call broker APIs and
does not create order intents.
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from statistics import mean


DEFAULT_MAX_POSITIONS = 20
DEFAULT_MAX_POSITION_WEIGHT = 0.10
DEFAULT_TARGET_GROSS_EXPOSURE = 1.0
PORTFOLIO_MODE = "long_only"
TARGET_MODE = "paper_portfolio_target_smoke_only"


@dataclass(frozen=True)
class PortfolioTarget:
    source: dict[str, str]
    target_side: str
    target_weight: float
    rank_in_portfolio: int
    target_mode: str = TARGET_MODE


@dataclass(frozen=True)
class DateDiagnostic:
    date: str
    selected_positions: int
    gross_target_weight: float
    cash_reserve_weight: float
    turnover_weight_change: float


def _read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise ValueError(f"Signal Candidate CSV not found: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = [{key: (value or "").strip() for key, value in row.items()} for row in csv.DictReader(handle)]
    if not rows:
        raise ValueError(f"Signal Candidate CSV has no rows: {path}")
    required = {"date", "code", "stock_name", "signal_state", "rank_in_date_state"}
    missing = required - set(rows[0])
    if missing:
        raise ValueError(f"Signal Candidate CSV missing required columns: {', '.join(sorted(missing))}")
    return rows


def _parse_rank(row: dict[str, str]) -> int:
    try:
        rank = int(float(row.get("rank_in_date_state", "")))
    except ValueError:
        return 999_999
    return rank if rank > 0 else 999_999


def _parse_float(value: str) -> float:
    try:
        return float(str(value or "").replace(",", "").strip())
    except ValueError:
        return 0.0


def _date_groups(rows: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        date = row.get("date", "").strip()
        if date:
            grouped[date].append(row)
    return dict(sorted(grouped.items()))


def generate_portfolio_targets(
    rows: list[dict[str, str]],
    *,
    max_positions: int = DEFAULT_MAX_POSITIONS,
    max_position_weight: float = DEFAULT_MAX_POSITION_WEIGHT,
    target_gross_exposure: float = DEFAULT_TARGET_GROSS_EXPOSURE,
) -> tuple[list[PortfolioTarget], list[DateDiagnostic]]:
    if max_positions <= 0:
        raise ValueError("max_positions must be positive")
    if max_position_weight <= 0 or max_position_weight > 1:
        raise ValueError("max_position_weight must be in (0, 1]")
    if target_gross_exposure <= 0 or target_gross_exposure > 1:
        raise ValueError("target_gross_exposure must be in (0, 1]")

    targets: list[PortfolioTarget] = []
    diagnostics: list[DateDiagnostic] = []
    previous_weights: dict[str, float] = {}

    for date, group in _date_groups(rows).items():
        buy_rows = [row for row in group if row.get("signal_state", "") == "BUY candidate"]
        buy_rows.sort(key=lambda row: (_parse_rank(row), -_parse_float(row.get("roc_pct", "")), row.get("code", "")))
        selected = buy_rows[:max_positions]
        if selected:
            base_weight = min(target_gross_exposure / len(selected), max_position_weight)
        else:
            base_weight = 0.0

        current_weights: dict[str, float] = {}
        for rank, row in enumerate(selected, start=1):
            code = row.get("code", "").strip().upper()
            if not code:
                continue
            current_weights[code] = base_weight
            targets.append(
                PortfolioTarget(
                    source=row,
                    target_side="LONG",
                    target_weight=base_weight,
                    rank_in_portfolio=rank,
                )
            )

        gross_weight = sum(current_weights.values())
        cash_reserve = max(0.0, 1.0 - gross_weight)
        all_codes = set(previous_weights) | set(current_weights)
        turnover = sum(abs(current_weights.get(code, 0.0) - previous_weights.get(code, 0.0)) for code in all_codes)
        diagnostics.append(
            DateDiagnostic(
                date=date,
                selected_positions=len(current_weights),
                gross_target_weight=gross_weight,
                cash_reserve_weight=cash_reserve,
                turnover_weight_change=turnover,
            )
        )
        previous_weights = current_weights

    return targets, diagnostics


def _format_weight(value: float) -> str:
    return f"{value:.6f}"


def write_csv(targets: list[PortfolioTarget], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = (
        "date",
        "code",
        "stock_name",
        "market",
        "target_side",
        "target_weight",
        "rank_in_portfolio",
        "source_signal_state",
        "source_rank_in_date_state",
        "source_roc_pct",
        "source_strategy",
        "source_signal_mode",
        "portfolio_mode",
        "target_mode",
        "order_intent_generated",
    )
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for target in targets:
            row = target.source
            writer.writerow(
                {
                    "date": row.get("date", ""),
                    "code": row.get("code", ""),
                    "stock_name": row.get("stock_name", ""),
                    "market": row.get("market", ""),
                    "target_side": target.target_side,
                    "target_weight": _format_weight(target.target_weight),
                    "rank_in_portfolio": str(target.rank_in_portfolio),
                    "source_signal_state": row.get("signal_state", ""),
                    "source_rank_in_date_state": row.get("rank_in_date_state", ""),
                    "source_roc_pct": row.get("roc_pct", ""),
                    "source_strategy": row.get("source_strategy", ""),
                    "source_signal_mode": row.get("signal_mode", ""),
                    "portfolio_mode": PORTFOLIO_MODE,
                    "target_mode": target.target_mode,
                    "order_intent_generated": "false",
                }
            )


def summarize(targets: list[PortfolioTarget], diagnostics: list[DateDiagnostic]) -> dict[str, object]:
    side_counts = Counter(target.target_side for target in targets)
    market_counts = Counter(target.source.get("market", "") for target in targets)
    return {
        "target_rows": len(targets),
        "target_dates": len({target.source.get("date", "") for target in targets if target.source.get("date", "")}),
        "side_counts": dict(sorted(side_counts.items())),
        "market_counts": dict(sorted(market_counts.items())),
        "avg_positions_per_date": mean([item.selected_positions for item in diagnostics]) if diagnostics else 0.0,
        "avg_gross_target_weight": mean([item.gross_target_weight for item in diagnostics]) if diagnostics else 0.0,
        "avg_cash_reserve_weight": mean([item.cash_reserve_weight for item in diagnostics]) if diagnostics else 0.0,
        "max_turnover_weight_change": max([item.turnover_weight_change for item in diagnostics], default=0.0),
    }


def _wikilink(path: Path) -> str:
    rendered = path.as_posix()
    return f"[[{rendered}|{rendered}]]"


def render_report(
    *,
    targets: list[PortfolioTarget],
    diagnostics: list[DateDiagnostic],
    summary: dict[str, object],
    input_path: Path,
    csv_output: Path | None,
    max_positions: int,
    max_position_weight: float,
    target_gross_exposure: float,
) -> str:
    lines = [
        "# Signal Portfolio Targets Smoke",
        "",
        f"- Signal input: {_wikilink(input_path)}",
        f"- Portfolio mode: `{PORTFOLIO_MODE}`",
        f"- Target mode: `{TARGET_MODE}`",
        f"- Max positions: `{max_positions}`",
        f"- Max position weight: `{max_position_weight:.2%}`",
        f"- Target gross exposure: `{target_gross_exposure:.2%}`",
        "- KIS API call: `false`",
        "- KRX API call: `false`",
        "- Order intent generated: `false`",
        "- Backtest readiness: `hold`",
        "- Live trading readiness: `blocked`",
    ]
    if csv_output:
        lines.append(f"- Machine-readable rows: {_wikilink(csv_output)}")

    lines.extend(
        [
            "",
            "## Summary",
            "",
            "| Metric | Value |",
            "| --- | ---: |",
            f"| Target rows | {summary['target_rows']} |",
            f"| Target dates | {summary['target_dates']} |",
            f"| Avg positions per date | {float(summary['avg_positions_per_date']):.2f} |",
            f"| Avg gross target weight | {float(summary['avg_gross_target_weight']):.4f} |",
            f"| Avg cash reserve weight | {float(summary['avg_cash_reserve_weight']):.4f} |",
            f"| Max turnover weight change | {float(summary['max_turnover_weight_change']):.4f} |",
            "",
            "## Side Counts",
            "",
            "| Side | Count |",
            "| --- | ---: |",
        ]
    )
    for side, count in dict(summary["side_counts"]).items():
        lines.append(f"| `{side}` | {count} |")
    if not summary["side_counts"]:
        lines.append("| `none` | 0 |")

    lines.extend(
        [
            "",
            "## Date Diagnostics",
            "",
            "| Date | Selected positions | Gross target weight | Cash reserve weight | Turnover weight change |",
            "| --- | ---: | ---: | ---: | ---: |",
        ]
    )
    for item in diagnostics:
        lines.append(
            f"| {item.date} | {item.selected_positions} | {_format_weight(item.gross_target_weight)} | "
            f"{_format_weight(item.cash_reserve_weight)} | {_format_weight(item.turnover_weight_change)} |"
        )

    latest_date = diagnostics[-1].date if diagnostics else ""
    latest_targets = [target for target in targets if target.source.get("date", "") == latest_date]
    lines.extend(
        [
            "",
            "## Latest Target Sample",
            "",
            "| Date | Rank | Side | Code | Company | Weight | Source ROC % |",
            "| --- | ---: | --- | --- | --- | ---: | ---: |",
        ]
    )
    for target in latest_targets[:30]:
        row = target.source
        lines.append(
            f"| {row.get('date', '')} | {target.rank_in_portfolio} | {target.target_side} | "
            f"`{row.get('code', '')}` | {row.get('stock_name', '')} | {_format_weight(target.target_weight)} | "
            f"{row.get('roc_pct', '')} |"
        )

    lines.extend(
        [
            "",
            "## Guardrails",
            "",
            "- These rows are target-weight diagnostics only, not order instructions.",
            "- `SELL candidate` rows are excluded in `long_only` mode; they are not short targets.",
            "- This does not include transaction costs, slippage, taxes, cash drag modeling, or benchmark comparison.",
            "- Keep `Backtest readiness` at `hold` until full Point-in-Time status coverage, costs, benchmark, OOS, and Bias Control pass.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate paper-only portfolio target rows from Signal Candidate rows.")
    parser.add_argument("--signals-input", required=True, type=Path)
    parser.add_argument("--max-positions", default=DEFAULT_MAX_POSITIONS, type=int)
    parser.add_argument("--max-position-weight", default=DEFAULT_MAX_POSITION_WEIGHT, type=float)
    parser.add_argument("--target-gross-exposure", default=DEFAULT_TARGET_GROSS_EXPOSURE, type=float)
    parser.add_argument("--csv-output", type=Path)
    parser.add_argument("--report-output", type=Path)
    args = parser.parse_args()

    try:
        signal_rows = _read_rows(args.signals_input)
        targets, diagnostics = generate_portfolio_targets(
            signal_rows,
            max_positions=args.max_positions,
            max_position_weight=args.max_position_weight,
            target_gross_exposure=args.target_gross_exposure,
        )
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc

    if args.csv_output:
        write_csv(targets, args.csv_output)
    report = render_report(
        targets=targets,
        diagnostics=diagnostics,
        summary=summarize(targets, diagnostics),
        input_path=args.signals_input,
        csv_output=args.csv_output,
        max_positions=args.max_positions,
        max_position_weight=args.max_position_weight,
        target_gross_exposure=args.target_gross_exposure,
    )
    if args.report_output:
        args.report_output.parent.mkdir(parents=True, exist_ok=True)
        with args.report_output.open("w", encoding="utf-8", newline="\n") as handle:
            handle.write(report)
    else:
        print(report, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
