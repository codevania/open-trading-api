# Point-in-Time Liquidity Filter Smoke

- Input: [[_report/quant/research/2026-07-03-kind-status-point-in-time-universe-smoke-20250102-20250124.rows.csv|_report/quant/research/2026-07-03-kind-status-point-in-time-universe-smoke-20250102-20250124.rows.csv]]
- Date range: `20250102-20250124`
- Mode: `point_in_time_liquidity_smoke`
- KIS API call: `false`
- Backtest readiness: `hold`
- Live trading readiness: `blocked`
- Liquidity Filter rule: `avg_trading_value_5d_krw >= 1,000,000,000`
- Machine-readable rows: [[_report/quant/research/2026-07-04-kind-status-point-in-time-liquidity-smoke-20250102-20250124.rows.csv|_report/quant/research/2026-07-04-kind-status-point-in-time-liquidity-smoke-20250102-20250124.rows.csv]]

## Summary

- Input rows: `46659`
- Dates: `17`
- Base `Point-in-Time Universe` include rows: `43553`
- Include rows after Liquidity Filter: `11877`
- Exclude rows after Liquidity Filter: `34782`
- Rows with full lookback evaluated: `33294`

## Liquidity Status Counts

| Status | Count |
| --- | ---: |
| `data_insufficient` | 10259 |
| `fail` | 21417 |
| `not_evaluated_preexisting_exclude` | 3106 |
| `pass` | 11877 |

## Final Status Counts

| Status | Count |
| --- | ---: |
| `exclude` | 34782 |
| `include` | 11877 |

## Exclusion Reason Counts

| Reason | Count |
| --- | ---: |
| `liquidity_history_insufficient` | 10259 |
| `liquidity_value_below_threshold` | 21417 |
| `security_group_not_plain_equity` | 854 |
| `status_event:managed_issue_active` | 280 |
| `stock_certificate_not_common` | 1972 |

## Evaluated Sample

| Date | Code | Company | Final Status | Avg Trading Value KRW | Liquidity Status |
| --- | --- | --- | --- | ---: | --- |
| `2025-01-08` | `000020` | 동화약품 | exclude | 400947202 | fail |
| `2025-01-08` | `000040` | KR모터스 | exclude | 57534489 | fail |
| `2025-01-08` | `000050` | 경방 | exclude | 30116918 | fail |
| `2025-01-08` | `000070` | 삼양홀딩스 | exclude | 539139660 | fail |
| `2025-01-08` | `000080` | 하이트진로 | include | 2681324764 | pass |
| `2025-01-08` | `000100` | 유한양행 | include | 284761898080 | pass |
| `2025-01-08` | `000120` | CJ대한통운 | include | 5915928640 | pass |
| `2025-01-08` | `000140` | 하이트진로홀딩스 | exclude | 148143636 | fail |
| `2025-01-08` | `000150` | 두산 | include | 53470885100 | pass |
| `2025-01-08` | `000180` | 성창기업지주 | exclude | 51630421 | fail |
| `2025-01-08` | `000210` | DL | include | 1335867920 | pass |
| `2025-01-08` | `000220` | 유유제약 | exclude | 869989511 | fail |
| `2025-01-08` | `000230` | 일동홀딩스 | exclude | 853608984 | fail |
| `2025-01-08` | `000240` | 한국앤컴퍼니 | include | 1317212544 | pass |
| `2025-01-08` | `000250` | 삼천당제약 | include | 66788564340 | pass |
| `2025-01-08` | `000270` | 기아 | include | 94294071460 | pass |
| `2025-01-08` | `000300` | 대유플러스 | exclude | 0 | fail |
| `2025-01-08` | `000320` | 노루홀딩스 | exclude | 125965620 | fail |
| `2025-01-08` | `000370` | 한화손해보험 | exclude | 658906988 | fail |
| `2025-01-08` | `000390` | 삼화페인트 | exclude | 208935586 | fail |

## Limitations

- This is still a smoke artifact because the current input covers only a bounded 17-date window.
- The first `lookback - 1` rows per code are excluded as `liquidity_history_insufficient` by design.
- Historical status coverage is still incomplete, so this output is not a Backtest input yet.
- Keep `Backtest readiness` at `hold` until full `Point-in-Time` status and Liquidity Filter coverage are available.
