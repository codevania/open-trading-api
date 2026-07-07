# Point-in-Time Status Replay Scaffold

- Market data: [[_report/raw/2026/2026-07-06/krx/openapi-market-data/20250102-20250221/market_data.csv|_report/raw/2026/2026-07-06/krx/openapi-market-data/20250102-20250221/market_data.csv]]
- Status events: [[_report/quant/data/point_in_time_status_events/2026-07-03-kind-current-status-events.market-enriched.csv|_report/quant/data/point_in_time_status_events/2026-07-03-kind-current-status-events.market-enriched.csv]]
- Output: [[_report/quant/research/2026-07-06-kind-status-replay-on-openapi-20250102-20250221.rows.csv|_report/quant/research/2026-07-06-kind-status-replay-on-openapi-20250102-20250221.rows.csv]]
- Interpretation: event-row replay scaffold only, not full historical status coverage
- Backtest readiness: `hold`

## Summary

| Metric | Value |
| --- | ---: |
| Input market rows | 90678 |
| Status event rows | 344 |
| Dates | 33 |
| Codes with events | 265 |
| Include rows by event state | 90126 |
| Exclude rows by event state | 552 |

## Guardrails

- `include_by_status_event` means no active exclusion in the provided event rows; it does not prove complete official status coverage.
- Use this only after event rows pass [[scripts/quant_point_in_time_status_events_validate.py|scripts/quant_point_in_time_status_events_validate.py]].
- `Backtest` remains `hold` until historical status coverage is validated for the selected scope.
