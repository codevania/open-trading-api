# AVGO Valuation

## Metadata

- Symbol: `AVGO`
- Company: Broadcom
- Prepared on: `2026-07-09`
- Base currency: `USD`
- Source date: `2026-07-08`
- Interpretation: pre-decision valuation draft only; no buy, sell, hold, or order intent is generated.
- Order intent generated: `false`

## Source Snapshot

- Local financial source: `_report/di/research/AVGO/financials.md`
- Local filing source: `_report/di/research/AVGO/sec-filing-summary.md`
- SEC filing sources: latest 10-Q filed `2026-06-09`, latest 10-K filed `2025-12-18`
- Latest market price source located: MarketWatch data-news article dated `2026-07-07`, reporting AVGO close at `$370.78`
- Share count source: SEC companyfacts `EntityCommonStockSharesOutstanding`, `4,757,580,198` shares as of `2026-05-29`, filed `2026-06-09`
- Post-price event source located: Investopedia article dated `2026-07-08` reporting a new Apple chip supply agreement with Broadcom; refresh price before `decision.md`.
- Fiscal-year caveat: Broadcom's fiscal year differs from the calendar year. FY2025 ended `2025-11-02`, and the latest 10-Q period ended `2026-05-03`.
- Cash/debt caveat: the local XBRL summary uses cash and cash equivalents for liquidity and `DebtLongtermAndShorttermCombinedAmount` as a debt proxy. Debt maturity, interest expense, leases, and commitments need note review before `decision.md`.

## Market Snapshot

| Item | Value | Source / note |
| --- | ---: | --- |
| Latest located close | `$370.78` | MarketWatch, `2026-07-07` close |
| Shares outstanding | `4.758B` | SEC companyfacts, `2026-05-29` |
| Market cap | `$1.764T` | price x shares |
| Cash and cash equivalents | `$19.6B` | SEC companyfacts summary, `2026-05-03` |
| Debt proxy | `$66.7B` | SEC companyfacts debt proxy, `2026-05-03` |
| Net cash proxy | `-$47.1B` | cash and cash equivalents minus debt proxy |
| Enterprise value proxy | `$1.811T` | market cap plus net debt proxy |

## Current Multiples

| Metric | FY2025 basis | Latest-quarter annualized basis | Note |
| --- | ---: | ---: | --- |
| P/E | `76.4x` | `47.4x` | LQA annualizes the `2026-05-03` quarter |
| EV / Revenue | `28.3x` | `20.4x` | Revenue multiple embeds AI custom silicon and software expectations |
| EV / EBIT | `71.0x` | `42.0x` | EBIT proxy is operating income |
| EV / FCF | `67.3x` | `44.3x` | LQA FCF uses estimated standalone Q2 FCF from H1 minus Q1 cash-flow data |
| FCF yield | `1.52%` | `2.32%` | FCF = operating cash flow minus capex |

## Scenario Range

| Scenario | Key assumptions to test | Valuation read | Main risk |
| --- | --- | --- | --- |
| Bull | Custom AI accelerator and Ethernet networking demand stays strong, Apple and hyperscaler design wins expand, VMware Cloud Foundation cash flow scales, and debt paydown continues without constraining capital returns | Current price can work if AI/custom silicon growth and infrastructure software durability justify a much higher multiple than Broadcom's historical semiconductor cycle | Paying peak AI/custom-silicon expectations before revenue durability is proven |
| Base | AI and networking growth remain strong but normalize, VMware integration supports cash flow, and debt declines gradually | Current price is a premium valuation that needs sustained Q2-like margin and FCF conversion | Limited margin of safety if growth expectations reset |
| Bear | Custom AI design wins disappoint, top customers or distributors reduce orders, VMware transition weakens retention, or debt/refinancing costs constrain capital returns | Downside can be material because FY2025 EV/FCF is above `60x` and net debt remains high | The stock can re-rate before reported revenue weakens |

## Reverse DCF / Expectation Check

