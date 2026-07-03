# Point-in-Time Status Replay Scaffold

## Summary

- Date: `2026-07-03`
- Scope: apply validated status-event rows to date/code market-data rows
- Backtest readiness: `hold`
- Raw status collection: `kind_current_snapshot_validated`

The replay scaffold turns normalized status events into row-level status flags on a market-data input. It is intentionally separate from KRX/KIND collection and from `Backtest`.

## Added Artifacts

- Replay script: [[scripts/quant_point_in_time_status_replay.py|scripts/quant_point_in_time_status_replay.py]]
- Tests: [[tests/test_quant_point_in_time_status_replay.py|tests/test_quant_point_in_time_status_replay.py]]
- Required validator: [[scripts/quant_point_in_time_status_events_validate.py|scripts/quant_point_in_time_status_events_validate.py]]
- KIND current snapshot replay result: [[_report/quant/research/2026-07-03-kind-status-replay-on-openapi-20250102-20250124|_report/quant/research/2026-07-03-kind-status-replay-on-openapi-20250102-20250124.md]]

## Replay Behavior

For each market-data row keyed by `date` and `code`, the script applies status events with `event_date <= date`.

Active exclusion flags:

| Flag | Active event |
| --- | --- |
| `pit_managed_issue_active` | `managed_issue=designated` until `managed_issue=released` |
| `pit_trading_halt_active` | `trading_halt=halted` until `trading_resume=resumed` |
| `pit_market_alert_active` | `market_alert=caution/warning/risk` until `market_alert=released` |
| `pit_delisting_active` | `delisting=delisting_notice/delisted` |

Output rows receive:

- `pit_status_replay_status`
- `pit_status_exclude_reasons`
- `pit_latest_event_date`
- `pit_applied_event_count`
- `pit_source_paths`

## Command Shape

```powershell
.venv\Scripts\python.exe scripts\quant_point_in_time_status_replay.py `
  --market-data _report\raw\YYYY\YYYY-MM-DD\krx\openapi-market-data\YYYYMMDD-YYYYMMDD\market_data.csv `
  --events _report\raw\YYYY\YYYY-MM-DD\krx\status\status_events.normalized.csv `
  --output _report\raw\YYYY\YYYY-MM-DD\krx\status\market_data.with_status.csv `
  --report-output _report\quant\research\YYYY-MM-DD-point-in-time-status-replay.md
```

## Current Judgment

This is useful local plumbing and has now been smoke-tested with one official KIND current snapshot.
The KIND replay used `344` valid status-event rows against the 17-date KRX OpenAPI market-data join and marked `280/46659` rows as `exclude_by_status_event`.
Market enrichment from the same join resolved `310/344` event rows; `34` remain `UNKNOWN`.
`include_by_status_event` means "not excluded by the provided event rows"; it does not prove complete historical status coverage.

Next gate:

1. Extend KIND or authenticated/manual KRX status coverage across the selected historical date range.
2. Add market classification where an official source or deterministic join can support it.
3. Validate the expanded events with [[scripts/quant_point_in_time_status_events_validate.py|scripts/quant_point_in_time_status_events_validate.py]].
4. Replay the expanded event set before wiring status flags into `Universe`.
