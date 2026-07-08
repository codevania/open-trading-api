# META Valuation

## Metadata

- Symbol: `META`
- Company: Meta Platforms
- Prepared on: `2026-07-09`
- Base currency: `USD`
- Source date: `2026-07-08`
- Interpretation: pre-decision valuation draft only; no buy, sell, hold, or order intent is generated.
- Order intent generated: `false`

## Source Snapshot

- Local financial source: `_report/di/research/META/financials.md`
- Local filing source: `_report/di/research/META/sec-filing-summary.md`
- SEC filing sources: latest 10-Q filed `2026-04-30`, latest 10-K filed `2026-01-29`
- Latest market price source located: MarketWatch data-news article dated `2026-07-06`, reporting META close at `$600.29`
- Share count source: SEC companyfacts `WeightedAverageNumberOfDilutedSharesOutstanding`, `2,564,000,000` shares for quarter ended `2026-03-31`, filed `2026-04-30`
- Share-count caveat: this note uses diluted weighted-average shares as a market-cap proxy because no clean point-in-time common shares outstanding tag was found in the local companyfacts file. Refresh the share-count treatment before `decision.md`.
- Cash/debt caveat: the local XBRL summary uses cash and cash equivalents for liquidity and `LongTermDebtNoncurrent` as a debt proxy. Lease, commitment, and marketable-securities details need 10-Q or 10-K note review before `decision.md`.

## Market Snapshot

| Item | Value | Source / note |
| --- | ---: | --- |
| Latest located close | `$600.29` | MarketWatch, `2026-07-06` close |
| Diluted shares proxy | `2.564B` | SEC companyfacts, quarter ended `2026-03-31` |
| Market cap proxy | `$1.539T` | price x diluted shares proxy |
| Cash and cash equivalents | `$23.4B` | SEC companyfacts summary, `2026-03-31` |
| Debt proxy | `$58.7B` | SEC companyfacts long-term debt proxy, `2026-03-31` |
| Net cash proxy | `-$35.3B` | cash and cash equivalents minus debt proxy |
| Enterprise value proxy | `$1.574T` | market cap plus net debt proxy |

## Current Multiples

| Metric | FY2025 basis | Latest-quarter annualized basis | Note |
| --- | ---: | ---: | --- |
| P/E | `25.4x` | `14.4x` | LQA net income may benefit from tax and non-operating effects |
| EV / Revenue | `7.8x` | `7.0x` | LQA annualizes the `2026-03-31` quarter |
| EV / EBIT | `18.9x` | `17.2x` | EBIT proxy is operating income |
| EV / FCF | `34.2x` | `29.8x` | FCF remains positive despite AI capex |
| FCF yield | `3.00%` | `3.43%` | FCF = operating cash flow minus capex |

## Scenario Range

| Scenario | Key assumptions to test | Valuation read | Main risk |
| --- | --- | --- | --- |
| Bull | AI improves ad targeting, ranking, creator tools, and messaging monetization; FoA engagement stays strong; Reality Labs losses remain tolerable; AI capex creates durable ad and compute returns | Current price can be reasonable if high-margin FoA profit keeps funding capex while FCF remains positive | Underestimating how much AI capex and commitments can keep rising |
| Base | Advertising growth remains healthy, FoA margin stays high, but AI infrastructure spending absorbs much of the incremental cash flow | Current price is closer to a fair quality-compounder valuation than an obvious bargain | Limited upside if capex keeps expanding faster than monetization |
| Bear | Ad growth slows, privacy or youth-safety regulation weakens targeting and measurement, Reality Labs losses continue, and AI infrastructure returns lag spending | Multiple compression risk rises because the market is paying for AI-funded growth while capex is structurally higher | FCF can disappoint even when revenue and operating income look strong |

## Reverse DCF / Expectation Check

- The current price uses a FY2025 P/E of about `25x`, EV/EBIT of about `19x`, and EV/FCF near `34x`.
- Compared with the other U.S. technology satellite candidates already drafted, META has stronger current FCF support than AMZN and GOOGL, but its capex guide and long-dated AI commitments create a large reinvestment risk.
- The weak point is not the core advertising engine today. The weak point is whether AI infrastructure, Reality Labs, and long-term commitments keep consuming cash faster than FoA monetization improves.
- The latest-quarter annualized P/E looks optically lower than FY2025 because Q1 2026 net income includes tax effects noted in the thesis data-limit memo. Operating income and FCF are better anchors.
- A reasonable decision note needs explicit assumptions for FoA ad growth, AI-driven monetization, Reality Labs loss tolerance, and capex normalization.
- This draft uses scenario framing only. A fuller reverse DCF should be added before a checked `decision.md`.

## ETF Overlap

- Core ETF overlap has not been calculated in this tracked note.
- Satellite ETF overlap has not been calculated in this tracked note.
- META is likely already present in S&P 500, total-market, Nasdaq-100, communication-services, and broad growth/technology exposures; exact weights must be checked from issuer holdings before a position decision.
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
- Latest annual filing used: `2026-01-29` 10-K for fiscal year ended `2025-12-31`.
- Latest price located: `2026-07-06` close at `$600.29`.
- ETF holdings source date: not recorded in this tracked note.
- Tax/account source date: not recorded in this tracked note.

## Decision Handoff

- Valuation conclusion: META remains a high-quality satellite candidate with real current FCF support, but the current decision depends on whether FoA advertising and AI monetization can absorb the rising AI/RL capex burden.
- Required follow-up before `decision.md`: current price refresh, share-count refresh, debt/lease/commitment note review, ETF overlap, tax/account route, maximum position size, add/trim rule, capex-normalization assumption, Reality Labs loss tolerance, and explicit reverse DCF assumptions.
- Invalidation link from `thesis.md`: watch ad revenue growth, ad impressions, average price per ad, FoA operating income, Reality Labs losses, AI infrastructure capex, long-term commitments, privacy/youth-safety regulation, and engagement trends.

## Sources

- `_report/di/research/META/financials.md`
- `_report/di/research/META/thesis.md`
- `_report/di/research/META/sec-filing-summary.md`
- `_report/raw/2026/2026-07-08/sec/META/companyfacts.raw.json`
- SEC 10-Q: `https://www.sec.gov/Archives/edgar/data/1326801/000162828026028526/meta-20260331.htm`
- SEC 10-K: `https://www.sec.gov/Archives/edgar/data/1326801/000162828026003942/meta-20251231.htm`
- MarketWatch data-news source for latest located close: `https://www.marketwatch.com/data-news/alphabet-inc-cl-c-stock-outperforms-competitors-on-strong-trading-day-4a652d95-771556787c19`
