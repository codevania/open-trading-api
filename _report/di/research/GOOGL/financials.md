# GOOGL Financials

## 메타

- Symbol: `GOOGL`
- Company: Alphabet Inc.
- 작성일: `2026-07-08`
- 기준 원천일: `2026-07-08`
- 원천: `_report/raw/2026/2026-07-08/sec/GOOGL/companyfacts.raw.json`
- 해석: SEC XBRL companyfacts 기반 재무 요약이며, 투자 추천 또는 주문 의도가 아니다.
- Order intent generated: `false`

## 연간 실적 요약

| 기간 종료 | 매출 | 영업이익 | 순이익 | 영업현금흐름 | Capex | Free Cash Flow | 영업이익률 | 순이익률 | FCF margin |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 2021-12-31 | $257.6B | $78.7B | $76.0B | $91.7B | $24.6B | $67.0B | 30.6% | 29.5% | 26.0% |
| 2022-12-31 | - | $74.8B | $60.0B | $91.5B | $31.5B | $60.0B | - | - | - |
| 2023-12-31 | $307.4B | $84.3B | $73.8B | $101.7B | $32.3B | $69.5B | 27.4% | 24.0% | 22.6% |
| 2024-12-31 | $350.0B | $112.4B | $100.1B | $125.3B | $52.5B | $72.8B | 32.1% | 28.6% | 20.8% |
| 2025-12-31 | $402.8B | $129.0B | $132.2B | $164.7B | $91.4B | $73.3B | 32.0% | 32.8% | 18.2% |

## 최근 분기 실적 요약

| 기간 종료 | 매출 | 영업이익 | 순이익 | 영업현금흐름 | Capex | Free Cash Flow | 영업이익률 | 순이익률 | FCF margin |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 2024-06-30 | $84.7B | $27.4B | $23.6B | - | - | - | 32.4% | 27.9% | - |
| 2024-09-30 | $88.3B | $28.5B | $26.3B | - | - | - | 32.3% | 29.8% | - |
| 2025-03-31 | $90.2B | $30.6B | $34.5B | $36.1B | $17.2B | $19.0B | 33.9% | 38.3% | 21.0% |
| 2025-06-30 | $96.4B | $31.3B | $28.2B | - | - | - | 32.4% | 29.2% | - |
| 2025-09-30 | $102.3B | $31.2B | $35.0B | - | - | - | 30.5% | 34.2% | - |
| 2026-03-31 | $109.9B | $39.7B | $62.6B | $45.8B | $35.7B | $10.1B | 36.1% | 56.9% | 9.2% |

## 재무상태

| 기간 종료 | 현금/단기투자 | Debt proxy | 순현금/(순부채 proxy) | 총자산 | 총부채 | 자본 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 2024-12-31 | $95.7B | $10.9B | $84.8B | $450.3B | $125.2B | $325.1B |
| 2025-03-31 | $95.3B | $10.9B | $84.4B | $475.4B | $130.1B | $345.3B |
| 2025-06-30 | $95.1B | $23.6B | $71.5B | $502.1B | $139.1B | $362.9B |
| 2025-09-30 | $98.5B | $21.6B | $76.9B | $536.5B | $149.6B | $386.9B |
| 2025-12-31 | $126.8B | $46.5B | $80.3B | $595.3B | $180.0B | $415.3B |
| 2026-03-31 | $126.8B | $77.5B | $49.3B | $703.9B | $225.2B | $478.7B |

## XBRL Concept 선택 메모

### Flow metrics

- `revenue`: `Revenues`; latest end `2025-12-31`, filed `2026-02-05`.
- `operating_income`: `OperatingIncomeLoss`; latest end `2025-12-31`, filed `2026-02-05`.
- `net_income`: `NetIncomeLoss`; latest end `2025-12-31`, filed `2026-02-05`.
- `operating_cash_flow`: `NetCashProvidedByUsedInOperatingActivities`; latest end `2025-12-31`, filed `2026-02-05`.
- `capex`: `PaymentsToAcquirePropertyPlantAndEquipment`; latest end `2025-12-31`, filed `2026-02-05`.

### Quarterly flow metrics

- `revenue`: `Revenues`; latest end `2026-03-31`, filed `2026-04-30`.
- `operating_income`: `OperatingIncomeLoss`; latest end `2026-03-31`, filed `2026-04-30`.
- `net_income`: `NetIncomeLoss`; latest end `2026-03-31`, filed `2026-04-30`.
- `operating_cash_flow`: `NetCashProvidedByUsedInOperatingActivities`; latest end `2026-03-31`, filed `2026-04-30`.
- `capex`: `PaymentsToAcquirePropertyPlantAndEquipment`; latest end `2026-03-31`, filed `2026-04-30`.

### Balance sheet metrics

- `cash_and_investments`: `CashCashEquivalentsAndShortTermInvestments`; latest end `2026-03-31`, filed `2026-04-30`.
- `assets`: `Assets`; latest end `2026-03-31`, filed `2026-04-30`.
- `liabilities`: `Liabilities`; latest end `2026-03-31`, filed `2026-04-30`.
- `debt_proxy`: `LongTermDebtNoncurrent`; latest end `2026-03-31`, filed `2026-04-30`.
- `equity`: `StockholdersEquity`; latest end `2026-03-31`, filed `2026-04-30`.

## 확인 필요

- SEC companyfacts는 표준화된 XBRL 숫자만 요약한다. 세그먼트, 가이던스, 리스크 문장은 `sec-filing-sections.md`와 원문 섹션을 같이 읽어야 한다.
- `Debt proxy`는 회사별 부채 태그 차이가 있어 순현금/순부채의 완전한 정의가 아니다. 10-K 주석에서 debt, lease, cash equivalents 정의를 확인해야 한다.
- Capex는 SEC 태그상 현금 유출액을 양수로 기록하는 경우를 기준으로 FCF = 영업현금흐름 - Capex로 계산했다.
