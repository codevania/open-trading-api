# Market Regime Scan - 2026-06-07

## 메타데이터

- 날짜: 2026-06-07
- 기준 시장: Mixed
- 기준 세션: US close 2026-06-05, KRX close 2026-06-05
- 작성 시각: 2026-06-07 KST
- 작성자: Codex
- 데이터 출처:
  - Cboe VIX: https://www.cboe.com/tradable-products/vix/
  - Yahoo Finance VIX: https://finance.yahoo.com/quote/%5EVIX/
  - Investing.com S&P 500 historical data: https://au.investing.com/indices/us-spx-500-historical-data
  - Investing.com Nasdaq Composite historical data: https://ca.investing.com/indices/nasdaq-composite-historical-data
  - Reuters via Investing.com market recap: https://www.investing.com/news/stock-market-news/hot-jobs-report-rising-rates-send-wall-streets-tech-favorites-sprawling-4729227
  - Aju Press KOSPI close note: https://m.ajupress.com/amp/20260605154242883
  - Bloomingbit KOSPI/USD-KRW close note: https://en.bloomingbit.io/feed/news/113608
- 원천 데이터 저장 위치: 미저장
- Perplexity/Chrome 사용 여부: 사용 안 함

## 사용 원칙

- 이 문서는 Strategy 실행 환경을 설명하는 보조 자료다.
- Market Regime은 Strategy의 Entry/Exit Signal을 직접 만들지 않는다.
- 이번 스캔은 공개 웹 검색 기반이며, API 원천 JSON을 저장하지 않았으므로 Backtest Source가 아니다.
- KRX 수치는 기사별 차이가 있어 KIS 또는 KRX 원천 확인 전까지 `medium` 이하 Confidence로만 사용한다.

## 1. Regime Summary

- Regime: risk-off
- Confidence: medium
- 한 줄 요약: 미국 기술주와 반도체 중심 급락, VIX 급등, KRX 반도체/기술주 동반 약세가 겹친 risk-off 세션이다.
- 오늘 Strategy 실행에 주는 영향: `001-strategy-universe-momentum`의 BUY 후보는 실제 행동 후보가 아니라 `Signal Candidate`로만 추적한다.
- 가장 중요한 불확실성: Sector Breadth와 KRX 공식 종가/수급 원천을 아직 교차 검증하지 못했다.

## 2. Core Market Data

| Category | Metric | 값 | 변화 | 출처 | 해석 |
| --- | --- | ---: | ---: | --- | --- |
| Index/Futures | S&P 500 | 7,383.74 | -2.64% | Investing.com historical data | 대형주 전반 약세 |
| Index/Futures | Nasdaq Composite | 25,709.43 | -4.18% | Investing.com historical data | Growth/Tech 중심 매도 |
| Volatility | VIX | 21.51 | +39.68% | Cboe, Yahoo Finance | 변동성 급등, risk-off 확인 |
| Index | KOSPI | 8,160.59 | -5.54% | Aju Press, Bloomingbit | 한국 기술주 동반 급락. 기사별 수치 차이 있어 공식 확인 필요 |
| Rates/FX | USD/KRW | 1,539.1 | +9.4 KRW | Bloomingbit | 원화 약세, 외국인 매도 압력 확인 필요 |
| Breadth | Sector Breadth | 미수집 | - | - | Heatmap/상승하락 종목 수 미확인 |
| Leadership | 주도 섹터/테마 | 기술주 약세 | - | Reuters recap | 반도체/AI 쏠림 조정 가능성 |

## 3. Breadth & Leadership

- 상승 우위 섹터: 미수집
- 하락 우위 섹터: Technology, Semiconductor 중심 약세로 추정
- 대형주 쏠림 여부: Nvidia와 AI chip maker 약세가 시장 하락을 키운 것으로 보이나, 공식 sector breadth는 미확인
- 방어주/경기민감주 흐름: 미수집
- Top Gainers/Losers에서 확인할 점: 하락이 mega-cap growth에 집중됐는지, 시장 전체로 확산됐는지 구분 필요
- Heatmap 또는 Sector Map 해석: 미수집. Perplexity 화면과 유사한 heatmap은 보조로만 사용 가능

