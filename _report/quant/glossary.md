# Quant Glossary

## Purpose

Quant 문서에서는 핵심 개념을 영어로 쓴다. 한국어는 설명을 돕기 위해 붙일 수 있지만, 제목과 체크리스트의 기준 용어는 영어를 우선한다.

## Term Rules

- 핵심 용어는 영어로 쓴다.
- 첫 등장 시 필요하면 `Universe: 투자 가능 후보 집합`처럼 한국어 설명을 붙인다.
- 파일명, Strategy ID, YAML key는 영어 또는 snake_case를 사용한다.
- 같은 개념에 여러 번역어를 섞지 않는다.

## Core Terms

| Term | Korean Description |
| --- | --- |
| Quant | 정량 규칙과 데이터로 투자 의사결정을 검증하는 방식 |
| Strategy | 사전에 정의한 투자 규칙과 검증 대상 |
| Universe | Strategy가 투자할 수 있는 후보 집합 |
| Investable Universe | 실제 과거 시점에 투자 가능했던 Universe |
| Point-in-Time Investable Universe | 특정 과거 시점에 실제로 투자 가능했던 종목만 포함한 Universe |
| Point-in-Time | 해당 과거 시점에 알 수 있었던 정보만 사용하는 기준 |
| Inclusion Rule | Universe에 포함하는 조건 |
| Exclusion Rule | Universe에서 제외하는 조건 |
| Liquidity Filter | 거래대금, 거래량, 스프레드 등 체결 가능성을 기준으로 Universe를 제한하는 규칙 |
| Listing Age | 상장 후 경과한 거래일 수 |
| Trading Halt | 거래정지 상태 |
| Delisting | 상장폐지 |
| Managed Issue | 관리종목 |
| Market Alert Issue | 투자주의, 투자경고, 투자위험 등 시장경보 종목 |
| Source Snapshot | 특정 시점에 수집한 원천 데이터 사본 |
| Source Hash | 원천 데이터 변경 여부를 감지하기 위한 해시값 |
| Manual Snapshot | 자동 API가 아니라 사람이 웹 UI에서 내려받아 저장한 Source Snapshot |
| Reproducible Official Snapshot | 공식 원천에서 절차와 파라미터를 재현해 다시 받을 수 있는 Source Snapshot |
| Signal | 매수/매도 후보를 만드는 정량 조건 |
| Position | 실제 자금이 들어간 상태와 크기 |
| Portfolio | 여러 Position 또는 Strategy의 조합 |
| Alpha | Benchmark 대비 초과 성과를 만들 수 있는 유효한 우위 |
| Benchmark | Strategy 성과를 비교할 기준 |
| KRX | Korea Exchange, 한국거래소 또는 KIS 국내시장 구분에서 KRX 시장을 뜻하는 기준 |
| Backtest | 과거 데이터로 Strategy를 모의 검증하는 과정 |
| Lookback | Signal이나 지표 계산에 사용하는 과거 관찰 기간 |
| Paper Signal | 실제 주문 없이 추적하는 Signal |
| Signal Candidate | 검증 전 또는 주문 전 단계에서 추적하는 Signal 후보 |
| Return | 수익률 |
| Volatility | 변동성 |
| Mean Reversion | 평균회귀 |
| Event Filter | 특정 이벤트를 기준으로 Signal을 제한하는 규칙 |
| Drawdown | 고점 대비 하락폭 |
| MDD | Maximum Drawdown, 전체 검증 기간 중 가장 큰 Drawdown |
| Buy-and-Hold | 매수 후 별도 매매 규칙 없이 보유하는 기준 전략 |
| Transaction Cost | 수수료, 세금, 거래세 등 주문 실행 때 발생하는 명시적 비용 |
| Slippage | 기대 체결가와 실제 체결가의 차이에서 생기는 암묵적 비용 |
| Turnover | 매매 회전율 |
| Survivorship Bias | 살아남은 종목만 보고 과거 성과를 과대평가하는 문제 |
| Lookahead Bias | 당시에는 몰랐던 미래 정보를 사용하는 문제 |
| Data Snooping | 반복 실험 뒤 우연히 좋은 결과만 고르는 문제 |
| Overfitting | 과거 데이터에만 지나치게 맞춘 문제 |
| Out-of-Sample | Strategy 설계에 쓰지 않은 기간 또는 시장 |
| Stress Period | 급락, 정책 충격, 테마 붕괴 같은 시험 구간 |
| Domain Hypothesis | 경제, 금융, 산업, 투자자 행동에 기반한 가설 |
| Domain Knowledge | Strategy 아이디어를 판단하기 위한 금융, 경제, 산업 지식 |
| Risk | 손실 가능성과 손실 규모를 다루는 조건 |
| Market Neutral | 시장 방향 노출을 낮추는 Portfolio 구성 방식 |
| Long-Short | Long Position과 Short Position을 함께 쓰는 방식 |
| Smoke Test | Strategy 성과 검증이 아니라 데이터 흐름 확인용 실행 |

