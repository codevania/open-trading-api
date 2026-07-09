# Point-in-Time Status Events Validation

- Events: [[_report/quant/data/point_in_time_status_events/2026-07-09-kind-current-status-events.csv|_report/quant/data/point_in_time_status_events/2026-07-09-kind-current-status-events.csv]]
- Schema: [[_report/quant/data/schemas/point_in_time_status_events.schema.json|_report/quant/data/schemas/point_in_time_status_events.schema.json]]
- Source policy: [[_report/quant/data/point_in_time_status_sources.yaml|_report/quant/data/point_in_time_status_sources.yaml]]
- Interpretation: schema validation only, not a `Point-in-Time Universe` or `Backtest` result
- Backtest readiness: `hold`

## Summary

| Metric | Value |
| --- | ---: |
| Input rows | 317 |
| Valid rows | 317 |
| Invalid rows | 0 |
| Duplicate event keys | 0 |

## Row Output

- [[_report/quant/research/2026-07-09-kind-status-events-validation.rows.csv|_report/quant/research/2026-07-09-kind-status-events-validation.rows.csv]]

## Status Type Counts

| Status Type | Rows |
| --- | ---: |
| `delisting` | 63 |
| `managed_issue` | 104 |
| `market_alert` | 25 |
| `trading_halt` | 125 |

## Source Counts

| Source | Rows |
| --- | ---: |
| `kind` | 317 |

## Guardrails

- Passing validation means normalized status-event rows match local schema/config only.
- It does not prove raw KRX/KIND collection coverage.
- Raw evidence must remain under `_report/raw/**` and stay out of commits.
- `Backtest` readiness remains `hold` until historical status replay is validated for the selected test scope.
