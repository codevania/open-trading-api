# DI ETF Holdings Source Status

- Run date: `2026-07-09`
- Candidate manifest: [[_report/di/candidates/core-satellite-candidates.yaml|core-satellite-candidates.yaml]]
- Raw root: `_report/raw`
- Interpretation: official holdings evidence only; no buy, sell, hold, or order intent is generated
- Order intent generated: `false`
- Private portfolio ETF weights stay only in [[_report/private/di/etf-overlap-inputs.yaml|etf-overlap-inputs.yaml]].

## Source Coverage

| ETF | Provider | Source state | Live fetch | Official source | Holdings API | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| `VOO` | `vanguard` | `manual_official_source_required` | `no` | https://investor.vanguard.com/investment-products/etfs/profile/voo | - | official profile page exists, but a stable holdings API was not confirmed |
| `VTI` | `vanguard` | `manual_official_source_required` | `no` | https://investor.vanguard.com/investment-products/etfs/profile/vti | - | official profile page exists, but a stable holdings API was not confirmed |
| `VT` | `vanguard` | `manual_official_source_required` | `no` | https://investor.vanguard.com/investment-products/etfs/profile/vt | - | official profile page exists, but a stable holdings API was not confirmed |
| `QQQ` | `invesco` | `confirmed_api` | `yes` | https://www.invesco.com/qqq-etf/en/about.html | https://dng-api.invesco.com/cache/v1/accounts/en_US/shareclasses/QQQ/holdings/fund?idType=ticker&interval=monthly&productType=ETF | official page exposes data-holding-api for QQQ holdings |

## Collected Candidate Weights

| ETF | Status | As of | Coverage | MSFT | GOOGL | AMZN | META | NVDA | AVGO | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `VOO` | `skipped_unresolved_source` | - | - | - | - | - | - | - | - | official profile page exists, but a stable holdings API was not confirmed |
| `VTI` | `skipped_unresolved_source` | - | - | - | - | - | - | - | - | official profile page exists, but a stable holdings API was not confirmed |
| `VT` | `skipped_unresolved_source` | - | - | - | - | - | - | - | - | official profile page exists, but a stable holdings API was not confirmed |
| `QQQ` | `collected` | 2026-07-07 | full | 4.6313% | 3.4273% | 4.2426% | 2.9228% | 7.6412% | 2.8187% | GOOG is reported separately at 3.180934%; decide whether to combine Alphabet classes in the private overlap input. |

## Next Use

1. Copy only official holding weights into the gitignored overlap input file.
2. Add private ETF portfolio weights there, not in this public report.
3. Rerun [[scripts/di_etf_overlap_check.py|di_etf_overlap_check.py]] before marking `etf_overlap_checked`.
