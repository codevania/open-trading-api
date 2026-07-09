"""Summarize Quant Backtest and live-trading readiness gates.

The checker reads already-generated local research artifacts. It does not call
KIS, KRX, or any broker API, and it never upgrades readiness on its own.
"""

from __future__ import annotations

import argparse
import csv
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from quant_io import write_text_lf


DEFAULT_MIN_MARKET_DATES = 20
DEFAULT_MIN_LIQUIDITY_LOOKBACK = 20


@dataclass(frozen=True)
class Gate:
    name: str
    status: str
    evidence: str
    next_action: str


def _read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise ValueError(f"missing CSV: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [{key: (value or "").strip() for key, value in row.items()} for row in csv.DictReader(handle)]


def _date_count(rows: list[dict[str, str]]) -> int:
    return len({row.get("date", "") for row in rows if row.get("date", "")})


def _count(rows: list[dict[str, str]], column: str, value: str) -> int:
    return sum(1 for row in rows if row.get(column, "") == value)


def _int_value(row: dict[str, str], column: str) -> int:
    text = row.get(column, "").strip()
    if not text:
        return 0
    try:
        return int(float(text))
    except ValueError:
        return 0


def _sorted_numeric_strings(values: set[str]) -> list[str]:
    def key(value: str) -> tuple[int, float | str]:
        try:
            return (0, float(value))
        except ValueError:
            return (1, value)

    return sorted(values, key=key)


def _float_value(row: dict[str, str], column: str) -> float:
    text = row.get(column, "").strip()
    if not text:
        return 0.0
    try:
        return float(text)
    except ValueError:
        return 0.0


def _read_text(path: Path | None) -> str:
    if path is None or not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def _markdown_metric(text: str, metric: str) -> str:
    match = re.search(rf"\| {re.escape(metric)} \| ([^|]+) \|", text)
    if not match:
        return ""
    return match.group(1).strip().strip("`")


def _markdown_code_metric(text: str, metric: str) -> str:
    match = re.search(rf"\| `{re.escape(metric)}` \| ([^|]+) \|", text)
    if not match:
        return ""
    return match.group(1).strip().strip("`")


def _lifecycle_missing_by_status(text: str) -> str:
    counts: list[str] = []
    for status_type in ("managed_issue", "market_alert", "trading_halt"):
        value = _markdown_code_metric(text, status_type)
        if not value:
            continue
        if value and value != "0":
            counts.append(f"{status_type}={value}")
    return ",".join(counts)


def _kis_preflight_gate(path: Path | None) -> Gate:
    text = _read_text(path)
    if not text:
        return Gate(
            "kis_demo_account",
            "blocked",
            "no local KIS demo account preflight report supplied",
            "fill local demo account config and rerun account preflight",
        )
    if "Ready for read-only demo account calls: `true`" in text:
        return Gate(
            "kis_demo_account",
            "pass_read_only_only",
            "local demo account preflight reports read-only readiness true",
            "add buying-power and sellable-quantity checks before any order executor",
        )
    if "KIS_PAPER_STOCK" in text and "fail" in text:
        evidence = "local demo account preflight reports KIS_PAPER_STOCK missing or invalid"
    else:
        evidence = "local demo account preflight is not ready"
    return Gate("kis_demo_account", "blocked", evidence, "fill KIS_PAPER_STOCK locally and rerun account preflight")


def _backtest_contract_gate(path: Path | None) -> Gate | None:
    if path is None:
        return None
    text = _read_text(path)
    if not text:
        return Gate(
            "backtest_input_contract",
            "hold",
            "no local Backtest input contract report supplied",
            "run quant_backtest_input_contract_validate.py on current smoke artifacts",
        )
    if "Contract status: `pass_smoke`" in text and "Order intent generated: `false`" in text:
        return Gate(
            "backtest_input_contract",
            "pass_smoke",
            "local contract report is pass_smoke and reports no order intents",
            "keep contract validation aligned whenever smoke inputs change",
        )
    return Gate(
        "backtest_input_contract",
        "hold",
        "local contract report is not pass_smoke",
        "repair contract failures before wiring a Backtest engine",
    )


def _backtest_pnl_gate(path: Path | None) -> Gate | None:
    if path is None:
        return None
    text = _read_text(path)
    if not text:
        return Gate(
            "backtest_pnl_smoke",
            "hold",
            "no local Backtest PnL smoke report supplied",
            "run quant_backtest_pnl_smoke.py on current portfolio target and forward-return rows",
        )
    if "PnL smoke status: `pass_smoke`" in text and "Order intent generated: `false`" in text:
        return Gate(
            "backtest_pnl_smoke",
            "pass_smoke",
            "local PnL smoke report is pass_smoke and reports no order intents",
            "keep PnL smoke diagnostic-only until costs, benchmark, OOS, and Bias Control are wired",
        )
    return Gate(
        "backtest_pnl_smoke",
        "hold",
        "local PnL smoke report is not pass_smoke",
        "repair PnL smoke coverage before interpreting any return diagnostics",
    )


def _backtest_assumptions_gate(path: Path | None) -> Gate | None:
    if path is None:
        return None
    text = _read_text(path)
    if not text:
        return Gate(
            "backtest_assumptions",
            "hold",
            "no local Backtest assumption validation report supplied",
            "run quant_backtest_assumptions_validate.py on the current assumption config",
        )
    if "Assumption status: `pass_assumption_only`" in text and "Order intent generated: `false`" in text:
        return Gate(
            "backtest_assumptions",
            "pass_assumption_only",
            "local cost/benchmark assumptions reconcile but are not a Backtest result",
            "replace placeholder commission with actual KIS fee schedule and wire benchmark returns into the engine",
        )
    return Gate(
        "backtest_assumptions",
        "hold",
        "local Backtest assumption report is not pass_assumption_only",
        "repair cost or benchmark assumption checks before wiring a Backtest engine",
    )


def _benchmark_returns_gate(path: Path | None) -> Gate | None:
    if path is None:
        return None
    text = _read_text(path)
    if not text:
        return Gate(
            "benchmark_returns_smoke",
            "hold",
            "no local benchmark return smoke report supplied",
            "run quant_benchmark_return_smoke.py on current Signal Candidate dates and KRX index rows",
        )
    if (
        "Mode: `paper_benchmark_return_smoke_only`" in text
        and "Order intent generated: `false`" in text
        and "Backtest readiness: `hold`" in text
    ):
        return Gate(
            "benchmark_returns_smoke",
            "pass_smoke",
            "local benchmark return smoke report is diagnostic-only and reports no order intents",
            "promote benchmark comparison from PnL smoke into the Backtest engine only after Point-in-Time and cost gates are ready",
        )
    return Gate(
        "benchmark_returns_smoke",
        "hold",
        "local benchmark return report is not a recognized smoke-only report",
        "repair benchmark return smoke before using it as Backtest comparison input",
    )


def _backtest_attribution_gate(path: Path | None) -> Gate | None:
    if path is None:
        return None
    text = _read_text(path)
    if not text:
        return Gate(
            "backtest_attribution_smoke",
            "hold",
            "no local Backtest attribution smoke report supplied",
            "run quant_backtest_attribution_smoke.py on current PnL smoke rows and cost assumptions",
        )
    if (
        "Attribution status: `pass_smoke_assumption_only`" in text
        and "Order intent generated: `false`" in text
        and "Backtest readiness: `hold`" in text
    ):
        evidence = "local attribution smoke links costs and benchmark-active return but remains assumption-only"
        if "broker_fee_override_required=true" in text:
            evidence += "; broker fee override still required"
        return Gate(
            "backtest_attribution_smoke",
            "pass_smoke_assumption_only",
            evidence,
            "replace assumed costs with actual KIS fees before production Backtest interpretation",
        )
    return Gate(
        "backtest_attribution_smoke",
        "hold",
        "local attribution report is not a recognized smoke-only assumption report",
        "repair attribution smoke before using cost or active-return diagnostics",
    )


def _oos_walk_forward_gate(path: Path | None) -> Gate | None:
    if path is None:
        return None
    text = _read_text(path)
    if not text:
        return Gate(
            "oos_walk_forward_preflight",
            "hold",
            "no local OOS/Walk-Forward preflight report supplied",
            "run quant_oos_walk_forward_preflight.py on current attribution smoke rows",
        )
    if (
        "OOS/WF preflight status: `pass_smoke_plumbing_only`" in text
        and "Order intent generated: `false`" in text
        and "OOS readiness: `hold`" in text
        and "Backtest readiness: `hold`" in text
    ):
        evidence = "local OOS/Walk-Forward temporal fold plumbing exists but readiness remains hold"
        if "broker_fee_override_required=true" in text:
            evidence += "; broker fee override still required"
        return Gate(
            "oos_walk_forward_preflight",
            "pass_smoke_plumbing_only",
            evidence,
            "run production OOS only after Point-in-Time coverage, actual costs, and Backtest engine gates pass",
        )
    return Gate(
        "oos_walk_forward_preflight",
        "hold",
        "local OOS/Walk-Forward report is not a recognized smoke-only preflight report",
        "repair OOS/Walk-Forward preflight before using temporal split diagnostics",
    )


def _bias_control_gate(path: Path | None) -> Gate | None:
    if path is None:
        return None
    text = _read_text(path)
    if not text:
        return Gate(
            "bias_control_preflight",
            "hold",
            "no local Bias Control preflight report supplied",
            "run quant_bias_control_preflight.py on the latest readiness and OOS reports",
        )
    if (
        "Bias Control status: `hold`" in text
        and "Order intent generated: `false`" in text
        and "Backtest readiness: `hold`" in text
    ):
        return Gate(
            "bias_control_preflight",
            "hold",
            "local Bias Control preflight exists and correctly keeps Bias Control at hold",
            "resolve Point-in-Time, actual costs, production OOS, and live-control blockers before any Bias Control pass",
        )
    if (
        "Bias Control status: `pass_smoke`" in text
        and "Order intent generated: `false`" in text
        and "Backtest readiness: `hold`" in text
    ):
        return Gate(
            "bias_control_preflight",
            "pass_smoke",
            "local Bias Control preflight reports smoke-only pass while Backtest remains hold",
            "do not treat smoke-only Bias Control as production pass",
        )
    return Gate(
        "bias_control_preflight",
        "hold",
        "local Bias Control report is not a recognized preflight report",
        "repair Bias Control preflight before using it in readiness summaries",
    )


def _status_evidence_collection_plan_gate(path: Path | None) -> Gate | None:
    if path is None:
        return None
    text = _read_text(path)
    if not text:
        return Gate(
            "point_in_time_status_evidence_collection_plan",
            "hold",
            "status evidence collection plan path was supplied but could not be read",
            "rerun quant_point_in_time_status_evidence_collection_plan.py",
        )
    if (
        "Point-in-Time Status Evidence Collection Plan" in text
        and "Order intent generated: `false`" in text
        and "Backtest readiness impact: `hold`" in text
    ):
        plan_rows = _markdown_metric(text, "Collection plan rows") or "unknown"
        blocker_counts = []
        for blocker in ("source_manifest_evidence", "release_resume_evidence", "market_label_resolution"):
            count = _markdown_code_metric(text, blocker)
            if count:
                blocker_counts.append(f"{blocker}={count}")
        evidence = f"local collection plan identifies {plan_rows} pending evidence rows and does not prove source coverage"
        if blocker_counts:
            evidence += f"; blockers {','.join(blocker_counts)}"
        return Gate(
            "point_in_time_status_evidence_collection_plan",
            "plan_only",
            evidence,
            "collect official raw evidence, fill source manifest, and rerun coverage audit",
        )
    return Gate(
        "point_in_time_status_evidence_collection_plan",
        "hold",
        "local status evidence collection plan is not a recognized plan-only report",
        "rerun quant_point_in_time_status_evidence_collection_plan.py",
    )


def _status_evidence_collection_queue_gate(path: Path | None) -> Gate | None:
    if path is None:
        return None
    text = _read_text(path)
    if not text:
        return Gate(
            "point_in_time_status_evidence_collection_queue",
            "hold",
            "status evidence collection queue path was supplied but could not be read",
            "rerun quant_point_in_time_status_evidence_collection_queue.py",
        )
    if (
        "Point-in-Time Status Evidence Collection Queue" in text
        and "Order intent generated: `false`" in text
        and "Backtest readiness impact: `hold`" in text
    ):
        queue_batches = _markdown_metric(text, "Queue batches") or "unknown"
        queued_rows = _markdown_metric(text, "Queued source rows") or "unknown"
        priority_counts = []
        for priority in ("1", "2", "3"):
            count = _markdown_code_metric(text, priority)
            if count:
                priority_counts.append(f"P{priority}={count}")
        evidence = f"local collection queue groups plan rows into {queue_batches} batches with {queued_rows} queued source rows"
        if priority_counts:
            evidence += f"; priority batches {','.join(priority_counts)}"
        return Gate(
            "point_in_time_status_evidence_collection_queue",
            "plan_only",
            evidence,
            "execute P1 source-manifest batches before P2 release/resume and P3 market-label batches",
        )
    return Gate(
        "point_in_time_status_evidence_collection_queue",
        "hold",
        "local status evidence collection queue is not a recognized plan-only report",
        "rerun quant_point_in_time_status_evidence_collection_queue.py",
    )


def _status_source_manifest_fill_packet_gate(path: Path | None) -> Gate | None:
    if path is None:
        return None
    text = _read_text(path)
    if not text:
        return Gate(
            "point_in_time_status_source_manifest_fill_packet",
            "hold",
            "source manifest fill packet path was supplied but could not be read",
            "rerun quant_point_in_time_status_source_manifest_fill_packet.py",
        )
    if (
        "Point-in-Time Status Source Manifest Fill Packet" in text
        and "Order intent generated: `false`" in text
        and "Backtest readiness impact: `hold`" in text
    ):
        fill_rows = _markdown_metric(text, "Fill packet rows") or "unknown"
        evidence = f"local P1 source-manifest fill packet has {fill_rows} rows but does not prove source coverage"
        if "not source coverage evidence" in text:
            evidence += "; report explicitly labels it as non-evidence"
        return Gate(
            "point_in_time_status_source_manifest_fill_packet",
            "plan_only",
            evidence,
            "capture official raw files, fill source_url/raw_path/confidence, then materialize and validate the manifest",
        )
    return Gate(
        "point_in_time_status_source_manifest_fill_packet",
        "hold",
        "local source manifest fill packet is not a recognized plan-only report",
        "rerun quant_point_in_time_status_source_manifest_fill_packet.py",
    )


def _status_source_manifest_materialize_gate(path: Path | None) -> Gate | None:
    if path is None:
        return None
    text = _read_text(path)
    if not text:
        return Gate(
            "point_in_time_status_source_manifest_materialized",
            "hold",
            "source manifest materialization report path was supplied but could not be read",
            "rerun quant_point_in_time_status_source_manifest_materialize.py after fill-packet capture fields are filled",
        )
    if (
        "Point-in-Time Status Source Manifest Materialize" in text
        and "Order intent generated: `false`" in text
        and "Backtest readiness impact: `hold`" in text
    ):
        manifest_rows = _markdown_metric(text, "Manifest rows") or "unknown"
        return Gate(
            "point_in_time_status_source_manifest_materialized",
            "materialized_unvalidated",
            f"local filled packet materialized {manifest_rows} source manifest rows, but validation and coverage audit are still required",
            "run quant_point_in_time_status_source_manifest_validate.py, then rerun status coverage audit",
        )
    return Gate(
        "point_in_time_status_source_manifest_materialized",
        "hold",
        "local source manifest materialization report is not a recognized materialization report",
        "rerun quant_point_in_time_status_source_manifest_materialize.py after official raw capture",
    )


def _status_coverage_gate(status_coverage: str, path: Path | None, lifecycle_gap_report: Path | None) -> Gate:
    text = _read_text(path)
    lifecycle_gap_text = _read_text(lifecycle_gap_report)
    if path is not None and not text:
        return Gate(
            "point_in_time_status_coverage",
            "hold",
            "status coverage report path was supplied but could not be read",
            "rerun quant_point_in_time_status_coverage_audit.py",
        )
    if status_coverage == "historical_complete" and (path is None or "Coverage status: `pass`" in text):
        return Gate(
            "point_in_time_status_coverage",
            "pass",
            f"status coverage mode is {status_coverage}",
            "keep auditing coverage whenever the market-data window changes",
        )
    if text and "Coverage status: `hold`" in text:
        evidence = f"status coverage mode is {status_coverage}; local coverage audit reports hold"
        manifest_validation = _markdown_metric(text, "Source coverage manifest validation")
        if manifest_validation:
            evidence += f"; source manifest validation={manifest_validation}"
        missing_source_types = _markdown_metric(text, "Source coverage missing status types")
        if missing_source_types and missing_source_types != "none":
            evidence += f"; missing source coverage={missing_source_types}"
        lifecycle_missing = _markdown_metric(lifecycle_gap_text, "Missing release/resume groups")
        if lifecycle_missing:
            evidence += f"; lifecycle missing release/resume groups={lifecycle_missing}"
        lifecycle_missing_by_status = _lifecycle_missing_by_status(lifecycle_gap_text)
        if lifecycle_missing_by_status:
            evidence += f"; lifecycle missing by status={lifecycle_missing_by_status}"
        return Gate(
            "point_in_time_status_coverage",
            "hold",
            evidence,
            "replace current-snapshot smoke with historical status-event coverage by rebalance date",
        )
    return Gate(
        "point_in_time_status_coverage",
        "hold",
        f"status coverage mode is {status_coverage}",
        "replace current-snapshot smoke with historical status-event coverage by rebalance date",
    )


def evaluate_readiness(
    *,
    liquidity_rows: list[dict[str, str]],
    signal_rows: list[dict[str, str]],
    forward_return_rows: list[dict[str, str]] | None = None,
    portfolio_target_rows: list[dict[str, str]] | None = None,
    backtest_contract_report: Path | None = None,
    backtest_pnl_report: Path | None = None,
    backtest_assumptions_report: Path | None = None,
    benchmark_returns_report: Path | None = None,
    backtest_attribution_report: Path | None = None,
    oos_walk_forward_report: Path | None = None,
    bias_control_report: Path | None = None,
    status_coverage_report: Path | None = None,
    status_lifecycle_gap_report: Path | None = None,
    status_evidence_collection_plan_report: Path | None = None,
    status_evidence_collection_queue_report: Path | None = None,
    status_source_manifest_fill_packet_report: Path | None = None,
    status_source_manifest_materialize_report: Path | None = None,
    kis_preflight_report: Path | None,
    min_market_dates: int = DEFAULT_MIN_MARKET_DATES,
    min_liquidity_lookback: int = DEFAULT_MIN_LIQUIDITY_LOOKBACK,
    status_coverage: str = "current_snapshot_smoke",
) -> tuple[list[Gate], dict[str, Any]]:
    if min_market_dates <= 0:
        raise ValueError("min_market_dates must be positive")
    if min_liquidity_lookback <= 0:
        raise ValueError("min_liquidity_lookback must be positive")

    date_count = _date_count(liquidity_rows)
    include_rows = _count(liquidity_rows, "pit_liquidity_final_status", "include")
    full_lookback_rows = sum(1 for row in liquidity_rows if _int_value(row, "pit_liquidity_rows_used") >= min_liquidity_lookback)
    signal_date_count = _date_count(signal_rows)
    buy_candidates = _count(signal_rows, "signal_state", "BUY candidate")
    sell_candidates = _count(signal_rows, "signal_state", "SELL candidate")
    forward_rows = forward_return_rows or []
    forward_complete_rows = _count(forward_rows, "evaluation_status", "complete")
    forward_horizons = _sorted_numeric_strings(
        {row.get("horizon_trading_days", "") for row in forward_rows if row.get("horizon_trading_days", "")}
    )
    portfolio_rows = portfolio_target_rows or []
    portfolio_date_count = _date_count(portfolio_rows)
    portfolio_order_intents = sum(1 for row in portfolio_rows if row.get("order_intent_generated", "").lower() != "false")
    portfolio_modes = {row.get("target_mode", "") for row in portfolio_rows if row.get("target_mode", "")}
    portfolio_gross_by_date: dict[str, float] = {}
    for row in portfolio_rows:
        date = row.get("date", "")
        if not date:
            continue
        portfolio_gross_by_date[date] = portfolio_gross_by_date.get(date, 0.0) + _float_value(row, "target_weight")

    gates = [
        Gate(
            "market_data_window",
            "pass" if date_count >= min_market_dates else "hold",
            f"{date_count} market-data dates available; minimum configured gate is {min_market_dates}",
            "extend KRX OpenAPI market-data collection" if date_count < min_market_dates else "keep extending for production strategy lookbacks",
        ),
        Gate(
            "liquidity_filter",
            "pass_smoke" if full_lookback_rows > 0 and include_rows > 0 else "hold",
            f"{include_rows} include rows; {full_lookback_rows} rows evaluated with at least {min_liquidity_lookback}-day lookback",
            "keep 20-day Liquidity Filter aligned with expanded status/date windows",
        ),
        Gate(
            "signal_candidates",
            "pass_smoke" if signal_rows else "hold",
            f"{len(signal_rows)} candidates across {signal_date_count} dates; BUY={buy_candidates}, SELL={sell_candidates}",
            "keep candidates paper-only until Backtest/OOS/Bias Control pass",
        ),
    ]
    if forward_return_rows is not None:
        gates.append(
            Gate(
                "forward_return_smoke",
                "pass_smoke" if forward_complete_rows > 0 else "hold",
                f"{forward_complete_rows}/{len(forward_rows)} forward-return rows complete across horizons {','.join(forward_horizons) or 'none'}",
                "extend market-data window so forward-return coverage reaches production horizons",
            )
        )
    if portfolio_target_rows is not None:
        portfolio_is_smoke_only = bool(portfolio_rows) and portfolio_order_intents == 0 and portfolio_modes == {
            "paper_portfolio_target_smoke_only"
        }
        gates.append(
            Gate(
                "portfolio_targets_smoke",
                "pass_smoke" if portfolio_is_smoke_only else "hold",
                f"{len(portfolio_rows)} target rows across {portfolio_date_count} dates; order-intent rows={portfolio_order_intents}",
                "keep target weights diagnostic-only until Backtest cost/benchmark/OOS gates are wired",
            )
        )

    contract_gate = _backtest_contract_gate(backtest_contract_report)
    if contract_gate is not None:
        gates.append(contract_gate)

    pnl_gate = _backtest_pnl_gate(backtest_pnl_report)
    if pnl_gate is not None:
        gates.append(pnl_gate)

    assumptions_gate = _backtest_assumptions_gate(backtest_assumptions_report)
    if assumptions_gate is not None:
        gates.append(assumptions_gate)

    benchmark_gate = _benchmark_returns_gate(benchmark_returns_report)
    if benchmark_gate is not None:
        gates.append(benchmark_gate)

    attribution_gate = _backtest_attribution_gate(backtest_attribution_report)
    if attribution_gate is not None:
        gates.append(attribution_gate)

    oos_gate = _oos_walk_forward_gate(oos_walk_forward_report)
    if oos_gate is not None:
        gates.append(oos_gate)

    bias_gate = _bias_control_gate(bias_control_report)
    if bias_gate is not None:
        gates.append(bias_gate)

    status_evidence_plan_gate = _status_evidence_collection_plan_gate(status_evidence_collection_plan_report)
    if status_evidence_plan_gate is not None:
        gates.append(status_evidence_plan_gate)

    status_evidence_queue_gate = _status_evidence_collection_queue_gate(status_evidence_collection_queue_report)
    if status_evidence_queue_gate is not None:
        gates.append(status_evidence_queue_gate)

    status_source_manifest_fill_packet_gate = _status_source_manifest_fill_packet_gate(
        status_source_manifest_fill_packet_report
    )
    if status_source_manifest_fill_packet_gate is not None:
        gates.append(status_source_manifest_fill_packet_gate)

    status_source_manifest_materialize_gate = _status_source_manifest_materialize_gate(
        status_source_manifest_materialize_report
    )
    if status_source_manifest_materialize_gate is not None:
        gates.append(status_source_manifest_materialize_gate)

    gates.append(_status_coverage_gate(status_coverage, status_coverage_report, status_lifecycle_gap_report))
    gates.extend(
        [
            Gate(
                "backtest_engine",
                "hold",
                "Backtest engine is not wired to Point-in-Time Universe, costs, benchmark, OOS, and Bias Control",
                "build Backtest only after Point-in-Time status coverage is acceptable for the selected scope",
            ),
            Gate(
                "live_trading_controls",
                "blocked",
                "no order executor, kill switch, explicit confirmation gate, status/cancel flow, or read-only account checks are complete",
                "finish demo read-only account gates before any order executor",
            ),
            _kis_preflight_gate(kis_preflight_report),
        ]
    )
    summary = {
        "market_data_dates": date_count,
        "liquidity_include_rows": include_rows,
        "liquidity_full_lookback_rows": full_lookback_rows,
        "signal_rows": len(signal_rows),
        "signal_dates": signal_date_count,
        "buy_candidates": buy_candidates,
        "sell_candidates": sell_candidates,
        "forward_return_rows": len(forward_rows) if forward_return_rows is not None else None,
        "forward_return_complete_rows": forward_complete_rows if forward_return_rows is not None else None,
        "forward_return_horizons": ",".join(forward_horizons) if forward_return_rows is not None else None,
        "portfolio_target_rows": len(portfolio_rows) if portfolio_target_rows is not None else None,
        "portfolio_target_dates": portfolio_date_count if portfolio_target_rows is not None else None,
        "portfolio_target_max_gross_weight": max(portfolio_gross_by_date.values(), default=0.0)
        if portfolio_target_rows is not None
        else None,
        "backtest_contract_report_supplied": backtest_contract_report is not None,
        "backtest_pnl_report_supplied": backtest_pnl_report is not None,
        "backtest_assumptions_report_supplied": backtest_assumptions_report is not None,
        "benchmark_returns_report_supplied": benchmark_returns_report is not None,
        "backtest_attribution_report_supplied": backtest_attribution_report is not None,
        "oos_walk_forward_report_supplied": oos_walk_forward_report is not None,
        "bias_control_report_supplied": bias_control_report is not None,
        "status_coverage_report_supplied": status_coverage_report is not None,
        "status_lifecycle_gap_report_supplied": status_lifecycle_gap_report is not None,
        "status_evidence_collection_plan_report_supplied": status_evidence_collection_plan_report is not None,
        "status_evidence_collection_queue_report_supplied": status_evidence_collection_queue_report is not None,
        "status_source_manifest_fill_packet_report_supplied": status_source_manifest_fill_packet_report is not None,
        "status_source_manifest_materialize_report_supplied": status_source_manifest_materialize_report is not None,
        "backtest_readiness": "hold",
        "live_trading_readiness": "blocked",
    }
    return gates, summary


def _wikilink(path: Path) -> str:
    rendered = path.as_posix()
    if path.suffix == ".md":
        target = rendered[: -len(path.suffix)]
        return f"[[{target}|{rendered}]]"
    return f"[[{rendered}|{rendered}]]"


def _render_report(
    *,
    gates: list[Gate],
    summary: dict[str, Any],
    liquidity_input: Path,
    signals_input: Path,
    forward_returns_input: Path | None,
    portfolio_targets_input: Path | None,
    backtest_contract_report: Path | None,
    backtest_pnl_report: Path | None,
    backtest_assumptions_report: Path | None,
    benchmark_returns_report: Path | None,
    backtest_attribution_report: Path | None,
    oos_walk_forward_report: Path | None,
    bias_control_report: Path | None,
    status_coverage_report: Path | None,
    status_lifecycle_gap_report: Path | None,
    status_evidence_collection_plan_report: Path | None,
    status_evidence_collection_queue_report: Path | None,
    status_source_manifest_fill_packet_report: Path | None,
    status_source_manifest_materialize_report: Path | None,
    kis_preflight_report: Path | None,
    status_coverage: str,
) -> str:
    lines = [
        "# Quant Readiness Check",
        "",
        f"- Liquidity input: {_wikilink(liquidity_input)}",
        f"- Signal input: {_wikilink(signals_input)}",
        f"- Forward-return input: {_wikilink(forward_returns_input) if forward_returns_input else '`not_supplied`'}",
        f"- Portfolio-target input: {_wikilink(portfolio_targets_input) if portfolio_targets_input else '`not_supplied`'}",
        f"- Backtest contract report: {_wikilink(backtest_contract_report) if backtest_contract_report else '`not_supplied`'}",
        f"- Backtest PnL smoke report: {_wikilink(backtest_pnl_report) if backtest_pnl_report else '`not_supplied`'}",
        f"- Backtest assumptions report: {_wikilink(backtest_assumptions_report) if backtest_assumptions_report else '`not_supplied`'}",
        f"- Benchmark returns report: {_wikilink(benchmark_returns_report) if benchmark_returns_report else '`not_supplied`'}",
        f"- Backtest attribution smoke report: {_wikilink(backtest_attribution_report) if backtest_attribution_report else '`not_supplied`'}",
        f"- OOS/Walk-Forward preflight report: {_wikilink(oos_walk_forward_report) if oos_walk_forward_report else '`not_supplied`'}",
        f"- Bias Control preflight report: {_wikilink(bias_control_report) if bias_control_report else '`not_supplied`'}",
        f"- Status coverage audit report: {_wikilink(status_coverage_report) if status_coverage_report else '`not_supplied`'}",
        f"- Status lifecycle gap report: {_wikilink(status_lifecycle_gap_report) if status_lifecycle_gap_report else '`not_supplied`'}",
        f"- Status evidence collection plan report: {_wikilink(status_evidence_collection_plan_report) if status_evidence_collection_plan_report else '`not_supplied`'}",
        f"- Status evidence collection queue report: {_wikilink(status_evidence_collection_queue_report) if status_evidence_collection_queue_report else '`not_supplied`'}",
        f"- Status source manifest fill packet report: {_wikilink(status_source_manifest_fill_packet_report) if status_source_manifest_fill_packet_report else '`not_supplied`'}",
        f"- Status source manifest materialize report: {_wikilink(status_source_manifest_materialize_report) if status_source_manifest_materialize_report else '`not_supplied`'}",
        f"- KIS preflight report: {_wikilink(kis_preflight_report) if kis_preflight_report else '`not_supplied`'}",
        f"- Status coverage mode: `{status_coverage}`",
        "- KIS API call: `false`",
        "- Order intent generated: `false`",
        f"- Backtest readiness: `{summary['backtest_readiness']}`",
        f"- Live trading readiness: `{summary['live_trading_readiness']}`",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| Market-data dates | {summary['market_data_dates']} |",
        f"| Liquidity include rows | {summary['liquidity_include_rows']} |",
        f"| Liquidity full-lookback rows | {summary['liquidity_full_lookback_rows']} |",
        f"| Signal rows | {summary['signal_rows']} |",
        f"| Signal dates | {summary['signal_dates']} |",
        f"| BUY candidates | {summary['buy_candidates']} |",
        f"| SELL candidates | {summary['sell_candidates']} |",
    ]
    if summary.get("forward_return_rows") is not None:
        lines.extend(
            [
                f"| Forward-return rows | {summary['forward_return_rows']} |",
                f"| Forward-return complete rows | {summary['forward_return_complete_rows']} |",
            ]
        )
        if summary.get("forward_return_horizons"):
            lines.append(f"| Forward-return horizons | {summary['forward_return_horizons']} |")
    if summary.get("portfolio_target_rows") is not None:
        lines.extend(
            [
                f"| Portfolio target rows | {summary['portfolio_target_rows']} |",
                f"| Portfolio target dates | {summary['portfolio_target_dates']} |",
                f"| Portfolio max gross target weight | {summary['portfolio_target_max_gross_weight']:.4f} |",
            ]
        )

    lines.extend(
        [
            "",
            "## Gates",
            "",
            "| Gate | Status | Evidence | Next action |",
            "| --- | --- | --- | --- |",
        ]
    )
    for gate in gates:
        lines.append(f"| `{gate.name}` | `{gate.status}` | {gate.evidence} | {gate.next_action} |")

    lines.extend(
        [
            "",
            "## Guardrails",
            "",
            "- Passing smoke gates does not make the strategy Backtest-ready.",
            "- Do not create KIS order intents from Signal Candidate rows.",
            "- Keep raw credentials and account values out of tracked reports.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize Quant Backtest and live-trading readiness gates.")
    parser.add_argument("--liquidity-input", required=True, type=Path)
    parser.add_argument("--signals-input", required=True, type=Path)
    parser.add_argument("--forward-returns-input", type=Path)
    parser.add_argument("--portfolio-targets-input", type=Path)
    parser.add_argument("--backtest-contract-report", type=Path)
    parser.add_argument("--backtest-pnl-report", type=Path)
    parser.add_argument("--backtest-assumptions-report", type=Path)
    parser.add_argument("--benchmark-returns-report", type=Path)
    parser.add_argument("--backtest-attribution-report", type=Path)
    parser.add_argument("--oos-walk-forward-report", type=Path)
    parser.add_argument("--bias-control-report", type=Path)
    parser.add_argument("--status-coverage-report", type=Path)
    parser.add_argument("--status-lifecycle-gap-report", type=Path)
    parser.add_argument("--status-evidence-collection-plan-report", type=Path)
    parser.add_argument("--status-evidence-collection-queue-report", type=Path)
    parser.add_argument("--status-source-manifest-fill-packet-report", type=Path)
    parser.add_argument("--status-source-manifest-materialize-report", type=Path)
    parser.add_argument("--kis-preflight-report", type=Path)
    parser.add_argument("--status-coverage", default="current_snapshot_smoke")
    parser.add_argument("--min-market-dates", default=DEFAULT_MIN_MARKET_DATES, type=int)
    parser.add_argument("--min-liquidity-lookback", default=DEFAULT_MIN_LIQUIDITY_LOOKBACK, type=int)
    parser.add_argument("--report-output", type=Path)
    args = parser.parse_args()

    try:
        liquidity_rows = _read_csv(args.liquidity_input)
        signal_rows = _read_csv(args.signals_input)
        forward_return_rows = _read_csv(args.forward_returns_input) if args.forward_returns_input else None
        portfolio_target_rows = _read_csv(args.portfolio_targets_input) if args.portfolio_targets_input else None
        gates, summary = evaluate_readiness(
            liquidity_rows=liquidity_rows,
            signal_rows=signal_rows,
            forward_return_rows=forward_return_rows,
            portfolio_target_rows=portfolio_target_rows,
            backtest_contract_report=args.backtest_contract_report,
            backtest_pnl_report=args.backtest_pnl_report,
            backtest_assumptions_report=args.backtest_assumptions_report,
            benchmark_returns_report=args.benchmark_returns_report,
            backtest_attribution_report=args.backtest_attribution_report,
            oos_walk_forward_report=args.oos_walk_forward_report,
            bias_control_report=args.bias_control_report,
            status_coverage_report=args.status_coverage_report,
            status_lifecycle_gap_report=args.status_lifecycle_gap_report,
            status_evidence_collection_plan_report=args.status_evidence_collection_plan_report,
            status_evidence_collection_queue_report=args.status_evidence_collection_queue_report,
            status_source_manifest_fill_packet_report=args.status_source_manifest_fill_packet_report,
            status_source_manifest_materialize_report=args.status_source_manifest_materialize_report,
            kis_preflight_report=args.kis_preflight_report,
            min_market_dates=args.min_market_dates,
            min_liquidity_lookback=args.min_liquidity_lookback,
            status_coverage=args.status_coverage,
        )
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc

    report = _render_report(
        gates=gates,
        summary=summary,
        liquidity_input=args.liquidity_input,
        signals_input=args.signals_input,
        forward_returns_input=args.forward_returns_input,
        portfolio_targets_input=args.portfolio_targets_input,
        backtest_contract_report=args.backtest_contract_report,
        backtest_pnl_report=args.backtest_pnl_report,
        backtest_assumptions_report=args.backtest_assumptions_report,
        benchmark_returns_report=args.benchmark_returns_report,
        backtest_attribution_report=args.backtest_attribution_report,
        oos_walk_forward_report=args.oos_walk_forward_report,
        bias_control_report=args.bias_control_report,
        status_coverage_report=args.status_coverage_report,
        status_lifecycle_gap_report=args.status_lifecycle_gap_report,
        status_evidence_collection_plan_report=args.status_evidence_collection_plan_report,
        status_evidence_collection_queue_report=args.status_evidence_collection_queue_report,
        status_source_manifest_fill_packet_report=args.status_source_manifest_fill_packet_report,
        status_source_manifest_materialize_report=args.status_source_manifest_materialize_report,
        kis_preflight_report=args.kis_preflight_report,
        status_coverage=args.status_coverage,
    )
    if args.report_output:
        write_text_lf(args.report_output, report)
    else:
        print(report, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
