# Quant Implementation Roadmap

## Metadata

- Date: 2026-06-14
- Scope: Quant trading research and implementation workflow
- Current phase: `current_snapshot_universe_v0`
- Overall implementation progress: `25-30%`
- Current Snapshot Universe progress: `70-80%`
- Backtest readiness: `hold`
- Live trading readiness: `blocked`

## Goal

Build a repeatable Quant workflow that starts from a rule-based `Universe`, generates `Signal Candidate` outputs, validates them through `Backtest`, `Out-of-Sample`, and `Bias Control`, then only later considers execution.

This roadmap is not a trading recommendation. It is an implementation control document.

## Stage Status

| Stage | Status | Progress | Current Evidence | Next Gate |
| --- | --- | ---: | --- | --- |
| 0. Project separation | done | 100% | Quant, DI, raw evidence, routines separated under `_report/` | Keep DI watchlists out of Quant Universe |
| 1. Quant learning baseline | in-progress | 35% | `_report/quant/learning-roadmap.md`, week 01 study log | Continue weekly study logs tied to outputs |
| 2. Strategy specification | in-progress | 50% | `001` Momentum and `002` Reversal specs exist | Keep Strategy rules stable before Backtest |
| 3. Current Snapshot Universe v0 | in-progress | 70-80% | KRX listed issues + managed issues parsed into current Universe | Add `Liquidity Filter` |
| 4. Point-in-Time Universe | blocked | 15-20% | Plan exists; current snapshot artifacts exist | Historical status snapshots or reliable replay source |
| 5. Market data pipeline | in-progress | 30-40% | KIS raw save and smoke validators exist | Batch OHLCV collection for Universe subset |
| 6. Liquidity Filter | next | 10% | Policy exists; not applied to Universe rows yet | Add avg trading value / volume inputs |
| 7. Backtest engine connection | not-started | 10% | Strategy `.kis.yaml` configs exist | Universe + OHLCV + cost model connected |
| 8. OOS / Walk-Forward | planned | 10% | OOS plan exists | Run only after Backtest pipeline works |
| 9. Bias Control pass | hold | 20% | Bias checklists exist; blockers documented | Point-in-Time and OOS evidence |
| 10. Paper Signal tracking | partial | 20-30% | Paper signal logs exist for smoke symbols | Use generated Universe input, not watchlist-only |
| 11. Execution / live trading | blocked | 0% | Position sizing policy blocks live use | Only after Backtest/OOS/Bias Control pass |

## Completed Artifacts

Core policy and learning:

- `_report/quant/README.md`
- `_report/quant/learning-roadmap.md`
- `_report/quant/glossary.md`
- `_report/quant/universe.md`

Strategy artifacts:

- `_report/quant/strategies/001-strategy-universe-momentum.md`
- `_report/quant/strategies/001-strategy-universe-momentum.kis.yaml`
- `_report/quant/strategies/001-strategy-universe-momentum.bias-control.md`
- `_report/quant/strategies/002-strategy-universe-short-term-reversal.md`
- `_report/quant/strategies/002-strategy-universe-short-term-reversal.kis.yaml`
- `_report/quant/strategies/002-strategy-universe-short-term-reversal.bias-control.md`

Current KRX snapshot artifacts:

- `_report/quant/research/2026-06-13-krx-manual-snapshot-manifest.pending.yaml`
- `_report/quant/research/2026-06-13-krx-manual-snapshot-verify-result.md`
- `_report/quant/research/2026-06-14-krx-managed-issues-current-exclusions.md`
- `_report/quant/research/2026-06-14-krx-current-universe-v0-builder.md`
- `_report/quant/research/2026-06-14-krx-current-universe-v0.md`
- `_report/quant/research/2026-06-14-krx-current-universe-v0.rows.csv`

Scripts and tests:

- `scripts/quant_krx_manifest_materialize.py`
- `scripts/quant_krx_manifest_verify.py`
- `scripts/quant_krx_managed_issues_extract.py`
- `scripts/quant_krx_current_universe_build.py`
- `scripts/quant_smoke_validate.py`
- `scripts/quant_calendar_audit.py`
- `tests/test_quant_krx_manifest_tools.py`
- `tests/test_quant_krx_managed_issues_extract.py`
- `tests/test_quant_krx_current_universe_build.py`
- `tests/test_quant_calendar_audit.py`

