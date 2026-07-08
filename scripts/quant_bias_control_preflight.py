"""Summarize paper-only Quant Bias Control preflight gates.

The preflight reads local readiness and diagnostic reports. It does not fetch
data, rerun a Backtest, optimize parameters, or generate order intents.
"""

from __future__ import annotations

import argparse
import csv
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:
    from quant_io import write_text_lf
except ModuleNotFoundError:  # pragma: no cover - used when imported as scripts.* in tests.
    from scripts.quant_io import write_text_lf


BIAS_MODE = "paper_bias_control_preflight_only"
OUTPUT_FIELDS = (
    "check_id",
    "category",
    "status",
    "evidence",
    "next_action",
    "bias_control_mode",
    "order_intent_generated",
)


@dataclass(frozen=True)
class BiasCheck:
    check_id: str
    category: str
    status: str
    evidence: str
    next_action: str


def _read_text(path: Path | None) -> str:
    if path is None:
        return ""
    if not path.exists():
        raise ValueError(f"report not found: {path}")
    return path.read_text(encoding="utf-8", errors="replace")


def _metric(text: str, label: str) -> str:
    match = re.search(rf"- {re.escape(label)}: `([^`]+)`", text)
    return match.group(1).strip() if match else ""


def _gate_status(text: str, gate_name: str) -> tuple[str, str]:
    match = re.search(rf"\| `{re.escape(gate_name)}` \| `([^`]+)` \| ([^|]+) \|", text)
    if not match:
        return "not_supplied", f"{gate_name} gate not found"
    return match.group(1).strip(), match.group(2).strip()


def _has_order_intents(texts: list[str]) -> bool:
    for text in texts:
        if "Order intent generated: `true`" in text:
            return True
    return False


def _check(
    check_id: str,
    category: str,
    status: str,
    evidence: str,
    next_action: str,
) -> BiasCheck:
    return BiasCheck(
        check_id=check_id,
        category=category,
        status=status,
        evidence=evidence.replace("|", "/"),
        next_action=next_action.replace("|", "/"),
    )


