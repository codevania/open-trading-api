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

If the dirty files are still present, stage/commit/push them before starting `Liquidity Filter`.

Suggested commit intent:

`Apply Listing Age guard to current KRX universe`

Use Lore commit protocol.

## Current Best Next Task

Add `Liquidity Filter` to the current Universe pipeline.

Target rule from existing Quant policy:

- `avg_trading_value_20d_krw >= 1,000,000,000`

Likely needed work:

1. Decide input source for OHLCV/trading value rows.
2. Reuse or extend `scripts/quant_smoke_validate.py` / KIS raw routines where possible.
3. Add a dedicated liquidity-enrichment or liquidity-filter script.
4. Generate a new derived artifact from current Universe rows.
5. Keep result as paper/smoke only until `Point-in-Time` is solved.

## Current Blockers

- Git commit/push for latest local changes may still be pending.
- KIS OHLCV batch collection is not yet connected to generated Universe rows.
- Historical KRX status data is not available by Rebalance date.
- Backtest remains `hold`.

## User Preferences

- Korean responses.
- Core Quant terms should stay in English, for example `Universe`, `Liquidity Filter`, `Backtest`, `Point-in-Time`.
- When mentioning stocks, include code and company name, for example `005930 Samsung Electronics`.
- Keep DI/Main/Game watchlists separate from Quant.
- Preserve raw evidence under `_report/raw/**`; do not commit raw files.

