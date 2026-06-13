# KRX Current Universe v0

- As-of date: `2026-06-13`
- Listed issues raw: `_report/raw/2026/2026-06-13/krx/universe/listed_issues_current.raw.csv`
- Listed issues encoding: `cp949`
- Managed issues raw: `_report/raw/2026/2026-06-13/krx/universe/managed_issues_current.raw.csv`
- Universe mode: `current_snapshot`
- Interpretation: `paper/smoke Universe only`, `not Point-in-Time Universe`
- Bias Control judgment: `hold`
- Machine-readable rows: `_report/quant/research/2026-06-14-krx-current-universe-v0.rows.csv`

## Summary

- Total listed rows: `2875`
- Included rows: `2457`
- Excluded rows: `418`

## Exclusion Reason Counts

| Reason | Count |
| --- | ---: |
| `instrument_name_excluded` | 97 |
| `instrument_type_excluded` | 101 |
| `managed_issue_current` | 101 |
| `market_not_allowed` | 107 |
| `preferred_share_name` | 15 |

## Included Sample

| Code | Company | Market | Security Type |
| --- | --- | --- | --- |
| `000020` | 동화약품 | KOSPI | 보통주 |
| `000040` | KR모터스 | KOSPI | 보통주 |
| `000050` | 경방 | KOSPI | 보통주 |
| `000070` | 삼양홀딩스 | KOSPI | 보통주 |
| `000080` | 하이트진로 | KOSPI | 보통주 |
| `000100` | 유한양행 | KOSPI | 보통주 |
| `000120` | CJ대한통운 | KOSPI | 보통주 |
| `000140` | 하이트진로홀딩스 | KOSPI | 보통주 |
| `000150` | 두산 | KOSPI | 보통주 |
| `000180` | 성창기업지주 | KOSPI | 보통주 |
| `0001A0` | 덕양에너젠 | KOSDAQ | 보통주 |
| `000210` | DL | KOSPI | 보통주 |
| `000220` | 유유제약 | KOSPI | 보통주 |
| `000230` | 일동홀딩스 | KOSPI | 보통주 |
| `000240` | 한국앤컴퍼니 | KOSPI | 보통주 |
| `000250` | 삼천당제약 | KOSDAQ | 보통주 |
| `000270` | 기아 | KOSPI | 보통주 |
| `000300` | DH오토넥스 | KOSPI | 보통주 |
| `000320` | 노루홀딩스 | KOSPI | 보통주 |
| `000370` | 한화손해보험 | KOSPI | 보통주 |

## Guardrails

- This Universe uses current KRX listed issues and current managed-issue exclusions only.
- Listing Age, Liquidity Filter, trading suspension, market-alert, and delisting history are not solved here.
- This artifact can drive paper/smoke validation but not a performance Backtest claim.
- Do not upgrade Strategy interpretation above `hold` until reproducible Point-in-Time snapshots exist.
