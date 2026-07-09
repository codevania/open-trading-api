# DI Candidate Evidence Gate

- Run date: `2026-07-10`
- Candidate manifest: [[_report/di/candidates/core-satellite-candidates.yaml|core-satellite-candidates.yaml]]
- Research root: `_report/di/research`
- Row filter: `all`
- Interpretation: readiness gate only; no buy or order intent is generated
- Order intent generated: `false`

## Summary

| Metric | Value |
| --- | ---: |
| Candidates checked | 17 |
| Ready for next review | 0 |
| Hold | 17 |

## Gate Results

| Section | Symbol | Name | Status | Missing evidence | Next action |
| --- | --- | --- | --- | --- | --- |
| `core_etfs` | `VOO` | Vanguard S&P 500 ETF | `hold` | `tax_account_fit`, `expense_ratio` | fill issuer, fee, NAV, distribution, tax, and account evidence |
| `core_etfs` | `VTI` | Vanguard Total Stock Market ETF | `hold` | `tax_account_fit`, `expense_ratio` | fill issuer, fee, NAV, distribution, tax, and account evidence |
| `core_etfs` | `VT` | Vanguard Total World Stock ETF | `hold` | `tax_account_fit`, `expense_ratio` | fill issuer, fee, NAV, distribution, tax, and account evidence |
| `korea_listed_etfs_to_verify` | `360750` | TIGER US S&P500 | `hold` | `currency_hedge`, `distribution_policy`, `tax_account_fit`, `expense_ratio` | fill issuer, fee, NAV, distribution, tax, and account evidence |
| `korea_listed_etfs_to_verify` | `360200` | ACE US S&P500 | `hold` | `currency_hedge`, `distribution_policy`, `tax_account_fit`, `expense_ratio` | fill issuer, fee, NAV, distribution, tax, and account evidence |
| `korea_listed_etfs_to_verify` | `379800` | KODEX US S&P500TR | `hold` | `source_url`, `currency_hedge`, `distribution_policy`, `tax_account_fit`, `expense_ratio` | fill issuer, fee, NAV, distribution, tax, and account evidence |
| `satellite_etfs_to_verify` | `QQQ` | Invesco QQQ Trust | `hold` | `tax_account_fit`, `expense_ratio` | fill issuer, fee, NAV, distribution, tax, and account evidence |
| `satellite_equities.primary_queue` | `MSFT` | Microsoft | `hold` | `research decision.md` | collect filings and write thesis/valuation/decision notes |
| `satellite_equities.primary_queue` | `GOOGL` | Alphabet | `hold` | `research decision.md` | collect filings and write thesis/valuation/decision notes |
| `satellite_equities.primary_queue` | `AMZN` | Amazon | `hold` | `research decision.md` | collect filings and write thesis/valuation/decision notes |
| `satellite_equities.primary_queue` | `META` | Meta Platforms | `hold` | `research decision.md` | collect filings and write thesis/valuation/decision notes |
| `satellite_equities.primary_queue` | `NVDA` | NVIDIA | `hold` | `research decision.md` | collect filings and write thesis/valuation/decision notes |
| `satellite_equities.primary_queue` | `AVGO` | Broadcom | `hold` | `research decision.md` | collect filings and write thesis/valuation/decision notes |
| `satellite_equities.secondary_queue` | `AAPL` | Apple | `hold` | `research sec-filing-summary.md`, `research sec-filing-documents.md`, `research sec-filing-sections.md`, `research financials.md`, `research thesis.md`, `research valuation.md`, `research decision.md` | collect filings and write thesis/valuation/decision notes |
| `satellite_equities.secondary_queue` | `TSM` | Taiwan Semiconductor Manufacturing | `hold` | `research sec-filing-summary.md`, `research sec-filing-documents.md`, `research sec-filing-sections.md`, `research financials.md`, `research thesis.md`, `research valuation.md`, `research decision.md` | collect filings and write thesis/valuation/decision notes |
| `satellite_equities.secondary_queue` | `ASML` | ASML Holding | `hold` | `research sec-filing-summary.md`, `research sec-filing-documents.md`, `research sec-filing-sections.md`, `research financials.md`, `research thesis.md`, `research valuation.md`, `research decision.md` | collect filings and write thesis/valuation/decision notes |
| `satellite_equities.secondary_queue` | `AMD` | Advanced Micro Devices | `hold` | `research sec-filing-summary.md`, `research sec-filing-documents.md`, `research sec-filing-sections.md`, `research financials.md`, `research thesis.md`, `research valuation.md`, `research decision.md` | collect filings and write thesis/valuation/decision notes |

## Promotion Rules

- ETF candidates stay out of [[_report/di/watchlist.yaml|_report/di/watchlist.yaml]] until issuer, cost, NAV/liquidity, distribution, tax, and account evidence are filled.
- Stock candidates stay out of active position review until SEC/DART source evidence, primary filing document and section maps, `financials.md`, `thesis.md`, `valuation.md`, and `decision.md` exist.
- A `ready_*` status means research process readiness only, not a recommendation to buy.
