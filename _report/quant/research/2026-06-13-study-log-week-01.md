# Quant Study Log

## Metadata

- Date: 2026-06-13
- Week: 1
- Topic: Quant mindset
- Study time: 60 minutes
- Author: Codex

## Sentence I Should Be Able To Explain

- Quant는 특정 종목을 맞히는 일이 아니라, 사전에 정의한 Universe 안에서 Strategy 규칙이 반복 가능한지 검증하는 일이다.

## Reading

- Material: `_report/quant/learning-roadmap.md`
- Key summary: first 12 weeks should focus on Strategy, data quality, Bias Control, and Backtest interpretation before any live trading.
- Unknown terms: `Alpha`, `Benchmark`, `MDD`, `Survivorship Bias`, `Lookahead Bias`, `Data Snooping`, `Overfitting`, `Point-in-Time`, `Slippage`, `Out-of-Sample`.

- Material: `_report/quant/universe.md`
- Key summary: Main/Game/DI watchlists are not Quant Universe inputs; a Quant Universe must be rule-based and reproducible.
- Unknown terms: `Investable Universe`, `Inclusion Rule`, `Exclusion Rule`, `Liquidity Filter`.

- Material: `_report/quant/strategies/001-strategy-universe-momentum.md`
- Key summary: the first Strategy is a Momentum baseline for Signal tracking, not a confirmed Alpha Strategy.
- Unknown terms: `ROC`, `Signal Timing`, `Stress Period`, `Position`.

## Practice

- Practice: reviewed the first paper Signal log and checked whether a 1D follow-up can be computed from saved raw data.
- Files or data used:
  - `_report/quant/research/2026-06-09-paper-signal-log.md`
  - `_report/raw/2026/2026-06-09/quant/smoke-test/`
  - `_report/quant/research/2026-06-13-paper-signal-follow-up.md`
- Commands run: repo file inspection only; no KIS MCP call was available in the current Codex tool surface.
- Result: 1D follow-up remains `data-unavailable` because the saved raw set ends at `20260605`.

## Concepts Learned

| Concept | My explanation | Still uncertain |
| --- | --- | --- |
| Universe | Strategy가 사전에 투자 가능하다고 정한 후보 집합이다. | KRX 데이터를 어떤 조합으로 자동화할지 |
| Strategy | 반복 가능한 규칙 묶음이다. 종목 감상이 아니다. | 언제 Strategy를 폐기할지 |
| Signal | Strategy 규칙이 만든 후보 상태다. 주문 지시가 아니다. | Signal 유지 기간 |
| Position | 실제 자금이 들어간 상태와 크기다. | 개인 자산 내 적정 비중 |
| Alpha | Benchmark보다 낫다고 주장하려는 초과 성과다. | 비용 반영 후 남는지 |
| Benchmark | Strategy와 비교할 기준이다. | KRX 전체 Universe에 맞는 대표 Benchmark |
| MDD | 고점 대비 최대 하락폭이다. | 어느 수준이면 폐기할지 |
| Survivorship Bias | 살아남은 종목만 보고 과거 성과를 좋게 착각하는 문제다. | 상폐/관리종목 데이터를 얼마나 확보해야 충분한지 |
| Lookahead Bias | 당시에는 몰랐던 미래 정보를 과거 판단에 쓰는 문제다. | 공시/상태 데이터의 실제 사용 가능 시점 |
| Data Snooping | 여러 조건을 시도한 뒤 우연히 좋은 결과만 고르는 문제다. | 폐기한 실험을 어떻게 기록할지 |
| Overfitting | 과거 데이터에만 너무 잘 맞아 미래에서 깨지는 문제다. | parameter 민감도 기준 |
| Point-in-Time | 해당 날짜에 실제 알 수 있었던 Universe와 데이터를 쓰는 방식이다. | KRX snapshot 자동화 가능성 |
| Slippage | 이론 가격과 실제 체결 가격의 차이다. | 국내 주식 체결 품질 추정치 |

## Link To Quant Strategy

- Universe link: Quant Universe는 `KRX common_stock + Listing Age + Liquidity Filter`처럼 규칙으로 시작해야 한다.
- Strategy hypothesis link: `001 Momentum`은 추세 지속, `002 Short-Term Reversal`은 과잉 반응 회복이라는 서로 다른 가설을 가진다.
- Data quality link: 저장된 raw가 없으면 follow-up 성과를 계산하지 않는다.
- Bias Control link: Point-in-Time Universe가 없으면 Backtest 해석은 `hold`다.
- Position/Risk link: paper Signal은 실제 Position으로 연결하지 않는다.

## Next Actions

1. KRX manual snapshot raw를 확보해 Point-in-Time Universe 준비를 시작한다.
2. KIS raw follow-up을 저장한 뒤 1D, 5D, 20D paper observation을 계산한다.
3. Week 2에서는 OHLCV, 거래대금, 거래정지, 상장/상폐 데이터 품질을 학습한다.

## Caution

- This log is a study record, not investment advice.
- Unknown terms should remain visible until verified.
- Good-looking practice output is not Strategy validation.
