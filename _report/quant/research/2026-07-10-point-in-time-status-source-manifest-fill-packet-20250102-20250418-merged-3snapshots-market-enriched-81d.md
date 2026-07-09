# Point-in-Time Status Source Manifest Fill Packet

- Source manifest draft: [[_report/quant/research/2026-07-09-point-in-time-status-source-manifest-draft-20250102-20250418-market-enriched-81d.rows.csv|_report/quant/research/2026-07-09-point-in-time-status-source-manifest-draft-20250102-20250418-market-enriched-81d.rows.csv]]
- Evidence queue: [[_report/quant/research/2026-07-10-point-in-time-status-evidence-collection-queue-merged-3snapshots-market-enriched-81d.rows.csv|_report/quant/research/2026-07-10-point-in-time-status-evidence-collection-queue-merged-3snapshots-market-enriched-81d.rows.csv]]
- Fill packet rows: [[_report/quant/research/2026-07-10-point-in-time-status-source-manifest-fill-packet-20250102-20250418-merged-3snapshots-market-enriched-81d.rows.csv|_report/quant/research/2026-07-10-point-in-time-status-source-manifest-fill-packet-20250102-20250418-merged-3snapshots-market-enriched-81d.rows.csv]]
- Coverage windows: `2025-01-02..2025-04-18`
- KIS/KRX API call: `false`
- Order intent generated: `false`
- Backtest readiness impact: `hold`
- Interpretation: fill checklist only, not source coverage evidence

## Summary

| Metric | Value |
| --- | ---: |
| Manifest draft rows | 10 |
| P1 queue batches | 10 |
| Fill packet rows | 10 |
| Unmatched manifest rows | `none` |

## Status Type Counts

| Status type | Rows |
| --- | ---: |
| `delisting` | 3 |
| `managed_issue` | 3 |
| `market_alert` | 2 |
| `trading_halt` | 2 |

## Source Counts

| Source | Rows |
| --- | ---: |
| `kind` | 3 |
| `krx_data_marketplace` | 3 |
| `manual_snapshot` | 4 |

## Fill Instructions

1. Use each `batch_id` to capture an official raw file from the listed source and candidate table.
2. Fill `source_url_to_fill`, `raw_path_to_fill`, and `confidence_to_fill` only after the raw file is saved under `_report/raw/**`.
3. Convert filled packet evidence into a source coverage manifest, then run the manifest validator and coverage audit.

## Guardrails

- This packet is not a valid source coverage manifest while fill fields are blank.
- Do not pass this packet to the coverage audit as evidence.
- Keep `Backtest readiness` at `hold` until filled manifest validation, lifecycle coverage, costs, OOS, and Bias Control pass.
