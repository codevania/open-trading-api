# Data Pipeline Smoke Test Result

- Source raw directory: `_report/raw/2026/2026-06-09/quant/smoke-test`
- Validator: `scripts/quant_smoke_validate.py`
- Universe definition mode: `manual_smoke_test`
- Interpretation: `Data Pipeline Smoke Test - Not Quant Validation`
- Bias Control judgment: `hold`
- Lookback: `20`
- Threshold: `0.0`
- Cost model reference: `_report/quant/research/2026-06-08-transaction-cost-slippage-assumptions.md`

| Symbol | Status | Rows | Latest Date | Latest Close | ROC % | Avg Trading Value 20D KRW | Message |
| --- | --- | ---: | --- | ---: | ---: | ---: | --- |
| `000660` | BUY candidate | 21 | 20260605 | 2070000 | 29.2942 | 12079720307940 | ok |
| `005930` | BUY candidate | 21 | 20260605 | 329000 | 23.6842 | 10431533672673 | ok |
| `035420` | BUY candidate | 21 | 20260605 | 255500 | 22.8365 | 657256761422 | ok |

## Limitations

- Manual symbol files are not a Quant Universe.
- This output must not be used as Strategy performance evidence.
- `BUY candidate` and `SELL candidate` are paper Signal Candidate states, not trade instructions.
- Point-in-Time Investable Universe remains required before Backtest interpretation.
- All listed files had at least 21 daily rows, so the parser and ROC calculation path passed.
- Full Backtest interpretation remains blocked until Point-in-Time Universe, OOS, and Bias Control pass.
