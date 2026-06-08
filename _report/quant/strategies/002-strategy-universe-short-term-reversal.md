# 002-strategy-universe-short-term-reversal

## Metadata

- Strategy ID: `002-strategy-universe-short-term-reversal`
- Strategy Name: Strategy Universe Short-Term Reversal Candidate v0
- 상태: candidate, not backtest ready
- 작성일: 2026-06-08
- 작성자: Codex
- 관련 YAML: `002-strategy-universe-short-term-reversal.kis.yaml`
- 연결 도구: Backtester `short_term_reversal` preset
- Bias Control: `_report/quant/strategies/002-strategy-universe-short-term-reversal.bias-control.md`
- Strategy Portfolio 역할: Momentum과 다른 실패 조건을 가진 두 번째 후보 Strategy

## 1. Economic/Financial Hypothesis

짧은 기간에 평균 가격 대비 과도하게 하락한 종목은 일시적 수급 왜곡, 과매도, 단기 뉴스 과잉 반응이 해소되며 평균으로 되돌아갈 수 있다.

- Domain Hypothesis: 단기 가격 충격이 항상 장기 Fundamental 훼손을 의미하지는 않는다.
- 관찰 가능한 현상: 종가가 단기 `SMA`보다 일정 비율 이상 낮다.
- 기대 효과: Momentum이 급격한 반전장에서 손실을 볼 때, 과매도 반등 후보를 별도 Signal Candidate로 포착한다.
- 실패 가능성이 높은 시장: 구조적 악재, 유동성 붕괴, 장기 하락 추세, 관리종목/거래정지 위험.
- 유리한 시장: range-bound, neutral, panic 후 단기 회복 구간.

## 2. Diversification Against Strategy 001

`001-strategy-universe-momentum`은 강한 종목의 추세 지속을 가정한다.

이 Strategy는 약해진 종목의 단기 평균회귀를 가정한다.

| Dimension | 001 Momentum | 002 Short-Term Reversal |
| --- | --- | --- |
| Core Signal | Positive ROC | Close below short SMA |
| Domain Hypothesis | Trend continuation | Overreaction reversal |
| Good Regime | risk-on, theme trend | neutral, range-bound, panic rebound |
| Main Failure | sharp reversal after strength | falling knife, structural decline |
| Correlation Risk | growth/theme crowding | distressed/liquidity traps |

두 Strategy는 같은 가격 데이터를 쓰지만, 진입 방향과 실패 조건이 다르다. 그래도 둘 다 price-only Strategy이므로 완전한 분산으로 보지 않는다.

## 3. Universe

Universe는 `_report/quant/universe.md`의 `v0` rule-based Universe를 공유한다.

필수 조건:

- KRX `KOSPI` 또는 `KOSDAQ` 보통주
- 정상 거래 가능 상태
- Listing Age 최소 `252 trading days`
- 최근 `20 trading days` 평균 거래대금 최소 `1,000,000,000 KRW`
- 최소 `600 trading days` OHLCV
- ETF, ETN, ELW, preferred share, SPAC, REIT 등 제외

Point-in-Time Universe가 없으면 결과 해석은 `hold` 이하로 둔다.

## 4. Entry Rule

Backtester `short_term_reversal` preset을 기준으로 한다.

- `period`: 5 trading days
- `threshold_pct`: 3.0
- Entry: `Close < SMA(period) * (1 - threshold_pct / 100)`
- 해석: 종가가 5일 평균보다 3% 이상 낮으면 과매도 후보로 본다.

## 5. Exit Rule

- Exit: `Close > SMA(period) * (1 + threshold_pct / 100)`
- 해석: 종가가 5일 평균보다 3% 이상 높으면 평균회귀가 과열로 바뀐 것으로 본다.
- Stop Loss: 5%

## 6. Risk and Position

현재 단계에서 실제 자금 배분은 금지한다.

- Capital allocation: `0%`
- 허용 행동: `paper Signal tracking only`
- Position policy: `_report/quant/research/2026-06-08-position-sizing-capital-allocation-policy.md`
- Transaction Cost/Slippage/Tax: `_report/quant/research/2026-06-08-transaction-cost-slippage-assumptions.md`

## 7. Validation Requirements

이 Strategy는 다음 조건 전까지 Backtest 성과로 해석하지 않는다.

- Point-in-Time Universe 확보
- raw daily OHLCV 최소 `600 trading days`
- `lookback` 대비 충분한 warmup
- Transaction Cost, Slippage, Tax 적용
- Out-of-Sample 결과 기록
- Stress period review
- Bias Control `pass`

## 8. Stop Conditions

다음 조건이면 폐기 또는 재설계한다.

- 하락 추세 종목을 반복 매수해 MDD가 과도하게 커진다.
- 거래대금이 얇은 종목에서 Slippage가 Signal edge를 제거한다.
- OOS에서 반등보다 추가 하락 비율이 높다.
- Market Regime `risk-off`에서 손실이 집중된다.
- Parameter가 특정 기간에만 맞는다.

## 9. Current Decision

현재 결정은 `candidate_hold`다.

다음 단계:

1. YAML loader 검증을 통과한다.
2. full smoke-test raw 확보 후 Signal Candidate 계산 가능성을 확인한다.
3. 001 Momentum과 같은 raw set에서 Signal overlap과 실패 조건 차이를 비교한다.
