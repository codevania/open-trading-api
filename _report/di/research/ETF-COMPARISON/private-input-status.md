# DI Private Input Status

- Run date: `2026-07-11`
- Candidate manifest: [[_report/di/candidates/core-satellite-candidates.yaml|core-satellite-candidates.yaml]]
- ETF overlap input file: [[_report/private/di/etf-overlap-inputs.yaml|etf-overlap-inputs.yaml]]
- Satellite decision input file: [[_report/private/di/satellite-decision-inputs.yaml|satellite-decision-inputs.yaml]]
- Queue scope: `primary_queue`
- Row filter: `all`
- Interpretation: private input completeness only; values are masked.
- Sensitive values printed: `false`
- Order intent generated: `false`

## Summary

| Metric | Value |
| --- | ---: |
| Fields checked | 80 |
| Filled fields | 53 |
| Missing fields | 27 |

## Summary By Area

| Area | Filled | Missing | Total |
| --- | ---: | ---: | ---: |
| ETF holding weight | 24 | 0 | 24 |
| ETF portfolio weight | 4 | 0 | 4 |
| ETF source meta | 4 | 0 | 4 |
| Satellite decision input | 21 | 27 | 48 |

## Field Status

| Area | Symbol | Field | Status | Safe next action |
| --- | --- | --- | --- | --- |
| ETF portfolio weight | `VOO` | `portfolio_etf_weights.VOO` | `filled` | no action; value is present but masked |
| ETF source meta | `VOO` | `etf_holdings.VOO.source_meta` | `filled` | no action; value is present but masked |
| ETF holding weight | `VOO:MSFT` | `etf_holdings.VOO.holdings.MSFT` | `filled` | no action; value is present but masked |
| ETF holding weight | `VOO:GOOGL` | `etf_holdings.VOO.holdings.GOOGL` | `filled` | no action; value is present but masked |
| ETF holding weight | `VOO:AMZN` | `etf_holdings.VOO.holdings.AMZN` | `filled` | no action; value is present but masked |
| ETF holding weight | `VOO:META` | `etf_holdings.VOO.holdings.META` | `filled` | no action; value is present but masked |
| ETF holding weight | `VOO:NVDA` | `etf_holdings.VOO.holdings.NVDA` | `filled` | no action; value is present but masked |
| ETF holding weight | `VOO:AVGO` | `etf_holdings.VOO.holdings.AVGO` | `filled` | no action; value is present but masked |
| ETF portfolio weight | `VTI` | `portfolio_etf_weights.VTI` | `filled` | no action; value is present but masked |
| ETF source meta | `VTI` | `etf_holdings.VTI.source_meta` | `filled` | no action; value is present but masked |
| ETF holding weight | `VTI:MSFT` | `etf_holdings.VTI.holdings.MSFT` | `filled` | no action; value is present but masked |
| ETF holding weight | `VTI:GOOGL` | `etf_holdings.VTI.holdings.GOOGL` | `filled` | no action; value is present but masked |
| ETF holding weight | `VTI:AMZN` | `etf_holdings.VTI.holdings.AMZN` | `filled` | no action; value is present but masked |
| ETF holding weight | `VTI:META` | `etf_holdings.VTI.holdings.META` | `filled` | no action; value is present but masked |
| ETF holding weight | `VTI:NVDA` | `etf_holdings.VTI.holdings.NVDA` | `filled` | no action; value is present but masked |
| ETF holding weight | `VTI:AVGO` | `etf_holdings.VTI.holdings.AVGO` | `filled` | no action; value is present but masked |
| ETF portfolio weight | `VT` | `portfolio_etf_weights.VT` | `filled` | no action; value is present but masked |
| ETF source meta | `VT` | `etf_holdings.VT.source_meta` | `filled` | no action; value is present but masked |
| ETF holding weight | `VT:MSFT` | `etf_holdings.VT.holdings.MSFT` | `filled` | no action; value is present but masked |
| ETF holding weight | `VT:GOOGL` | `etf_holdings.VT.holdings.GOOGL` | `filled` | no action; value is present but masked |
| ETF holding weight | `VT:AMZN` | `etf_holdings.VT.holdings.AMZN` | `filled` | no action; value is present but masked |
| ETF holding weight | `VT:META` | `etf_holdings.VT.holdings.META` | `filled` | no action; value is present but masked |
| ETF holding weight | `VT:NVDA` | `etf_holdings.VT.holdings.NVDA` | `filled` | no action; value is present but masked |
| ETF holding weight | `VT:AVGO` | `etf_holdings.VT.holdings.AVGO` | `filled` | no action; value is present but masked |
| ETF portfolio weight | `QQQ` | `portfolio_etf_weights.QQQ` | `filled` | no action; value is present but masked |
| ETF source meta | `QQQ` | `etf_holdings.QQQ.source_meta` | `filled` | no action; value is present but masked |
| ETF holding weight | `QQQ:MSFT` | `etf_holdings.QQQ.holdings.MSFT` | `filled` | no action; value is present but masked |
| ETF holding weight | `QQQ:GOOGL` | `etf_holdings.QQQ.holdings.GOOGL` | `filled` | no action; value is present but masked |
| ETF holding weight | `QQQ:AMZN` | `etf_holdings.QQQ.holdings.AMZN` | `filled` | no action; value is present but masked |
| ETF holding weight | `QQQ:META` | `etf_holdings.QQQ.holdings.META` | `filled` | no action; value is present but masked |
| ETF holding weight | `QQQ:NVDA` | `etf_holdings.QQQ.holdings.NVDA` | `filled` | no action; value is present but masked |
| ETF holding weight | `QQQ:AVGO` | `etf_holdings.QQQ.holdings.AVGO` | `filled` | no action; value is present but masked |
| Satellite decision input | `MSFT` | `inputs.MSFT.latest_price_checked` | `filled` | no action; value is present but masked |
| Satellite decision input | `MSFT` | `inputs.MSFT.valuation_range_checked` | `filled` | no action; value is present but masked |
| Satellite decision input | `MSFT` | `inputs.MSFT.reverse_dcf_checked` | `filled` | no action; value is present but masked |
| Satellite decision input | `MSFT` | `inputs.MSFT.etf_overlap_checked` | `filled` | no action; value is present but masked |
| Satellite decision input | `MSFT` | `inputs.MSFT.tax_account_route` | `missing` | record taxable, ISA, pension, or IRP route |
| Satellite decision input | `MSFT` | `inputs.MSFT.max_position_size` | `filled` | no action; value is present but masked |
| Satellite decision input | `MSFT` | `inputs.MSFT.add_trim_rule` | `filled` | no action; value is present but masked |
| Satellite decision input | `MSFT` | `inputs.MSFT.source_freshness_checked` | `missing` | record filing, price, holdings, and tax check dates |
| Satellite decision input | `GOOGL` | `inputs.GOOGL.latest_price_checked` | `missing` | record latest price, currency, timestamp, and source |
| Satellite decision input | `GOOGL` | `inputs.GOOGL.valuation_range_checked` | `missing` | record base, bear, and bull valuation range |
| Satellite decision input | `GOOGL` | `inputs.GOOGL.reverse_dcf_checked` | `missing` | record scenario or reverse-DCF assumptions |
| Satellite decision input | `GOOGL` | `inputs.GOOGL.etf_overlap_checked` | `filled` | no action; value is present but masked |
| Satellite decision input | `GOOGL` | `inputs.GOOGL.tax_account_route` | `missing` | record taxable, ISA, pension, or IRP route |
| Satellite decision input | `GOOGL` | `inputs.GOOGL.max_position_size` | `filled` | no action; value is present but masked |
| Satellite decision input | `GOOGL` | `inputs.GOOGL.add_trim_rule` | `filled` | no action; value is present but masked |
| Satellite decision input | `GOOGL` | `inputs.GOOGL.source_freshness_checked` | `missing` | record filing, price, holdings, and tax check dates |
| Satellite decision input | `AMZN` | `inputs.AMZN.latest_price_checked` | `missing` | record latest price, currency, timestamp, and source |
| Satellite decision input | `AMZN` | `inputs.AMZN.valuation_range_checked` | `missing` | record base, bear, and bull valuation range |
| Satellite decision input | `AMZN` | `inputs.AMZN.reverse_dcf_checked` | `missing` | record scenario or reverse-DCF assumptions |
| Satellite decision input | `AMZN` | `inputs.AMZN.etf_overlap_checked` | `filled` | no action; value is present but masked |
| Satellite decision input | `AMZN` | `inputs.AMZN.tax_account_route` | `missing` | record taxable, ISA, pension, or IRP route |
| Satellite decision input | `AMZN` | `inputs.AMZN.max_position_size` | `filled` | no action; value is present but masked |
| Satellite decision input | `AMZN` | `inputs.AMZN.add_trim_rule` | `filled` | no action; value is present but masked |
| Satellite decision input | `AMZN` | `inputs.AMZN.source_freshness_checked` | `missing` | record filing, price, holdings, and tax check dates |
| Satellite decision input | `META` | `inputs.META.latest_price_checked` | `missing` | record latest price, currency, timestamp, and source |
| Satellite decision input | `META` | `inputs.META.valuation_range_checked` | `missing` | record base, bear, and bull valuation range |
| Satellite decision input | `META` | `inputs.META.reverse_dcf_checked` | `missing` | record scenario or reverse-DCF assumptions |
| Satellite decision input | `META` | `inputs.META.etf_overlap_checked` | `filled` | no action; value is present but masked |
| Satellite decision input | `META` | `inputs.META.tax_account_route` | `missing` | record taxable, ISA, pension, or IRP route |
| Satellite decision input | `META` | `inputs.META.max_position_size` | `filled` | no action; value is present but masked |
| Satellite decision input | `META` | `inputs.META.add_trim_rule` | `filled` | no action; value is present but masked |
| Satellite decision input | `META` | `inputs.META.source_freshness_checked` | `missing` | record filing, price, holdings, and tax check dates |
| Satellite decision input | `NVDA` | `inputs.NVDA.latest_price_checked` | `missing` | record latest price, currency, timestamp, and source |
| Satellite decision input | `NVDA` | `inputs.NVDA.valuation_range_checked` | `missing` | record base, bear, and bull valuation range |
| Satellite decision input | `NVDA` | `inputs.NVDA.reverse_dcf_checked` | `missing` | record scenario or reverse-DCF assumptions |
| Satellite decision input | `NVDA` | `inputs.NVDA.etf_overlap_checked` | `filled` | no action; value is present but masked |
| Satellite decision input | `NVDA` | `inputs.NVDA.tax_account_route` | `missing` | record taxable, ISA, pension, or IRP route |
| Satellite decision input | `NVDA` | `inputs.NVDA.max_position_size` | `filled` | no action; value is present but masked |
| Satellite decision input | `NVDA` | `inputs.NVDA.add_trim_rule` | `filled` | no action; value is present but masked |
| Satellite decision input | `NVDA` | `inputs.NVDA.source_freshness_checked` | `missing` | record filing, price, holdings, and tax check dates |
| Satellite decision input | `AVGO` | `inputs.AVGO.latest_price_checked` | `missing` | record latest price, currency, timestamp, and source |
| Satellite decision input | `AVGO` | `inputs.AVGO.valuation_range_checked` | `missing` | record base, bear, and bull valuation range |
| Satellite decision input | `AVGO` | `inputs.AVGO.reverse_dcf_checked` | `missing` | record scenario or reverse-DCF assumptions |
| Satellite decision input | `AVGO` | `inputs.AVGO.etf_overlap_checked` | `filled` | no action; value is present but masked |
| Satellite decision input | `AVGO` | `inputs.AVGO.tax_account_route` | `missing` | record taxable, ISA, pension, or IRP route |
| Satellite decision input | `AVGO` | `inputs.AVGO.max_position_size` | `filled` | no action; value is present but masked |
| Satellite decision input | `AVGO` | `inputs.AVGO.add_trim_rule` | `filled` | no action; value is present but masked |
| Satellite decision input | `AVGO` | `inputs.AVGO.source_freshness_checked` | `missing` | record filing, price, holdings, and tax check dates |

## Privacy Boundary

- This report must show only `filled` or `missing`, never private weights, account routes, account names, or position limits.
- Keep `_report/private/di/` gitignored. Commit this status report only because the values are masked.
- Use this report to decide which private fields to fill before running overlap and decision-prep gates.
