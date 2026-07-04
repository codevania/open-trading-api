# Quant Next Session Handoff - 2026-06-14

## Start Here

If a new Codex session starts, read these files first:

1. [[omx_wiki/quant-implementation-status-2026-06-14|omx_wiki/quant-implementation-status-2026-06-14.md]]
2. [[omx_wiki/quant-krx-current-universe-v0|omx_wiki/quant-krx-current-universe-v0.md]]
3. [[_report/quant/implementation-roadmap|_report/quant/implementation-roadmap.md]]
4. [[_report/quant/research/2026-06-14-krx-current-universe-v0|_report/quant/research/2026-06-14-krx-current-universe-v0.md]]
5. [[_report/quant/universe|_report/quant/universe.md]]

## First Commands

```powershell
git status --short
uv run python -m unittest discover tests
```

If thirtysixth-capture local changes are still present, stage/commit them before expanding OHLCV coverage again.

Suggested commit intent:

`Capture thirtysixth KIS OHLCV universe batch`

Use Lore commit protocol.

## Current Best Next Task

Use the 23-date KRX OpenAPI market-data merge, KIND status replay, `Point-in-Time Universe` smoke, 20-day `Point-in-Time` Liquidity Filter smoke, and paper-only Momentum Signal Candidate smoke as the local plumbing baseline. The next lane is to extend KIND or authenticated/manual KRX status coverage by date/source, resolve remaining `UNKNOWN` market rows where official evidence supports it, and keep the Universe/Liquidity/Signal smoke aligned until it can become a Backtest input. KIS demo trading is only at local preflight level; do not build or run an order executor until demo auth/account, buying-power, sellable-quantity, status/cancel, kill-switch, and explicit confirmation gates are implemented.

Already implemented in the latest local work:

