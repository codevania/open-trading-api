# Quant Implementation Status - 2026-06-14

## Summary

- Overall Quant implementation progress: `25-30%`
- Current Snapshot Universe v0 progress: `70-80%`
- Backtest readiness: `hold`
- Live trading readiness: `blocked`
- Current phase: `current_snapshot_universe_v0`

The project is beyond planning and now has a usable current-snapshot Universe artifact. It is still not Backtest-ready because `Point-in-Time Universe`, `Liquidity Filter`, OHLCV batch collection, OOS, and Bias Control are incomplete.

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
- Tests for manifest verification, managed issue extraction, current Universe build, and calendar audit pass.

## Current Universe v0

Artifacts:

- `_report/quant/research/2026-06-14-krx-current-universe-v0.md`
- `_report/quant/research/2026-06-14-krx-current-universe-v0.rows.csv`
- `scripts/quant_krx_current_universe_build.py`
- `tests/test_quant_krx_current_universe_build.py`

Current result:

- Total rows: `2875`
- Include: `2390`
- Exclude: `485`
- Duplicate code count: `0`
- `005930 Samsung Electronics`: included
- `121850 코이즈`: excluded by `managed_issue_current`
- `0004V0 엔비알모션`: excluded by `listing_age_calendar_insufficient`

Filters currently applied:

- KOSPI/KOSDAQ only.
- Exclude SPAC, REIT, ETF, ETN, ELW, preferred-share-like instruments.
- Exclude current KRX managed issues.
- Apply `365 calendar days` Listing Age guard.

Important caveat:

- Strategy target is `252 trading days` Listing Age, but current artifact uses `365 calendar days` because a full trading-day calendar and historical `Point-in-Time` status data are not yet built.

## Dirty Local Changes

As of this capture, these changes were local and not committed because `git add` escalation was blocked by a usage-limit failure:

- `_report/quant/README.md`
- `_report/quant/universe.md`
- `_report/quant/implementation-roadmap.md`
- `_report/quant/research/2026-06-14-krx-current-universe-v0-builder.md`
- `_report/quant/research/2026-06-14-krx-current-universe-v0.md`
- `_report/quant/research/2026-06-14-krx-current-universe-v0.rows.csv`
- `scripts/quant_krx_current_universe_build.py`
- `tests/test_quant_krx_current_universe_build.py`
- `omx_wiki/*`

## Verification Already Run

- `uv run python -m unittest discover tests`
- `uv run python -m py_compile scripts\quant_krx_current_universe_build.py scripts\quant_krx_managed_issues_extract.py`
- Current Universe sanity checks:
  - `2875` total rows
  - `2390` included rows
  - `485` excluded rows
  - duplicate code count `0`
  - `005930 Samsung Electronics` included
  - `121850 코이즈` excluded
  - `0004V0 엔비알모션` excluded by Listing Age

## Next Gates

1. Commit and push current local changes.
2. Add `Liquidity Filter`.
3. Connect generated Universe rows to OHLCV batch collection.
4. Generate paper/smoke `Signal Candidate` outputs from Universe rows, not manual watchlists.
5. Build `Point-in-Time Universe` path.
6. Only then run Backtest/OOS/Walk-Forward and Bias Control pass.

## Do Not Do

- Do not treat current snapshot Universe as historical membership.
- Do not treat current snapshot results as Backtest-ready.
- Do not use DI/Main/Game watchlists as Quant Universe.
- Do not strip alphanumeric KRX short codes to digits. Preserve codes like `0004V0`.
- Do not move toward live trading while Backtest readiness is `hold`.

