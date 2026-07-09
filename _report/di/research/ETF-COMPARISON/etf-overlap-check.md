# DI ETF Overlap Check

- Run date: `2026-07-10`
- Candidate manifest: `_report/di/candidates/core-satellite-candidates.yaml`
- ETF overlap input file: `_report/private/di/etf-overlap-inputs.yaml`
- Queue scope: `primary_queue`
- Portfolio weight context: `research_target_scenario_not_actual_holdings`
- Interpretation: overlap-prep only; no buy, sell, hold, or order intent is generated
- Order intent generated: `false`
- Formula: `portfolio ETF weight * ETF holding weight / 100 = portfolio overlap percentage points`

## Summary

| Metric | Value |
| --- | ---: |
| Candidates checked | 6 |
| Ready for private decision input | 6 |
| Needs overlap inputs | 0 |

## Candidate Overlap State

| Queue | Symbol | Name | Status | ETF holding weights | Portfolio overlap estimate | Missing before etf_overlap_checked | Safe next action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `primary_queue` | `MSFT` | Microsoft | `ready_for_private_decision_input` | `VOO=5.14%`, `VTI=4.60%`, `VT=2.82%`, `QQQ=4.63%` | `4.39pp` | - | copy overlap summary into private satellite-decision-inputs.yaml |
| `primary_queue` | `GOOGL` | Alphabet | `ready_for_private_decision_input` | `VOO=3.41%`, `VTI=3.05%`, `VT=1.89%`, `QQQ=3.43%` | `2.96pp` | - | copy overlap summary into private satellite-decision-inputs.yaml |
| `primary_queue` | `AMZN` | Amazon | `ready_for_private_decision_input` | `VOO=4.07%`, `VTI=3.60%`, `VT=2.19%`, `QQQ=4.24%` | `3.52pp` | - | copy overlap summary into private satellite-decision-inputs.yaml |
| `primary_queue` | `META` | Meta Platforms | `ready_for_private_decision_input` | `VOO=2.13%`, `VTI=1.90%`, `VT=1.16%`, `QQQ=2.92%` | `1.92pp` | - | copy overlap summary into private satellite-decision-inputs.yaml |
| `primary_queue` | `NVDA` | NVIDIA | `ready_for_private_decision_input` | `VOO=7.89%`, `VTI=6.70%`, `VT=4.17%`, `QQQ=7.64%` | `6.75pp` | - | copy overlap summary into private satellite-decision-inputs.yaml |
| `primary_queue` | `AVGO` | Broadcom | `ready_for_private_decision_input` | `VOO=3.26%`, `VTI=2.91%`, `VT=1.74%`, `QQQ=2.82%` | `2.76pp` | - | copy overlap summary into private satellite-decision-inputs.yaml |

## Input Rules

- Use official issuer holdings or factsheet data and record `as_of`, `source_url`, and `coverage` for every ETF checked.
- Put personal ETF portfolio weights only in the gitignored private input file.
- Use `0` for an ETF that is deliberately not held, rather than leaving the field blank.
- For `GOOGL`, confirm whether the ETF source separates `GOOGL` and `GOOG` share classes before copying the result into a decision input.
