# KRX OpenAPI Historical Collection Plan

- Plan type: `krx_openapi_history_missing_raw`
- Date range: `20250102` to `20250110`
- Capture date: `2026-07-03`
- Include weekends: `false`
- Interpretation: local missing-raw plan only, not a `Point-in-Time Universe` or `Backtest` result

## Totals

| Metric | Value |
| --- | ---: |
| Candidate dates | 7 |
| Complete dates | 7 |
| Existing raw files | 42 |
| Missing requests | 0 |

## JSON Plan

- [[_report/quant/research/2026-07-03-krx-openapi-history-collection-result-20250102-20250110.requests.json|_report/quant/research/2026-07-03-krx-openapi-history-collection-result-20250102-20250110.requests.json]]

## Date Plan

| bas_dd | Weekday | Complete | Missing services |
| --- | --- | --- | --- |
| `20250102` | Thursday | `true` | - |
| `20250103` | Friday | `true` | - |
| `20250106` | Monday | `true` | - |
| `20250107` | Tuesday | `true` | - |
| `20250108` | Wednesday | `true` | - |
| `20250109` | Thursday | `true` | - |
| `20250110` | Friday | `true` | - |

## Guardrails

- Weekend filtering is not a KRX trading-calendar guarantee; holidays can still produce zero-row raws.
- The collector should still save raw responses and metadata for every attempted date.
- Backtest readiness remains `hold` until `Point-in-Time` status replay and historical coverage are validated.