- [[scripts/quant_krx_openapi_probe.py|scripts/quant_krx_openapi_probe.py]]
- [[tests/test_quant_krx_openapi_probe.py|tests/test_quant_krx_openapi_probe.py]]
- [[scripts/quant_krx_openapi_collect.py|scripts/quant_krx_openapi_collect.py]]
- [[tests/test_quant_krx_openapi_collect.py|tests/test_quant_krx_openapi_collect.py]]
- [[scripts/quant_krx_openapi_normalize.py|scripts/quant_krx_openapi_normalize.py]]
- [[tests/test_quant_krx_openapi_normalize.py|tests/test_quant_krx_openapi_normalize.py]]
- [[scripts/quant_krx_openapi_history_plan.py|scripts/quant_krx_openapi_history_plan.py]]
- [[tests/test_quant_krx_openapi_history_plan.py|tests/test_quant_krx_openapi_history_plan.py]]
- [[scripts/quant_krx_openapi_continuity_audit.py|scripts/quant_krx_openapi_continuity_audit.py]]
- [[tests/test_quant_krx_openapi_continuity_audit.py|tests/test_quant_krx_openapi_continuity_audit.py]]
- [[scripts/quant_krx_openapi_market_data_join.py|scripts/quant_krx_openapi_market_data_join.py]]
- [[tests/test_quant_krx_openapi_market_data_join.py|tests/test_quant_krx_openapi_market_data_join.py]]
- [[_report/quant/research/2026-07-03-krx-openapi-key-next-steps|_report/quant/research/2026-07-03-krx-openapi-key-next-steps.md]]
- [[_report/quant/research/2026-07-03-krx-openapi-normalize-smoke|_report/quant/research/2026-07-03-krx-openapi-normalize-smoke.md]]
- [[_report/quant/research/2026-07-03-krx-openapi-history-plan-20250102-20250110|_report/quant/research/2026-07-03-krx-openapi-history-plan-20250102-20250110.md]]
- [[_report/quant/research/2026-07-03-krx-openapi-history-plan-20250102-20250110.requests.json|_report/quant/research/2026-07-03-krx-openapi-history-plan-20250102-20250110.requests.json]]
- [[_report/quant/research/2026-07-03-krx-openapi-history-collection-result-20250102-20250110|_report/quant/research/2026-07-03-krx-openapi-history-collection-result-20250102-20250110.md]]
- [[_report/quant/research/2026-07-03-krx-openapi-history-collection-result-20250102-20250110.requests.json|_report/quant/research/2026-07-03-krx-openapi-history-collection-result-20250102-20250110.requests.json]]
- [[_report/quant/research/2026-07-03-krx-openapi-history-normalize-result-20250102-20250110|_report/quant/research/2026-07-03-krx-openapi-history-normalize-result-20250102-20250110.md]]
- [[_report/quant/research/2026-07-03-krx-openapi-continuity-audit-20250102-20250110|_report/quant/research/2026-07-03-krx-openapi-continuity-audit-20250102-20250110.md]]
- [[_report/quant/research/2026-07-03-krx-openapi-continuity-audit-20250102-20250110.rows.csv|_report/quant/research/2026-07-03-krx-openapi-continuity-audit-20250102-20250110.rows.csv]]
- [[_report/quant/research/2026-07-03-krx-openapi-market-data-join-20250102-20250110|_report/quant/research/2026-07-03-krx-openapi-market-data-join-20250102-20250110.md]]
- [[_report/quant/research/2026-07-03-krx-openapi-history-plan-20250113-20250124|_report/quant/research/2026-07-03-krx-openapi-history-plan-20250113-20250124.md]]
- [[_report/quant/research/2026-07-03-krx-openapi-history-plan-20250113-20250124.requests.json|_report/quant/research/2026-07-03-krx-openapi-history-plan-20250113-20250124.requests.json]]
- [[_report/quant/research/2026-07-03-krx-openapi-history-collection-result-20250113-20250124|_report/quant/research/2026-07-03-krx-openapi-history-collection-result-20250113-20250124.md]]
- [[_report/quant/research/2026-07-03-krx-openapi-history-collection-result-20250113-20250124.requests.json|_report/quant/research/2026-07-03-krx-openapi-history-collection-result-20250113-20250124.requests.json]]
- [[_report/quant/research/2026-07-03-krx-openapi-history-normalize-result-20250113-20250124|_report/quant/research/2026-07-03-krx-openapi-history-normalize-result-20250113-20250124.md]]
- [[_report/quant/research/2026-07-03-krx-openapi-continuity-audit-20250113-20250124|_report/quant/research/2026-07-03-krx-openapi-continuity-audit-20250113-20250124.md]]
- [[_report/quant/research/2026-07-03-krx-openapi-continuity-audit-20250113-20250124.rows.csv|_report/quant/research/2026-07-03-krx-openapi-continuity-audit-20250113-20250124.rows.csv]]
- [[_report/quant/research/2026-07-03-krx-openapi-market-data-join-20250113-20250124|_report/quant/research/2026-07-03-krx-openapi-market-data-join-20250113-20250124.md]]
- [[_report/quant/research/2026-07-03-krx-openapi-history-normalize-result-20250102-20250124|_report/quant/research/2026-07-03-krx-openapi-history-normalize-result-20250102-20250124.md]]
- [[_report/quant/research/2026-07-03-krx-openapi-continuity-audit-20250102-20250124|_report/quant/research/2026-07-03-krx-openapi-continuity-audit-20250102-20250124.md]]
- [[_report/quant/research/2026-07-03-krx-openapi-continuity-audit-20250102-20250124.rows.csv|_report/quant/research/2026-07-03-krx-openapi-continuity-audit-20250102-20250124.rows.csv]]
- [[_report/quant/research/2026-07-03-krx-openapi-market-data-join-20250102-20250124|_report/quant/research/2026-07-03-krx-openapi-market-data-join-20250102-20250124.md]]
- [[_report/quant/research/2026-07-04-krx-openapi-history-plan-20250127-20250207|_report/quant/research/2026-07-04-krx-openapi-history-plan-20250127-20250207.md]]
- [[_report/quant/research/2026-07-04-krx-openapi-history-plan-20250127-20250207.requests.json|_report/quant/research/2026-07-04-krx-openapi-history-plan-20250127-20250207.requests.json]]
- [[_report/quant/research/2026-07-04-krx-openapi-history-collection-result-20250127-20250207|_report/quant/research/2026-07-04-krx-openapi-history-collection-result-20250127-20250207.md]]
- [[_report/quant/research/2026-07-04-krx-openapi-history-collection-result-20250127-20250207.requests.json|_report/quant/research/2026-07-04-krx-openapi-history-collection-result-20250127-20250207.requests.json]]
- [[_report/quant/research/2026-07-04-krx-openapi-history-normalize-result-20250127-20250207|_report/quant/research/2026-07-04-krx-openapi-history-normalize-result-20250127-20250207.md]]
- [[_report/quant/research/2026-07-04-krx-openapi-continuity-audit-20250127-20250207|_report/quant/research/2026-07-04-krx-openapi-continuity-audit-20250127-20250207.md]]
- [[_report/quant/research/2026-07-04-krx-openapi-continuity-audit-20250127-20250207.rows.csv|_report/quant/research/2026-07-04-krx-openapi-continuity-audit-20250127-20250207.rows.csv]]
- [[_report/quant/research/2026-07-04-krx-openapi-market-data-join-20250127-20250207|_report/quant/research/2026-07-04-krx-openapi-market-data-join-20250127-20250207.md]]
- [[scripts/quant_krx_openapi_market_data_merge.py|scripts/quant_krx_openapi_market_data_merge.py]]
- [[tests/test_quant_krx_openapi_market_data_merge.py|tests/test_quant_krx_openapi_market_data_merge.py]]
- [[_report/quant/research/2026-07-04-krx-openapi-market-data-merge-20250102-20250207|_report/quant/research/2026-07-04-krx-openapi-market-data-merge-20250102-20250207.md]]
- [[_report/quant/research/2026-07-03-point-in-time-status-source-gap|_report/quant/research/2026-07-03-point-in-time-status-source-gap.md]]
- [[_report/quant/research/2026-07-03-point-in-time-status-event-schema|_report/quant/research/2026-07-03-point-in-time-status-event-schema.md]]
- [[_report/quant/data/README|_report/quant/data/README.md]]
- [[_report/quant/data/point_in_time_status_sources.yaml|_report/quant/data/point_in_time_status_sources.yaml]]
- [[_report/quant/data/schemas/point_in_time_status_events.schema.json|_report/quant/data/schemas/point_in_time_status_events.schema.json]]
- [[scripts/quant_point_in_time_status_events_validate.py|scripts/quant_point_in_time_status_events_validate.py]]
- [[tests/test_quant_point_in_time_status_events_validate.py|tests/test_quant_point_in_time_status_events_validate.py]]
- [[scripts/quant_point_in_time_status_replay.py|scripts/quant_point_in_time_status_replay.py]]
- [[tests/test_quant_point_in_time_status_replay.py|tests/test_quant_point_in_time_status_replay.py]]
- [[_report/quant/research/2026-07-03-point-in-time-status-replay-scaffold|_report/quant/research/2026-07-03-point-in-time-status-replay-scaffold.md]]
- [[scripts/quant_krx_data_marketplace_status_probe.py|scripts/quant_krx_data_marketplace_status_probe.py]]
- [[tests/test_quant_krx_data_marketplace_status_probe.py|tests/test_quant_krx_data_marketplace_status_probe.py]]
- [[_report/quant/research/2026-07-03-krx-data-marketplace-status-source-probe|_report/quant/research/2026-07-03-krx-data-marketplace-status-source-probe.md]]
- [[scripts/quant_kind_status_source_probe.py|scripts/quant_kind_status_source_probe.py]]
- [[tests/test_quant_kind_status_source_probe.py|tests/test_quant_kind_status_source_probe.py]]
- [[_report/quant/research/2026-07-03-kind-status-source-probe|_report/quant/research/2026-07-03-kind-status-source-probe.md]]
- [[scripts/quant_kind_status_events_extract.py|scripts/quant_kind_status_events_extract.py]]
- [[tests/test_quant_kind_status_events_extract.py|tests/test_quant_kind_status_events_extract.py]]
- [[_report/quant/data/point_in_time_status_events/2026-07-03-kind-current-status-events.csv|_report/quant/data/point_in_time_status_events/2026-07-03-kind-current-status-events.csv]]
- [[_report/quant/research/2026-07-03-kind-status-events-extract|_report/quant/research/2026-07-03-kind-status-events-extract.md]]
- [[_report/quant/research/2026-07-03-kind-status-events-validation|_report/quant/research/2026-07-03-kind-status-events-validation.md]]
- [[_report/quant/research/2026-07-03-kind-status-events-validation.rows.csv|_report/quant/research/2026-07-03-kind-status-events-validation.rows.csv]]
- [[_report/quant/research/2026-07-03-kind-status-replay-on-openapi-20250102-20250124|_report/quant/research/2026-07-03-kind-status-replay-on-openapi-20250102-20250124.md]]
- [[_report/quant/research/2026-07-03-kind-status-replay-on-openapi-20250102-20250124.rows.csv|_report/quant/research/2026-07-03-kind-status-replay-on-openapi-20250102-20250124.rows.csv]]
- [[scripts/quant_point_in_time_status_events_enrich_market.py|scripts/quant_point_in_time_status_events_enrich_market.py]]
- [[tests/test_quant_point_in_time_status_events_enrich_market.py|tests/test_quant_point_in_time_status_events_enrich_market.py]]
- [[_report/quant/data/point_in_time_status_events/2026-07-03-kind-current-status-events.market-enriched.csv|_report/quant/data/point_in_time_status_events/2026-07-03-kind-current-status-events.market-enriched.csv]]
- [[_report/quant/research/2026-07-03-kind-status-events-market-enrich|_report/quant/research/2026-07-03-kind-status-events-market-enrich.md]]
- [[_report/quant/research/2026-07-03-kind-status-events-market-enriched-validation|_report/quant/research/2026-07-03-kind-status-events-market-enriched-validation.md]]
- [[_report/quant/research/2026-07-03-kind-status-events-market-enriched-validation.rows.csv|_report/quant/research/2026-07-03-kind-status-events-market-enriched-validation.rows.csv]]
- [[scripts/quant_point_in_time_universe_build.py|scripts/quant_point_in_time_universe_build.py]]
- [[tests/test_quant_point_in_time_universe_build.py|tests/test_quant_point_in_time_universe_build.py]]
- [[_report/quant/research/2026-07-03-kind-status-point-in-time-universe-smoke-20250102-20250124|_report/quant/research/2026-07-03-kind-status-point-in-time-universe-smoke-20250102-20250124.md]]
- [[_report/quant/research/2026-07-03-kind-status-point-in-time-universe-smoke-20250102-20250124.rows.csv|_report/quant/research/2026-07-03-kind-status-point-in-time-universe-smoke-20250102-20250124.rows.csv]]
- [[_report/quant/research/2026-07-04-kind-status-replay-on-openapi-20250102-20250207|_report/quant/research/2026-07-04-kind-status-replay-on-openapi-20250102-20250207.md]]
- [[_report/quant/research/2026-07-04-kind-status-replay-on-openapi-20250102-20250207.rows.csv|_report/quant/research/2026-07-04-kind-status-replay-on-openapi-20250102-20250207.rows.csv]]
- [[_report/quant/research/2026-07-04-kind-status-point-in-time-universe-smoke-20250102-20250207|_report/quant/research/2026-07-04-kind-status-point-in-time-universe-smoke-20250102-20250207.md]]
- [[_report/quant/research/2026-07-04-kind-status-point-in-time-universe-smoke-20250102-20250207.rows.csv|_report/quant/research/2026-07-04-kind-status-point-in-time-universe-smoke-20250102-20250207.rows.csv]]
- [[scripts/quant_point_in_time_liquidity_filter.py|scripts/quant_point_in_time_liquidity_filter.py]]
- [[tests/test_quant_point_in_time_liquidity_filter.py|tests/test_quant_point_in_time_liquidity_filter.py]]
- [[_report/quant/research/2026-07-04-kind-status-point-in-time-liquidity-smoke-20250102-20250124|_report/quant/research/2026-07-04-kind-status-point-in-time-liquidity-smoke-20250102-20250124.md]]
- [[_report/quant/research/2026-07-04-kind-status-point-in-time-liquidity-smoke-20250102-20250124.rows.csv|_report/quant/research/2026-07-04-kind-status-point-in-time-liquidity-smoke-20250102-20250124.rows.csv]]
- [[_report/quant/research/2026-07-04-kind-status-point-in-time-liquidity-smoke-20d-20250102-20250207|_report/quant/research/2026-07-04-kind-status-point-in-time-liquidity-smoke-20d-20250102-20250207.md]]
- [[_report/quant/research/2026-07-04-kind-status-point-in-time-liquidity-smoke-20d-20250102-20250207.rows.csv|_report/quant/research/2026-07-04-kind-status-point-in-time-liquidity-smoke-20d-20250102-20250207.rows.csv]]
- [[scripts/quant_point_in_time_signal_candidates.py|scripts/quant_point_in_time_signal_candidates.py]]
- [[tests/test_quant_point_in_time_signal_candidates.py|tests/test_quant_point_in_time_signal_candidates.py]]
- [[_report/quant/research/2026-07-04-kind-status-point-in-time-momentum-signal-candidates-smoke-20250102-20250124|_report/quant/research/2026-07-04-kind-status-point-in-time-momentum-signal-candidates-smoke-20250102-20250124.md]]
- [[_report/quant/research/2026-07-04-kind-status-point-in-time-momentum-signal-candidates-smoke-20250102-20250124.rows.csv|_report/quant/research/2026-07-04-kind-status-point-in-time-momentum-signal-candidates-smoke-20250102-20250124.rows.csv]]
- [[scripts/quant_kis_demo_order_preflight.py|scripts/quant_kis_demo_order_preflight.py]]
- [[tests/test_quant_kis_demo_order_preflight.py|tests/test_quant_kis_demo_order_preflight.py]]
- [[scripts/quant_kis_demo_account_preflight.py|scripts/quant_kis_demo_account_preflight.py]]
- [[tests/test_quant_kis_demo_account_preflight.py|tests/test_quant_kis_demo_account_preflight.py]]
- [[_report/quant/research/2026-07-03-kis-demo-trading-readiness|_report/quant/research/2026-07-03-kis-demo-trading-readiness.md]]
- [[_report/quant/research/2026-07-04-kis-demo-account-preflight|_report/quant/research/2026-07-04-kis-demo-account-preflight.md]]
- [[scripts/quant_liquidity_filter.py|scripts/quant_liquidity_filter.py]]
- [[tests/test_quant_liquidity_filter.py|tests/test_quant_liquidity_filter.py]]
- [[scripts/quant_kis_ohlcv_batch_plan.py|scripts/quant_kis_ohlcv_batch_plan.py]]
- [[tests/test_quant_kis_ohlcv_batch_plan.py|tests/test_quant_kis_ohlcv_batch_plan.py]]
- [[scripts/quant_kis_ohlcv_capture.py|scripts/quant_kis_ohlcv_capture.py]]
- [[tests/test_quant_kis_ohlcv_capture.py|tests/test_quant_kis_ohlcv_capture.py]]
- [[_report/quant/research/2026-06-14-krx-current-universe-v0-liquidity-smoke|_report/quant/research/2026-06-14-krx-current-universe-v0-liquidity-smoke.md]]
- [[_report/quant/research/2026-06-14-krx-current-universe-v0-liquidity-smoke.rows.csv|_report/quant/research/2026-06-14-krx-current-universe-v0-liquidity-smoke.rows.csv]]
- [[_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-batch-plan|_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-batch-plan.md]]
- [[_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-batch-plan.requests.jsonl|_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-batch-plan.requests.jsonl]]
- [[_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-batch-plan-next10|_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-batch-plan-next10.md]]
- [[_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-batch-plan-next10.requests.jsonl|_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-batch-plan-next10.requests.jsonl]]
- [[_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-capture-dry-run|_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-capture-dry-run.md]]
- [[_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-capture-result|_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-capture-result.md]]
- [[_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-capture-dry-run-next10|_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-capture-dry-run-next10.md]]
- [[_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-capture-result-next10|_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-capture-result-next10.md]]
- [[_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-capture-validator-result|_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-capture-validator-result.md]]
- [[_report/quant/research/2026-06-15-krx-current-universe-v0-liquidity-smoke-expanded|_report/quant/research/2026-06-15-krx-current-universe-v0-liquidity-smoke-expanded.md]]
- [[_report/quant/research/2026-06-15-krx-current-universe-v0-liquidity-smoke-expanded.rows.csv|_report/quant/research/2026-06-15-krx-current-universe-v0-liquidity-smoke-expanded.rows.csv]]
- [[_report/quant/research/2026-06-16-quant-pipeline-gap-prep-list|_report/quant/research/2026-06-16-quant-pipeline-gap-prep-list.md]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-third10|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-third10.md]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-third10.requests.jsonl|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-third10.requests.jsonl]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-dry-run-third10|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-dry-run-third10.md]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-result-third10|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-result-third10.md]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-validator-result-third10|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-validator-result-third10.md]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-liquidity-smoke-expanded-third10|_report/quant/research/2026-06-17-krx-current-universe-v0-liquidity-smoke-expanded-third10.md]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-liquidity-smoke-expanded-third10.rows.csv|_report/quant/research/2026-06-17-krx-current-universe-v0-liquidity-smoke-expanded-third10.rows.csv]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-fourth10|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-fourth10.md]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-fourth10.requests.jsonl|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-fourth10.requests.jsonl]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-dry-run-fourth10|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-dry-run-fourth10.md]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-result-fourth10|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-result-fourth10.md]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-validator-result-fourth10|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-validator-result-fourth10.md]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-liquidity-smoke-expanded-fourth10|_report/quant/research/2026-06-17-krx-current-universe-v0-liquidity-smoke-expanded-fourth10.md]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-liquidity-smoke-expanded-fourth10.rows.csv|_report/quant/research/2026-06-17-krx-current-universe-v0-liquidity-smoke-expanded-fourth10.rows.csv]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-fifth10|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-fifth10.md]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-fifth10.requests.jsonl|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-fifth10.requests.jsonl]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-dry-run-fifth10|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-dry-run-fifth10.md]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-result-fifth10|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-result-fifth10.md]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-sixth10|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-sixth10.md]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-sixth10.requests.jsonl|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-sixth10.requests.jsonl]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-dry-run-sixth10|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-dry-run-sixth10.md]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-result-sixth10|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-result-sixth10.md]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-seventh10|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-seventh10.md]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-seventh10.requests.jsonl|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-seventh10.requests.jsonl]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-dry-run-seventh10|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-dry-run-seventh10.md]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-result-seventh10|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-result-seventh10.md]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-validator-result-seventh10|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-validator-result-seventh10.md]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-liquidity-smoke-expanded-seventh10|_report/quant/research/2026-06-17-krx-current-universe-v0-liquidity-smoke-expanded-seventh10.md]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-liquidity-smoke-expanded-seventh10.rows.csv|_report/quant/research/2026-06-17-krx-current-universe-v0-liquidity-smoke-expanded-seventh10.rows.csv]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-eighth10|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-eighth10.md]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-eighth10.requests.jsonl|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-eighth10.requests.jsonl]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-dry-run-eighth10|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-dry-run-eighth10.md]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-result-eighth10|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-result-eighth10.md]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-ninth10|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-ninth10.md]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-ninth10.requests.jsonl|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-ninth10.requests.jsonl]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-dry-run-ninth10|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-dry-run-ninth10.md]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-result-ninth10|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-result-ninth10.md]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-tenth10|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-tenth10.md]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-tenth10.requests.jsonl|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-tenth10.requests.jsonl]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-dry-run-tenth10|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-dry-run-tenth10.md]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-result-tenth10|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-result-tenth10.md]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-validator-result-tenth10|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-validator-result-tenth10.md]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-liquidity-smoke-expanded-tenth10|_report/quant/research/2026-06-17-krx-current-universe-v0-liquidity-smoke-expanded-tenth10.md]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-liquidity-smoke-expanded-tenth10.rows.csv|_report/quant/research/2026-06-17-krx-current-universe-v0-liquidity-smoke-expanded-tenth10.rows.csv]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-eleventh10|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-eleventh10.md]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-eleventh10.requests.jsonl|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-eleventh10.requests.jsonl]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-dry-run-eleventh10|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-dry-run-eleventh10.md]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-result-eleventh10|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-result-eleventh10.md]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-twelfth10|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-twelfth10.md]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-twelfth10.requests.jsonl|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-twelfth10.requests.jsonl]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-dry-run-twelfth10|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-dry-run-twelfth10.md]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-result-twelfth10|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-result-twelfth10.md]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-thirteenth10|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-thirteenth10.md]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-thirteenth10.requests.jsonl|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-thirteenth10.requests.jsonl]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-dry-run-thirteenth10|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-dry-run-thirteenth10.md]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-result-thirteenth10|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-result-thirteenth10.md]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-validator-result-thirteenth10|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-validator-result-thirteenth10.md]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-liquidity-smoke-expanded-thirteenth10|_report/quant/research/2026-06-17-krx-current-universe-v0-liquidity-smoke-expanded-thirteenth10.md]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-liquidity-smoke-expanded-thirteenth10.rows.csv|_report/quant/research/2026-06-17-krx-current-universe-v0-liquidity-smoke-expanded-thirteenth10.rows.csv]]
- [[_report/quant/research/2026-06-18-krx-current-universe-v0-ohlcv-batch-plan-fourteenth10|_report/quant/research/2026-06-18-krx-current-universe-v0-ohlcv-batch-plan-fourteenth10.md]]
- [[_report/quant/research/2026-06-18-krx-current-universe-v0-ohlcv-batch-plan-fourteenth10.requests.jsonl|_report/quant/research/2026-06-18-krx-current-universe-v0-ohlcv-batch-plan-fourteenth10.requests.jsonl]]
- [[_report/quant/research/2026-06-18-krx-current-universe-v0-ohlcv-capture-dry-run-fourteenth10|_report/quant/research/2026-06-18-krx-current-universe-v0-ohlcv-capture-dry-run-fourteenth10.md]]
- [[_report/quant/research/2026-06-18-krx-current-universe-v0-ohlcv-capture-result-fourteenth10|_report/quant/research/2026-06-18-krx-current-universe-v0-ohlcv-capture-result-fourteenth10.md]]
- [[_report/quant/research/2026-06-18-krx-current-universe-v0-ohlcv-batch-plan-fifteenth10|_report/quant/research/2026-06-18-krx-current-universe-v0-ohlcv-batch-plan-fifteenth10.md]]
- [[_report/quant/research/2026-06-18-krx-current-universe-v0-ohlcv-batch-plan-fifteenth10.requests.jsonl|_report/quant/research/2026-06-18-krx-current-universe-v0-ohlcv-batch-plan-fifteenth10.requests.jsonl]]
- [[_report/quant/research/2026-06-18-krx-current-universe-v0-ohlcv-capture-dry-run-fifteenth10|_report/quant/research/2026-06-18-krx-current-universe-v0-ohlcv-capture-dry-run-fifteenth10.md]]
- [[_report/quant/research/2026-06-18-krx-current-universe-v0-ohlcv-capture-result-fifteenth10|_report/quant/research/2026-06-18-krx-current-universe-v0-ohlcv-capture-result-fifteenth10.md]]
- [[_report/quant/research/2026-06-18-krx-current-universe-v0-ohlcv-batch-plan-sixteenth10|_report/quant/research/2026-06-18-krx-current-universe-v0-ohlcv-batch-plan-sixteenth10.md]]
- [[_report/quant/research/2026-06-18-krx-current-universe-v0-ohlcv-batch-plan-sixteenth10.requests.jsonl|_report/quant/research/2026-06-18-krx-current-universe-v0-ohlcv-batch-plan-sixteenth10.requests.jsonl]]
- [[_report/quant/research/2026-06-18-krx-current-universe-v0-ohlcv-capture-dry-run-sixteenth10|_report/quant/research/2026-06-18-krx-current-universe-v0-ohlcv-capture-dry-run-sixteenth10.md]]
- [[_report/quant/research/2026-06-18-krx-current-universe-v0-ohlcv-capture-result-sixteenth10|_report/quant/research/2026-06-18-krx-current-universe-v0-ohlcv-capture-result-sixteenth10.md]]
- [[_report/quant/research/2026-06-18-krx-current-universe-v0-ohlcv-capture-validator-result-sixteenth10|_report/quant/research/2026-06-18-krx-current-universe-v0-ohlcv-capture-validator-result-sixteenth10.md]]
- [[_report/quant/research/2026-06-18-krx-current-universe-v0-liquidity-smoke-expanded-sixteenth10|_report/quant/research/2026-06-18-krx-current-universe-v0-liquidity-smoke-expanded-sixteenth10.md]]
- [[_report/quant/research/2026-06-18-krx-current-universe-v0-liquidity-smoke-expanded-sixteenth10.rows.csv|_report/quant/research/2026-06-18-krx-current-universe-v0-liquidity-smoke-expanded-sixteenth10.rows.csv]]
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-seventeenth10|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-seventeenth10.md]]
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-seventeenth10.requests.jsonl|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-seventeenth10.requests.jsonl]]
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-dry-run-seventeenth10|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-dry-run-seventeenth10.md]]
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-result-seventeenth10|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-result-seventeenth10.md]]
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-eighteenth10|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-eighteenth10.md]]
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-eighteenth10.requests.jsonl|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-eighteenth10.requests.jsonl]]
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-dry-run-eighteenth10|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-dry-run-eighteenth10.md]]
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-result-eighteenth10|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-result-eighteenth10.md]]
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-nineteenth10|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-nineteenth10.md]]
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-nineteenth10.requests.jsonl|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-nineteenth10.requests.jsonl]]
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-dry-run-nineteenth10|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-dry-run-nineteenth10.md]]
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-result-nineteenth10|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-result-nineteenth10.md]]
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-validator-result-nineteenth10|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-validator-result-nineteenth10.md]]
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-liquidity-smoke-expanded-nineteenth10|_report/quant/research/2026-06-30-krx-current-universe-v0-liquidity-smoke-expanded-nineteenth10.md]]
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-liquidity-smoke-expanded-nineteenth10.rows.csv|_report/quant/research/2026-06-30-krx-current-universe-v0-liquidity-smoke-expanded-nineteenth10.rows.csv]]
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentieth10|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentieth10.md]]
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentieth10.requests.jsonl|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentieth10.requests.jsonl]]
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-dry-run-twentieth10|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-dry-run-twentieth10.md]]
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-result-twentieth10|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-result-twentieth10.md]]
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyfirst10|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyfirst10.md]]
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyfirst10.requests.jsonl|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyfirst10.requests.jsonl]]
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-dry-run-twentyfirst10|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-dry-run-twentyfirst10.md]]
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-result-twentyfirst10|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-result-twentyfirst10.md]]
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentysecond10|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentysecond10.md]]
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentysecond10.requests.jsonl|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentysecond10.requests.jsonl]]
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-dry-run-twentysecond10|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-dry-run-twentysecond10.md]]
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-result-twentysecond10|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-result-twentysecond10.md]]
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentythird10|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentythird10.md]]
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentythird10.requests.jsonl|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentythird10.requests.jsonl]]
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-dry-run-twentythird10|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-dry-run-twentythird10.md]]
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-result-twentythird10|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-result-twentythird10.md]]
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyfourth10|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyfourth10.md]]
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyfourth10.requests.jsonl|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyfourth10.requests.jsonl]]
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-dry-run-twentyfourth10|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-dry-run-twentyfourth10.md]]
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-result-twentyfourth10|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-result-twentyfourth10.md]]
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-validator-result-twentyfourth10|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-validator-result-twentyfourth10.md]]
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-liquidity-smoke-expanded-twentyfourth10|_report/quant/research/2026-06-30-krx-current-universe-v0-liquidity-smoke-expanded-twentyfourth10.md]]
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-liquidity-smoke-expanded-twentyfourth10.rows.csv|_report/quant/research/2026-06-30-krx-current-universe-v0-liquidity-smoke-expanded-twentyfourth10.rows.csv]]
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyfifth10|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyfifth10.md]]
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyfifth10.requests.jsonl|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyfifth10.requests.jsonl]]
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-dry-run-twentyfifth10|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-dry-run-twentyfifth10.md]]
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-result-twentyfifth10|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-result-twentyfifth10.md]]
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentysixth10|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentysixth10.md]]
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentysixth10.requests.jsonl|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentysixth10.requests.jsonl]]
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-dry-run-twentysixth10|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-dry-run-twentysixth10.md]]
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-result-twentysixth10|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-result-twentysixth10.md]]
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyseventh10|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyseventh10.md]]
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyseventh10.requests.jsonl|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyseventh10.requests.jsonl]]
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-dry-run-twentyseventh10|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-dry-run-twentyseventh10.md]]
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-result-twentyseventh10|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-result-twentyseventh10.md]]
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyeighth10|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyeighth10.md]]
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyeighth10.requests.jsonl|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyeighth10.requests.jsonl]]
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-dry-run-twentyeighth10|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-dry-run-twentyeighth10.md]]
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-result-twentyeighth10|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-result-twentyeighth10.md]]
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyninth10|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyninth10.md]]
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyninth10.requests.jsonl|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyninth10.requests.jsonl]]
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-dry-run-twentyninth10|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-dry-run-twentyninth10.md]]
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-result-twentyninth10|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-result-twentyninth10.md]]
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-validator-result-twentyninth10|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-validator-result-twentyninth10.md]]
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-liquidity-smoke-expanded-twentyninth10|_report/quant/research/2026-06-30-krx-current-universe-v0-liquidity-smoke-expanded-twentyninth10.md]]
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-liquidity-smoke-expanded-twentyninth10.rows.csv|_report/quant/research/2026-06-30-krx-current-universe-v0-liquidity-smoke-expanded-twentyninth10.rows.csv]]
- [[_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtieth10|_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtieth10.md]]
- [[_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtieth10.requests.jsonl|_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtieth10.requests.jsonl]]
- [[_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-capture-dry-run-thirtieth10|_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-capture-dry-run-thirtieth10.md]]
- [[_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-capture-result-thirtieth10|_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-capture-result-thirtieth10.md]]
- [[_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-capture-validator-result-thirtieth10|_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-capture-validator-result-thirtieth10.md]]
- [[_report/quant/research/2026-07-01-krx-current-universe-v0-liquidity-smoke-expanded-thirtieth10|_report/quant/research/2026-07-01-krx-current-universe-v0-liquidity-smoke-expanded-thirtieth10.md]]
- [[_report/quant/research/2026-07-01-krx-current-universe-v0-liquidity-smoke-expanded-thirtieth10.rows.csv|_report/quant/research/2026-07-01-krx-current-universe-v0-liquidity-smoke-expanded-thirtieth10.rows.csv]]
- [[_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtyfirst10|_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtyfirst10.md]]
- [[_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtyfirst10.requests.jsonl|_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtyfirst10.requests.jsonl]]
- [[_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-capture-dry-run-thirtyfirst10|_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-capture-dry-run-thirtyfirst10.md]]
- [[_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-capture-result-thirtyfirst10|_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-capture-result-thirtyfirst10.md]]
- [[_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtysecond10|_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtysecond10.md]]
- [[_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtysecond10.requests.jsonl|_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtysecond10.requests.jsonl]]
- [[_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-capture-dry-run-thirtysecond10|_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-capture-dry-run-thirtysecond10.md]]
- [[_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-capture-result-thirtysecond10|_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-capture-result-thirtysecond10.md]]
- [[_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtythird10|_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtythird10.md]]
- [[_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtythird10.requests.jsonl|_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtythird10.requests.jsonl]]
- [[_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-capture-dry-run-thirtythird10|_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-capture-dry-run-thirtythird10.md]]
- [[_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-capture-result-thirtythird10|_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-capture-result-thirtythird10.md]]
- [[_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtyfourth10|_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtyfourth10.md]]
- [[_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtyfourth10.requests.jsonl|_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtyfourth10.requests.jsonl]]
- [[_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-capture-dry-run-thirtyfourth10|_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-capture-dry-run-thirtyfourth10.md]]
- [[_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-capture-result-thirtyfourth10|_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-capture-result-thirtyfourth10.md]]
- [[_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtyfifth10|_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtyfifth10.md]]
- [[_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtyfifth10.requests.jsonl|_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtyfifth10.requests.jsonl]]
- [[_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-capture-dry-run-thirtyfifth10|_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-capture-dry-run-thirtyfifth10.md]]
- [[_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-capture-result-thirtyfifth10|_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-capture-result-thirtyfifth10.md]]
- [[_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-capture-validator-result-thirtyfifth10|_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-capture-validator-result-thirtyfifth10.md]]
- [[_report/quant/research/2026-07-01-krx-current-universe-v0-liquidity-smoke-expanded-thirtyfifth10|_report/quant/research/2026-07-01-krx-current-universe-v0-liquidity-smoke-expanded-thirtyfifth10.md]]
- [[_report/quant/research/2026-07-01-krx-current-universe-v0-liquidity-smoke-expanded-thirtyfifth10.rows.csv|_report/quant/research/2026-07-01-krx-current-universe-v0-liquidity-smoke-expanded-thirtyfifth10.rows.csv]]
- [[_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtysixth10|_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtysixth10.md]]
- [[_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtysixth10.requests.jsonl|_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtysixth10.requests.jsonl]]
- [[_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-capture-dry-run-thirtysixth10|_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-capture-dry-run-thirtysixth10.md]]
- [[_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-capture-result-thirtysixth10|_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-capture-result-thirtysixth10.md]]
- [[_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-capture-validator-result-thirtysixth10|_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-capture-validator-result-thirtysixth10.md]]
- [[_report/quant/research/2026-07-01-krx-current-universe-v0-liquidity-smoke-expanded-thirtysixth10|_report/quant/research/2026-07-01-krx-current-universe-v0-liquidity-smoke-expanded-thirtysixth10.md]]
- [[_report/quant/research/2026-07-01-krx-current-universe-v0-liquidity-smoke-expanded-thirtysixth10.rows.csv|_report/quant/research/2026-07-01-krx-current-universe-v0-liquidity-smoke-expanded-thirtysixth10.rows.csv]]
- [[_report/quant/research/2026-07-01-user-action-items-temp|_report/quant/research/2026-07-01-user-action-items-temp.md]]
- Target rule: `avg_trading_value_20d_krw >= 1,000,000,000`
- Saved raw coverage currently evaluates 361 unique rows. `180` pass and `181` fail the threshold.
- `2029` base-included rows are `liquidity_raw_missing`, which means raw coverage is missing, not that those stocks are illiquid.
- First OHLCV batch dry-run selected `10` requests from generated Universe `include` rows.
- First OHLCV direct capture saved 10 raw files under `_report/raw/2026/2026-06-15/quant/universe-ohlcv/`.
- Second OHLCV batch dry-run selected the next `10` requests after skipping existing raw.
- Second OHLCV direct capture saved 10 more raw files under `_report/raw/2026/2026-06-15/quant/universe-ohlcv/`.
- Third OHLCV batch dry-run selected the next `10` requests after skipping `20` existing raw files.
- Third OHLCV direct capture saved 10 more raw files under `_report/raw/2026/2026-06-15/quant/universe-ohlcv/`; the directory now has `30` Universe raw files.
- Fourth OHLCV batch dry-run selected the next `10` requests after skipping `30` existing raw files.
- Fourth OHLCV direct capture saved 10 more raw files under `_report/raw/2026/2026-06-15/quant/universe-ohlcv/`; the directory then had `40` Universe raw files. `000660 SK하이닉스` overlaps with an older paper-follow-up raw row, so the then-current Liquidity Filter had `42` unique evaluated rows, not `43`.
- Fifth, sixth, and seventh OHLCV batch dry-runs selected three additional `10` request queues after skipping `40`, `50`, and `60` existing raw files.
- Fifth, sixth, and seventh direct captures saved `30` more raw files under `_report/raw/2026/2026-06-15/quant/universe-ohlcv/`; the directory then had `70` Universe raw files. Because `000660 SK하이닉스` overlaps with an older paper-follow-up raw row, the then-current Liquidity Filter had `72` unique evaluated rows, not `73`.
- Eighth, ninth, and tenth OHLCV batch dry-runs selected three additional `10` request queues after skipping `70`, `80`, and `90` existing raw files.
- Eighth, ninth, and tenth direct captures saved `30` more raw files under `_report/raw/2026/2026-06-15/quant/universe-ohlcv/`; the directory then had `100` Universe raw files. Because `000660 SK하이닉스` overlaps with an older paper-follow-up raw row, the then-current Liquidity Filter had `102` unique evaluated rows, not `103`.
- Eleventh, twelfth, and thirteenth OHLCV batch dry-runs selected three additional `10` request queues after skipping `100`, `110`, and `120` existing raw files.
- Eleventh, twelfth, and thirteenth direct captures saved `30` more raw files under `_report/raw/2026/2026-06-15/quant/universe-ohlcv/`; the directory then had `130` Universe raw files. Because `000660 SK하이닉스` overlaps with an older paper-follow-up raw row, the then-current Liquidity Filter had `132` unique evaluated rows, not `133`.
- Fourteenth, fifteenth, and sixteenth OHLCV batch dry-runs selected three additional `10` request queues after skipping `130`, `140`, and `150` existing raw files.
- Fourteenth, fifteenth, and sixteenth direct captures saved `30` more raw files under `_report/raw/2026/2026-06-15/quant/universe-ohlcv/`; the directory then had `160` Universe raw files. Because `000660 SK하이닉스` overlaps with an older paper-follow-up raw row, the then-current Liquidity Filter had `162` unique evaluated rows, not `163`.
- Seventeenth, eighteenth, and nineteenth OHLCV batch dry-runs selected three additional `10` request queues after skipping `160`, `170`, and `180` existing raw files.
- Seventeenth, eighteenth, and nineteenth direct captures saved `30` more raw files under `_report/raw/2026/2026-06-15/quant/universe-ohlcv/`; the directory then had `190` Universe raw files. Because `000660 SK하이닉스` overlaps with an older paper-follow-up raw row, the then-current Liquidity Filter had `192` unique evaluated rows, not `193`.
- Twentieth through twentyfourth OHLCV batch dry-runs selected five additional `10` request queues after skipping `190`, `200`, `210`, `220`, and `230` existing raw files.
- Twentieth through twentyfourth direct captures saved `50` more raw files under `_report/raw/2026/2026-06-15/quant/universe-ohlcv/`; the directory then had `240` Universe raw files. Because `000660 SK하이닉스` overlaps with an older paper-follow-up raw row, the then-current Liquidity Filter had `242` unique evaluated rows, not `243`.
- Twentyfifth through twentyninth OHLCV batch dry-runs selected five additional `10` request queues after skipping `240`, `250`, `260`, `270`, and `280` existing raw files.
- Twentyfifth through twentyninth direct captures saved `50` more raw files under `_report/raw/2026/2026-06-15/quant/universe-ohlcv/`; the directory then had `290` Universe raw files. Because `000660 SK하이닉스` and `005930 삼성전자` overlap with older paper-follow-up raw rows while `035420 NAVER` remains extra, the then-current Liquidity Filter had `291` unique evaluated rows.
- Thirtieth OHLCV batch dry-run selected one additional `10` request queue after skipping `290` existing raw files.
- Thirtieth direct capture saved `10` more raw files under `_report/raw/2026/2026-06-15/quant/universe-ohlcv/`; the directory then had `300` Universe raw files. Because `000660 SK하이닉스` and `005930 삼성전자` overlap with older paper-follow-up raw rows while `035420 NAVER` remains extra, the then-current Liquidity Filter had `301` unique evaluated rows.
- Thirtyfirst through thirtyfifth OHLCV batch dry-runs selected five additional `10` request queues after skipping `300`, `310`, `320`, `330`, and `340` existing raw files.
- Thirtyfirst through thirtyfifth direct captures saved `50` more raw files under `_report/raw/2026/2026-06-15/quant/universe-ohlcv/`; the directory then had `350` Universe raw files. Because `000660 SK하이닉스` and `005930 삼성전자` overlap with older paper-follow-up raw rows while `035420 NAVER` remains extra, the then-current Liquidity Filter had `351` unique evaluated rows.
- Thirtysixth OHLCV batch dry-run selected one additional `10` request queue after skipping `350` existing raw files.
- Thirtysixth direct capture saved `10` more raw files under `_report/raw/2026/2026-06-15/quant/universe-ohlcv/`; the directory now has `360` Universe raw files. Because `000660 SK하이닉스` and `005930 삼성전자` overlap with older paper-follow-up raw rows while `035420 NAVER` remains extra, the latest Liquidity Filter has `361` unique evaluated rows.
- KRX OpenAPI core collector smoke-tested `2025-01-02` and saved raw files under `_report/raw/2026/2026-07-03/krx/openapi/`. Row counts: `kospi_stock_daily=961`, `kosdaq_stock_daily=1784`, `kospi_issue_base=961`, `kosdaq_issue_base=1784`, `kospi_index_daily=51`, `kosdaq_index_daily=40`.
- KRX OpenAPI normalizer smoke-tested the saved `2025-01-02` raws into three tables: `stock_daily=2745`, `issue_base=2745`, `index_daily=91`.
- KRX OpenAPI history plan smoke-tested `2025-01-02` to `2025-01-10`: `7` weekday candidate dates, `1` complete date, `6` existing raw files, and `36` missing requests.
- KRX OpenAPI history collection executed the `36` missing read-only requests; the same range now has `7` complete dates, `42` saved raw files, and `0` missing requests.
- KRX OpenAPI history normalization over `2025-01-02` to `2025-01-10` produced `stock_daily=19212`, `issue_base=19212`, and `index_daily=637` rows.
- KRX OpenAPI continuity audit over that normalized window passed with `7` audited dates, `0` row-count alerts, `0` duplicate date/code keys, and `0` stock/issue code mismatches. The only row movement was a `-1` KOSDAQ stock/issue row delta on `2025-01-08`.
- KRX OpenAPI market-data join over that initial window produced `19212` joined rows with `0` stock/issue mismatches: `6727` KOSPI rows and `12485` KOSDAQ rows.
- KRX OpenAPI extended history plan for `2025-01-13` to `2025-01-24` started with `10` candidate dates and `60` missing requests, then collection completed all `60` read-only requests with `0` missing requests.
- KRX OpenAPI extended normalization over `2025-01-13` to `2025-01-24` produced `stock_daily=27447`, `issue_base=27447`, and `index_daily=910` rows.
- KRX OpenAPI combined normalization over `2025-01-02` to `2025-01-24` produced `stock_daily=46659`, `issue_base=46659`, and `index_daily=1547` rows.
- KRX OpenAPI combined continuity audit over the 17-date window passed with `0` row-count alerts, `0` duplicate date/code keys, and `0` stock/issue code mismatches.
- KRX OpenAPI combined market-data join over the 17-date window produced `46659` joined rows with `0` stock/issue mismatches: `16337` KOSPI rows and `30322` KOSDAQ rows.
- KRX OpenAPI history collection was extended over `2025-01-27` to `2025-02-07`; `60` read-only raw requests completed with `0` missing requests. `2025-01-27` through `2025-01-30` had issue-base rows but no stock-daily/index rows, so the join drops those issue-only dates as non-trading-date evidence.
- KRX OpenAPI market-data merge over `2025-01-02` to `2025-02-07` produced `63165` joined rows across `23` trading dates: `22106` KOSPI rows and `41059` KOSDAQ rows.
- Point-in-Time status source gap is documented: KRX OpenAPI handles market data, while historical status replay still needs broader KRX Data Marketplace and/or KIND coverage.
- Point-in-Time status-event schema/config scaffolding and validator are implemented; one KIND current snapshot normalized into `344` valid rows with `0` invalid rows.
- Point-in-Time status replay scaffold is implemented; the KIND current snapshot replay marked `382/63165` 23-date KRX OpenAPI market-data rows as `exclude_by_status_event`.
- Point-in-Time status-event market enrichment is implemented; `310/344` KIND event rows resolved from the 17-date market-data join and `34` remain `UNKNOWN`.
- Point-in-Time Universe smoke is implemented; 23-date replayed market-data rows produced `58961` include and `4204` exclude rows.
- Point-in-Time Liquidity Filter smoke is implemented; 23-date replayed market-data rows with a 20-day rule produced `4034` include and `59131` exclude rows, with `10236` rows evaluated on the full 20-day lookback.
- Point-in-Time Momentum Signal Candidate smoke is implemented; 17-date, 5-day Momentum over the Liquidity rows produced `480` paper-only candidates across `12` candidate dates: `240` BUY candidates and `240` SELL candidates. This is not a Backtest result and does not generate order intents.
- KIS demo order intent preflight and local demo account preflight are implemented. The latest local MCP `.env.kis` check found `KIS_PAPER_STOCK` empty without printing or storing account values. Controlled first KIS demo order estimate remains `3-7 working days` after local demo auth/account verification; Quant-pipeline-driven demo trading estimate is `3-6 weeks`.
- KRX Data Marketplace status-source probe is implemented; it found the official status screen `bld` values but all core unattended JSON probes returned `auth_required`/`LOGOUT`.
- KIND public fallback probe is implemented; `6/7` status-source downloads produced usable table snapshots without login, but the result is still current-snapshot evidence, not full historical coverage.
- KRX OpenAPI `2026-07-02` smoke returned HTTP `200` but `0` rows for all six core services, so use known historical trading days for parser development until latest-date availability is confirmed.
- Current Codex App surface did not expose the KIS MCP tool, so `find_api_detail` was not callable here. Local [[MCP/Kis Trading MCP/configs/domestic_stock.json|MCP/Kis Trading MCP/configs/domestic_stock.json]] and `examples_llm` sample docs were used as the fallback API detail evidence, and only the read-only quotation endpoint was called.

