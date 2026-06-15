# Data Pipeline Smoke Test Result

- Source raw directory: `_report/raw/2026/2026-06-15/quant/universe-ohlcv`
- Validator: `scripts/quant_smoke_validate.py`
- Universe definition mode: `manual_smoke_test`
- Interpretation: `Data Pipeline Smoke Test - Not Quant Validation`
- Bias Control judgment: `hold`
- Lookback: `20`
- Threshold: `0.0`
- Cost model reference: `_report/quant/research/2026-06-08-transaction-cost-slippage-assumptions.md`

| Symbol | Status | Rows | Latest Date | Latest Close | ROC % | Avg Trading Value 20D KRW | Message |
| --- | --- | ---: | --- | ---: | ---: | ---: | --- |
| `000020` | SELL candidate | 71 | 20260615 | 5370 | -10.9453 | 780294214 | ok |
| `000040` | SELL candidate | 71 | 20260615 | 340 | -14.5729 | 91423666 | ok |
| `000050` | SELL candidate | 71 | 20260615 | 8700 | -10.4938 | 916143963 | ok |
| `000070` | SELL candidate | 71 | 20260615 | 57100 | -9.2210 | 790201820 | ok |
| `000080` | SELL candidate | 71 | 20260615 | 16020 | -7.3453 | 3189955734 | ok |
| `000100` | SELL candidate | 71 | 20260615 | 78900 | -11.7450 | 27434149333 | ok |
| `000120` | SELL candidate | 71 | 20260615 | 85300 | -10.0211 | 6503111895 | ok |
| `000140` | SELL candidate | 71 | 20260615 | 8380 | -7.0953 | 228453086 | ok |
| `000150` | BUY candidate | 71 | 20260615 | 1709000 | 0.3523 | 220005532594 | ok |
| `000180` | SELL candidate | 71 | 20260615 | 5150 | -18.5127 | 95916534 | ok |

## Limitations

- Manual symbol files are not a Quant Universe.
- This output must not be used as Strategy performance evidence.
- `BUY candidate` and `SELL candidate` are paper Signal Candidate states, not trade instructions.
- Point-in-Time Investable Universe remains required before Backtest interpretation.
- All listed files had at least 21 daily rows, so the parser and ROC calculation path passed.
- Full Backtest interpretation remains blocked until Point-in-Time Universe, OOS, and Bias Control pass.
