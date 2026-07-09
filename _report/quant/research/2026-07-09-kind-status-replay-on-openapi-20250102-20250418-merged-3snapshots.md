# Point-in-Time Status Replay Scaffold

- Market data: [[_report/raw/2026/2026-07-08/krx/openapi-market-data/20250102-20250418/market_data.csv|_report/raw/2026/2026-07-08/krx/openapi-market-data/20250102-20250418/market_data.csv]]
- Status events: [[_report/quant/data/point_in_time_status_events/2026-07-09-kind-current-status-events.merged-20260703-20260708-20260709.market-enriched-81d.csv|_report/quant/data/point_in_time_status_events/2026-07-09-kind-current-status-events.merged-20260703-20260708-20260709.market-enriched-81d.csv]]
- Output: [[_report/quant/data/point_in_time_status_events/2026-07-09-kind-status-replay-on-openapi-20250102-20250418-merged-3snapshots.rows.csv|_report/quant/data/point_in_time_status_events/2026-07-09-kind-status-replay-on-openapi-20250102-20250418-merged-3snapshots.rows.csv]]
- Interpretation: event-row replay scaffold only, not full historical status coverage
- Backtest readiness: `hold`

## Summary

| Metric | Value |
| --- | ---: |
| Input market rows | 198137 |
| Status event rows | 634 |
| Dates | 72 |
| Codes with events | 296 |
| Include rows by event state | 196491 |
| Exclude rows by event state | 1646 |

## Guardrails

- `include_by_status_event` means no active exclusion in the provided event rows; it does not prove complete official status coverage.
- Use this only after event rows pass [[scripts/quant_point_in_time_status_events_validate.py|scripts/quant_point_in_time_status_events_validate.py]].
- `Backtest` remains `hold` until historical status coverage is validated for the selected scope.
