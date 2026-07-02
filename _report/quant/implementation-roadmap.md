# Quant Implementation Roadmap

## Metadata

- Date: 2026-06-14
- Last updated: 2026-07-03
- Scope: Quant trading research and implementation workflow
- Current phase: `point_in_time_status_replay_scaffold`
- Overall implementation progress: `60-64%`
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
| 1. Quant learning baseline | in-progress | 35% | [[_report/quant/learning-roadmap|_report/quant/learning-roadmap.md]], week 01 study log | Continue weekly study logs tied to outputs |
| 2. Strategy specification | in-progress | 50% | `001` Momentum and `002` Reversal specs exist | Keep Strategy rules stable before Backtest |
| 3. Current Snapshot Universe v0 | in-progress | 85-90% | KRX listed issues + managed issues parsed into current Universe; 360 Universe OHLCV raw files applied to Liquidity Filter smoke | Expand OHLCV coverage beyond first 360 captured rows |
| 4. Point-in-Time Universe | in-progress | 40-45% | KRX OpenAPI market-data path works; status source gap, status-event schema, validator, replay scaffold, and KRX Data Marketplace status-source probe are documented | Get one authenticated/manual KRX status raw sample or switch to KIND fallback |
| 5. Market data pipeline | in-progress | 75-80% | KIS raw save, smoke validators, Universe OHLCV queue, first 360 KIS captures, KRX OpenAPI core raw collector/normalizer, 17-date historical collection smoke, continuity audit, and date-scoped market-data join exist | Connect Point-in-Time status replay or extend another bounded historical window |
| 6. Liquidity Filter | in-progress | 40-45% | [[scripts/quant_liquidity_filter.py|scripts/quant_liquidity_filter.py]]; 361 unique saved raw rows evaluated against current Universe | Fill OHLCV coverage beyond the first 361 evaluated rows |
| 7. Backtest engine connection | not-started | 10% | Strategy `.kis.yaml` configs exist | Universe + OHLCV + cost model connected |
| 8. OOS / Walk-Forward | planned | 10% | OOS plan exists | Run only after Backtest pipeline works |
| 9. Bias Control pass | hold | 20% | Bias checklists exist; blockers documented | Point-in-Time and OOS evidence |
| 10. Paper Signal tracking | partial | 20-30% | Paper signal logs exist for smoke symbols | Use generated Universe input, not watchlist-only |
| 11. Execution / live trading | blocked | 0% | Position sizing policy blocks live use | Only after Backtest/OOS/Bias Control pass |

## Completed Artifacts

Core policy and learning:

- [[_report/quant/README|_report/quant/README.md]]
- [[_report/quant/learning-roadmap|_report/quant/learning-roadmap.md]]
- [[_report/quant/glossary|_report/quant/glossary.md]]
- [[_report/quant/universe|_report/quant/universe.md]]

Strategy artifacts:

- [[_report/quant/strategies/001-strategy-universe-momentum|_report/quant/strategies/001-strategy-universe-momentum.md]]
- [[_report/quant/strategies/001-strategy-universe-momentum.kis.yaml|_report/quant/strategies/001-strategy-universe-momentum.kis.yaml]]
- [[_report/quant/strategies/001-strategy-universe-momentum.bias-control.md|_report/quant/strategies/001-strategy-universe-momentum.bias-control.md]]
- [[_report/quant/strategies/002-strategy-universe-short-term-reversal|_report/quant/strategies/002-strategy-universe-short-term-reversal.md]]
- [[_report/quant/strategies/002-strategy-universe-short-term-reversal.kis.yaml|_report/quant/strategies/002-strategy-universe-short-term-reversal.kis.yaml]]
- [[_report/quant/strategies/002-strategy-universe-short-term-reversal.bias-control.md|_report/quant/strategies/002-strategy-universe-short-term-reversal.bias-control.md]]

Current KRX snapshot artifacts:

