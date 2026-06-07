# Market Regime Scan 템플릿

## 메타데이터

- 날짜:
- 기준 시장: KRX | US | Crypto | Mixed
- 기준 세션:
- 작성 시각:
- 작성자: Codex
- 데이터 출처:
- 원천 데이터 저장 위치:
- Perplexity/Chrome 사용 여부: 사용 안 함 | 요약 보조 | 로그인 화면 확인

## 사용 원칙

- Market Regime Scan은 Strategy 실행 환경을 설명하는 보조 자료다.
- Market Regime은 Strategy의 Entry/Exit Signal을 직접 만들지 않는다.
- Risk-off 또는 High-volatility 판정은 Position, Confidence, 추적 우선순위를 조정할 수 있지만, Backtest 없이 Strategy 규칙을 바꾸지 않는다.
- Perplexity, 뉴스 요약, 예측시장은 Idea Source 또는 Event Filter로만 사용한다.
- 수치 판단은 가능한 한 공식 거래소, Broker API, 검증 가능한 금융 데이터, 저장된 원천 응답으로 확인한다.
- 스크린샷은 보조 증거일 뿐이며, 스크린샷 없이도 재현 가능한 데이터 소스를 우선한다.

## 1. Regime Summary

- Regime: risk-on | neutral | risk-off | high-volatility | event-driven | data-insufficient
- Confidence: low | medium | high
- 한 줄 요약:
- 오늘 Strategy 실행에 주는 영향:
- 가장 중요한 불확실성:

## 2. Core Market Data

| Category | Metric | 값 | 변화 | 출처 | 해석 |
| --- | --- | ---: | ---: | --- | --- |
| Index/Futures | S&P 500 또는 KOSPI | - | - | - | - |
| Index/Futures | Nasdaq 또는 KOSDAQ | - | - | - | - |
| Volatility | VIX 또는 변동성 proxy | - | - | - | - |
| Rates/FX | 미국 10Y 또는 USD/KRW | - | - | - | - |
| Breadth | Sector Breadth 또는 상승/하락 종목 비율 | - | - | - | - |
| Leadership | 주도 섹터/테마 | - | - | - | - |
| Liquidity | 거래대금/거래량 proxy | - | - | - | - |

## 3. Breadth & Leadership

- 상승 우위 섹터:
- 하락 우위 섹터:
- 대형주 쏠림 여부:
- 방어주/경기민감주 흐름:
- Top Gainers/Losers에서 확인할 점:
- Heatmap 또는 Sector Map 해석:

## 4. News/Event Filter

| Event | 출처 | 시장 영향 | 관련 Strategy | 확인 필요 |
| --- | --- | --- | --- | --- |
| - | - | - | - | - |

- Macro Event:
- Earnings/Event:
- Policy/Regulation:
- Geopolitical/Supply Shock:
- Crypto 또는 대체자산 충격:

## 5. Risk Filter

- VIX 급등 여부:
- Index/Futures 동반 급락 여부:
- 특정 섹터 집중 하락 여부:
- USD/KRW 또는 금리 충격 여부:
- 거래량 급증을 동반한 매도 압력 여부:
- Risk 판정: normal | caution | defensive | data-insufficient

## 6. Strategy Impact

| Strategy | Signal 상태 | Regime 영향 | 필요한 행동 | 무효화 조건 |
| --- | --- | --- | --- | --- |
| `001-strategy-universe-momentum` | Signal Candidate only | - | - | - |

- Regime이 Strategy를 보류시키는가:
- Position 크기 또는 현금 비중 검토가 필요한가:
- Backtest에서 별도 Stress Period로 표시할 이벤트인가:
- 다음 일일 리포트에 반영할 문장:

## 7. Data Quality

- 최신성:
- 출처 신뢰도:
- 교차 검증 여부:
- 누락 데이터:
- 로그인/유료 데이터 의존 여부:
- 사람이 직접 재확인해야 할 항목:

## 8. Next Checks

1.
2.
3.
