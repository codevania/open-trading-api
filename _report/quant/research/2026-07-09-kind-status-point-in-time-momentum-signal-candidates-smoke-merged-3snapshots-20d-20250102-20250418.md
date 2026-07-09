# Point-in-Time Momentum Signal Candidates Smoke

- Input: [[_report/quant/research/2026-07-09-kind-status-point-in-time-liquidity-smoke-merged-3snapshots-20d-20250102-20250418.rows.csv|_report/quant/research/2026-07-09-kind-status-point-in-time-liquidity-smoke-merged-3snapshots-20d-20250102-20250418.rows.csv]]
- Date range: `2025-01-02..2025-04-18`
- Strategy: `001-strategy-universe-momentum`
- Mode: `paper_signal_candidate_only`
- KIS API call: `false`
- Order intent generated: `false`
- Backtest readiness: `hold`
- Live trading readiness: `blocked`
- Rule: `5d ROC > 0.00%` for BUY candidates; `5d ROC < 0` for SELL candidates
- Top N per date/state: `20`
- Machine-readable rows: [[_report/quant/research/2026-07-09-kind-status-point-in-time-momentum-signal-candidates-smoke-merged-3snapshots-20d-20250102-20250418.rows.csv|_report/quant/research/2026-07-09-kind-status-point-in-time-momentum-signal-candidates-smoke-merged-3snapshots-20d-20250102-20250418.rows.csv]]

## Summary

- Candidate rows: `2120`
- Candidate dates: `53`
- Latest candidate date: `2025-04-18`

## State Counts

| State | Count |
| --- | ---: |
| `BUY candidate` | 1060 |
| `SELL candidate` | 1060 |

## Latest Date Sample

| State | Rank | Code | Company | ROC % | Close |
| --- | ---: | --- | --- | ---: | ---: |
| BUY candidate | 1 | `389140` | 포바이포 | 270.8333 | 22250 |
| BUY candidate | 2 | `013720` | CBI | 112.7660 | 1500 |
| BUY candidate | 3 | `042940` | 상지건설 | 92.2688 | 38050 |
| BUY candidate | 4 | `317770` | 엑스페릭스 | 78.5714 | 5500 |
| BUY candidate | 5 | `357880` | SKAI | 63.8365 | 2605 |
| BUY candidate | 6 | `246690` | TS인베스트먼트 | 61.6162 | 2400 |
| BUY candidate | 7 | `033230` | 인성정보 | 60.2402 | 2535 |
| BUY candidate | 8 | `263700` | 케어랩스 | 60.0000 | 3520 |
| BUY candidate | 9 | `060260` | 뉴보텍 | 57.4521 | 1891 |
| BUY candidate | 10 | `398120` | 에스지헬스케어 | 55.8984 | 4295 |
| BUY candidate | 11 | `054300` | 팬스타엔터프라이즈 | 53.3081 | 811 |
| BUY candidate | 12 | `006220` | 제주은행 | 52.4725 | 11100 |
| BUY candidate | 13 | `429270` | 시지트로닉스 | 51.2448 | 7290 |
| BUY candidate | 14 | `289010` | 아이스크림에듀 | 50.4399 | 5130 |
| BUY candidate | 15 | `444530` | 심플랫폼 | 47.0848 | 16650 |
| BUY candidate | 16 | `315640` | 딥노이드 | 46.3542 | 8430 |
| BUY candidate | 17 | `020710` | 시공테크 | 40.4255 | 9900 |
| BUY candidate | 18 | `241520` | DSC인베스트먼트 | 36.7852 | 8850 |
| BUY candidate | 19 | `382150` | 온코크로스 | 36.5149 | 15590 |
| BUY candidate | 20 | `393210` | 토마토시스템 | 35.6897 | 7870 |
| SELL candidate | 1 | `051630` | 진양화학 | -46.6744 | 2285 |
| SELL candidate | 2 | `003780` | 진양산업 | -31.8456 | 5650 |
| SELL candidate | 3 | `010640` | 진양폴리 | -24.8644 | 4155 |
| SELL candidate | 4 | `193250` | 링크드 | -24.6050 | 668 |
| SELL candidate | 5 | `053580` | 웹케시 | -22.7642 | 12350 |
| SELL candidate | 6 | `052400` | 코나아이 | -22.0436 | 33950 |
| SELL candidate | 7 | `024830` | 세원물산 | -19.9463 | 8950 |
| SELL candidate | 8 | `140430` | 카티스 | -19.5903 | 3140 |
| SELL candidate | 9 | `010770` | 평화홀딩스 | -18.5703 | 9910 |
| SELL candidate | 10 | `048430` | 유라테크 | -18.2469 | 13710 |
| SELL candidate | 11 | `007390` | 네이처셀 | -17.5194 | 26600 |
| SELL candidate | 12 | `043910` | 자연과환경 | -17.4504 | 790 |
| SELL candidate | 13 | `035200` | 프럼파스트 | -17.4451 | 6010 |
| SELL candidate | 14 | `435570` | 에르코스 | -16.9329 | 26000 |
| SELL candidate | 15 | `019570` | 플루토스 | -15.5738 | 309 |
| SELL candidate | 16 | `088340` | 유라클 | -14.5794 | 22850 |
| SELL candidate | 17 | `014160` | 대영포장 | -14.0824 | 1690 |
| SELL candidate | 18 | `308100` | 형지글로벌 | -13.6618 | 7710 |
| SELL candidate | 19 | `355390` | 크라우드웍스 | -13.1596 | 13330 |
| SELL candidate | 20 | `294570` | 쿠콘 | -12.8571 | 21350 |

## Guardrails

- These rows are `Signal Candidate` tracking rows only, not trade instructions.
- The source `Point-in-Time` and Liquidity Filter inputs are still smoke artifacts.
- Do not generate orders from this file.
- Keep `Backtest readiness` at `hold` until full historical status, production Liquidity Filter, cost model, OOS, and Bias Control pass.
