# Quant Implementation Roadmap

## Metadata

- Date: 2026-06-14
- Last updated: 2026-07-09
- Scope: Quant trading research and implementation workflow
- Current phase: `forward_price_81d_readiness_smoke`
- Overall implementation progress: `85-88%`
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
| 4. Point-in-Time Universe | in-progress | 78-81% | KRX OpenAPI market-data path works; two KIND current snapshots are merged into `497` logical status-event rows, 81-date local market enrichment reduces merged `UNKNOWN` market labels from `48` to `47`, a 72-date `Point-in-Time Universe` smoke produced `184549` include / `13588` exclude rows, and status coverage audit keeps this at `hold` because the source is still `current_snapshot_smoke` with `0` release/resume-like events and no source coverage manifest; lifecycle gap report identifies `304` code/status groups that need release/resume evidence | Obtain historical transition coverage plus a source coverage manifest, then keep Universe eligibility smoke aligned |
| 5. Market data pipeline | in-progress | 95-97% | KIS raw save, smoke validators, Universe OHLCV queue, first 360 KIS captures, KRX OpenAPI core raw collector/normalizer, 72-date historical status-replay market-data merge, 81-date forward-price merge through `2025-05-02`, continuity audit, date-scoped market-data join, status replay smoke, and resumable existing-raw verification exist | Extend status coverage, not only prices, before Backtest promotion |
| 6. Liquidity Filter | in-progress | 72-76% | [[scripts/quant_liquidity_filter.py|scripts/quant_liquidity_filter.py]] evaluates 361 current Universe saved-raw rows; [[scripts/quant_point_in_time_liquidity_filter.py|scripts/quant_point_in_time_liquidity_filter.py]] produced a 72-date, 20-day Point-in-Time smoke with `54138` include rows and `135316` full-lookback rows | Keep 20-day rule aligned while status coverage expands |
| 7. Backtest engine connection | preflight | 47-52% | [[scripts/quant_backtest_input_contract_validate.py|scripts/quant_backtest_input_contract_validate.py]] validates the 72-date, 20-day smoke artifacts as internally joinable, [[scripts/quant_backtest_pnl_smoke.py|scripts/quant_backtest_pnl_smoke.py]] computes diagnostic weighted-return and benchmark-excess smoke rows with complete 1-day target coverage after extending prices through `2025-05-02`, [[scripts/quant_backtest_assumptions_validate.py|scripts/quant_backtest_assumptions_validate.py]] validates local cost/benchmark assumptions as `pass_assumption_only`, and [[scripts/quant_benchmark_return_smoke.py|scripts/quant_benchmark_return_smoke.py]] computes complete benchmark return smoke rows, while Backtest remains `hold` | Wire engine only after Point-in-Time status coverage, actual fee override, production benchmark attribution, OOS, and Bias Control are acceptable |
| 8. OOS / Walk-Forward | planned | 10% | OOS plan exists | Run only after Backtest pipeline works |
| 9. Bias Control pass | hold | 20% | Bias checklists exist; blockers documented | Point-in-Time and OOS evidence |
| 10. Paper Signal tracking | partial | 76-80% | 72-date, 20-day Point-in-Time Liquidity rows now feed `2120` paper-only Momentum `Signal Candidate` rows, complete `1,5` trading-day forward-return coverage using prices through `2025-05-02`, long-only portfolio target, Backtest input contract, and PnL smoke outputs | Keep candidates signal-only until production Point-in-Time coverage, Backtest, OOS, and Bias Control pass |
| 11. Execution / live trading | blocked | 5% | Demo-only order intent preflight exists; no KIS order executor exists | Only after Backtest/OOS/Bias Control pass |

## Completed Artifacts

Latest 2026-07-08 forward-price coverage artifacts for the existing 72-date signal window:

- [[_report/quant/research/2026-07-08-krx-openapi-history-plan-20250421-20250502|_report/quant/research/2026-07-08-krx-openapi-history-plan-20250421-20250502.md]]
- [[_report/quant/research/2026-07-08-krx-openapi-history-plan-20250421-20250502.requests.json|_report/quant/research/2026-07-08-krx-openapi-history-plan-20250421-20250502.requests.json]]
- [[_report/quant/research/2026-07-08-krx-openapi-history-collection-result-20250421-20250502|_report/quant/research/2026-07-08-krx-openapi-history-collection-result-20250421-20250502.md]]
- [[_report/quant/research/2026-07-08-krx-openapi-history-collection-result-20250421-20250502.requests.json|_report/quant/research/2026-07-08-krx-openapi-history-collection-result-20250421-20250502.requests.json]]
- [[_report/quant/research/2026-07-08-krx-openapi-history-normalize-result-20250421-20250502|_report/quant/research/2026-07-08-krx-openapi-history-normalize-result-20250421-20250502.md]]
- [[_report/quant/research/2026-07-08-krx-openapi-continuity-audit-20250421-20250502|_report/quant/research/2026-07-08-krx-openapi-continuity-audit-20250421-20250502.md]]
- [[_report/quant/research/2026-07-08-krx-openapi-continuity-audit-20250421-20250502.rows.csv|_report/quant/research/2026-07-08-krx-openapi-continuity-audit-20250421-20250502.rows.csv]]
- [[_report/quant/research/2026-07-08-krx-openapi-market-data-join-20250421-20250502|_report/quant/research/2026-07-08-krx-openapi-market-data-join-20250421-20250502.md]]
- [[_report/quant/research/2026-07-08-krx-openapi-market-data-merge-20250102-20250502|_report/quant/research/2026-07-08-krx-openapi-market-data-merge-20250102-20250502.md]]
- [[_report/quant/research/2026-07-08-signal-forward-return-smoke-20d-20250102-20250418-price-through-20250502|_report/quant/research/2026-07-08-signal-forward-return-smoke-20d-20250102-20250418-price-through-20250502.md]]
- [[_report/quant/research/2026-07-08-signal-forward-return-smoke-20d-20250102-20250418-price-through-20250502.rows.csv|_report/quant/research/2026-07-08-signal-forward-return-smoke-20d-20250102-20250418-price-through-20250502.rows.csv]]
- [[_report/quant/research/2026-07-08-benchmark-return-smoke-20d-20250102-20250418-price-through-20250502|_report/quant/research/2026-07-08-benchmark-return-smoke-20d-20250102-20250418-price-through-20250502.md]]
- [[_report/quant/research/2026-07-08-benchmark-return-smoke-20d-20250102-20250418-price-through-20250502.rows.csv|_report/quant/research/2026-07-08-benchmark-return-smoke-20d-20250102-20250418-price-through-20250502.rows.csv]]
- [[_report/quant/research/2026-07-08-backtest-pnl-smoke-20d-20250102-20250418-price-through-20250502|_report/quant/research/2026-07-08-backtest-pnl-smoke-20d-20250102-20250418-price-through-20250502.md]]
- [[_report/quant/research/2026-07-08-backtest-pnl-smoke-20d-20250102-20250418-price-through-20250502.rows.csv|_report/quant/research/2026-07-08-backtest-pnl-smoke-20d-20250102-20250418-price-through-20250502.rows.csv]]
- [[_report/quant/research/2026-07-08-quant-readiness-check-20d-20250102-20250418-price-through-20250502|_report/quant/research/2026-07-08-quant-readiness-check-20d-20250102-20250418-price-through-20250502.md]]
- [[_report/quant/research/2026-07-09-quant-readiness-check-20d-20250102-20250418-price-through-20250502-lifecycle-gaps|_report/quant/research/2026-07-09-quant-readiness-check-20d-20250102-20250418-price-through-20250502-lifecycle-gaps.md]]
- [[_report/quant/research/2026-07-09-quant-readiness-check-20d-20250102-20250418-price-through-20250502-market-enriched-81d-status|_report/quant/research/2026-07-09-quant-readiness-check-20d-20250102-20250418-price-through-20250502-market-enriched-81d-status.md]]

Baseline 2026-07-08 72-date smoke artifacts:

- [[_report/quant/research/2026-07-08-krx-openapi-history-plan-20250407-20250418|_report/quant/research/2026-07-08-krx-openapi-history-plan-20250407-20250418.md]]
- [[_report/quant/research/2026-07-08-krx-openapi-history-plan-20250407-20250418.requests.json|_report/quant/research/2026-07-08-krx-openapi-history-plan-20250407-20250418.requests.json]]
- [[_report/quant/research/2026-07-08-krx-openapi-history-collection-result-20250407-20250418|_report/quant/research/2026-07-08-krx-openapi-history-collection-result-20250407-20250418.md]]
- [[_report/quant/research/2026-07-08-krx-openapi-history-collection-result-20250407-20250418.requests.json|_report/quant/research/2026-07-08-krx-openapi-history-collection-result-20250407-20250418.requests.json]]
- [[_report/quant/research/2026-07-08-krx-openapi-history-normalize-result-20250407-20250418|_report/quant/research/2026-07-08-krx-openapi-history-normalize-result-20250407-20250418.md]]
- [[_report/quant/research/2026-07-08-krx-openapi-continuity-audit-20250407-20250418|_report/quant/research/2026-07-08-krx-openapi-continuity-audit-20250407-20250418.md]]
- [[_report/quant/research/2026-07-08-krx-openapi-continuity-audit-20250407-20250418.rows.csv|_report/quant/research/2026-07-08-krx-openapi-continuity-audit-20250407-20250418.rows.csv]]
- [[_report/quant/research/2026-07-08-krx-openapi-market-data-join-20250407-20250418|_report/quant/research/2026-07-08-krx-openapi-market-data-join-20250407-20250418.md]]
- [[_report/quant/research/2026-07-08-krx-openapi-market-data-merge-20250102-20250418|_report/quant/research/2026-07-08-krx-openapi-market-data-merge-20250102-20250418.md]]
- [[_report/quant/research/2026-07-08-kind-status-replay-on-openapi-20250102-20250418-merged-snapshots|_report/quant/research/2026-07-08-kind-status-replay-on-openapi-20250102-20250418-merged-snapshots.md]]
- [[_report/quant/research/2026-07-08-kind-status-replay-on-openapi-20250102-20250418-merged-snapshots.rows.csv|_report/quant/research/2026-07-08-kind-status-replay-on-openapi-20250102-20250418-merged-snapshots.rows.csv]]
- [[_report/quant/research/2026-07-08-point-in-time-status-coverage-audit-20250102-20250418-merged-snapshots|_report/quant/research/2026-07-08-point-in-time-status-coverage-audit-20250102-20250418-merged-snapshots.md]]
- [[_report/quant/research/2026-07-08-point-in-time-status-coverage-audit-20250102-20250418-merged-snapshots.rows.csv|_report/quant/research/2026-07-08-point-in-time-status-coverage-audit-20250102-20250418-merged-snapshots.rows.csv]]
- [[_report/quant/research/2026-07-09-kind-status-events-merged-market-enrich-81d|_report/quant/research/2026-07-09-kind-status-events-merged-market-enrich-81d.md]]
- [[_report/quant/research/2026-07-09-kind-status-events-merged-market-enriched-81d-validation|_report/quant/research/2026-07-09-kind-status-events-merged-market-enriched-81d-validation.md]]
- [[_report/quant/research/2026-07-09-kind-status-events-merged-market-enriched-81d-validation.rows.csv|_report/quant/research/2026-07-09-kind-status-events-merged-market-enriched-81d-validation.rows.csv]]
- [[_report/quant/research/2026-07-09-kind-status-events-unknown-market-targets-market-enriched-81d|_report/quant/research/2026-07-09-kind-status-events-unknown-market-targets-market-enriched-81d.md]]
- [[_report/quant/research/2026-07-09-kind-status-events-unknown-market-targets-market-enriched-81d.rows.csv|_report/quant/research/2026-07-09-kind-status-events-unknown-market-targets-market-enriched-81d.rows.csv]]
- [[_report/quant/research/2026-07-09-point-in-time-status-coverage-audit-20250102-20250418-merged-snapshots-market-enriched-81d|_report/quant/research/2026-07-09-point-in-time-status-coverage-audit-20250102-20250418-merged-snapshots-market-enriched-81d.md]]
- [[_report/quant/research/2026-07-09-point-in-time-status-coverage-audit-20250102-20250418-merged-snapshots-market-enriched-81d.rows.csv|_report/quant/research/2026-07-09-point-in-time-status-coverage-audit-20250102-20250418-merged-snapshots-market-enriched-81d.rows.csv]]
- [[_report/quant/research/2026-07-09-point-in-time-status-lifecycle-gaps-20250102-20250418-merged-snapshots-market-enriched-81d|_report/quant/research/2026-07-09-point-in-time-status-lifecycle-gaps-20250102-20250418-merged-snapshots-market-enriched-81d.md]]
- [[_report/quant/research/2026-07-09-point-in-time-status-lifecycle-gaps-20250102-20250418-merged-snapshots-market-enriched-81d.rows.csv|_report/quant/research/2026-07-09-point-in-time-status-lifecycle-gaps-20250102-20250418-merged-snapshots-market-enriched-81d.rows.csv]]
- [[_report/quant/research/2026-07-08-kind-status-point-in-time-universe-smoke-merged-snapshots-20250102-20250418|_report/quant/research/2026-07-08-kind-status-point-in-time-universe-smoke-merged-snapshots-20250102-20250418.md]]
- [[_report/quant/research/2026-07-08-kind-status-point-in-time-universe-smoke-merged-snapshots-20250102-20250418.rows.csv|_report/quant/research/2026-07-08-kind-status-point-in-time-universe-smoke-merged-snapshots-20250102-20250418.rows.csv]]
- [[_report/quant/research/2026-07-08-kind-status-point-in-time-liquidity-smoke-20d-20250102-20250418|_report/quant/research/2026-07-08-kind-status-point-in-time-liquidity-smoke-20d-20250102-20250418.md]]
- [[_report/quant/research/2026-07-08-kind-status-point-in-time-liquidity-smoke-20d-20250102-20250418.rows.csv|_report/quant/research/2026-07-08-kind-status-point-in-time-liquidity-smoke-20d-20250102-20250418.rows.csv]]
- [[_report/quant/research/2026-07-08-kind-status-point-in-time-momentum-signal-candidates-smoke-20d-20250102-20250418|_report/quant/research/2026-07-08-kind-status-point-in-time-momentum-signal-candidates-smoke-20d-20250102-20250418.md]]
- [[_report/quant/research/2026-07-08-kind-status-point-in-time-momentum-signal-candidates-smoke-20d-20250102-20250418.rows.csv|_report/quant/research/2026-07-08-kind-status-point-in-time-momentum-signal-candidates-smoke-20d-20250102-20250418.rows.csv]]
- [[_report/quant/research/2026-07-08-signal-forward-return-smoke-20d-20250102-20250418|_report/quant/research/2026-07-08-signal-forward-return-smoke-20d-20250102-20250418.md]]
- [[_report/quant/research/2026-07-08-signal-forward-return-smoke-20d-20250102-20250418.rows.csv|_report/quant/research/2026-07-08-signal-forward-return-smoke-20d-20250102-20250418.rows.csv]]
- [[_report/quant/research/2026-07-08-signal-portfolio-targets-smoke-20d-20250102-20250418|_report/quant/research/2026-07-08-signal-portfolio-targets-smoke-20d-20250102-20250418.md]]
- [[_report/quant/research/2026-07-08-signal-portfolio-targets-smoke-20d-20250102-20250418.rows.csv|_report/quant/research/2026-07-08-signal-portfolio-targets-smoke-20d-20250102-20250418.rows.csv]]
- [[_report/quant/research/2026-07-08-backtest-input-contract-validate-20250102-20250418|_report/quant/research/2026-07-08-backtest-input-contract-validate-20250102-20250418.md]]
- [[_report/quant/research/2026-07-08-backtest-pnl-smoke-20d-20250102-20250418|_report/quant/research/2026-07-08-backtest-pnl-smoke-20d-20250102-20250418.md]]
- [[_report/quant/research/2026-07-08-backtest-pnl-smoke-20d-20250102-20250418.rows.csv|_report/quant/research/2026-07-08-backtest-pnl-smoke-20d-20250102-20250418.rows.csv]]
- [[_report/quant/research/2026-07-08-benchmark-return-smoke-20d-20250102-20250418|_report/quant/research/2026-07-08-benchmark-return-smoke-20d-20250102-20250418.md]]
- [[_report/quant/research/2026-07-08-benchmark-return-smoke-20d-20250102-20250418.rows.csv|_report/quant/research/2026-07-08-benchmark-return-smoke-20d-20250102-20250418.rows.csv]]
- [[_report/quant/research/2026-07-08-quant-readiness-check-20d-20250102-20250418-merged-status|_report/quant/research/2026-07-08-quant-readiness-check-20d-20250102-20250418-merged-status.md]]

