# Point-in-Time Status Coverage Audit

- Market data: [[_report/raw/2026/2026-07-08/krx/openapi-market-data/20250102-20250307/market_data.csv|_report/raw/2026/2026-07-08/krx/openapi-market-data/20250102-20250307/market_data.csv]]
- Status events: [[_report/quant/data/point_in_time_status_events/2026-07-08-kind-current-status-events.market-enriched-42d.csv|_report/quant/data/point_in_time_status_events/2026-07-08-kind-current-status-events.market-enriched-42d.csv]]
- Replayed market-data: [[_report/quant/research/2026-07-08-kind-status-replay-on-openapi-20250102-20250307-second-snapshot.rows.csv|_report/quant/research/2026-07-08-kind-status-replay-on-openapi-20250102-20250307-second-snapshot.rows.csv]]
- Output: [[_report/quant/research/2026-07-08-point-in-time-status-coverage-audit-20250102-20250307-second-snapshot.rows.csv|_report/quant/research/2026-07-08-point-in-time-status-coverage-audit-20250102-20250307-second-snapshot.rows.csv]]
- Coverage mode: `current_snapshot_smoke`
- Coverage status: `hold`
- KIS/KRX API call: `false`
- Order intent generated: `false`
- Interpretation: status coverage audit only, not a `Backtest` result

## Summary

| Metric | Value |
| --- | ---: |
| Market rows | 115447 |
| Market dates | 42 |
| Market codes | 2766 |
| Market window | `2025-01-02..2025-03-07` |
| Status event rows | 327 |
| Status event codes | 250 |
| Event date window | `2022-03-24..2026-07-08` |
| Raw status source paths | 6 |
| Raw status capture dates | 1 |
| Raw status capture date window | `2026-07-08..2026-07-08` |
| Release/resume-like event rows | 0 |
| Replayed rows | 115447 |
| Replay matched market rows | 115447 |
| Replay missing market rows | 0 |
| Rows with any status-event code | 9242 |
| Rows with applied status event | 663 |
| Rows excluded by status event | 663 |

## Status Type Counts

| Status type | Rows |
| --- | ---: |
| `delisting` | 63 |
| `managed_issue` | 102 |
| `market_alert` | 35 |
| `trading_halt` | 127 |

## Status Value Counts

| Status value | Rows |
| --- | ---: |
| `caution` | 20 |
| `delisted` | 63 |
| `designated` | 102 |
| `halted` | 127 |
| `risk` | 1 |
| `warning` | 14 |

## Lifecycle Diagnostics

| Status type | Active-like rows | Release/resume-like rows |
| --- | ---: | ---: |
| `managed_issue` | 102 | 0 |
| `market_alert` | 35 | 0 |
| `trading_halt` | 127 | 0 |

## Source Counts

| Source | Rows |
| --- | ---: |
| `kind` | 327 |

## Hold Reasons

- coverage mode is not `historical_complete`
- no release/resume-like events are present, so active-state lifetimes are one-sided
- status types with active-like events but no release/resume rows: `managed_issue,market_alert,trading_halt`
- status events currently map to a single raw capture date: `2026-07-08`

## Guardrails

- Event-code ratios are diagnostic; a stock with no status event is not automatically a data gap.
- Current snapshot events can exclude active issues, but they do not prove historical state transitions.
- Keep `Backtest readiness` at `hold` until source coverage is reproducible for every rebalance date.
