# Quant Implementation Status - 2026-06-14

## Summary

- Overall Quant implementation progress: `40-45%`
- Current Snapshot Universe v0 progress: `85-90%`
- Backtest readiness: `hold`
- Live trading readiness: `blocked`
- Current phase: `current_snapshot_universe_v0`

The project is beyond planning and now has a usable current-snapshot Universe artifact, a saved-raw Liquidity Filter smoke artifact, a Universe-based OHLCV request queue, and the first 20 read-only KIS captured Universe rows. It is still not Backtest-ready because `Point-in-Time Universe`, full-Universe OHLCV raw collection, OOS, and Bias Control are incomplete.

## Completed

- Quant work was separated from DI / general investing work.
- Core Quant docs exist under `_report/quant/`.
- Beginner learning roadmap exists: `_report/quant/learning-roadmap.md`.
- Strategy specs exist for:
  - `001-strategy-universe-momentum`
  - `002-strategy-universe-short-term-reversal`
- KRX raw manual snapshot process exists.
- KRX `managed_issues_current.raw.csv` was manually downloaded and verified.
- KRX `listed_issues_current.raw.csv` was manually downloaded and verified.
- Current KRX Universe v0 was generated from listed issues + managed issue exclusions.
- Saved-raw Liquidity Filter smoke was generated from current Universe rows + KIS daily raw files.
- Universe `include` rows were converted into a KIS OHLCV request queue dry-run.
- The first 20 request queue rows were captured through the read-only KIS quotation endpoint using local KIS sample auth fallback because the current Codex App surface did not expose the KIS MCP tool.
- Tests for manifest verification, managed issue extraction, current Universe build, OHLCV batch planning, Liquidity Filter, and calendar audit pass.

## Current Universe v0

Artifacts:

- `_report/quant/research/2026-06-14-krx-current-universe-v0.md`
- `_report/quant/research/2026-06-14-krx-current-universe-v0.rows.csv`
- `_report/quant/research/2026-06-14-krx-current-universe-v0-liquidity-smoke.md`
- `_report/quant/research/2026-06-14-krx-current-universe-v0-liquidity-smoke.rows.csv`
- `_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-batch-plan.md`
- `_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-batch-plan.requests.jsonl`
- `_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-batch-plan-next10.md`
- `_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-batch-plan-next10.requests.jsonl`
- `_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-capture-dry-run.md`
- `_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-capture-result.md`
- `_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-capture-dry-run-next10.md`
- `_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-capture-result-next10.md`
- `_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-capture-validator-result.md`
- `_report/quant/research/2026-06-15-krx-current-universe-v0-liquidity-smoke-expanded.md`
- `_report/quant/research/2026-06-15-krx-current-universe-v0-liquidity-smoke-expanded.rows.csv`
- `_report/quant/research/2026-06-16-quant-pipeline-gap-prep-list.md`
- `scripts/quant_krx_current_universe_build.py`
- `scripts/quant_kis_ohlcv_batch_plan.py`
- `scripts/quant_kis_ohlcv_capture.py`
- `scripts/quant_liquidity_filter.py`
- `tests/test_quant_krx_current_universe_build.py`
- `tests/test_quant_kis_ohlcv_batch_plan.py`
- `tests/test_quant_kis_ohlcv_capture.py`
- `tests/test_quant_liquidity_filter.py`

Current result:

- Total rows: `2875`
- Include: `2390`
- Exclude: `485`
- Duplicate code count: `0`
- `005930 Samsung Electronics`: included
- `121850 코이즈`: excluded by `managed_issue_current`
- `0004V0 엔비알모션`: excluded by `listing_age_calendar_insufficient`
- Expanded Liquidity smoke evaluated rows with saved raw OHLCV: `23`
- Expanded Liquidity smoke pass count: `14`
- Expanded Liquidity smoke fail count: `9`
- Expanded Liquidity smoke `liquidity_raw_missing`: `2367` base-included rows without saved raw OHLCV
- OHLCV batch plan dry-run selected requests: `10`
- OHLCV batch plan first rows: `000020 동화약품`, `000040 KR모터스`, `000050 경방`
- OHLCV next10 batch plan first rows: `000210 DL`, `000220 유유제약`, `000230 일동홀딩스`
- First OHLCV capture result: `9` saved, `1` skipped-existing, raw stored under `_report/raw/2026/2026-06-15/quant/universe-ohlcv/`
- Second OHLCV capture result: `10` saved, raw stored under `_report/raw/2026/2026-06-15/quant/universe-ohlcv/`
- KIS MCP `find_api_detail` status: unavailable in current Codex App surface; local `MCP/Kis Trading MCP/configs/domestic_stock.json` and `examples_llm` sample were used as API detail fallback for read-only direct capture.

Filters currently applied:

