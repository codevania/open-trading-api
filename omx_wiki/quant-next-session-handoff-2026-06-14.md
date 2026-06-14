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

If the Liquidity Filter dirty files are still present, stage/commit/push them before starting OHLCV batch collection work.

Suggested commit intent:

`Apply Liquidity Filter smoke to current KRX universe`

Use Lore commit protocol.

## Current Best Next Task

Connect generated current Universe rows to OHLCV batch collection.

Already implemented in the latest local work:

- `scripts/quant_liquidity_filter.py`
- `tests/test_quant_liquidity_filter.py`
- `_report/quant/research/2026-06-14-krx-current-universe-v0-liquidity-smoke.md`
- `_report/quant/research/2026-06-14-krx-current-universe-v0-liquidity-smoke.rows.csv`
- Target rule: `avg_trading_value_20d_krw >= 1,000,000,000`
- Saved raw coverage currently evaluates `000660 SK hynix`, `005930 Samsung Electronics`, and `035420 NAVER`; all pass.
- `2387` base-included rows are `liquidity_raw_missing`, which means raw coverage is missing, not that those stocks are illiquid.

Likely needed work:

1. Preflight KIS daily OHLCV API with `find_api_detail`.
2. Build a batch collection path from `_report/quant/research/2026-06-14-krx-current-universe-v0.rows.csv` included rows.
3. Save raw KIS responses under `_report/raw/**`; do not commit raw files.
4. Re-run `scripts/quant_liquidity_filter.py` on the expanded raw directory.
5. Keep result as paper/smoke only until `Point-in-Time` is solved.

## Current Blockers

- Git commit/push for latest Liquidity Filter local changes may still be pending.
- KIS OHLCV batch collection is not yet connected to generated Universe rows.
- Historical KRX status data is not available by Rebalance date.
- Backtest remains `hold`.

## User Preferences

- Korean responses.
- Core Quant terms should stay in English, for example `Universe`, `Liquidity Filter`, `Backtest`, `Point-in-Time`.
- When mentioning stocks, include code and company name, for example `005930 Samsung Electronics`.
- Keep DI/Main/Game watchlists separate from Quant.
- Preserve raw evidence under `_report/raw/**`; do not commit raw files.
