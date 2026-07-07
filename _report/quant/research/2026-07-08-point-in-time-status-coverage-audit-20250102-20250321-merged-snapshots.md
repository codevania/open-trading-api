# Point-in-Time Status Coverage Audit

- Market data: [[_report/raw/2026/2026-07-08/krx/openapi-market-data/20250102-20250321/market_data.csv|_report/raw/2026/2026-07-08/krx/openapi-market-data/20250102-20250321/market_data.csv]]
- Status events: [[_report/quant/data/point_in_time_status_events/2026-07-08-kind-current-status-events.merged-20260703-20260708.csv|_report/quant/data/point_in_time_status_events/2026-07-08-kind-current-status-events.merged-20260703-20260708.csv]]
- Replayed market-data: [[_report/quant/research/2026-07-08-kind-status-replay-on-openapi-20250102-20250321-merged-snapshots.rows.csv|_report/quant/research/2026-07-08-kind-status-replay-on-openapi-20250102-20250321-merged-snapshots.rows.csv]]
- Output: [[_report/quant/research/2026-07-08-point-in-time-status-coverage-audit-20250102-20250321-merged-snapshots.rows.csv|_report/quant/research/2026-07-08-point-in-time-status-coverage-audit-20250102-20250321-merged-snapshots.rows.csv]]
- Coverage mode: `current_snapshot_smoke`
- Coverage status: `hold`
- KIS/KRX API call: `false`
- Order intent generated: `false`
- Interpretation: status coverage audit only, not a `Backtest` result

## Summary

| Metric | Value |
| --- | ---: |
| Market rows | 142990 |
| Market dates | 52 |
| Market codes | 2772 |
| Market window | `2025-01-02..2025-03-21` |
| Status event rows | 497 |
| Status event codes | 286 |
| Event date window | `2022-03-24..2026-07-08` |
| Raw status source paths | 14 |
| Raw status capture dates | 2 |
| Raw status capture date window | `2026-07-03..2026-07-08` |
| Release/resume-like event rows | 0 |
| Replayed rows | 142990 |
| Replay matched market rows | 142990 |
| Replay missing market rows | 0 |
| Rows with any status-event code | 13220 |
| Rows with applied status event | 889 |
| Rows excluded by status event | 889 |

## Status Type Counts

| Status type | Rows |
| --- | ---: |
| `delisting` | 64 |
| `managed_issue` | 105 |
| `market_alert` | 75 |
| `trading_halt` | 253 |

## Status Value Counts

| Status value | Rows |
| --- | ---: |
| `caution` | 55 |
| `delisted` | 64 |
| `designated` | 105 |
| `halted` | 253 |
| `risk` | 1 |
| `warning` | 19 |

## Lifecycle Diagnostics

| Status type | Active-like rows | Release/resume-like rows |
| --- | ---: | ---: |
| `managed_issue` | 105 | 0 |
| `market_alert` | 75 | 0 |
| `trading_halt` | 253 | 0 |

## Source Counts

| Source | Rows |
| --- | ---: |
| `kind` | 497 |

## Hold Reasons

- coverage mode is not `historical_complete`
- no release/resume-like events are present, so active-state lifetimes are one-sided
- status types with active-like events but no release/resume rows: `managed_issue,market_alert,trading_halt`

## Guardrails

- Event-code ratios are diagnostic; a stock with no status event is not automatically a data gap.
- Current snapshot events can exclude active issues, but they do not prove historical state transitions.
- Keep `Backtest readiness` at `hold` until source coverage is reproducible for every rebalance date.
