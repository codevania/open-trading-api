# Position Sizing and Capital Allocation Policy

## Metadata

- 작성일: 2026-06-08
- 작성자: Codex
- 대상: Quant Strategy 전체
- 현재 판정: hold
- 목적: 검증 전 Strategy Signal을 실제 투자 규모와 분리하고, 단계별 Exposure cap을 정한다.

## 1. Principle

Quant는 종목을 고르는 작업이 아니라 Strategy를 검증하는 작업이다.

따라서 `Position Sizing`은 특정 종목 확신도가 아니라 다음 조건으로 결정한다.

- Strategy validation stage
- Data quality
- Point-in-Time Universe 확보 여부
- Out-of-Sample 결과
- Drawdown tolerance
- Liquidity and Slippage
- 전체 자산 내 역할

## 2. Capital Buckets

이 문서는 실제 계좌 금액, 보유수량, 현금 잔고를 기록하지 않는다.

개념상 전체 투자 가능 자산은 다음 bucket으로 나눈다.

| Bucket | Purpose | Quant Relation |
| --- | --- | --- |
| Core DI | 재량 투자와 장기 관찰 | Quant Universe가 아님 |
| Quant Research | Strategy 연구와 Signal tracking | paper only |
| Quant Pilot | 검증 통과 후 소액 실험 | approval required |
| Cash Buffer | 유동성, 오류 대응, 기회 대기 | 항상 별도 유지 |

현재 `001-strategy-universe-momentum`은 `Quant Research` bucket에만 속한다.

## 3. Stage-Based Exposure Cap

| Stage | Required Evidence | Allowed Action | Strategy Capital Cap | Single Position Cap |
| --- | --- | --- | ---: | ---: |
| 0. Idea | Domain Hypothesis only | 문서화 | 0% | 0% |
| 1. Smoke Test | raw parser and Signal Candidate works | paper Signal tracking | 0% | 0% |
| 2. Backtest Hold | Point-in-Time incomplete or OOS incomplete | paper Signal tracking | 0% | 0% |
| 3. Backtest Pass | Point-in-Time Universe, OOS, cost model, Bias Control pass | pilot review only | 1% max | 0.25% max |
| 4. Forward Paper Pass | 최소 4주 이상 live paper tracking | pilot eligible | 2% max | 0.5% max |
| 5. Production Review | 장애 대응, order checks, drawdown stop documented | separate approval required | TBD | TBD |

현재 상태:

- `001-strategy-universe-momentum`: Stage 1 또는 Stage 2 이하
- 실제 capital allocation: `0%`
- 허용 행동: `paper Signal tracking`

## 4. Risk Limits

검증 전 기본 제한:

- Leverage: 0
- Short selling: 금지
- Derivatives: 금지
- Order automation: 금지
- Manual watchlist performance claim: 금지

Pilot 전 최소 요구:

- Point-in-Time Universe 확보
- 최소 2년 이상 또는 lookback의 10배 이상 daily OHLCV
- Transaction Cost, Slippage, Tax 적용
- Out-of-Sample 결과 기록
- Stress period review
- Paper Signal tracking 결과 기록
- Kill switch 조건 문서화

## 5. Cash Buffer Rule

Quant Strategy가 production review를 통과하기 전까지 현금 비중은 Strategy Signal로 줄이지 않는다.

Pilot 단계에서도 Cash Buffer는 다음 목적으로 분리한다.

- 주문 실패와 중복 주문 대응
- 급락/거래정지/호가 공백 대응
- Strategy 중단 후 재배치 대기
- DI와 Quant 의사결정 충돌 방지

## 6. Stop and De-Risk Rules

다음 중 하나라도 발생하면 Strategy capital cap을 즉시 `0%`로 되돌린다.

- raw data anomaly
- duplicated or missing trading dates
- Point-in-Time Universe 재현 실패
- cost model 누락
- OOS 결과가 in-sample 대비 크게 악화
- MDD가 사전 허용치를 초과
- Signal와 실제 체결 가능 가격의 괴리가 반복
- Strategy logic 변경 후 재검증 미완료

## 7. Current Decision

현재 Quant 작업의 목적은 실제 매매가 아니라 검증 체계 구축이다.

따라서 현재 결정은 다음과 같다.

- `001-strategy-universe-momentum` capital allocation: `0%`
- 실행 방식: `paper Signal tracking only`
- 다음 해제 조건: full smoke test raw 확보, Point-in-Time Universe 확보, Backtest/OOS/Bias Control 통과

이 문서는 투자 조언이 아니라 프로젝트 내부 Risk Policy다.
