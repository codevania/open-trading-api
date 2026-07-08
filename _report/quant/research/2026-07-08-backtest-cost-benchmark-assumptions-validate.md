# Backtest Cost Benchmark Assumptions Validation

- Assumptions: [[_report/quant/data/backtest_cost_benchmark_assumptions.yaml|_report/quant/data/backtest_cost_benchmark_assumptions.yaml]]
- Assumption status: `pass_assumption_only`
- Backtest readiness: `hold`
- Live trading readiness: `blocked`
- KIS/KRX API call: `false`
- Order intent generated: `false`
- Interpretation: local assumption contract only, not a `Backtest` result

## Summary

| Metric | Value |
| --- | ---: |
| Checks | 3 |
| Hold checks | 0 |

## Checks

| Check | Status | Evidence |
| --- | --- | --- |
| `required_sections` | `pass` | cost_model and benchmark sections are present |
| `cost_model` | `pass_assumption_only` | 2 market cost assumptions reconcile |
| `benchmark` | `pass_assumption_only` | primary=KOSPI; source=krx_openapi_index_daily |

## Guardrails

- `pass_assumption_only` means the local assumptions reconcile; it is not Backtest readiness.
- Replace placeholder commission with the actual KIS account/channel fee schedule before production Backtest.
- Benchmark return rows still need to be joined into the Backtest engine separately.