Previous 62-date baseline artifacts:

- [[_report/quant/research/2026-07-08-krx-openapi-history-plan-20250324-20250404|_report/quant/research/2026-07-08-krx-openapi-history-plan-20250324-20250404.md]]
- [[_report/quant/research/2026-07-08-krx-openapi-history-plan-20250324-20250404.requests.json|_report/quant/research/2026-07-08-krx-openapi-history-plan-20250324-20250404.requests.json]]
- [[_report/quant/research/2026-07-08-krx-openapi-history-collection-result-20250324-20250404|_report/quant/research/2026-07-08-krx-openapi-history-collection-result-20250324-20250404.md]]
- [[_report/quant/research/2026-07-08-krx-openapi-history-collection-result-20250324-20250404.requests.json|_report/quant/research/2026-07-08-krx-openapi-history-collection-result-20250324-20250404.requests.json]]
- [[_report/quant/research/2026-07-08-krx-openapi-history-normalize-result-20250324-20250404|_report/quant/research/2026-07-08-krx-openapi-history-normalize-result-20250324-20250404.md]]
- [[_report/quant/research/2026-07-08-krx-openapi-continuity-audit-20250324-20250404|_report/quant/research/2026-07-08-krx-openapi-continuity-audit-20250324-20250404.md]]
- [[_report/quant/research/2026-07-08-krx-openapi-continuity-audit-20250324-20250404.rows.csv|_report/quant/research/2026-07-08-krx-openapi-continuity-audit-20250324-20250404.rows.csv]]
- [[_report/quant/research/2026-07-08-krx-openapi-market-data-join-20250324-20250404|_report/quant/research/2026-07-08-krx-openapi-market-data-join-20250324-20250404.md]]
- [[_report/quant/research/2026-07-08-krx-openapi-market-data-merge-20250102-20250404|_report/quant/research/2026-07-08-krx-openapi-market-data-merge-20250102-20250404.md]]
- [[_report/quant/research/2026-07-08-kind-status-replay-on-openapi-20250102-20250404-merged-snapshots|_report/quant/research/2026-07-08-kind-status-replay-on-openapi-20250102-20250404-merged-snapshots.md]]
- [[_report/quant/research/2026-07-08-kind-status-replay-on-openapi-20250102-20250404-merged-snapshots.rows.csv|_report/quant/research/2026-07-08-kind-status-replay-on-openapi-20250102-20250404-merged-snapshots.rows.csv]]
- [[_report/quant/research/2026-07-08-point-in-time-status-coverage-audit-20250102-20250404-merged-snapshots|_report/quant/research/2026-07-08-point-in-time-status-coverage-audit-20250102-20250404-merged-snapshots.md]]
- [[_report/quant/research/2026-07-08-point-in-time-status-coverage-audit-20250102-20250404-merged-snapshots.rows.csv|_report/quant/research/2026-07-08-point-in-time-status-coverage-audit-20250102-20250404-merged-snapshots.rows.csv]]
- [[_report/quant/research/2026-07-08-kind-status-point-in-time-universe-smoke-merged-snapshots-20250102-20250404|_report/quant/research/2026-07-08-kind-status-point-in-time-universe-smoke-merged-snapshots-20250102-20250404.md]]
- [[_report/quant/research/2026-07-08-kind-status-point-in-time-universe-smoke-merged-snapshots-20250102-20250404.rows.csv|_report/quant/research/2026-07-08-kind-status-point-in-time-universe-smoke-merged-snapshots-20250102-20250404.rows.csv]]
- [[_report/quant/research/2026-07-08-kind-status-point-in-time-liquidity-smoke-20d-20250102-20250404|_report/quant/research/2026-07-08-kind-status-point-in-time-liquidity-smoke-20d-20250102-20250404.md]]
- [[_report/quant/research/2026-07-08-kind-status-point-in-time-liquidity-smoke-20d-20250102-20250404.rows.csv|_report/quant/research/2026-07-08-kind-status-point-in-time-liquidity-smoke-20d-20250102-20250404.rows.csv]]
- [[_report/quant/research/2026-07-08-kind-status-point-in-time-momentum-signal-candidates-smoke-20d-20250102-20250404|_report/quant/research/2026-07-08-kind-status-point-in-time-momentum-signal-candidates-smoke-20d-20250102-20250404.md]]
- [[_report/quant/research/2026-07-08-kind-status-point-in-time-momentum-signal-candidates-smoke-20d-20250102-20250404.rows.csv|_report/quant/research/2026-07-08-kind-status-point-in-time-momentum-signal-candidates-smoke-20d-20250102-20250404.rows.csv]]
- [[_report/quant/research/2026-07-08-signal-forward-return-smoke-20d-20250102-20250404|_report/quant/research/2026-07-08-signal-forward-return-smoke-20d-20250102-20250404.md]]
- [[_report/quant/research/2026-07-08-signal-forward-return-smoke-20d-20250102-20250404.rows.csv|_report/quant/research/2026-07-08-signal-forward-return-smoke-20d-20250102-20250404.rows.csv]]
- [[_report/quant/research/2026-07-08-signal-portfolio-targets-smoke-20d-20250102-20250404|_report/quant/research/2026-07-08-signal-portfolio-targets-smoke-20d-20250102-20250404.md]]
- [[_report/quant/research/2026-07-08-signal-portfolio-targets-smoke-20d-20250102-20250404.rows.csv|_report/quant/research/2026-07-08-signal-portfolio-targets-smoke-20d-20250102-20250404.rows.csv]]
- [[_report/quant/research/2026-07-08-backtest-input-contract-validate-20250102-20250404|_report/quant/research/2026-07-08-backtest-input-contract-validate-20250102-20250404.md]]
- [[_report/quant/research/2026-07-08-backtest-pnl-smoke-20d-20250102-20250404|_report/quant/research/2026-07-08-backtest-pnl-smoke-20d-20250102-20250404.md]]
- [[_report/quant/research/2026-07-08-backtest-pnl-smoke-20d-20250102-20250404.rows.csv|_report/quant/research/2026-07-08-backtest-pnl-smoke-20d-20250102-20250404.rows.csv]]
- [[_report/quant/research/2026-07-08-backtest-cost-benchmark-assumptions-validate|_report/quant/research/2026-07-08-backtest-cost-benchmark-assumptions-validate.md]]
- [[_report/quant/research/2026-07-08-benchmark-return-smoke-20d-20250102-20250404|_report/quant/research/2026-07-08-benchmark-return-smoke-20d-20250102-20250404.md]]
- [[_report/quant/research/2026-07-08-benchmark-return-smoke-20d-20250102-20250404.rows.csv|_report/quant/research/2026-07-08-benchmark-return-smoke-20d-20250102-20250404.rows.csv]]
- [[_report/quant/research/2026-07-08-quant-readiness-check-20d-20250102-20250404-merged-status|_report/quant/research/2026-07-08-quant-readiness-check-20d-20250102-20250404-merged-status.md]]

Previous 52-date baseline artifacts:

