# Backtest Attribution Smoke

- PnL smoke input: [[_report/quant/research/2026-07-08-backtest-pnl-smoke-20d-20250102-20250418-price-through-20250502.rows.csv|_report/quant/research/2026-07-08-backtest-pnl-smoke-20d-20250102-20250418-price-through-20250502.rows.csv]]
- Assumptions input: [[_report/quant/data/backtest_cost_benchmark_assumptions.yaml|_report/quant/data/backtest_cost_benchmark_assumptions.yaml]]
- Attribution mode: `paper_backtest_attribution_smoke_assumption_only`
- Attribution status: `pass_smoke_assumption_only`
- Backtest readiness: `hold`
- Live trading readiness: `blocked`
- KIS API call: `false`
- KRX API call: `false`
- Order intent generated: `false`
- Interpretation: cost and benchmark attribution smoke only, not a production `Backtest` result
- Machine-readable rows: [[_report/quant/research/2026-07-09-backtest-attribution-smoke-20d-20250102-20250418-price-through-20250502.rows.csv|_report/quant/research/2026-07-09-backtest-attribution-smoke-20d-20250102-20250418-price-through-20250502.rows.csv]]

## Summary

| Metric | Value |
| --- | ---: |
| Attribution rows | 53 |
| PnL rows | 1060 |
| Dates | 53 |
| Horizons | 1 |
| Broker fee override required | `true` |
| Avg gross return % | 0.3758 |
| Avg baseline net return % | 0.0458 |
| Avg stress net return % | -0.3242 |
| Avg baseline active return % | 0.0280 |

## Attribution Status Counts

| Status | Count |
| --- | ---: |
| `pass_smoke_assumption_only` | 53 |

## Date-Horizon Attribution