def build_bias_checks(
    *,
    readiness_text: str,
    oos_text: str = "",
    status_coverage_text: str = "",
    strategy_bias_texts: list[str] | None = None,
) -> tuple[list[BiasCheck], dict[str, Any]]:
    strategy_bias_texts = strategy_bias_texts or []
    texts = [readiness_text, oos_text, status_coverage_text, *strategy_bias_texts]
    if not readiness_text:
        raise ValueError("readiness report text is required")
    if _has_order_intents(texts):
        raise ValueError("Bias Control preflight refuses reports with generated order intents")

    point_status, point_evidence = _gate_status(readiness_text, "point_in_time_status_coverage")
    oos_status, oos_evidence = _gate_status(readiness_text, "oos_walk_forward_preflight")
    attribution_status, attribution_evidence = _gate_status(readiness_text, "backtest_attribution_smoke")
    benchmark_status, benchmark_evidence = _gate_status(readiness_text, "benchmark_returns_smoke")
    forward_status, forward_evidence = _gate_status(readiness_text, "forward_return_smoke")
    backtest_engine_status, backtest_engine_evidence = _gate_status(readiness_text, "backtest_engine")
    live_status, live_evidence = _gate_status(readiness_text, "live_trading_controls")
    kis_status, kis_evidence = _gate_status(readiness_text, "kis_demo_account")
    backtest_readiness = _metric(readiness_text, "Backtest readiness") or "hold"
    live_readiness = _metric(readiness_text, "Live trading readiness") or "blocked"

    broker_fee_required = "broker_fee_override_required=true" in oos_text or "broker fee override still required" in readiness_text
    oos_readiness = _metric(oos_text, "OOS readiness") or "hold"
    strategy_bias_hold_count = sum(1 for text in strategy_bias_texts if "hold" in text.lower())

    checks = [
        _check(
            "survivorship_bias",
            "Point-in-Time Universe",
            "pass" if point_status == "pass" else "hold",
            point_evidence,
            "obtain historical status-event coverage and a validated source manifest",
        ),
        _check(
            "lookahead_bias",
            "Signal timing",
            "pass_smoke" if forward_status == "pass_smoke" else "hold",
            forward_evidence,
            "keep signal, target, and forward-return timing separated by rebalance date",
        ),
        _check(
            "data_snooping",
            "OOS / Walk-Forward",
            "pass_smoke_plumbing_only" if oos_status == "pass_smoke_plumbing_only" else "hold",
            oos_evidence,
            "run production OOS only after Backtest and Point-in-Time gates pass",
        ),
        _check(
            "overfitting",
            "OOS readiness",
            "hold" if oos_readiness != "pass" else "pass",
            f"OOS readiness={oos_readiness}",
            "do not tune parameters from the current smoke fold results",
        ),
        _check(
            "cost_bias",
            "Costs and slippage",
            "hold" if broker_fee_required or attribution_status != "pass_smoke_assumption_only" else "pass_smoke",
            attribution_evidence,
            "replace assumed costs with actual KIS account/channel fee evidence",
        ),
        _check(
            "benchmark_bias",
            "Benchmark attribution",
            "pass_smoke" if benchmark_status == "pass_smoke" else "hold",
            benchmark_evidence,
            "wire benchmark attribution into the production Backtest engine",
        ),
        _check(
            "execution_bias",
            "Execution controls",
            "blocked" if live_status == "blocked" or live_readiness == "blocked" else "hold",
            live_evidence,
            "keep live trading blocked until account, order, cancel, and kill-switch gates pass",
        ),
        _check(
            "account_bias",
            "KIS demo account",
            "blocked" if kis_status == "blocked" else "hold",
            kis_evidence,
            "complete local read-only demo account preflight before any order executor",
        ),
        _check(
            "backtest_interpretation",
            "Backtest engine",
            "hold" if backtest_engine_status != "pass" or backtest_readiness != "pass" else "pass",
            f"{backtest_engine_evidence}; Backtest readiness={backtest_readiness}",
            "do not interpret smoke returns as strategy performance",
        ),
    ]
    if strategy_bias_texts:
        checks.append(
            _check(
                "strategy_bias_docs",
                "Strategy checklist",
                "hold" if strategy_bias_hold_count else "pass_smoke",
                f"{len(strategy_bias_texts)} strategy bias docs supplied; docs containing hold={strategy_bias_hold_count}",
                "keep strategy checklist in sync with generated evidence",
            )
        )

    status_counts = Counter(row.status for row in checks)
    blocking_statuses = {"hold", "blocked", "not_supplied"}
    overall_status = "hold" if any(row.status in blocking_statuses for row in checks) else "pass_smoke"
    summary = {
        "bias_control_status": overall_status,
        "backtest_readiness": backtest_readiness,
        "live_trading_readiness": live_readiness,
        "checks": len(checks),
        "status_counts": dict(sorted(status_counts.items())),
        "strategy_bias_docs": len(strategy_bias_texts),
        "broker_fee_override_required": broker_fee_required,
    }
    return checks, summary


def write_csv(rows: list[BiasCheck], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "check_id": row.check_id,
                    "category": row.category,
                    "status": row.status,
                    "evidence": row.evidence,
                    "next_action": row.next_action,
                    "bias_control_mode": BIAS_MODE,
                    "order_intent_generated": "false",
                }
            )


def _wikilink(path: Path) -> str:
    rendered = path.as_posix()
    return f"[[{rendered}|{rendered}]]"


