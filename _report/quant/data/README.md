# Quant Data Scaffolding

This directory is for small schema, config, and fixture-scale examples only.
Do not store bulk raw market data here.

Raw source evidence belongs under `_report/raw/**` and should remain
uncommitted unless a later policy explicitly allows a tiny sanitized fixture.

## Current Files

- [[_report/quant/data/schemas/point_in_time_status_events.schema.json|_report/quant/data/schemas/point_in_time_status_events.schema.json]] defines normalized `Point-in-Time` status-event rows.
- [[_report/quant/data/point_in_time_status_sources.yaml|_report/quant/data/point_in_time_status_sources.yaml]] records the source policy for KRX Data Marketplace, KIND, and manual snapshots.

## Guardrails

- A valid status-event row is not a `Point-in-Time Universe` by itself.
- A status-event CSV must point back to raw evidence under `_report/raw/**`.
- `Backtest` readiness stays `hold` until enough status events can replay historical Universe membership for the selected test scope.