| Date | Horizon | Status | Gross % | Baseline cost % | Baseline net % | Benchmark % | Baseline active % | Cash weight | Notes |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 2025-02-04 | 1 | `pass_smoke_assumption_only` | 4.0869 | 0.3300 | 3.7569 | 1.1113 | 2.6456 | 0.000000 | broker_fee_override_required |
| 2025-02-05 | 1 | `pass_smoke_assumption_only` | 1.6179 | 0.3300 | 1.2879 | 1.0951 | 0.1928 | 0.000000 | broker_fee_override_required |
| 2025-02-06 | 1 | `pass_smoke_assumption_only` | -0.5553 | 0.3300 | -0.8853 | -0.5846 | -0.3007 | 0.000000 | broker_fee_override_required |
| 2025-02-07 | 1 | `pass_smoke_assumption_only` | 1.0469 | 0.3300 | 0.7169 | -0.0258 | 0.7427 | 0.000000 | broker_fee_override_required |
| 2025-02-10 | 1 | `pass_smoke_assumption_only` | 2.2295 | 0.3300 | 1.8995 | 0.7052 | 1.1943 | 0.000000 | broker_fee_override_required |
| 2025-02-11 | 1 | `pass_smoke_assumption_only` | -1.7512 | 0.3300 | -2.0812 | 0.3679 | -2.4491 | 0.000000 | broker_fee_override_required |
| 2025-02-12 | 1 | `pass_smoke_assumption_only` | 3.3519 | 0.3300 | 3.0219 | 1.3648 | 1.6571 | 0.000000 | broker_fee_override_required |
| 2025-02-13 | 1 | `pass_smoke_assumption_only` | -0.6723 | 0.3300 | -1.0023 | 0.3051 | -1.3074 | 0.000000 | broker_fee_override_required |
| 2025-02-14 | 1 | `pass_smoke_assumption_only` | 3.1014 | 0.3300 | 2.7714 | 0.7476 | 2.0238 | 0.000000 | broker_fee_override_required |
| 2025-02-17 | 1 | `pass_smoke_assumption_only` | 1.3800 | 0.3300 | 1.0500 | 0.6279 | 0.4221 | 0.000000 | broker_fee_override_required |
| 2025-02-18 | 1 | `pass_smoke_assumption_only` | -0.1508 | 0.3300 | -0.4808 | 1.7021 | -2.1829 | 0.000000 | broker_fee_override_required |
| 2025-02-19 | 1 | `pass_smoke_assumption_only` | 0.6617 | 0.3300 | 0.3317 | -0.6536 | 0.9853 | 0.000000 | broker_fee_override_required |
| 2025-02-20 | 1 | `pass_smoke_assumption_only` | -1.8658 | 0.3300 | -2.1958 | 0.0196 | -2.2154 | 0.000000 | broker_fee_override_required |
| 2025-02-21 | 1 | `pass_smoke_assumption_only` | -2.0886 | 0.3300 | -2.4186 | -0.3507 | -2.0679 | 0.000000 | broker_fee_override_required |
| 2025-02-24 | 1 | `pass_smoke_assumption_only` | -2.2327 | 0.3300 | -2.5627 | -0.5663 | -1.9964 | 0.000000 | broker_fee_override_required |
| 2025-02-25 | 1 | `pass_smoke_assumption_only` | -1.1545 | 0.3300 | -1.4845 | 0.4106 | -1.8951 | 0.000000 | broker_fee_override_required |
| 2025-02-26 | 1 | `pass_smoke_assumption_only` | 0.1121 | 0.3300 | -0.2179 | -0.7323 | 0.5144 | 0.000000 | broker_fee_override_required |
| 2025-02-27 | 1 | `pass_smoke_assumption_only` | -2.0531 | 0.3300 | -2.3831 | -3.3935 | 1.0104 | 0.000000 | broker_fee_override_required |
| 2025-02-28 | 1 | `pass_smoke_assumption_only` | -4.0064 | 0.3300 | -4.3364 | -0.1524 | -4.1840 | 0.000000 | broker_fee_override_required |
| 2025-03-04 | 1 | `pass_smoke_assumption_only` | 2.3124 | 0.3300 | 1.9824 | 1.1550 | 0.8274 | 0.000000 | broker_fee_override_required |
| 2025-03-05 | 1 | `pass_smoke_assumption_only` | 1.4125 | 0.3300 | 1.0825 | 0.7048 | 0.3777 | 0.000000 | broker_fee_override_required |
| 2025-03-06 | 1 | `pass_smoke_assumption_only` | -3.6670 | 0.3300 | -3.9970 | -0.4922 | -3.5048 | 0.000000 | broker_fee_override_required |
| 2025-03-07 | 1 | `pass_smoke_assumption_only` | 1.7530 | 0.3300 | 1.4230 | 0.2696 | 1.1534 | 0.000000 | broker_fee_override_required |
| 2025-03-10 | 1 | `pass_smoke_assumption_only` | -0.8655 | 0.3300 | -1.1955 | -1.2757 | 0.0802 | 0.000000 | broker_fee_override_required |
| 2025-03-11 | 1 | `pass_smoke_assumption_only` | 0.5840 | 0.3300 | 0.2540 | 1.4667 | -1.2127 | 0.000000 | broker_fee_override_required |
| 2025-03-12 | 1 | `pass_smoke_assumption_only` | -2.7670 | 0.3300 | -3.0970 | -0.0458 | -3.0512 | 0.000000 | broker_fee_override_required |
| 2025-03-13 | 1 | `pass_smoke_assumption_only` | 0.1101 | 0.3300 | -0.2199 | -0.2829 | 0.0630 | 0.000000 | broker_fee_override_required |
| 2025-03-14 | 1 | `pass_smoke_assumption_only` | -0.7303 | 0.3300 | -1.0603 | 1.7273 | -2.7876 | 0.000000 | broker_fee_override_required |
| 2025-03-17 | 1 | `pass_smoke_assumption_only` | -0.7852 | 0.3300 | -1.1152 | 0.0632 | -1.1784 | 0.000000 | broker_fee_override_required |
| 2025-03-18 | 1 | `pass_smoke_assumption_only` | -1.2102 | 0.3300 | -1.5402 | 0.6232 | -2.1634 | 0.000000 | broker_fee_override_required |
| 2025-03-19 | 1 | `pass_smoke_assumption_only` | -1.9282 | 0.3300 | -2.2582 | 0.3226 | -2.5808 | 0.000000 | broker_fee_override_required |
| 2025-03-20 | 1 | `pass_smoke_assumption_only` | -3.1450 | 0.3300 | -3.4750 | 0.2287 | -3.7037 | 0.000000 | broker_fee_override_required |
| 2025-03-21 | 1 | `pass_smoke_assumption_only` | -1.5722 | 0.3300 | -1.9022 | -0.4184 | -1.4838 | 0.000000 | broker_fee_override_required |
| 2025-03-24 | 1 | `pass_smoke_assumption_only` | 0.3801 | 0.3300 | 0.0501 | -0.6178 | 0.6679 | 0.000000 | broker_fee_override_required |
| 2025-03-25 | 1 | `pass_smoke_assumption_only` | -3.7362 | 0.3300 | -4.0662 | 1.0754 | -5.1416 | 0.000000 | broker_fee_override_required |
| 2025-03-26 | 1 | `pass_smoke_assumption_only` | -1.4189 | 0.3300 | -1.7489 | -1.3915 | -0.3574 | 0.000000 | broker_fee_override_required |
| 2025-03-27 | 1 | `pass_smoke_assumption_only` | -1.9918 | 0.3300 | -2.3218 | -1.8860 | -0.4358 | 0.000000 | broker_fee_override_required |
| 2025-03-28 | 1 | `pass_smoke_assumption_only` | -0.1384 | 0.3300 | -0.4684 | -3.0047 | 2.5363 | 0.000000 | broker_fee_override_required |
| 2025-03-31 | 1 | `pass_smoke_assumption_only` | 7.6629 | 0.3300 | 7.3329 | 1.6231 | 5.7098 | 0.000000 | broker_fee_override_required |
| 2025-04-01 | 1 | `pass_smoke_assumption_only` | 2.8777 | 0.3300 | 2.5477 | -0.6159 | 3.1636 | 0.000000 | broker_fee_override_required |
| 2025-04-02 | 1 | `pass_smoke_assumption_only` | -2.0982 | 0.3300 | -2.4282 | -0.7646 | -1.6636 | 0.000000 | broker_fee_override_required |
| 2025-04-03 | 1 | `pass_smoke_assumption_only` | 3.9291 | 0.3300 | 3.5991 | -0.8558 | 4.4549 | 0.000000 | broker_fee_override_required |
| 2025-04-04 | 1 | `pass_smoke_assumption_only` | 14.1586 | 0.3300 | 13.8286 | -5.5658 | 19.3944 | 0.000000 | broker_fee_override_required |
| 2025-04-07 | 1 | `pass_smoke_assumption_only` | 0.6639 | 0.3300 | 0.3339 | 0.2590 | 0.0749 | 0.000000 | broker_fee_override_required |
| 2025-04-08 | 1 | `pass_smoke_assumption_only` | -5.5424 | 0.3300 | -5.8724 | -1.7363 | -4.1361 | 0.000000 | broker_fee_override_required |
| 2025-04-09 | 1 | `pass_smoke_assumption_only` | 2.5854 | 0.3300 | 2.2554 | 6.5989 | -4.3435 | 0.000000 | broker_fee_override_required |
| 2025-04-10 | 1 | `pass_smoke_assumption_only` | -0.7744 | 0.3300 | -1.1044 | -0.5047 | -0.5997 | 0.000000 | broker_fee_override_required |
| 2025-04-11 | 1 | `pass_smoke_assumption_only` | 2.7058 | 0.3300 | 2.3758 | 0.9524 | 1.4234 | 0.000000 | broker_fee_override_required |
| 2025-04-14 | 1 | `pass_smoke_assumption_only` | 0.1867 | 0.3300 | -0.1433 | 0.8763 | -1.0196 | 0.000000 | broker_fee_override_required |
| 2025-04-15 | 1 | `pass_smoke_assumption_only` | 0.7816 | 0.3300 | 0.4516 | -1.2101 | 1.6617 | 0.000000 | broker_fee_override_required |
| 2025-04-16 | 1 | `pass_smoke_assumption_only` | 6.0500 | 0.3300 | 5.7200 | 0.9389 | 4.7811 | 0.000000 | broker_fee_override_required |
| 2025-04-17 | 1 | `pass_smoke_assumption_only` | 1.6893 | 0.3300 | 1.3593 | 0.5266 | 0.8327 | 0.000000 | broker_fee_override_required |
| 2025-04-18 | 1 | `pass_smoke_assumption_only` | 1.3861 | 0.3300 | 1.0561 | 0.2013 | 0.8548 | 0.000000 | broker_fee_override_required |

## Guardrails

- Costs use local assumption rows only; `broker_fee_override_required=true` means actual KIS account/channel fees are still missing.
- Baseline and stress cost estimates are date/horizon diagnostics, not execution fills.
- Benchmark-active return uses local benchmark smoke rows already joined into PnL smoke; it is not production benchmark attribution.
- Cash return is assumed to be zero for this smoke, and cash drag is reported only as a diagnostic.
- This still does not model rebalance execution timing, taxes beyond round-trip assumptions, delisting/event timing, OOS, or Bias Control.
- Keep `Backtest readiness` at `hold` until historical `Point-in-Time` status coverage, actual costs, production benchmark attribution, OOS, and Bias Control pass.
- Keep `Live trading readiness` at `blocked`; this script never creates order intents.
