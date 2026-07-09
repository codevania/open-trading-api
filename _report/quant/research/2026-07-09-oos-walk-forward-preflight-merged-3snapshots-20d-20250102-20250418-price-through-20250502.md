# OOS Walk-Forward Preflight

- Attribution input: [[_report/quant/research/2026-07-09-backtest-attribution-smoke-merged-3snapshots-20d-20250102-20250418-price-through-20250502.rows.csv|_report/quant/research/2026-07-09-backtest-attribution-smoke-merged-3snapshots-20d-20250102-20250418-price-through-20250502.rows.csv]]
- Preflight mode: `paper_oos_walk_forward_preflight_smoke_only`
- OOS/WF preflight status: `pass_smoke_plumbing_only`
- OOS readiness: `hold`
- Backtest readiness: `hold`
- Live trading readiness: `blocked`
- KIS API call: `false`
- KRX API call: `false`
- Order intent generated: `false`
- Interpretation: temporal fold plumbing smoke only, not an OOS or production `Backtest` result
- Machine-readable folds: [[_report/quant/research/2026-07-09-oos-walk-forward-preflight-merged-3snapshots-20d-20250102-20250418-price-through-20250502.folds.csv|_report/quant/research/2026-07-09-oos-walk-forward-preflight-merged-3snapshots-20d-20250102-20250418-price-through-20250502.folds.csv]]

## Summary

| Metric | Value |
| --- | ---: |
| Attribution rows | 53 |
| Fold rows | 3 |
| Dates | 53 |
| Horizons | 1 |
| Min train dates | 20 |
| Test dates per fold | 10 |
| Requested folds | 3 |
| Broker fee override required | `true` |
| Avg test baseline net return % | -0.0827 |
| Avg test baseline active return % | 0.0466 |

## Fold Status Counts

| Status | Count |
| --- | ---: |
| `pass_smoke_plumbing_only` | 3 |

## Walk-Forward Folds

| Fold | Horizon | Status | Train | Test | Train avg net % | Test avg net % | Test avg active % | Test positive rate | Notes |
| --- | ---: | --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| `wf_01` | 1 | `pass_smoke_plumbing_only` | 2025-02-04..2025-03-04 | 2025-03-05..2025-03-18 | -0.1615 | -0.9466 | -1.2224 | 0.3000 | broker_fee_override_required;point_in_time_status_coverage_not_historical_complete;production_backtest_not_wired |
| `wf_02` | 1 | `pass_smoke_plumbing_only` | 2025-02-04..2025-03-18 | 2025-03-19..2025-04-01 | -0.4232 | -0.6310 | -0.1625 | 0.3000 | broker_fee_override_required;point_in_time_status_coverage_not_historical_complete;production_backtest_not_wired |
| `wf_03` | 1 | `pass_smoke_plumbing_only` | 2025-02-04..2025-04-01 | 2025-04-02..2025-04-15 | -0.4751 | 1.3296 | 1.5247 | 0.6000 | broker_fee_override_required;point_in_time_status_coverage_not_historical_complete;production_backtest_not_wired |

## Guardrails

- This preflight only checks deterministic temporal segmentation of attribution smoke rows.
- It does not optimize parameters, choose a strategy, or validate production OOS performance.
- It inherits assumption-only costs; `broker_fee_override_required=true` still blocks production interpretation.
- It inherits the current `Point-in-Time` status coverage gap and therefore keeps OOS readiness at `hold`.
- Keep `Backtest readiness` at `hold` until historical `Point-in-Time` status coverage, actual costs, production benchmark attribution, OOS, and Bias Control pass.
- Keep `Live trading readiness` at `blocked`; this script never creates order intents.
