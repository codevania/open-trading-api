# Data Pipeline Smoke Test Result

- Source raw directory: `_report/raw/2026/2026-06-05`
- Validator: `scripts/quant_smoke_validate.py`
- Universe definition mode: `manual_smoke_test`
- Interpretation: `Data Pipeline Smoke Test - Not Quant Validation`
- Bias Control judgment: `hold`
- Lookback: `20`
- Threshold: `0.0`
- Cost model reference: `_report/quant/research/2026-06-08-transaction-cost-slippage-assumptions.md`

| Symbol | Status | Rows | Latest Date | Latest Close | ROC % | Avg Trading Value 20D KRW | Message |
| --- | --- | ---: | --- | ---: | ---: | ---: | --- |
| `000660` | data-insufficient | 5 | 20260605 | 2070000 |  |  | need at least 21 rows for 20-day ROC |
| `005930` | data-insufficient | 5 | 20260605 | 329000 |  |  | need at least 21 rows for 20-day ROC |
| `454910` | data-insufficient | 5 | 20260605 | 140300 |  |  | need at least 21 rows for 20-day ROC |

## Limitations

- Manual symbol files are not a Quant Universe.
- This output must not be used as Strategy performance evidence.
- Point-in-Time Investable Universe remains required before Backtest interpretation.
- Files with fewer than 21 daily rows only prove the parser and `data-insufficient` path.
- Full smoke test acceptance remains blocked until raw files with enough daily rows are saved under `_report/raw/YYYY/YYYY-MM-DD/quant/smoke-test/`.
