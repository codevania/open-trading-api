# Point-in-Time Status Lifecycle Gap Report

- Status events: [[_report/quant/data/point_in_time_status_events/2026-07-08-kind-current-status-events.merged-20260703-20260708.csv|_report/quant/data/point_in_time_status_events/2026-07-08-kind-current-status-events.merged-20260703-20260708.csv]]
- Market data: [[_report/raw/2026/2026-07-08/krx/openapi-market-data/20250102-20250418/market_data.csv|_report/raw/2026/2026-07-08/krx/openapi-market-data/20250102-20250418/market_data.csv]]
- Output: [[_report/quant/research/2026-07-09-point-in-time-status-lifecycle-gaps-20250102-20250418-merged-snapshots.rows.csv|_report/quant/research/2026-07-09-point-in-time-status-lifecycle-gaps-20250102-20250418-merged-snapshots.rows.csv]]
- Required lifecycle status types: `managed_issue,trading_halt,market_alert`
- KIS/KRX API call: `false`
- Order intent generated: `false`
- Backtest readiness impact: `hold`
- Interpretation: lifecycle collection-target diagnostic, not historical status truth

## Summary

| Metric | Value |
| --- | ---: |
| Status event rows | 497 |
| Status event codes | 286 |
| Market rows | 198137 |
| Market codes | 2776 |
| Market window | `2025-01-02..2025-04-18` |
| Lifecycle groups | 304 |
| Missing release/resume groups | 304 |
| Active after latest release groups | 0 |
| Has release/resume evidence groups | 0 |
| Release without active groups | 0 |

## Lifecycle Gap Status Counts

| Gap status | Groups |
| --- | ---: |
| `missing_release_resume_evidence` | 304 |

## Gap Counts By Status Type

| Status type | Missing release/resume | Active after latest release | Has release/resume | Release without active |
| --- | ---: | ---: | ---: | ---: |
| `managed_issue` | 104 | 0 | 0 | 0 |
| `market_alert` | 70 | 0 | 0 | 0 |
| `trading_halt` | 130 | 0 | 0 | 0 |

## Input Status Type Counts

| Status type | Rows |
| --- | ---: |
| `delisting` | 64 |
| `managed_issue` | 105 |
| `market_alert` | 75 |
| `trading_halt` | 253 |

## Guardrails

- `trading_resume` rows are counted as release-like evidence for `trading_halt` lifecycle groups.
- Rows with `missing_release_resume_evidence` are collection targets for official transition evidence.
- This report does not prove historical completeness and must not promote `Backtest readiness`.
