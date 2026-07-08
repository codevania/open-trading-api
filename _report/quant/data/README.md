# Quant Data Scaffolding

This directory is for small schema, config, and fixture-scale examples only.
Do not store bulk raw market data here.

Raw source evidence belongs under `_report/raw/**` and should remain
uncommitted unless a later policy explicitly allows a tiny sanitized fixture.

## Current Files

- [[_report/quant/data/schemas/point_in_time_status_events.schema.json|_report/quant/data/schemas/point_in_time_status_events.schema.json]] defines normalized `Point-in-Time` status-event rows.
- [[_report/quant/data/point_in_time_status_sources.yaml|_report/quant/data/point_in_time_status_sources.yaml]] records the source policy for KRX Data Marketplace, KIND, and manual snapshots.
- [[_report/quant/data/templates/point_in_time_status_source_coverage_manifest.template.csv|_report/quant/data/templates/point_in_time_status_source_coverage_manifest.template.csv]] is the header-only template for source coverage manifests consumed by [[scripts/quant_point_in_time_status_coverage_audit.py|scripts/quant_point_in_time_status_coverage_audit.py]].
- [[scripts/quant_point_in_time_status_source_manifest_validate.py|scripts/quant_point_in_time_status_source_manifest_validate.py]] validates a filled source coverage manifest against the source policy, raw evidence paths, required status types, and selected market-data window. [[scripts/quant_point_in_time_status_coverage_audit.py|scripts/quant_point_in_time_status_coverage_audit.py]] also applies this validation when `--source-coverage-manifest` is supplied.
- [[_report/quant/data/backtest_cost_benchmark_assumptions.yaml|_report/quant/data/backtest_cost_benchmark_assumptions.yaml]] records local Backtest cost and benchmark assumptions consumed by [[scripts/quant_backtest_assumptions_validate.py|scripts/quant_backtest_assumptions_validate.py]].

## Source Coverage Manifest

`historical_complete` status coverage requires a source coverage manifest in addition to normalized status events and replayed market-data rows.

Required columns:

- `status_type`: one required status type, for example `managed_issue`, `trading_halt`, `market_alert`, or `delisting`.
- `coverage_start` / `coverage_end`: inclusive `YYYY-MM-DD` window covered by the raw official source.
- `source`: source key from [[_report/quant/data/point_in_time_status_sources.yaml|_report/quant/data/point_in_time_status_sources.yaml]].
- `source_url`: official KRX/KIND page or download URL when available.
- `raw_path`: repo-relative raw evidence path under `_report/raw/**`.
- `confidence`: `high`, `medium`, or `low`.
- `notes`: short evidence note.

The manifest validator checks every row for policy/source/raw-path validity, but only the required status types count toward required market-window coverage. Rows outside the required status type scope can pass row validation while still not satisfying the coverage gate.

Validation command shape:

```powershell
.venv\Scripts\python.exe scripts\quant_point_in_time_status_source_manifest_validate.py `
  --manifest _report\quant\data\point_in_time_status_source_coverage_manifest.csv `
  --market-data _report\raw\2026\2026-07-08\krx\openapi-market-data\20250102-20250418\market_data.csv `
  --report-output _report\quant\research\YYYY-MM-DD-point-in-time-status-source-manifest-validate.md
```

## Guardrails

- A valid status-event row is not a `Point-in-Time Universe` by itself.
- A status-event CSV must point back to raw evidence under `_report/raw/**`.
- A source coverage manifest must cover the selected market-data window for every required status type before `historical_complete` can pass.
- A Backtest assumptions file can validate as `pass_assumption_only`, but that does not make the Backtest engine ready.
- `Backtest` readiness stays `hold` until enough status events can replay historical Universe membership for the selected test scope.
