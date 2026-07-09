# Point-in-Time Status Unknown Market Targets

- Events: [[_report/quant/data/point_in_time_status_events/2026-07-09-kind-current-status-events.merged-20260703-20260708-20260709.market-enriched-81d.csv|_report/quant/data/point_in_time_status_events/2026-07-09-kind-current-status-events.merged-20260703-20260708-20260709.market-enriched-81d.csv]]
- Output: [[_report/quant/research/2026-07-09-kind-status-events-unknown-market-targets-merged-3snapshots-market-enriched-81d.rows.csv|_report/quant/research/2026-07-09-kind-status-events-unknown-market-targets-merged-3snapshots-market-enriched-81d.rows.csv]]
- KIS/KRX API call: `false`
- Order intent generated: `false`
- Backtest readiness impact: `none`
- Interpretation: market-label collection targets only, not status transition evidence

## Summary

| Metric | Value |
| --- | ---: |
| Event rows | 634 |
| Unknown market rows | 61 |
| Unknown market codes | 31 |
| Raw capture dates | 3 |
| Raw capture date window | `2026-07-03..2026-07-09` |

## Status Type Counts

| Status type | Rows |
| --- | ---: |
| `delisting` | 9 |
| `managed_issue` | 6 |
| `market_alert` | 4 |
| `trading_halt` | 42 |

## Source Counts

| Source | Rows |
| --- | ---: |
| `kind` | 61 |

## Guardrails

- Resolving these rows may improve market labels, but it does not solve release/resume lifecycle coverage.
- Keep `Backtest readiness` at `hold` until historical status transition evidence and source coverage manifest validation pass.
- Do not infer market labels without official evidence or deterministic local market-data joins.