- [[_report/quant/research/2026-07-08-krx-openapi-history-plan-20250310-20250321|_report/quant/research/2026-07-08-krx-openapi-history-plan-20250310-20250321.md]]
- [[_report/quant/research/2026-07-08-krx-openapi-history-plan-20250310-20250321.requests.json|_report/quant/research/2026-07-08-krx-openapi-history-plan-20250310-20250321.requests.json]]
- [[_report/quant/research/2026-07-08-krx-openapi-history-collection-result-20250310-20250321|_report/quant/research/2026-07-08-krx-openapi-history-collection-result-20250310-20250321.md]]
- [[_report/quant/research/2026-07-08-krx-openapi-history-collection-result-20250310-20250321.requests.json|_report/quant/research/2026-07-08-krx-openapi-history-collection-result-20250310-20250321.requests.json]]
- [[_report/quant/research/2026-07-08-krx-openapi-history-normalize-result-20250310-20250321|_report/quant/research/2026-07-08-krx-openapi-history-normalize-result-20250310-20250321.md]]
- [[_report/quant/research/2026-07-08-krx-openapi-continuity-audit-20250310-20250321|_report/quant/research/2026-07-08-krx-openapi-continuity-audit-20250310-20250321.md]]
- [[_report/quant/research/2026-07-08-krx-openapi-continuity-audit-20250310-20250321.rows.csv|_report/quant/research/2026-07-08-krx-openapi-continuity-audit-20250310-20250321.rows.csv]]
- [[_report/quant/research/2026-07-08-krx-openapi-market-data-join-20250310-20250321|_report/quant/research/2026-07-08-krx-openapi-market-data-join-20250310-20250321.md]]
- [[_report/quant/research/2026-07-08-krx-openapi-market-data-merge-20250102-20250321|_report/quant/research/2026-07-08-krx-openapi-market-data-merge-20250102-20250321.md]]
- [[_report/quant/research/2026-07-08-kind-status-replay-on-openapi-20250102-20250321-merged-snapshots|_report/quant/research/2026-07-08-kind-status-replay-on-openapi-20250102-20250321-merged-snapshots.md]]
- [[_report/quant/research/2026-07-08-kind-status-replay-on-openapi-20250102-20250321-merged-snapshots.rows.csv|_report/quant/research/2026-07-08-kind-status-replay-on-openapi-20250102-20250321-merged-snapshots.rows.csv]]
- [[_report/quant/research/2026-07-08-point-in-time-status-coverage-audit-20250102-20250321-merged-snapshots|_report/quant/research/2026-07-08-point-in-time-status-coverage-audit-20250102-20250321-merged-snapshots.md]]
- [[_report/quant/research/2026-07-08-point-in-time-status-coverage-audit-20250102-20250321-merged-snapshots.rows.csv|_report/quant/research/2026-07-08-point-in-time-status-coverage-audit-20250102-20250321-merged-snapshots.rows.csv]]
- [[_report/quant/research/2026-07-08-kind-status-point-in-time-universe-smoke-merged-snapshots-20250102-20250321|_report/quant/research/2026-07-08-kind-status-point-in-time-universe-smoke-merged-snapshots-20250102-20250321.md]]
- [[_report/quant/research/2026-07-08-kind-status-point-in-time-universe-smoke-merged-snapshots-20250102-20250321.rows.csv|_report/quant/research/2026-07-08-kind-status-point-in-time-universe-smoke-merged-snapshots-20250102-20250321.rows.csv]]
- [[_report/quant/research/2026-07-08-kind-status-point-in-time-liquidity-smoke-20d-20250102-20250321|_report/quant/research/2026-07-08-kind-status-point-in-time-liquidity-smoke-20d-20250102-20250321.md]]
- [[_report/quant/research/2026-07-08-kind-status-point-in-time-liquidity-smoke-20d-20250102-20250321.rows.csv|_report/quant/research/2026-07-08-kind-status-point-in-time-liquidity-smoke-20d-20250102-20250321.rows.csv]]
- [[_report/quant/research/2026-07-08-kind-status-point-in-time-momentum-signal-candidates-smoke-20d-20250102-20250321|_report/quant/research/2026-07-08-kind-status-point-in-time-momentum-signal-candidates-smoke-20d-20250102-20250321.md]]
- [[_report/quant/research/2026-07-08-kind-status-point-in-time-momentum-signal-candidates-smoke-20d-20250102-20250321.rows.csv|_report/quant/research/2026-07-08-kind-status-point-in-time-momentum-signal-candidates-smoke-20d-20250102-20250321.rows.csv]]
- [[_report/quant/research/2026-07-08-signal-forward-return-smoke-20d-20250102-20250321|_report/quant/research/2026-07-08-signal-forward-return-smoke-20d-20250102-20250321.md]]
- [[_report/quant/research/2026-07-08-signal-forward-return-smoke-20d-20250102-20250321.rows.csv|_report/quant/research/2026-07-08-signal-forward-return-smoke-20d-20250102-20250321.rows.csv]]
- [[_report/quant/research/2026-07-08-signal-portfolio-targets-smoke-20d-20250102-20250321|_report/quant/research/2026-07-08-signal-portfolio-targets-smoke-20d-20250102-20250321.md]]
- [[_report/quant/research/2026-07-08-signal-portfolio-targets-smoke-20d-20250102-20250321.rows.csv|_report/quant/research/2026-07-08-signal-portfolio-targets-smoke-20d-20250102-20250321.rows.csv]]
- [[_report/quant/research/2026-07-08-backtest-input-contract-validate-20250102-20250321|_report/quant/research/2026-07-08-backtest-input-contract-validate-20250102-20250321.md]]
- [[_report/quant/research/2026-07-08-backtest-pnl-smoke-20d-20250102-20250321|_report/quant/research/2026-07-08-backtest-pnl-smoke-20d-20250102-20250321.md]]
- [[_report/quant/research/2026-07-08-backtest-pnl-smoke-20d-20250102-20250321.rows.csv|_report/quant/research/2026-07-08-backtest-pnl-smoke-20d-20250102-20250321.rows.csv]]
- [[_report/quant/research/2026-07-08-quant-readiness-check-20d-20250102-20250321-merged-status|_report/quant/research/2026-07-08-quant-readiness-check-20d-20250102-20250321-merged-status.md]]

- [[_report/quant/research/2026-07-08-krx-openapi-history-plan-20250224-20250307|_report/quant/research/2026-07-08-krx-openapi-history-plan-20250224-20250307.md]]
- [[_report/quant/research/2026-07-08-krx-openapi-history-plan-20250224-20250307.requests.json|_report/quant/research/2026-07-08-krx-openapi-history-plan-20250224-20250307.requests.json]]
- [[_report/quant/research/2026-07-08-krx-openapi-history-collection-result-20250224-20250307|_report/quant/research/2026-07-08-krx-openapi-history-collection-result-20250224-20250307.md]]
- [[_report/quant/research/2026-07-08-krx-openapi-history-collection-result-20250224-20250307.requests.json|_report/quant/research/2026-07-08-krx-openapi-history-collection-result-20250224-20250307.requests.json]]
- [[_report/quant/research/2026-07-08-krx-openapi-history-normalize-result-20250224-20250307|_report/quant/research/2026-07-08-krx-openapi-history-normalize-result-20250224-20250307.md]]
- [[_report/quant/research/2026-07-08-krx-openapi-continuity-audit-20250224-20250307|_report/quant/research/2026-07-08-krx-openapi-continuity-audit-20250224-20250307.md]]
- [[_report/quant/research/2026-07-08-krx-openapi-continuity-audit-20250224-20250307.rows.csv|_report/quant/research/2026-07-08-krx-openapi-continuity-audit-20250224-20250307.rows.csv]]
- [[_report/quant/research/2026-07-08-krx-openapi-market-data-join-20250224-20250307|_report/quant/research/2026-07-08-krx-openapi-market-data-join-20250224-20250307.md]]
- [[_report/quant/research/2026-07-08-krx-openapi-market-data-merge-20250102-20250307|_report/quant/research/2026-07-08-krx-openapi-market-data-merge-20250102-20250307.md]]
- [[_report/quant/research/2026-07-08-kind-status-replay-on-openapi-20250102-20250307|_report/quant/research/2026-07-08-kind-status-replay-on-openapi-20250102-20250307.md]]
- [[_report/quant/research/2026-07-08-kind-status-replay-on-openapi-20250102-20250307.rows.csv|_report/quant/research/2026-07-08-kind-status-replay-on-openapi-20250102-20250307.rows.csv]]
- [[_report/quant/research/2026-07-08-point-in-time-status-coverage-audit-20250102-20250307|_report/quant/research/2026-07-08-point-in-time-status-coverage-audit-20250102-20250307.md]]
- [[_report/quant/research/2026-07-08-point-in-time-status-coverage-audit-20250102-20250307.rows.csv|_report/quant/research/2026-07-08-point-in-time-status-coverage-audit-20250102-20250307.rows.csv]]
- [[_report/quant/research/2026-07-08-kind-status-source-probe|_report/quant/research/2026-07-08-kind-status-source-probe.md]]
- [[_report/quant/data/point_in_time_status_events/2026-07-08-kind-current-status-events.csv|_report/quant/data/point_in_time_status_events/2026-07-08-kind-current-status-events.csv]]
- [[_report/quant/research/2026-07-08-kind-status-events-extract|_report/quant/research/2026-07-08-kind-status-events-extract.md]]
- [[_report/quant/research/2026-07-08-kind-status-events-validation|_report/quant/research/2026-07-08-kind-status-events-validation.md]]
- [[_report/quant/research/2026-07-08-kind-status-events-validation.rows.csv|_report/quant/research/2026-07-08-kind-status-events-validation.rows.csv]]
- [[_report/quant/data/point_in_time_status_events/2026-07-08-kind-current-status-events.market-enriched-42d.csv|_report/quant/data/point_in_time_status_events/2026-07-08-kind-current-status-events.market-enriched-42d.csv]]
- [[_report/quant/research/2026-07-08-kind-status-events-market-enrich-42d|_report/quant/research/2026-07-08-kind-status-events-market-enrich-42d.md]]
- [[_report/quant/research/2026-07-08-kind-status-replay-on-openapi-20250102-20250307-second-snapshot|_report/quant/research/2026-07-08-kind-status-replay-on-openapi-20250102-20250307-second-snapshot.md]]
- [[_report/quant/research/2026-07-08-kind-status-replay-on-openapi-20250102-20250307-second-snapshot.rows.csv|_report/quant/research/2026-07-08-kind-status-replay-on-openapi-20250102-20250307-second-snapshot.rows.csv]]
- [[_report/quant/research/2026-07-08-point-in-time-status-coverage-audit-20250102-20250307-second-snapshot|_report/quant/research/2026-07-08-point-in-time-status-coverage-audit-20250102-20250307-second-snapshot.md]]
- [[_report/quant/research/2026-07-08-point-in-time-status-coverage-audit-20250102-20250307-second-snapshot.rows.csv|_report/quant/research/2026-07-08-point-in-time-status-coverage-audit-20250102-20250307-second-snapshot.rows.csv]]
- [[scripts/quant_point_in_time_status_events_merge.py|scripts/quant_point_in_time_status_events_merge.py]]
- [[tests/test_quant_point_in_time_status_events_merge.py|tests/test_quant_point_in_time_status_events_merge.py]]
- [[_report/quant/data/point_in_time_status_events/2026-07-08-kind-current-status-events.merged-20260703-20260708.csv|_report/quant/data/point_in_time_status_events/2026-07-08-kind-current-status-events.merged-20260703-20260708.csv]]
- [[_report/quant/research/2026-07-08-kind-status-events-merge-20260703-20260708|_report/quant/research/2026-07-08-kind-status-events-merge-20260703-20260708.md]]
- [[_report/quant/research/2026-07-08-kind-status-events-merged-20260703-20260708-validation|_report/quant/research/2026-07-08-kind-status-events-merged-20260703-20260708-validation.md]]
- [[_report/quant/research/2026-07-08-kind-status-events-merged-20260703-20260708-validation.rows.csv|_report/quant/research/2026-07-08-kind-status-events-merged-20260703-20260708-validation.rows.csv]]
- [[_report/quant/research/2026-07-08-kind-status-replay-on-openapi-20250102-20250307-merged-snapshots|_report/quant/research/2026-07-08-kind-status-replay-on-openapi-20250102-20250307-merged-snapshots.md]]
- [[_report/quant/research/2026-07-08-kind-status-replay-on-openapi-20250102-20250307-merged-snapshots.rows.csv|_report/quant/research/2026-07-08-kind-status-replay-on-openapi-20250102-20250307-merged-snapshots.rows.csv]]
- [[_report/quant/research/2026-07-08-point-in-time-status-coverage-audit-20250102-20250307-merged-snapshots|_report/quant/research/2026-07-08-point-in-time-status-coverage-audit-20250102-20250307-merged-snapshots.md]]
- [[_report/quant/research/2026-07-08-point-in-time-status-coverage-audit-20250102-20250307-merged-snapshots.rows.csv|_report/quant/research/2026-07-08-point-in-time-status-coverage-audit-20250102-20250307-merged-snapshots.rows.csv]]
- [[_report/quant/research/2026-07-08-kind-status-point-in-time-universe-smoke-merged-snapshots-20250102-20250307|_report/quant/research/2026-07-08-kind-status-point-in-time-universe-smoke-merged-snapshots-20250102-20250307.md]]
- [[_report/quant/research/2026-07-08-kind-status-point-in-time-universe-smoke-merged-snapshots-20250102-20250307.rows.csv|_report/quant/research/2026-07-08-kind-status-point-in-time-universe-smoke-merged-snapshots-20250102-20250307.rows.csv]]
- [[_report/quant/research/2026-07-08-kind-status-point-in-time-universe-smoke-20250102-20250307|_report/quant/research/2026-07-08-kind-status-point-in-time-universe-smoke-20250102-20250307.md]]
- [[_report/quant/research/2026-07-08-kind-status-point-in-time-universe-smoke-20250102-20250307.rows.csv|_report/quant/research/2026-07-08-kind-status-point-in-time-universe-smoke-20250102-20250307.rows.csv]]
- [[_report/quant/research/2026-07-08-kind-status-point-in-time-liquidity-smoke-20d-20250102-20250307|_report/quant/research/2026-07-08-kind-status-point-in-time-liquidity-smoke-20d-20250102-20250307.md]]
- [[_report/quant/research/2026-07-08-kind-status-point-in-time-liquidity-smoke-20d-20250102-20250307.rows.csv|_report/quant/research/2026-07-08-kind-status-point-in-time-liquidity-smoke-20d-20250102-20250307.rows.csv]]
- [[_report/quant/research/2026-07-08-kind-status-point-in-time-momentum-signal-candidates-smoke-20d-20250102-20250307|_report/quant/research/2026-07-08-kind-status-point-in-time-momentum-signal-candidates-smoke-20d-20250102-20250307.md]]
- [[_report/quant/research/2026-07-08-kind-status-point-in-time-momentum-signal-candidates-smoke-20d-20250102-20250307.rows.csv|_report/quant/research/2026-07-08-kind-status-point-in-time-momentum-signal-candidates-smoke-20d-20250102-20250307.rows.csv]]
- [[_report/quant/research/2026-07-08-signal-forward-return-smoke-20d-20250102-20250307|_report/quant/research/2026-07-08-signal-forward-return-smoke-20d-20250102-20250307.md]]
- [[_report/quant/research/2026-07-08-signal-forward-return-smoke-20d-20250102-20250307.rows.csv|_report/quant/research/2026-07-08-signal-forward-return-smoke-20d-20250102-20250307.rows.csv]]
- [[_report/quant/research/2026-07-08-signal-portfolio-targets-smoke-20d-20250102-20250307|_report/quant/research/2026-07-08-signal-portfolio-targets-smoke-20d-20250102-20250307.md]]
- [[_report/quant/research/2026-07-08-signal-portfolio-targets-smoke-20d-20250102-20250307.rows.csv|_report/quant/research/2026-07-08-signal-portfolio-targets-smoke-20d-20250102-20250307.rows.csv]]
- [[_report/quant/research/2026-07-08-backtest-input-contract-validate-20250102-20250307|_report/quant/research/2026-07-08-backtest-input-contract-validate-20250102-20250307.md]]
- [[_report/quant/research/2026-07-08-backtest-pnl-smoke-20d-20250102-20250307|_report/quant/research/2026-07-08-backtest-pnl-smoke-20d-20250102-20250307.md]]
- [[_report/quant/research/2026-07-08-backtest-pnl-smoke-20d-20250102-20250307.rows.csv|_report/quant/research/2026-07-08-backtest-pnl-smoke-20d-20250102-20250307.rows.csv]]
- [[_report/quant/research/2026-07-08-quant-readiness-check-20d-20250102-20250307|_report/quant/research/2026-07-08-quant-readiness-check-20d-20250102-20250307.md]]
- [[_report/quant/research/2026-07-08-quant-readiness-check-20d-20250102-20250307-merged-status|_report/quant/research/2026-07-08-quant-readiness-check-20d-20250102-20250307-merged-status.md]]
- Implementation hygiene: remaining Quant report-output generators now route Markdown reports through [[scripts/quant_io.py|scripts/quant_io.py]] `write_text_lf`; CSV writers keep explicit `lineterminator="\n"`.

