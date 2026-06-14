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

If the OHLCV batch plan dirty files are still present, stage/commit them before attempting live KIS MCP capture.

Suggested commit intent:

`Plan KIS OHLCV batches from current KRX universe`

Use Lore commit protocol.

## Current Best Next Task

Execute the first generated Universe OHLCV request queue in a KIS MCP-capable surface.

Already implemented in the latest local work:

- `scripts/quant_liquidity_filter.py`
- `tests/test_quant_liquidity_filter.py`
- `scripts/quant_kis_ohlcv_batch_plan.py`
- `tests/test_quant_kis_ohlcv_batch_plan.py`
- `_report/quant/research/2026-06-14-krx-current-universe-v0-liquidity-smoke.md`
- `_report/quant/research/2026-06-14-krx-current-universe-v0-liquidity-smoke.rows.csv`
- `_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-batch-plan.md`
- `_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-batch-plan.requests.jsonl`
- Target rule: `avg_trading_value_20d_krw >= 1,000,000,000`
- Saved raw coverage currently evaluates `000660 SK hynix`, `005930 Samsung Electronics`, and `035420 NAVER`; all pass.
- `2387` base-included rows are `liquidity_raw_missing`, which means raw coverage is missing, not that those stocks are illiquid.
- First OHLCV batch dry-run selected `10` requests from generated Universe `include` rows.
- Current Codex App surface did not expose the KIS MCP tool, so no live KIS calls were made.

Likely needed work:

1. Preflight KIS daily OHLCV API with `domestic_stock.find_api_detail` in a surface where the MCP tool is available.
2. Execute `_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-batch-plan.requests.jsonl` request rows.
3. Save raw KIS responses under `_report/raw/2026/2026-06-15/quant/universe-ohlcv/`; do not commit raw files.
4. Re-run `scripts/quant_liquidity_filter.py` on the expanded raw directory.
5. Keep result as paper/smoke only until `Point-in-Time` is solved.

## Current Blockers

- Git commit for latest OHLCV batch plan local changes may still be pending.
- KIS OHLCV request queue is generated but not yet executed against live KIS MCP.
- Historical KRX status data is not available by Rebalance date.
- Backtest remains `hold`.

## User Preferences

- Korean responses.
- Core Quant terms should stay in English, for example `Universe`, `Liquidity Filter`, `Backtest`, `Point-in-Time`.
- When mentioning stocks, include code and company name, for example `005930 Samsung Electronics`.
- Keep DI/Main/Game watchlists separate from Quant.
- Preserve raw evidence under `_report/raw/**`; do not commit raw files.