- [[_report/quant/research/2026-06-13-krx-manual-snapshot-manifest.pending.yaml|_report/quant/research/2026-06-13-krx-manual-snapshot-manifest.pending.yaml]]
- [[_report/quant/research/2026-06-13-krx-manual-snapshot-verify-result|_report/quant/research/2026-06-13-krx-manual-snapshot-verify-result.md]]
- [[_report/quant/research/2026-06-14-krx-managed-issues-current-exclusions|_report/quant/research/2026-06-14-krx-managed-issues-current-exclusions.md]]
- [[_report/quant/research/2026-06-14-krx-current-universe-v0-builder|_report/quant/research/2026-06-14-krx-current-universe-v0-builder.md]]
- [[_report/quant/research/2026-06-14-krx-current-universe-v0|_report/quant/research/2026-06-14-krx-current-universe-v0.md]]
- [[_report/quant/research/2026-06-14-krx-current-universe-v0.rows.csv|_report/quant/research/2026-06-14-krx-current-universe-v0.rows.csv]]
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
- [[_report/quant/research/2026-07-03-krx-openapi-key-next-steps|_report/quant/research/2026-07-03-krx-openapi-key-next-steps.md]]

KRX OpenAPI core artifacts:

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
- Local secret template: `.env.krx.example`; actual `.env.krx` is git-ignored and must not be committed.
- Raw smoke evidence is saved under `_report/raw/2026/2026-07-03/krx/openapi/` and remains uncommitted.

Scripts and tests:

- [[scripts/quant_krx_manifest_materialize.py|scripts/quant_krx_manifest_materialize.py]]
- [[scripts/quant_krx_manifest_verify.py|scripts/quant_krx_manifest_verify.py]]
- [[scripts/quant_krx_managed_issues_extract.py|scripts/quant_krx_managed_issues_extract.py]]
- [[scripts/quant_krx_current_universe_build.py|scripts/quant_krx_current_universe_build.py]]
- [[scripts/quant_kis_ohlcv_batch_plan.py|scripts/quant_kis_ohlcv_batch_plan.py]]
- [[scripts/quant_kis_ohlcv_capture.py|scripts/quant_kis_ohlcv_capture.py]]
- [[scripts/quant_liquidity_filter.py|scripts/quant_liquidity_filter.py]]
- [[scripts/quant_smoke_validate.py|scripts/quant_smoke_validate.py]]
- [[scripts/quant_calendar_audit.py|scripts/quant_calendar_audit.py]]
- [[tests/test_quant_krx_manifest_tools.py|tests/test_quant_krx_manifest_tools.py]]
- [[tests/test_quant_krx_managed_issues_extract.py|tests/test_quant_krx_managed_issues_extract.py]]
- [[tests/test_quant_krx_current_universe_build.py|tests/test_quant_krx_current_universe_build.py]]
- [[tests/test_quant_kis_ohlcv_batch_plan.py|tests/test_quant_kis_ohlcv_batch_plan.py]]
- [[tests/test_quant_kis_ohlcv_capture.py|tests/test_quant_kis_ohlcv_capture.py]]
- [[tests/test_quant_liquidity_filter.py|tests/test_quant_liquidity_filter.py]]
- [[tests/test_quant_calendar_audit.py|tests/test_quant_calendar_audit.py]]

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
- Full-Universe `Liquidity Filter` coverage is incomplete because only the first 360 generated Universe OHLCV rows have been captured.

## KRX OpenAPI Core Raw Smoke

Status: `usable_for_raw_collection`

Approved and smoke-tested core services:

| service id | API | 2025-01-02 rows |
| --- | --- | ---: |
| `kospi_stock_daily` | 유가증권 일별매매정보 | 961 |
| `kosdaq_stock_daily` | 코스닥 일별매매정보 | 1784 |
| `kospi_issue_base` | 유가증권 종목기본정보 | 961 |
| `kosdaq_issue_base` | 코스닥 종목기본정보 | 1784 |
| `kospi_index_daily` | KOSPI 시리즈 일별시세정보 | 51 |
| `kosdaq_index_daily` | KOSDAQ 시리즈 일별시세정보 | 40 |

Notes:

