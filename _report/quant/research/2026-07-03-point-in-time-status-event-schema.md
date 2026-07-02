# Point-in-Time Status Event Schema

## Summary

- Date: `2026-07-03`
- Scope: local `Point-in-Time` status-event schema/config scaffolding
- Backtest readiness: `hold`
- Raw collection status: `not_started_for_status_events`

This step creates the local contract for status events before any KRX Data Marketplace or KIND status raw sample is wired into `Universe`.

## Added Artifacts

- Schema: [[_report/quant/data/schemas/point_in_time_status_events.schema.json|_report/quant/data/schemas/point_in_time_status_events.schema.json]]
- Source policy: [[_report/quant/data/point_in_time_status_sources.yaml|_report/quant/data/point_in_time_status_sources.yaml]]
- Data scaffolding README: [[_report/quant/data/README|_report/quant/data/README.md]]
- Validator: [[scripts/quant_point_in_time_status_events_validate.py|scripts/quant_point_in_time_status_events_validate.py]]
- Tests: [[tests/test_quant_point_in_time_status_events_validate.py|tests/test_quant_point_in_time_status_events_validate.py]]

## Normalized Row Contract

Required columns:

| Column | Rule |
| --- | --- |
| `event_date` | ISO `YYYY-MM-DD` |
| `code` | KRX short code, alphanumeric preserved exactly |
| `market` | `KOSPI`, `KOSDAQ`, `KONEX`, or `UNKNOWN` |
| `status_type` | managed issue, trading halt/resume, market alert, listing, listing change, or delisting |
| `status_value` | constrained by `status_type` |
| `source` | `krx_data_marketplace`, `kind`, or `manual_snapshot` |
| `source_url` | official HTTPS URL when available |
| `raw_path` | repo-relative path under `_report/raw/**` |
| `confidence` | `high`, `medium`, or `low` |
| `notes` | parser caveats |

## Command Shape

```powershell
.venv\Scripts\python.exe scripts\quant_point_in_time_status_events_validate.py `
  --events _report\raw\YYYY\YYYY-MM-DD\krx\status\status_events.normalized.csv `
  --rows-output _report\raw\YYYY\YYYY-MM-DD\krx\status\status_events.validation.rows.csv `
  --report-output _report\quant\research\YYYY-MM-DD-point-in-time-status-events-validation.md
```

## Current Judgment

The schema and validator are ready for a small official raw sample. They do not prove historical coverage and do not upgrade `Backtest` readiness.

Next gate:

1. Save one KRX Data Marketplace or KIND status raw sample under `_report/raw/**`.
2. Normalize it into the schema above.
3. Run the validator and keep the validation report.
4. Only then decide how to replay status events into `Universe`.

## Guardrails

- Do not treat KRX OpenAPI market-data rows as status replay.
- Do not commit raw KRX/KIND status files.
- Keep `Backtest` at `hold` until historical status coverage is sufficient for the selected test scope.
