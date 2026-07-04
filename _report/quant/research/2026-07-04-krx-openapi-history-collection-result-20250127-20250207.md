# KRX OpenAPI Historical Collection Plan

- Plan type: `krx_openapi_history_missing_raw`
- Date range: `20250127` to `20250207`
- Capture date: `2026-07-04`
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

- [[_report/quant/research/2026-07-04-krx-openapi-history-collection-result-20250127-20250207.requests.json|_report/quant/research/2026-07-04-krx-openapi-history-collection-result-20250127-20250207.requests.json]]

## Date Plan

| bas_dd | Weekday | Complete | Missing services |
| --- | --- | --- | --- |
| `20250127` | Monday | `true` | - |
| `20250128` | Tuesday | `true` | - |
| `20250129` | Wednesday | `true` | - |
| `20250130` | Thursday | `true` | - |
| `20250131` | Friday | `true` | - |
| `20250203` | Monday | `true` | - |
| `20250204` | Tuesday | `true` | - |
| `20250205` | Wednesday | `true` | - |
| `20250206` | Thursday | `true` | - |
| `20250207` | Friday | `true` | - |

## Guardrails

- Weekend filtering is not a KRX trading-calendar guarantee; holidays can still produce zero-row raws.
- The collector should still save raw responses and metadata for every attempted date.
- Backtest readiness remains `hold` until `Point-in-Time` status replay and historical coverage are validated.