- All six services returned HTTP `200` with `OutBlock_1` JSON rows for `2025-01-02`.
- The same six services returned HTTP `200` but `0` rows for `2026-07-02`; treat that date as unavailable for schema validation until KRX data availability is confirmed.
- This solves the first official raw-market-data gate, but it does not yet solve `Point-in-Time` status replay for managed issues, trading halts, or delistings.
- Current Liquidity Filter output is an expanded saved-raw smoke artifact, not full current Universe coverage.
- Backtest, OOS, Walk-Forward, and Bias Control have not passed.

## KRX OpenAPI Normalize Smoke

Status: `usable_for_parser_development`

Validated on the saved `2025-01-02` KRX OpenAPI core raw files:

| table | rows | interpretation |
| --- | ---: | --- |
| `stock_daily` | 2745 | KOSPI/KOSDAQ daily market rows normalized into stable local columns |
| `issue_base` | 2745 | KOSPI/KOSDAQ issue master rows normalized with standard code, short code, listing date, market, and listed shares |
| `index_daily` | 91 | KOSPI/KOSDAQ index rows normalized for benchmark plumbing |

Artifacts:

- [[scripts/quant_krx_openapi_normalize.py|scripts/quant_krx_openapi_normalize.py]]
- [[tests/test_quant_krx_openapi_normalize.py|tests/test_quant_krx_openapi_normalize.py]]
- [[_report/quant/research/2026-07-03-krx-openapi-normalize-smoke|_report/quant/research/2026-07-03-krx-openapi-normalize-smoke.md]]

Remaining limitation:

- This is a parser/market-data normalization milestone, not a `Point-in-Time Universe` or `Backtest` milestone.
- Management designation, trading halt, market alert, and delisting replay still need historical status sources.

## KRX OpenAPI Historical Collection Smoke

Status: `usable_for_multi_date_parser_development`

Latest validated coverage spans `2025-01-02` to `2025-01-24` across `17` weekday rows after adding `2025-01-13` to `2025-01-24`.

| metric | value |
| --- | ---: |
| candidate dates | 17 |
| complete dates after collection | 17 |
| saved raw files in range | 102 |
| missing requests after collection | 0 |
| normalized `stock_daily` rows | 46659 |
| normalized `issue_base` rows | 46659 |
| normalized `index_daily` rows | 1547 |

Artifacts:

- [[scripts/quant_krx_openapi_history_plan.py|scripts/quant_krx_openapi_history_plan.py]]
- [[tests/test_quant_krx_openapi_history_plan.py|tests/test_quant_krx_openapi_history_plan.py]]
- [[_report/quant/research/2026-07-03-krx-openapi-history-plan-20250102-20250110|_report/quant/research/2026-07-03-krx-openapi-history-plan-20250102-20250110.md]]
- [[_report/quant/research/2026-07-03-krx-openapi-history-plan-20250102-20250110.requests.json|_report/quant/research/2026-07-03-krx-openapi-history-plan-20250102-20250110.requests.json]]
- [[_report/quant/research/2026-07-03-krx-openapi-history-collection-result-20250102-20250110|_report/quant/research/2026-07-03-krx-openapi-history-collection-result-20250102-20250110.md]]
- [[_report/quant/research/2026-07-03-krx-openapi-history-normalize-result-20250102-20250110|_report/quant/research/2026-07-03-krx-openapi-history-normalize-result-20250102-20250110.md]]
- [[_report/quant/research/2026-07-03-krx-openapi-history-plan-20250113-20250124|_report/quant/research/2026-07-03-krx-openapi-history-plan-20250113-20250124.md]]
- [[_report/quant/research/2026-07-03-krx-openapi-history-plan-20250113-20250124.requests.json|_report/quant/research/2026-07-03-krx-openapi-history-plan-20250113-20250124.requests.json]]
- [[_report/quant/research/2026-07-03-krx-openapi-history-collection-result-20250113-20250124|_report/quant/research/2026-07-03-krx-openapi-history-collection-result-20250113-20250124.md]]
- [[_report/quant/research/2026-07-03-krx-openapi-history-collection-result-20250113-20250124.requests.json|_report/quant/research/2026-07-03-krx-openapi-history-collection-result-20250113-20250124.requests.json]]
- [[_report/quant/research/2026-07-03-krx-openapi-history-normalize-result-20250113-20250124|_report/quant/research/2026-07-03-krx-openapi-history-normalize-result-20250113-20250124.md]]
- [[_report/quant/research/2026-07-03-krx-openapi-history-normalize-result-20250102-20250124|_report/quant/research/2026-07-03-krx-openapi-history-normalize-result-20250102-20250124.md]]