## 4. News/Event Filter

| Event | 출처 | 시장 영향 | 관련 Strategy | 확인 필요 |
| --- | --- | --- | --- | --- |
| 미국 고용지표 강세와 금리 우려 | Reuters via Investing.com | 성장주 valuation 압박 | Momentum, Growth exposure | 금리/채권 데이터 확인 |
| Semiconductor/AI chip selloff | Reuters via Investing.com | Nasdaq와 KRX 기술주 동반 약세 | Momentum | 개별 종목보다 sector shock로 분리 |
| KOSPI 급락 및 원화 약세 | Aju Press, Bloomingbit | KRX risk-off | KRX Universe Strategy | KIS/KRX 공식 종가 및 수급 확인 |

- Macro Event: 고용지표 강세에 따른 hawkish Fed 우려
- Earnings/Event: Broadcom/AI chip 관련 매도 압력
- Policy/Regulation: 미수집
- Geopolitical/Supply Shock: 미수집
- Crypto 또는 대체자산 충격: 미수집

## 5. Risk Filter

- VIX 급등 여부: 예. 21.51, +39.68%
- Index/Futures 동반 급락 여부: 예. S&P 500 -2.64%, Nasdaq Composite -4.18%
- 특정 섹터 집중 하락 여부: 기술주/반도체 중심으로 추정
- USD/KRW 또는 금리 충격 여부: USD/KRW 상승 확인. 금리 수치 미수집
- 거래량 급증을 동반한 매도 압력 여부: Nasdaq 거래량 데이터는 확인됐으나 해석용 비교 미수집
- Risk 판정: defensive

## 6. Strategy Impact

| Strategy | Signal 상태 | Regime 영향 | 필요한 행동 | 무효화 조건 |
| --- | --- | --- | --- | --- |
| `001-strategy-universe-momentum` | Signal Candidate only | Risk-off에서 Momentum False Positive 가능성 증가 | 신규 BUY 행동 후보로 승격하지 않고 Paper 추적 | VIX 안정, breadth 회복, KRX 공식 데이터 확인 전까지 보류 |

- Regime이 Strategy를 보류시키는가: 예. 신규 행동 후보는 보류하고 Signal Candidate 추적만 한다.
- Position 크기 또는 현금 비중 검토가 필요한가: 예. 실제 Position 문서가 없으므로 투자 행동은 분리한다.
- Backtest에서 별도 Stress Period로 표시할 이벤트인가: 예. `2026-06-05 tech/chip selloff`로 표시 후보.
- 다음 일일 리포트에 반영할 문장: `Market Regime은 risk-off로 판정한다. VIX 급등과 미국/한국 기술주 동반 약세가 확인되어 Quant BUY 후보는 Signal Candidate로만 추적한다.`

## 7. Data Quality

- 최신성: 마지막 닫힌 세션 기준. 2026-06-07은 주말이므로 장중 데이터가 아니다.
- 출처 신뢰도: VIX는 Cboe/Yahoo로 교차 확인. S&P 500/Nasdaq은 Investing.com historical data 사용. KRX는 기사 기반이라 공식 확인 필요.
- 교차 검증 여부: VIX와 미국 지수는 2개 이상 출처로 대략 일치. KOSPI는 기사별 수치 차이 존재.
- 누락 데이터: Sector Breadth, KRX 상승/하락 종목 수, 투자자 수급, 금리 수치, Futures 실시간값.
- 로그인/유료 데이터 의존 여부: 없음.
- 사람이 직접 재확인해야 할 항목: KRX 공식 종가, 외국인/기관 수급, KOSDAQ, sector breadth.

## 8. Next Checks

1. KIS/KRX 원천으로 2026-06-05 KOSPI/KOSDAQ 및 주요 반도체 종목 종가를 확인한다.
2. 가능하면 VIX, S&P 500, Nasdaq 값을 API/공식 소스로 저장하는 방법을 정한다.
3. `001-strategy-universe-momentum` Backtest에서 2026-06-05를 Stress Period 후보로 표시한다.
