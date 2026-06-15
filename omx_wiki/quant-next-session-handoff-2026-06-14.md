# Quant Next Session Handoff - 2026-06-14

## Start Here

If a new Codex session starts, read these files first:

1. `omx_wiki/quant-implementation-status-2026-06-14.md`
2. `omx_wiki/quant-krx-current-universe-v0.md`
3. `_report/quant/implementation-roadmap.md`
4. `_report/quant/research/2026-06-14-krx-current-universe-v0.md`
5. `_report/quant/universe.md`

## First Commands

```powershell
git status --short
uv run python -m unittest discover tests
```

If second-capture local changes are still present, stage/commit them before expanding OHLCV coverage again.

Suggested commit intent:

`Capture second KIS OHLCV universe batch`

Use Lore commit protocol.

## Current Best Next Task

Continue generated Universe OHLCV coverage after the first 20 captured rows.

Already implemented in the latest local work:

- `scripts/quant_liquidity_filter.py`
- `tests/test_quant_liquidity_filter.py`
- `scripts/quant_kis_ohlcv_batch_plan.py`
- `tests/test_quant_kis_ohlcv_batch_plan.py`
- `scripts/quant_kis_ohlcv_capture.py`
- `tests/test_quant_kis_ohlcv_capture.py`
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
- Target rule: `avg_trading_value_20d_krw >= 1,000,000,000`
- Saved raw coverage currently evaluates 23 rows. `14` pass and `9` fail the threshold.
- `2367` base-included rows are `liquidity_raw_missing`, which means raw coverage is missing, not that those stocks are illiquid.
- First OHLCV batch dry-run selected `10` requests from generated Universe `include` rows.
- First OHLCV direct capture saved 10 raw files under `_report/raw/2026/2026-06-15/quant/universe-ohlcv/`.
- Second OHLCV batch dry-run selected the next `10` requests after skipping existing raw.
- Second OHLCV direct capture saved 10 more raw files under `_report/raw/2026/2026-06-15/quant/universe-ohlcv/`.
- Current Codex App surface did not expose the KIS MCP tool, so `find_api_detail` was not callable here. Local `MCP/Kis Trading MCP/configs/domestic_stock.json` and `examples_llm` sample docs were used as the fallback API detail evidence, and only the read-only quotation endpoint was called.

Likely needed work:

1. Preflight KIS daily OHLCV API with `domestic_stock.find_api_detail` in a surface where the MCP tool is available.
2. Generate the next small request queue with `scripts/quant_kis_ohlcv_batch_plan.py --skip-existing --limit 10` against `_report/raw/2026/2026-06-15/quant/universe-ohlcv/`; after the second capture this should skip `20` existing raw files.
3. Execute the next queue with `scripts/quant_kis_ohlcv_capture.py`.
4. Save raw KIS responses under `_report/raw/2026/2026-06-15/quant/universe-ohlcv/`; do not commit raw files.
5. Re-run `scripts/quant_smoke_validate.py` and `scripts/quant_liquidity_filter.py` on the expanded raw directory.
6. Keep result as paper/smoke only until `Point-in-Time` is solved.

## Current Blockers

- Git commit for latest OHLCV second-capture local changes may still be pending.
- Full generated Universe OHLCV coverage is still incomplete.
- Historical KRX status data is not available by Rebalance date.
- Backtest remains `hold`.

## User Preferences

- Korean responses.
- Core Quant terms should stay in English, for example `Universe`, `Liquidity Filter`, `Backtest`, `Point-in-Time`.
- When mentioning stocks, include code and company name, for example `005930 Samsung Electronics`.
- Keep DI/Main/Game watchlists separate from Quant.
- Preserve raw evidence under `_report/raw/**`; do not commit raw files.
