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
| `000210` | SELL candidate | 71 | 20260615 | 55200 | -12.6582 | 5921823646 | ok |
| `000220` | SELL candidate | 71 | 20260615 | 3900 | -3.7037 | 3165085379 | ok |
| `000230` | SELL candidate | 71 | 20260615 | 7300 | -14.3192 | 191386718 | ok |
| `000240` | BUY candidate | 71 | 20260615 | 30650 | 25.6148 | 6074605698 | ok |
| `000250` | SELL candidate | 71 | 20260615 | 266000 | -34.3210 | 68200375025 | ok |
| `000270` | SELL candidate | 71 | 20260615 | 167500 | -5.9517 | 270150484096 | ok |
| `000300` | HOLD | 71 | 20260615 | 4200 | 0.0000 | 0 | ok |
| `000320` | SELL candidate | 71 | 20260615 | 17850 | -12.5000 | 227570928 | ok |
| `000370` | SELL candidate | 71 | 20260615 | 6720 | -1.8978 | 9478891538 | ok |
| `000390` | SELL candidate | 71 | 20260615 | 6600 | -19.5122 | 1498245029 | ok |
| `000400` | SELL candidate | 71 | 20260615 | 1886 | -9.7608 | 2067630817 | ok |
| `000430` | BUY candidate | 71 | 20260615 | 5130 | 20.7059 | 6172444250 | ok |
| `000440` | SELL candidate | 71 | 20260615 | 14910 | -21.3193 | 1209107190 | ok |
| `000480` | BUY candidate | 71 | 20260615 | 4880 | 0.6186 | 190881915 | ok |
| `000490` | SELL candidate | 71 | 20260615 | 8280 | -21.3675 | 2840997054 | ok |
| `000500` | SELL candidate | 71 | 20260615 | 252000 | -36.8421 | 70754542325 | ok |
| `000520` | SELL candidate | 71 | 20260615 | 7520 | -12.6597 | 1561701103 | ok |
| `000540` | SELL candidate | 71 | 20260615 | 3715 | -11.1244 | 632356360 | ok |
| `000590` | SELL candidate | 71 | 20260615 | 72700 | -6.5553 | 85107110 | ok |
| `000640` | SELL candidate | 71 | 20260615 | 84800 | -12.3061 | 1567737722 | ok |

## Limitations

- Manual symbol files are not a Quant Universe.
- This output must not be used as Strategy performance evidence.
- `BUY candidate` and `SELL candidate` are paper Signal Candidate states, not trade instructions.
- Point-in-Time Investable Universe remains required before Backtest interpretation.
- All listed files had at least 21 daily rows, so the parser and ROC calculation path passed.
- Full Backtest interpretation remains blocked until Point-in-Time Universe, OOS, and Bias Control pass.
