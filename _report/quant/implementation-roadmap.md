# Quant Implementation Roadmap

## Metadata

- Date: 2026-06-14
- Scope: Quant trading research and implementation workflow
- Current phase: `current_snapshot_universe_v0`
- Overall implementation progress: `40-45%`
- Current Snapshot Universe progress: `85-90%`
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
| 3. Current Snapshot Universe v0 | in-progress | 85-90% | KRX listed issues + managed issues parsed into current Universe; 350 Universe OHLCV raw files applied to Liquidity Filter smoke | Expand OHLCV coverage beyond first 350 captured rows |
| 4. Point-in-Time Universe | blocked | 15-20% | Plan exists; current snapshot artifacts exist | Historical status snapshots or reliable replay source |
| 5. Market data pipeline | in-progress | 45-50% | KIS raw save, smoke validators, Universe-based OHLCV request queue, and first 350 read-only KIS captures exist | Continue resumable Universe OHLCV capture batches |
| 6. Liquidity Filter | in-progress | 40-45% | `scripts/quant_liquidity_filter.py`; 351 unique saved raw rows evaluated against current Universe | Fill OHLCV coverage beyond the first 351 evaluated rows |
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
- `_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-third10.md`
- `_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-third10.requests.jsonl`
- `_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-dry-run-third10.md`
- `_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-result-third10.md`
- `_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-validator-result-third10.md`
- `_report/quant/research/2026-06-17-krx-current-universe-v0-liquidity-smoke-expanded-third10.md`
- `_report/quant/research/2026-06-17-krx-current-universe-v0-liquidity-smoke-expanded-third10.rows.csv`
- `_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-fourth10.md`
- `_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-fourth10.requests.jsonl`
- `_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-dry-run-fourth10.md`
- `_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-result-fourth10.md`
- `_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-validator-result-fourth10.md`
- `_report/quant/research/2026-06-17-krx-current-universe-v0-liquidity-smoke-expanded-fourth10.md`
- `_report/quant/research/2026-06-17-krx-current-universe-v0-liquidity-smoke-expanded-fourth10.rows.csv`
- `_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-*-fifth10*`
- `_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-*-sixth10*`
- `_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-*-seventh10*`
- `_report/quant/research/2026-06-17-krx-current-universe-v0-liquidity-smoke-expanded-seventh10.md`
- `_report/quant/research/2026-06-17-krx-current-universe-v0-liquidity-smoke-expanded-seventh10.rows.csv`
- `_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-*-eighth10*`
- `_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-*-ninth10*`
- `_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-*-tenth10*`
- `_report/quant/research/2026-06-17-krx-current-universe-v0-liquidity-smoke-expanded-tenth10.md`
- `_report/quant/research/2026-06-17-krx-current-universe-v0-liquidity-smoke-expanded-tenth10.rows.csv`
- `_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-*-eleventh10*`
- `_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-*-twelfth10*`
- `_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-*-thirteenth10*`
- `_report/quant/research/2026-06-17-krx-current-universe-v0-liquidity-smoke-expanded-thirteenth10.md`
- `_report/quant/research/2026-06-17-krx-current-universe-v0-liquidity-smoke-expanded-thirteenth10.rows.csv`
- `_report/quant/research/2026-06-18-krx-current-universe-v0-ohlcv-*-fourteenth10*`
- `_report/quant/research/2026-06-18-krx-current-universe-v0-ohlcv-*-fifteenth10*`
- `_report/quant/research/2026-06-18-krx-current-universe-v0-ohlcv-*-sixteenth10*`
- `_report/quant/research/2026-06-18-krx-current-universe-v0-liquidity-smoke-expanded-sixteenth10.md`
- `_report/quant/research/2026-06-18-krx-current-universe-v0-liquidity-smoke-expanded-sixteenth10.rows.csv`
- `_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-*-seventeenth10*`
- `_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-*-eighteenth10*`
- `_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-*-nineteenth10*`
- `_report/quant/research/2026-06-30-krx-current-universe-v0-liquidity-smoke-expanded-nineteenth10.md`
- `_report/quant/research/2026-06-30-krx-current-universe-v0-liquidity-smoke-expanded-nineteenth10.rows.csv`
- `_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-*-twentieth10*`
- `_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-*-twentyfirst10*`
- `_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-*-twentysecond10*`
- `_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-*-twentythird10*`
- `_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-*-twentyfourth10*`
- `_report/quant/research/2026-06-30-krx-current-universe-v0-liquidity-smoke-expanded-twentyfourth10.md`
- `_report/quant/research/2026-06-30-krx-current-universe-v0-liquidity-smoke-expanded-twentyfourth10.rows.csv`
- `_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-*-twentyfifth10*`
- `_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-*-twentysixth10*`
- `_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-*-twentyseventh10*`
- `_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-*-twentyeighth10*`
- `_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-*-twentyninth10*`
- `_report/quant/research/2026-06-30-krx-current-universe-v0-liquidity-smoke-expanded-twentyninth10.md`
- `_report/quant/research/2026-06-30-krx-current-universe-v0-liquidity-smoke-expanded-twentyninth10.rows.csv`
- `_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-*-thirtieth10*`
- `_report/quant/research/2026-07-01-krx-current-universe-v0-liquidity-smoke-expanded-thirtieth10.md`
- `_report/quant/research/2026-07-01-krx-current-universe-v0-liquidity-smoke-expanded-thirtieth10.rows.csv`
- `_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-*-thirtyfirst10*`
- `_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-*-thirtysecond10*`
- `_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-*-thirtythird10*`
- `_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-*-thirtyfourth10*`
- `_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-*-thirtyfifth10*`
- `_report/quant/research/2026-07-01-krx-current-universe-v0-liquidity-smoke-expanded-thirtyfifth10.md`
- `_report/quant/research/2026-07-01-krx-current-universe-v0-liquidity-smoke-expanded-thirtyfifth10.rows.csv`
- `_report/quant/research/2026-07-01-user-action-items-temp.md`

