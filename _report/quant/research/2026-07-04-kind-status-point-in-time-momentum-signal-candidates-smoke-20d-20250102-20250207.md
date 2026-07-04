# Point-in-Time Momentum Signal Candidates Smoke

- Input: [[_report/quant/research/2026-07-04-kind-status-point-in-time-liquidity-smoke-20d-20250102-20250207.rows.csv|_report/quant/research/2026-07-04-kind-status-point-in-time-liquidity-smoke-20d-20250102-20250207.rows.csv]]
- Date range: `20250102-20250207`
- Strategy: `001-strategy-universe-momentum`
- Mode: `paper_signal_candidate_only`
- KIS API call: `false`
- Order intent generated: `false`
- Backtest readiness: `hold`
- Live trading readiness: `blocked`
- Rule: `20d ROC > 0.00%` for BUY candidates; `20d ROC < 0` for SELL candidates
- Top N per date/state: `20`
- Machine-readable rows: [[_report/quant/research/2026-07-04-kind-status-point-in-time-momentum-signal-candidates-smoke-20d-20250102-20250207.rows.csv|_report/quant/research/2026-07-04-kind-status-point-in-time-momentum-signal-candidates-smoke-20d-20250102-20250207.rows.csv]]

## Summary

- Candidate rows: `120`
- Candidate dates: `3`
- Latest candidate date: `2025-02-07`

## State Counts

| State | Count |
| --- | ---: |
| `BUY candidate` | 60 |
| `SELL candidate` | 60 |

## Latest Date Sample

| State | Rank | Code | Company | ROC % | Close |
| --- | ---: | --- | --- | ---: | ---: |
| BUY candidate | 1 | `010100` | 한국무브넥스 | 135.4391 | 7640 |
| BUY candidate | 2 | `160190` | 하이젠알앤엠 | 127.3499 | 40150 |
| BUY candidate | 3 | `161580` | 필옵틱스 | 112.9496 | 44400 |
| BUY candidate | 4 | `098460` | 고영 | 100.8869 | 18120 |
| BUY candidate | 5 | `351320` | 에스에이티이엔지 | 89.2911 | 2510 |
| BUY candidate | 6 | `112290` | 와이씨켐 | 88.1051 | 27200 |
| BUY candidate | 7 | `171010` | 램테크놀러지 | 80.7692 | 5640 |
| BUY candidate | 8 | `277810` | 레인보우로보틱스 | 76.1803 | 410500 |
| BUY candidate | 9 | `168360` | 펨트론 | 74.1573 | 10850 |
| BUY candidate | 10 | `332570` | 와이팜 | 68.6380 | 4705 |
| BUY candidate | 11 | `080220` | 제주반도체 | 68.6176 | 16710 |
| BUY candidate | 12 | `466100` | 클로봇 | 66.0870 | 19100 |
| BUY candidate | 13 | `219550` | 디와이디 | 64.1818 | 903 |
| BUY candidate | 14 | `042660` | 한화오션 | 62.4672 | 61900 |
| BUY candidate | 15 | `115310` | 인포바인 | 55.7971 | 32250 |
| BUY candidate | 16 | `119850` | 지엔씨에너지 | 54.2022 | 12660 |
| BUY candidate | 17 | `301300` | 바이브컴퍼니 | 53.4442 | 6460 |
| BUY candidate | 18 | `042000` | 카페24 | 52.6738 | 57100 |
| BUY candidate | 19 | `064350` | 현대로템 | 52.1989 | 79600 |
| BUY candidate | 20 | `089010` | 켐트로닉스 | 52.1610 | 25700 |
| SELL candidate | 1 | `019490` | 엑시큐어하이트론 | -74.8915 | 752 |
| SELL candidate | 2 | `381620` | 제닉스 | -63.3028 | 10000 |
| SELL candidate | 3 | `178780` | 일월지엠엘 | -58.7861 | 3565 |
| SELL candidate | 4 | `091440` | 한울소재과학 | -54.1272 | 3390 |
| SELL candidate | 5 | `065650` | 하이퍼코퍼레이션 | -52.9887 | 582 |
| SELL candidate | 6 | `214610` | 미코바이오메드 | -45.0850 | 905 |
| SELL candidate | 7 | `206400` | 베노티앤알 | -44.7000 | 1659 |
| SELL candidate | 8 | `012170` | 아센디오 | -42.6434 | 230 |
| SELL candidate | 9 | `196300` | 애니젠 | -42.2881 | 6810 |
| SELL candidate | 10 | `355390` | 크라우드웍스 | -40.9121 | 8940 |
| SELL candidate | 11 | `015020` | 이스타코 | -39.0496 | 1180 |
| SELL candidate | 12 | `432980` | 엠에프씨 | -37.5000 | 4050 |
| SELL candidate | 13 | `064960` | SNT모티브 | -37.2549 | 25600 |
| SELL candidate | 14 | `387570` | 파인메딕스 | -36.0589 | 7820 |
| SELL candidate | 15 | `058110` | 멕아이씨에스 | -32.6765 | 2050 |
| SELL candidate | 16 | `253840` | 수젠텍 | -31.9429 | 6200 |
| SELL candidate | 17 | `298060` | 에스씨엠생명과학 | -30.5764 | 1385 |
| SELL candidate | 18 | `418620` | 이에이트 | -29.3919 | 4180 |
| SELL candidate | 19 | `065500` | 오리엔트정공 | -27.2425 | 4380 |
| SELL candidate | 20 | `115450` | HLB테라퓨틱스 | -26.3977 | 10400 |

## Guardrails

- These rows are `Signal Candidate` tracking rows only, not trade instructions.
- The source `Point-in-Time` and Liquidity Filter inputs are still smoke artifacts.
- Do not generate orders from this file.
- Keep `Backtest readiness` at `hold` until full historical status, production Liquidity Filter, cost model, OOS, and Bias Control pass.
