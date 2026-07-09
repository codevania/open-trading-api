# Bias Control Preflight

- Readiness report: [[_report/quant/research/2026-07-09-quant-readiness-check-merged-3snapshots-20d-20250102-20250418-price-through-20250502-oos-preflight.md|_report/quant/research/2026-07-09-quant-readiness-check-merged-3snapshots-20d-20250102-20250418-price-through-20250502-oos-preflight.md]]
- OOS/Walk-Forward report: [[_report/quant/research/2026-07-09-oos-walk-forward-preflight-merged-3snapshots-20d-20250102-20250418-price-through-20250502.md|_report/quant/research/2026-07-09-oos-walk-forward-preflight-merged-3snapshots-20d-20250102-20250418-price-through-20250502.md]]
- Status coverage report: [[_report/quant/research/2026-07-09-point-in-time-status-coverage-audit-20250102-20250418-merged-3snapshots-market-enriched-81d.md|_report/quant/research/2026-07-09-point-in-time-status-coverage-audit-20250102-20250418-merged-3snapshots-market-enriched-81d.md]]
- Strategy bias reports: [[_report/quant/strategies/001-strategy-universe-momentum.bias-control.md|_report/quant/strategies/001-strategy-universe-momentum.bias-control.md]], [[_report/quant/strategies/002-strategy-universe-short-term-reversal.bias-control.md|_report/quant/strategies/002-strategy-universe-short-term-reversal.bias-control.md]]
- Bias Control mode: `paper_bias_control_preflight_only`
- Bias Control status: `hold`
- Backtest readiness: `hold`
- Live trading readiness: `blocked`
- KIS API call: `false`
- KRX API call: `false`
- Order intent generated: `false`
- Interpretation: Bias Control preflight only, not a production `Backtest` or investment result
- Machine-readable checks: [[_report/quant/research/2026-07-09-bias-control-preflight-merged-3snapshots-20d-20250102-20250418-price-through-20250502.rows.csv|_report/quant/research/2026-07-09-bias-control-preflight-merged-3snapshots-20d-20250102-20250418-price-through-20250502.rows.csv]]

## Summary

| Metric | Value |
| --- | ---: |
| Checks | 10 |
| Strategy bias docs | 2 |
| Broker fee override required | `true` |

## Status Counts

| Status | Count |
| --- | ---: |
| `blocked` | 2 |
| `hold` | 5 |
| `pass_smoke` | 2 |
| `pass_smoke_plumbing_only` | 1 |

## Checks

| Check | Category | Status | Evidence | Next action |
| --- | --- | --- | --- | --- |
| `survivorship_bias` | Point-in-Time Universe | `hold` | status coverage mode is current_snapshot_smoke; local coverage audit reports hold; source manifest validation=not_supplied; missing source coverage=managed_issue,trading_halt,market_alert,delisting; lifecycle missing release/resume groups=314; lifecycle missing by status=managed_issue=106,market_alert=78,trading_halt=130 | obtain historical status-event coverage and a validated source manifest |
| `lookahead_bias` | Signal timing | `pass_smoke` | 4240/4240 forward-return rows complete across horizons 1,5 | keep signal, target, and forward-return timing separated by rebalance date |
| `data_snooping` | OOS / Walk-Forward | `pass_smoke_plumbing_only` | local OOS/Walk-Forward temporal fold plumbing exists but readiness remains hold; broker fee override still required | run production OOS only after Backtest and Point-in-Time gates pass |
| `overfitting` | OOS readiness | `hold` | OOS readiness=hold | do not tune parameters from the current smoke fold results |
| `cost_bias` | Costs and slippage | `hold` | local attribution smoke links costs and benchmark-active return but remains assumption-only; broker fee override still required | replace assumed costs with actual KIS account/channel fee evidence |
| `benchmark_bias` | Benchmark attribution | `pass_smoke` | local benchmark return smoke report is diagnostic-only and reports no order intents | wire benchmark attribution into the production Backtest engine |
| `execution_bias` | Execution controls | `blocked` | no order executor, kill switch, explicit confirmation gate, status/cancel flow, or read-only account checks are complete | keep live trading blocked until account, order, cancel, and kill-switch gates pass |
| `account_bias` | KIS demo account | `blocked` | local demo account preflight reports KIS_PAPER_STOCK missing or invalid | complete local read-only demo account preflight before any order executor |
| `backtest_interpretation` | Backtest engine | `hold` | Backtest engine is not wired to Point-in-Time Universe, costs, benchmark, OOS, and Bias Control; Backtest readiness=hold | do not interpret smoke returns as strategy performance |
| `strategy_bias_docs` | Strategy checklist | `hold` | 2 strategy bias docs supplied; docs containing hold=2 | keep strategy checklist in sync with generated evidence |

## Guardrails

- `pass_smoke` and `pass_smoke_plumbing_only` are not production Bias Control passes.
- Current blocker classes remain historical `Point-in-Time` coverage, actual KIS fee override, production Backtest/OOS, and live trading controls.
- Do not tune parameters or promote Signal Candidate rows from this preflight.
- Keep `Live trading readiness` at `blocked`; this script never creates order intents.