Previous 2026-07-06 smoke artifacts:

- [[_report/quant/research/2026-07-06-krx-openapi-history-plan-20250210-20250221|_report/quant/research/2026-07-06-krx-openapi-history-plan-20250210-20250221.md]]
- [[_report/quant/research/2026-07-06-krx-openapi-history-plan-20250210-20250221.requests.json|_report/quant/research/2026-07-06-krx-openapi-history-plan-20250210-20250221.requests.json]]
- [[_report/quant/research/2026-07-06-krx-openapi-history-collection-result-20250210-20250221|_report/quant/research/2026-07-06-krx-openapi-history-collection-result-20250210-20250221.md]]
- [[_report/quant/research/2026-07-06-krx-openapi-history-collection-result-20250210-20250221.requests.json|_report/quant/research/2026-07-06-krx-openapi-history-collection-result-20250210-20250221.requests.json]]
- [[_report/quant/research/2026-07-06-krx-openapi-history-normalize-result-20250210-20250221|_report/quant/research/2026-07-06-krx-openapi-history-normalize-result-20250210-20250221.md]]
- [[_report/quant/research/2026-07-06-krx-openapi-continuity-audit-20250210-20250221|_report/quant/research/2026-07-06-krx-openapi-continuity-audit-20250210-20250221.md]]
- [[_report/quant/research/2026-07-06-krx-openapi-continuity-audit-20250210-20250221.rows.csv|_report/quant/research/2026-07-06-krx-openapi-continuity-audit-20250210-20250221.rows.csv]]
- [[_report/quant/research/2026-07-06-krx-openapi-market-data-join-20250210-20250221|_report/quant/research/2026-07-06-krx-openapi-market-data-join-20250210-20250221.md]]
- [[_report/quant/research/2026-07-06-krx-openapi-market-data-merge-20250102-20250221|_report/quant/research/2026-07-06-krx-openapi-market-data-merge-20250102-20250221.md]]
- [[_report/quant/research/2026-07-06-kind-status-replay-on-openapi-20250102-20250221|_report/quant/research/2026-07-06-kind-status-replay-on-openapi-20250102-20250221.md]]
- [[_report/quant/research/2026-07-06-kind-status-replay-on-openapi-20250102-20250221.rows.csv|_report/quant/research/2026-07-06-kind-status-replay-on-openapi-20250102-20250221.rows.csv]]
- [[_report/quant/research/2026-07-06-point-in-time-status-coverage-audit-20250102-20250221|_report/quant/research/2026-07-06-point-in-time-status-coverage-audit-20250102-20250221.md]]
- [[_report/quant/research/2026-07-06-point-in-time-status-coverage-audit-20250102-20250221.rows.csv|_report/quant/research/2026-07-06-point-in-time-status-coverage-audit-20250102-20250221.rows.csv]]
- [[_report/quant/research/2026-07-08-kind-status-events-market-enrich-33d|_report/quant/research/2026-07-08-kind-status-events-market-enrich-33d.md]]
- [[_report/quant/research/2026-07-08-kind-status-events-market-enriched-33d-validation|_report/quant/research/2026-07-08-kind-status-events-market-enriched-33d-validation.md]]
- [[_report/quant/research/2026-07-08-kind-status-events-market-enriched-33d-validation.rows.csv|_report/quant/research/2026-07-08-kind-status-events-market-enriched-33d-validation.rows.csv]]
- [[_report/quant/research/2026-07-06-kind-status-point-in-time-universe-smoke-20250102-20250221|_report/quant/research/2026-07-06-kind-status-point-in-time-universe-smoke-20250102-20250221.md]]
- [[_report/quant/research/2026-07-06-kind-status-point-in-time-universe-smoke-20250102-20250221.rows.csv|_report/quant/research/2026-07-06-kind-status-point-in-time-universe-smoke-20250102-20250221.rows.csv]]
- [[_report/quant/research/2026-07-06-kind-status-point-in-time-liquidity-smoke-20d-20250102-20250221|_report/quant/research/2026-07-06-kind-status-point-in-time-liquidity-smoke-20d-20250102-20250221.md]]
- [[_report/quant/research/2026-07-06-kind-status-point-in-time-liquidity-smoke-20d-20250102-20250221.rows.csv|_report/quant/research/2026-07-06-kind-status-point-in-time-liquidity-smoke-20d-20250102-20250221.rows.csv]]
- [[_report/quant/research/2026-07-06-kind-status-point-in-time-momentum-signal-candidates-smoke-20d-20250102-20250221|_report/quant/research/2026-07-06-kind-status-point-in-time-momentum-signal-candidates-smoke-20d-20250102-20250221.md]]
- [[_report/quant/research/2026-07-06-kind-status-point-in-time-momentum-signal-candidates-smoke-20d-20250102-20250221.rows.csv|_report/quant/research/2026-07-06-kind-status-point-in-time-momentum-signal-candidates-smoke-20d-20250102-20250221.rows.csv]]
- [[_report/quant/research/2026-07-06-signal-forward-return-smoke-20d-20250102-20250221|_report/quant/research/2026-07-06-signal-forward-return-smoke-20d-20250102-20250221.md]]
- [[_report/quant/research/2026-07-06-signal-forward-return-smoke-20d-20250102-20250221.rows.csv|_report/quant/research/2026-07-06-signal-forward-return-smoke-20d-20250102-20250221.rows.csv]]
- [[_report/quant/research/2026-07-06-signal-portfolio-targets-smoke-20d-20250102-20250221|_report/quant/research/2026-07-06-signal-portfolio-targets-smoke-20d-20250102-20250221.md]]
- [[_report/quant/research/2026-07-06-signal-portfolio-targets-smoke-20d-20250102-20250221.rows.csv|_report/quant/research/2026-07-06-signal-portfolio-targets-smoke-20d-20250102-20250221.rows.csv]]
- [[_report/quant/research/2026-07-06-backtest-input-contract-20d|_report/quant/research/2026-07-06-backtest-input-contract-20d.md]]
- [[_report/quant/research/2026-07-06-backtest-pnl-smoke-20d-20250102-20250221|_report/quant/research/2026-07-06-backtest-pnl-smoke-20d-20250102-20250221.md]]
- [[_report/quant/research/2026-07-06-backtest-pnl-smoke-20d-20250102-20250221.rows.csv|_report/quant/research/2026-07-06-backtest-pnl-smoke-20d-20250102-20250221.rows.csv]]
- [[_report/quant/research/2026-07-06-quant-readiness-check-20d-with-extended-market-data|_report/quant/research/2026-07-06-quant-readiness-check-20d-with-extended-market-data.md]]

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
- [[scripts/quant_kind_status_source_probe.py|scripts/quant_kind_status_source_probe.py]]
- [[tests/test_quant_kind_status_source_probe.py|tests/test_quant_kind_status_source_probe.py]]
- [[_report/quant/research/2026-07-03-kind-status-source-probe|_report/quant/research/2026-07-03-kind-status-source-probe.md]]
- [[scripts/quant_kind_status_events_extract.py|scripts/quant_kind_status_events_extract.py]]
- [[tests/test_quant_kind_status_events_extract.py|tests/test_quant_kind_status_events_extract.py]]
- [[_report/quant/data/point_in_time_status_events/2026-07-03-kind-current-status-events.csv|_report/quant/data/point_in_time_status_events/2026-07-03-kind-current-status-events.csv]]
- [[_report/quant/research/2026-07-03-kind-status-events-extract|_report/quant/research/2026-07-03-kind-status-events-extract.md]]
- [[_report/quant/research/2026-07-03-kind-status-events-validation|_report/quant/research/2026-07-03-kind-status-events-validation.md]]
- [[_report/quant/research/2026-07-03-kind-status-events-validation.rows.csv|_report/quant/research/2026-07-03-kind-status-events-validation.rows.csv]]
- [[_report/quant/research/2026-07-03-kind-status-replay-on-openapi-20250102-20250124|_report/quant/research/2026-07-03-kind-status-replay-on-openapi-20250102-20250124.md]]
- [[_report/quant/research/2026-07-03-kind-status-replay-on-openapi-20250102-20250124.rows.csv|_report/quant/research/2026-07-03-kind-status-replay-on-openapi-20250102-20250124.rows.csv]]
- [[scripts/quant_point_in_time_status_events_enrich_market.py|scripts/quant_point_in_time_status_events_enrich_market.py]]
- [[tests/test_quant_point_in_time_status_events_enrich_market.py|tests/test_quant_point_in_time_status_events_enrich_market.py]]
- [[_report/quant/data/point_in_time_status_events/2026-07-03-kind-current-status-events.market-enriched.csv|_report/quant/data/point_in_time_status_events/2026-07-03-kind-current-status-events.market-enriched.csv]]
- [[_report/quant/research/2026-07-03-kind-status-events-market-enrich|_report/quant/research/2026-07-03-kind-status-events-market-enrich.md]]
- [[_report/quant/research/2026-07-03-kind-status-events-market-enriched-validation|_report/quant/research/2026-07-03-kind-status-events-market-enriched-validation.md]]
- [[_report/quant/research/2026-07-03-kind-status-events-market-enriched-validation.rows.csv|_report/quant/research/2026-07-03-kind-status-events-market-enriched-validation.rows.csv]]
- [[_report/quant/data/point_in_time_status_events/2026-07-03-kind-current-status-events.market-enriched-33d.csv|_report/quant/data/point_in_time_status_events/2026-07-03-kind-current-status-events.market-enriched-33d.csv]]
- [[_report/quant/research/2026-07-08-kind-status-events-market-enrich-33d|_report/quant/research/2026-07-08-kind-status-events-market-enrich-33d.md]]
- [[_report/quant/research/2026-07-08-kind-status-events-market-enriched-33d-validation|_report/quant/research/2026-07-08-kind-status-events-market-enriched-33d-validation.md]]
- [[_report/quant/research/2026-07-08-kind-status-events-market-enriched-33d-validation.rows.csv|_report/quant/research/2026-07-08-kind-status-events-market-enriched-33d-validation.rows.csv]]
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

