# Paper Signal Tracking Routine

## Purpose

검증 전 Quant Signal Candidate를 실제 매매와 분리해 관찰한다.

이 routine은 주문, 추천, 확정 Signal을 만들지 않는다. `Data Pipeline Smoke Test` 또는 이후 paper run에서 나온 Candidate를 날짜별로 기록하고, 다음 거래일 이후 가격 흐름과 데이터 품질을 추적한다.

## Inputs

- `_report/quant/research/YYYY-MM-DD-data-pipeline-smoke-test-result.md`
- Strategy spec and `.kis.yaml`
- raw data quality notes
- Market Regime Scan if available

## Output

```text
_report/quant/research/YYYY-MM-DD-paper-signal-log.md
```

## Required Labels

반드시 다음 문구를 유지한다.

- `paper tracking only`
- `not trade instruction`
- `manual_smoke_test`
- `Point-in-Time Universe pending`
- `Bias Control: hold`

## Tracking Table

각 row는 다음을 기록한다.

| Field | Meaning |
| --- | --- |
| Strategy | Strategy ID |
| Symbol | KRX symbol |
| Signal Date | Signal 계산 기준일 |
| Candidate State | BUY candidate / SELL candidate / HOLD / data-insufficient |
| Evidence | ROC, SMA divergence, close, volume |
| Data Source | raw directory or result file |
| Follow-Up Window | next 1D, 5D, 20D paper observation |
| Invalidator | data anomaly, hypothesis break, regime mismatch |
| Action | always paper tracking only before validation |

## Update Cycle

1. Smoke-test or paper-run result를 읽는다.
2. Candidate state를 그대로 옮긴다.
3. 실제 주문 문구를 제거한다.
4. 다음 관찰일을 정한다.
5. 후속 가격 흐름은 성과가 아니라 관찰 결과로만 기록한다.

## Stop Conditions

- raw source가 없다.
- Signal date가 불명확하다.
- Candidate state가 매매 지시처럼 쓰였다.
- Point-in-Time Universe가 없는 결과를 Backtest처럼 해석한다.
- DI watchlist를 Quant Universe로 오해하게 만드는 문구가 있다.
