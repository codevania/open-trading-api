# KRX Current Universe v0 Liquidity Filter Smoke

- As-of date: `2026-06-15`
- Source Universe rows: `_report/quant/research/2026-06-14-krx-current-universe-v0.rows.csv`
- Source raw directories:
  - `_report/raw/2026/2026-06-13/quant/paper-follow-up`
  - `_report/raw/2026/2026-06-15/quant/universe-ohlcv`
- Filter mode: `current_snapshot_liquidity_smoke`
- Interpretation: `paper/smoke Universe only`, `not Point-in-Time Universe`
- Bias Control judgment: `hold`
- Liquidity Filter rule: `avg_trading_value_20d_krw >= 1,000,000,000`
- Machine-readable rows: `_report/quant/research/2026-06-30-krx-current-universe-v0-liquidity-smoke-expanded-twentyninth10.rows.csv`

## Summary

- Total rows: `2875`
- Base included rows before Liquidity Filter: `2390`
- Included rows after Liquidity Filter: `149`
- Excluded rows after Liquidity Filter: `2726`
- Rows with raw OHLCV evaluated: `291`

## Liquidity Filter Status Counts

| Status | Count |
| --- | ---: |
| `data_missing` | 2099 |
| `fail` | 142 |
| `not_evaluated_preexisting_exclude` | 485 |
| `pass` | 149 |

## Exclusion Reason Counts

| Reason | Count |
| --- | ---: |
| `instrument_name_excluded` | 97 |
| `instrument_type_excluded` | 101 |
| `liquidity_raw_missing` | 2099 |
| `liquidity_value_below_threshold` | 142 |
| `listing_age_calendar_insufficient` | 102 |
| `managed_issue_current` | 101 |
| `market_not_allowed` | 107 |
| `preferred_share_name` | 15 |

## Evaluated Sample

| Code | Company | Final Status | Avg Trading Value 20D KRW | Liquidity Status | Latest Date |
| --- | --- | --- | ---: | --- | --- |
| `000020` | 동화약품 | exclude | 780294214 | fail | 20260615 |
| `000040` | KR모터스 | exclude | 91423666 | fail | 20260615 |
| `000050` | 경방 | exclude | 916143963 | fail | 20260615 |
| `000070` | 삼양홀딩스 | exclude | 790201820 | fail | 20260615 |
| `000140` | 하이트진로홀딩스 | exclude | 228453086 | fail | 20260615 |
| `000180` | 성창기업지주 | exclude | 95916534 | fail | 20260615 |
| `000230` | 일동홀딩스 | exclude | 191386718 | fail | 20260615 |
| `000300` | DH오토넥스 | exclude | 0 | fail | 20260615 |
| `000320` | 노루홀딩스 | exclude | 227570928 | fail | 20260615 |
| `000480` | CR홀딩스 | exclude | 190881915 | fail | 20260615 |
| `000540` | 흥국화재 | exclude | 632356360 | fail | 20260615 |
| `000590` | CS홀딩스 | exclude | 85107110 | fail | 20260615 |
| `000700` | 유수홀딩스 | exclude | 247776027 | fail | 20260615 |
| `000760` | 이화산업 | exclude | 24757780 | fail | 20260615 |
| `000850` | 화천기공 | exclude | 464103022 | fail | 20260615 |
| `000860` | 강남제비스코 | exclude | 367853396 | fail | 20260615 |
| `000890` | 보해양조 | exclude | 228505147 | fail | 20260615 |
| `000910` | 유니온 | exclude | 374059314 | fail | 20260615 |
| `000950` | 전방 | exclude | 38060089 | fail | 20260615 |
| `000970` | 한국주철관 | exclude | 325537980 | fail | 20260615 |

## Limitations

- This is a derived smoke artifact from the current snapshot Universe, not a Point-in-Time Universe.
- Missing raw OHLCV is marked as `liquidity_raw_missing`; it is a data-coverage blocker, not evidence that the stock is illiquid.
- The derived final `status` excludes rows that cannot prove the Liquidity Filter from saved raw data.
- KIS batch collection for the full generated Universe remains required before this can represent the full current Universe.
- Backtest, OOS, Walk-Forward, and Bias Control interpretation remain `hold`.
