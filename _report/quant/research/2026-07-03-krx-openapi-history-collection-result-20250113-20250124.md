# KRX OpenAPI Historical Collection Plan

- Plan type: `krx_openapi_history_missing_raw`
- Date range: `20250113` to `20250124`
- Capture date: `2026-07-03`
- Include weekends: `false`
- Interpretation: local missing-raw plan only, not a `Point-in-Time Universe` or `Backtest` result

## Totals

| Metric | Value |
| --- | ---: |
| Candidate dates | 10 |
| Complete dates | 10 |
| Existing raw files | 60 |
| Missing requests | 0 |

## JSON Plan

- [[_report/quant/research/2026-07-03-krx-openapi-history-collection-result-20250113-20250124.requests.json|_report/quant/research/2026-07-03-krx-openapi-history-collection-result-20250113-20250124.requests.json]]

## Date Plan

| bas_dd | Weekday | Complete | Missing services |
| --- | --- | --- | --- |
| `20250113` | Monday | `true` | - |
| `20250114` | Tuesday | `true` | - |
| `20250115` | Wednesday | `true` | - |
| `20250116` | Thursday | `true` | - |
| `20250117` | Friday | `true` | - |
| `20250120` | Monday | `true` | - |
| `20250121` | Tuesday | `true` | - |
| `20250122` | Wednesday | `true` | - |
| `20250123` | Thursday | `true` | - |
| `20250124` | Friday | `true` | - |

## Guardrails

- Weekend filtering is not a KRX trading-calendar guarantee; holidays can still produce zero-row raws.
- The collector should still save raw responses and metadata for every attempted date.
- Backtest readiness remains `hold` until `Point-in-Time` status replay and historical coverage are validated.
