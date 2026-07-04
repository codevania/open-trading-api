# Signal Portfolio Targets Smoke

- Signal input: [[_report/quant/research/2026-07-04-kind-status-point-in-time-momentum-signal-candidates-smoke-20d-20250102-20250207.rows.csv|_report/quant/research/2026-07-04-kind-status-point-in-time-momentum-signal-candidates-smoke-20d-20250102-20250207.rows.csv]]
- Portfolio mode: `long_only`
- Target mode: `paper_portfolio_target_smoke_only`
- Max positions: `20`
- Max position weight: `5.00%`
- Target gross exposure: `100.00%`
- KIS API call: `false`
- KRX API call: `false`
- Order intent generated: `false`
- Backtest readiness: `hold`
- Live trading readiness: `blocked`
- Machine-readable rows: [[_report/quant/research/2026-07-05-signal-portfolio-targets-smoke-20d-20250102-20250207.rows.csv|_report/quant/research/2026-07-05-signal-portfolio-targets-smoke-20d-20250102-20250207.rows.csv]]

## Summary

| Metric | Value |
| --- | ---: |
| Target rows | 60 |
| Target dates | 3 |
| Avg positions per date | 20.00 |
| Avg gross target weight | 1.0000 |
| Avg cash reserve weight | 0.0000 |
| Max turnover weight change | 1.0000 |

## Side Counts

| Side | Count |
| --- | ---: |
| `LONG` | 60 |

## Date Diagnostics

| Date | Selected positions | Gross target weight | Cash reserve weight | Turnover weight change |
| --- | ---: | ---: | ---: | ---: |
| 2025-02-05 | 20 | 1.000000 | 0.000000 | 1.000000 |
| 2025-02-06 | 20 | 1.000000 | 0.000000 | 0.700000 |
| 2025-02-07 | 20 | 1.000000 | 0.000000 | 0.500000 |

## Latest Target Sample

| Date | Rank | Side | Code | Company | Weight | Source ROC % |
| --- | ---: | --- | --- | --- | ---: | ---: |
| 2025-02-07 | 1 | LONG | `010100` | 한국무브넥스 | 0.050000 | 135.4391 |
| 2025-02-07 | 2 | LONG | `160190` | 하이젠알앤엠 | 0.050000 | 127.3499 |
| 2025-02-07 | 3 | LONG | `161580` | 필옵틱스 | 0.050000 | 112.9496 |
| 2025-02-07 | 4 | LONG | `098460` | 고영 | 0.050000 | 100.8869 |
| 2025-02-07 | 5 | LONG | `351320` | 에스에이티이엔지 | 0.050000 | 89.2911 |
| 2025-02-07 | 6 | LONG | `112290` | 와이씨켐 | 0.050000 | 88.1051 |
| 2025-02-07 | 7 | LONG | `171010` | 램테크놀러지 | 0.050000 | 80.7692 |
| 2025-02-07 | 8 | LONG | `277810` | 레인보우로보틱스 | 0.050000 | 76.1803 |
| 2025-02-07 | 9 | LONG | `168360` | 펨트론 | 0.050000 | 74.1573 |
| 2025-02-07 | 10 | LONG | `332570` | 와이팜 | 0.050000 | 68.6380 |
| 2025-02-07 | 11 | LONG | `080220` | 제주반도체 | 0.050000 | 68.6176 |
| 2025-02-07 | 12 | LONG | `466100` | 클로봇 | 0.050000 | 66.0870 |
| 2025-02-07 | 13 | LONG | `219550` | 디와이디 | 0.050000 | 64.1818 |
| 2025-02-07 | 14 | LONG | `042660` | 한화오션 | 0.050000 | 62.4672 |
| 2025-02-07 | 15 | LONG | `115310` | 인포바인 | 0.050000 | 55.7971 |
| 2025-02-07 | 16 | LONG | `119850` | 지엔씨에너지 | 0.050000 | 54.2022 |
| 2025-02-07 | 17 | LONG | `301300` | 바이브컴퍼니 | 0.050000 | 53.4442 |
| 2025-02-07 | 18 | LONG | `042000` | 카페24 | 0.050000 | 52.6738 |
| 2025-02-07 | 19 | LONG | `064350` | 현대로템 | 0.050000 | 52.1989 |
| 2025-02-07 | 20 | LONG | `089010` | 켐트로닉스 | 0.050000 | 52.1610 |

## Guardrails

- These rows are target-weight diagnostics only, not order instructions.
- `SELL candidate` rows are excluded in `long_only` mode; they are not short targets.
- This does not include transaction costs, slippage, taxes, cash drag modeling, or benchmark comparison.
- Keep `Backtest readiness` at `hold` until full Point-in-Time status coverage, costs, benchmark, OOS, and Bias Control pass.