- `Point-in-Time Universe` full historical path is not built; the latest evidence is a 72-date KIND current-snapshot replay smoke over two merged capture dates.
- Historical managed issue / trading suspension / market alert / delisting status is not reproducible across the full target Rebalance date range; two KIND current snapshots have been normalized and replayed, but release/resume-like lifecycle rows are still absent.
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
- [[_report/quant/research/2026-07-04-krx-openapi-history-plan-20250127-20250207|_report/quant/research/2026-07-04-krx-openapi-history-plan-20250127-20250207.md]]
- [[_report/quant/research/2026-07-04-krx-openapi-history-collection-result-20250127-20250207|_report/quant/research/2026-07-04-krx-openapi-history-collection-result-20250127-20250207.md]]
- [[_report/quant/research/2026-07-04-krx-openapi-history-normalize-result-20250127-20250207|_report/quant/research/2026-07-04-krx-openapi-history-normalize-result-20250127-20250207.md]]
- [[_report/quant/research/2026-07-04-krx-openapi-continuity-audit-20250127-20250207|_report/quant/research/2026-07-04-krx-openapi-continuity-audit-20250127-20250207.md]]
- [[_report/quant/research/2026-07-04-krx-openapi-continuity-audit-20250127-20250207.rows.csv|_report/quant/research/2026-07-04-krx-openapi-continuity-audit-20250127-20250207.rows.csv]]
- [[_report/quant/research/2026-07-04-krx-openapi-market-data-join-20250127-20250207|_report/quant/research/2026-07-04-krx-openapi-market-data-join-20250127-20250207.md]]
- [[scripts/quant_krx_openapi_market_data_merge.py|scripts/quant_krx_openapi_market_data_merge.py]]
- [[tests/test_quant_krx_openapi_market_data_merge.py|tests/test_quant_krx_openapi_market_data_merge.py]]
- [[_report/quant/research/2026-07-04-krx-openapi-market-data-merge-20250102-20250207|_report/quant/research/2026-07-04-krx-openapi-market-data-merge-20250102-20250207.md]]
- [[scripts/quant_krx_openapi_history_collect.py|scripts/quant_krx_openapi_history_collect.py]]
- [[tests/test_quant_krx_openapi_history_collect.py|tests/test_quant_krx_openapi_history_collect.py]]
- [[_report/quant/research/2026-07-06-krx-openapi-market-data-join-20250210-20250221|_report/quant/research/2026-07-06-krx-openapi-market-data-join-20250210-20250221.md]]
- [[_report/quant/research/2026-07-06-krx-openapi-market-data-merge-20250102-20250221|_report/quant/research/2026-07-06-krx-openapi-market-data-merge-20250102-20250221.md]]

Latest merged market-data smoke over `2025-01-02` to `2025-04-18`:

| metric | value |
| --- | ---: |
| merged rows | 198137 |
| date count | 72 |
| KOSPI rows | 69242 |
| KOSDAQ rows | 128895 |

The `2025-01-27` through `2025-01-30` and `2025-03-03` KRX rows had issue-base data but no stock-daily/index rows and were dropped from joined market data as non-trading-date evidence.

Remaining limitation:

- This is a clean market-data input, not a `Point-in-Time Universe`; historical managed issue, trading halt, market alert, and delisting replay still need separate status sources.

## Point-in-Time Status Source Gap

Status: `kind_fallback_merged_current_snapshots_validated`

Official-source check:

- KRX OpenAPI service list covers market data and issue base rows but does not expose the needed managed issue, trading halt, market alert, or delisting event replay as a visible core OpenAPI service.
- KRX Data Marketplace stock `종목정보` pages, especially `전종목 지정내역`, are the next official candidate for status snapshots.
- KIND is the event/disclosure fallback candidate when KRX Data Marketplace does not provide a clean historical table.
- KRX Data Marketplace status-source probe identified official menu/screen/bld mappings for `전종목 지정내역`, `관리종목 현황`, `매매거래정지종목 현황`, `상장폐지종목 현황`, `정리매매종목 현황`, and market-alert pages.
- The same probe classified all core status JSON calls as `auth_required` because KRX returned `LOGOUT` without an authenticated Data Marketplace session.

KIND fallback result:

- KIND public status downloads were usable for `6/7` probed sources without login on both `2026-07-03` and `2026-07-08`.
- The `2026-07-08` KIND current snapshot normalized into `327` valid status-event rows with `0` invalid rows.
- Market enrichment from the 42-date market-data join resolved `297/327` second-snapshot event rows and left `30` as `UNKNOWN`.
- A local evidence merge combined the `2026-07-03` and `2026-07-08` KIND current snapshots into `497` logical status-event rows, preserving `2` raw capture dates and `14` raw source paths; the original merged set had `48` `UNKNOWN` market rows, and the 81-date market enrichment reduces this to `47`.
- Merged status-event validation stayed `497/497` valid with `0` duplicate event keys.
- The merged KIND events replayed against the latest 72-date KRX OpenAPI market-data merge and marked `1646/198137` rows as `exclude_by_status_event`.
- The merged replayed market-data rows were converted into a 72-date `Point-in-Time Universe` smoke with `184549` include rows and `13588` exclude rows.
- Status coverage is still not historical-complete because release/resume-like rows remain `0` for managed issue, market alert, and trading halt lifecycles.

Artifact:

- [[_report/quant/research/2026-07-03-point-in-time-status-source-gap|_report/quant/research/2026-07-03-point-in-time-status-source-gap.md]]
- [[_report/quant/research/2026-07-03-krx-data-marketplace-status-source-probe|_report/quant/research/2026-07-03-krx-data-marketplace-status-source-probe.md]]
- [[_report/quant/research/2026-07-03-kind-status-source-probe|_report/quant/research/2026-07-03-kind-status-source-probe.md]]
- [[_report/quant/research/2026-07-03-kind-status-events-extract|_report/quant/research/2026-07-03-kind-status-events-extract.md]]
- [[_report/quant/research/2026-07-03-kind-status-events-validation|_report/quant/research/2026-07-03-kind-status-events-validation.md]]
- [[_report/quant/research/2026-07-03-kind-status-replay-on-openapi-20250102-20250124|_report/quant/research/2026-07-03-kind-status-replay-on-openapi-20250102-20250124.md]]
- [[_report/quant/research/2026-07-04-kind-status-replay-on-openapi-20250102-20250207|_report/quant/research/2026-07-04-kind-status-replay-on-openapi-20250102-20250207.md]]
- [[_report/quant/research/2026-07-04-kind-status-replay-on-openapi-20250102-20250207.rows.csv|_report/quant/research/2026-07-04-kind-status-replay-on-openapi-20250102-20250207.rows.csv]]
- [[_report/quant/research/2026-07-06-kind-status-replay-on-openapi-20250102-20250221|_report/quant/research/2026-07-06-kind-status-replay-on-openapi-20250102-20250221.md]]
- [[_report/quant/research/2026-07-06-kind-status-replay-on-openapi-20250102-20250221.rows.csv|_report/quant/research/2026-07-06-kind-status-replay-on-openapi-20250102-20250221.rows.csv]]
- [[_report/quant/research/2026-07-06-point-in-time-status-coverage-audit-20250102-20250221|_report/quant/research/2026-07-06-point-in-time-status-coverage-audit-20250102-20250221.md]]
- [[_report/quant/research/2026-07-06-point-in-time-status-coverage-audit-20250102-20250221.rows.csv|_report/quant/research/2026-07-06-point-in-time-status-coverage-audit-20250102-20250221.rows.csv]]
- [[_report/quant/research/2026-07-08-kind-status-replay-on-openapi-20250102-20250307|_report/quant/research/2026-07-08-kind-status-replay-on-openapi-20250102-20250307.md]]
- [[_report/quant/research/2026-07-08-kind-status-replay-on-openapi-20250102-20250307.rows.csv|_report/quant/research/2026-07-08-kind-status-replay-on-openapi-20250102-20250307.rows.csv]]
- [[_report/quant/research/2026-07-08-point-in-time-status-coverage-audit-20250102-20250307|_report/quant/research/2026-07-08-point-in-time-status-coverage-audit-20250102-20250307.md]]
- [[_report/quant/research/2026-07-08-point-in-time-status-coverage-audit-20250102-20250307.rows.csv|_report/quant/research/2026-07-08-point-in-time-status-coverage-audit-20250102-20250307.rows.csv]]
- [[_report/quant/research/2026-07-08-kind-status-source-probe|_report/quant/research/2026-07-08-kind-status-source-probe.md]]
- [[_report/quant/research/2026-07-08-kind-status-events-extract|_report/quant/research/2026-07-08-kind-status-events-extract.md]]
- [[_report/quant/research/2026-07-08-kind-status-events-validation|_report/quant/research/2026-07-08-kind-status-events-validation.md]]
- [[_report/quant/research/2026-07-08-kind-status-events-market-enrich-42d|_report/quant/research/2026-07-08-kind-status-events-market-enrich-42d.md]]
- [[_report/quant/research/2026-07-08-kind-status-replay-on-openapi-20250102-20250307-second-snapshot|_report/quant/research/2026-07-08-kind-status-replay-on-openapi-20250102-20250307-second-snapshot.md]]
- [[_report/quant/research/2026-07-08-kind-status-replay-on-openapi-20250102-20250307-second-snapshot.rows.csv|_report/quant/research/2026-07-08-kind-status-replay-on-openapi-20250102-20250307-second-snapshot.rows.csv]]
- [[_report/quant/research/2026-07-08-point-in-time-status-coverage-audit-20250102-20250307-second-snapshot|_report/quant/research/2026-07-08-point-in-time-status-coverage-audit-20250102-20250307-second-snapshot.md]]
- [[_report/quant/research/2026-07-08-point-in-time-status-coverage-audit-20250102-20250307-second-snapshot.rows.csv|_report/quant/research/2026-07-08-point-in-time-status-coverage-audit-20250102-20250307-second-snapshot.rows.csv]]
- [[_report/quant/research/2026-07-08-kind-status-events-merge-20260703-20260708|_report/quant/research/2026-07-08-kind-status-events-merge-20260703-20260708.md]]
- [[_report/quant/research/2026-07-08-kind-status-events-merged-20260703-20260708-validation|_report/quant/research/2026-07-08-kind-status-events-merged-20260703-20260708-validation.md]]
- [[_report/quant/research/2026-07-08-kind-status-events-merged-20260703-20260708-validation.rows.csv|_report/quant/research/2026-07-08-kind-status-events-merged-20260703-20260708-validation.rows.csv]]
- [[_report/quant/research/2026-07-08-kind-status-replay-on-openapi-20250102-20250307-merged-snapshots|_report/quant/research/2026-07-08-kind-status-replay-on-openapi-20250102-20250307-merged-snapshots.md]]
- [[_report/quant/research/2026-07-08-kind-status-replay-on-openapi-20250102-20250307-merged-snapshots.rows.csv|_report/quant/research/2026-07-08-kind-status-replay-on-openapi-20250102-20250307-merged-snapshots.rows.csv]]
- [[_report/quant/research/2026-07-08-point-in-time-status-coverage-audit-20250102-20250307-merged-snapshots|_report/quant/research/2026-07-08-point-in-time-status-coverage-audit-20250102-20250307-merged-snapshots.md]]
- [[_report/quant/research/2026-07-08-point-in-time-status-coverage-audit-20250102-20250307-merged-snapshots.rows.csv|_report/quant/research/2026-07-08-point-in-time-status-coverage-audit-20250102-20250307-merged-snapshots.rows.csv]]
- [[_report/quant/research/2026-07-08-kind-status-point-in-time-universe-smoke-merged-snapshots-20250102-20250307|_report/quant/research/2026-07-08-kind-status-point-in-time-universe-smoke-merged-snapshots-20250102-20250307.md]]
- [[_report/quant/research/2026-07-08-kind-status-point-in-time-universe-smoke-merged-snapshots-20250102-20250307.rows.csv|_report/quant/research/2026-07-08-kind-status-point-in-time-universe-smoke-merged-snapshots-20250102-20250307.rows.csv]]
- [[scripts/quant_point_in_time_universe_build.py|scripts/quant_point_in_time_universe_build.py]]
- [[tests/test_quant_point_in_time_universe_build.py|tests/test_quant_point_in_time_universe_build.py]]
- [[_report/quant/research/2026-07-03-kind-status-point-in-time-universe-smoke-20250102-20250124|_report/quant/research/2026-07-03-kind-status-point-in-time-universe-smoke-20250102-20250124.md]]
- [[_report/quant/research/2026-07-03-kind-status-point-in-time-universe-smoke-20250102-20250124.rows.csv|_report/quant/research/2026-07-03-kind-status-point-in-time-universe-smoke-20250102-20250124.rows.csv]]
- [[_report/quant/research/2026-07-04-kind-status-point-in-time-universe-smoke-20250102-20250207|_report/quant/research/2026-07-04-kind-status-point-in-time-universe-smoke-20250102-20250207.md]]
- [[_report/quant/research/2026-07-04-kind-status-point-in-time-universe-smoke-20250102-20250207.rows.csv|_report/quant/research/2026-07-04-kind-status-point-in-time-universe-smoke-20250102-20250207.rows.csv]]
- [[_report/quant/research/2026-07-06-kind-status-point-in-time-universe-smoke-20250102-20250221|_report/quant/research/2026-07-06-kind-status-point-in-time-universe-smoke-20250102-20250221.md]]
- [[_report/quant/research/2026-07-06-kind-status-point-in-time-universe-smoke-20250102-20250221.rows.csv|_report/quant/research/2026-07-06-kind-status-point-in-time-universe-smoke-20250102-20250221.rows.csv]]
- [[_report/quant/research/2026-07-08-kind-status-point-in-time-universe-smoke-20250102-20250307|_report/quant/research/2026-07-08-kind-status-point-in-time-universe-smoke-20250102-20250307.md]]
- [[_report/quant/research/2026-07-08-kind-status-point-in-time-universe-smoke-20250102-20250307.rows.csv|_report/quant/research/2026-07-08-kind-status-point-in-time-universe-smoke-20250102-20250307.rows.csv]]

