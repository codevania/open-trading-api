# Point-in-Time Liquidity Filter Smoke

- Input: [[_report/quant/research/2026-07-08-kind-status-point-in-time-universe-smoke-merged-snapshots-20250102-20250404.rows.csv|_report/quant/research/2026-07-08-kind-status-point-in-time-universe-smoke-merged-snapshots-20250102-20250404.rows.csv]]
- Date range: `20250102-20250404`
- Mode: `point_in_time_liquidity_smoke`
- KIS API call: `false`
- Backtest readiness: `hold`
- Live trading readiness: `blocked`
- Liquidity Filter rule: `avg_trading_value_20d_krw >= 1,000,000,000`
- Machine-readable rows: [[_report/quant/research/2026-07-08-kind-status-point-in-time-liquidity-smoke-20d-20250102-20250404.rows.csv|_report/quant/research/2026-07-08-kind-status-point-in-time-liquidity-smoke-20d-20250102-20250404.rows.csv]]

## Summary

- Input rows: `170567`
- Dates: `62`
- Base `Point-in-Time Universe` include rows: `159048`
- Include rows after Liquidity Filter: `44235`
- Exclude rows after Liquidity Filter: `126332`
- Rows with full lookback evaluated: `109890`

## Liquidity Status Counts

| Status | Count |
| --- | ---: |
| `data_insufficient` | 49158 |
| `fail` | 65655 |
| `not_evaluated_preexisting_exclude` | 11519 |
| `pass` | 44235 |

## Final Status Counts

| Status | Count |
| --- | ---: |
| `exclude` | 126332 |
| `include` | 44235 |

## Exclusion Reason Counts

| Reason | Count |
| --- | ---: |
| `liquidity_history_insufficient` | 49158 |
| `liquidity_value_below_threshold` | 65655 |
| `security_group_not_plain_equity` | 3100 |
| `status_event:managed_issue_active` | 1227 |
| `stock_certificate_not_common` | 7192 |

## Evaluated Sample

| Date | Code | Company | Final Status | Avg Trading Value KRW | Liquidity Status |
| --- | --- | --- | --- | ---: | --- |
| `2025-02-04` | `000020` | 동화약품 | exclude | 324442732 | fail |
| `2025-02-04` | `000040` | KR모터스 | exclude | 68871093 | fail |
| `2025-02-04` | `000050` | 경방 | exclude | 23983752 | fail |
| `2025-02-04` | `000070` | 삼양홀딩스 | exclude | 394315125 | fail |
| `2025-02-04` | `000080` | 하이트진로 | include | 3144282638 | pass |
| `2025-02-04` | `000100` | 유한양행 | include | 214862387075 | pass |
| `2025-02-04` | `000120` | CJ대한통운 | include | 5500663670 | pass |
| `2025-02-04` | `000140` | 하이트진로홀딩스 | exclude | 114606983 | fail |
| `2025-02-04` | `000150` | 두산 | include | 44959732575 | pass |
| `2025-02-04` | `000180` | 성창기업지주 | exclude | 104958043 | fail |
| `2025-02-04` | `000210` | DL | include | 1236242680 | pass |
| `2025-02-04` | `000220` | 유유제약 | exclude | 358537811 | fail |
| `2025-02-04` | `000230` | 일동홀딩스 | exclude | 351249400 | fail |
| `2025-02-04` | `000240` | 한국앤컴퍼니 | include | 1498222470 | pass |
| `2025-02-04` | `000250` | 삼천당제약 | include | 83629551465 | pass |
| `2025-02-04` | `000270` | 기아 | include | 115925002315 | pass |
| `2025-02-04` | `000300` | 대유플러스 | exclude | 0 | fail |
| `2025-02-04` | `000320` | 노루홀딩스 | exclude | 107163584 | fail |
| `2025-02-04` | `000370` | 한화손해보험 | exclude | 666930878 | fail |
| `2025-02-04` | `000390` | 삼화페인트 | exclude | 190440441 | fail |

## Limitations

- This is still a smoke artifact because the current input covers only a bounded `62`-date window.
- The first `lookback - 1` rows per code are excluded as `liquidity_history_insufficient` by design.
- Historical status coverage is still incomplete, so this output is not a Backtest input yet.
- Keep `Backtest readiness` at `hold` until full `Point-in-Time` status and Liquidity Filter coverage are available.
