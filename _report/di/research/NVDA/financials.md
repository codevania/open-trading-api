# NVDA Financials

## 메타

- Symbol: `NVDA`
- Company: NVIDIA CORP
- 작성일: `2026-07-08`
- 기준 원천일: `2026-07-08`
- 원천: `_report/raw/2026/2026-07-08/sec/NVDA/companyfacts.raw.json`
- 해석: SEC XBRL companyfacts 기반 재무 요약이며, 투자 추천 또는 주문 의도가 아니다.
- Order intent generated: `false`

## 연간 실적 요약

| 기간 종료 | 매출 | 영업이익 | 순이익 | 영업현금흐름 | Capex | Free Cash Flow | 영업이익률 | 순이익률 | FCF margin |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 2022-01-30 | $26.9B | $10.0B | $9.8B | $9.1B | $976.0M | $8.1B | 37.3% | 36.2% | 30.2% |
| 2023-01-29 | $27.0B | $4.2B | $4.4B | $5.6B | $1.8B | $3.8B | 15.7% | 16.2% | 14.1% |
| 2024-01-28 | $60.9B | $33.0B | $29.8B | $28.1B | $1.1B | $27.0B | 54.1% | 48.8% | 44.4% |
| 2025-01-26 | $130.5B | $81.5B | $72.9B | $64.1B | $3.2B | $60.9B | 62.4% | 55.8% | 46.6% |
| 2026-01-25 | $215.9B | $130.4B | $120.1B | $102.7B | $6.0B | $96.7B | 60.4% | 55.6% | 44.8% |

## 최근 분기 실적 요약

| 기간 종료 | 매출 | 영업이익 | 순이익 | 영업현금흐름 | Capex | Free Cash Flow | 영업이익률 | 순이익률 | FCF margin |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 2024-07-28 | $30.0B | $18.6B | $16.6B | - | - | - | 62.1% | 55.3% | - |
| 2024-10-27 | $35.1B | $21.9B | $19.3B | - | - | - | 62.3% | 55.0% | - |
| 2025-04-27 | $44.1B | $21.6B | $18.8B | $27.4B | $1.2B | $26.2B | 49.1% | 42.6% | 59.4% |
| 2025-07-27 | $46.7B | $28.4B | $26.4B | - | - | - | 60.8% | 56.5% | - |
| 2025-10-26 | $57.0B | $36.0B | $31.9B | - | - | - | 63.2% | 56.0% | - |
| 2026-04-26 | $81.6B | $53.5B | $58.3B | $50.3B | $1.8B | $48.6B | 65.6% | 71.5% | 59.5% |

## 재무상태

| 기간 종료 | 현금/단기투자 | Debt proxy | 순현금/(순부채 proxy) | 총자산 | 총부채 | 자본 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 2025-01-26 | $8.6B | $8.5B | $126.0M | $111.6B | $32.3B | $79.3B |
| 2025-04-27 | $15.2B | $8.5B | $6.8B | $125.3B | $41.4B | $83.8B |
| 2025-07-27 | $11.6B | $8.5B | $3.2B | $140.7B | $40.6B | $100.1B |
| 2025-10-26 | $11.5B | $8.5B | $3.0B | $161.1B | $42.3B | $118.9B |
| 2026-01-25 | $10.6B | $8.5B | $2.1B | $206.8B | $49.5B | $157.3B |
| 2026-04-26 | $13.2B | $8.5B | $4.8B | $259.5B | $64.0B | $195.5B |

## XBRL Concept 선택 메모

### Flow metrics

- `revenue`: `Revenues`; latest end `2026-01-25`, filed `2026-02-25`.
- `operating_income`: `OperatingIncomeLoss`; latest end `2026-01-25`, filed `2026-02-25`.
- `net_income`: `NetIncomeLoss`; latest end `2026-01-25`, filed `2026-02-25`.
- `operating_cash_flow`: `NetCashProvidedByUsedInOperatingActivities`; latest end `2026-01-25`, filed `2026-02-25`.
- `capex`: `PaymentsToAcquireProductiveAssets`; latest end `2026-01-25`, filed `2026-02-25`.

### Quarterly flow metrics

- `revenue`: `Revenues`; latest end `2026-04-26`, filed `2026-05-20`.
- `operating_income`: `OperatingIncomeLoss`; latest end `2026-04-26`, filed `2026-05-20`.
- `net_income`: `NetIncomeLoss`; latest end `2026-04-26`, filed `2026-05-20`.
- `operating_cash_flow`: `NetCashProvidedByUsedInOperatingActivities`; latest end `2026-04-26`, filed `2026-05-20`.
- `capex`: `PaymentsToAcquireProductiveAssets`; latest end `2026-04-26`, filed `2026-05-20`.

### Balance sheet metrics

- `cash_and_investments`: `CashAndCashEquivalentsAtCarryingValue`; latest end `2026-04-26`, filed `2026-05-20`.
- `assets`: `Assets`; latest end `2026-04-26`, filed `2026-05-20`.
- `liabilities`: `Liabilities`; latest end `2026-04-26`, filed `2026-05-20`.
- `debt_proxy`: `LongTermDebt`; latest end `2026-04-26`, filed `2026-05-20`.
- `equity`: `StockholdersEquity`; latest end `2026-04-26`, filed `2026-05-20`.

## 확인 필요

- SEC companyfacts는 표준화된 XBRL 숫자만 요약한다. 세그먼트, 가이던스, 리스크 문장은 `sec-filing-sections.md`와 원문 섹션을 같이 읽어야 한다.
- `Debt proxy`는 회사별 부채 태그 차이가 있어 순현금/순부채의 완전한 정의가 아니다. 10-K 주석에서 debt, lease, cash equivalents 정의를 확인해야 한다.
- Capex는 SEC 태그상 현금 유출액을 양수로 기록하는 경우를 기준으로 FCF = 영업현금흐름 - Capex로 계산했다.