Next gate:

- Add historical transition evidence, not just more current snapshots: release/resume rows for managed issues, market alerts, and trading halts must be reproducible by rebalance date before treating the Universe smoke as a Backtest input.

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

Current validated sample:

- [[_report/quant/data/point_in_time_status_events/2026-07-03-kind-current-status-events.csv|_report/quant/data/point_in_time_status_events/2026-07-03-kind-current-status-events.csv]] has `344` valid rows and `0` duplicate event keys.
- [[_report/quant/data/point_in_time_status_events/2026-07-08-kind-current-status-events.merged-20260703-20260708.csv|_report/quant/data/point_in_time_status_events/2026-07-08-kind-current-status-events.merged-20260703-20260708.csv]] merges two KIND current snapshots into `497` logical status-event rows and validates with `0` duplicate event keys.

Next gate:

- Add market classification and historical release/resume coverage for status events, then keep validation at `0` invalid rows.

## Point-in-Time Status Replay Scaffold

Status: `validated_kind_merged_snapshots_replayed_on_72_date_market_data`

Implemented local replay:

- Validates status events with [[scripts/quant_point_in_time_status_events_validate.py|scripts/quant_point_in_time_status_events_validate.py]] before replay.
- Applies events where `event_date <= market-data date`.
- Emits row-level `pit_*` fields for active managed issue, trading halt, market alert, and delisting state.
- Keeps `include_by_status_event` explicitly scoped to the provided event rows; it is not full official status coverage.

Artifact:

- [[_report/quant/research/2026-07-03-point-in-time-status-replay-scaffold|_report/quant/research/2026-07-03-point-in-time-status-replay-scaffold.md]]
- [[_report/quant/research/2026-07-03-kind-status-replay-on-openapi-20250102-20250124|_report/quant/research/2026-07-03-kind-status-replay-on-openapi-20250102-20250124.md]]
- [[_report/quant/research/2026-07-03-kind-status-replay-on-openapi-20250102-20250124.rows.csv|_report/quant/research/2026-07-03-kind-status-replay-on-openapi-20250102-20250124.rows.csv]]
- [[_report/quant/research/2026-07-04-kind-status-replay-on-openapi-20250102-20250207|_report/quant/research/2026-07-04-kind-status-replay-on-openapi-20250102-20250207.md]]
- [[_report/quant/research/2026-07-04-kind-status-replay-on-openapi-20250102-20250207.rows.csv|_report/quant/research/2026-07-04-kind-status-replay-on-openapi-20250102-20250207.rows.csv]]
- [[_report/quant/research/2026-07-06-kind-status-replay-on-openapi-20250102-20250221|_report/quant/research/2026-07-06-kind-status-replay-on-openapi-20250102-20250221.md]]
- [[_report/quant/research/2026-07-06-kind-status-replay-on-openapi-20250102-20250221.rows.csv|_report/quant/research/2026-07-06-kind-status-replay-on-openapi-20250102-20250221.rows.csv]]
- [[_report/quant/research/2026-07-08-kind-status-replay-on-openapi-20250102-20250307|_report/quant/research/2026-07-08-kind-status-replay-on-openapi-20250102-20250307.md]]
- [[_report/quant/research/2026-07-08-kind-status-replay-on-openapi-20250102-20250307.rows.csv|_report/quant/research/2026-07-08-kind-status-replay-on-openapi-20250102-20250307.rows.csv]]
- [[_report/quant/research/2026-07-08-kind-status-replay-on-openapi-20250102-20250307-merged-snapshots|_report/quant/research/2026-07-08-kind-status-replay-on-openapi-20250102-20250307-merged-snapshots.md]]
- [[_report/quant/research/2026-07-08-kind-status-replay-on-openapi-20250102-20250307-merged-snapshots.rows.csv|_report/quant/research/2026-07-08-kind-status-replay-on-openapi-20250102-20250307-merged-snapshots.rows.csv]]
- [[_report/quant/research/2026-07-08-kind-status-replay-on-openapi-20250102-20250321-merged-snapshots|_report/quant/research/2026-07-08-kind-status-replay-on-openapi-20250102-20250321-merged-snapshots.md]]
- [[_report/quant/research/2026-07-08-kind-status-replay-on-openapi-20250102-20250321-merged-snapshots.rows.csv|_report/quant/research/2026-07-08-kind-status-replay-on-openapi-20250102-20250321-merged-snapshots.rows.csv]]
- [[_report/quant/research/2026-07-08-kind-status-replay-on-openapi-20250102-20250404-merged-snapshots|_report/quant/research/2026-07-08-kind-status-replay-on-openapi-20250102-20250404-merged-snapshots.md]]
- [[_report/quant/research/2026-07-08-kind-status-replay-on-openapi-20250102-20250404-merged-snapshots.rows.csv|_report/quant/research/2026-07-08-kind-status-replay-on-openapi-20250102-20250404-merged-snapshots.rows.csv]]
- [[_report/quant/research/2026-07-08-kind-status-replay-on-openapi-20250102-20250418-merged-snapshots|_report/quant/research/2026-07-08-kind-status-replay-on-openapi-20250102-20250418-merged-snapshots.md]]
- [[_report/quant/research/2026-07-08-kind-status-replay-on-openapi-20250102-20250418-merged-snapshots.rows.csv|_report/quant/research/2026-07-08-kind-status-replay-on-openapi-20250102-20250418-merged-snapshots.rows.csv]]

Latest smoke result:

- Market data input rows: `198137`
- Status event rows: `497`
- Codes with events: `286`
- Include rows by event state: `196491`
- Exclude rows by event state: `1646`

Status coverage audit:

- [[scripts/quant_point_in_time_status_coverage_audit.py|scripts/quant_point_in_time_status_coverage_audit.py]]
- [[tests/test_quant_point_in_time_status_coverage_audit.py|tests/test_quant_point_in_time_status_coverage_audit.py]]
- [[_report/quant/data/templates/point_in_time_status_source_coverage_manifest.template.csv|_report/quant/data/templates/point_in_time_status_source_coverage_manifest.template.csv]]
- [[scripts/quant_point_in_time_status_source_manifest_validate.py|scripts/quant_point_in_time_status_source_manifest_validate.py]]
- [[tests/test_quant_point_in_time_status_source_manifest_validate.py|tests/test_quant_point_in_time_status_source_manifest_validate.py]]
- [[scripts/quant_point_in_time_status_lifecycle_gap_report.py|scripts/quant_point_in_time_status_lifecycle_gap_report.py]]
- [[tests/test_quant_point_in_time_status_lifecycle_gap_report.py|tests/test_quant_point_in_time_status_lifecycle_gap_report.py]]
- [[scripts/quant_point_in_time_status_unknown_market_report.py|scripts/quant_point_in_time_status_unknown_market_report.py]]
- [[tests/test_quant_point_in_time_status_unknown_market_report.py|tests/test_quant_point_in_time_status_unknown_market_report.py]]
- [[_report/quant/research/2026-07-06-point-in-time-status-coverage-audit-20250102-20250221|_report/quant/research/2026-07-06-point-in-time-status-coverage-audit-20250102-20250221.md]]
- [[_report/quant/research/2026-07-06-point-in-time-status-coverage-audit-20250102-20250221.rows.csv|_report/quant/research/2026-07-06-point-in-time-status-coverage-audit-20250102-20250221.rows.csv]]
- [[_report/quant/research/2026-07-08-point-in-time-status-coverage-audit-20250102-20250307|_report/quant/research/2026-07-08-point-in-time-status-coverage-audit-20250102-20250307.md]]
- [[_report/quant/research/2026-07-08-point-in-time-status-coverage-audit-20250102-20250307.rows.csv|_report/quant/research/2026-07-08-point-in-time-status-coverage-audit-20250102-20250307.rows.csv]]
- [[_report/quant/research/2026-07-08-point-in-time-status-coverage-audit-20250102-20250307-merged-snapshots|_report/quant/research/2026-07-08-point-in-time-status-coverage-audit-20250102-20250307-merged-snapshots.md]]
- [[_report/quant/research/2026-07-08-point-in-time-status-coverage-audit-20250102-20250307-merged-snapshots.rows.csv|_report/quant/research/2026-07-08-point-in-time-status-coverage-audit-20250102-20250307-merged-snapshots.rows.csv]]
- [[_report/quant/research/2026-07-08-point-in-time-status-coverage-audit-20250102-20250321-merged-snapshots|_report/quant/research/2026-07-08-point-in-time-status-coverage-audit-20250102-20250321-merged-snapshots.md]]
- [[_report/quant/research/2026-07-08-point-in-time-status-coverage-audit-20250102-20250321-merged-snapshots.rows.csv|_report/quant/research/2026-07-08-point-in-time-status-coverage-audit-20250102-20250321-merged-snapshots.rows.csv]]
- [[_report/quant/research/2026-07-08-point-in-time-status-coverage-audit-20250102-20250404-merged-snapshots|_report/quant/research/2026-07-08-point-in-time-status-coverage-audit-20250102-20250404-merged-snapshots.md]]
- [[_report/quant/research/2026-07-08-point-in-time-status-coverage-audit-20250102-20250404-merged-snapshots.rows.csv|_report/quant/research/2026-07-08-point-in-time-status-coverage-audit-20250102-20250404-merged-snapshots.rows.csv]]
- [[_report/quant/research/2026-07-08-point-in-time-status-coverage-audit-20250102-20250418-merged-snapshots|_report/quant/research/2026-07-08-point-in-time-status-coverage-audit-20250102-20250418-merged-snapshots.md]]
- [[_report/quant/research/2026-07-08-point-in-time-status-coverage-audit-20250102-20250418-merged-snapshots.rows.csv|_report/quant/research/2026-07-08-point-in-time-status-coverage-audit-20250102-20250418-merged-snapshots.rows.csv]]
- [[_report/quant/research/2026-07-09-kind-status-events-merged-market-enrich-81d|_report/quant/research/2026-07-09-kind-status-events-merged-market-enrich-81d.md]]
- [[_report/quant/research/2026-07-09-kind-status-events-merged-market-enriched-81d-validation|_report/quant/research/2026-07-09-kind-status-events-merged-market-enriched-81d-validation.md]]
- [[_report/quant/research/2026-07-09-kind-status-events-merged-market-enriched-81d-validation.rows.csv|_report/quant/research/2026-07-09-kind-status-events-merged-market-enriched-81d-validation.rows.csv]]
- [[_report/quant/research/2026-07-09-kind-status-events-unknown-market-targets-market-enriched-81d|_report/quant/research/2026-07-09-kind-status-events-unknown-market-targets-market-enriched-81d.md]]
- [[_report/quant/research/2026-07-09-kind-status-events-unknown-market-targets-market-enriched-81d.rows.csv|_report/quant/research/2026-07-09-kind-status-events-unknown-market-targets-market-enriched-81d.rows.csv]]
- [[_report/quant/research/2026-07-09-point-in-time-status-coverage-audit-20250102-20250418-merged-snapshots-market-enriched-81d|_report/quant/research/2026-07-09-point-in-time-status-coverage-audit-20250102-20250418-merged-snapshots-market-enriched-81d.md]]
- [[_report/quant/research/2026-07-09-point-in-time-status-coverage-audit-20250102-20250418-merged-snapshots-market-enriched-81d.rows.csv|_report/quant/research/2026-07-09-point-in-time-status-coverage-audit-20250102-20250418-merged-snapshots-market-enriched-81d.rows.csv]]
- [[_report/quant/research/2026-07-09-point-in-time-status-lifecycle-gaps-20250102-20250418-merged-snapshots|_report/quant/research/2026-07-09-point-in-time-status-lifecycle-gaps-20250102-20250418-merged-snapshots.md]]
- [[_report/quant/research/2026-07-09-point-in-time-status-lifecycle-gaps-20250102-20250418-merged-snapshots.rows.csv|_report/quant/research/2026-07-09-point-in-time-status-lifecycle-gaps-20250102-20250418-merged-snapshots.rows.csv]]
- [[_report/quant/research/2026-07-09-point-in-time-status-lifecycle-gaps-20250102-20250418-merged-snapshots-market-enriched-81d|_report/quant/research/2026-07-09-point-in-time-status-lifecycle-gaps-20250102-20250418-merged-snapshots-market-enriched-81d.md]]
- [[_report/quant/research/2026-07-09-point-in-time-status-lifecycle-gaps-20250102-20250418-merged-snapshots-market-enriched-81d.rows.csv|_report/quant/research/2026-07-09-point-in-time-status-lifecycle-gaps-20250102-20250418-merged-snapshots-market-enriched-81d.rows.csv]]
- Latest market enrichment: 81-date local market-data resolves `1` additional merged status-event market label; merged events now have `47` `UNKNOWN` market rows across `31` codes, down from `48`. Unknown-market target rows are split by status type as `trading_halt=28`, `delisting=9`, `managed_issue=6`, and `market_alert=4`.
- Coverage status: `hold`
- Coverage mode: `current_snapshot_smoke`
- Replayed rows: `198137`; replay missing rows: `0`
- Rows with any status-event code: `18320`; rows with applied status event: `1646`; rows excluded by status event: `1646`
- Raw status capture dates: `2` (`2026-07-03..2026-07-08`)
- Release/resume-like event rows: `0`, so active-state lifetimes remain one-sided and not historical-complete.
- Source coverage manifest rows: `0`; missing manifest coverage for `managed_issue`, `trading_halt`, `market_alert`, and `delisting`.
- Source coverage manifest validation: `not_supplied`; row failures: `0`.
- [[scripts/quant_point_in_time_status_coverage_audit.py|scripts/quant_point_in_time_status_coverage_audit.py]] now applies [[scripts/quant_point_in_time_status_source_manifest_validate.py|scripts/quant_point_in_time_status_source_manifest_validate.py]] when a source coverage manifest is supplied; source policy, raw evidence paths, required status types, and market-window coverage must validate before `historical_complete` can pass.
- Lifecycle diagnostics: `managed_issue` `105/0`, `market_alert` `75/0`, and `trading_halt` `253/0` active-like/release-resume rows.
- Lifecycle gap report: the latest market-enriched report still has `304` code/status lifecycle groups with `missing_release_resume_evidence` (`managed_issue=104`, `market_alert=70`, `trading_halt=130`). These rows are collection targets for official transition evidence, not historical truth and not a Backtest promotion.
- The audit pass gate now also requires every lifecycle status type with active-like rows to have release/resume-like rows, at least one dated raw capture path, and a source coverage manifest that passes source-policy/raw-path validation and covers the market-data window for every required status type.

