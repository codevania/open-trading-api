# Point-in-Time Status Replay Scaffold

- Market data: [[_report/raw/2026/2026-07-08/krx/openapi-market-data/20250102-20250321/market_data.csv|_report/raw/2026/2026-07-08/krx/openapi-market-data/20250102-20250321/market_data.csv]]
- Status events: [[_report/quant/data/point_in_time_status_events/2026-07-08-kind-current-status-events.merged-20260703-20260708.csv|_report/quant/data/point_in_time_status_events/2026-07-08-kind-current-status-events.merged-20260703-20260708.csv]]
- Output: [[_report/quant/research/2026-07-08-kind-status-replay-on-openapi-20250102-20250321-merged-snapshots.rows.csv|_report/quant/research/2026-07-08-kind-status-replay-on-openapi-20250102-20250321-merged-snapshots.rows.csv]]
- Interpretation: event-row replay scaffold only, not full historical status coverage
- Backtest readiness: `hold`

## Summary

| Metric | Value |
| --- | ---: |
| Input market rows | 142990 |
| Status event rows | 497 |
| Dates | 52 |
| Codes with events | 286 |
| Include rows by event state | 142101 |
| Exclude rows by event state | 889 |

## Guardrails

- `include_by_status_event` means no active exclusion in the provided event rows; it does not prove complete official status coverage.
- Use this only after event rows pass [[scripts/quant_point_in_time_status_events_validate.py|scripts/quant_point_in_time_status_events_validate.py]].
- `Backtest` remains `hold` until historical status coverage is validated for the selected scope.
