# Transaction Cost and Slippage Assumptions

## Metadata

- 작성일: 2026-06-08
- 작성자: Codex
- 대상 Strategy: `001-strategy-universe-momentum`
- 대상 Market: `KRX`
- 현재 판정: hold
- 목적: Backtest 전에 `Transaction Cost`, `Slippage`, `Tax` 가정을 고정해 Strategy 성과 과대평가를 막는다.

## 1. 원칙

이 문서는 실거래 수수료 안내가 아니라 Quant 연구용 비용 가정이다.

실제 주문 전에는 다음을 반드시 교체한다.

- 실제 증권사 계좌의 commission rate
- 주문 채널별 수수료
- 세법 변경 사항
- 종목별 호가 공백과 체결 가능성

Strategy 결과는 비용 차감 전/후를 항상 분리해 기록한다.

## 2. Baseline Cost Model v0

| Component | Side | Baseline | Stress | Notes |
| --- | --- | ---: | ---: | --- |
| `Commission` | buy/sell | `1.5 bps` | `5.0 bps` | 실제 KIS 계좌 수수료로 override 필요 |
| `Slippage` | buy/sell | `5.0 bps` | `20.0 bps` | Universe v0의 Liquidity Filter 통과 종목 기준 |
| `Tax` | sell only | `20.0 bps` | `20.0 bps` | 2026년 KRX listed shares 총 거래세 가정 |

Baseline round-trip cost:

```text
buy_cost_bps  = commission 1.5 + slippage 5.0
sell_cost_bps = commission 1.5 + slippage 5.0 + tax 20.0
round_trip_cost_bps = 33.0
```

Stress round-trip cost:

```text
buy_cost_bps  = commission 5.0 + slippage 20.0
sell_cost_bps = commission 5.0 + slippage 20.0 + tax 20.0
round_trip_cost_bps = 70.0
```

## 3. 2026 KRX Tax Assumption

2026년 연구 기준으로 KRX listed shares 매도 거래세는 총 `0.20%`로 둔다.

해석:

- `0.20% = 20.0 bps`
- Backtest에서는 매수 시점이 아니라 매도 시점에만 적용한다.
- KOSPI와 KOSDAQ 모두 `20.0 bps`로 둔다.
- KOSPI의 세부 구성은 증권거래세와 농어촌특별세로 나뉠 수 있으나, Strategy 비용 모델에서는 총 매도 비용만 사용한다.

확인 출처:

- PwC Tax Summaries, Republic of Korea, Corporate - Other taxes: `https://taxsummaries.pwc.com/republic-of-korea/corporate/other-taxes`
- Yonhap News Agency, 2026 KOSPI transaction tax report: `https://en.yna.co.kr/view/AEN20251201003500320`
- Asia Business Daily, 2026 KOSPI/KOSDAQ securities transaction tax report: `https://view.asiae.co.kr/en/article/2025120109040485489`

## 4. Slippage Assumption

`Slippage`는 현재 고정된 Universe v0의 Liquidity Filter를 전제로 한다.

Universe v0 조건:

- `avg_trading_value_20d_krw >= 1,000,000,000`
- `min_ohlcv_trading_days >= 600`
- 거래정지, 관리종목, 투자주의/경고/위험, 상장폐지 예정 제외

따라서 baseline `Slippage`는 `5.0 bps per side`로 둔다.

다만 다음 경우에는 stress `20.0 bps per side`를 사용한다.

- 장중 급락 또는 급등
- 시장 전체 유동성 축소
- 거래대금은 충분하지만 호가 공백이 큰 종목
- 시가/종가 근처 주문
- `Market Regime`이 `risk-off` 또는 `high-volatility`

## 5. Commission Assumption

`Commission`은 실제 KIS 계좌/채널 수수료가 아니라 연구용 placeholder다.

기본값:

- `1.5 bps per side`

Stress:

- `5.0 bps per side`

실거래 검토 전 필수 조치:

- 실제 계좌의 국내주식 온라인 commission rate 확인
- 주문 채널별 차이 확인
- 최소 수수료 또는 유관기관 제비용 포함 여부 확인
- 세금과 commission을 중복 계산하지 않았는지 확인

## 6. Bias Control 영향

이 문서 작성 후에도 최종 판정은 `hold`다.

개선된 점:

- 비용 없는 Backtest 결과를 성과로 오해하지 않도록 기본 비용 모델을 고정했다.
- `Transaction Cost`, `Slippage`, `Tax` 가정이 Strategy config에 들어갈 수 있다.

남은 blocker:

- `Point-in-Time Investable Universe` 미확보
- KRX 수동 snapshot raw file 미확보
- KRX/KIS OHLCV calendar 충돌 audit 미완료
- Out-of-Sample 또는 walk-forward 구간 미설정

## 7. Strategy Config 반영 기준

`001-strategy-universe-momentum.kis.yaml`에는 다음을 반영한다.

- `risk.transaction_cost.current_status: baseline_assumption_set_external_fee_override_required`
- `risk.slippage.current_status: baseline_assumption_set`
- `risk.tax.current_status: 2026_krx_sell_side_assumption_set`
- `validation_policy.cost_model.required: true`

이 가정은 Strategy 비교의 최소 방어선이다. 실제 실거래 판단에는 부족하다.
