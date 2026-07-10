# DI Satellite Equity Decision Prep

- Run date: `2026-07-11`
- Candidate manifest: [[_report/di/candidates/core-satellite-candidates.yaml|core-satellite-candidates.yaml]]
- Research root: `_report/di/research`
- Decision input file: [[_report/private/di/satellite-decision-inputs.yaml|satellite-decision-inputs.yaml]]
- Queue scope: `primary_queue`
- Row filter: `all`
- Interpretation: pre-decision checklist only; no buy, sell, hold, or order intent is generated
- Order intent generated: `false`

## Summary

| Metric | Value |
| --- | ---: |
| Candidates checked | 6 |
| Ready for checked decision | 6 |
| Needs prep | 0 |

## Candidate Prep State

| Queue | Symbol | Name | Status | Research state | Required before decision.md | Safe next action |
| --- | --- | --- | --- | --- | --- | --- |
| `primary_queue` | `MSFT` | Microsoft | `ready_for_checked_decision` | present: financials.md+thesis.md+valuation.md+decision.md; pending: none | - | review checked decision.md and watchlist promotion separately; no order intent |
| `primary_queue` | `GOOGL` | Alphabet | `ready_for_checked_decision` | present: financials.md+thesis.md+valuation.md; pending: decision.md | - | write checked decision.md with no order intent |
| `primary_queue` | `AMZN` | Amazon | `ready_for_checked_decision` | present: financials.md+thesis.md+valuation.md; pending: decision.md | - | write checked decision.md with no order intent |
| `primary_queue` | `META` | Meta Platforms | `ready_for_checked_decision` | present: financials.md+thesis.md+valuation.md; pending: decision.md | - | write checked decision.md with no order intent |
| `primary_queue` | `NVDA` | NVIDIA | `ready_for_checked_decision` | present: financials.md+thesis.md+valuation.md; pending: decision.md | - | write checked decision.md with no order intent |
| `primary_queue` | `AVGO` | Broadcom | `ready_for_checked_decision` | present: financials.md+thesis.md+valuation.md; pending: decision.md | - | write checked decision.md with no order intent |

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