Likely needed work:

1. Preserve `2025-01-08` row-count movement as an event-validation item, not as a Backtest conclusion.
2. Extend KIND or authenticated/manual KRX status coverage across the selected historical date range.
3. Resolve the remaining `34` `UNKNOWN` KIND market rows only where an official source or deterministic join can support it.
4. Re-run [[scripts/quant_point_in_time_status_events_validate.py|scripts/quant_point_in_time_status_events_validate.py]], [[scripts/quant_point_in_time_status_replay.py|scripts/quant_point_in_time_status_replay.py]], [[scripts/quant_point_in_time_universe_build.py|scripts/quant_point_in_time_universe_build.py]], and [[scripts/quant_point_in_time_liquidity_filter.py|scripts/quant_point_in_time_liquidity_filter.py]] on the expanded event/date set.
5. Continue KIS OHLCV batch capture only as secondary cross-check or to fill fields KRX OpenAPI does not provide.
6. After the user fills `KIS_PAPER_STOCK` in the ignored MCP `.env.kis`, rerun [[scripts/quant_kis_demo_account_preflight.py|scripts/quant_kis_demo_account_preflight.py]] before any read-only account API calls.
7. Re-run [[scripts/quant_point_in_time_signal_candidates.py|scripts/quant_point_in_time_signal_candidates.py]] only as paper/smoke after the Universe and Liquidity rows are rebuilt; do not treat its output as orders.
8. Extend the KRX OpenAPI market-data window further before attempting production Momentum lookbacks.
9. Keep result as paper/smoke only until full `Point-in-Time` status replay is solved.

## Current Blockers

- Full generated Universe OHLCV coverage is still incomplete.
- KRX OpenAPI stock daily/basic/index market data is available, but historical managed issue / trading halt / delisting status replay is still incomplete.
- KRX Data Marketplace status JSON is not yet unattended-accessible; probes returned `auth_required` without a login session.
- KIND current snapshot fallback is validated, but it is not full historical `Point-in-Time` coverage.
- KIS demo trading remains blocked beyond local preflight; `KIS_PAPER_STOCK` is empty in the ignored MCP `.env.kis`.
- Backtest remains `hold`.

## User Preferences

- Korean responses.
- Core Quant terms should stay in English, for example `Universe`, `Liquidity Filter`, `Backtest`, `Point-in-Time`.
- When mentioning stocks, include code and company name, for example `005930 Samsung Electronics`.
- Keep DI/Main/Game watchlists separate from Quant.
- Preserve raw evidence under `_report/raw/**`; do not commit raw files.
