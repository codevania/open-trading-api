# AMZN Financials

## 메타

- Symbol: `AMZN`
- Company: AMAZON COM INC
- 작성일: `2026-07-08`
- 기준 원천일: `2026-07-08`
- 원천: `_report/raw/2026/2026-07-08/sec/AMZN/companyfacts.raw.json`
- 해석: SEC XBRL companyfacts 기반 재무 요약이며, 투자 추천 또는 주문 의도가 아니다.
- Order intent generated: `false`

## 연간 실적 요약

| 기간 종료 | 매출 | 영업이익 | 순이익 | 영업현금흐름 | Capex | Free Cash Flow | 영업이익률 | 순이익률 | FCF margin |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 2021-12-31 | $469.8B | $24.9B | $33.4B | $46.3B | $61.1B | -$14.7B | 5.3% | 7.1% | -3.1% |
| 2022-12-31 | $514.0B | $12.2B | -$2.7B | $46.8B | $63.6B | -$16.9B | 2.4% | -0.5% | -3.3% |
| 2023-12-31 | $574.8B | $36.9B | $30.4B | $84.9B | $52.7B | $32.2B | 6.4% | 5.3% | 5.6% |
| 2024-12-31 | $638.0B | $68.6B | $59.2B | $115.9B | $83.0B | $32.9B | 10.8% | 9.3% | 5.2% |
| 2025-12-31 | $716.9B | $80.0B | $77.7B | $139.5B | $131.8B | $7.7B | 11.2% | 10.8% | 1.1% |

## 최근 분기 실적 요약

| 기간 종료 | 매출 | 영업이익 | 순이익 | 영업현금흐름 | Capex | Free Cash Flow | 영업이익률 | 순이익률 | FCF margin |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 2024-06-30 | $148.0B | $14.7B | $13.5B | $25.3B | $17.6B | $7.7B | 9.9% | 9.1% | 5.2% |
| 2024-09-30 | $158.9B | $17.4B | $15.3B | $26.0B | $22.6B | $3.4B | 11.0% | 9.6% | 2.1% |
| 2025-03-31 | $155.7B | $18.4B | $17.1B | $17.0B | $25.0B | -$8.0B | 11.8% | 11.0% | -5.1% |
| 2025-06-30 | $167.7B | $19.2B | $18.2B | $32.5B | $32.2B | $332.0M | 11.4% | 10.8% | 0.2% |
| 2025-09-30 | $180.2B | $17.4B | $21.2B | $35.5B | $35.1B | $430.0M | 9.7% | 11.8% | 0.2% |
| 2026-03-31 | $181.5B | $23.9B | $30.3B | $26.0B | $44.2B | -$18.2B | 13.1% | 16.7% | -10.0% |

## 재무상태

| 기간 종료 | 현금/단기투자 | Debt proxy | 순현금/(순부채 proxy) | 총자산 | 총부채 | 자본 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 2024-12-31 | $78.8B | $58.0B | $20.8B | $624.9B | - | $286.0B |
| 2025-03-31 | $66.2B | $58.8B | $7.5B | $643.3B | - | $305.9B |
| 2025-06-30 | $57.7B | $56.1B | $1.7B | $682.2B | - | $333.8B |
| 2025-09-30 | $66.9B | $55.1B | $11.8B | $727.9B | - | $369.6B |
| 2025-12-31 | $86.8B | $68.8B | $18.0B | $818.0B | - | $411.1B |
| 2026-03-31 | $101.8B | $122.6B | -$20.8B | $916.6B | - | $441.9B |

## XBRL Concept 선택 메모

### Flow metrics

- `revenue`: `RevenueFromContractWithCustomerExcludingAssessedTax`; latest end `2025-12-31`, filed `2026-02-06`.
- `operating_income`: `OperatingIncomeLoss`; latest end `2025-12-31`, filed `2026-02-06`.
- `net_income`: `NetIncomeLoss`; latest end `2025-12-31`, filed `2026-02-06`.
- `operating_cash_flow`: `NetCashProvidedByUsedInOperatingActivities`; latest end `2025-12-31`, filed `2026-02-06`.
- `capex`: `PaymentsToAcquireProductiveAssets`; latest end `2025-12-31`, filed `2026-02-06`.

### Quarterly flow metrics

- `revenue`: `RevenueFromContractWithCustomerExcludingAssessedTax`; latest end `2026-03-31`, filed `2026-04-30`.
- `operating_income`: `OperatingIncomeLoss`; latest end `2026-03-31`, filed `2026-04-30`.
- `net_income`: `NetIncomeLoss`; latest end `2026-03-31`, filed `2026-04-30`.
- `operating_cash_flow`: `NetCashProvidedByUsedInOperatingActivities`; latest end `2026-03-31`, filed `2026-04-30`.
- `capex`: `PaymentsToAcquireProductiveAssets`; latest end `2026-03-31`, filed `2026-04-30`.

### Balance sheet metrics

- `cash_and_investments`: `CashAndCashEquivalentsAtCarryingValue`; latest end `2026-03-31`, filed `2026-04-30`.
- `assets`: `Assets`; latest end `2026-03-31`, filed `2026-04-30`.
- `liabilities`: no usable SEC companyfacts concept found in the configured alternatives.
- `debt_proxy`: `LongTermDebt`; latest end `2026-03-31`, filed `2026-04-30`.
- `equity`: `StockholdersEquity`; latest end `2026-03-31`, filed `2026-04-30`.

## 확인 필요

- SEC companyfacts는 표준화된 XBRL 숫자만 요약한다. 세그먼트, 가이던스, 리스크 문장은 `sec-filing-sections.md`와 원문 섹션을 같이 읽어야 한다.
- `Debt proxy`는 회사별 부채 태그 차이가 있어 순현금/순부채의 완전한 정의가 아니다. 10-K 주석에서 debt, lease, cash equivalents 정의를 확인해야 한다.
- Capex는 SEC 태그상 현금 유출액을 양수로 기록하는 경우를 기준으로 FCF = 영업현금흐름 - Capex로 계산했다.
