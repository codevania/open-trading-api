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
| `VOO` | `vanguard` | `confirmed_api` | `yes` | https://investor.vanguard.com/investment-products/etfs/profile/voo | https://investor.vanguard.com/vmf/api/voo/portfolio-holding/stock.json | official Vanguard profile app exposes portfolio-holding stock JSON |
| `VTI` | `vanguard` | `confirmed_api` | `yes` | https://investor.vanguard.com/investment-products/etfs/profile/vti | https://investor.vanguard.com/vmf/api/vti/portfolio-holding/stock.json | official Vanguard profile app exposes portfolio-holding stock JSON |
| `VT` | `vanguard` | `confirmed_api` | `yes` | https://investor.vanguard.com/investment-products/etfs/profile/vt | https://investor.vanguard.com/vmf/api/vt/portfolio-holding/stock.json | official Vanguard profile app exposes portfolio-holding stock JSON |
| `QQQ` | `invesco` | `confirmed_api` | `yes` | https://www.invesco.com/qqq-etf/en/about.html | https://dng-api.invesco.com/cache/v1/accounts/en_US/shareclasses/QQQ/holdings/fund?idType=ticker&interval=monthly&productType=ETF | official page exposes data-holding-api for QQQ holdings |

## Collected Candidate Weights

| ETF | Status | As of | Coverage | MSFT | GOOGL | AMZN | META | NVDA | AVGO | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `VOO` | `collected` | 2026-05-31 | full | 5.1400% | 3.4100% | 4.0700% | 2.1300% | 7.8900% | 3.2600% | GOOG is reported separately at 2.710000%; decide whether to combine Alphabet classes in the private overlap input. |
| `VTI` | `collected` | 2026-05-31 | full | 4.6000% | 3.0500% | 3.6000% | 1.9000% | 6.7000% | 2.9100% | GOOG is reported separately at 2.390000%; decide whether to combine Alphabet classes in the private overlap input. |
| `VT` | `collected` | 2026-05-31 | full | 2.8200% | 1.8900% | 2.1900% | 1.1600% | 4.1700% | 1.7400% | GOOG is reported separately at 1.480000%; decide whether to combine Alphabet classes in the private overlap input. |
| `QQQ` | `collected` | 2026-07-07 | full | 4.6313% | 3.4273% | 4.2426% | 2.9228% | 7.6412% | 2.8187% | GOOG is reported separately at 3.180934%; decide whether to combine Alphabet classes in the private overlap input. |

## Next Use

1. Copy only official holding weights into the gitignored overlap input file.
2. Add private ETF portfolio weights there, not in this public report.
3. Rerun [[scripts/di_etf_overlap_check.py|di_etf_overlap_check.py]] before marking `etf_overlap_checked`.