Remaining limitation:

- The plan filters weekends only; it is not a verified KRX trading calendar.
- Holidays and unavailable dates must be interpreted from saved collector metadata and normalized row counts.
- This still does not provide historical managed issue, trading halt, market alert, or delisting replay.

## KRX OpenAPI Continuity Audit Smoke

Status: `passed_for_small_window`

Validated over normalized `2025-01-02` to `2025-01-24` rows:

| metric | value |
| --- | ---: |
| audited dates | 17 |
| row-count alerts | 0 |
| duplicate date/code keys | 0 |
| stock/issue code mismatches | 0 |

Artifacts:

- [[scripts/quant_krx_openapi_continuity_audit.py|scripts/quant_krx_openapi_continuity_audit.py]]
- [[tests/test_quant_krx_openapi_continuity_audit.py|tests/test_quant_krx_openapi_continuity_audit.py]]
- [[_report/quant/research/2026-07-03-krx-openapi-continuity-audit-20250102-20250110|_report/quant/research/2026-07-03-krx-openapi-continuity-audit-20250102-20250110.md]]
- [[_report/quant/research/2026-07-03-krx-openapi-continuity-audit-20250102-20250110.rows.csv|_report/quant/research/2026-07-03-krx-openapi-continuity-audit-20250102-20250110.rows.csv]]
- [[_report/quant/research/2026-07-03-krx-openapi-continuity-audit-20250113-20250124|_report/quant/research/2026-07-03-krx-openapi-continuity-audit-20250113-20250124.md]]
- [[_report/quant/research/2026-07-03-krx-openapi-continuity-audit-20250113-20250124.rows.csv|_report/quant/research/2026-07-03-krx-openapi-continuity-audit-20250113-20250124.rows.csv]]
- [[_report/quant/research/2026-07-03-krx-openapi-continuity-audit-20250102-20250124|_report/quant/research/2026-07-03-krx-openapi-continuity-audit-20250102-20250124.md]]
- [[_report/quant/research/2026-07-03-krx-openapi-continuity-audit-20250102-20250124.rows.csv|_report/quant/research/2026-07-03-krx-openapi-continuity-audit-20250102-20250124.rows.csv]]

Observed data movement:

- `2025-01-08` stock/issue rows dropped from `2745` to `2744` because KOSDAQ rows moved from `1784` to `1783`; this is below the alert threshold but still needs event-source validation before Backtest use.
- `2025-01-23` and `2025-01-24` increased to `2746` and `2749` stock/issue rows; this is also below the alert threshold but needs status/listing-event evidence before Backtest use.

## KRX OpenAPI Market Data Join Smoke

Status: `usable_for_date_scoped_market_data_input`

Joined normalized `stock_daily` and `issue_base` rows over `2025-01-02` to `2025-01-24`:

| metric | value |
| --- | ---: |
| joined rows | 46659 |
| date count | 17 |
| missing issue rows for stock rows | 0 |
| missing stock rows for issue rows | 0 |
| KOSPI rows | 16337 |
| KOSDAQ rows | 30322 |

Artifacts:

