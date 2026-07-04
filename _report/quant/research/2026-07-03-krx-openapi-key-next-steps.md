# KRX OpenAPI Key Next Steps

## Status

- User has obtained a KRX OpenAPI authentication key.
- User reported that the requested KRX OpenAPI services were approved.
- The key must not be pasted into chat, `_report/`, `omx_wiki/`, tracked scripts, or commit history.
- Local secret path: `.env.krx`
- Example template: `.env.krx.example`
- Read-only probe script: [[scripts/quant_krx_openapi_probe.py|scripts/quant_krx_openapi_probe.py]]
- Core read-only collector: [[scripts/quant_krx_openapi_collect.py|scripts/quant_krx_openapi_collect.py]]
- Saved-raw normalizer: [[scripts/quant_krx_openapi_normalize.py|scripts/quant_krx_openapi_normalize.py]]
- Historical missing-raw planner: [[scripts/quant_krx_openapi_history_plan.py|scripts/quant_krx_openapi_history_plan.py]]
- Continuity auditor: [[scripts/quant_krx_openapi_continuity_audit.py|scripts/quant_krx_openapi_continuity_audit.py]]
- Market-data join: [[scripts/quant_krx_openapi_market_data_join.py|scripts/quant_krx_openapi_market_data_join.py]]
- Market-data merge: [[scripts/quant_krx_openapi_market_data_merge.py|scripts/quant_krx_openapi_market_data_merge.py]]
- Point-in-Time status source gap: [[_report/quant/research/2026-07-03-point-in-time-status-source-gap|_report/quant/research/2026-07-03-point-in-time-status-source-gap.md]]
- Point-in-Time status-event schema: [[_report/quant/research/2026-07-03-point-in-time-status-event-schema|_report/quant/research/2026-07-03-point-in-time-status-event-schema.md]]
- Point-in-Time status-event validator: [[scripts/quant_point_in_time_status_events_validate.py|scripts/quant_point_in_time_status_events_validate.py]]
- Point-in-Time status replay scaffold: [[scripts/quant_point_in_time_status_replay.py|scripts/quant_point_in_time_status_replay.py]]
- KRX Data Marketplace status-source probe: [[scripts/quant_krx_data_marketplace_status_probe.py|scripts/quant_krx_data_marketplace_status_probe.py]]
- KRX Data Marketplace status-source probe result: [[_report/quant/research/2026-07-03-krx-data-marketplace-status-source-probe|_report/quant/research/2026-07-03-krx-data-marketplace-status-source-probe.md]]
- KIND status-source probe: [[scripts/quant_kind_status_source_probe.py|scripts/quant_kind_status_source_probe.py]]
- KIND status-event extractor: [[scripts/quant_kind_status_events_extract.py|scripts/quant_kind_status_events_extract.py]]
- KIND status-source probe result: [[_report/quant/research/2026-07-03-kind-status-source-probe|_report/quant/research/2026-07-03-kind-status-source-probe.md]]
- KIND status-event extraction result: [[_report/quant/research/2026-07-03-kind-status-events-extract|_report/quant/research/2026-07-03-kind-status-events-extract.md]]
- KIND status-event validation result: [[_report/quant/research/2026-07-03-kind-status-events-validation|_report/quant/research/2026-07-03-kind-status-events-validation.md]]
- KIND status replay result: [[_report/quant/research/2026-07-03-kind-status-replay-on-openapi-20250102-20250124|_report/quant/research/2026-07-03-kind-status-replay-on-openapi-20250102-20250124.md]]
- Point-in-Time status-event market enrichment: [[scripts/quant_point_in_time_status_events_enrich_market.py|scripts/quant_point_in_time_status_events_enrich_market.py]]
- KIND status-event market enrichment result: [[_report/quant/research/2026-07-03-kind-status-events-market-enrich|_report/quant/research/2026-07-03-kind-status-events-market-enrich.md]]
- Point-in-Time Momentum Signal Candidate generator: [[scripts/quant_point_in_time_signal_candidates.py|scripts/quant_point_in_time_signal_candidates.py]]
- Point-in-Time Momentum Signal Candidate smoke result: [[_report/quant/research/2026-07-04-kind-status-point-in-time-momentum-signal-candidates-smoke-20250102-20250124|_report/quant/research/2026-07-04-kind-status-point-in-time-momentum-signal-candidates-smoke-20250102-20250124.md]]
- Latest 20-day Point-in-Time Momentum Signal Candidate smoke result: [[_report/quant/research/2026-07-04-kind-status-point-in-time-momentum-signal-candidates-smoke-20d-20250102-20250207|_report/quant/research/2026-07-04-kind-status-point-in-time-momentum-signal-candidates-smoke-20d-20250102-20250207.md]]
- Quant readiness checker: [[scripts/quant_readiness_check.py|scripts/quant_readiness_check.py]]
- Latest 20-day Quant readiness check: [[_report/quant/research/2026-07-04-quant-readiness-check-20d|_report/quant/research/2026-07-04-quant-readiness-check-20d.md]]
- Latest KRX OpenAPI market-data merge: [[_report/quant/research/2026-07-04-krx-openapi-market-data-merge-20250102-20250207|_report/quant/research/2026-07-04-krx-openapi-market-data-merge-20250102-20250207.md]]
- Latest Point-in-Time Liquidity Filter 20-day smoke: [[_report/quant/research/2026-07-04-kind-status-point-in-time-liquidity-smoke-20d-20250102-20250207|_report/quant/research/2026-07-04-kind-status-point-in-time-liquidity-smoke-20d-20250102-20250207.md]]

