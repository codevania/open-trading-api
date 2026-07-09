# Point-in-Time Status Coverage Audit

- Market data: [[_report/raw/2026/2026-07-08/krx/openapi-market-data/20250102-20250418/market_data.csv|_report/raw/2026/2026-07-08/krx/openapi-market-data/20250102-20250418/market_data.csv]]
- Status events: [[_report/quant/data/point_in_time_status_events/2026-07-09-kind-current-status-events.merged-20260703-20260708-20260709.market-enriched-81d.csv|_report/quant/data/point_in_time_status_events/2026-07-09-kind-current-status-events.merged-20260703-20260708-20260709.market-enriched-81d.csv]]
- Replayed market-data: [[_report/quant/data/point_in_time_status_events/2026-07-09-kind-status-replay-on-openapi-20250102-20250418-merged-3snapshots.rows.csv|_report/quant/data/point_in_time_status_events/2026-07-09-kind-status-replay-on-openapi-20250102-20250418-merged-3snapshots.rows.csv]]
- Source coverage manifest: `not_supplied`
- Source policy: [[_report/quant/data/point_in_time_status_sources.yaml|_report/quant/data/point_in_time_status_sources.yaml]]
- Output: [[_report/quant/research/2026-07-09-point-in-time-status-coverage-audit-20250102-20250418-merged-3snapshots-market-enriched-81d.rows.csv|_report/quant/research/2026-07-09-point-in-time-status-coverage-audit-20250102-20250418-merged-3snapshots-market-enriched-81d.rows.csv]]
- Coverage mode: `current_snapshot_smoke`
- Coverage status: `hold`
- KIS/KRX API call: `false`
- Order intent generated: `false`
- Interpretation: status coverage audit only, not a `Backtest` result

## Summary

| Metric | Value |
| --- | ---: |
| Market rows | 198137 |
| Market dates | 72 |
| Market codes | 2776 |
| Market window | `2025-01-02..2025-04-18` |
| Status event rows | 634 |
| Status event codes | 296 |
| Event date window | `2022-03-24..2026-07-09` |
| Raw status source paths | 17 |
| Raw status capture dates | 3 |
| Raw status capture date window | `2026-07-03..2026-07-09` |
| Release/resume-like event rows | 0 |
| Replayed rows | 198137 |
| Replay matched market rows | 198137 |
| Replay missing market rows | 0 |
| Source coverage manifest rows | 0 |
| Source coverage manifest row failures | 0 |
| Source coverage manifest validation | `not_supplied` |
| Source coverage missing status types | `managed_issue,trading_halt,market_alert,delisting` |
| Rows with any status-event code | 19040 |
| Rows with applied status event | 1646 |
| Rows excluded by status event | 1646 |

## Status Type Counts

| Status type | Rows |
| --- | ---: |
| `delisting` | 64 |
| `managed_issue` | 107 |
| `market_alert` | 85 |
| `trading_halt` | 378 |

## Status Value Counts

| Status value | Rows |
| --- | ---: |
| `caution` | 65 |
| `delisted` | 64 |
| `designated` | 107 |
| `halted` | 378 |
| `risk` | 1 |
| `warning` | 19 |

## Lifecycle Diagnostics

| Status type | Active-like rows | Release/resume-like rows |
| --- | ---: | ---: |
| `managed_issue` | 107 | 0 |
| `market_alert` | 85 | 0 |
| `trading_halt` | 378 | 0 |

## Source Counts

| Source | Rows |
| --- | ---: |
| `kind` | 634 |

## Hold Reasons

- coverage mode is not `historical_complete`
- no release/resume-like events are present, so active-state lifetimes are one-sided
- status types with active-like events but no release/resume rows: `managed_issue,market_alert,trading_halt`
- source coverage manifest was not supplied

## Guardrails

- Event-code ratios are diagnostic; a stock with no status event is not automatically a data gap.
- Current snapshot events can exclude active issues, but they do not prove historical state transitions.
- `historical_complete` also requires a source coverage manifest that passes source-policy/raw-path validation and covers the market-data window for every required status type.
- Keep `Backtest readiness` at `hold` until source coverage is reproducible for every rebalance date.
