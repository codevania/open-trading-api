# KIND Status Events Extract

- Capture date: `2026-07-03`
- Raw directory: [[_report/raw/2026/2026-07-03/kind/status-source-probe|_report/raw/2026/2026-07-03/kind/status-source-probe]]
- Events output: [[_report/quant/data/point_in_time_status_events/2026-07-03-kind-current-status-events.csv|_report/quant/data/point_in_time_status_events/2026-07-03-kind-current-status-events.csv]]
- Event rows: `344`
- Deduped rows: `5`
- Source: `kind`
- Interpretation: normalized current/status snapshot events; not complete historical Point-in-Time coverage
- Backtest readiness: `hold`

## Rows By Snapshot

| Snapshot | Event rows |
| --- | ---: |
| `delisted_company` | 62 |
| `managed_issue` | 104 |
| `market_alert_caution` | 40 |
| `market_alert_risk` | 1 |
| `market_alert_warning` | 16 |
| `trading_halt` | 126 |

## Guardrails

- `trading_halt` rows use the capture date because the KIND current halt snapshot does not expose halt start dates.
- `market` is `UNKNOWN` until joined to an official listed-issue or market classification source.
- Use [[scripts/quant_point_in_time_status_events_validate.py|scripts/quant_point_in_time_status_events_validate.py]] before replay.
- This advances source normalization, but it does not make `Backtest` ready without historical coverage.
