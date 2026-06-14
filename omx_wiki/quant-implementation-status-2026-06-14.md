# Quant Implementation Status - 2026-06-14

## Summary

- Overall Quant implementation progress: `30-35%`
- Current Snapshot Universe v0 progress: `80-85%`
- Backtest readiness: `hold`
- Live trading readiness: `blocked`
- Current phase: `current_snapshot_universe_v0`

The project is beyond planning and now has a usable current-snapshot Universe artifact plus a saved-raw Liquidity Filter smoke artifact. It is still not Backtest-ready because `Point-in-Time Universe`, full-Universe OHLCV batch collection, OOS, and Bias Control are incomplete.

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
- Tests for manifest verification, managed issue extraction, current Universe build, Liquidity Filter, and calendar audit pass.

## Current Universe v0

Artifacts:

- `_report/quant/research/2026-06-14-krx-current-universe-v0.md`
- `_report/quant/research/2026-06-14-krx-current-universe-v0.rows.csv`
- `_report/quant/research/2026-06-14-krx-current-universe-v0-liquidity-smoke.md`
- `_report/quant/research/2026-06-14-krx-current-universe-v0-liquidity-smoke.rows.csv`
- `scripts/quant_krx_current_universe_build.py`
- `scripts/quant_liquidity_filter.py`
- `tests/test_quant_krx_current_universe_build.py`
- `tests/test_quant_liquidity_filter.py`

Current result:

- Total rows: `2875`
- Include: `2390`
- Exclude: `485`
- Duplicate code count: `0`
- `005930 Samsung Electronics`: included
- `121850 코이즈`: excluded by `managed_issue_current`
- `0004V0 엔비알모션`: excluded by `listing_age_calendar_insufficient`
- Liquidity smoke evaluated rows with saved raw OHLCV: `3`
- Liquidity smoke pass: `000660 SK hynix`, `005930 Samsung Electronics`, `035420 NAVER`
- Liquidity smoke `liquidity_raw_missing`: `2387` base-included rows without saved raw OHLCV

Filters currently applied:

- KOSPI/KOSDAQ only.
- Exclude SPAC, REIT, ETF, ETN, ELW, preferred-share-like instruments.
- Exclude current KRX managed issues.
- Apply `365 calendar days` Listing Age guard.
- Apply saved-raw Liquidity Filter smoke for rows with KIS OHLCV raw coverage.

Important caveat:

- Strategy target is `252 trading days` Listing Age, but current artifact uses `365 calendar days` because a full trading-day calendar and historical `Point-in-Time` status data are not yet built.
- Liquidity Filter output is still smoke-only because full generated Universe rows are not connected to OHLCV batch collection.

## Dirty Local Changes

As of this capture, Liquidity Filter implementation changes are local unless a later commit records them:

- `_report/quant/README.md`
- `_report/quant/universe.md`
- `_report/quant/implementation-roadmap.md`
- `_report/quant/research/2026-06-14-krx-current-universe-v0-liquidity-smoke.md`
- `_report/quant/research/2026-06-14-krx-current-universe-v0-liquidity-smoke.rows.csv`
- `scripts/quant_liquidity_filter.py`
- `tests/test_quant_liquidity_filter.py`
- `omx_wiki/*`

## Verification Already Run

- `uv run python -m unittest discover tests`
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
- Liquidity Filter smoke sanity checks:
  - total rows `2875`
  - base included rows before Liquidity Filter `2390`
  - included rows after saved-raw Liquidity Filter `3`
  - `000660 SK hynix`, `005930 Samsung Electronics`, `035420 NAVER` pass
  - `2387` base-included rows are `liquidity_raw_missing`

## Next Gates

1. Commit and push current Liquidity Filter local changes if still pending.
2. Connect generated Universe rows to OHLCV batch collection.
3. Expand Liquidity Filter coverage beyond manually saved raw files.
4. Generate paper/smoke `Signal Candidate` outputs from Universe rows, not manual watchlists.
5. Build `Point-in-Time Universe` path.
6. Only then run Backtest/OOS/Walk-Forward and Bias Control pass.

## Do Not Do

- Do not treat current snapshot Universe as historical membership.
- Do not treat current snapshot results as Backtest-ready.
- Do not use DI/Main/Game watchlists as Quant Universe.
- Do not strip alphanumeric KRX short codes to digits. Preserve codes like `0004V0`.
- Do not move toward live trading while Backtest readiness is `hold`.
