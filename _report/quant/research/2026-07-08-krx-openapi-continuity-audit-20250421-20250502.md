# KRX OpenAPI Continuity Audit

- Source normalized dir: [[_report/raw/2026/2026-07-08/krx/openapi-normalized/20250421-20250502|_report/raw/2026/2026-07-08/krx/openapi-normalized/20250421-20250502]]
- Interpretation: normalized row-count continuity audit, not a `Point-in-Time Universe` or `Backtest` result
- Bias Control judgment: `hold`

## Summary

| Metric | Value |
| --- | ---: |
| Audited dates | 10 |
| Row-count alerts | 2 |
| Duplicate date/code keys | 0 |
| Stock/issue code mismatches | 2758 |

## Row Output

- [[_report/quant/research/2026-07-08-krx-openapi-continuity-audit-20250421-20250502.rows.csv|_report/quant/research/2026-07-08-krx-openapi-continuity-audit-20250421-20250502.rows.csv]]

## Date Rows

| Date | Stock Rows | Issue Rows | Index Rows | Stock Delta | Issue Delta | Alert | Missing Pair Count |
| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: |
| `2025-04-21` | 2757 | 2757 | 91 | - | - | `false` | 0 |
| `2025-04-22` | 2757 | 2757 | 91 | 0 | 0 | `false` | 0 |
| `2025-04-23` | 2757 | 2757 | 91 | 0 | 0 | `false` | 0 |
| `2025-04-24` | 2757 | 2757 | 91 | 0 | 0 | `false` | 0 |
| `2025-04-25` | 2757 | 2757 | 91 | 0 | 0 | `false` | 0 |
| `2025-04-28` | 2758 | 2758 | 91 | 1 | 1 | `false` | 0 |
| `2025-04-29` | 2758 | 2758 | 91 | 0 | 0 | `false` | 0 |
| `2025-04-30` | 2758 | 2758 | 91 | 0 | 0 | `false` | 0 |
| `2025-05-01` | 0 | 2758 | 0 | -2758 | 0 | `true` | 2758 |
| `2025-05-02` | 2758 | 2758 | 91 | 2758 | 0 | `true` | 0 |

## Guardrails

- Small row-count deltas can be legitimate listing or delisting changes, but they still require event-source validation before Backtest use.
- Zero duplicate keys and zero stock/issue mismatches only validate normalized table consistency for this window.
- Backtest readiness remains `hold` until `Point-in-Time` status replay and broader historical coverage are validated.