- [[scripts/quant_krx_openapi_market_data_join.py|scripts/quant_krx_openapi_market_data_join.py]]
- [[tests/test_quant_krx_openapi_market_data_join.py|tests/test_quant_krx_openapi_market_data_join.py]]
- [[_report/quant/research/2026-07-03-krx-openapi-market-data-join-20250102-20250110|_report/quant/research/2026-07-03-krx-openapi-market-data-join-20250102-20250110.md]]
- [[_report/quant/research/2026-07-03-krx-openapi-market-data-join-20250113-20250124|_report/quant/research/2026-07-03-krx-openapi-market-data-join-20250113-20250124.md]]
- [[_report/quant/research/2026-07-03-krx-openapi-market-data-join-20250102-20250124|_report/quant/research/2026-07-03-krx-openapi-market-data-join-20250102-20250124.md]]

Remaining limitation:

- This is a clean market-data input, not a `Point-in-Time Universe`; historical managed issue, trading halt, market alert, and delisting replay still need separate status sources.

## Point-in-Time Status Source Gap

Status: `source_gap_confirmed_for_openapi_core`

Official-source check:

- KRX OpenAPI service list covers market data and issue base rows but does not expose the needed managed issue, trading halt, market alert, or delisting event replay as a visible core OpenAPI service.
- KRX Data Marketplace stock `종목정보` pages, especially `전종목 지정내역`, are the next official candidate for status snapshots.
- KIND is the event/disclosure fallback candidate when KRX Data Marketplace does not provide a clean historical table.
- KRX Data Marketplace status-source probe identified official menu/screen/bld mappings for `전종목 지정내역`, `관리종목 현황`, `매매거래정지종목 현황`, `상장폐지종목 현황`, `정리매매종목 현황`, and market-alert pages.
- The same probe classified all core status JSON calls as `auth_required` because KRX returned `LOGOUT` without an authenticated Data Marketplace session.

Artifact:

- [[_report/quant/research/2026-07-03-point-in-time-status-source-gap|_report/quant/research/2026-07-03-point-in-time-status-source-gap.md]]
- [[_report/quant/research/2026-07-03-krx-data-marketplace-status-source-probe|_report/quant/research/2026-07-03-krx-data-marketplace-status-source-probe.md]]

Next gate:

- Save one authenticated/manual KRX Data Marketplace status raw sample or use KIND fallback before wiring status replay into `Universe`.

## Point-in-Time Status Event Schema

Status: `schema_scaffold_ready`

Implemented local contract:

- [[_report/quant/data/schemas/point_in_time_status_events.schema.json|_report/quant/data/schemas/point_in_time_status_events.schema.json]]
- [[_report/quant/data/point_in_time_status_sources.yaml|_report/quant/data/point_in_time_status_sources.yaml]]
- [[scripts/quant_point_in_time_status_events_validate.py|scripts/quant_point_in_time_status_events_validate.py]]
- [[tests/test_quant_point_in_time_status_events_validate.py|tests/test_quant_point_in_time_status_events_validate.py]]
- [[_report/quant/research/2026-07-03-point-in-time-status-event-schema|_report/quant/research/2026-07-03-point-in-time-status-event-schema.md]]
- [[scripts/quant_point_in_time_status_replay.py|scripts/quant_point_in_time_status_replay.py]]
- [[tests/test_quant_point_in_time_status_replay.py|tests/test_quant_point_in_time_status_replay.py]]
- [[_report/quant/research/2026-07-03-point-in-time-status-replay-scaffold|_report/quant/research/2026-07-03-point-in-time-status-replay-scaffold.md]]

Validator checks:

- Required normalized columns are present.
- `event_date` is ISO `YYYY-MM-DD`.
- KRX short codes preserve alphanumeric symbols.
- `market`, `status_type`, `status_value`, `source`, and `confidence` stay inside explicit allowlists.
- `raw_path` remains repo-relative under `_report/raw/**`.
- `source_url` follows the configured source policy when present.

Next gate:

- Save one official KRX Data Marketplace or KIND status raw sample under `_report/raw/**`, normalize it into this schema, and run the validator.

## Point-in-Time Status Replay Scaffold

Status: `replay_scaffold_ready_for_validated_events`

Implemented local replay:

- Validates status events with [[scripts/quant_point_in_time_status_events_validate.py|scripts/quant_point_in_time_status_events_validate.py]] before replay.
- Applies events where `event_date <= market-data date`.
- Emits row-level `pit_*` fields for active managed issue, trading halt, market alert, and delisting state.
- Keeps `include_by_status_event` explicitly scoped to the provided event rows; it is not full official status coverage.

