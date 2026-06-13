# Market Regime Scan

## Metadata

- Date: 2026-06-13
- Reference market: Mixed
- Reference session: 2026-06-12 US close and 2026-06-12 KRX close
- Written at: 2026-06-13 KST
- Author: Codex
- Data sources:
  - MarketWatch June 12, 2026 US market live coverage: `https://www.marketwatch.com/livecoverage/stock-market-today-s-p-500-nasdaq-dow-jones-spacex-ipo-first-trade-us-iran-peace-deal`
  - Business Insider June 13, 2026 KOSPI report: `https://www.businessinsider.com/kospi-stock-index-price-south-korea-markets-samsung-sk-hynix-2026-6`
  - MarketWatch June 9, 2026 VIX note: `https://www.marketwatch.com/livecoverage/stock-market-today-dow-jones-s-p-500-nasdaq-technology-shares-oil-prices-israel-iran-pause-strikes/card/vix-pulls-a-sharp-u-turn-climbs-to-2-month-high-DO1Im07hOHOFUykF6dPm`
- Raw data storage: not saved; public web reference only
- Perplexity/Chrome usage: not used

## 1. Regime Summary

- Regime: `event-driven`, `high-volatility`
- Confidence: low
- One-line summary: US and Korean equities rebounded, but the move followed a sharp volatility shock and was tied to event headlines rather than a stable Quant regime.
- Strategy impact today: keep `001-strategy-universe-momentum` and `002-strategy-universe-short-term-reversal` as paper Signal Candidates only.
- Most important uncertainty: no saved broker/API raw for index levels, breadth, rates, FX, and KRX sector breadth.

## 2. Core Market Data

| Category | Metric | Value | Change | Source | Interpretation |
| --- | --- | ---: | ---: | --- | --- |
| Index/Futures | S&P 500 / Dow / Nasdaq | not captured as raw | up on 2026-06-12 | MarketWatch | broad US rebound, but not enough for a rule change |
| Index/Futures | KOSPI | not captured as raw | closed up about `4.6%` after intraday surge | Business Insider | strong rebound after a volatile week |
| Volatility | VIX | `21.80` intraday reference on 2026-06-09 | sharp intraday rise | MarketWatch | volatility shock remains relevant |
| Rates/FX | US 10Y or USD/KRW | not captured | not captured | - | `data-insufficient` |
| Breadth | Sector Breadth or advancers/decliners | not captured | not captured | - | `data-insufficient` |
| Leadership | Leading sector/theme | AI / semiconductor rebound | positive on 2026-06-12 | Business Insider | leadership is concentrated in AI-sensitive names |
| Liquidity | Trading value / volume proxy | not captured | not captured | - | `data-insufficient` |

## 3. Breadth & Leadership

- Upside leadership: AI and semiconductor-linked large caps, based on the KOSPI rebound report.
- Downside leadership: not captured.
- Large-cap concentration: likely high, but not proven without saved breadth data.
- Defensive/cyclical split: not captured.
- Top Gainers/Losers check: required before using this scan in a daily report.
- Heatmap or Sector Map interpretation: not captured in a reproducible raw file.

## 4. News/Event Filter

| Event | Source | Market Impact | Related Strategy | Need to Verify |
| --- | --- | --- | --- | --- |
| US market rebound and weekly gains | MarketWatch | risk appetite improved into the June 12 close | `001-strategy-universe-momentum` | exact index closes and breadth |
| KOSPI rebound after a sharp weekly drawdown | Business Insider | KRX recovered but remained volatile | `001`, `002` | KRX official index close and sector breadth |
| VIX spike earlier in the week | MarketWatch | volatility regime remains elevated | all paper Strategies | latest VIX close and 5D path |
| Geopolitical / oil headline changes | MarketWatch | event-driven risk filter | all paper Strategies | crude, FX, and rate reaction |

- Macro Event: geopolitical headlines and oil price reaction.
- Earnings/Event: not checked.
- Policy/Regulation: not checked.
- Geopolitical/Supply Shock: active filter.
- Crypto or alternative asset shock: not checked.

## 5. Risk Filter

- VIX spike: yes, based on the 2026-06-09 VIX reference.
- Index/Futures simultaneous selloff: happened earlier in the week, but exact stored index path is missing.
- Sector concentration risk: yes, AI and semiconductor leadership appears dominant.
- USD/KRW or rate shock: `data-insufficient`.
- Volume-backed sell pressure: `data-insufficient`.
- Risk judgment: `caution`.

## 6. Strategy Impact

| Strategy | Signal State | Regime Impact | Required Action | Invalidator |
| --- | --- | --- | --- | --- |
| `001-strategy-universe-momentum` | Signal Candidate only | event-driven rebound can make Momentum look better than it is | track only; no Position change | Point-in-Time failure, volatility reversal, unsaved raw |
| `002-strategy-universe-short-term-reversal` | Candidate spec only | high volatility can create reversal candidates but also falling-knife risk | no execution; wait for raw and Bias Control | structural decline, liquidity failure, unsaved raw |

- Does Regime pause Strategy execution: yes for real execution; no for paper observation.
- Position or cash review required: no live Position exists.
- Stress Period flag for future Backtest: yes, mark week of 2026-06-08 as high-volatility / event-driven.
- Daily report sentence: "Quant Signal Candidates remain paper-only because the market is event-driven and volatility remains elevated."

## 7. Data Quality

- Freshness: web references are current to June 12-13, 2026.
- Source reliability: public financial media; not a saved broker/API raw set.
- Cross-check: limited to web-source agreement on rebound plus volatility.
- Missing data: exact official index closes, KRX breadth, sector breadth, rates, FX, trading value, latest VIX close.
- Login/paid data dependency: none for this scan, but raw-grade verification is still missing.
- Human recheck required: official KRX index close and KIS/broker raw capture.

## 8. Next Checks

1. Save official or broker/API raw for KOSPI, KOSDAQ, S&P 500, Nasdaq, VIX, USD/KRW, and US 10Y.
2. Add KRX sector breadth or at least advancers/decliners before treating this as a repeatable regime input.
3. Keep Market Regime separate from Entry/Exit Signal until Backtest proves a filter rule.
