# Out-of-Sample and Walk-Forward Plan

## Metadata

- 작성일: 2026-06-08
- 작성자: Codex
- 대상 Strategy: `001-strategy-universe-momentum`
- 대상 Market: `KRX`
- 현재 판정: hold
- 목적: Backtest 전에 `In-Sample`, `Out-of-Sample`, `Walk-Forward` 구간을 고정해 `Data Snooping`과 `Overfitting` 위험을 줄인다.

## 1. 원칙

이 문서는 성과 검증 구간을 미리 고정하기 위한 계획이다.

중요 원칙:

- `Out-of-Sample` 성과를 보고 parameter를 다시 고르지 않는다.
- `lookback` 후보는 이미 정한 `20`, `60`, `120`, `252`만 사용한다.
- `threshold`는 `0.0`, `stop_loss_pct`는 `10.0`으로 둔다.
- 가장 좋은 parameter 하나만 골라 Strategy 성과로 주장하지 않는다.
- 모든 결과는 비용 반영 전/후를 분리한다.
- `Point-in-Time Investable Universe`가 확보되지 않으면 결과 판정은 `hold`다.

## 2. Date Window v0

날짜는 calendar date로 고정하고, 실행 시 실제 KRX trading calendar의 직전/직후 거래일로 보정한다.

| Segment | Calendar Date | Purpose | Interpretation |
| --- | --- | --- | --- |
| `warmup` | 2018-01-01 to 2019-12-31 | `600 trading days` 이상 history 확보 여부 확인 | 성과 해석 제외 |
| `in_sample` | 2020-01-01 to 2022-12-31 | Strategy rule과 data pipeline 안정성 확인 | 연구용 |
| `out_of_sample` | 2023-01-01 to 2025-12-31 | 사전 고정 rule의 검증 | `hold` 또는 제한적 해석 |
| `forward_paper` | 2026-01-01 onward | 실제 Signal Candidate 추적 | Paper Signal only |

주의:

- 실제 데이터가 2018년부터 확보되지 않으면 시작일을 늦추지 말고 `Data Quality`에 기록한다.
- 특정 종목의 상장일이 늦어 `warmup`이 부족하면 해당 종목은 Universe에서 제외하거나 smoke test limitation으로 기록한다.
- 2026년 구간은 현재 진행 중인 구간이므로 Backtest 성과 판정에 섞지 않는다.

## 3. Walk-Forward v0

기본 `Walk-Forward`는 3년 관찰, 1년 검증으로 둔다.

| Fold | Training/Observation | Test | Notes |
| --- | --- | --- | --- |
| `wf_01` | 2020-01-01 to 2022-12-31 | 2023-01-01 to 2023-12-31 | 첫 OOS |
| `wf_02` | 2021-01-01 to 2023-12-31 | 2024-01-01 to 2024-12-31 | regime 변화 확인 |
| `wf_03` | 2022-01-01 to 2024-12-31 | 2025-01-01 to 2025-12-31 | 최근 구간 확인 |

해석 규칙:

- Training window는 parameter를 새로 최적화하는 용도가 아니다.
- 각 fold에서 동일 parameter 후보군을 그대로 실행한다.
- OOS fold 중 하나만 좋고 나머지가 약하면 `hold` 또는 `fail`로 둔다.
- 2025년 상반기 관세/정책 충격 같은 event-driven stress는 별도 해석한다.

## 4. Required Outputs

각 실행 결과에는 다음을 남긴다.

- `Universe definition`
- `Universe source_mode`
- `Point-in-Time` 여부
- `Transaction Cost`, `Slippage`, `Tax`
- `Benchmark`
- `parameter set`
- `in_sample` 결과
- `out_of_sample` 결과
- `walk_forward` fold별 결과
- `Stress Period` 결과
- `Data Quality` limitation
- `Bias Control` 판정

## 5. Pass/Hold/Fail Gate

| Status | Condition |
| --- | --- |
| `pass` | `Point-in-Time Investable Universe`와 OOS/walk-forward 결과가 모두 재현 가능하고 Bias Control blocker가 없다. |
| `hold` | 검증 구간은 고정했지만 Universe, raw data, calendar, stress 검증 일부가 미완료다. |
| `fail` | 현재 survivor/manual universe를 성과 증거로 사용했거나 OOS 결과를 보고 parameter를 재선택했다. |

현재 판정은 `hold`다.

## 6. Next Action

1. `Data Pipeline Smoke Test`를 별도 문서 기준으로 실행한다.
2. KIS/KRX data calendar가 이 window를 지원하는지 확인한다.
3. `Point-in-Time Investable Universe` raw snapshot이 준비되면 이 window로 parser와 Backtest를 연결한다.
4. Backtest report는 [[_report/quant/templates/backtest-report|_report/quant/templates/backtest-report.md]] 형식을 따른다.