Universe eligibility smoke:

- [[scripts/quant_point_in_time_universe_build.py|scripts/quant_point_in_time_universe_build.py]] consumes status-replayed market-data rows and emits local `pit_universe_*` eligibility fields.
- Latest 72-date smoke output: [[_report/quant/research/2026-07-08-kind-status-point-in-time-universe-smoke-merged-snapshots-20250102-20250418|_report/quant/research/2026-07-08-kind-status-point-in-time-universe-smoke-merged-snapshots-20250102-20250418.md]]
- Machine-readable rows: [[_report/quant/research/2026-07-08-kind-status-point-in-time-universe-smoke-merged-snapshots-20250102-20250418.rows.csv|_report/quant/research/2026-07-08-kind-status-point-in-time-universe-smoke-merged-snapshots-20250102-20250418.rows.csv]]
- Input rows: `198137`
- Include rows: `184549`
- Exclude rows: `13588`
- Exclusion reason counts: `stock_certificate_not_common=8352`, `security_group_not_plain_equity=3590`, `status_event:managed_issue_active=1646`

Point-in-Time Liquidity Filter smoke:

- [[scripts/quant_point_in_time_liquidity_filter.py|scripts/quant_point_in_time_liquidity_filter.py]]
- [[tests/test_quant_point_in_time_liquidity_filter.py|tests/test_quant_point_in_time_liquidity_filter.py]]
- Previous 17-date, 5-day smoke output: [[_report/quant/research/2026-07-04-kind-status-point-in-time-liquidity-smoke-20250102-20250124|_report/quant/research/2026-07-04-kind-status-point-in-time-liquidity-smoke-20250102-20250124.md]]
- Latest 72-date, 20-day smoke output: [[_report/quant/research/2026-07-08-kind-status-point-in-time-liquidity-smoke-20d-20250102-20250418|_report/quant/research/2026-07-08-kind-status-point-in-time-liquidity-smoke-20d-20250102-20250418.md]]
- Machine-readable rows: [[_report/quant/research/2026-07-08-kind-status-point-in-time-liquidity-smoke-20d-20250102-20250418.rows.csv|_report/quant/research/2026-07-08-kind-status-point-in-time-liquidity-smoke-20d-20250102-20250418.rows.csv]]
- Result: `54138` include rows and `143999` exclude rows after `avg_trading_value_20d_krw >= 1,000,000,000`; `135316` rows had full 20-day lookback evaluation.
- Limitation: historical status coverage is still incomplete, so this is not a Backtest input even though the Liquidity Filter lookback is now production-length for the bounded smoke range.

Point-in-Time Momentum Signal Candidate smoke:

- [[scripts/quant_point_in_time_signal_candidates.py|scripts/quant_point_in_time_signal_candidates.py]]
- [[tests/test_quant_point_in_time_signal_candidates.py|tests/test_quant_point_in_time_signal_candidates.py]]
- Previous 17-date, 5-day Momentum smoke output: [[_report/quant/research/2026-07-04-kind-status-point-in-time-momentum-signal-candidates-smoke-20250102-20250124|_report/quant/research/2026-07-04-kind-status-point-in-time-momentum-signal-candidates-smoke-20250102-20250124.md]]
- Latest 72-date, 20-day Momentum smoke output: [[_report/quant/research/2026-07-08-kind-status-point-in-time-momentum-signal-candidates-smoke-20d-20250102-20250418|_report/quant/research/2026-07-08-kind-status-point-in-time-momentum-signal-candidates-smoke-20d-20250102-20250418.md]]
- Machine-readable rows: [[_report/quant/research/2026-07-08-kind-status-point-in-time-momentum-signal-candidates-smoke-20d-20250102-20250418.rows.csv|_report/quant/research/2026-07-08-kind-status-point-in-time-momentum-signal-candidates-smoke-20d-20250102-20250418.rows.csv]]
- Result: `2120` paper-only Signal Candidate rows across `53` candidate dates: `1060` BUY candidates and `1060` SELL candidates.
- Limitation: this uses `5d ROC` over a bounded 72-date smoke range after a 20-day Liquidity Filter; it is not a Backtest result and does not generate order intents.

Signal forward-return smoke:

- [[scripts/quant_signal_forward_return_smoke.py|scripts/quant_signal_forward_return_smoke.py]]
- [[tests/test_quant_signal_forward_return_smoke.py|tests/test_quant_signal_forward_return_smoke.py]]
- [[_report/quant/research/2026-07-08-signal-forward-return-smoke-20d-20250102-20250418|_report/quant/research/2026-07-08-signal-forward-return-smoke-20d-20250102-20250418.md]]
- [[_report/quant/research/2026-07-08-signal-forward-return-smoke-20d-20250102-20250418.rows.csv|_report/quant/research/2026-07-08-signal-forward-return-smoke-20d-20250102-20250418.rows.csv]]
- Latest price-through output: [[_report/quant/research/2026-07-08-signal-forward-return-smoke-20d-20250102-20250418-price-through-20250502|_report/quant/research/2026-07-08-signal-forward-return-smoke-20d-20250102-20250418-price-through-20250502.md]]
- Latest price-through rows: [[_report/quant/research/2026-07-08-signal-forward-return-smoke-20d-20250102-20250418-price-through-20250502.rows.csv|_report/quant/research/2026-07-08-signal-forward-return-smoke-20d-20250102-20250418-price-through-20250502.rows.csv]]
- Latest result: `4240` horizon evaluation rows from `2120` Signal Candidate rows across `1,5` trading-day horizons; `4240` rows complete and `0` rows are `missing_forward_price` after extending local prices through `2025-05-02`.
- Limitation: this is still a coverage/diagnostic smoke, not a Backtest, because `Point-in-Time` status coverage, costs, OOS, and Bias Control remain incomplete.

Signal portfolio target smoke:

- [[scripts/quant_signal_portfolio_targets_smoke.py|scripts/quant_signal_portfolio_targets_smoke.py]]
- [[tests/test_quant_signal_portfolio_targets_smoke.py|tests/test_quant_signal_portfolio_targets_smoke.py]]
- [[_report/quant/research/2026-07-08-signal-portfolio-targets-smoke-20d-20250102-20250418|_report/quant/research/2026-07-08-signal-portfolio-targets-smoke-20d-20250102-20250418.md]]
- [[_report/quant/research/2026-07-08-signal-portfolio-targets-smoke-20d-20250102-20250418.rows.csv|_report/quant/research/2026-07-08-signal-portfolio-targets-smoke-20d-20250102-20250418.rows.csv]]
- Result: `1060` long-only paper target rows across `53` rebalance dates, using `20` BUY candidates per date at `5%` target weight each; `SELL candidate` rows remain exclusions, not short targets.
- Limitation: this is target-weight diagnostics only. It does not model costs, slippage, taxes, benchmark returns, cash drag, or order quantities.

Backtest input contract validation:

- [[scripts/quant_backtest_input_contract_validate.py|scripts/quant_backtest_input_contract_validate.py]]
- [[tests/test_quant_backtest_input_contract_validate.py|tests/test_quant_backtest_input_contract_validate.py]]
- [[_report/quant/research/2026-07-08-backtest-input-contract-validate-20250102-20250418|_report/quant/research/2026-07-08-backtest-input-contract-validate-20250102-20250418.md]]
- Result: contract status `pass_smoke` with `0` hold checks across required columns, key uniqueness, date/code integrity, Signal-Liquidity join, forward-return horizon coverage, portfolio-target join, and portfolio weight bounds.
- Limitation: this proves the current smoke artifacts are internally joinable. It still does not provide costs, slippage, taxes, benchmark returns, cash drag, OOS, Bias Control, or full historical `Point-in-Time` status coverage.

Backtest PnL smoke:

- [[scripts/quant_backtest_pnl_smoke.py|scripts/quant_backtest_pnl_smoke.py]]
- [[tests/test_quant_backtest_pnl_smoke.py|tests/test_quant_backtest_pnl_smoke.py]]
- [[_report/quant/research/2026-07-08-backtest-pnl-smoke-20d-20250102-20250418|_report/quant/research/2026-07-08-backtest-pnl-smoke-20d-20250102-20250418.md]]
- [[_report/quant/research/2026-07-08-backtest-pnl-smoke-20d-20250102-20250418.rows.csv|_report/quant/research/2026-07-08-backtest-pnl-smoke-20d-20250102-20250418.rows.csv]]
- Latest price-through output: [[_report/quant/research/2026-07-08-backtest-pnl-smoke-20d-20250102-20250418-price-through-20250502|_report/quant/research/2026-07-08-backtest-pnl-smoke-20d-20250102-20250418-price-through-20250502.md]]
- Latest price-through rows: [[_report/quant/research/2026-07-08-backtest-pnl-smoke-20d-20250102-20250418-price-through-20250502.rows.csv|_report/quant/research/2026-07-08-backtest-pnl-smoke-20d-20250102-20250418-price-through-20250502.rows.csv]]
- Latest result: 1-day horizon PnL smoke status `pass_smoke` with `1060` rows, `1060` complete rows, `1060` KOSPI benchmark joined rows, `0` `missing_forward_price` rows, and average weighted excess vs benchmark of `0.0179%`.
- Limitation: weighted-return contribution is target weight times raw forward return, and benchmark excess is diagnostic math only. It is not a production Backtest and does not model costs, slippage, taxes, cash drag, rebalance execution, or delisting/event timing.

