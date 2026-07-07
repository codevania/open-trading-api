# Point-in-Time Universe Smoke

- Replayed market-data input: [[_report/quant/research/2026-07-08-kind-status-replay-on-openapi-20250102-20250321-merged-snapshots.rows.csv|_report/quant/research/2026-07-08-kind-status-replay-on-openapi-20250102-20250321-merged-snapshots.rows.csv]]
- Output: [[_report/quant/research/2026-07-08-kind-status-point-in-time-universe-smoke-merged-snapshots-20250102-20250321.rows.csv|_report/quant/research/2026-07-08-kind-status-point-in-time-universe-smoke-merged-snapshots-20250102-20250321.rows.csv]]
- Mode: `status_replay_smoke`
- Interpretation: Universe eligibility smoke only, not a full historical Backtest input
- Backtest readiness: `hold`

## Summary

| Metric | Value |
| --- | ---: |
| Input rows | 142990 |
| Output rows | 142990 |
| Dates | 52 |
| Include rows | 133465 |
| Exclude rows | 9525 |

## Exclusion Reason Counts

| Reason | Rows |
| --- | ---: |
| `security_group_not_plain_equity` | 2604 |
| `status_event:managed_issue_active` | 889 |
| `stock_certificate_not_common` | 6032 |

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
| `2025-01-31` | 2566 | 183 |
| `2025-02-03` | 2567 | 183 |
| `2025-02-04` | 2568 | 183 |
| `2025-02-05` | 2569 | 183 |
| `2025-02-06` | 2569 | 183 |
| `2025-02-07` | 2569 | 183 |
| `2025-02-10` | 2568 | 183 |
| `2025-02-11` | 2567 | 183 |
| `2025-02-12` | 2568 | 183 |
| `2025-02-13` | 2569 | 183 |
| `2025-02-14` | 2568 | 183 |
| `2025-02-17` | 2569 | 183 |
| `2025-02-18` | 2569 | 183 |
| `2025-02-19` | 2568 | 183 |
| `2025-02-20` | 2569 | 183 |
| `2025-02-21` | 2568 | 183 |
| `2025-02-24` | 2568 | 183 |
| `2025-02-25` | 2569 | 183 |
| `2025-02-26` | 2569 | 183 |
| `2025-02-27` | 2569 | 183 |
| `2025-02-28` | 2569 | 183 |
| `2025-03-04` | 2569 | 183 |
| `2025-03-05` | 2569 | 183 |
| `2025-03-06` | 2570 | 183 |
| `2025-03-07` | 2570 | 183 |
| `2025-03-10` | 2570 | 183 |
| `2025-03-11` | 2570 | 183 |
| `2025-03-12` | 2570 | 183 |
| `2025-03-13` | 2570 | 183 |
| `2025-03-14` | 2570 | 184 |
| `2025-03-17` | 2569 | 185 |
| `2025-03-18` | 2569 | 185 |
| `2025-03-19` | 2569 | 185 |
| `2025-03-20` | 2572 | 185 |
| `2025-03-21` | 2570 | 188 |

## Guardrails

- This consumes supplied status replay rows; it does not prove status-source completeness.
- `include` means the row passed the local instrument/status filters in this smoke input.
- Do not treat this as Backtest-ready until historical status coverage, Liquidity Filter, and strategy/OOS gates are complete.
