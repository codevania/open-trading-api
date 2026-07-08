# Wiki Log

## 2026-06-14

- Created canonical `omx_wiki/` knowledge base.
- Captured Quant implementation status, KRX current Universe v0, and next-session handoff notes.

## 2026-07-05

- Captured GitHub-safe personal asset portfolio policy for debt stabilization, tax reserve handling, and DI core-satellite strategy.
- Captured GitHub-safe DI next-session handoff so discretionary investing can continue from a fresh Codex session.
- Added DI research setup notes, OpenDART/SEC environment examples, and reusable company/ETF research routines.
- Added OpenDART and SEC EDGAR raw collection scripts for repeatable DI company research.
- Added a DI core ETF and US tech satellite candidate manifest plus a Markdown comparison generator.
- Added a DI candidate evidence gate to block watchlist promotion until required research evidence exists.
- Added a DI ETF source-page collector so official issuer evidence can be preserved before candidate fields are filled.
- Tightened the DI candidate evidence gate so empty stock templates and unchecked decision notes cannot pass watchlist promotion.
- Verified official source URLs for `360750` and `360200`, and left `379800` unresolved pending a confirmed KODEX detail page.
- Added an SEC filing-summary renderer for satellite equity source-readiness checks.
- Generated SEC filing summaries for primary U.S. satellite equities: `MSFT`, `GOOGL`, `AMZN`, `META`, `NVDA`, and `AVGO`.
- Added SEC primary filing document collection and source maps for the primary U.S. satellite equity queue.
- Added SEC filing section maps for primary U.S. satellite equities so thesis work can start from Business, Risk Factors, and MD&A raw text.
- Generated SEC companyfacts financial summaries for primary U.S. satellite equities.
- Drafted the first MSFT satellite-equity thesis from SEC filing sections and companyfacts financial evidence.
- Drafted the GOOGL satellite-equity thesis with advertising, Google Cloud, AI capex, and regulatory risk evidence.
- Drafted the AMZN satellite-equity thesis with AWS, retail advertising, capex, FCF, and regulatory risk evidence.
- Drafted the META satellite-equity thesis with FoA advertising, AI monetization, Reality Labs losses, capex, and regulatory risk evidence.
- Drafted the NVDA satellite-equity thesis with Data Center AI infrastructure, Blackwell, customer concentration, supply chain, and export-control risk evidence.
- Drafted the AVGO satellite-equity thesis with custom AI silicon, Ethernet networking, VMware/VCF software, customer concentration, debt, and integration risk evidence.
- Added a DI satellite-equity decision-prep report so primary queue stocks stay blocked until valuation, ETF overlap, tax/account route, position sizing, add/trim rules, and source freshness inputs are checked.
- Tightened the DI candidate evidence gate so satellite equities also require `valuation.md` before watchlist or active position review.
- Updated valuation and decision templates to match the satellite decision-prep gate, and tightened placeholder filtering so TODO-heavy valuation notes cannot pass promotion.
- Tightened the DI satellite decision-prep report so copied TODO-heavy valuation templates still remain pending before `decision.md`.
- Added a gitignored DI satellite decision-input path and example template so account route, sizing, overlap, and freshness checks stay separate from the public candidate manifest.
- Drafted the first MSFT valuation note from local SEC financials, SEC share-count data, and the latest located market close, while keeping ETF overlap, tax/account route, and position sizing blocked in private decision inputs.
- Drafted the GOOGL valuation note from local SEC financials, SEC share-count data, and the latest located market close, with share-class, capex, regulatory, ETF overlap, tax/account route, and sizing caveats left gated before decision.
- Drafted the AMZN valuation note from local SEC financials, SEC share-count data, and the latest located market close, with AWS/AI capex, FCF normalization, debt/lease review, ETF overlap, tax/account route, and sizing caveats left gated before decision.
- Drafted the META valuation note from local SEC financials, diluted-share proxy data, and the latest located market close, with AI capex, Reality Labs losses, share-count refresh, commitment review, ETF overlap, tax/account route, and sizing caveats left gated before decision.
- Drafted the NVDA valuation note from local SEC financials, SEC share-count data, and the latest located market close, with customer concentration, export-control, supply-chain, product-transition, ETF overlap, tax/account route, and sizing caveats left gated before decision.
- Drafted the AVGO valuation note from local SEC financials, SEC share-count data, the latest located market close, and a post-price Apple supply-deal event source, with debt, customer concentration, VMware conversion, custom AI silicon, ETF overlap, tax/account route, and sizing caveats left gated before decision.

## 2026-07-09

- Expanded the gitignored DI satellite decision-input example to cover every primary U.S. satellite equity candidate and added a test that keeps it aligned with the public candidate manifest.
- Added a DI ETF overlap input template and calculator so official ETF holding weights plus private ETF portfolio weights can feed the `etf_overlap_checked` blocker without exposing account details.
- Linked the ETF overlap checker into the ETF and company research routines so future DI sessions can resume the blocker-clearing flow from the repo docs.
- Added a DI ETF holdings collector and source-status report: QQQ is wired to the official Invesco holdings API, while VOO/VTI/VT remain manual official-source checks until a stable Vanguard holdings endpoint is confirmed.
