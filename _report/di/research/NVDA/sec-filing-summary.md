# NVDA SEC Filing Summary

- Run date: `2026-07-08`
- Generated at: `2026-07-08T03:35:44+09:00`
- Raw dir: `_report/raw/2026/2026-07-08/sec/NVDA`
- Source: SEC EDGAR raw JSON collected for DI research
- Interpretation: source-readiness summary only; no buy or order intent is generated
- Order intent generated: `false`

## Entity

| Field | Value |
| --- | --- |
| Ticker | `NVDA` |
| CIK | `0001045810` |
| Company | NVIDIA CORP |
| Companyfacts entity | NVIDIA CORP |
| Taxonomies | `dei, invest, us-gaap, srt, ecd, ffd` |

## Latest Core Filings

| Form | Filing date | Report date | Accession | Primary document | SEC URL |
| --- | --- | --- | --- | --- | --- |
| `8-K` | 2026-07-02 | 2026-06-28 | `0001045810-26-000060` | nvda-20260628.htm | https://www.sec.gov/Archives/edgar/data/1045810/000104581026000060/nvda-20260628.htm |
| `8-K` | 2026-06-30 | 2026-06-24 | `0001045810-26-000056` | nvda-20260624.htm | https://www.sec.gov/Archives/edgar/data/1045810/000104581026000056/nvda-20260624.htm |
| `10-Q` | 2026-05-20 | 2026-04-26 | `0001045810-26-000052` | nvda-20260426.htm | https://www.sec.gov/Archives/edgar/data/1045810/000104581026000052/nvda-20260426.htm |
| `10-K` | 2026-02-25 | 2026-01-25 | `0001045810-26-000021` | nvda-20260125.htm | https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm |
| `10-Q` | 2025-11-19 | 2025-10-26 | `0001045810-25-000230` | nvda-20251026.htm | https://www.sec.gov/Archives/edgar/data/1045810/000104581025000230/nvda-20251026.htm |
| `10-K` | 2025-02-26 | 2025-01-26 | `0001045810-25-000023` | nvda-20250126.htm | https://www.sec.gov/Archives/edgar/data/1045810/000104581025000023/nvda-20250126.htm |

## XBRL Concept Snapshot

| Concept | Status | Latest value | Unit | FY | FP | Period end | Filed | Form |
| --- | --- | ---: | --- | --- | --- | --- | --- | --- |
| `RevenueFromContractWithCustomerExcludingAssessedTax` | `stale` | 26,914,000,000 | USD | 2022 | FY | 2022-01-30 | 2022-03-18 | 10-K |
| `Revenues` | `ok` | 81,615,000,000 | USD | 2027 | Q1 | 2026-04-26 | 2026-05-20 | 10-Q |
| `OperatingIncomeLoss` | `ok` | 53,536,000,000 | USD | 2027 | Q1 | 2026-04-26 | 2026-05-20 | 10-Q |
| `NetIncomeLoss` | `ok` | 58,321,000,000 | USD | 2027 | Q1 | 2026-04-26 | 2026-05-20 | 10-Q |
| `Assets` | `ok` | 259,474,000,000 | USD | 2027 | Q1 | 2026-04-26 | 2026-05-20 | 10-Q |
| `Liabilities` | `ok` | 64,000,000,000 | USD | 2027 | Q1 | 2026-04-26 | 2026-05-20 | 10-Q |
| `StockholdersEquity` | `ok` | 195,474,000,000 | USD | 2027 | Q1 | 2026-04-26 | 2026-05-20 | 10-Q |
| `NetCashProvidedByUsedInOperatingActivities` | `ok` | 50,344,000,000 | USD | 2027 | Q1 | 2026-04-26 | 2026-05-20 | 10-Q |
| `PaymentsToAcquirePropertyPlantAndEquipment` | `stale` | 372,000,000 | USD | 2020 | Q2 | 2020-07-26 | 2020-08-19 | 10-Q |

## Next Actions

1. Read the latest 10-K Business, Risk Factors, and MD&A sections before writing `thesis.md`.
2. Use the latest 10-Q and 8-K filings to check whether the thesis is stale.
3. Convert XBRL facts into `financials.md` only after checking fiscal period alignment and units.
4. Keep the candidate on `hold` until `thesis.md` and `decision.md` contain filled evidence and a checked decision.
