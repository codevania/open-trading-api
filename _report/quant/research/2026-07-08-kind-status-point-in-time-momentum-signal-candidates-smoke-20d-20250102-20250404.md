# Point-in-Time Momentum Signal Candidates Smoke

- Input: [[_report/quant/research/2026-07-08-kind-status-point-in-time-liquidity-smoke-20d-20250102-20250404.rows.csv|_report/quant/research/2026-07-08-kind-status-point-in-time-liquidity-smoke-20d-20250102-20250404.rows.csv]]
- Date range: `20250102-20250404`
- Strategy: `001-strategy-universe-momentum`
- Mode: `paper_signal_candidate_only`
- KIS API call: `false`
- Order intent generated: `false`
- Backtest readiness: `hold`
- Live trading readiness: `blocked`
- Rule: `5d ROC > 0.00%` for BUY candidates; `5d ROC < 0` for SELL candidates
- Top N per date/state: `20`
- Machine-readable rows: [[_report/quant/research/2026-07-08-kind-status-point-in-time-momentum-signal-candidates-smoke-20d-20250102-20250404.rows.csv|_report/quant/research/2026-07-08-kind-status-point-in-time-momentum-signal-candidates-smoke-20d-20250102-20250404.rows.csv]]

## Summary

- Candidate rows: `1720`
- Candidate dates: `43`
- Latest candidate date: `2025-04-04`

## State Counts

| State | Count |
| --- | ---: |
| `BUY candidate` | 860 |
| `SELL candidate` | 860 |

## Latest Date Sample

| State | Rank | Code | Company | ROC % | Close |
| --- | ---: | --- | --- | ---: | ---: |
| BUY candidate | 1 | `308100` | 형지글로벌 | 141.2262 | 11410 |
| BUY candidate | 2 | `258790` | 소프트캠프 | 100.6522 | 1846 |
| BUY candidate | 3 | `011080` | 형지I&C | 93.9006 | 2575 |
| BUY candidate | 4 | `088340` | 유라클 | 93.4189 | 24100 |
| BUY candidate | 5 | `008600` | 윌비스 | 91.7949 | 748 |
| BUY candidate | 6 | `010770` | 평화홀딩스 | 73.1707 | 9940 |
| BUY candidate | 7 | `053580` | 웹케시 | 71.5831 | 17450 |
| BUY candidate | 8 | `011090` | 에넥스 | 71.3178 | 884 |
| BUY candidate | 9 | `435570` | 에르코스 | 69.1092 | 11770 |
| BUY candidate | 10 | `048430` | 유라테크 | 59.7015 | 13910 |
| BUY candidate | 11 | `090080` | 평화산업 | 49.2537 | 1600 |
| BUY candidate | 12 | `004770` | 써니전자 | 44.7867 | 3055 |
| BUY candidate | 13 | `388720` | 유일로보틱스 | 44.7735 | 83100 |
| BUY candidate | 14 | `376980` | 원티드랩 | 43.0605 | 8040 |
| BUY candidate | 15 | `001000` | 신라섬유 | 42.8571 | 1480 |
| BUY candidate | 16 | `475460` | 미트박스 | 41.1282 | 13760 |
| BUY candidate | 17 | `075130` | 플랜티넷 | 38.7755 | 3400 |
| BUY candidate | 18 | `407400` | 꿈비 | 35.5091 | 10380 |
| BUY candidate | 19 | `014160` | 대영포장 | 34.9810 | 1775 |
| BUY candidate | 20 | `039240` | 경남스틸 | 34.3380 | 6240 |
| SELL candidate | 1 | `194370` | 제이에스코퍼레이션 | -56.6458 | 7600 |
| SELL candidate | 2 | `101390` | 아이엠 | -37.1810 | 517 |
| SELL candidate | 3 | `352770` | 셀레스트라 | -33.8374 | 350 |
| SELL candidate | 4 | `109070` | 주성코퍼레이션 | -28.2813 | 918 |
| SELL candidate | 5 | `412540` | 제일엠앤에스 | -27.1296 | 3935 |
| SELL candidate | 6 | `154030` | 아시아종묘 | -25.3125 | 1912 |
| SELL candidate | 7 | `148250` | 알엔투테크놀로지 | -21.5923 | 6500 |
| SELL candidate | 8 | `013890` | 지누스 | -20.0487 | 16430 |
| SELL candidate | 9 | `381620` | 제닉스 | -19.6939 | 7870 |
| SELL candidate | 10 | `097870` | 효성오앤비 | -19.6658 | 6250 |
| SELL candidate | 11 | `212710` | 아이에스티이 | -18.2587 | 9670 |
| SELL candidate | 12 | `393970` | 대진첨단소재 | -17.5740 | 13930 |
| SELL candidate | 13 | `056090` | 시지메드텍 | -17.0444 | 915 |
| SELL candidate | 14 | `323280` | 태성 | -16.2162 | 23250 |
| SELL candidate | 15 | `465480` | 인스피언 | -16.2084 | 5790 |
| SELL candidate | 16 | `053290` | NE능률 | -16.0671 | 3500 |
| SELL candidate | 17 | `204270` | 제이앤티씨 | -15.4535 | 14170 |
| SELL candidate | 18 | `025820` | 이구산업 | -15.1544 | 4395 |
| SELL candidate | 19 | `319660` | 피에스케이 | -14.4762 | 17960 |
| SELL candidate | 20 | `109610` | 에스와이 | -14.4295 | 3825 |

## Guardrails

- These rows are `Signal Candidate` tracking rows only, not trade instructions.
- The source `Point-in-Time` and Liquidity Filter inputs are still smoke artifacts.
- Do not generate orders from this file.
- Keep `Backtest readiness` at `hold` until full historical status, production Liquidity Filter, cost model, OOS, and Bias Control pass.
