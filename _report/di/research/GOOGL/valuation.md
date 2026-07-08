# GOOGL Valuation

## Metadata

- Symbol: `GOOGL`
- Company: Alphabet
- Prepared on: `2026-07-09`
- Base currency: `USD`
- Source date: `2026-07-08`
- Interpretation: pre-decision valuation draft only; no buy, sell, hold, or order intent is generated.
- Order intent generated: `false`

## Source Snapshot

- Local financial source: `_report/di/research/GOOGL/financials.md`
- Local filing source: `_report/di/research/GOOGL/sec-filing-summary.md`
- SEC filing sources: latest 10-Q filed `2026-04-30`, latest 10-K filed `2026-02-05`
- Latest market price source located: MarketWatch data-news article dated `2026-07-07`, reporting GOOGL close at `$367.03`
- Share count source: SEC companyfacts `CommonStockSharesOutstanding`, `12,116,000,000` shares as of `2026-03-31`, filed `2026-04-30`
- Share-class caveat: this note uses the GOOGL Class A close against Alphabet's combined common share count as a practical proxy. Refresh the GOOGL/GOOG class treatment before writing `decision.md`.

## Market Snapshot

| Item | Value | Source / note |
| --- | ---: | --- |
| Latest located close | `$367.03` | MarketWatch, `2026-07-07` close |
| Shares outstanding | `12.116B` | SEC companyfacts, `2026-03-31` |
| Market cap | `$4.447T` | price x shares |
| Cash and short-term investments | `$126.8B` | SEC companyfacts summary, `2026-03-31` |
| Debt proxy | `$77.5B` | SEC companyfacts long-term debt proxy, `2026-03-31` |
| Net cash proxy | `$49.3B` | cash and investments minus debt proxy |
| Enterprise value proxy | `$4.398T` | market cap minus net cash proxy |

## Current Multiples

| Metric | FY2025 basis | Latest-quarter annualized basis | Note |
| --- | ---: | ---: | --- |
| P/E | `33.6x` | `17.8x` | LQA net income is distorted upward by equity securities gains |
| EV / Revenue | `10.9x` | `10.0x` | LQA annualizes the `2026-03-31` quarter |
| EV / EBIT | `34.1x` | `27.7x` | EBIT proxy is operating income |
| EV / FCF | `60.0x` | `108.9x` | LQA FCF is depressed by heavy capex |
| FCF yield | `1.65%` | `0.91%` | FCF = operating cash flow minus capex |

## Scenario Range

| Scenario | Key assumptions to test | Valuation read | Main risk |
| --- | --- | --- | --- |
| Bull | Search monetization stays resilient through AI interface changes, Google Cloud keeps scaling, TPU/Gemini investments create durable cost and product advantages, and regulatory remedies remain manageable | Current price can work only if operating profit growth compounds for years and capex begins to convert into higher future FCF | Paying a premium while capex and regulatory risks are still rising |
| Base | Search and YouTube remain strong, Cloud continues growing, but AI capex stays elevated and FCF recovery is slower than revenue growth | Current price looks demanding and needs explicit confidence in AI return on invested capital | Limited margin of safety if growth normalizes |
| Bear | AI search changes reduce ad monetization, antitrust remedies weaken distribution or ad-tech economics, Cloud commitments pressure margins, and Other Bets losses remain material | Multiple compression risk is high because FY2025 EV/FCF is already near `60x` | Downside can appear through valuation compression before revenue declines |

## Reverse DCF / Expectation Check

- The current price uses a FY2025 P/E of about `34x` and an EV/FCF multiple near `60x`.
- The market is valuing Alphabet as more than an ad business: it is paying for Search durability, YouTube scale, Cloud growth, Gemini/TPU optionality, and long-run AI infrastructure returns.
- The weak point is cash conversion. FY2025 FCF margin fell to `18.2%` from `20.8%` in FY2024, and the latest-quarter annualized FCF multiple is above `100x` because capex rose sharply.
- The latest-quarter P/E looks optically cheap because net income included non-operating equity securities gains. This draft does not treat that LQA P/E as a clean operating signal.
- A reasonable decision note needs an explicit view on whether AI changes increase Search/YouTube monetization, protect Cloud economics, and justify sustained capex.
- This draft uses scenario framing only. A fuller reverse DCF should be added before a checked `decision.md`.

## ETF Overlap

- Core ETF overlap has not been calculated in this tracked note.
- Satellite ETF overlap has not been calculated in this tracked note.
- GOOGL is likely already present in S&P 500, total-market, Nasdaq-100, and broad technology or communication-services exposures; exact weights must be checked from issuer holdings before a position decision.
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
- Latest annual filing used: `2026-02-05` 10-K for fiscal year ended `2025-12-31`.
- Latest price located: `2026-07-07` close at `$367.03`.
- ETF holdings source date: not recorded in this tracked note.
- Tax/account source date: not recorded in this tracked note.

## Decision Handoff

- Valuation conclusion: GOOGL remains a high-quality satellite candidate, but the current price already discounts durable Search, Cloud, AI, and FCF recovery. The margin of safety is not obvious on FY2025 FCF.
- Required follow-up before `decision.md`: current price refresh, GOOGL/GOOG share-class treatment, ETF overlap, tax/account route, maximum position size, add/trim rule, antitrust update, and explicit reverse DCF assumptions.
- Invalidation link from `thesis.md`: watch Search and YouTube ad monetization, Google Cloud growth and margin, AI capex return, DOJ and ad-tech remedies, TPU/data-center commitments, and Other Bets losses.

## Sources

- `_report/di/research/GOOGL/financials.md`
- `_report/di/research/GOOGL/thesis.md`
- `_report/di/research/GOOGL/sec-filing-summary.md`
- `_report/raw/2026/2026-07-08/sec/GOOGL/companyfacts.raw.json`
- SEC 10-Q: `https://www.sec.gov/Archives/edgar/data/1652044/000165204426000048/goog-20260331.htm`
- SEC 10-K: `https://www.sec.gov/Archives/edgar/data/1652044/000165204426000018/goog-20251231.htm`
- MarketWatch data-news source for latest located close: `https://www.marketwatch.com/data-news/news-corp-cl-a-stock-outperforms-competitors-on-strong-trading-day-87503289-a53c01deae73`
