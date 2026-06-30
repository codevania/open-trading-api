# Data Pipeline Smoke Test Result

- Source raw directory: `_report/raw/2026/2026-06-13/quant/paper-follow-up`
- Validator: [[scripts/quant_smoke_validate.py|scripts/quant_smoke_validate.py]]
- Universe definition mode: `manual_smoke_test`
- Interpretation: `Data Pipeline Smoke Test - Not Quant Validation`
- Bias Control judgment: `hold`
- Lookback: `5`
- Threshold: `0.0`
- Cost model reference: [[_report/quant/research/2026-06-08-transaction-cost-slippage-assumptions|_report/quant/research/2026-06-08-transaction-cost-slippage-assumptions.md]]

| Symbol | Status | Rows | Latest Date | Latest Close | ROC % | Avg Trading Value 20D KRW | Message |
| --- | --- | ---: | --- | ---: | ---: | ---: | --- |
| `000660 SK hynix` | BUY candidate | 20 | 20260612 | 2150000 | 3.8647 | 12079686842833 | ok |
| `005930 Samsung Electronics` | SELL candidate | 20 | 20260612 | 322500 | -1.9757 | 10406371176321 | ok |
| `035420 NAVER` | SELL candidate | 20 | 20260612 | 247000 | -3.3268 | 963846182491 | ok |

## Limitations

- Manual symbol files are not a Quant Universe.
- This output must not be used as Strategy performance evidence.
- `BUY candidate` and `SELL candidate` are paper Signal Candidate states, not trade instructions.
- Point-in-Time Investable Universe remains required before Backtest interpretation.
- All listed files had at least 6 daily rows, so the parser and ROC calculation path passed.
- Full Backtest interpretation remains blocked until Point-in-Time Universe, OOS, and Bias Control pass.
