# KRX OpenAPI Continuity Audit

- Source normalized dir: [[_report/raw/2026/2026-07-08/krx/openapi-normalized/20250224-20250307|_report/raw/2026/2026-07-08/krx/openapi-normalized/20250224-20250307]]
- Interpretation: normalized row-count continuity audit, not a `Point-in-Time Universe` or `Backtest` result
- Bias Control judgment: `hold`

## Summary

| Metric | Value |
| --- | ---: |
| Audited dates | 10 |
| Row-count alerts | 2 |
| Duplicate date/code keys | 0 |
| Stock/issue code mismatches | 2752 |

## Row Output

- [[_report/quant/research/2026-07-08-krx-openapi-continuity-audit-20250224-20250307.rows.csv|_report/quant/research/2026-07-08-krx-openapi-continuity-audit-20250224-20250307.rows.csv]]

## Date Rows

| Date | Stock Rows | Issue Rows | Index Rows | Stock Delta | Issue Delta | Alert | Missing Pair Count |
| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: |
| `2025-02-24` | 2751 | 2751 | 91 | - | - | `false` | 0 |
| `2025-02-25` | 2752 | 2752 | 91 | 1 | 1 | `false` | 0 |
| `2025-02-26` | 2752 | 2752 | 91 | 0 | 0 | `false` | 0 |
| `2025-02-27` | 2752 | 2752 | 91 | 0 | 0 | `false` | 0 |
| `2025-02-28` | 2752 | 2752 | 91 | 0 | 0 | `false` | 0 |
| `2025-03-03` | 0 | 2752 | 0 | -2752 | 0 | `true` | 2752 |
| `2025-03-04` | 2752 | 2752 | 91 | 2752 | 0 | `true` | 0 |
| `2025-03-05` | 2752 | 2752 | 91 | 0 | 0 | `false` | 0 |
| `2025-03-06` | 2753 | 2753 | 91 | 1 | 1 | `false` | 0 |
| `2025-03-07` | 2753 | 2753 | 91 | 0 | 0 | `false` | 0 |

## Guardrails

- Small row-count deltas can be legitimate listing or delisting changes, but they still require event-source validation before Backtest use.
- Zero duplicate keys and zero stock/issue mismatches only validate normalized table consistency for this window.
- Backtest readiness remains `hold` until `Point-in-Time` status replay and broader historical coverage are validated.
