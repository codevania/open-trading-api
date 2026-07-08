# NVDA Valuation

## Metadata

- Symbol: `NVDA`
- Company: NVIDIA
- Prepared on: `2026-07-09`
- Base currency: `USD`
- Source date: `2026-07-08`
- Interpretation: pre-decision valuation draft only; no buy, sell, hold, or order intent is generated.
- Order intent generated: `false`

## Source Snapshot

- Local financial source: `_report/di/research/NVDA/financials.md`
- Local filing source: `_report/di/research/NVDA/sec-filing-summary.md`
- SEC filing sources: latest 10-Q filed `2026-05-20`, latest 10-K filed `2026-02-25`
- Latest market price source located: MarketWatch data-news article dated `2026-07-06`, reporting NVDA close at `$195.55`
- Share count source: SEC companyfacts `EntityCommonStockSharesOutstanding`, `24,200,000,000` shares as of `2026-05-15`, filed `2026-05-20`
- Fiscal-year caveat: NVIDIA's fiscal year differs from the calendar year. FY2026 ended `2026-01-25`, and the `2026-04-26` quarter is FY2027 Q1.
- Cash/debt caveat: the local XBRL summary uses cash and cash equivalents for liquidity and `LongTermDebt` as a debt proxy. Marketable securities, purchase commitments, leases, and supply-chain obligations need note review before `decision.md`.

## Market Snapshot

| Item | Value | Source / note |
| --- | ---: | --- |
| Latest located close | `$195.55` | MarketWatch, `2026-07-06` close |
| Shares outstanding | `24.200B` | SEC companyfacts, `2026-05-15` |
| Market cap | `$4.732T` | price x shares |
| Cash and cash equivalents | `$13.2B` | SEC companyfacts summary, `2026-04-26` |
| Debt proxy | `$8.5B` | SEC companyfacts long-term debt proxy, `2026-04-26` |
| Net cash proxy | `$4.8B` | cash and cash equivalents minus debt proxy |
| Enterprise value proxy | `$4.728T` | market cap minus net cash proxy |

## Current Multiples

| Metric | FY2026 basis | Latest-quarter annualized basis | Note |
| --- | ---: | ---: | --- |
| P/E | `39.4x` | `20.3x` | LQA net income may include tax and non-operating effects |
| EV / Revenue | `21.9x` | `14.5x` | LQA annualizes FY2027 Q1 |
| EV / EBIT | `36.3x` | `22.1x` | EBIT proxy is operating income |
| EV / FCF | `48.9x` | `24.3x` | LQA FCF is extremely strong and should be stress-tested |
| FCF yield | `2.04%` | `4.11%` | FCF = operating cash flow minus capex |

## Scenario Range

| Scenario | Key assumptions to test | Valuation read | Main risk |
| --- | --- | --- | --- |
| Bull | Data Center demand stays supply-constrained, Blackwell and Rubin transitions execute cleanly, networking attach remains high, export restrictions stay manageable, and hyperscaler capex continues | Current price can be reasonable if FY2027 Q1 strength is a durable run-rate rather than a cyclical peak | Assuming current growth and margin can persist without disruption |
| Base | AI infrastructure demand remains strong but growth normalizes, gross margin stays high but below peak, and customer concentration remains elevated | Current price is a premium-quality valuation with less margin of safety if growth slows | Multiple compression if the market shifts from scarcity pricing to normalized semiconductor-cycle pricing |
| Bear | Hyperscaler orders slow, customer ASICs take share, export controls widen, supply-chain bottlenecks disrupt shipments, or product transitions create inventory and warranty charges | Downside can be large because FY2026 EV/FCF is near `49x` and expectations are already high | Strong current earnings may not protect the stock if forward orders weaken |

## Reverse DCF / Expectation Check

- The current price uses a FY2026 P/E of about `39x`, EV/EBIT of about `36x`, and EV/FCF near `49x`.
- The latest-quarter annualized multiples are much lower because FY2027 Q1 revenue, operating income, and FCF were exceptionally strong. This draft does not treat one quarter as a full-cycle normalized run-rate.
- The market is paying for NVIDIA as the core AI infrastructure supplier: GPUs, networking, rack-scale systems, CUDA, and accelerated-computing software.
- The weak point is concentration and cycle risk. A small number of direct customers represented a large share of FY2027 Q1 revenue, and the thesis depends on continued hyperscaler and AI-cloud capex.
- A reasonable decision note needs explicit stress tests for Data Center growth normalization, gross margin compression, export controls, customer concentration, and custom-ASIC substitution.
- This draft uses scenario framing only. A fuller reverse DCF should be added before a checked `decision.md`.

## ETF Overlap

- Core ETF overlap has not been calculated in this tracked note.
- Satellite ETF overlap has not been calculated in this tracked note.
- NVDA is likely already a large weight in S&P 500, total-market, Nasdaq-100, semiconductor, AI, and broad technology/growth exposures; exact weights must be checked from issuer holdings before a position decision.
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

- Latest SEC filing used: `2026-05-20` 10-Q for period ended `2026-04-26`.
- Latest annual filing used: `2026-02-25` 10-K for fiscal year ended `2026-01-25`.
- Latest price located: `2026-07-06` close at `$195.55`.
- ETF holdings source date: not recorded in this tracked note.
- Tax/account source date: not recorded in this tracked note.

## Decision Handoff

- Valuation conclusion: NVDA remains the highest-purity AI infrastructure satellite candidate, but the current valuation requires confidence that FY2027 Q1 strength is not near a cyclical peak and that customer concentration, export controls, supply-chain constraints, and product-transition risk stay manageable.
- Required follow-up before `decision.md`: current price refresh, ETF overlap, tax/account route, maximum position size, add/trim rule, customer concentration stress test, export-control scenario, supply-chain commitment review, product-transition risk review, and explicit reverse DCF assumptions.
- Invalidation link from `thesis.md`: watch Data Center revenue growth, gross margin, operating margin, direct customer concentration, H20/H200 and China/export-control updates, Blackwell/Rubin transition quality, inventory or warranty charges, supply-chain commitments, and hyperscaler capex signals.

## Sources

- `_report/di/research/NVDA/financials.md`
- `_report/di/research/NVDA/thesis.md`
- `_report/di/research/NVDA/sec-filing-summary.md`
- `_report/raw/2026/2026-07-08/sec/NVDA/companyfacts.raw.json`
- SEC 10-Q: `https://www.sec.gov/Archives/edgar/data/1045810/000104581026000052/nvda-20260426.htm`
- SEC 10-K: `https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm`
- MarketWatch data-news source for latest located close: `https://www.marketwatch.com/data-news/texas-instruments-inc-stock-outperforms-competitors-on-strong-trading-day-0061ac06-1ba29957097c`
