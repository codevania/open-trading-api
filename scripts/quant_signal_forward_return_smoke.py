"""Compute paper-only forward-return diagnostics for Signal Candidate rows.

This is not a Backtest. It only checks whether local Signal Candidate rows can
be joined to later local close prices without broker/API calls or order intents.
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from statistics import mean


DEFAULT_HORIZONS = (1, 5)


@dataclass(frozen=True)
class ForwardReturnRow:
    signal: dict[str, str]
    horizon: int
    evaluation_status: str
    forward_date: str = ""
    signal_close: float | None = None
    forward_close: float | None = None
    raw_forward_return_pct: float | None = None
    directional_forward_score_pct: float | None = None


def _read_csv(path: Path, required: set[str], label: str) -> list[dict[str, str]]:
    if not path.exists():
        raise ValueError(f"{label} CSV not found: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = [{key: (value or "").strip() for key, value in row.items()} for row in csv.DictReader(handle)]
    if not rows:
        raise ValueError(f"{label} CSV has no rows: {path}")
    missing = required - set(rows[0])
    if missing:
        raise ValueError(f"{label} CSV missing required columns: {', '.join(sorted(missing))}")
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


def _parse_horizons(value: str) -> tuple[int, ...]:
    horizons: list[int] = []
    for token in value.split(","):
        text = token.strip()
        if not text:
            continue
        try:
            horizon = int(text)
        except ValueError as exc:
            raise ValueError(f"invalid horizon: {text}") from exc
        if horizon <= 0:
            raise ValueError("horizons must be positive")
        horizons.append(horizon)
    if not horizons:
        raise ValueError("at least one horizon is required")
    return tuple(dict.fromkeys(horizons))


def _price_index(price_rows: list[dict[str, str]]) -> dict[str, list[tuple[str, float]]]:
    by_code: dict[str, dict[str, float]] = defaultdict(dict)
    for row in price_rows:
        code = row.get("code", "").strip().upper()
        date = row.get("date", "").strip()
        close = _parse_float(row.get("close", ""))
        if not code or not date or close is None:
            continue
        by_code[code][date] = close
    return {code: sorted(values.items()) for code, values in by_code.items()}


def _directional_score(signal_state: str, raw_return_pct: float) -> float:
    if signal_state == "SELL candidate":
        return -raw_return_pct
    return raw_return_pct


def evaluate_forward_returns(
    signal_rows: list[dict[str, str]],
    price_rows: list[dict[str, str]],
    horizons: tuple[int, ...] = DEFAULT_HORIZONS,
) -> list[ForwardReturnRow]:
    if not horizons:
        raise ValueError("at least one horizon is required")
    if any(horizon <= 0 for horizon in horizons):
        raise ValueError("horizons must be positive")

    prices_by_code = _price_index(price_rows)
    results: list[ForwardReturnRow] = []

    for signal in signal_rows:
        code = signal.get("code", "").strip().upper()
        signal_date = signal.get("date", "").strip()
        signal_state = signal.get("signal_state", "").strip()
        prices = prices_by_code.get(code, [])
        date_to_index = {date: index for index, (date, _close) in enumerate(prices)}
        signal_index = date_to_index.get(signal_date)
        signal_close = _parse_float(signal.get("close", ""))
        if signal_index is not None:
            signal_close = prices[signal_index][1]

        for horizon in horizons:
            if signal_index is None or signal_close is None:
                results.append(ForwardReturnRow(signal, horizon, "missing_signal_price", signal_close=signal_close))
                continue
            forward_index = signal_index + horizon
            if forward_index >= len(prices):
                results.append(
                    ForwardReturnRow(
                        signal,
                        horizon,
                        "missing_forward_price",
                        signal_close=signal_close,
                    )
                )
                continue
            forward_date, forward_close = prices[forward_index]
            raw_return = ((forward_close / signal_close) - 1.0) * 100.0
            results.append(
                ForwardReturnRow(
                    signal=signal,
                    horizon=horizon,
                    evaluation_status="complete",
                    forward_date=forward_date,
                    signal_close=signal_close,
                    forward_close=forward_close,
                    raw_forward_return_pct=raw_return,
                    directional_forward_score_pct=_directional_score(signal_state, raw_return),
                )
            )
    return results


def _format_float(value: float | None) -> str:
    if value is None:
        return ""
    return f"{value:.4f}"


def write_csv(rows: list[ForwardReturnRow], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = (
        "date",
        "code",
        "stock_name",
        "market",
        "signal_state",
        "horizon_trading_days",
        "evaluation_status",
        "forward_date",
        "signal_close",
        "forward_close",
        "raw_forward_return_pct",
        "directional_forward_score_pct",
        "source_strategy",
        "signal_mode",
        "evaluation_mode",
    )
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for result in rows:
            signal = result.signal
            writer.writerow(
                {
                    "date": signal.get("date", ""),
                    "code": signal.get("code", ""),
                    "stock_name": signal.get("stock_name", ""),
                    "market": signal.get("market", ""),
                    "signal_state": signal.get("signal_state", ""),
                    "horizon_trading_days": str(result.horizon),
                    "evaluation_status": result.evaluation_status,
                    "forward_date": result.forward_date,
                    "signal_close": _format_float(result.signal_close),
                    "forward_close": _format_float(result.forward_close),
                    "raw_forward_return_pct": _format_float(result.raw_forward_return_pct),
                    "directional_forward_score_pct": _format_float(result.directional_forward_score_pct),
                    "source_strategy": signal.get("source_strategy", ""),
                    "signal_mode": signal.get("signal_mode", ""),
                    "evaluation_mode": "paper_forward_return_smoke_only",
                }
            )


def summarize(rows: list[ForwardReturnRow]) -> dict[str, object]:
    status_counts = Counter(row.evaluation_status for row in rows)
    horizon_counts = Counter(str(row.horizon) for row in rows)
    state_counts = Counter(row.signal.get("signal_state", "") for row in rows)
    complete_by_horizon: dict[str, list[float]] = defaultdict(list)
    raw_by_horizon: dict[str, list[float]] = defaultdict(list)
    for row in rows:
        if row.evaluation_status != "complete" or row.directional_forward_score_pct is None or row.raw_forward_return_pct is None:
            continue
        key = str(row.horizon)
        complete_by_horizon[key].append(row.directional_forward_score_pct)
        raw_by_horizon[key].append(row.raw_forward_return_pct)
    return {
        "rows": len(rows),
        "status_counts": dict(sorted(status_counts.items())),
        "horizon_counts": dict(sorted(horizon_counts.items())),
        "state_counts": dict(sorted(state_counts.items())),
        "complete_rows": status_counts.get("complete", 0),
        "avg_directional_score_by_horizon": {key: mean(values) for key, values in sorted(complete_by_horizon.items()) if values},
        "avg_raw_return_by_horizon": {key: mean(values) for key, values in sorted(raw_by_horizon.items()) if values},
    }


def _wikilink(path: Path) -> str:
    rendered = path.as_posix()
    return f"[[{rendered}|{rendered}]]"


def render_report(
    *,
    rows: list[ForwardReturnRow],
    summary: dict[str, object],
    signals_input: Path,
    price_input: Path,
    horizons: tuple[int, ...],
    csv_output: Path | None,
) -> str:
    lines = [
        "# Signal Forward Return Smoke",
        "",
        f"- Signal input: {_wikilink(signals_input)}",
        f"- Price input: {_wikilink(price_input)}",
        f"- Horizons: `{','.join(str(horizon) for horizon in horizons)}` trading days",
        "- Mode: `paper_forward_return_smoke_only`",
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
            f"- Evaluation rows: `{summary['rows']}`",
            f"- Complete rows: `{summary['complete_rows']}`",
            "",
            "## Status Counts",
            "",
            "| Status | Count |",
            "| --- | ---: |",
        ]
    )
    for status, count in dict(summary["status_counts"]).items():
        lines.append(f"| `{status}` | {count} |")

    lines.extend(["", "## Average Complete Returns", "", "| Horizon | Avg raw return % | Avg directional score % |", "| ---: | ---: | ---: |"])
    avg_raw = dict(summary["avg_raw_return_by_horizon"])
    avg_directional = dict(summary["avg_directional_score_by_horizon"])
    for horizon in sorted({*avg_raw.keys(), *avg_directional.keys()}, key=int):
        lines.append(f"| {horizon} | {_format_float(avg_raw.get(horizon))} | {_format_float(avg_directional.get(horizon))} |")
    if not avg_raw and not avg_directional:
        lines.append("| `none` |  |  |")

    latest_complete = [row for row in rows if row.evaluation_status == "complete"][-30:]
    lines.extend(
        [
            "",
            "## Complete Row Sample",
            "",
            "| Signal date | Horizon | Forward date | State | Code | Company | Raw return % | Directional score % |",
            "| --- | ---: | --- | --- | --- | --- | ---: | ---: |",
        ]
    )
    for row in latest_complete:
        signal = row.signal
        lines.append(
            f"| {signal.get('date', '')} | {row.horizon} | {row.forward_date} | {signal.get('signal_state', '')} | "
            f"`{signal.get('code', '')}` | {signal.get('stock_name', '')} | "
            f"{_format_float(row.raw_forward_return_pct)} | {_format_float(row.directional_forward_score_pct)} |"
        )

    lines.extend(
        [
            "",
            "## Guardrails",
            "",
            "- This is a forward-return coverage/diagnostic smoke, not a Backtest.",
            "- The directional score is a diagnostic sign convention, not a PnL calculation.",
            "- Missing forward prices usually mean the current smoke window ends too soon after a signal date.",
            "- Keep Signal Candidate rows paper-only until full Point-in-Time status coverage, costs, OOS, and Bias Control pass.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Compute paper-only forward-return diagnostics for Signal Candidate rows.")
    parser.add_argument("--signals-input", required=True, type=Path)
    parser.add_argument("--price-input", required=True, type=Path)
    parser.add_argument("--horizons", default=",".join(str(value) for value in DEFAULT_HORIZONS))
    parser.add_argument("--csv-output", type=Path)
    parser.add_argument("--report-output", type=Path)
    args = parser.parse_args()

    try:
        horizons = _parse_horizons(args.horizons)
        signal_rows = _read_csv(
            args.signals_input,
            {"date", "code", "stock_name", "close", "signal_state"},
            "Signal Candidate",
        )
        price_rows = _read_csv(args.price_input, {"date", "code", "close"}, "Price")
        rows = evaluate_forward_returns(signal_rows, price_rows, horizons)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc

    if args.csv_output:
        write_csv(rows, args.csv_output)
    report = render_report(
        rows=rows,
        summary=summarize(rows),
        signals_input=args.signals_input,
        price_input=args.price_input,
        horizons=horizons,
        csv_output=args.csv_output,
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
