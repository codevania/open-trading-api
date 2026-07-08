# Point-in-Time Status Source Manifest Draft

- Lifecycle gaps: [[_report/quant/research/2026-07-09-point-in-time-status-lifecycle-gaps-20250102-20250418-merged-snapshots-market-enriched-81d.rows.csv|_report/quant/research/2026-07-09-point-in-time-status-lifecycle-gaps-20250102-20250418-merged-snapshots-market-enriched-81d.rows.csv]]
- Source policy: [[_report/quant/data/point_in_time_status_sources.yaml|_report/quant/data/point_in_time_status_sources.yaml]]
- Output: [[_report/quant/research/2026-07-09-point-in-time-status-source-manifest-draft-20250102-20250418-market-enriched-81d.rows.csv|_report/quant/research/2026-07-09-point-in-time-status-source-manifest-draft-20250102-20250418-market-enriched-81d.rows.csv]]
- Coverage window: `2025-01-02..2025-04-18`
- Required status types: `managed_issue,trading_halt,market_alert,delisting`
- Draft status: `pending_raw_evidence`
- KIS/KRX API call: `false`
- Order intent generated: `false`
- Backtest readiness impact: `hold`
- Interpretation: collection planning only, not source coverage evidence

## Summary

| Metric | Value |
| --- | ---: |
| Lifecycle gap rows | 304 |
| Draft manifest rows | 10 |

## Lifecycle Targets By Status Type

| Status type | Target groups | Target codes |
| --- | ---: | ---: |
| `managed_issue` | 104 | 104 |
| `trading_halt` | 130 | 130 |
| `market_alert` | 70 | 70 |
| `delisting` | 0 | 0 |

## Candidate Sources

| Source | Draft rows |
| --- | ---: |
| `kind` | 3 |
| `krx_data_marketplace` | 3 |
| `manual_snapshot` | 4 |

## Guardrails

- `source_url`, `raw_path`, and `confidence` are intentionally blank in the draft.
- Do not pass this draft as source evidence until official raw files are saved and those fields are filled.
- A valid source manifest still does not promote `Backtest readiness`; normalized status events, replay, costs, OOS, and Bias Control must also pass.
