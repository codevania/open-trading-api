# Backtest Input Contract Validate

- Liquidity input: [[_report/quant/research/2026-07-04-kind-status-point-in-time-liquidity-smoke-20d-20250102-20250207.rows.csv|_report/quant/research/2026-07-04-kind-status-point-in-time-liquidity-smoke-20d-20250102-20250207.rows.csv]]
- Signal input: [[_report/quant/research/2026-07-04-kind-status-point-in-time-momentum-signal-candidates-smoke-20d-20250102-20250207.rows.csv|_report/quant/research/2026-07-04-kind-status-point-in-time-momentum-signal-candidates-smoke-20d-20250102-20250207.rows.csv]]
- Forward-return input: [[_report/quant/research/2026-07-05-signal-forward-return-smoke-20d-20250102-20250207.rows.csv|_report/quant/research/2026-07-05-signal-forward-return-smoke-20d-20250102-20250207.rows.csv]]
- Portfolio-target input: [[_report/quant/research/2026-07-05-signal-portfolio-targets-smoke-20d-20250102-20250207.rows.csv|_report/quant/research/2026-07-05-signal-portfolio-targets-smoke-20d-20250102-20250207.rows.csv]]
- Expected horizons: `1,5`
- Max position weight: `5.00%`
- Max gross exposure: `100.00%`
- KIS API call: `false`
- KRX API call: `false`
- Order intent generated: `false`
- Contract status: `pass_smoke`
- Backtest readiness: `hold`
- Live trading readiness: `blocked`

## Summary

| Metric | Value |
| --- | ---: |
| Liquidity rows | 63165 |
| Signal rows | 120 |
| Forward-return rows | 240 |
| Portfolio target rows | 60 |
| Liquidity dates | 23 |
| Signal dates | 3 |
| Portfolio target dates | 3 |
| Hold checks | 0 |
| Max gross observed | 1.000000 |

## Checks

| Check | Status | Evidence | Next action |
| --- | --- | --- | --- |
| `required_columns` | `pass` | liquidity missing=none; signals missing=none; forward_returns missing=none; portfolio_targets missing=none | keep schema contract stable |
| `key_uniqueness` | `pass` | liquidity duplicate_keys=0; signals duplicate_keys=0; forward_returns duplicate_keys=0; portfolio_targets duplicate_keys=0 | use these keys for Backtest preflight joins |
| `date_code_integrity` | `pass` | liquidity bad_date_or_code=0; signals bad_date_or_code=0; forward_returns bad_date_or_code=0; portfolio_targets bad_date_or_code=0 | date/code fields are joinable |
| `signal_liquidity_contract` | `pass` | signals_not_in_liquid_universe=0; unexpected_signal_states=none; non_paper_signal_modes=0 | signals are liquidity-backed and paper-only |
| `forward_return_contract` | `pass` | forward_rows_without_signal=0; unexpected_statuses=none; non_paper_modes=0; bad_horizons=0; missing_signal_horizon_keys=0 | forward-return rows cover every signal/horizon key |
| `portfolio_target_contract` | `pass` | targets_without_buy_signal=0; order_intent_rows=0; non_long_targets=0; non_long_only_modes=0; non_paper_target_modes=0 | portfolio targets are long-only and diagnostic-only |
| `portfolio_weight_bounds` | `pass` | bad_weight_rows=0; overweight_rows=0; gross_exposure_violations=0; max_gross_observed=1.000000 | portfolio weights stay inside configured bounds |

## Guardrails

- Passing this contract means the smoke artifacts are internally joinable; it is not a Backtest result.
- This does not model transaction costs, slippage, taxes, benchmark returns, cash drag, or execution constraints.
- Keep `Backtest readiness` at `hold` until historical `Point-in-Time` status coverage, cost model, benchmark, OOS, and Bias Control pass.
- Keep `Live trading readiness` at `blocked` until demo account, buying-power, sellable-quantity, order status/cancel, kill switch, and explicit confirmation gates are implemented.