## Why This Matters

KRX OpenAPI is the preferred source for reproducible official KRX market data in the Quant pipeline.
It can reduce dependence on current-snapshot KIS OHLCV collection, but it does not by itself solve the full `Point-in-Time Universe`.

The first objective is not a Backtest. The first objective is a read-only raw-data smoke test.

## User-Side Secret Handling

Create the ignored local file:

```powershell
Copy-Item .env.krx.example .env.krx
notepad .env.krx
```

Fill only this value:

```env
KRX_AUTH_KEY=your_key_here
```

Do not put the key in command arguments. Command history is easier to leak than an ignored local env file.

## KRX Service Approval Needed

KRX OpenAPI has two gates:

1. API authentication key.
2. API service usage approval for each dataset/product.

For the Quant pipeline, prioritize these stock services first:

- KOSPI daily trading data.
- KOSDAQ daily trading data.
- KOSPI basic issue data.
- KOSDAQ basic issue data.
- KOSPI index daily data.
- KOSDAQ index daily data.

The KRX service page provides the official sample/service URL after the service is available. Use that URL in the probe script.

Approved core service mapping:

| service id | KRX API name | endpoint |
| --- | --- | --- |
| `kospi_stock_daily` | 유가증권 일별매매정보 | `https://data-dbg.krx.co.kr/svc/apis/sto/stk_bydd_trd` |
| `kosdaq_stock_daily` | 코스닥 일별매매정보 | `https://data-dbg.krx.co.kr/svc/apis/sto/ksq_bydd_trd` |
| `kospi_issue_base` | 유가증권 종목기본정보 | `https://data-dbg.krx.co.kr/svc/apis/sto/stk_isu_base_info` |
| `kosdaq_issue_base` | 코스닥 종목기본정보 | `https://data-dbg.krx.co.kr/svc/apis/sto/ksq_isu_base_info` |
| `kospi_index_daily` | KOSPI 시리즈 일별시세정보 | `https://data-dbg.krx.co.kr/svc/apis/idx/kospi_dd_trd` |
| `kosdaq_index_daily` | KOSDAQ 시리즈 일별시세정보 | `https://data-dbg.krx.co.kr/svc/apis/idx/kosdaq_dd_trd` |

## Read-Only Smoke Command Shape

```powershell
uv run python scripts/quant_krx_openapi_probe.py `
  --url "OFFICIAL_KRX_SAMPLE_URL" `
  --param basDd=YYYYMMDD `
  --output _report/raw/YYYY/YYYY-MM-DD/krx/openapi/smoke.raw.json
