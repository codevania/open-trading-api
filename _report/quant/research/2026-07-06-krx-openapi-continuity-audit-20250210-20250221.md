# KRX OpenAPI Continuity Audit

- Source normalized dir: [[_report/raw/2026/2026-07-06/krx/openapi-normalized/20250210-20250221|_report/raw/2026/2026-07-06/krx/openapi-normalized/20250210-20250221]]
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

- [[_report/quant/research/2026-07-06-krx-openapi-continuity-audit-20250210-20250221.rows.csv|_report/quant/research/2026-07-06-krx-openapi-continuity-audit-20250210-20250221.rows.csv]]

## Date Rows

| Date | Stock Rows | Issue Rows | Index Rows | Stock Delta | Issue Delta | Alert | Missing Pair Count |
| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: |
| `2025-02-10` | 2751 | 2751 | 91 | - | - | `false` | 0 |
| `2025-02-11` | 2750 | 2750 | 91 | -1 | -1 | `false` | 0 |
| `2025-02-12` | 2751 | 2751 | 91 | 1 | 1 | `false` | 0 |
| `2025-02-13` | 2752 | 2752 | 91 | 1 | 1 | `false` | 0 |
| `2025-02-14` | 2751 | 2751 | 91 | -1 | -1 | `false` | 0 |
| `2025-02-17` | 2752 | 2752 | 91 | 1 | 1 | `false` | 0 |
| `2025-02-18` | 2752 | 2752 | 91 | 0 | 0 | `false` | 0 |
| `2025-02-19` | 2751 | 2751 | 91 | -1 | -1 | `false` | 0 |
| `2025-02-20` | 2752 | 2752 | 91 | 1 | 1 | `false` | 0 |
| `2025-02-21` | 2751 | 2751 | 91 | -1 | -1 | `false` | 0 |

## Guardrails

- Small row-count deltas can be legitimate listing or delisting changes, but they still require event-source validation before Backtest use.
- Zero duplicate keys and zero stock/issue mismatches only validate normalized table consistency for this window.
- Backtest readiness remains `hold` until `Point-in-Time` status replay and broader historical coverage are validated.