- The current price uses a FY2025 P/E of about `76x`, EV/EBIT of about `71x`, and EV/FCF near `67x`.
- Latest-quarter annualized multiples are lower because the `2026-05-03` quarter had stronger revenue, operating margin, and profit. The FCF calculation uses estimated standalone Q2 cash flow from H1 minus Q1 because the companyfacts cash-flow tags are cumulative.
- The market is paying for Broadcom as an AI infrastructure supplier with custom accelerators, Ethernet networking, optical/connectivity components, and VMware infrastructure software cash flow.
- The weak point is balance-sheet and concentration risk. Net debt remains material, and the thesis note flags a large semiconductor distributor and top end customers as important concentration exposures.
- The July 8 Apple supply agreement may change near-term sentiment, but this draft's price source predates that news. Refresh price and event impact before `decision.md`.
- A reasonable decision note needs explicit stress tests for custom AI silicon demand, VMware conversion, debt paydown, top-customer concentration, and semiconductor-cycle normalization.
- This draft uses scenario framing only. A fuller reverse DCF should be added before a checked `decision.md`.

## ETF Overlap

- Core ETF overlap has not been calculated in this tracked note.
- Satellite ETF overlap has not been calculated in this tracked note.
- AVGO is likely already present in S&P 500, total-market, Nasdaq-100, semiconductor, AI, and broad technology/growth exposures; exact weights must be checked from issuer holdings before a position decision.
- Record the actual overlap check in `_report/private/di/satellite-decision-inputs.yaml` before writing `decision.md`.

## Tax And Account Route

- Account route is not recorded in this tracked note because it may be personal portfolio information.
- Korean tax treatment for U.S. direct holdings, domestic-listed U.S. equity ETFs, ISA, pension, and IRP routes must be checked separately.
- Record the selected route in `_report/private/di/satellite-decision-inputs.yaml` before writing `decision.md`.

## Position Sizing

- First lot size is not recorded in this tracked note.
- Maximum single-name weight is not recorded in this tracked note.
- Add/trim rules are not recorded in this tracked note.
- Sizing must be set after ETF overlap and total satellite-equity exposure are checked.

## Source Freshness

- Latest SEC filing used: `2026-06-09` 10-Q for period ended `2026-05-03`.
- Latest annual filing used: `2025-12-18` 10-K for fiscal year ended `2025-11-02`.
- Latest price located: `2026-07-07` close at `$370.78`.
- Post-price event located: `2026-07-08` Apple chip supply agreement article; price must be refreshed.
- ETF holdings source date: not recorded in this tracked note.
- Tax/account source date: not recorded in this tracked note.

## Decision Handoff

- Valuation conclusion: AVGO remains a high-quality AI infrastructure and infrastructure-software satellite candidate, but the current valuation requires confidence that AI custom silicon, Ethernet networking, VMware cash flow, and Apple/hyperscaler design wins can offset net debt, customer concentration, and semiconductor cyclicality.
- Required follow-up before `decision.md`: current price refresh after the Apple supply-deal news, ETF overlap, tax/account route, maximum position size, add/trim rule, debt maturity and interest review, top-customer concentration stress test, VMware conversion check, custom AI design-win durability check, and explicit reverse DCF assumptions.
- Invalidation link from `thesis.md`: watch custom AI accelerator/XPU revenue, AI networking demand, VMware Cloud Foundation conversion, debt paydown, interest expense, top distributor and top end-customer concentration, supply-chain/geopolitical risks, and semiconductor-cycle weakness.

## Sources

- `_report/di/research/AVGO/financials.md`
- `_report/di/research/AVGO/thesis.md`
- `_report/di/research/AVGO/sec-filing-summary.md`
- `_report/raw/2026/2026-07-08/sec/AVGO/companyfacts.raw.json`
- SEC 10-Q: `https://www.sec.gov/Archives/edgar/data/1730168/000173016826000054/avgo-20260503.htm`
- SEC 10-K: `https://www.sec.gov/Archives/edgar/data/1730168/000173016825000121/avgo-20251102.htm`
- MarketWatch data-news source for latest located close: `https://www.marketwatch.com/data-news/skyworks-solutions-inc-stock-underperforms-tuesday-when-compared-to-competitors-e98d7f85-81a2e60b93d6`
- Investopedia post-price event source: `https://www.investopedia.com/broadcom-stock-jumps-on-new-usd30-billion-deal-to-supply-chips-to-apple-avgo-aapl-12014008`