```

The script sends the key as request header `AUTH_KEY` and writes:

- raw response: the `--output` path
- metadata sidecar: `smoke.raw.json.meta.json`

After the core service mapping is known, collect all core raw files with:

```powershell
.venv\Scripts\python.exe scripts/quant_krx_openapi_collect.py --bas-dd YYYYMMDD
```

If `uv run` fails with a local cache permission error, use `.venv\Scripts\python.exe`.

Smoke result on `2025-01-02`:

| service id | row count |
| --- | ---: |
| `kospi_stock_daily` | 961 |
| `kosdaq_stock_daily` | 1784 |
| `kospi_issue_base` | 961 |
| `kosdaq_issue_base` | 1784 |
| `kospi_index_daily` | 51 |
| `kosdaq_index_daily` | 40 |

Smoke result on `2026-07-02`:

- HTTP `200` for all six services.
- `OutBlock_1` row count was `0` for all six services.
- Treat `2026-07-02` as not usable for schema validation yet; use known historical trading days for parser development.

## Interpretation Gate

Passing one KRX OpenAPI smoke test changes the status to:

- KRX OpenAPI access: `usable_for_raw_collection`
- KRX OpenAPI normalizer: `usable_for_parser_development` on saved `2025-01-02` core raws
- KRX OpenAPI historical window: `usable_for_multi_date_parser_development` for `2025-01-02` through `2025-01-24`
- KRX OpenAPI continuity audit: `passed_for_17_date_window`
- KRX OpenAPI market-data join/merge: `usable_for_23_date_market_data_input`
- KRX Data Marketplace unattended status JSON access: `auth_required`
- KIND public status fallback: `344_valid_events_replayed_on_17_date_smoke`
- KIND market enrichment: `310_of_344_events_resolved_from_17_date_market_data_join`
- Point-in-Time status-event validator: `validated_kind_current_snapshot`
- Point-in-Time status replay scaffold: `validated_kind_snapshot_replayed_on_23_date_market_data`
- Point-in-Time Universe smoke: `58961_include_4204_exclude_on_23_date_window`
- Point-in-Time Liquidity Filter smoke: `4034_include_59131_exclude_on_23_date_20_day_window`
- Point-in-Time Momentum Signal Candidate smoke: `120_candidates_3_dates_20_day_paper_only`
- Quant readiness check: `market_data_pass_liquidity_signal_pass_smoke_backtest_hold_live_blocked`
- KIS demo trading readiness: `blocked_missing_kis_paper_stock`
- Backtest readiness: still `hold`
- Live trading readiness: still `blocked`

Backtest interpretation remains blocked until the pipeline can reproduce `Point-in-Time` status fields by Rebalance date, including listing status, managed issue status, trading suspension, and delisting events.

## Agent Next Steps

After core KRX OpenAPI coverage and the KIND current snapshot smoke:

1. Preserve the `2025-01-08` row-count movement as an event-validation item.
2. Extend KIND or authenticated/manual KRX status coverage across the selected historical date range.
3. Resolve remaining `34` `UNKNOWN` KIND market rows only where official source evidence or a deterministic market-data join can support it.
4. Validate the expanded event rows with [[scripts/quant_point_in_time_status_events_validate.py|scripts/quant_point_in_time_status_events_validate.py]] and replay them with [[scripts/quant_point_in_time_status_replay.py|scripts/quant_point_in_time_status_replay.py]].
5. Rebuild the `Point-in-Time Universe` smoke with [[scripts/quant_point_in_time_universe_build.py|scripts/quant_point_in_time_universe_build.py]] after each expanded status-event set.
6. Rebuild the `Point-in-Time` Liquidity Filter smoke with [[scripts/quant_point_in_time_liquidity_filter.py|scripts/quant_point_in_time_liquidity_filter.py]] after each expanded status/date set; the 20-day lookback now works on the 23-date smoke but is still not Backtest-ready.
7. Rebuild the Momentum Signal Candidate smoke with [[scripts/quant_point_in_time_signal_candidates.py|scripts/quant_point_in_time_signal_candidates.py]] only after the Point-in-Time Universe and Liquidity rows are refreshed; keep it paper-only.
8. Rerun [[scripts/quant_readiness_check.py|scripts/quant_readiness_check.py]] after each Point-in-Time, Liquidity Filter, Signal Candidate, or KIS account milestone.
9. Keep KIS demo trading at dry-run/local preflight only until `KIS_PAPER_STOCK` is filled, auth/account read-only preflight passes, buying-power/sellable-quantity checks exist, and status/cancel flow, kill switch, and explicit confirmation gate exist. See [[_report/quant/research/2026-07-03-kis-demo-trading-readiness|_report/quant/research/2026-07-03-kis-demo-trading-readiness.md]].
10. Validate status replay coverage before connecting normalized market-data rows to `Universe` or `Backtest` code.
11. Extend KRX OpenAPI market-data coverage further before production Momentum lookbacks.
12. Keep `Backtest` readiness at `hold` until historical status replay is solved.
