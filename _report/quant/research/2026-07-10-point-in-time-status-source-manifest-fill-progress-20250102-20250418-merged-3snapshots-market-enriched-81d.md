# Point-in-Time Status Source Manifest Fill Progress

- Fill packet: [[_report/quant/research/2026-07-10-point-in-time-status-source-manifest-fill-packet-20250102-20250418-merged-3snapshots-market-enriched-81d.rows.csv|_report/quant/research/2026-07-10-point-in-time-status-source-manifest-fill-packet-20250102-20250418-merged-3snapshots-market-enriched-81d.rows.csv]]
- Progress rows: [[_report/quant/research/2026-07-10-point-in-time-status-source-manifest-fill-progress-20250102-20250418-merged-3snapshots-market-enriched-81d.rows.csv|_report/quant/research/2026-07-10-point-in-time-status-source-manifest-fill-progress-20250102-20250418-merged-3snapshots-market-enriched-81d.rows.csv]]
- KIS/KRX API call: `false`
- Order intent generated: `false`
- Backtest readiness impact: `hold`
- Interpretation: fill progress only, not source coverage evidence

## Summary

| Metric | Value |
| --- | ---: |
| Fill packet rows | 10 |
| Materializable rows | 0 |
| Blocked rows | 10 |
| Raw path exists rows | 0 |

## Missing Field Counts

| Field | Rows |
| --- | ---: |
| `confidence_to_fill` | 10 |
| `evidence_capture_status` | 10 |
| `raw_path_to_fill` | 10 |
| `source_url_to_fill` | 10 |

## Status/Source Counts

| Status type | Source | Rows | Materializable |
| --- | --- | ---: | ---: |
| `delisting` | `kind` | 1 | 0 |
| `delisting` | `krx_data_marketplace` | 1 | 0 |
| `delisting` | `manual_snapshot` | 1 | 0 |
| `managed_issue` | `kind` | 1 | 0 |
| `managed_issue` | `krx_data_marketplace` | 1 | 0 |
| `managed_issue` | `manual_snapshot` | 1 | 0 |
| `market_alert` | `krx_data_marketplace` | 1 | 0 |
| `market_alert` | `manual_snapshot` | 1 | 0 |
| `trading_halt` | `kind` | 1 | 0 |
| `trading_halt` | `manual_snapshot` | 1 | 0 |

## Next Action

1. Capture official raw files for blocked rows.
2. Fill `source_url_to_fill`, `raw_path_to_fill`, `confidence_to_fill`, and non-pending `evidence_capture_status`.
3. Run [[scripts/quant_point_in_time_status_source_manifest_materialize.py|scripts/quant_point_in_time_status_source_manifest_materialize.py]] only after `Materializable rows` equals `Fill packet rows`.

## Guardrails

- This progress report does not validate source coverage.
- Do not pass progress rows to the coverage audit.
- Keep `Backtest readiness` at `hold` until manifest validation, coverage audit, lifecycle coverage, costs, OOS, and Bias Control pass.
