# Point-in-Time Status Evidence Collection Queue

- Evidence plan: [[_report/quant/research/2026-07-09-point-in-time-status-evidence-collection-plan-20250102-20250418-merged-3snapshots-market-enriched-81d.rows.csv|_report/quant/research/2026-07-09-point-in-time-status-evidence-collection-plan-20250102-20250418-merged-3snapshots-market-enriched-81d.rows.csv]]
- Queue rows: [[_report/quant/research/2026-07-10-point-in-time-status-evidence-collection-queue-merged-3snapshots-market-enriched-81d.rows.csv|_report/quant/research/2026-07-10-point-in-time-status-evidence-collection-queue-merged-3snapshots-market-enriched-81d.rows.csv]]
- Batch size: `25`
- KIS/KRX API call: `false`
- Order intent generated: `false`
- Backtest readiness impact: `hold`
- Interpretation: execution queue only, not source coverage evidence

## Summary

| Metric | Value |
| --- | ---: |
| Evidence plan rows | 385 |
| Unique codes in plan | 243 |
| Queue batches | 33 |
| Queued source rows | 385 |

## Priority Batch Counts

| Priority | Batches |
| --- | ---: |
| `1` | 10 |
| `2` | 18 |
| `3` | 5 |

## Blocker Batch Counts

| Blocker | Batches |
| --- | ---: |
| `market_label_resolution` | 5 |
| `release_resume_evidence` | 18 |
| `source_manifest_evidence` | 10 |

## Status Type Batch Counts

| Status type | Batches |
| --- | ---: |
| `delisting` | 4 |
| `managed_issue` | 10 |
| `market_alert` | 8 |
| `trading_halt` | 11 |

## Suggested Source Batch Counts

| Suggested source | Batches |
| --- | ---: |
| `kind` | 5 |
| `kind:Managed issue event;Trading halt or resumption disclosure;Delisting disclosure` | 3 |
| `kind;manual_snapshot` | 7 |
| `krx_data_marketplace:Designated details of all issues;Market alert issue;Delisting` | 3 |
| `krx_data_marketplace;kind;manual_snapshot` | 6 |
| `krx_data_marketplace;manual_snapshot` | 5 |
| `manual_snapshot:Manual download captured from an official KRX or KIND page` | 4 |

## Collection Status Batch Counts

| Collection status | Batches |
| --- | ---: |
| `pending_market_label_evidence` | 5 |
| `pending_raw_evidence` | 10 |
| `pending_release_resume_evidence` | 18 |

## Execution Order

1. Execute `P1-*` source manifest batches first and fill official `source_url`, `raw_path`, and `confidence` evidence.
2. Execute `P2-*` release/resume batches only after the matching source manifest evidence is filled.
3. Execute `P3-*` UNKNOWN market label batches with official evidence or deterministic local joins only.

## Guardrails

- This queue is derived from the plan and is not a filled source coverage manifest.
- Do not pass queue rows to the coverage audit as evidence.
- Keep `Backtest readiness` at `hold` until filled manifest validation, lifecycle coverage, costs, OOS, and Bias Control pass.
