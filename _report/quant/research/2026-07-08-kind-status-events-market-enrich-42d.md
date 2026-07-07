# Point-in-Time Status Events Market Enrichment

- Events input: [[_report/quant/data/point_in_time_status_events/2026-07-08-kind-current-status-events.csv|_report/quant/data/point_in_time_status_events/2026-07-08-kind-current-status-events.csv]]
- Market-data input: [[_report/raw/2026/2026-07-08/krx/openapi-market-data/20250102-20250307/market_data.csv|_report/raw/2026/2026-07-08/krx/openapi-market-data/20250102-20250307/market_data.csv]]
- Output: [[_report/quant/data/point_in_time_status_events/2026-07-08-kind-current-status-events.market-enriched-42d.csv|_report/quant/data/point_in_time_status_events/2026-07-08-kind-current-status-events.market-enriched-42d.csv]]
- Interpretation: local market-label enrichment only, not additional status coverage
- Backtest readiness: `hold`

## Summary

| Metric | Value |
| --- | ---: |
| Input event rows | 327 |
| Output event rows | 327 |
| Market-data rows | 115447 |
| Mapped codes | 2766 |
| Resolved UNKNOWN market rows | 297 |
| Retained matching market rows | 0 |
| Retained source-market conflicts | 0 |
| Ambiguous market mappings | 0 |
| Unresolved no market mapping | 30 |

## Guardrails

- This only fills market labels when the provided market-data join has deterministic code-to-market evidence.
- Unresolved rows remain `UNKNOWN` and must not be interpreted as excluded or included by market.
- `Backtest` remains `hold` until historical status coverage is validated for the selected scope.
