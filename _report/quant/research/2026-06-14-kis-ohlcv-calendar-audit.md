# KIS OHLCV Calendar Audit Result

- Source raw directory: `_report/raw/2026/2026-06-13/quant/paper-follow-up`
- Auditor: `scripts/quant_calendar_audit.py`
- Expected calendar source: `symbol-union`
- Overall status: `reference-only`
- Interpretation: `calendar coverage audit only`, `not Backtest ready`
- Bias Control judgment: `hold`

| Symbol | Status | Rows | Unique Dates | First Date | Last Date | Missing Dates | Extra Dates | Duplicate Dates |
| --- | --- | ---: | ---: | --- | --- | --- | --- | --- |
| `000660 SK hynix` | pass | 20 | 20 | 20260514 | 20260612 |  |  |  |
| `005930 Samsung Electronics` | pass | 20 | 20 | 20260514 | 20260612 |  |  |  |
| `035420 NAVER` | pass | 20 | 20 | 20260514 | 20260612 |  |  |  |

## Guardrails

- This audit compares saved OHLCV dates only.
- Without an external KRX/KIS trading calendar, a `pass` is not possible; symbol-union mode is `reference-only` at best.
- Calendar coverage consistency does not solve Survivorship Bias or Point-in-Time Universe construction.
- Keep Strategy interpretation at `hold` until official Universe snapshots, OOS, and Bias Control pass.