Scripts and tests:

- `scripts/quant_krx_manifest_materialize.py`
- `scripts/quant_krx_manifest_verify.py`
- `scripts/quant_krx_managed_issues_extract.py`
- `scripts/quant_krx_current_universe_build.py`
- `scripts/quant_kis_ohlcv_batch_plan.py`
- `scripts/quant_kis_ohlcv_capture.py`
- `scripts/quant_liquidity_filter.py`
- `scripts/quant_smoke_validate.py`
- `scripts/quant_calendar_audit.py`
- `tests/test_quant_krx_manifest_tools.py`
- `tests/test_quant_krx_managed_issues_extract.py`
- `tests/test_quant_krx_current_universe_build.py`
- `tests/test_quant_kis_ohlcv_batch_plan.py`
- `tests/test_quant_kis_ohlcv_capture.py`
- `tests/test_quant_liquidity_filter.py`
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
- Saved-raw Liquidity Filter smoke: `avg_trading_value_20d_krw >= 1,000,000,000`.

Known limitation:

- The Strategy target rule is `252 trading days` Listing Age, but this artifact uses `365 calendar days` because a full trading calendar and historical Point-in-Time snapshots are not built yet.
- The expanded Liquidity Filter smoke artifact only evaluates rows with saved raw OHLCV under `_report/raw/2026/2026-06-13/quant/paper-follow-up/` and `_report/raw/2026/2026-06-15/quant/universe-ohlcv/`; missing raw is a data-coverage blocker, not an illiquidity finding.

## Open Blockers

Hard blockers before Backtest interpretation:

- `Point-in-Time Universe` is not built.
- Historical managed issue / trading suspension / market alert / delisting status is not reproducible by Rebalance date.
- Full-Universe `Liquidity Filter` coverage is incomplete because only the first 350 generated Universe OHLCV rows have been captured.
- Current Liquidity Filter output is an expanded saved-raw smoke artifact, not full current Universe coverage.
- Backtest, OOS, Walk-Forward, and Bias Control have not passed.

Soft blockers:

- KRX downloads are manual snapshots, not automated reproducible downloads.
- KRX `관리종목 지정 내역(개별종목)` has range/UI constraints and is not a full historical Universe source.
- Some current KRX codes are alphanumeric short codes, so code handling must preserve values such as `0004V0`.

## Next Implementation Steps

### Step A. Connect Universe to OHLCV Batch Collection

Goal:

- Stop relying on manually selected raw files for Liquidity Filter coverage.
- Use generated current Universe rows as the batch input list for KIS daily OHLCV collection.

Current implemented path:

- `scripts/quant_kis_ohlcv_batch_plan.py` reads generated Universe rows and emits a resumable request queue.
- `_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-batch-plan.md` records a first dry-run with `10` requests.
- `_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-batch-plan-next10.md` records the next `10` requests after skipping existing raw.
- `_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-third10.md` records the third `10` requests after skipping `20` existing raw files.
- `_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-fourth10.md` records the fourth `10` requests after skipping `30` existing raw files.
- `_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-fifth10.md`, `...-sixth10.md`, and `...-seventh10.md` record three more `10` request queues after skipping `40`, `50`, and `60` existing raw files.
- `_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-eighth10.md`, `...-ninth10.md`, and `...-tenth10.md` record three more `10` request queues after skipping `70`, `80`, and `90` existing raw files.
- `_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-eleventh10.md`, `...-twelfth10.md`, and `...-thirteenth10.md` record three more `10` request queues after skipping `100`, `110`, and `120` existing raw files.
- `_report/quant/research/2026-06-18-krx-current-universe-v0-ohlcv-batch-plan-fourteenth10.md`, `...-fifteenth10.md`, and `...-sixteenth10.md` record three more `10` request queues after skipping `130`, `140`, and `150` existing raw files.
- `_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-seventeenth10.md`, `...-eighteenth10.md`, and `...-nineteenth10.md` record three more `10` request queues after skipping `160`, `170`, and `180` existing raw files.
- `_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentieth10.md`, `...-twentyfirst10.md`, `...-twentysecond10.md`, `...-twentythird10.md`, and `...-twentyfourth10.md` record five more `10` request queues after skipping `190`, `200`, `210`, `220`, and `230` existing raw files.
- `_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyfifth10.md`, `...-twentysixth10.md`, `...-twentyseventh10.md`, `...-twentyeighth10.md`, and `...-twentyninth10.md` record five more `10` request queues after skipping `240`, `250`, `260`, `270`, and `280` existing raw files.
- `_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtieth10.md` records one more `10` request queue after skipping `290` existing raw files.
- `_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtyfirst10.md`, `...-thirtysecond10.md`, `...-thirtythird10.md`, `...-thirtyfourth10.md`, and `...-thirtyfifth10.md` record five more `10` request queues after skipping `300`, `310`, `320`, `330`, and `340` existing raw files.
- `_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-batch-plan*.requests.jsonl` files are machine-readable request queues.
- `_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-third10.requests.jsonl` is the machine-readable third request queue.
- `_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-fourth10.requests.jsonl` is the machine-readable fourth request queue.
- `_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-fifth10.requests.jsonl`, `...-sixth10.requests.jsonl`, and `...-seventh10.requests.jsonl` are the machine-readable fifth through seventh request queues.
- `_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-eighth10.requests.jsonl`, `...-ninth10.requests.jsonl`, and `...-tenth10.requests.jsonl` are the machine-readable eighth through tenth request queues.
- `_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-eleventh10.requests.jsonl`, `...-twelfth10.requests.jsonl`, and `...-thirteenth10.requests.jsonl` are the machine-readable eleventh through thirteenth request queues.
- `_report/quant/research/2026-06-18-krx-current-universe-v0-ohlcv-batch-plan-fourteenth10.requests.jsonl`, `...-fifteenth10.requests.jsonl`, and `...-sixteenth10.requests.jsonl` are the machine-readable fourteenth through sixteenth request queues.
- `_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-seventeenth10.requests.jsonl`, `...-eighteenth10.requests.jsonl`, and `...-nineteenth10.requests.jsonl` are the machine-readable seventeenth through nineteenth request queues.
- `_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentieth10.requests.jsonl`, `...-twentyfirst10.requests.jsonl`, `...-twentysecond10.requests.jsonl`, `...-twentythird10.requests.jsonl`, and `...-twentyfourth10.requests.jsonl` are the machine-readable twentieth through twentyfourth request queues.
- `_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyfifth10.requests.jsonl`, `...-twentysixth10.requests.jsonl`, `...-twentyseventh10.requests.jsonl`, `...-twentyeighth10.requests.jsonl`, and `...-twentyninth10.requests.jsonl` are the machine-readable twentyfifth through twentyninth request queues.
- `_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtieth10.requests.jsonl` is the machine-readable thirtieth request queue.
- `_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtyfirst10.requests.jsonl`, `...-thirtysecond10.requests.jsonl`, `...-thirtythird10.requests.jsonl`, `...-thirtyfourth10.requests.jsonl`, and `...-thirtyfifth10.requests.jsonl` are the machine-readable thirtyfirst through thirtyfifth request queues.

Guardrail:

- KIS data calls must still be preflighted with `find_api_detail`.
- Raw responses stay under `_report/raw/**` and are not committed.
- The current Codex App surface did not expose the KIS MCP tool, so `find_api_detail` could not be called directly here. The first live subset used local KIS config/example API detail as a fallback and called only the read-only quotation endpoint through `examples_llm/kis_auth.py`.

Next gate:

- In a surface with KIS MCP access, run `domestic_stock.find_api_detail` for `inquire_daily_itemchartprice`. Then continue small resumable OHLCV capture batches from `--skip-existing` state `350`, save raw responses under `_report/raw/2026/2026-06-15/quant/universe-ohlcv/`, and re-run `scripts/quant_liquidity_filter.py`.

### Step B. Expand Liquidity Filter Coverage

Current implemented path:

- `scripts/quant_liquidity_filter.py` reads current Universe rows and saved KIS daily raw files.
- `_report/quant/research/2026-06-15-krx-current-universe-v0-liquidity-smoke-expanded.md` records the expanded paper/smoke run.
- `_report/quant/research/2026-07-01-krx-current-universe-v0-liquidity-smoke-expanded-thirtyfifth10.md` records the latest expanded paper/smoke run.
- Latest expanded run evaluates `351` saved raw rows against the current Universe: `174` pass, `177` fail, `2039` `liquidity_raw_missing`, and `485` `not_evaluated_preexisting_exclude`.
- Saved raw coverage currently evaluates 351 unique rows. See `_report/quant/research/2026-07-01-krx-current-universe-v0-liquidity-smoke-expanded-thirtyfifth10.rows.csv` for the authoritative pass/fail row set.

Target rule:

- `avg_trading_value_20d_krw >= 1,000,000,000`

Remaining input needed:

- Daily OHLCV / trading value for all generated candidate Universe rows, or for additional documented current Universe subsets.
- At minimum, enough data to calculate recent `20 trading days` average trading value.

Output already added:

- `avg_trading_value_20d_krw`
- `liquidity_filter_status`
- final `status` and `reason` after the saved-raw Liquidity Filter pass

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
