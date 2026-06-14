# KRX Current Universe v0

- As-of date: `2026-06-13`
- Listed issues raw: `_report/raw/2026/2026-06-13/krx/universe/listed_issues_current.raw.csv`
- Listed issues encoding: `cp949`
- Managed issues raw: `_report/raw/2026/2026-06-13/krx/universe/managed_issues_current.raw.csv`
- Universe mode: `current_snapshot`
- Interpretation: `paper/smoke Universe only`, `not Point-in-Time Universe`
- Bias Control judgment: `hold`
- Listing Age guard: `365` calendar days minimum
- Machine-readable rows: `_report/quant/research/2026-06-14-krx-current-universe-v0.rows.csv`

## Summary

- Total listed rows: `2875`
- Included rows: `2390`
- Excluded rows: `485`

## Exclusion Reason Counts

| Reason | Count |
| --- | ---: |
| `instrument_name_excluded` | 97 |
| `instrument_type_excluded` | 101 |
| `listing_age_calendar_insufficient` | 102 |
| `managed_issue_current` | 101 |
| `market_not_allowed` | 107 |
| `preferred_share_name` | 15 |

## Included Sample

| Code | Company | Market | Security Type | Listing Date | Calendar Age Days |
| --- | --- | --- | --- | --- | ---: |
| `000020` | 동화약품 | KOSPI | 보통주 | 1976/03/24 | 18343 |
| `000040` | KR모터스 | KOSPI | 보통주 | 1976/05/25 | 18281 |
| `000050` | 경방 | KOSPI | 보통주 | 1956/03/03 | 25669 |
| `000070` | 삼양홀딩스 | KOSPI | 보통주 | 1968/12/27 | 20987 |
| `000080` | 하이트진로 | KOSPI | 보통주 | 2009/10/19 | 6081 |
| `000100` | 유한양행 | KOSPI | 보통주 | 1962/11/01 | 23235 |
| `000120` | CJ대한통운 | KOSPI | 보통주 | 1956/07/02 | 25548 |
| `000140` | 하이트진로홀딩스 | KOSPI | 보통주 | 1973/09/19 | 19260 |
| `000150` | 두산 | KOSPI | 보통주 | 1973/06/29 | 19342 |
| `000180` | 성창기업지주 | KOSPI | 보통주 | 1976/06/02 | 18273 |
| `000210` | DL | KOSPI | 보통주 | 1976/02/02 | 18394 |
| `000220` | 유유제약 | KOSPI | 보통주 | 1975/11/18 | 18470 |
| `000230` | 일동홀딩스 | KOSPI | 보통주 | 1975/06/28 | 18613 |
| `000240` | 한국앤컴퍼니 | KOSPI | 보통주 | 1968/12/27 | 20987 |
| `000250` | 삼천당제약 | KOSDAQ | 보통주 | 2000/10/04 | 9383 |
| `000270` | 기아 | KOSPI | 보통주 | 1973/07/21 | 19320 |
| `000300` | DH오토넥스 | KOSPI | 보통주 | 1975/06/09 | 18632 |
| `000320` | 노루홀딩스 | KOSPI | 보통주 | 1973/08/10 | 19300 |
| `000370` | 한화손해보험 | KOSPI | 보통주 | 1975/06/30 | 18611 |
| `000390` | SP삼화 | KOSPI | 보통주 | 1993/09/10 | 11964 |

## Guardrails

- This Universe uses current KRX listed issues and current managed-issue exclusions only.
- Listing Age is represented by a calendar-day guard, not exact trading-day age.
- Liquidity Filter, trading suspension, market-alert, and delisting history are not solved here.
- This artifact can drive paper/smoke validation but not a performance Backtest claim.
- Do not upgrade Strategy interpretation above `hold` until reproducible Point-in-Time snapshots exist.
