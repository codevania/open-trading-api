# Point-in-Time Status Source Coverage Manifest Validate

- Manifest: [[_report/quant/research/2026-07-09-point-in-time-status-source-manifest-draft-20250102-20250418-market-enriched-81d.rows.csv|_report/quant/research/2026-07-09-point-in-time-status-source-manifest-draft-20250102-20250418-market-enriched-81d.rows.csv]]
- Source policy: [[_report/quant/data/point_in_time_status_sources.yaml|_report/quant/data/point_in_time_status_sources.yaml]]
- Market-data input: `not_supplied`
- Market window: `2025-01-02..2025-04-18`
- Required status types: `managed_issue,trading_halt,market_alert,delisting`
- Overall status: `fail`
- KIS/KRX API call: `false`
- Order intent generated: `false`
- Interpretation: source manifest validation only, not a `Backtest` result

## Summary

| Metric | Value |
| --- | ---: |
| Manifest rows | 10 |
| Row failures | 10 |
| Missing coverage status types | `none` |

## Row Checks

| Row | Status type | Coverage | Source | Raw path | Status | Message |
| ---: | --- | --- | --- | --- | --- | --- |
| 2 | `managed_issue` | `2025-01-02..2025-04-18` | `krx_data_marketplace` | `` | `fail` | source_url is empty; raw_path is empty; confidence must be high, medium, or low |
| 3 | `managed_issue` | `2025-01-02..2025-04-18` | `kind` | `` | `fail` | source_url is empty; raw_path is empty; confidence must be high, medium, or low |
| 4 | `managed_issue` | `2025-01-02..2025-04-18` | `manual_snapshot` | `` | `fail` | source_url is empty; raw_path is empty; confidence must be high, medium, or low |
| 5 | `trading_halt` | `2025-01-02..2025-04-18` | `kind` | `` | `fail` | source_url is empty; raw_path is empty; confidence must be high, medium, or low |
| 6 | `trading_halt` | `2025-01-02..2025-04-18` | `manual_snapshot` | `` | `fail` | source_url is empty; raw_path is empty; confidence must be high, medium, or low |
| 7 | `market_alert` | `2025-01-02..2025-04-18` | `krx_data_marketplace` | `` | `fail` | source_url is empty; raw_path is empty; confidence must be high, medium, or low |
| 8 | `market_alert` | `2025-01-02..2025-04-18` | `manual_snapshot` | `` | `fail` | source_url is empty; raw_path is empty; confidence must be high, medium, or low |
| 9 | `delisting` | `2025-01-02..2025-04-18` | `krx_data_marketplace` | `` | `fail` | source_url is empty; raw_path is empty; confidence must be high, medium, or low |
| 10 | `delisting` | `2025-01-02..2025-04-18` | `kind` | `` | `fail` | source_url is empty; raw_path is empty; confidence must be high, medium, or low |
| 11 | `delisting` | `2025-01-02..2025-04-18` | `manual_snapshot` | `` | `fail` | source_url is empty; raw_path is empty; confidence must be high, medium, or low |

## Guardrails

- This validator does not prove that normalized status-event rows are complete.
- A passing manifest only proves the source coverage rows are locally usable by the coverage audit gate.
- Keep `Backtest readiness` at `hold` until status events, replay, costs, OOS, and Bias Control pass.
