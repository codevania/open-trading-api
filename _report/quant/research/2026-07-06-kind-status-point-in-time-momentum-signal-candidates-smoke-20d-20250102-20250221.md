# Point-in-Time Momentum Signal Candidates Smoke

- Input: [[_report/quant/research/2026-07-06-kind-status-point-in-time-liquidity-smoke-20d-20250102-20250221.rows.csv|_report/quant/research/2026-07-06-kind-status-point-in-time-liquidity-smoke-20d-20250102-20250221.rows.csv]]
- Date range: `2025-01-02..2025-02-21`
- Strategy: `001-strategy-universe-momentum`
- Mode: `paper_signal_candidate_only`
- KIS API call: `false`
- Order intent generated: `false`
- Backtest readiness: `hold`
- Live trading readiness: `blocked`
- Rule: `20d ROC > 0.00%` for BUY candidates; `20d ROC < 0` for SELL candidates
- Top N per date/state: `20`
- Machine-readable rows: [[_report/quant/research/2026-07-06-kind-status-point-in-time-momentum-signal-candidates-smoke-20d-20250102-20250221.rows.csv|_report/quant/research/2026-07-06-kind-status-point-in-time-momentum-signal-candidates-smoke-20d-20250102-20250221.rows.csv]]

## Summary

- Candidate rows: `520`
- Candidate dates: `13`
- Latest candidate date: `2025-02-21`

## State Counts

| State | Count |
| --- | ---: |
| `BUY candidate` | 260 |
| `SELL candidate` | 260 |

## Latest Date Sample

| State | Rank | Code | Company | ROC % | Close |
| --- | ---: | --- | --- | ---: | ---: |
| BUY candidate | 1 | `226950` | 올릭스 | 206.4631 | 43150 |
| BUY candidate | 2 | `388720` | 유일로보틱스 | 110.9792 | 71100 |
| BUY candidate | 3 | `105550` | 엣지파운드리 | 104.3478 | 4935 |
| BUY candidate | 4 | `010770` | 평화홀딩스 | 93.9279 | 5110 |
| BUY candidate | 5 | `340930` | 유일에너테크 | 91.6124 | 2650 |
| BUY candidate | 6 | `382150` | 온코크로스 | 88.1406 | 12850 |
| BUY candidate | 7 | `065170` | 비엘팜텍 | 86.5672 | 3625 |
| BUY candidate | 8 | `377030` | 맥스트 | 84.5192 | 2360 |
| BUY candidate | 9 | `347700` | 라이프시맨틱스 | 79.2115 | 7500 |
| BUY candidate | 10 | `082270` | 젬백스 | 78.7679 | 32500 |
| BUY candidate | 11 | `012450` | 한화에어로스페이스 | 74.8344 | 660000 |
| BUY candidate | 12 | `241520` | DSC인베스트먼트 | 73.9895 | 4950 |
| BUY candidate | 13 | `113810` | 디젠스 | 73.3021 | 2220 |
| BUY candidate | 14 | `119850` | 지엔씨에너지 | 71.9043 | 16520 |
| BUY candidate | 15 | `351320` | 에스에이티이엔지 | 67.8322 | 2400 |
| BUY candidate | 16 | `090710` | 휴림로봇 | 67.3755 | 2755 |
| BUY candidate | 17 | `419530` | SAMG엔터 | 67.2378 | 24400 |
| BUY candidate | 18 | `331520` | 밸로프 | 65.1050 | 1022 |
| BUY candidate | 19 | `172670` | 에이엘티 | 64.4737 | 12500 |
| BUY candidate | 20 | `038390` | 레드캡투어 | 63.7931 | 14250 |
| SELL candidate | 1 | `210120` | 캔버스엔 | -82.8241 | 3710 |
| SELL candidate | 2 | `078860` | 엔에스이엔엠 | -70.3654 | 2190 |
| SELL candidate | 3 | `065650` | 하이퍼코퍼레이션 | -68.4484 | 425 |
| SELL candidate | 4 | `290690` | 소룩스 | -62.3670 | 2830 |
| SELL candidate | 5 | `381620` | 제닉스 | -62.2408 | 11290 |
| SELL candidate | 6 | `019490` | 엑시큐어하이트론 | -50.3871 | 769 |
| SELL candidate | 7 | `192410` | 오늘이엔엠 | -49.9476 | 956 |
| SELL candidate | 8 | `091440` | 한울소재과학 | -46.0425 | 2795 |
| SELL candidate | 9 | `064960` | SNT모티브 | -43.7247 | 27800 |
| SELL candidate | 10 | `355390` | 크라우드웍스 | -41.7052 | 8820 |
| SELL candidate | 11 | `214610` | 미코바이오메드 | -38.7518 | 844 |
| SELL candidate | 12 | `187660` | 현대ADM | -32.5090 | 1883 |
| SELL candidate | 13 | `073570` | 리튬포어스 | -31.7594 | 1055 |
| SELL candidate | 14 | `115610` | 이미지스 | -31.2046 | 2370 |
| SELL candidate | 15 | `294090` | 이오플로우 | -27.7429 | 2305 |
| SELL candidate | 16 | `039240` | 경남스틸 | -24.8371 | 4615 |
| SELL candidate | 17 | `083660` | CSA 코스믹 | -24.6591 | 663 |
| SELL candidate | 18 | `033100` | 제룡전기 | -24.6324 | 41000 |
| SELL candidate | 19 | `443060` | HD현대마린솔루션 | -24.2857 | 143100 |
| SELL candidate | 20 | `445680` | 큐리옥스바이오시스템즈 | -23.7438 | 15480 |

## Guardrails

- These rows are `Signal Candidate` tracking rows only, not trade instructions.
- The source `Point-in-Time` and Liquidity Filter inputs are still smoke artifacts.
- Do not generate orders from this file.
- Keep `Backtest readiness` at `hold` until full historical status, production Liquidity Filter, cost model, OOS, and Bias Control pass.