Backtest cost/benchmark assumptions validation:

- [[scripts/quant_backtest_assumptions_validate.py|scripts/quant_backtest_assumptions_validate.py]]
- [[tests/test_quant_backtest_assumptions_validate.py|tests/test_quant_backtest_assumptions_validate.py]]
- [[_report/quant/data/backtest_cost_benchmark_assumptions.yaml|_report/quant/data/backtest_cost_benchmark_assumptions.yaml]]
- [[_report/quant/research/2026-07-08-backtest-cost-benchmark-assumptions-validate|_report/quant/research/2026-07-08-backtest-cost-benchmark-assumptions-validate.md]]
- Result: local cost and benchmark assumptions validate as `pass_assumption_only` with `0` hold checks.
- Limitation: `pass_assumption_only` only proves the assumption contract reconciles. It is not a Backtest result and still needs actual KIS fee override plus benchmark return wiring.

Benchmark return smoke:

- [[scripts/quant_benchmark_return_smoke.py|scripts/quant_benchmark_return_smoke.py]]
- [[tests/test_quant_benchmark_return_smoke.py|tests/test_quant_benchmark_return_smoke.py]]
- [[_report/quant/research/2026-07-08-benchmark-return-smoke-20d-20250102-20250418|_report/quant/research/2026-07-08-benchmark-return-smoke-20d-20250102-20250418.md]]
- [[_report/quant/research/2026-07-08-benchmark-return-smoke-20d-20250102-20250418.rows.csv|_report/quant/research/2026-07-08-benchmark-return-smoke-20d-20250102-20250418.rows.csv]]
- Latest price-through output: [[_report/quant/research/2026-07-08-benchmark-return-smoke-20d-20250102-20250418-price-through-20250502|_report/quant/research/2026-07-08-benchmark-return-smoke-20d-20250102-20250418-price-through-20250502.md]]
- Latest price-through rows: [[_report/quant/research/2026-07-08-benchmark-return-smoke-20d-20250102-20250418-price-through-20250502.rows.csv|_report/quant/research/2026-07-08-benchmark-return-smoke-20d-20250102-20250418-price-through-20250502.rows.csv]]
- Latest result: `318` benchmark horizon rows across `53` Signal Candidate dates, `3` benchmarks, and `1,5` trading-day horizons; `318` rows complete and `0` rows are `missing_forward_index` after extending index prices through `2025-05-02`.
- Limitation: benchmark return rows are diagnostic comparison inputs only. KOSPI is joined to PnL smoke for excess-return math, but this is not production benchmark attribution and still has no costs, cash drag, OOS, or Bias Control.

Quant readiness check:

- [[scripts/quant_readiness_check.py|scripts/quant_readiness_check.py]]
- [[tests/test_quant_readiness_check.py|tests/test_quant_readiness_check.py]]
- [[_report/quant/research/2026-07-04-quant-readiness-check-20d|_report/quant/research/2026-07-04-quant-readiness-check-20d.md]]
- [[_report/quant/research/2026-07-05-quant-readiness-check-20d-with-portfolio-targets|_report/quant/research/2026-07-05-quant-readiness-check-20d-with-portfolio-targets.md]]
- [[_report/quant/research/2026-07-05-quant-readiness-check-20d-with-backtest-contract|_report/quant/research/2026-07-05-quant-readiness-check-20d-with-backtest-contract.md]]
- [[_report/quant/research/2026-07-05-quant-readiness-check-20d-with-backtest-pnl-smoke|_report/quant/research/2026-07-05-quant-readiness-check-20d-with-backtest-pnl-smoke.md]]
- [[_report/quant/research/2026-07-06-quant-readiness-check-20d-with-extended-market-data|_report/quant/research/2026-07-06-quant-readiness-check-20d-with-extended-market-data.md]]
- [[_report/quant/research/2026-07-08-quant-readiness-check-20d-20250102-20250307|_report/quant/research/2026-07-08-quant-readiness-check-20d-20250102-20250307.md]]
- [[_report/quant/research/2026-07-08-quant-readiness-check-20d-20250102-20250418-merged-status|_report/quant/research/2026-07-08-quant-readiness-check-20d-20250102-20250418-merged-status.md]]
- Latest price-through readiness with market-enriched status evidence: [[_report/quant/research/2026-07-09-quant-readiness-check-20d-20250102-20250418-price-through-20250502-market-enriched-81d-status|_report/quant/research/2026-07-09-quant-readiness-check-20d-20250102-20250418-price-through-20250502-market-enriched-81d-status.md]]
- Result: market-data window `pass`, Liquidity Filter `pass_smoke`, Signal Candidate `pass_smoke`, forward-return smoke `pass_smoke` with complete `1,5` horizon coverage, portfolio target smoke `pass_smoke`, Backtest input contract `pass_smoke`, Backtest PnL smoke `pass_smoke`, Backtest assumptions `pass_assumption_only`, benchmark returns smoke `pass_smoke`, Point-in-Time status coverage `hold` with merged coverage audit evidence including source manifest validation `not_supplied` and lifecycle missing release/resume groups `304`, Backtest engine `hold`, live trading controls `blocked`, KIS demo account `blocked`.
- Guardrail: the readiness checker makes no KIS API calls and generates no order intents.

Next gate:

- Extend status coverage and Liquidity Filter coverage before treating `pit_universe_status=include` or generated Signal Candidate rows as a Backtest input.

KIS demo trading preflight artifacts:

- [[scripts/quant_kis_demo_order_preflight.py|scripts/quant_kis_demo_order_preflight.py]]
- [[tests/test_quant_kis_demo_order_preflight.py|tests/test_quant_kis_demo_order_preflight.py]]
- [[scripts/quant_kis_demo_account_preflight.py|scripts/quant_kis_demo_account_preflight.py]]
- [[tests/test_quant_kis_demo_account_preflight.py|tests/test_quant_kis_demo_account_preflight.py]]
- [[_report/quant/research/2026-07-03-kis-demo-trading-readiness|_report/quant/research/2026-07-03-kis-demo-trading-readiness.md]]
- [[_report/quant/research/2026-07-04-kis-demo-account-preflight|_report/quant/research/2026-07-04-kis-demo-account-preflight.md]]

KIS demo readiness judgment:

- Current state: `not_ready_but_preflight_started`
- Controlled first KIS demo order estimate: `3-7 working days` after local demo auth/account verification.
- Quant-pipeline-driven demo trading estimate: `3-6 weeks`.
- The current preflight is dry-run validation only; it does not call KIS and cannot place orders.
- Local demo account preflight found `KIS_PAPER_STOCK` empty in the ignored MCP `.env.kis`; no credential or account values were stored in the report.

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
- [[scripts/quant_point_in_time_liquidity_filter.py|scripts/quant_point_in_time_liquidity_filter.py]] also applies a 20-day date-scoped Liquidity Filter to the 72-date Point-in-Time smoke rows.

Target rule:

- `avg_trading_value_20d_krw >= 1,000,000,000`

Remaining input needed:

- More daily OHLCV / trading value windows for stability checks beyond the first 72-date smoke range.
- Expanded status-event coverage for the same dates before using the 20-day Liquidity Filter output as Backtest input.

Output already added:

- `avg_trading_value_20d_krw`
- `liquidity_filter_status`
- final `status` and `reason` after the saved-raw Liquidity Filter pass

### Step C. Connect Universe to Paper Signal

Goal:

- Stop using manual watchlist-only smoke symbols as the main Quant input.
- Use `current snapshot Universe v0` as the input list for paper/smoke validation.

Current implemented path:

- [[scripts/quant_point_in_time_signal_candidates.py|scripts/quant_point_in_time_signal_candidates.py]] reads Point-in-Time Liquidity Filter rows and emits paper-only Momentum Signal Candidate rows.
- Latest smoke output: [[_report/quant/research/2026-07-08-kind-status-point-in-time-momentum-signal-candidates-smoke-20d-20250102-20250418|_report/quant/research/2026-07-08-kind-status-point-in-time-momentum-signal-candidates-smoke-20d-20250102-20250418.md]]
- Latest smoke rows: [[_report/quant/research/2026-07-08-kind-status-point-in-time-momentum-signal-candidates-smoke-20d-20250102-20250418.rows.csv|_report/quant/research/2026-07-08-kind-status-point-in-time-momentum-signal-candidates-smoke-20d-20250102-20250418.rows.csv]]
- Latest smoke produced `2120` Signal Candidate rows across `53` candidate dates with `lookback=5` and `top_n_per_state=20` after the 20-day Liquidity Filter.

Guardrail:

- Paper/smoke signals are not trade instructions.
- These candidates are not order intents and should not be used for trading execution.

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
- KRX OpenAPI date-scoped market-data join/merge: usable as a 72-date smoke input for status replay development and an 81-date local forward-price coverage input through `2025-05-02`.
- KRX Data Marketplace status-source probe: official status screen `bld` identifiers found, but unattended JSON access is `auth_required`.
- KIND public status fallback: two current snapshots (`2026-07-03`, `2026-07-08`) were merged into `497` logical status-event rows and replayed against the 72-date KRX OpenAPI market-data merge, marking `1646/198137` rows as `exclude_by_status_event`; the merged coverage audit now sees `2` raw capture dates but still has `0` release/resume-like rows and no source coverage manifest.
- Point-in-Time status-event schema: KIND current snapshot samples are normalized, market-enriched, merged, and validated.
- Point-in-Time status replay and Universe smoke: merged KIND current snapshot events replayed on a 72-date market-data smoke, then converted to `184549` include / `13588` exclude Universe rows; historical coverage still incomplete.
- Point-in-Time Liquidity Filter smoke: a 72-date, 20-day smoke produced `54138` include rows and `143999` exclude rows, with `135316` rows evaluated on the full 20-day lookback.
- Point-in-Time Momentum Signal Candidate smoke: 72-date, 20-day Liquidity + 5-day Momentum smoke produced `2120` paper-only candidates across `53` candidate dates; this is not a Backtest result and does not generate order intents.
- Signal forward-return smoke: `2120` Signal Candidate rows were evaluated over `1,5` trading-day horizons, producing `4240` diagnostic rows with `4240` complete and `0` missing forward prices after extending local prices through `2025-05-02`.
- Signal portfolio target smoke: `1060` long-only paper target rows were generated across `53` rebalance dates at `5%` per selected BUY candidate, with no order intents.
- Backtest input contract validation: latest 20-day contract report is `pass_smoke` with `0` hold checks, proving the current smoke artifacts are internally joinable but not a Backtest result.
- Backtest PnL smoke: latest 1-day horizon diagnostic report is `pass_smoke` with `1060` target/horizon rows, `1060` complete rows, `1060` KOSPI benchmark joined rows, `0` missing forward prices, and average weighted excess vs benchmark of `0.0179%`.
- Backtest cost/benchmark assumptions: latest local assumption contract is `pass_assumption_only`; it still needs actual KIS fee override and benchmark return wiring before production Backtest.
- Benchmark return smoke: latest price-through report produced `318` complete benchmark horizon rows for KOSPI, KOSDAQ, and KOSPI200; KOSPI is joined into the PnL smoke as diagnostic benchmark-excess math, not production attribution.
- Quant readiness check: latest 20-day price-through smoke gate report using the market-enriched merged status coverage audit and lifecycle gap report marks market-data window `pass`, Liquidity Filter, Signal Candidate, forward-return, portfolio targets, Backtest input contract, Backtest PnL smoke, and benchmark returns as `pass_smoke`, Backtest assumptions as `pass_assumption_only`, Point-in-Time status coverage `hold` with lifecycle missing release/resume groups `304`, Backtest engine `hold`, live trading controls `blocked`, and KIS demo account `blocked`.
- KIS demo trading: dry-run order intent and local account preflight exist, but the local MCP `.env.kis` is missing `KIS_PAPER_STOCK`; buying-power checks, order status/cancel flow, kill switch, and explicit confirmation gate are not implemented.
- Backtest readiness: `hold`.
- Live trading readiness: `blocked`.
