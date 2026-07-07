# Signal Portfolio Targets Smoke

- Signal input: [[_report/quant/research/2026-07-06-kind-status-point-in-time-momentum-signal-candidates-smoke-20d-20250102-20250221.rows.csv|_report/quant/research/2026-07-06-kind-status-point-in-time-momentum-signal-candidates-smoke-20d-20250102-20250221.rows.csv]]
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
- Machine-readable rows: [[_report/quant/research/2026-07-06-signal-portfolio-targets-smoke-20d-20250102-20250221.rows.csv|_report/quant/research/2026-07-06-signal-portfolio-targets-smoke-20d-20250102-20250221.rows.csv]]

## Summary

| Metric | Value |
| --- | ---: |
| Target rows | 260 |
| Target dates | 13 |
| Avg positions per date | 20.00 |
| Avg gross target weight | 1.0000 |
| Avg cash reserve weight | 0.0000 |
| Max turnover weight change | 1.0000 |

## Side Counts

| Side | Count |
| --- | ---: |
| `LONG` | 260 |

## Date Diagnostics

| Date | Selected positions | Gross target weight | Cash reserve weight | Turnover weight change |
| --- | ---: | ---: | ---: | ---: |
| 2025-02-05 | 20 | 1.000000 | 0.000000 | 1.000000 |
| 2025-02-06 | 20 | 1.000000 | 0.000000 | 0.700000 |
| 2025-02-07 | 20 | 1.000000 | 0.000000 | 0.500000 |
| 2025-02-10 | 20 | 1.000000 | 0.000000 | 0.700000 |
| 2025-02-11 | 20 | 1.000000 | 0.000000 | 0.700000 |
| 2025-02-12 | 20 | 1.000000 | 0.000000 | 0.600000 |
| 2025-02-13 | 20 | 1.000000 | 0.000000 | 0.600000 |
| 2025-02-14 | 20 | 1.000000 | 0.000000 | 0.500000 |
| 2025-02-17 | 20 | 1.000000 | 0.000000 | 0.400000 |
| 2025-02-18 | 20 | 1.000000 | 0.000000 | 0.700000 |
| 2025-02-19 | 20 | 1.000000 | 0.000000 | 0.700000 |
| 2025-02-20 | 20 | 1.000000 | 0.000000 | 0.500000 |
| 2025-02-21 | 20 | 1.000000 | 0.000000 | 0.500000 |

## Latest Target Sample

| Date | Rank | Side | Code | Company | Weight | Source ROC % |
| --- | ---: | --- | --- | --- | ---: | ---: |
| 2025-02-21 | 1 | LONG | `226950` | 올릭스 | 0.050000 | 206.4631 |
| 2025-02-21 | 2 | LONG | `388720` | 유일로보틱스 | 0.050000 | 110.9792 |
| 2025-02-21 | 3 | LONG | `105550` | 엣지파운드리 | 0.050000 | 104.3478 |
| 2025-02-21 | 4 | LONG | `010770` | 평화홀딩스 | 0.050000 | 93.9279 |
| 2025-02-21 | 5 | LONG | `340930` | 유일에너테크 | 0.050000 | 91.6124 |
| 2025-02-21 | 6 | LONG | `382150` | 온코크로스 | 0.050000 | 88.1406 |
| 2025-02-21 | 7 | LONG | `065170` | 비엘팜텍 | 0.050000 | 86.5672 |
| 2025-02-21 | 8 | LONG | `377030` | 맥스트 | 0.050000 | 84.5192 |
| 2025-02-21 | 9 | LONG | `347700` | 라이프시맨틱스 | 0.050000 | 79.2115 |
| 2025-02-21 | 10 | LONG | `082270` | 젬백스 | 0.050000 | 78.7679 |
| 2025-02-21 | 11 | LONG | `012450` | 한화에어로스페이스 | 0.050000 | 74.8344 |
| 2025-02-21 | 12 | LONG | `241520` | DSC인베스트먼트 | 0.050000 | 73.9895 |
| 2025-02-21 | 13 | LONG | `113810` | 디젠스 | 0.050000 | 73.3021 |
| 2025-02-21 | 14 | LONG | `119850` | 지엔씨에너지 | 0.050000 | 71.9043 |
| 2025-02-21 | 15 | LONG | `351320` | 에스에이티이엔지 | 0.050000 | 67.8322 |
| 2025-02-21 | 16 | LONG | `090710` | 휴림로봇 | 0.050000 | 67.3755 |
| 2025-02-21 | 17 | LONG | `419530` | SAMG엔터 | 0.050000 | 67.2378 |
| 2025-02-21 | 18 | LONG | `331520` | 밸로프 | 0.050000 | 65.1050 |
| 2025-02-21 | 19 | LONG | `172670` | 에이엘티 | 0.050000 | 64.4737 |
| 2025-02-21 | 20 | LONG | `038390` | 레드캡투어 | 0.050000 | 63.7931 |

## Guardrails

- These rows are target-weight diagnostics only, not order instructions.
- `SELL candidate` rows are excluded in `long_only` mode; they are not short targets.
- This does not include transaction costs, slippage, taxes, cash drag modeling, or benchmark comparison.
- Keep `Backtest readiness` at `hold` until full Point-in-Time status coverage, costs, benchmark, OOS, and Bias Control pass.