## Detailed Term Notes

### KRX

KRX는 Korea Exchange, 즉 한국거래소를 뜻한다. 이 저장소의 국내주식 리포트와 KIS API 문맥에서는 보통 국내 정규 거래소 시장을 가리키는 시장 표기로 쓴다. 예를 들어 watchlist의 `시장: KRX`는 해당 종목을 국내 거래소 상장 종목으로 관찰한다는 뜻이고, KIS API 파라미터에서는 `fid_cond_mrkt_div_code`의 `J:KRX`처럼 거래 시장 구분에 연결된다.

주의할 점은 `KRX`와 `KRX100`을 섞지 않는 것이다. `KRX`는 거래소 또는 시장 구분이고, `KRX100`은 지수 이름이다. NXT, SOR, UN 같은 거래소/통합 구분이 함께 나오는 경우에는 어떤 체결 시장의 데이터를 보고 있는지 별도로 적어야 한다.

### Lookback

Lookback은 Signal, 지표, 필터를 계산할 때 뒤돌아보는 과거 기간이다. `lookback: 20`이면 보통 최근 20개 거래일 또는 20개 bar를 사용한다는 뜻이다. 정확한 단위는 Strategy Spec에서 `trading_days`, `bars`, `minutes`처럼 명시해야 한다.

Lookback은 미래 정보를 쓰지 않아야 한다. 오늘 Signal을 계산한다면 오늘 장중/종가 포함 여부를 명확히 하고, 미래 가격이나 이후 거래량을 포함하면 Lookahead Bias가 된다. Lookback이 길면 초반에는 계산 가능한 데이터가 부족해 Strategy가 idle 상태가 되므로, Backtest 결과에서 첫 거래일과 워밍업 기간을 함께 확인해야 한다.

### Domain Hypothesis

Domain Hypothesis는 단순히 "차트가 좋아 보인다"가 아니라 경제, 금융, 산업, 투자자 행동에 근거한 Strategy 가설이다. 예를 들어 "실적 개선과 수급 유입이 함께 발생한 대형 반도체주는 일정 기간 상대강도가 유지될 수 있다"처럼 왜 초과성과가 날 수 있는지를 설명한다.

Backtest는 Domain Hypothesis를 검증하는 도구이지, 가설을 대신 만들어 주는 도구가 아니다. Domain Hypothesis가 비어 있으면 좋은 수익률이 나와도 Data Snooping이나 Overfitting일 가능성이 커진다. 결과 문서에는 가설, 필요한 데이터, 실패 조건, 어떤 시장 국면에서 깨질 수 있는지를 함께 적는다.

### Signal Candidate

Signal Candidate는 아직 실제 매매 Signal로 승격하지 않은 후보 신호다. 조건은 관측됐지만 Backtest, 데이터 품질, Bias Control, 거래 비용, 무효화 조건 검토가 끝나지 않은 상태를 뜻한다.

이 저장소의 퀀트 루틴에서는 검증 전 항목을 "매매 Signal"이 아니라 "Quant Signal Candidate"로 기록한다. Signal Candidate를 기록할 때는 발생 조건, 사용 데이터, 필요한 lookback, 무효화 조건, 다음 확인 항목을 같이 남겨야 한다. 실제 주문 판단으로 이어지려면 Backtest와 리포트/decision-log 검토가 별도로 필요하다.

### MDD