## Current Snapshot Universe v0

Current generated status:

- Total listed rows: `2875`
- Included rows: `2390`
- Excluded rows: `485`
- Duplicate code count: `0`
- `005930 Samsung Electronics`: `include`
- `121850 코이즈`: `exclude` by `managed_issue_current`
- `0004V0 엔비알모션`: `exclude` by `listing_age_calendar_insufficient`

Applied filters:

- Keep KOSPI/KOSDAQ rows.
- Exclude SPAC, REIT, ETF, ETN, ELW, preferred-share-like instruments.
- Exclude current managed issues.
- Apply `365 calendar days` Listing Age guard.

Known limitation:

- The Strategy target rule is `252 trading days` Listing Age, but this artifact uses `365 calendar days` because a full trading calendar and historical Point-in-Time snapshots are not built yet.

## Open Blockers

Hard blockers before Backtest interpretation:

- `Point-in-Time Universe` is not built.
- Historical managed issue / trading suspension / market alert / delisting status is not reproducible by Rebalance date.
- `Liquidity Filter` is not applied to generated Universe rows.
- OHLCV batch collection is not connected to the generated Universe.
- Backtest, OOS, Walk-Forward, and Bias Control have not passed.

Soft blockers:

- KRX downloads are manual snapshots, not automated reproducible downloads.
- KRX `관리종목 지정 내역(개별종목)` has range/UI constraints and is not a full historical Universe source.
- Some current KRX codes are alphanumeric short codes, so code handling must preserve values such as `0004V0`.

## Next Implementation Steps

### Step A. Commit Current Local Changes

Status: pending because git staging was blocked by usage-limit approval failure.

Files currently expected to be dirty:

- `_report/quant/README.md`
- `_report/quant/universe.md`
- `_report/quant/research/2026-06-14-krx-current-universe-v0-builder.md`
- `_report/quant/research/2026-06-14-krx-current-universe-v0.md`
- `_report/quant/research/2026-06-14-krx-current-universe-v0.rows.csv`
- `scripts/quant_krx_current_universe_build.py`
- `tests/test_quant_krx_current_universe_build.py`

Commit intent:

`Apply Listing Age guard to current KRX universe`

### Step B. Add Liquidity Filter

Input needed:

- Daily OHLCV / trading value for candidate Universe rows.
- At minimum, enough data to calculate recent `20 trading days` average trading value.

Target rule:

- `avg_trading_value_20d_krw >= 1,000,000,000`

Output:

- Add `avg_trading_value_20d_krw`.
- Add `liquidity_filter_status`.
- Exclude rows failing the threshold.

### Step C. Connect Universe to Paper Signal

Goal:

- Stop using manual watchlist-only smoke symbols as the main Quant input.
- Use `current snapshot Universe v0` as the input list for paper/smoke validation.

Guardrail:

- Paper/smoke signals are not trade instructions.

### Step D. Build Point-in-Time Path

Goal:

- Reproduce Universe membership by Rebalance date.

Required fields:

- listed status
- listing date
- delisting date
- managed issue status
- trading suspension status
- market alert status
- OHLCV availability

Pass condition:

- Historical Rebalance dates can be reconstructed without using future-known membership.

### Step E. Backtest and OOS

Only after:

- Universe input is stable.
- OHLCV data is available.
- Transaction Cost / Slippage assumptions are fixed.
- Point-in-Time status is at least acceptable for the test scope.

Output:

- `_report/quant/templates/backtest-report.md` based result document.
- Bias Control checklist attached.

## Current Completion Judgment

The project is beyond planning and has a usable current-snapshot data artifact. However, it is not yet a Backtest-ready Quant system.

Current state:

- Research and policy foundation: strong enough to proceed.
- Current Snapshot Universe: usable for paper/smoke validation.
- Backtest readiness: `hold`.
- Live trading readiness: `blocked`.

