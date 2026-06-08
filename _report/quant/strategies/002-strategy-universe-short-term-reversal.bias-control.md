# 002-strategy-universe-short-term-reversal Bias Control

## Metadata

- Strategy ID: `002-strategy-universe-short-term-reversal`
- 작성일: 2026-06-08
- 현재 판정: hold

## Survivorship Bias

- 판정: hold
- 이유: Point-in-Time Investable Universe가 아직 없다.
- 요구: 과거 rebalance date 기준으로 실제 투자 가능했던 Universe snapshot이 필요하다.

## Lookahead Bias

- 판정: hold
- 방어 규칙:
  - Signal은 장마감 후 확정된 OHLCV만 사용한다.
  - 실제 진입 가능 시점은 다음 거래 세션으로 둔다.
  - 뉴스/공시는 Signal 시점 이전에 접근 가능했던 것만 사용한다.

## Data Snooping

- 판정: hold
- 방어 규칙:
  - `period`와 `threshold_pct`는 최적화 대상이 아니라 민감도 분석 대상으로 둔다.
  - 폐기한 parameter 결과도 기록한다.
  - 001 Momentum 결과를 본 뒤 유리한 종목만 골라 적용하지 않는다.

## Overfitting

- 판정: hold
- 방어 규칙:
  - In-Sample, Out-of-Sample, Forward Paper 구간을 분리한다.
  - Transaction Cost, Slippage, Tax를 적용한다.
  - `risk-off`와 panic 구간을 따로 확인한다.

## Manual Symbol Bias

- 판정: hold
- 방어 규칙:
  - Main/Game/DI watchlist는 Quant Universe가 아니다.
  - manual symbol set은 Data Pipeline Smoke Test에만 사용한다.
  - manual smoke-test 결과는 Strategy 성과로 해석하지 않는다.

## Current Judgment

최종 판정은 `hold`다.

해제 조건:

- Point-in-Time Universe 확보
- full smoke-test raw 확보
- OOS 결과 기록
- Stress period review
- 001 Momentum과 실패 조건 차이 확인
