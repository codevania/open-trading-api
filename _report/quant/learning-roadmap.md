# 퀀트 초보자 학습 로드맵

## 목적

퀀트를 처음 배우는 상태에서 "Strategy를 문서화하고, 데이터를 확인하고, 편향을 통제한 Backtest를 해석할 수 있는 수준"까지 가기 위한 학습 계획이다. 목표는 빠르게 자동매매를 붙이는 것이 아니라, 좋은 질문과 나쁜 Backtest를 구분하는 능력을 먼저 만드는 것이다.

## 전제

- Main/Game/관심종목은 재량 리서치용이다. 퀀트 학습에서는 Strategy 규칙과 Investable Universe를 먼저 본다.
- 처음 12주는 실전 주문, 자동매매, 레버리지, 선물/옵션을 다루지 않는다.
- AI는 코드와 요약을 도울 수 있지만, 투자 가설과 검증 판정은 사람이 확인한다.
- 매주 산출물을 남긴다. 읽기만 하고 끝내지 않는다.

## 12주 목표

12주 뒤에는 다음을 할 수 있어야 한다.

- Return, Volatility, MDD, Transaction Cost, Slippage를 설명한다.
- pandas로 OHLCV 데이터를 읽고 Return, 이동평균, ROC 같은 기본 피처를 만든다.
- Strategy Spec서를 작성하고, Universe와 Inclusion/Exclusion Rules을 분리한다.
- Survivorship Bias, Lookahead Bias, Data Snooping, Overfitting을 체크리스트로 판정한다.
- Backtest 결과를 "좋다/나쁘다"가 아니라 "어떤 조건에서 성립했고 어디서 깨지는지"로 해석한다.
- 일일 리포트에는 검증 전 Strategy를 매매 Signal이 아니라 "퀀트 Signal Candidate"로만 기록한다.

## 학습 단계

| 주차 | 주제 | 익힐 것 | 산출물 |
| --- | --- | --- | --- |
| 1 | 퀀트 사고방식 | 종목 선택과 Strategy 검증의 차이, Alpha, Benchmark, Risk | [[_report/quant/templates/study-log|_report/quant/templates/study-log.md]]로 첫 학습 로그 |
| 2 | 시장 데이터 기초 | OHLCV, 수정주가, 거래대금, 거래정지, 상장/상폐 | 데이터 품질 체크 메모 |
| 3 | Python 기초 | 변수, 리스트/딕셔너리, 함수, 파일 읽기 | 작은 CSV를 읽고 행 수/컬럼 출력 |
| 4 | pandas/NumPy 기초 | DataFrame, 날짜 인덱스, 결측 처리, pct_change, rolling | 종가 Return과 이동평균 계산 노트 |
| 5 | Return과 Risk | 단순/누적 Return, Volatility, MDD, 승률, turnover | Return 지표 정의표 |
| 6 | Universe 설계 | rule-based universe, point-in-time, Liquidity Filter | `KRX 보통주 + Liquidity Filter` 초안 |
| 7 | Strategy Spec | 가설, 진입, 청산, 무효화 조건, 실패 시장 | `001-strategy-universe-momentum` 보완 |
| 8 | Backtest 구조 | Signal 계산 시점, 체결 시점, 수수료, Slippage | Backtest 실행 전 점검표 |
| 9 | Bias Control | Survivorship Bias, Lookahead Bias, Data Snooping, Overfitting | Bias Control 체크리스트 작성 |
| 10 | 결과 해석 | Benchmark, 구간별 성과, stress period, out-of-sample | Backtest 결과 템플릿 초안 |
| 11 | Strategy 다각화 | 모멘텀과 다른 실패 조건의 Strategy 찾기 | 두 번째 Strategy 후보 1개 명세 |
| 12 | Signal 추적 | paper signal, 일일 리포트 연결, decision-log 조건 | 일일 리포트 반영 규칙 초안 |

## 매주 반복 루틴

1. 한 주에 한 개 주제만 다룬다.
2. 학습 시작 전에 "이번 주에 설명할 수 있어야 하는 문장"을 한 줄로 쓴다.
3. 공식 문서나 기존 repo 문서를 30분 읽는다.
4. 작은 실습을 30분 한다.
5. [[_report/quant/templates/study-log|_report/quant/templates/study-log.md]]를 복사해 학습 로그를 남긴다.
6. 모르는 용어는 "모르는 것" 섹션에 남기고, 추정으로 채우지 않는다.
7. 매주 산출물이 Strategy Spec, Universe 원칙, Backtest 템플릿 중 어디에 연결되는지 적는다.

## 먼저 익힐 핵심 개념

- Universe: Strategy가 투자할 수 있다고 사전에 정한 후보 집합.
- Signal: 매수/매도 후보를 만들기 위한 정량 조건.
- Position: 실제 자금이 들어간 상태와 크기.
- Benchmark: Strategy가 이겨야 하는 비교 대상.
- MDD: 고점 대비 최대 하락폭.
- Transaction Cost: 수수료, 세금, Slippage, 호가 공백.
- Survivorship Bias: 살아남은 종목만 보고 과거 성과를 좋게 착각하는 문제.
- Lookahead Bias: 당시에는 몰랐던 미래 정보를 과거 시점에 사용한 문제.
- Data Snooping: 여러 조건을 반복 실험한 뒤 우연히 좋은 결과만 고르는 문제.
- Overfitting: 과거 데이터에만 너무 잘 맞아 미래에서 깨지는 문제.
- out-of-sample: Strategy를 만들 때 보지 않은 기간이나 시장에서 검증하는 것.

## 금지할 지름길

- "AI가 추천한 종목"을 퀀트 Strategy로 취급하지 않는다.
- Main/Game 관심종목 몇 개로 좋은 결과가 나왔다고 Strategy Alpha로 주장하지 않는다.
- 파라미터를 계속 바꿔 가장 좋은 Return만 남기지 않는다.
- 수수료, 세금, Slippage 없는 Backtest를 실전 기대수익으로 읽지 않는다.
- Backtest 통과 전에는 주문 API나 자동매매 연결을 논의하지 않는다.

## 추천 학습 자료

무료 공식 문서 위주로 시작한다.

- [Python Tutorial](https://docs.python.org/3/tutorial/): Python 문법과 자료구조 기초.
- [pandas Getting started](https://pandas.pydata.org/docs/dev/getting_started/index.html): 표 형태 데이터와 시계열 처리를 익히기 위한 시작점.
- [NumPy quickstart](https://numpy.org/doc/stable/user/quickstart.html): 배열 연산과 기본 수치 계산.
- [QuantConnect Research Guide](https://www.quantconnect.com/docs/v2/writing-algorithms/key-concepts/research-guide): Survivorship Bias, Lookahead Bias 같은 리서치 함정 확인.
- [QuantConnect Backtesting Getting Started](https://www.quantconnect.com/docs/v2/our-platform/backtesting/getting-started): Backtest가 무엇을 검증하고 무엇을 보장하지 않는지 확인.

## 현재 repo에서 바로 할 첫 과제

1. 이 문서를 읽고 모르는 용어 10개를 `study-log`에 적는다.
2. [[_report/quant/universe|_report/quant/universe.md]]의 "허용 가능한 Quant Universe 정의 방식"을 다시 읽는다.
3. `001-strategy-universe-momentum`의 Economic/Financial Hypothesis을 자신의 말로 3문장으로 바꿔 쓴다.
4. `KRX 보통주 + 최소 상장기간 + 최소 거래대금` Universe 초안을 작성한다.
5. 아직 Backtest를 돌리지 않는다. 먼저 Universe와 Bias Control 조건을 확정한다.