Artifact:

- [[_report/quant/research/2026-07-03-point-in-time-status-replay-scaffold|_report/quant/research/2026-07-03-point-in-time-status-replay-scaffold.md]]

Next gate:

- After one official raw status sample is normalized and validated, run the replay scaffold against the 17-date KRX OpenAPI market-data join.

Soft blockers:

- KRX Data Marketplace status JSON endpoints returned `auth_required`/`LOGOUT` in unattended probes.
- KRX downloads are manual or authenticated snapshots, not yet automated reproducible downloads.
- KRX `관리종목 지정 내역(개별종목)` has range/UI constraints and is not a full historical Universe source.
- Some current KRX codes are alphanumeric short codes, so code handling must preserve values such as `0004V0`.

## Next Implementation Steps

### Step A. Connect Universe to OHLCV Batch Collection

Goal:

- Stop relying on manually selected raw files for Liquidity Filter coverage.
- Use generated current Universe rows as the batch input list for KIS daily OHLCV collection.

Current implemented path:

- [[scripts/quant_kis_ohlcv_batch_plan.py|scripts/quant_kis_ohlcv_batch_plan.py]] reads generated Universe rows and emits a resumable request queue.
- [[_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-batch-plan|_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-batch-plan.md]] records a first dry-run with `10` requests.
- [[_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-batch-plan-next10|_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-batch-plan-next10.md]] records the next `10` requests after skipping existing raw.
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-third10|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-third10.md]] records the third `10` requests after skipping `20` existing raw files.
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-fourth10|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-fourth10.md]] records the fourth `10` requests after skipping `30` existing raw files.
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-fifth10|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-fifth10.md]], [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-sixth10|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-sixth10.md]], and [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-seventh10|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-seventh10.md]] record three more `10` request queues after skipping `40`, `50`, and `60` existing raw files.
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-eighth10|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-eighth10.md]], [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-ninth10|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-ninth10.md]], and [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-tenth10|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-tenth10.md]] record three more `10` request queues after skipping `70`, `80`, and `90` existing raw files.
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-eleventh10|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-eleventh10.md]], [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-twelfth10|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-twelfth10.md]], and [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-thirteenth10|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-thirteenth10.md]] record three more `10` request queues after skipping `100`, `110`, and `120` existing raw files.
- [[_report/quant/research/2026-06-18-krx-current-universe-v0-ohlcv-batch-plan-fourteenth10|_report/quant/research/2026-06-18-krx-current-universe-v0-ohlcv-batch-plan-fourteenth10.md]], [[_report/quant/research/2026-06-18-krx-current-universe-v0-ohlcv-batch-plan-fifteenth10|_report/quant/research/2026-06-18-krx-current-universe-v0-ohlcv-batch-plan-fifteenth10.md]], and [[_report/quant/research/2026-06-18-krx-current-universe-v0-ohlcv-batch-plan-sixteenth10|_report/quant/research/2026-06-18-krx-current-universe-v0-ohlcv-batch-plan-sixteenth10.md]] record three more `10` request queues after skipping `130`, `140`, and `150` existing raw files.
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-seventeenth10|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-seventeenth10.md]], [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-eighteenth10|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-eighteenth10.md]], and [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-nineteenth10|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-nineteenth10.md]] record three more `10` request queues after skipping `160`, `170`, and `180` existing raw files.
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentieth10|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentieth10.md]], [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyfirst10|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyfirst10.md]], [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentysecond10|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentysecond10.md]], [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentythird10|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentythird10.md]], and [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyfourth10|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyfourth10.md]] record five more `10` request queues after skipping `190`, `200`, `210`, `220`, and `230` existing raw files.
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyfifth10|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyfifth10.md]], [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentysixth10|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentysixth10.md]], [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyseventh10|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyseventh10.md]], [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyeighth10|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyeighth10.md]], and [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyninth10|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyninth10.md]] record five more `10` request queues after skipping `240`, `250`, `260`, `270`, and `280` existing raw files.
- [[_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtieth10|_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtieth10.md]] records one more `10` request queue after skipping `290` existing raw files.
- [[_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtyfirst10|_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtyfirst10.md]], [[_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtysecond10|_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtysecond10.md]], [[_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtythird10|_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtythird10.md]], [[_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtyfourth10|_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtyfourth10.md]], and [[_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtyfifth10|_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtyfifth10.md]] record five more `10` request queues after skipping `300`, `310`, `320`, `330`, and `340` existing raw files.
- [[_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtysixth10|_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtysixth10.md]] records one more `10` request queue after skipping `350` existing raw files.
- [[_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-batch-plan-next10.requests.jsonl|_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-batch-plan-next10.requests.jsonl]] is a machine-readable request queue.
- [[_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-batch-plan.requests.jsonl|_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-batch-plan.requests.jsonl]] is a machine-readable request queue.
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-third10.requests.jsonl|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-third10.requests.jsonl]] is the machine-readable third request queue.
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-fourth10.requests.jsonl|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-fourth10.requests.jsonl]] is the machine-readable fourth request queue.
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-fifth10.requests.jsonl|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-fifth10.requests.jsonl]], [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-sixth10.requests.jsonl|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-sixth10.requests.jsonl]], and [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-seventh10.requests.jsonl|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-seventh10.requests.jsonl]] are the machine-readable fifth through seventh request queues.
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-eighth10.requests.jsonl|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-eighth10.requests.jsonl]], [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-ninth10.requests.jsonl|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-ninth10.requests.jsonl]], and [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-tenth10.requests.jsonl|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-tenth10.requests.jsonl]] are the machine-readable eighth through tenth request queues.
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-eleventh10.requests.jsonl|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-eleventh10.requests.jsonl]], [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-twelfth10.requests.jsonl|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-twelfth10.requests.jsonl]], and [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-thirteenth10.requests.jsonl|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-thirteenth10.requests.jsonl]] are the machine-readable eleventh through thirteenth request queues.
- [[_report/quant/research/2026-06-18-krx-current-universe-v0-ohlcv-batch-plan-fourteenth10.requests.jsonl|_report/quant/research/2026-06-18-krx-current-universe-v0-ohlcv-batch-plan-fourteenth10.requests.jsonl]], [[_report/quant/research/2026-06-18-krx-current-universe-v0-ohlcv-batch-plan-fifteenth10.requests.jsonl|_report/quant/research/2026-06-18-krx-current-universe-v0-ohlcv-batch-plan-fifteenth10.requests.jsonl]], and [[_report/quant/research/2026-06-18-krx-current-universe-v0-ohlcv-batch-plan-sixteenth10.requests.jsonl|_report/quant/research/2026-06-18-krx-current-universe-v0-ohlcv-batch-plan-sixteenth10.requests.jsonl]] are the machine-readable fourteenth through sixteenth request queues.
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-seventeenth10.requests.jsonl|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-seventeenth10.requests.jsonl]], [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-eighteenth10.requests.jsonl|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-eighteenth10.requests.jsonl]], and [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-nineteenth10.requests.jsonl|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-nineteenth10.requests.jsonl]] are the machine-readable seventeenth through nineteenth request queues.
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentieth10.requests.jsonl|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentieth10.requests.jsonl]], [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyfirst10.requests.jsonl|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyfirst10.requests.jsonl]], [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentysecond10.requests.jsonl|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentysecond10.requests.jsonl]], [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentythird10.requests.jsonl|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentythird10.requests.jsonl]], and [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyfourth10.requests.jsonl|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyfourth10.requests.jsonl]] are the machine-readable twentieth through twentyfourth request queues.
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyfifth10.requests.jsonl|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyfifth10.requests.jsonl]], [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentysixth10.requests.jsonl|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentysixth10.requests.jsonl]], [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyseventh10.requests.jsonl|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyseventh10.requests.jsonl]], [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyeighth10.requests.jsonl|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyeighth10.requests.jsonl]], and [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyninth10.requests.jsonl|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyninth10.requests.jsonl]] are the machine-readable twentyfifth through twentyninth request queues.
- [[_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtieth10.requests.jsonl|_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtieth10.requests.jsonl]] is the machine-readable thirtieth request queue.
- [[_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtyfirst10.requests.jsonl|_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtyfirst10.requests.jsonl]], [[_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtysecond10.requests.jsonl|_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtysecond10.requests.jsonl]], [[_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtythird10.requests.jsonl|_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtythird10.requests.jsonl]], [[_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtyfourth10.requests.jsonl|_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtyfourth10.requests.jsonl]], and [[_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtyfifth10.requests.jsonl|_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtyfifth10.requests.jsonl]] are the machine-readable thirtyfirst through thirtyfifth request queues.
- [[_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtysixth10.requests.jsonl|_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtysixth10.requests.jsonl]] is the machine-readable thirtysixth request queue.

