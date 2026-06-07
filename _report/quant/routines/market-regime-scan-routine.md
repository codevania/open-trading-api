# Market Regime Scan 루틴

## 목적

스냅샷 없이도 시장 환경을 재현 가능한 데이터로 수집하고, Quant Strategy 실행 환경을 `Risk-on`, `Neutral`, `Risk-off`, `High-volatility`, `Event-driven`, `Data-insufficient` 중 하나로 정리한다.

이 루틴은 종목 추천, Strategy Entry/Exit Signal, 주문 판단을 만들지 않는다. 일일 리포트와 Quant Research에서 Strategy Signal Candidate의 배경과 Risk Filter를 설명하기 위한 보조 루틴이다.

## 입력

- 템플릿: `_report/quant/templates/market-regime-scan.md`
- Quant 원칙: `_report/quant/README.md`
- Universe 원칙: `_report/quant/universe.md`
- 대상 Strategy: `_report/quant/strategies/*.md`
- DI 일일 리포트 템플릿: `_report/di/templates/daily-report.md`
- 원천 데이터 저장소: `_report/raw/YYYY/YYYY-MM-DD/market-regime/`

## 사용 가능한 데이터 소스

1. Broker/API 데이터
   - KIS MCP 국내/해외 주식 API
   - KIS MCP를 호출할 때는 반드시 먼저 `find_api_detail`로 파라미터를 확인한다.
2. 공개 금융 데이터
   - 지수, Futures, VIX, 금리, 환율, 섹터 ETF, Gainers/Losers, 주요 뉴스.
   - 최신성에 민감하므로 작성 시각과 출처를 함께 적는다.
3. Perplexity Finance 또는 유사 화면
   - Codex Chrome extension 또는 Computer Use로 로그인 화면을 확인할 수 있을 때만 사용한다.
   - Perplexity 요약은 Idea Source 또는 News/Event Filter로만 사용하고, 수치 판단은 별도 데이터로 교차 확인한다.
4. 스크린샷
   - 사용자가 제공한 경우에만 보조 증거로 해석한다.
   - 스크린샷은 자동 수집 루틴의 필수 입력이 아니다.

## 수집 항목

### US Market

- S&P 500, Nasdaq, Dow 또는 주요 Futures
- VIX
- 미국 10년물 금리
- Dollar Index 또는 주요 환율
- Sector Breadth 또는 주요 섹터 ETF 흐름
- Mega-cap Leadership: NVDA, AAPL, MSFT, GOOGL, META, TSLA 등
- Top Gainers/Losers
- 주요 Macro/Event Headline

### KRX Market

- KOSPI, KOSDAQ
- USD/KRW
- 시장 거래대금
- 상승/하락 종목 수 또는 업종 흐름
- 외국인/기관 시장 수급이 필요하면 KIS MCP 문서 확인 후 조회한다.
- 기존 Main/Game/관심종목 그룹은 Quant Universe가 아니라 재량 관찰 context로만 본다.

### Cross-Asset

- Crypto 급락/급등이 Risk Sentiment에 영향을 주는지 확인한다.
- Crude Oil, Gold, Rates, FX 중 당일 Event와 연결되는 항목만 기록한다.
- 관련성이 낮으면 수집하지 않고 `미수집`으로 남긴다.

## 판정 규칙

### Risk-on

- 주요 Index/Futures가 상승 또는 안정적이다.
- VIX가 낮거나 하락한다.
- 상승 섹터가 넓고 특정 Mega-cap만으로 지수가 버티는 흐름이 아니다.
- Momentum Strategy의 Signal Candidate 추적에 우호적이다.

### Neutral

- Index/Futures, VIX, Breadth가 혼재되어 있다.
- Event는 있지만 시장 방향이 명확하지 않다.
- Strategy Signal은 기록하되 Confidence를 과장하지 않는다.

### Risk-off

- 주요 Index/Futures가 동반 하락한다.
- VIX가 급등하거나 높은 수준을 유지한다.
- Heatmap 또는 Breadth가 광범위하게 악화된다.
- Momentum BUY 후보는 `Signal Candidate`로만 기록하고 실제 행동 후보는 보수적으로 쓴다.

### High-volatility

- VIX 급등, 급락장, 대형 이벤트, 거래량 급증이 동반된다.
- Backtest에서 별도 Stress Period로 표시할 수 있는지 검토한다.
- 단기 Signal의 False Positive 가능성을 높게 본다.

### Event-driven

- 시장 전체보다 특정 Macro, Earnings, Policy, Geopolitical, Supply Shock가 설명력을 가진다.
- Strategy 일반 규칙보다 Event Filter가 더 중요할 수 있음을 메모한다.

### Data-insufficient

- 출처가 불명확하거나 최신성을 확인할 수 없다.
- 로그인/유료 화면 요약만 있고 원천 수치가 없다.
- 필요한 지표가 충돌하고 교차 검증이 안 된다.

## 작성 절차

1. 기준일, 기준 세션, 대상 시장을 확정한다.
2. `_report/quant/templates/market-regime-scan.md`를 복사해 `_report/quant/research/YYYY-MM-DD-market-regime-scan.md` 형식으로 작성한다.
3. 수집 가능한 공개 데이터와 Broker/API 데이터를 먼저 확인한다.
4. KIS MCP를 쓸 때는 해당 API의 `find_api_detail`을 먼저 호출한다.
5. Perplexity Finance는 로그인 화면 확인이 가능할 때만 보조 요약으로 사용한다.
6. `Core Market Data`, `Breadth & Leadership`, `News/Event Filter`, `Risk Filter`를 채운다.
7. 최종 Regime과 Confidence를 판정한다.
8. 대상 Strategy별로 `Strategy Impact`를 작성한다.
9. 일일 리포트의 `시장 배경`에는 한 줄 요약과 핵심 근거만 옮긴다.
10. Quant Strategy 문서나 Backtest 결과를 수정해야 하는 경우 별도 작업으로 분리한다.

## 일일 리포트 반영 형식

```text
Market Regime: risk-off / Confidence: medium
근거: Nasdaq Futures 급락, VIX 급등, 기술주 Heatmap 약세
Strategy 영향: 001-strategy-universe-momentum BUY 후보는 Signal Candidate로만 추적, 신규 행동 후보는 보류
누락 데이터: Sector Breadth 원천 미확인
```

## 중지 조건

- 최신성을 확인할 수 없는 값만 있다.
- 로그인 화면 요약만 있고 교차 검증할 수 있는 수치가 없다.
- 주문 판단 또는 종목 추천을 만들라는 요구로 흐름이 바뀐다.
- KIS MCP 파라미터를 확인하지 않은 상태에서 API를 호출해야 한다.
- Market Regime 판정을 Strategy 성과 증거처럼 써야만 결론이 성립한다.

중지 조건이 발생하면 `data-insufficient`로 표시하고, 필요한 다음 확인 항목을 남긴다.
