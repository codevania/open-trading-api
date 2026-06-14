# KRX Current Universe v0 Liquidity Filter Smoke

- As-of date: `2026-06-13`
- Source Universe rows: `_report/quant/research/2026-06-14-krx-current-universe-v0.rows.csv`
- Source raw directories:
  - `_report/raw/2026/2026-06-13/quant/paper-follow-up`
- Filter mode: `current_snapshot_liquidity_smoke`
- Interpretation: `paper/smoke Universe only`, `not Point-in-Time Universe`
- Bias Control judgment: `hold`
- Liquidity Filter rule: `avg_trading_value_20d_krw >= 1,000,000,000`
- Machine-readable rows: `_report/quant/research/2026-06-14-krx-current-universe-v0-liquidity-smoke.rows.csv`

## Summary

- Total rows: `2875`
- Base included rows before Liquidity Filter: `2390`
- Included rows after Liquidity Filter: `3`
- Excluded rows after Liquidity Filter: `2872`
- Rows with raw OHLCV evaluated: `3`

## Liquidity Filter Status Counts

| Status | Count |
| --- | ---: |
| `data_missing` | 2387 |
| `not_evaluated_preexisting_exclude` | 485 |
| `pass` | 3 |

## Exclusion Reason Counts

| Reason | Count |
| --- | ---: |
| `instrument_name_excluded` | 97 |
| `instrument_type_excluded` | 101 |
| `liquidity_raw_missing` | 2387 |
| `listing_age_calendar_insufficient` | 102 |
| `managed_issue_current` | 101 |
| `market_not_allowed` | 107 |
| `preferred_share_name` | 15 |

## Evaluated Sample

| Code | Company | Final Status | Avg Trading Value 20D KRW | Liquidity Status | Latest Date |
| --- | --- | --- | ---: | --- | --- |
| `000660` | SK하이닉스 | include | 12079686842833 | pass | 20260612 |
| `005930` | 삼성전자 | include | 10406371176321 | pass | 20260612 |
| `035420` | NAVER | include | 963846182491 | pass | 20260612 |

## Limitations

- This is a derived smoke artifact from the current snapshot Universe, not a Point-in-Time Universe.
- Missing raw OHLCV is marked as `liquidity_raw_missing`; it is a data-coverage blocker, not evidence that the stock is illiquid.
- The derived final `status` excludes rows that cannot prove the Liquidity Filter from saved raw data.
- KIS batch collection for the full generated Universe remains required before this can represent the full current Universe.
- Backtest, OOS, Walk-Forward, and Bias Control interpretation remain `hold`.
