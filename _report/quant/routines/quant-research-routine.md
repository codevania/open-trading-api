# 퀀트 Strategy 준비 및 검증 루틴

## 목적

Strategy 아이디어를 바로 주문으로 연결하지 않고, 문서화된 Strategy Spec과 Backtest 결과를 거쳐 DI 일일 리포트 Signal로 추적하기 위한 절차다. `_report/di/watchlist.yaml`의 Main, Game, 관심종목 그룹은 재량 리서치용이며 Quant Universe로 사용하지 않는다. 퀀트는 종목을 고르는 작업이 아니라 Strategy와 Investable Universe 규칙을 검증하는 작업이다.

## 입력

- Universe 원칙: `_report/quant/universe.md`
- Strategy별 Universe 규칙: `_report/quant/strategies/*.md`
- Strategy Spec: `_report/quant/strategies/*.md`
- Strategy YAML: `_report/quant/strategies/*.kis.yaml`
- 결과 템플릿: `_report/quant/templates/backtest-report.md`
- Bias Control 체크리스트: `_report/quant/templates/bias-control-checklist.md`
- Market Regime Scan 템플릿: `_report/quant/templates/market-regime-scan.md`
- 원천 데이터 저장소: `_report/raw/YYYY/YYYY-MM-DD/`

## 절차

### 0. Market Regime Scan 확인

1. Strategy Signal을 DI 일일 리포트에 연결하기 전 `_report/quant/routines/market-regime-scan-routine.md`로 시장 환경을 확인한다.
2. Market Regime은 Entry/Exit Signal을 만들지 않고, Strategy 실행 환경과 Risk Filter만 설명한다.
3. `risk-off` 또는 `high-volatility` 판정이면 BUY 후보를 매매 Signal로 승격하지 않고 `Signal Candidate`로만 둔다.
4. Perplexity Finance, 뉴스 요약, 예측시장은 Idea Source 또는 Event Filter로만 쓰고 수치 판단은 교차 검증한다.
5. 최신성이나 출처가 불충분하면 Regime을 `data-insufficient`로 둔다.

### 1. Universe 확인

1. `_report/quant/universe.md`를 먼저 읽는다.
2. 대상 Strategy 문서에 Inclusion/Exclusion Rules이 있는지 확인한다.
3. Main/Game/관심종목 그룹을 기본 Universe로 쓰고 있으면 Backtest를 중단한다.
4. Manual Watchlist를 사용해야 하는 경우에는 "Data Pipeline Smoke Test"로만 표시한다.
5. 종목 코드, 시장, 해외 종목의 `exchange_code`는 실제 데이터 조회 전 검증하되, Strategy Universe를 종목명으로 정의하지 않는다.

### 2. Strategy Spec 확인

1. `_report/quant/strategies/`에서 대상 Strategy 문서를 읽는다.
2. 진입, 청산, 손절, 무효화 조건이 빠져 있으면 Backtest 전에 보완한다.
3. `.kis.yaml`이 있는 경우 YAML 파싱을 먼저 확인한다.
4. Economic/Financial Hypothesis, Strategy Portfolio 내 역할, AI 사용 범위가 비어 있으면 성과 검증 전에 보완한다.
5. 단일 Strategy를 분산된 Strategy Portfolio처럼 해석하지 않는다.

### 3. 데이터 확인

1. KIS MCP 데이터를 호출해야 하면 먼저 `find_api_detail`로 API 파라미터를 확인한다.
2. 일봉 OHLCV, 거래량, 필요한 보조 지표 데이터를 확보한다.
3. 원천 응답을 `_report/raw/YYYY/YYYY-MM-DD/SYMBOL/` 아래에 저장한다.
4. `ConvertFrom-Json` 또는 YAML/JSON 파서로 원천 파일이 파싱되는지 확인한다.
5. 현재 관심종목을 과거에 소급 적용하는 실험이면 퀀트 성과 검증이 아니라 smoke test로 제한한다.
6. 공개 데이터만으로 검증 가능한 가설인지, 비공개/유료 데이터가 필요한 가설인지 구분한다.

### 4. Backtest 실행

1. `_report/quant/templates/bias-control-checklist.md`를 기준으로 Bias Control 항목을 먼저 검토한다.
2. 현재 watchlist만 사용한 실행은 생존/선택 편향이 있으므로 성과 증거가 아니라 smoke test로 표시한다.
3. Backtester preset 또는 `.kis.yaml` import 흐름을 사용한다.
4. 시장별로 Benchmark를 분리한다.
5. Total Return, CAGR, MDD, Sharpe, 승률, 거래 횟수, Turnover를 기록한다.
6. Docker, Lean, 의존성, 데이터 부족으로 실행하지 못하면 이유를 결과 문서에 남긴다.
7. 파라미터 반복 비교는 최적값 찾기가 아니라 민감도와 실패 조건으로 기록한다.
8. in-sample과 out-of-sample을 분리하지 못하면 최종 판정은 `hold` 이하로 둔다.

### 5. 결과 기록

1. `_report/quant/templates/backtest-report.md`를 기준으로 결과 문서를 작성한다.
2. Bias Control 체크리스트의 최종 판정을 결과 문서에 연결한다.
3. 차트가 있으면 자산 곡선과 drawdown을 우선 첨부한다.
4. 결과가 좋아도 데이터 품질, 특정 구간 의존성, 거래 횟수 부족을 같이 검토한다.
5. 가장 좋은 파라미터만 골라 Strategy 성과로 주장하지 않고, 민감도와 실패 조건을 함께 기록한다.
6. Position 크기, 현금 비중, 전체 자산 내 비중은 Strategy 성과와 별도 항목으로 기록한다.
7. AI가 생성한 코드나 요약은 사람이 검토한 가설과 데이터 근거를 대체하지 않는다.

### 6. 일일 리포트 반영

1. 검증 전에는 "매매 Signal"이 아니라 "퀀트 Signal Candidate"로만 쓴다.
2. Signal 발생 시 근거 데이터와 무효화 조건을 함께 적는다.
3. 실제 판단 변경이 있을 때만 `_report/di/decisions/decision-log.md`에 누적한다.

## 중지 조건

- 종목 코드가 불명확하다.
- Universe가 Strategy 규칙이 아니라 Main/Game/관심종목 목록으로 정의되어 있다.
- 데이터가 Strategy lookback보다 짧다.
- 원천 응답이 비정상이다.
- Survivorship Bias, Lookahead Bias, Data Snooping, Overfitting 위험을 판정할 수 없다.
- Economic/Financial Hypothesis이나 Strategy 다각화 역할이 비어 있다.
- 단일 Strategy 결과를 포트폴리오 Alpha로 주장해야만 성립한다.
- 주문 API 호출이 필요하다.
- Backtest 환경이 준비되지 않았다.

중지 조건이 발생하면 추정으로 메우지 말고, 제한 사항과 다음 확인 항목을 문서에 남긴다.
