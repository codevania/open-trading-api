# Quant Readiness Check

- Liquidity input: [[_report/quant/research/2026-07-08-kind-status-point-in-time-liquidity-smoke-20d-20250102-20250404.rows.csv|_report/quant/research/2026-07-08-kind-status-point-in-time-liquidity-smoke-20d-20250102-20250404.rows.csv]]
- Signal input: [[_report/quant/research/2026-07-08-kind-status-point-in-time-momentum-signal-candidates-smoke-20d-20250102-20250404.rows.csv|_report/quant/research/2026-07-08-kind-status-point-in-time-momentum-signal-candidates-smoke-20d-20250102-20250404.rows.csv]]
- Forward-return input: [[_report/quant/research/2026-07-08-signal-forward-return-smoke-20d-20250102-20250404.rows.csv|_report/quant/research/2026-07-08-signal-forward-return-smoke-20d-20250102-20250404.rows.csv]]
- Portfolio-target input: [[_report/quant/research/2026-07-08-signal-portfolio-targets-smoke-20d-20250102-20250404.rows.csv|_report/quant/research/2026-07-08-signal-portfolio-targets-smoke-20d-20250102-20250404.rows.csv]]
- Backtest contract report: [[_report/quant/research/2026-07-08-backtest-input-contract-validate-20250102-20250404.md|_report/quant/research/2026-07-08-backtest-input-contract-validate-20250102-20250404.md]]
- Backtest PnL smoke report: [[_report/quant/research/2026-07-08-backtest-pnl-smoke-20d-20250102-20250404.md|_report/quant/research/2026-07-08-backtest-pnl-smoke-20d-20250102-20250404.md]]
- Backtest assumptions report: [[_report/quant/research/2026-07-08-backtest-cost-benchmark-assumptions-validate.md|_report/quant/research/2026-07-08-backtest-cost-benchmark-assumptions-validate.md]]
- Benchmark returns report: [[_report/quant/research/2026-07-08-benchmark-return-smoke-20d-20250102-20250404.md|_report/quant/research/2026-07-08-benchmark-return-smoke-20d-20250102-20250404.md]]
- Status coverage audit report: [[_report/quant/research/2026-07-08-point-in-time-status-coverage-audit-20250102-20250404-merged-snapshots.md|_report/quant/research/2026-07-08-point-in-time-status-coverage-audit-20250102-20250404-merged-snapshots.md]]
- KIS preflight report: [[_report/quant/research/2026-07-04-kis-demo-account-preflight.md|_report/quant/research/2026-07-04-kis-demo-account-preflight.md]]
- Status coverage mode: `current_snapshot_smoke`
- KIS API call: `false`
- Order intent generated: `false`
- Backtest readiness: `hold`
- Live trading readiness: `blocked`

## Summary

| Metric | Value |
| --- | ---: |
| Market-data dates | 62 |
| Liquidity include rows | 44235 |
| Liquidity full-lookback rows | 109890 |
| Signal rows | 1720 |
| Signal dates | 43 |
| BUY candidates | 860 |
| SELL candidates | 860 |
| Forward-return rows | 3440 |
| Forward-return complete rows | 3200 |
| Forward-return horizons | 1,5 |
| Portfolio target rows | 860 |
| Portfolio target dates | 43 |
| Portfolio max gross target weight | 1.0000 |

## Gates

| Gate | Status | Evidence | Next action |
| --- | --- | --- | --- |
| `market_data_window` | `pass` | 62 market-data dates available; minimum configured gate is 20 | keep extending for production strategy lookbacks |
| `liquidity_filter` | `pass_smoke` | 44235 include rows; 109890 rows evaluated with at least 20-day lookback | keep 20-day Liquidity Filter aligned with expanded status/date windows |
| `signal_candidates` | `pass_smoke` | 1720 candidates across 43 dates; BUY=860, SELL=860 | keep candidates paper-only until Backtest/OOS/Bias Control pass |
| `forward_return_smoke` | `pass_smoke` | 3200/3440 forward-return rows complete across horizons 1,5 | extend market-data window so forward-return coverage reaches production horizons |
| `portfolio_targets_smoke` | `pass_smoke` | 860 target rows across 43 dates; order-intent rows=0 | keep target weights diagnostic-only until Backtest cost/benchmark/OOS gates are wired |
| `backtest_input_contract` | `pass_smoke` | local contract report is pass_smoke and reports no order intents | keep contract validation aligned whenever smoke inputs change |
| `backtest_pnl_smoke` | `pass_smoke` | local PnL smoke report is pass_smoke and reports no order intents | keep PnL smoke diagnostic-only until costs, benchmark, OOS, and Bias Control are wired |
| `backtest_assumptions` | `pass_assumption_only` | local cost/benchmark assumptions reconcile but are not a Backtest result | replace placeholder commission with actual KIS fee schedule and wire benchmark returns into the engine |
| `benchmark_returns_smoke` | `pass_smoke` | local benchmark return smoke report is diagnostic-only and reports no order intents | promote benchmark comparison from PnL smoke into the Backtest engine only after Point-in-Time and cost gates are ready |
| `point_in_time_status_coverage` | `hold` | status coverage mode is current_snapshot_smoke; local coverage audit reports hold | replace current-snapshot smoke with historical status-event coverage by rebalance date |
| `backtest_engine` | `hold` | Backtest engine is not wired to Point-in-Time Universe, costs, benchmark, OOS, and Bias Control | build Backtest only after Point-in-Time status coverage is acceptable for the selected scope |
| `live_trading_controls` | `blocked` | no order executor, kill switch, explicit confirmation gate, status/cancel flow, or read-only account checks are complete | finish demo read-only account gates before any order executor |
| `kis_demo_account` | `blocked` | local demo account preflight reports KIS_PAPER_STOCK missing or invalid | fill KIS_PAPER_STOCK locally and rerun account preflight |

## Guardrails

- Passing smoke gates does not make the strategy Backtest-ready.
- Do not create KIS order intents from Signal Candidate rows.
- Keep raw credentials and account values out of tracked reports.
