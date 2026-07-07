# Point-in-Time Momentum Signal Candidates Smoke

- Input: [[_report/quant/research/2026-07-08-kind-status-point-in-time-liquidity-smoke-20d-20250102-20250321.rows.csv|_report/quant/research/2026-07-08-kind-status-point-in-time-liquidity-smoke-20d-20250102-20250321.rows.csv]]
- Date range: `20250102-20250321`
- Strategy: `001-strategy-universe-momentum`
- Mode: `paper_signal_candidate_only`
- KIS API call: `false`
- Order intent generated: `false`
- Backtest readiness: `hold`
- Live trading readiness: `blocked`
- Rule: `5d ROC > 0.00%` for BUY candidates; `5d ROC < 0` for SELL candidates
- Top N per date/state: `20`
- Machine-readable rows: [[_report/quant/research/2026-07-08-kind-status-point-in-time-momentum-signal-candidates-smoke-20d-20250102-20250321.rows.csv|_report/quant/research/2026-07-08-kind-status-point-in-time-momentum-signal-candidates-smoke-20d-20250102-20250321.rows.csv]]

## Summary

- Candidate rows: `1320`
- Candidate dates: `33`
- Latest candidate date: `2025-03-21`

## State Counts

| State | Count |
| --- | ---: |
| `BUY candidate` | 660 |
| `SELL candidate` | 660 |

## Latest Date Sample

| State | Rank | Code | Company | ROC % | Close |
| --- | ---: | --- | --- | ---: | ---: |
| BUY candidate | 1 | `069920` | 엑시온그룹 | 88.9937 | 1202 |
| BUY candidate | 2 | `101390` | 아이엠 | 63.9362 | 1541 |
| BUY candidate | 3 | `008970` | 동양철관 | 36.8481 | 1207 |
| BUY candidate | 4 | `009410` | 태영건설 | 32.8512 | 3215 |
| BUY candidate | 5 | `024720` | 콜마홀딩스 | 28.9916 | 9210 |
| BUY candidate | 6 | `036930` | 주성엔지니어링 | 25.1108 | 42350 |
| BUY candidate | 7 | `340360` | 다보링크 | 24.7598 | 1688 |
| BUY candidate | 8 | `073190` | 듀오백 | 24.0602 | 3300 |
| BUY candidate | 9 | `232140` | 와이씨 | 23.1141 | 12730 |
| BUY candidate | 10 | `051160` | 지어소프트 | 22.2360 | 9840 |
| BUY candidate | 11 | `199730` | 바이오인프라 | 22.0238 | 6150 |
| BUY candidate | 12 | `032790` | 엠젠솔루션 | 21.7606 | 1231 |
| BUY candidate | 13 | `011230` | 삼화전자 | 20.2586 | 4185 |
| BUY candidate | 14 | `267320` | 나인테크 | 19.7432 | 3730 |
| BUY candidate | 15 | `051500` | CJ프레시웨이 | 19.6517 | 24050 |
| BUY candidate | 16 | `115180` | 큐리언트 | 19.5055 | 8700 |
| BUY candidate | 17 | `194480` | 데브시스터즈 | 17.4627 | 39350 |
| BUY candidate | 18 | `356860` | 티엘비 | 17.3469 | 23000 |
| BUY candidate | 19 | `011300` | 성안머티리얼스 | 17.3228 | 596 |
| BUY candidate | 20 | `053350` | 이니텍 | 17.1429 | 7380 |
| SELL candidate | 1 | `085810` | 알티캐스트 | -53.4495 | 641 |
| SELL candidate | 2 | `028300` | HLB | -35.4167 | 46500 |
| SELL candidate | 3 | `174900` | 앱클론 | -34.6060 | 8050 |
| SELL candidate | 4 | `067630` | HLB생명과학 | -33.1473 | 5990 |
| SELL candidate | 5 | `047920` | HLB제약 | -30.7692 | 17100 |
| SELL candidate | 6 | `015020` | 이스타코 | -26.6557 | 1340 |
| SELL candidate | 7 | `001570` | 금양 | -26.2844 | 9900 |
| SELL candidate | 8 | `113810` | 디젠스 | -25.1282 | 1460 |
| SELL candidate | 9 | `025950` | 동신건설 | -23.7963 | 41150 |
| SELL candidate | 10 | `003580` | HLB글로벌 | -23.6808 | 2965 |
| SELL candidate | 11 | `214610` | 미코바이오메드 | -22.4860 | 555 |
| SELL candidate | 12 | `068050` | 팬엔터테인먼트 | -21.3740 | 3090 |
| SELL candidate | 13 | `475830` | 오름테라퓨틱 | -20.9302 | 23800 |
| SELL candidate | 14 | `226950` | 올릭스 | -20.6237 | 39450 |
| SELL candidate | 15 | `278650` | HLB바이오스텝 | -19.8157 | 1740 |
| SELL candidate | 16 | `010170` | 대한광통신 | -19.6774 | 498 |
| SELL candidate | 17 | `045660` | 에이텍 | -19.6078 | 26650 |
| SELL candidate | 18 | `013360` | 일성건설 | -19.2913 | 3075 |
| SELL candidate | 19 | `024850` | HLB이노베이션 | -19.2713 | 1994 |
| SELL candidate | 20 | `049180` | 셀루메드 | -19.2361 | 1163 |

## Guardrails

- These rows are `Signal Candidate` tracking rows only, not trade instructions.
- The source `Point-in-Time` and Liquidity Filter inputs are still smoke artifacts.
- Do not generate orders from this file.
- Keep `Backtest readiness` at `hold` until full historical status, production Liquidity Filter, cost model, OOS, and Bias Control pass.
