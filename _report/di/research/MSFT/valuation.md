# MSFT Valuation

## Metadata

- Symbol: `MSFT`
- Company: Microsoft
- Prepared on: `2026-07-09`
- Base currency: `USD`
- Source date: `2026-07-08`
- Interpretation: pre-decision valuation draft only; no buy, sell, hold, or order intent is generated.
- Order intent generated: `false`

## Source Snapshot

- Local financial source: `_report/di/research/MSFT/financials.md`
- Local filing source: `_report/di/research/MSFT/sec-filing-summary.md`
- SEC filing sources: latest 10-Q filed `2026-04-29`, latest 10-K filed `2025-07-30`
- Latest market price source located: MarketWatch data-news article dated `2026-07-07`, reporting MSFT close at `$388.84`
- Share count source: SEC companyfacts `EntityCommonStockSharesOutstanding`, `7,428,434,704` shares as of `2026-04-23`, filed `2026-04-29`

## Market Snapshot

| Item | Value | Source / note |
| --- | ---: | --- |
| Latest located close | `$388.84` | MarketWatch, `2026-07-07` close |
| Shares outstanding | `7.428B` | SEC companyfacts, `2026-04-23` |
| Market cap | `$2.888T` | price x shares |
| Cash and short-term investments | `$78.3B` | SEC companyfacts summary, `2026-03-31` |
| Debt proxy | `$40.3B` | SEC companyfacts long-term debt proxy, `2026-03-31` |
| Net cash proxy | `$38.0B` | cash and investments minus debt proxy |
| Enterprise value proxy | `$2.850T` | market cap minus net cash proxy |

## Current Multiples

| Metric | FY2025 basis | Latest-quarter annualized basis | Note |
| --- | ---: | ---: | --- |
| P/E | `28.4x` | `22.7x` | LQA net income was unusually strong; use with caution |
| EV / Revenue | `10.1x` | `8.6x` | LQA annualizes the `2026-03-31` quarter |
| EV / EBIT | `22.2x` | `18.6x` | EBIT proxy is operating income |
| EV / FCF | `39.8x` | `45.1x` | LQA FCF is depressed by heavy capex |
| FCF yield | `2.48%` | `2.19%` | FCF = operating cash flow minus capex |

## Scenario Range

| Scenario | Key assumptions to test | Valuation read | Main risk |
| --- | --- | --- | --- |
| Bull | Azure/AI demand remains high, Microsoft 365 Copilot monetization compounds, operating margin stays mid-40s, capex starts converting into durable FCF | Current price can be reasonable if normalized earnings and FCF grow faster than capex for several years | Paying a premium before AI infrastructure returns are visible |
| Base | Revenue growth stays strong but normalizes, capex remains elevated, FCF margin recovers only gradually from FY2025 pressure | Current price looks like a quality-compounder price, not an obvious bargain | Limited margin of safety if growth slows |
| Bear | Azure growth decelerates, AI capex stays high, Microsoft Cloud margin compresses, OpenAI/regulatory/security issues create drag | Multiple contraction risk is material because FCF yield is low | Downside can arrive before accounting earnings weaken |

## Reverse DCF / Expectation Check

- The current price uses a FY2025 P/E of about `28x` and an EV/FCF multiple near `40x`.
- The market is giving Microsoft credit for high-quality recurring revenue, Azure/AI growth, and durable enterprise software margins.
- The weak point is cash conversion: FY2025 FCF margin fell to `25.4%` from `30.2%` in FY2024 because capex rose faster than operating cash flow.
- A reasonable decision note needs an explicit view on whether AI infrastructure capex becomes high-return growth investment or persistent FCF dilution.
- This draft uses scenario framing only. A fuller reverse DCF should be added before a checked `decision.md`.

## ETF Overlap

- Core ETF overlap has not been calculated in this tracked note.
- Satellite ETF overlap has not been calculated in this tracked note.
- MSFT is likely already present in S&P 500, total-market, and Nasdaq-100 style exposures; exact weights must be checked from issuer holdings before a position decision.
- Record the actual overlap check in [[_report/private/di/satellite-decision-inputs.yaml|satellite-decision-inputs.yaml]] before writing `decision.md`.

## Tax And Account Route

- Account route is not recorded in this tracked note because it may be personal portfolio information.
- Korean tax treatment for U.S. direct holdings, domestic-listed U.S. equity ETFs, ISA, pension, and IRP routes must be checked separately.
- Record the selected route in [[_report/private/di/satellite-decision-inputs.yaml|satellite-decision-inputs.yaml]] before writing `decision.md`.

## Position Sizing

- First lot size is not recorded in this tracked note.
- Maximum single-name weight is not recorded in this tracked note.
- Add/trim rules are not recorded in this tracked note.
- Sizing must be set after ETF overlap and total satellite-equity exposure are checked.

## Source Freshness

- Latest SEC filing used: `2026-04-29` 10-Q for period ended `2026-03-31`.
- Latest annual filing used: `2025-07-30` 10-K for fiscal year ended `2025-06-30`.
- Latest price located: `2026-07-07` close at `$388.84`.
- ETF holdings source date: not recorded in this tracked note.
- Tax/account source date: not recorded in this tracked note.

## Decision Handoff

- Valuation conclusion: MSFT remains a high-quality candidate, but the current price requires confidence in sustained Azure/AI growth and eventual FCF recovery after heavy capex.
- Required follow-up before `decision.md`: current price refresh, ETF overlap, tax/account route, maximum position size, add/trim rule, and explicit reverse DCF assumptions.
- Invalidation link from `thesis.md`: watch Azure growth, Microsoft Cloud margin, FCF margin, AI capex return, OpenAI dependency, regulatory/security issues, and customer trust.

## Sources

- `_report/di/research/MSFT/financials.md`
- `_report/di/research/MSFT/thesis.md`
- `_report/di/research/MSFT/sec-filing-summary.md`
- `_report/raw/2026/2026-07-08/sec/MSFT/companyfacts.raw.json`
- SEC 10-Q: `https://www.sec.gov/Archives/edgar/data/789019/000119312526191507/msft-20260331.htm`
- SEC 10-K: `https://www.sec.gov/Archives/edgar/data/789019/000095017025100235/msft-20250630.htm`
- MarketWatch data-news source for latest located close: `https://www.marketwatch.com/data-news/snap-inc-stock-underperforms-tuesday-when-compared-to-competitors-b46041f0-b7c0068764fe`