MDD는 Maximum Drawdown의 약자이며, 전체 기간 중 자산 곡선이 고점에서 저점까지 가장 크게 하락한 비율이다. 단순 손실률이 아니라 "이전 고점 대비 얼마나 깊게 빠졌는가"를 본다. 예를 들어 자산이 100에서 130까지 올랐다가 91까지 하락했다면 Drawdown은 `(91 / 130) - 1 = -30%`이고, 그 기간의 최대값이 MDD가 된다.

MDD는 Strategy를 실제로 버틸 수 있는지 보는 핵심 지표다. 총수익률이 높아도 MDD가 너무 크면 투자자는 중간에 전략을 중단할 가능성이 크다. 그래서 Backtest 결과에서는 Return, CAGR, Sharpe만 보지 말고 MDD와 Drawdown 차트, 회복 기간을 함께 확인한다.

### Buy-and-Hold

Buy-and-Hold는 특정 종목이나 Benchmark를 매수한 뒤 Backtest 기간 끝까지 보유하는 기준 전략이다. 매매 규칙이 거의 없으므로 Strategy가 실제로 Alpha를 냈는지 비교하기 위한 단순하고 강한 baseline으로 쓴다.

예를 들어 삼성전자 momentum Strategy를 검증한다면, 같은 기간 삼성전자를 처음부터 끝까지 보유한 Buy-and-Hold 성과와 비교해야 한다. Strategy가 거래를 많이 했는데 Buy-and-Hold보다 수익률이 낮거나 MDD가 비슷하면, 복잡한 규칙이 실익을 만들지 못한 것이다.

### Backtest

Backtest는 과거 데이터로 Strategy를 모의 실행해 성과와 위험을 검증하는 과정이다. 핵심은 과거 시점마다 실제로 알 수 있었던 데이터만 사용하고, 그 시점의 Universe, 거래 가능성, 비용, 체결 조건을 최대한 반영하는 것이다.

Backtest 결과에는 최소한 기간, Universe, Benchmark, Total Return, CAGR, MDD, Sharpe, 승률, 거래 횟수, Turnover, Transaction Cost, Slippage 가정을 기록한다. 좋은 결과가 나와도 Survivorship Bias, Lookahead Bias, Data Snooping, Overfitting을 확인하지 못하면 최종 투자 근거로 쓰지 않는다.

### Slippage

Slippage는 주문을 내려고 기대한 가격과 실제 체결 가격 사이의 차이다. 매수에서는 예상보다 비싸게 체결되거나, 매도에서는 예상보다 싸게 체결되는 형태로 나타난다. 수수료처럼 명시적으로 청구되지는 않지만 실현 수익률을 깎는 비용이다.

Slippage는 유동성이 낮은 종목, 급등락 구간, 장초반/장마감, 큰 주문 수량에서 커지기 쉽다. Backtest에서 Slippage를 0으로 두면 실전 성과가 과대평가될 수 있으므로, 최소한 고정 bp, 가격 대비 비율, 호가 스프레드 기반 가정 중 하나를 명시해야 한다.

### Transaction Cost

Transaction Cost는 주문 실행에 직접 붙는 명시적 거래 비용이다. 국내주식에서는 위탁수수료, 유관기관 수수료, 세금 또는 거래세 성격의 비용을 포함할 수 있다. Strategy가 자주 사고파는 구조라면 작은 비용도 누적되어 성과를 크게 낮춘다.

Transaction Cost는 Slippage와 구분해서 기록한다. Transaction Cost는 계좌/시장/상품별로 정해진 비용에 가깝고, Slippage는 시장 유동성과 체결 상황에 따라 달라지는 가격 차이다. Backtest 보고서에는 둘을 합쳐 "거래 비용 반영"이라고만 쓰지 말고 각각의 가정을 분리해 남긴다.

## Preferred Examples

- `Universe`를 정의한다.
- `Strategy`의 `Signal`과 `Position`을 분리한다.
- `Backtest` 결과에는 `Survivorship Bias`, `Lookahead Bias`, `Data Snooping`, `Overfitting` 판정을 붙인다.
- `Signal Candidate`는 검증 전 후보로만 쓰고 실제 주문 신호처럼 표현하지 않는다.
- `Lookback`은 단위와 포함 기준을 Strategy Spec에 명시한다.
- Main/Game/watchlist 실행은 `Smoke Test`로만 기록한다.
