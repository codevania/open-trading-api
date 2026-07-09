# Point-in-Time Status Evidence Collection Plan

- Lifecycle gaps: [[_report/quant/research/2026-07-09-point-in-time-status-lifecycle-gaps-20250102-20250418-merged-3snapshots-market-enriched-81d.rows.csv|_report/quant/research/2026-07-09-point-in-time-status-lifecycle-gaps-20250102-20250418-merged-3snapshots-market-enriched-81d.rows.csv]]
- Source manifest draft: [[_report/quant/research/2026-07-09-point-in-time-status-source-manifest-draft-20250102-20250418-market-enriched-81d.rows.csv|_report/quant/research/2026-07-09-point-in-time-status-source-manifest-draft-20250102-20250418-market-enriched-81d.rows.csv]]
- Unknown market targets: [[_report/quant/research/2026-07-09-kind-status-events-unknown-market-targets-merged-3snapshots-market-enriched-81d.rows.csv|_report/quant/research/2026-07-09-kind-status-events-unknown-market-targets-merged-3snapshots-market-enriched-81d.rows.csv]]
- Output: [[_report/quant/research/2026-07-09-point-in-time-status-evidence-collection-plan-20250102-20250418-merged-3snapshots-market-enriched-81d.rows.csv|_report/quant/research/2026-07-09-point-in-time-status-evidence-collection-plan-20250102-20250418-merged-3snapshots-market-enriched-81d.rows.csv]]
- KIS/KRX API call: `false`
- Order intent generated: `false`
- Backtest readiness impact: `hold`
- Interpretation: collection plan only, not source coverage evidence

## Summary

| Metric | Value |
| --- | ---: |
| Lifecycle gap rows | 314 |
| Manifest draft rows | 10 |
| Unknown market rows | 61 |
| Collection plan rows | 385 |

## Priority Counts

| Priority | Rows |
| --- | ---: |
| `1` | 10 |
| `2` | 314 |
| `3` | 61 |

## Blocker Counts

| Blocker | Rows |
| --- | ---: |
| `market_label_resolution` | 61 |
| `release_resume_evidence` | 314 |
| `source_manifest_evidence` | 10 |

## Status Type Counts

| Status type | Rows |
| --- | ---: |
| `delisting` | 12 |
| `managed_issue` | 115 |
| `market_alert` | 84 |
| `trading_halt` | 174 |

## Collection Status Counts

| Collection status | Rows |
| --- | ---: |
| `pending_market_label_evidence` | 61 |
| `pending_raw_evidence` | 10 |
| `pending_release_resume_evidence` | 314 |

## Execution Order

1. Fill source manifest evidence rows from official raw KRX/KIND files.
2. Collect release/resume or inactive-state evidence for lifecycle gap rows.
3. Resolve UNKNOWN market labels only with official evidence or deterministic local joins.

## Guardrails

- This plan is not a filled source coverage manifest.
- Do not pass this plan to the coverage audit as evidence.
- Keep `Backtest readiness` at `hold` until filled manifest validation, lifecycle coverage, costs, OOS, and Bias Control pass.
