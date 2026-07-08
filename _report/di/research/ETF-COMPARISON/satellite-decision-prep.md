# DI Satellite Equity Decision Prep

- Run date: `2026-07-09`
- Candidate manifest: `_report/di/candidates/core-satellite-candidates.yaml`
- Research root: `_report/di/research`
- Decision input file: `_report/private/di/satellite-decision-inputs.yaml`
- Queue scope: `primary_queue`
- Interpretation: pre-decision checklist only; no buy, sell, hold, or order intent is generated
- Order intent generated: `false`

## Summary

| Metric | Value |
| --- | ---: |
| Candidates checked | 6 |
| Ready for checked decision | 0 |
| Needs prep | 6 |

## Candidate Prep State

| Queue | Symbol | Name | Status | Research state | Required before decision.md | Safe next action |
| --- | --- | --- | --- | --- | --- | --- |
| `primary_queue` | `MSFT` | Microsoft | `needs_decision_inputs` | present: financials.md+thesis.md+valuation.md; pending: decision.md | `latest_price`, `valuation_range`, `reverse_dcf_or_scenario`, `etf_overlap`, `tax_account_route`, `max_position_size`, `add_trim_rule`, `source_freshness` | fill valuation, overlap, tax/account, sizing, and freshness inputs before decision.md |
| `primary_queue` | `GOOGL` | Alphabet | `needs_decision_inputs` | present: financials.md+thesis.md; pending: valuation.md+decision.md | `valuation.md`, `latest_price`, `valuation_range`, `reverse_dcf_or_scenario`, `etf_overlap`, `tax_account_route`, `max_position_size`, `add_trim_rule`, `source_freshness` | fill valuation, overlap, tax/account, sizing, and freshness inputs before decision.md |
| `primary_queue` | `AMZN` | Amazon | `needs_decision_inputs` | present: financials.md+thesis.md; pending: valuation.md+decision.md | `valuation.md`, `latest_price`, `valuation_range`, `reverse_dcf_or_scenario`, `etf_overlap`, `tax_account_route`, `max_position_size`, `add_trim_rule`, `source_freshness` | fill valuation, overlap, tax/account, sizing, and freshness inputs before decision.md |
| `primary_queue` | `META` | Meta Platforms | `needs_decision_inputs` | present: financials.md+thesis.md; pending: valuation.md+decision.md | `valuation.md`, `latest_price`, `valuation_range`, `reverse_dcf_or_scenario`, `etf_overlap`, `tax_account_route`, `max_position_size`, `add_trim_rule`, `source_freshness` | fill valuation, overlap, tax/account, sizing, and freshness inputs before decision.md |
| `primary_queue` | `NVDA` | NVIDIA | `needs_decision_inputs` | present: financials.md+thesis.md; pending: valuation.md+decision.md | `valuation.md`, `latest_price`, `valuation_range`, `reverse_dcf_or_scenario`, `etf_overlap`, `tax_account_route`, `max_position_size`, `add_trim_rule`, `source_freshness` | fill valuation, overlap, tax/account, sizing, and freshness inputs before decision.md |
| `primary_queue` | `AVGO` | Broadcom | `needs_decision_inputs` | present: financials.md+thesis.md; pending: valuation.md+decision.md | `valuation.md`, `latest_price`, `valuation_range`, `reverse_dcf_or_scenario`, `etf_overlap`, `tax_account_route`, `max_position_size`, `add_trim_rule`, `source_freshness` | fill valuation, overlap, tax/account, sizing, and freshness inputs before decision.md |

## Manual Inputs Required Before decision.md

- `latest_price`: latest market price, currency, and timestamp.
- `valuation_range`: base/bull/bear range or comparable multiple range tied to current price.
- `reverse_dcf_or_scenario`: explicit assumptions needed to justify the current price.
- `etf_overlap`: overlap with core ETF and satellite ETF holdings so single-name exposure is not double-counted.
- `tax_account_route`: taxable account, ISA, pension, or IRP route and the expected tax/reporting treatment.
- `max_position_size`: maximum single-name weight before adding the first lot.
- `add_trim_rule`: written rule for adding, trimming, or stopping additional buys.
- `source_freshness`: date of latest filing, facts, price, holdings, and tax/account checks.

## Promotion Boundary

- This report does not create or update `decision.md`.
- A candidate remains blocked until required inputs are recorded and a checked decision note is written.
- A ready status means process readiness to write a decision note, not a recommendation to buy.