- KOSPI/KOSDAQ only.
- Exclude SPAC, REIT, ETF, ETN, ELW, preferred-share-like instruments.
- Exclude current KRX managed issues.
- Apply `365 calendar days` Listing Age guard.
- Apply saved-raw Liquidity Filter smoke for rows with KIS OHLCV raw coverage.

Important caveat:

- Strategy target is `252 trading days` Listing Age, but current artifact uses `365 calendar days` because a full trading-day calendar and historical `Point-in-Time` status data are not yet built.
- Liquidity Filter output is still smoke-only because full generated Universe rows are not connected to OHLCV batch collection.

## Worktree Notes

Check `git status --short` before resuming. Raw KIS responses under `_report/raw/**` are intentionally not committed.

The first-capture implementation files are expected to be tracked after the current work is committed:

- `scripts/quant_kis_ohlcv_capture.py`
- `tests/test_quant_kis_ohlcv_capture.py`
- `_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-capture-*.md`
- `_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-batch-plan-next10*`
- `_report/quant/research/2026-06-15-krx-current-universe-v0-liquidity-smoke-expanded*`
- `_report/quant/research/2026-06-16-quant-pipeline-gap-prep-list.md`

## Verification Already Run

- `uv run python -m unittest discover tests`
- `uv run python -m unittest tests.test_quant_kis_ohlcv_batch_plan`
- `uv run python -m unittest tests.test_quant_kis_ohlcv_capture`
- `uv run python -m py_compile scripts\quant_kis_ohlcv_batch_plan.py tests\test_quant_kis_ohlcv_batch_plan.py`
- `uv run python -m unittest tests.test_quant_liquidity_filter`
- `uv run python -m py_compile scripts\quant_liquidity_filter.py tests\test_quant_liquidity_filter.py`
- `uv run python -m py_compile scripts\quant_krx_current_universe_build.py scripts\quant_krx_managed_issues_extract.py`
- Current Universe sanity checks:
  - `2875` total rows
  - `2390` included rows
  - `485` excluded rows
  - duplicate code count `0`
  - `005930 Samsung Electronics` included
  - `121850 코이즈` excluded
  - `0004V0 엔비알모션` excluded by Listing Age
- Initial Liquidity Filter smoke sanity checks (`2026-06-14` artifact):
  - total rows `2875`
  - base included rows before Liquidity Filter `2390`
  - included rows after saved-raw Liquidity Filter `3`
  - `000660 SK하이닉스`, `005930 삼성전자`, `035420 NAVER` pass
  - `2387` base-included rows are `liquidity_raw_missing`
- OHLCV batch plan sanity checks:
  - total Universe rows `2875`
  - base included rows `2390`
  - selected requests `10`
  - request params include `env_dv`, `fid_cond_mrkt_div_code`, `fid_input_iscd`, `fid_input_date_1`, `fid_input_date_2`, `fid_period_div_code`, `fid_org_adj_prc`
- First OHLCV capture sanity checks:
  - queue validation dry-run selected 10 rows
  - live direct capture recorded `saved` 9 and `skipped_existing` 1
  - validator parsed 10 raw files, each with 71 daily rows and latest date `20260615`
- Second OHLCV capture sanity checks:
  - next10 queue validation dry-run selected 10 rows
  - live direct capture recorded `saved` 10
  - validator parsed 20 raw files, each with 71 daily rows and latest date `20260615`
- Expanded Liquidity Filter smoke sanity checks:
  - total rows `2875`
  - base included rows before Liquidity Filter `2390`
  - rows with raw OHLCV evaluated `23`
  - included rows after saved-raw Liquidity Filter `14`
  - failed rows after saved-raw Liquidity Filter `9`
  - `liquidity_raw_missing` `2367`

## Next Gates

1. Continue OHLCV coverage in small resumable batches from generated Universe rows.
2. In a KIS MCP-capable surface, run `domestic_stock.find_api_detail` for `inquire_daily_itemchartprice`; if unavailable, keep documenting the local API detail fallback explicitly.
3. Save raw responses under `_report/raw/2026/2026-06-15/quant/universe-ohlcv/` and do not commit raw files.
4. Re-run `scripts/quant_smoke_validate.py` and `scripts/quant_liquidity_filter.py` after each documented batch.
5. Generate paper/smoke `Signal Candidate` outputs from Universe rows, not manual watchlists.
6. Build `Point-in-Time Universe` path.
7. Only then run Backtest/OOS/Walk-Forward and Bias Control pass.

## Do Not Do

- Do not treat current snapshot Universe as historical membership.
- Do not treat current snapshot results as Backtest-ready.
- Do not use DI/Main/Game watchlists as Quant Universe.
- Do not strip alphanumeric KRX short codes to digits. Preserve codes like `0004V0`.
- Do not move toward live trading while Backtest readiness is `hold`.
