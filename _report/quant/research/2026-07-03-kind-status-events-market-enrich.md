# Point-in-Time Status Events Market Enrichment

- Events input: [[_report/quant/data/point_in_time_status_events/2026-07-03-kind-current-status-events.csv|_report/quant/data/point_in_time_status_events/2026-07-03-kind-current-status-events.csv]]
- Market-data input: [[_report/raw/2026/2026-07-03/krx/openapi-market-data/20250102-20250124/market_data.csv|_report/raw/2026/2026-07-03/krx/openapi-market-data/20250102-20250124/market_data.csv]]
- Output: [[_report/quant/data/point_in_time_status_events/2026-07-03-kind-current-status-events.market-enriched.csv|_report/quant/data/point_in_time_status_events/2026-07-03-kind-current-status-events.market-enriched.csv]]
- Interpretation: local market-label enrichment only, not additional status coverage
- Backtest readiness: `hold`

## Summary

| Metric | Value |
| --- | ---: |
| Input event rows | 344 |
| Output event rows | 344 |
| Market-data rows | 46659 |
| Mapped codes | 2751 |
| Resolved UNKNOWN market rows | 310 |
| Retained matching market rows | 0 |
| Retained source-market conflicts | 0 |
| Ambiguous market mappings | 0 |
| Unresolved no market mapping | 34 |

## Guardrails

- This only fills market labels when the provided market-data join has deterministic code-to-market evidence.
- Unresolved rows remain `UNKNOWN` and must not be interpreted as excluded or included by market.
- `Backtest` remains `hold` until historical status coverage is validated for the selected scope.