def render_report(
    *,
    rows: list[BiasCheck],
    summary: dict[str, Any],
    readiness_report: Path,
    oos_report: Path | None,
    status_coverage_report: Path | None,
    strategy_bias_reports: list[Path],
    csv_output: Path | None,
) -> str:
    lines = [
        "# Bias Control Preflight",
        "",
        f"- Readiness report: {_wikilink(readiness_report)}",
        f"- OOS/Walk-Forward report: {_wikilink(oos_report) if oos_report else '`not_supplied`'}",
        f"- Status coverage report: {_wikilink(status_coverage_report) if status_coverage_report else '`not_supplied`'}",
        f"- Strategy bias reports: {', '.join(_wikilink(path) for path in strategy_bias_reports) if strategy_bias_reports else '`not_supplied`'}",
        f"- Bias Control mode: `{BIAS_MODE}`",
        f"- Bias Control status: `{summary['bias_control_status']}`",
        f"- Backtest readiness: `{summary['backtest_readiness']}`",
        f"- Live trading readiness: `{summary['live_trading_readiness']}`",
        "- KIS API call: `false`",
        "- KRX API call: `false`",
        "- Order intent generated: `false`",
        "- Interpretation: Bias Control preflight only, not a production `Backtest` or investment result",
    ]
    if csv_output is not None:
        lines.append(f"- Machine-readable checks: {_wikilink(csv_output)}")

    lines.extend(
        [
            "",
            "## Summary",
            "",
            "| Metric | Value |",
            "| --- | ---: |",
            f"| Checks | {summary['checks']} |",
            f"| Strategy bias docs | {summary['strategy_bias_docs']} |",
            f"| Broker fee override required | `{str(summary['broker_fee_override_required']).lower()}` |",
            "",
            "## Status Counts",
            "",
            "| Status | Count |",
            "| --- | ---: |",
        ]
    )
    for status, count in summary["status_counts"].items():
        lines.append(f"| `{status}` | {count} |")

    lines.extend(
        [
            "",
            "## Checks",
            "",
            "| Check | Category | Status | Evidence | Next action |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for row in rows:
        lines.append(f"| `{row.check_id}` | {row.category} | `{row.status}` | {row.evidence} | {row.next_action} |")

    lines.extend(
        [
            "",
            "## Guardrails",
            "",
            "- `pass_smoke` and `pass_smoke_plumbing_only` are not production Bias Control passes.",
            "- Current blocker classes remain historical `Point-in-Time` coverage, actual KIS fee override, production Backtest/OOS, and live trading controls.",
            "- Do not tune parameters or promote Signal Candidate rows from this preflight.",
            "- Keep `Live trading readiness` at `blocked`; this script never creates order intents.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize paper-only Quant Bias Control preflight gates.")
    parser.add_argument("--readiness-report", required=True, type=Path)
    parser.add_argument("--oos-walk-forward-report", type=Path)
    parser.add_argument("--status-coverage-report", type=Path)
    parser.add_argument("--strategy-bias-report", action="append", default=[], type=Path)
    parser.add_argument("--csv-output", type=Path)
    parser.add_argument("--report-output", type=Path)
    args = parser.parse_args()

    try:
        readiness_text = _read_text(args.readiness_report)
        oos_text = _read_text(args.oos_walk_forward_report)
        status_coverage_text = _read_text(args.status_coverage_report)
        strategy_texts = [_read_text(path) for path in args.strategy_bias_report]
        rows, summary = build_bias_checks(
            readiness_text=readiness_text,
            oos_text=oos_text,
            status_coverage_text=status_coverage_text,
            strategy_bias_texts=strategy_texts,
        )
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc

    if args.csv_output:
        write_csv(rows, args.csv_output)
    report = render_report(
        rows=rows,
        summary=summary,
        readiness_report=args.readiness_report,
        oos_report=args.oos_walk_forward_report,
        status_coverage_report=args.status_coverage_report,
        strategy_bias_reports=args.strategy_bias_report,
        csv_output=args.csv_output,
    )
    if args.report_output:
        write_text_lf(args.report_output, report)
    else:
        print(report, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
