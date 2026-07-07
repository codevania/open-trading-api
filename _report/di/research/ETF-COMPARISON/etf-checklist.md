# DI Core ETF and Satellite Candidate Comparison

- Run date: `2026-07-08`
- Candidate manifest: `_report/di/candidates/core-satellite-candidates.yaml`
- Manifest version: `1`
- Interpretation: candidate screening aid only; final buy decisions require a written thesis and tax/account verification

## Portfolio Frame

- Strategy: `debt-stabilized core-satellite`
- Horizon: `5-10 years`
- Status: research queue only, not a buy list

### Priority Order

1. keep tax and short-term cash outside risk assets
2. reduce interest-rate and cash-flow risk first
3. build broad-market ETF core before single-stock satellites
4. add satellite equities only after a written thesis and invalidation rule

### Guardrails

- core_first: `yes`
- satellite_total_limit_policy: `keep small until the process is proven`
- single_name_limit_policy: `start small; do not average down without a fresh thesis`

Excluded from long-term core:
- leveraged ETF
- inverse ETF
- single-theme concentrated ETF
- product with unclear fee or tax treatment

## Core ETF Candidates

| Symbol | Name | Listing | Role | Benchmark | FX hedge | Distribution | Expense | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| VOO | Vanguard S&P 500 ETF | US | US large-cap core | S&P 500 Index | unhedged | distributes | TODO | candidate |
| VTI | Vanguard Total Stock Market ETF | US | total US equity core | CRSP US Total Market Index | unhedged | distributes | TODO | candidate |
| VT | Vanguard Total World Stock ETF | US | global equity core | FTSE Global All Cap Index | unhedged | distributes | TODO | candidate |

## Korea-Listed ETF Verification Queue

| Code | Name | Benchmark | FX hedge | Distribution | Tax/account check | Status |
| --- | --- | --- | --- | --- | --- | --- |
| 360750 | TIGER US S&P500 | S&P 500 Index | verify | verify | check ISA/pension/IRP eligibility and taxable-account treatment | needs_issuer_and_tax_verification |
| 360200 | ACE US S&P500 | S&P 500 Index | verify | verify | check ISA/pension/IRP eligibility and taxable-account treatment | needs_issuer_and_tax_verification |
| 379800 | KODEX US S&P500TR | S&P 500 total-return style index | verify | likely reinvestment/TR style; verify | check ISA/pension/IRP eligibility and taxable-account treatment | needs_issuer_and_tax_verification |

## Satellite ETF Verification Queue

| Symbol | Name | Listing | Role | Benchmark | Tax/account check | Status |
| --- | --- | --- | --- | --- | --- | --- |
| QQQ | Invesco QQQ Trust | US | growth satellite ETF, not broad core | Nasdaq-100 Index | US direct account; Korean tax treatment must be checked | satellite_candidate |

## Satellite Equity Queue

### Primary Queue

| Symbol | Name | Market | Role | Filings | Status | First read |
| --- | --- | --- | --- | --- | --- | --- |
| MSFT | Microsoft | NASDAQ | cloud, enterprise software, AI platform | 10-K, 10-Q, 8-K, XBRL | candidate | Start with revenue growth, operating margin, cloud backlog, capex, and AI monetization risk. |
| GOOGL | Alphabet | NASDAQ | search, ads, cloud, AI | 10-K, 10-Q, 8-K, XBRL | candidate | Watch search share, AI disruption, cloud margin, regulatory risk, and capital returns. |
| AMZN | Amazon | NASDAQ | ecommerce, AWS, advertising, logistics | 10-K, 10-Q, 8-K, XBRL | candidate | Separate retail margin, AWS growth, advertising, capex, and free cash flow. |
| META | Meta Platforms | NASDAQ | social platforms, ads, AI infrastructure | 10-K, 10-Q, 8-K, XBRL | candidate | Track ad growth, engagement, Reality Labs losses, AI capex, and regulatory risk. |
| NVDA | NVIDIA | NASDAQ | AI accelerators and platform ecosystem | 10-K, 10-Q, 8-K, XBRL | candidate | High-quality but valuation/cycle sensitive; require explicit downside scenario before buying. |
| AVGO | Broadcom | NASDAQ | networking semiconductors and infrastructure software | 10-K, 10-Q, 8-K, XBRL | candidate | Track AI networking, VMware integration, debt, margins, and capital allocation. |

### Secondary Queue

| Symbol | Name | Market | Role | Filings | Status | First read |
| --- | --- | --- | --- | --- | --- | --- |
| AAPL | Apple | NASDAQ | devices, services, ecosystem | 10-K, 10-Q, 8-K, XBRL | secondary_candidate | Mature compounder; watch device cycle, China exposure, services growth, and buybacks. |
| TSM | Taiwan Semiconductor Manufacturing | NYSE | advanced foundry | 20-F, 6-K, annual report | secondary_candidate | Foreign issuer/ADR; include geopolitical, FX, and customer concentration risk. |
| ASML | ASML Holding | NASDAQ | lithography equipment | 20-F, 6-K, annual report | secondary_candidate | Foreign issuer/ADR; check order cycle, export controls, and EU tax/dividend handling. |
| AMD | Advanced Micro Devices | NASDAQ | CPUs, GPUs, AI accelerators | 10-K, 10-Q, 8-K, XBRL | secondary_candidate | More competitive/cyclical thesis; compare data-center GPU traction versus NVIDIA. |


## Manual Checks Before Buy

### ETF

- exact index and replication method
- total expense and other implicit costs
- AUM, average trading value, spread, and NAV premium/discount
- distribution policy and dividend tax
- domestic-listed versus US-direct tax and reporting
- ISA, pension, and IRP eligibility

### STOCK

- latest annual and quarterly filings
- 5-year revenue, operating income, free cash flow, debt, dilution, and buyback trend
- valuation range and reverse DCF assumptions
- bear case and invalidation rule
- maximum position size and add/trim rule


## Next Actions

1. Fill issuer page, factsheet, expense, AUM, spread, NAV gap, and distribution fields for each ETF.
2. Compare domestic-listed S&P 500 ETFs against US-direct VOO/VTI/VT using the same tax assumptions.
3. For each satellite stock, run SEC EDGAR collection before writing thesis/valuation/decision notes.
4. Move only approved candidates into `_report/di/watchlist.yaml` after a decision note exists.