Guardrail:

- KIS data calls must still be preflighted with `find_api_detail`.
- Raw responses stay under `_report/raw/**` and are not committed.
- The current Codex App surface did not expose the KIS MCP tool, so `find_api_detail` could not be called directly here. The first live subset used local KIS config/example API detail as a fallback and called only the read-only quotation endpoint through `examples_llm/kis_auth.py`.

Next gate:

- In a surface with KIS MCP access, run `domestic_stock.find_api_detail` for `inquire_daily_itemchartprice`. Then continue small resumable OHLCV capture batches from `--skip-existing` state `360`, save raw responses under `_report/raw/2026/2026-06-15/quant/universe-ohlcv/`, and re-run [[scripts/quant_liquidity_filter.py|scripts/quant_liquidity_filter.py]].

### Step B. Expand Liquidity Filter Coverage

Current implemented path:

- [[scripts/quant_liquidity_filter.py|scripts/quant_liquidity_filter.py]] reads current Universe rows and saved KIS daily raw files.
- [[_report/quant/research/2026-06-15-krx-current-universe-v0-liquidity-smoke-expanded|_report/quant/research/2026-06-15-krx-current-universe-v0-liquidity-smoke-expanded.md]] records the expanded paper/smoke run.
- [[_report/quant/research/2026-07-01-krx-current-universe-v0-liquidity-smoke-expanded-thirtysixth10|_report/quant/research/2026-07-01-krx-current-universe-v0-liquidity-smoke-expanded-thirtysixth10.md]] records the latest expanded paper/smoke run.
- Latest expanded run evaluates `361` saved raw rows against the current Universe: `180` pass, `181` fail, `2029` `liquidity_raw_missing`, and `485` `not_evaluated_preexisting_exclude`.
- Saved raw coverage currently evaluates 361 unique rows. See [[_report/quant/research/2026-07-01-krx-current-universe-v0-liquidity-smoke-expanded-thirtysixth10.rows.csv|_report/quant/research/2026-07-01-krx-current-universe-v0-liquidity-smoke-expanded-thirtysixth10.rows.csv]] for the authoritative pass/fail row set.

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

- [[_report/quant/templates/backtest-report|_report/quant/templates/backtest-report.md]] based result document.
- Bias Control checklist attached.

## Current Completion Judgment

The project is beyond planning and has a usable current-snapshot data artifact. However, it is not yet a Backtest-ready Quant system.

Current state:

- Research and policy foundation: strong enough to proceed.
- Current Snapshot Universe: usable for paper/smoke validation.
- KRX OpenAPI core raw collection and normalization: usable for parser development and historical market-data collection.
- KRX OpenAPI date-scoped market-data join: usable as a 17-date smoke input for status replay development.
- KRX Data Marketplace status-source probe: official status screen `bld` identifiers found, but unattended JSON access is `auth_required`.
- Point-in-Time status-event schema: ready for one official raw sample normalization test.
- Point-in-Time status replay scaffold: ready for validated status-event rows.
- Backtest readiness: `hold`.
- Live trading readiness: `blocked`.
