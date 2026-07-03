# Point-in-Time Universe Smoke

- Replayed market-data input: [[_report/quant/research/2026-07-03-kind-status-replay-on-openapi-20250102-20250124.rows.csv|_report/quant/research/2026-07-03-kind-status-replay-on-openapi-20250102-20250124.rows.csv]]
- Output: [[_report/quant/research/2026-07-03-kind-status-point-in-time-universe-smoke-20250102-20250124.rows.csv|_report/quant/research/2026-07-03-kind-status-point-in-time-universe-smoke-20250102-20250124.rows.csv]]
- Mode: `status_replay_smoke`
- Interpretation: Universe eligibility smoke only, not a full historical Backtest input
- Backtest readiness: `hold`

## Summary

| Metric | Value |
| --- | ---: |
| Input rows | 46659 |
| Output rows | 46659 |
| Dates | 17 |
| Include rows | 43553 |
| Exclude rows | 3106 |

## Exclusion Reason Counts

| Reason | Rows |
| --- | ---: |
| `security_group_not_plain_equity` | 854 |
| `status_event:managed_issue_active` | 280 |
| `stock_certificate_not_common` | 1972 |

## Date Counts

| Date | Include | Exclude |
| --- | ---: | ---: |
| `2025-01-02` | 2562 | 183 |
| `2025-01-03` | 2562 | 183 |
| `2025-01-06` | 2562 | 183 |
| `2025-01-07` | 2562 | 183 |
| `2025-01-08` | 2562 | 182 |
| `2025-01-09` | 2562 | 182 |
| `2025-01-10` | 2562 | 182 |
| `2025-01-13` | 2562 | 182 |
| `2025-01-14` | 2562 | 182 |
| `2025-01-15` | 2561 | 183 |
| `2025-01-16` | 2561 | 183 |
| `2025-01-17` | 2561 | 183 |
| `2025-01-20` | 2561 | 183 |
| `2025-01-21` | 2561 | 183 |
| `2025-01-22` | 2561 | 183 |
| `2025-01-23` | 2563 | 183 |
| `2025-01-24` | 2566 | 183 |

## Guardrails

- This consumes supplied status replay rows; it does not prove status-source completeness.
- `include` means the row passed the local instrument/status filters in this smoke input.
- Do not treat this as Backtest-ready until historical status coverage, Liquidity Filter, and strategy/OOS gates are complete.
