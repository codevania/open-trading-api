# KRX OpenAPI Continuity Audit

- Source normalized dir: [[_report/quant/data/krx_openapi/normalized/20250407-20250418|_report/quant/data/krx_openapi/normalized/20250407-20250418]]
- Interpretation: normalized row-count continuity audit, not a `Point-in-Time Universe` or `Backtest` result
- Bias Control judgment: `hold`

## Summary

| Metric | Value |
| --- | ---: |
| Audited dates | 10 |
| Row-count alerts | 0 |
| Duplicate date/code keys | 0 |
| Stock/issue code mismatches | 0 |

## Row Output

- [[_report/quant/research/2026-07-08-krx-openapi-continuity-audit-20250407-20250418.rows.csv|_report/quant/research/2026-07-08-krx-openapi-continuity-audit-20250407-20250418.rows.csv]]

## Date Rows

| Date | Stock Rows | Issue Rows | Index Rows | Stock Delta | Issue Delta | Alert | Missing Pair Count |
| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: |
| `2025-04-07` | 2757 | 2757 | 91 | - | - | `false` | 0 |
| `2025-04-08` | 2757 | 2757 | 91 | 0 | 0 | `false` | 0 |
| `2025-04-09` | 2757 | 2757 | 91 | 0 | 0 | `false` | 0 |
| `2025-04-10` | 2757 | 2757 | 91 | 0 | 0 | `false` | 0 |
| `2025-04-11` | 2757 | 2757 | 91 | 0 | 0 | `false` | 0 |
| `2025-04-14` | 2757 | 2757 | 91 | 0 | 0 | `false` | 0 |
| `2025-04-15` | 2757 | 2757 | 91 | 0 | 0 | `false` | 0 |
| `2025-04-16` | 2757 | 2757 | 91 | 0 | 0 | `false` | 0 |
| `2025-04-17` | 2757 | 2757 | 91 | 0 | 0 | `false` | 0 |
| `2025-04-18` | 2757 | 2757 | 91 | 0 | 0 | `false` | 0 |

## Guardrails

- Small row-count deltas can be legitimate listing or delisting changes, but they still require event-source validation before Backtest use.
- Zero duplicate keys and zero stock/issue mismatches only validate normalized table consistency for this window.
- Backtest readiness remains `hold` until `Point-in-Time` status replay and broader historical coverage are validated.
