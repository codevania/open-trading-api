# Quant Readiness Check

- Liquidity input: [[_report/quant/research/2026-07-04-kind-status-point-in-time-liquidity-smoke-20d-20250102-20250207.rows.csv|_report/quant/research/2026-07-04-kind-status-point-in-time-liquidity-smoke-20d-20250102-20250207.rows.csv]]
- Signal input: [[_report/quant/research/2026-07-04-kind-status-point-in-time-momentum-signal-candidates-smoke-20d-20250102-20250207.rows.csv|_report/quant/research/2026-07-04-kind-status-point-in-time-momentum-signal-candidates-smoke-20d-20250102-20250207.rows.csv]]
- Forward-return input: [[_report/quant/research/2026-07-05-signal-forward-return-smoke-20d-20250102-20250207.rows.csv|_report/quant/research/2026-07-05-signal-forward-return-smoke-20d-20250102-20250207.rows.csv]]
- Portfolio-target input: [[_report/quant/research/2026-07-05-signal-portfolio-targets-smoke-20d-20250102-20250207.rows.csv|_report/quant/research/2026-07-05-signal-portfolio-targets-smoke-20d-20250102-20250207.rows.csv]]
- KIS preflight report: [[_report/quant/research/2026-07-04-kis-demo-account-preflight.md|_report/quant/research/2026-07-04-kis-demo-account-preflight.md]]
- Status coverage mode: `current_snapshot_smoke`
- KIS API call: `false`
- Order intent generated: `false`
- Backtest readiness: `hold`
- Live trading readiness: `blocked`

## Summary

| Metric | Value |
| --- | ---: |
| Market-data dates | 23 |
| Liquidity include rows | 4034 |
| Liquidity full-lookback rows | 10236 |
| Signal rows | 120 |
| Signal dates | 3 |
| BUY candidates | 60 |
| SELL candidates | 60 |
| Forward-return rows | 240 |
| Forward-return complete rows | 80 |
| Forward-return horizons | 1,5 |
| Portfolio target rows | 60 |
| Portfolio target dates | 3 |
| Portfolio max gross target weight | 1.0000 |

## Gates

| Gate | Status | Evidence | Next action |
| --- | --- | --- | --- |
| `market_data_window` | `pass` | 23 market-data dates available; minimum configured gate is 20 | keep extending for production strategy lookbacks |
| `liquidity_filter` | `pass_smoke` | 4034 include rows; 10236 rows evaluated with at least 20-day lookback | keep 20-day Liquidity Filter aligned with expanded status/date windows |
| `signal_candidates` | `pass_smoke` | 120 candidates across 3 dates; BUY=60, SELL=60 | keep candidates paper-only until Backtest/OOS/Bias Control pass |
| `forward_return_smoke` | `pass_smoke` | 80/240 forward-return rows complete across horizons 1,5 | extend market-data window so forward-return coverage reaches production horizons |
| `portfolio_targets_smoke` | `pass_smoke` | 60 target rows across 3 dates; order-intent rows=0 | keep target weights diagnostic-only until Backtest cost/benchmark/OOS gates are wired |
| `point_in_time_status_coverage` | `hold` | status coverage mode is current_snapshot_smoke | replace current-snapshot smoke with historical status-event coverage by rebalance date |
| `backtest_engine` | `hold` | Backtest engine is not wired to Point-in-Time Universe, costs, benchmark, OOS, and Bias Control | build Backtest only after Point-in-Time status coverage is acceptable for the selected scope |
| `live_trading_controls` | `blocked` | no order executor, kill switch, explicit confirmation gate, status/cancel flow, or read-only account checks are complete | finish demo read-only account gates before any order executor |
| `kis_demo_account` | `blocked` | local demo account preflight reports KIS_PAPER_STOCK missing or invalid | fill KIS_PAPER_STOCK locally and rerun account preflight |

## Guardrails

- Passing smoke gates does not make the strategy Backtest-ready.
- Do not create KIS order intents from Signal Candidate rows.
- Keep raw credentials and account values out of tracked reports.
