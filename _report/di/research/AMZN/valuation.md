# AMZN Valuation

## Metadata

- Symbol: `AMZN`
- Company: Amazon
- Prepared on: `2026-07-09`
- Base currency: `USD`
- Source date: `2026-07-08`
- Interpretation: pre-decision valuation draft only; no buy, sell, hold, or order intent is generated.
- Order intent generated: `false`

## Source Snapshot

- Local financial source: `_report/di/research/AMZN/financials.md`
- Local filing source: `_report/di/research/AMZN/sec-filing-summary.md`
- SEC filing sources: latest 10-Q filed `2026-04-30`, latest 10-K filed `2026-02-06`
- Latest market price source located: MarketWatch data-news article dated `2026-07-07`, reporting AMZN close at `$245.98`
- Share count source: SEC companyfacts `CommonStockSharesOutstanding`, `10,754,000,000` shares as of `2026-03-31`, filed `2026-04-30`
- Cash/debt caveat: the local XBRL summary uses cash and cash equivalents for liquidity and `LongTermDebt` as a debt proxy. Lease, finance obligation, marketable securities, and commitment details need 10-K note review before `decision.md`.

## Market Snapshot

| Item | Value | Source / note |
| --- | ---: | --- |
| Latest located close | `$245.98` | MarketWatch, `2026-07-07` close |
| Shares outstanding | `10.754B` | SEC companyfacts, `2026-03-31` |
| Market cap | `$2.645T` | price x shares |
| Cash and cash equivalents | `$101.8B` | SEC companyfacts summary, `2026-03-31` |
| Debt proxy | `$122.6B` | SEC companyfacts long-term debt proxy, `2026-03-31` |
| Net cash proxy | `-$20.8B` | cash and cash equivalents minus debt proxy |
| Enterprise value proxy | `$2.666T` | market cap plus net debt proxy |

## Current Multiples

| Metric | FY2025 basis | Latest-quarter annualized basis | Note |
| --- | ---: | ---: | --- |
| P/E | `34.0x` | `21.8x` | LQA net income can move with non-operating and seasonal effects |
| EV / Revenue | `3.7x` | `3.7x` | Lower revenue multiple reflects retail scale and lower consolidated margin |
| EV / EBIT | `33.3x` | `27.9x` | EBIT proxy is operating income |
| EV / FCF | `346.2x` | not meaningful | LQA FCF is negative after heavy capex |
| FCF yield | `0.29%` | `-2.75%` | FCF = operating cash flow minus capex |

## Scenario Range

| Scenario | Key assumptions to test | Valuation read | Main risk |
| --- | --- | --- | --- |
| Bull | AWS growth stays high, AI infrastructure capex converts into durable AWS revenue, advertising and third-party seller economics keep retail margin expanding, and capex intensity normalizes | Current price can work if operating income compounds and FCF rebounds sharply after the investment cycle | Paying before FCF conversion is visible |
| Base | AWS and advertising grow, retail operating leverage continues, but AI/data-center capex remains elevated for several years | Current price is not cheap on operating income and is extremely demanding on current FCF | Valuation depends more on future FCF recovery than current cash generation |
| Bear | AWS growth slows while capex remains high, retail logistics costs absorb advertising gains, and regulatory or seller-platform pressure raises compliance costs | Multiple compression risk is material because current FCF yield is near zero | The market can reprice the stock as capex-heavy infrastructure rather than a high-FCF platform |

## Reverse DCF / Expectation Check

- The current price uses a FY2025 P/E of about `34x`, EV/EBIT of about `33x`, and XBRL-based EV/FCF above `300x`.
- The market is paying for AWS, advertising, third-party seller services, Prime retention, logistics scale, and the possibility that AI capex becomes high-return infrastructure rather than permanent cash drag.
- The weak point is free cash flow. FY2025 XBRL-based FCF was only `$7.7B`, and Q1 2026 annualized FCF is negative because capex exceeded operating cash flow.
- The company-defined FCF in the thesis note is higher than the XBRL simple calculation, but it is still low relative to the current market cap.
- A reasonable decision note needs a clear answer to one question: when does the current capex wave turn into recurring AWS/AI operating income and normalized FCF?
- This draft uses scenario framing only. A fuller reverse DCF should be added before a checked `decision.md`.

## ETF Overlap

- Core ETF overlap has not been calculated in this tracked note.
- Satellite ETF overlap has not been calculated in this tracked note.
- AMZN is likely already present in S&P 500, total-market, Nasdaq-100, consumer-discretionary, and broad technology/growth exposures; exact weights must be checked from issuer holdings before a position decision.
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

- Latest SEC filing used: `2026-04-30` 10-Q for period ended `2026-03-31`.
- Latest annual filing used: `2026-02-06` 10-K for fiscal year ended `2025-12-31`.
- Latest price located: `2026-07-07` close at `$245.98`.
- ETF holdings source date: not recorded in this tracked note.
- Tax/account source date: not recorded in this tracked note.

## Decision Handoff

- Valuation conclusion: AMZN remains a high-quality satellite candidate, but the current valuation requires confidence that AWS/AI capex will translate into operating income and normalized FCF. On current FCF, the margin of safety is weak.
- Required follow-up before `decision.md`: current price refresh, 10-K debt/lease/commitment note review, ETF overlap, tax/account route, maximum position size, add/trim rule, capex-normalization assumption, and explicit reverse DCF assumptions.
- Invalidation link from `thesis.md`: watch AWS revenue and operating income, company-defined and XBRL FCF, technology infrastructure capex, advertising and third-party seller growth, fulfillment/shipping costs, and regulatory or litigation pressure.

## Sources

- `_report/di/research/AMZN/financials.md`
- `_report/di/research/AMZN/thesis.md`
- `_report/di/research/AMZN/sec-filing-summary.md`
- `_report/raw/2026/2026-07-08/sec/AMZN/companyfacts.raw.json`
- SEC 10-Q: `https://www.sec.gov/Archives/edgar/data/1018724/000101872426000014/amzn-20260331.htm`
- SEC 10-K: `https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm`
- MarketWatch data-news source for latest located close: `https://www.marketwatch.com/data-news/target-corp-stock-outperforms-competitors-on-strong-trading-day-d30926b5-18148b04e7bd`
