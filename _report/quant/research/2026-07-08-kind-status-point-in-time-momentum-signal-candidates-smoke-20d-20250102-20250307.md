# Point-in-Time Momentum Signal Candidates Smoke

- Input: [[_report/quant/research/2026-07-08-kind-status-point-in-time-liquidity-smoke-20d-20250102-20250307.rows.csv|_report/quant/research/2026-07-08-kind-status-point-in-time-liquidity-smoke-20d-20250102-20250307.rows.csv]]
- Date range: `2025-01-02..2025-03-07`
- Strategy: `001-strategy-universe-momentum`
- Mode: `paper_signal_candidate_only`
- KIS API call: `false`
- Order intent generated: `false`
- Backtest readiness: `hold`
- Live trading readiness: `blocked`
- Rule: `5d ROC > 0.00%` for BUY candidates; `5d ROC < 0` for SELL candidates
- Top N per date/state: `20`
- Machine-readable rows: [[_report/quant/research/2026-07-08-kind-status-point-in-time-momentum-signal-candidates-smoke-20d-20250102-20250307.rows.csv|_report/quant/research/2026-07-08-kind-status-point-in-time-momentum-signal-candidates-smoke-20d-20250102-20250307.rows.csv]]

## Summary

- Candidate rows: `920`
- Candidate dates: `23`
- Latest candidate date: `2025-03-07`

## State Counts

| State | Count |
| --- | ---: |
| `BUY candidate` | 460 |
| `SELL candidate` | 460 |

## Latest Date Sample

| State | Rank | Code | Company | ROC % | Close |
| --- | ---: | --- | --- | ---: | ---: |
| BUY candidate | 1 | `008970` | 동양철관 | 47.7239 | 1006 |
| BUY candidate | 2 | `092790` | 넥스틸 | 47.6015 | 16000 |
| BUY candidate | 3 | `071090` | 하이스틸 | 43.6364 | 4345 |
| BUY candidate | 4 | `097230` | HJ중공업 | 43.3225 | 8800 |
| BUY candidate | 5 | `005010` | 휴스틸 | 38.3929 | 6200 |
| BUY candidate | 6 | `039610` | 화성밸브 | 38.0499 | 11610 |
| BUY candidate | 7 | `035200` | 프럼파스트 | 32.1678 | 4725 |
| BUY candidate | 8 | `456010` | 아이씨티케이 | 31.6854 | 11720 |
| BUY candidate | 9 | `129920` | 대성하이텍 | 29.7600 | 4055 |
| BUY candidate | 10 | `408900` | 스튜디오미르 | 27.4443 | 3715 |
| BUY candidate | 11 | `005710` | 대원산업 | 27.3490 | 7590 |
| BUY candidate | 12 | `310210` | 보로노이 | 26.8542 | 148800 |
| BUY candidate | 13 | `290690` | 소룩스 | 25.8656 | 3090 |
| BUY candidate | 14 | `058430` | 포스코스틸리온 | 23.9474 | 47100 |
| BUY candidate | 15 | `476080` | M83 | 22.6151 | 18380 |
| BUY candidate | 16 | `047810` | 한국항공우주 | 22.4270 | 79700 |
| BUY candidate | 17 | `484870` | 엠앤씨솔루션 | 22.0877 | 80700 |
| BUY candidate | 18 | `003570` | SNT다이내믹스 | 21.8644 | 35950 |
| BUY candidate | 19 | `306200` | 세아제강 | 21.3974 | 194600 |
| BUY candidate | 20 | `024740` | 한일단조 | 21.0784 | 2470 |
| SELL candidate | 1 | `001570` | 금양 | -43.9485 | 13060 |
| SELL candidate | 2 | `060230` | 소니드 | -39.2982 | 519 |
| SELL candidate | 3 | `001470` | 삼부토건 | -29.9564 | 643 |
| SELL candidate | 4 | `051980` | 중앙첨단소재 | -27.6772 | 4795 |
| SELL candidate | 5 | `323350` | 다원넥스뷰 | -25.6678 | 6400 |
| SELL candidate | 6 | `054180` | 메디콕스 | -25.5319 | 245 |
| SELL candidate | 7 | `418550` | 제이오 | -25.2798 | 11350 |
| SELL candidate | 8 | `348370` | 엔켐 | -25.2675 | 90800 |
| SELL candidate | 9 | `281740` | 레이크머티리얼즈 | -24.5043 | 14850 |
| SELL candidate | 10 | `331520` | 밸로프 | -23.1569 | 813 |
| SELL candidate | 11 | `393890` | 더블유씨피 | -22.6366 | 8920 |
| SELL candidate | 12 | `033790` | 피노 | -21.8159 | 6200 |
| SELL candidate | 13 | `323280` | 태성 | -20.8614 | 29400 |
| SELL candidate | 14 | `010170` | 대한광통신 | -20.6897 | 598 |
| SELL candidate | 15 | `450080` | 에코프로머티 | -20.4666 | 75000 |
| SELL candidate | 16 | `112040` | 위메이드 | -20.0758 | 31650 |
| SELL candidate | 17 | `177900` | 쓰리에이로직스 | -19.7861 | 7500 |
| SELL candidate | 18 | `382150` | 온코크로스 | -19.5333 | 9310 |
| SELL candidate | 19 | `328130` | 루닛 | -19.4357 | 51400 |
| SELL candidate | 20 | `317240` | TS트릴리온 | -19.0332 | 268 |

## Guardrails

- These rows are `Signal Candidate` tracking rows only, not trade instructions.
- The source `Point-in-Time` and Liquidity Filter inputs are still smoke artifacts.
- Do not generate orders from this file.
- Keep `Backtest readiness` at `hold` until full historical status, production Liquidity Filter, cost model, OOS, and Bias Control pass.
