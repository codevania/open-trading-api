# Point-in-Time Momentum Signal Candidates Smoke

- Input: [[_report/quant/research/2026-07-04-kind-status-point-in-time-liquidity-smoke-20250102-20250124.rows.csv|_report/quant/research/2026-07-04-kind-status-point-in-time-liquidity-smoke-20250102-20250124.rows.csv]]
- Date range: `20250102-20250124`
- Strategy: `001-strategy-universe-momentum`
- Mode: `paper_signal_candidate_only`
- KIS API call: `false`
- Order intent generated: `false`
- Backtest readiness: `hold`
- Live trading readiness: `blocked`
- Rule: `5d ROC > 0.00%` for BUY candidates; `5d ROC < 0` for SELL candidates
- Top N per date/state: `20`
- Machine-readable rows: [[_report/quant/research/2026-07-04-kind-status-point-in-time-momentum-signal-candidates-smoke-20250102-20250124.rows.csv|_report/quant/research/2026-07-04-kind-status-point-in-time-momentum-signal-candidates-smoke-20250102-20250124.rows.csv]]

## Summary

- Candidate rows: `480`
- Candidate dates: `12`
- Latest candidate date: `2025-01-24`

## State Counts

| State | Count |
| --- | ---: |
| `BUY candidate` | 240 |
| `SELL candidate` | 240 |

## Latest Date Sample

| State | Rank | Code | Company | ROC % | Close |
| --- | ---: | --- | --- | ---: | ---: |
| BUY candidate | 1 | `177350` | 베셀 | 457.4257 | 1126 |
| BUY candidate | 2 | `098460` | 고영 | 68.0851 | 15800 |
| BUY candidate | 3 | `313760` | 캐리 | 53.6000 | 3840 |
| BUY candidate | 4 | `069540` | 빛과전자 | 52.4416 | 1436 |
| BUY candidate | 5 | `331520` | 밸로프 | 51.7857 | 935 |
| BUY candidate | 6 | `007660` | 이수페타시스 | 44.5230 | 40900 |
| BUY candidate | 7 | `004870` | 티웨이홀딩스 | 43.7741 | 1120 |
| BUY candidate | 8 | `010770` | 평화홀딩스 | 39.6887 | 3590 |
| BUY candidate | 9 | `091810` | 티웨이항공 | 38.3838 | 4110 |
| BUY candidate | 10 | `274090` | 켄코아에어로스페이스 | 36.8914 | 14620 |
| BUY candidate | 11 | `080220` | 제주반도체 | 35.1075 | 13200 |
| BUY candidate | 12 | `432720` | 퀄리타스반도체 | 34.1709 | 13350 |
| BUY candidate | 13 | `070960` | 모나용평 | 34.1654 | 4300 |
| BUY candidate | 14 | `119850` | 지엔씨에너지 | 34.1046 | 13330 |
| BUY candidate | 15 | `046970` | 우리로 | 31.6416 | 1660 |
| BUY candidate | 16 | `332570` | 와이팜 | 31.5876 | 4020 |
| BUY candidate | 17 | `090080` | 평화산업 | 30.7377 | 1276 |
| BUY candidate | 18 | `024830` | 세원물산 | 30.5660 | 10380 |
| BUY candidate | 19 | `477530` | 한국제14호스팩 | 30.4457 | 2605 |
| BUY candidate | 20 | `083650` | 비에이치아이 | 29.9779 | 23500 |
| SELL candidate | 1 | `381620` | 제닉스 | -68.8704 | 9370 |
| SELL candidate | 2 | `064960` | SNT모티브 | -48.3283 | 25500 |
| SELL candidate | 3 | `019490` | 엑시큐어하이트론 | -43.3099 | 966 |
| SELL candidate | 4 | `106240` | 파인테크닉스 | -28.6449 | 1527 |
| SELL candidate | 5 | `312610` | 에이에프더블류 | -26.4780 | 1455 |
| SELL candidate | 6 | `039240` | 경남스틸 | -21.6833 | 5490 |
| SELL candidate | 7 | `013890` | 지누스 | -19.0299 | 21700 |
| SELL candidate | 8 | `028080` | 휴맥스홀딩스 | -17.9551 | 3290 |
| SELL candidate | 9 | `002410` | 범양건영 | -17.2789 | 3040 |
| SELL candidate | 10 | `225530` | 보광산업 | -17.1334 | 5030 |
| SELL candidate | 11 | `131760` | 파인텍 | -16.9751 | 1032 |
| SELL candidate | 12 | `387570` | 파인메딕스 | -16.2264 | 8880 |
| SELL candidate | 13 | `134580` | 탑코미디어 | -15.3377 | 1943 |
| SELL candidate | 14 | `351870` | 차이커뮤니케이션 | -15.2208 | 10750 |
| SELL candidate | 15 | `322780` | 코퍼스코리아 | -14.4008 | 850 |
| SELL candidate | 16 | `084110` | 휴온스글로벌 | -14.3207 | 35000 |
| SELL candidate | 17 | `009450` | 경동나비엔 | -14.2180 | 90500 |
| SELL candidate | 18 | `290690` | 소룩스 | -14.1975 | 6950 |
| SELL candidate | 19 | `362320` | 청담글로벌 | -14.0845 | 5490 |
| SELL candidate | 20 | `034120` | SBS | -13.9344 | 21000 |

## Guardrails

- These rows are `Signal Candidate` tracking rows only, not trade instructions.
- The source `Point-in-Time` and Liquidity Filter inputs are still smoke artifacts.
- Do not generate orders from this file.
- Keep `Backtest readiness` at `hold` until full historical status, production Liquidity Filter, cost model, OOS, and Bias Control pass.
