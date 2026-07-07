# AMZN SEC Filing Summary

- Run date: `2026-07-08`
- Generated at: `2026-07-08T03:35:44+09:00`
- Raw dir: `_report/raw/2026/2026-07-08/sec/AMZN`
- Source: SEC EDGAR raw JSON collected for DI research
- Interpretation: source-readiness summary only; no buy or order intent is generated
- Order intent generated: `false`

## Entity

| Field | Value |
| --- | --- |
| Ticker | `AMZN` |
| CIK | `0001018724` |
| Company | AMAZON COM INC |
| Companyfacts entity | AMAZON COM INC |
| Taxonomies | `dei, us-gaap, ecd, ffd` |

## Latest Core Filings

| Form | Filing date | Report date | Accession | Primary document | SEC URL |
| --- | --- | --- | --- | --- | --- |
| `8-K` | 2026-06-12 | 2026-06-12 | `0001104659-26-073562` | tm2613616d5_8k.htm | https://www.sec.gov/Archives/edgar/data/1018724/000110465926073562/tm2613616d5_8k.htm |
| `8-K` | 2026-06-10 | 2026-06-08 | `0001104659-26-072140` | tm2613616d4_8k.htm | https://www.sec.gov/Archives/edgar/data/1018724/000110465926072140/tm2613616d4_8k.htm |
| `10-Q` | 2026-04-30 | 2026-03-31 | `0001018724-26-000014` | amzn-20260331.htm | https://www.sec.gov/Archives/edgar/data/1018724/000101872426000014/amzn-20260331.htm |
| `10-K` | 2026-02-06 | 2025-12-31 | `0001018724-26-000004` | amzn-20251231.htm | https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm |
| `10-Q` | 2025-10-31 | 2025-09-30 | `0001018724-25-000123` | amzn-20250930.htm | https://www.sec.gov/Archives/edgar/data/1018724/000101872425000123/amzn-20250930.htm |
| `10-K` | 2025-02-07 | 2024-12-31 | `0001018724-25-000004` | amzn-20241231.htm | https://www.sec.gov/Archives/edgar/data/1018724/000101872425000004/amzn-20241231.htm |

## XBRL Concept Snapshot

| Concept | Status | Latest value | Unit | FY | FP | Period end | Filed | Form |
| --- | --- | ---: | --- | --- | --- | --- | --- | --- |
| `RevenueFromContractWithCustomerExcludingAssessedTax` | `ok` | 181,519,000,000 | USD | 2026 | Q1 | 2026-03-31 | 2026-04-30 | 10-Q |
| `Revenues` | `no_fact` | - | - | - | - | - | - | - |
| `OperatingIncomeLoss` | `ok` | 23,852,000,000 | USD | 2026 | Q1 | 2026-03-31 | 2026-04-30 | 10-Q |
| `NetIncomeLoss` | `ok` | 30,255,000,000 | USD | 2026 | Q1 | 2026-03-31 | 2026-04-30 | 10-Q |
| `Assets` | `ok` | 916,630,000,000 | USD | 2026 | Q1 | 2026-03-31 | 2026-04-30 | 10-Q |
| `Liabilities` | `no_fact` | - | - | - | - | - | - | - |
| `StockholdersEquity` | `ok` | 441,914,000,000 | USD | 2026 | Q1 | 2026-03-31 | 2026-04-30 | 10-Q |
| `NetCashProvidedByUsedInOperatingActivities` | `ok` | 26,032,000,000 | USD | 2026 | Q1 | 2026-03-31 | 2026-04-30 | 10-Q |
| `PaymentsToAcquirePropertyPlantAndEquipment` | `stale` | 1,861,000,000 | USD | 2017 | Q1 | 2017-03-31 | 2017-04-28 | 10-Q |

## Next Actions

1. Read the latest 10-K Business, Risk Factors, and MD&A sections before writing `thesis.md`.
2. Use the latest 10-Q and 8-K filings to check whether the thesis is stale.
3. Convert XBRL facts into `financials.md` only after checking fiscal period alignment and units.
4. Keep the candidate on `hold` until `thesis.md` and `decision.md` contain filled evidence and a checked decision.
