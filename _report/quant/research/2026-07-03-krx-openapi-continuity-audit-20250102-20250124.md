# KRX OpenAPI Continuity Audit

- Source normalized dir: [[_report/raw/2026/2026-07-03/krx/openapi-normalized/20250102-20250124|_report/raw/2026/2026-07-03/krx/openapi-normalized/20250102-20250124]]
- Interpretation: normalized row-count continuity audit, not a `Point-in-Time Universe` or `Backtest` result
- Bias Control judgment: `hold`

## Summary

| Metric | Value |
| --- | ---: |
| Audited dates | 17 |
| Row-count alerts | 0 |
| Duplicate date/code keys | 0 |
| Stock/issue code mismatches | 0 |

## Row Output

- [[_report/quant/research/2026-07-03-krx-openapi-continuity-audit-20250102-20250124.rows.csv|_report/quant/research/2026-07-03-krx-openapi-continuity-audit-20250102-20250124.rows.csv]]

## Date Rows

| Date | Stock Rows | Issue Rows | Index Rows | Stock Delta | Issue Delta | Alert | Missing Pair Count |
| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: |
| `2025-01-02` | 2745 | 2745 | 91 | - | - | `false` | 0 |
| `2025-01-03` | 2745 | 2745 | 91 | 0 | 0 | `false` | 0 |
| `2025-01-06` | 2745 | 2745 | 91 | 0 | 0 | `false` | 0 |
| `2025-01-07` | 2745 | 2745 | 91 | 0 | 0 | `false` | 0 |
| `2025-01-08` | 2744 | 2744 | 91 | -1 | -1 | `false` | 0 |
| `2025-01-09` | 2744 | 2744 | 91 | 0 | 0 | `false` | 0 |
| `2025-01-10` | 2744 | 2744 | 91 | 0 | 0 | `false` | 0 |
| `2025-01-13` | 2744 | 2744 | 91 | 0 | 0 | `false` | 0 |
| `2025-01-14` | 2744 | 2744 | 91 | 0 | 0 | `false` | 0 |
| `2025-01-15` | 2744 | 2744 | 91 | 0 | 0 | `false` | 0 |
| `2025-01-16` | 2744 | 2744 | 91 | 0 | 0 | `false` | 0 |
| `2025-01-17` | 2744 | 2744 | 91 | 0 | 0 | `false` | 0 |
| `2025-01-20` | 2744 | 2744 | 91 | 0 | 0 | `false` | 0 |
| `2025-01-21` | 2744 | 2744 | 91 | 0 | 0 | `false` | 0 |
| `2025-01-22` | 2744 | 2744 | 91 | 0 | 0 | `false` | 0 |
| `2025-01-23` | 2746 | 2746 | 91 | 2 | 2 | `false` | 0 |
| `2025-01-24` | 2749 | 2749 | 91 | 3 | 3 | `false` | 0 |

## Guardrails

- Small row-count deltas can be legitimate listing or delisting changes, but they still require event-source validation before Backtest use.
- Zero duplicate keys and zero stock/issue mismatches only validate normalized table consistency for this window.
- Backtest readiness remains `hold` until `Point-in-Time` status replay and broader historical coverage are validated.
