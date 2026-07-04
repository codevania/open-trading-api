# KRX OpenAPI Market Data Merge Result

- Output: [[_report/raw/2026/2026-07-04/krx/openapi-market-data/20250102-20250207/market_data.csv|_report/raw/2026/2026-07-04/krx/openapi-market-data/20250102-20250207/market_data.csv]]
- Interpretation: joined market-data merge, not a `Point-in-Time Universe` or `Backtest` result
- Bias Control judgment: `hold`

## Inputs

| Input | Rows |
| --- | ---: |
| [[_report/raw/2026/2026-07-03/krx/openapi-market-data/20250102-20250124/market_data.csv|_report/raw/2026/2026-07-03/krx/openapi-market-data/20250102-20250124/market_data.csv]] | 46659 |
| [[_report/raw/2026/2026-07-04/krx/openapi-market-data/20250127-20250207/market_data.csv|_report/raw/2026/2026-07-04/krx/openapi-market-data/20250127-20250207/market_data.csv]] | 16506 |

## Summary

| Metric | Value |
| --- | ---: |
| Merged rows | 63165 |
| Date count | 23 |

## Market Counts

| Market | Rows |
| --- | ---: |
| `KOSDAQ` | 41059 |
| `KOSPI` | 22106 |

## Date Counts

| Date | Rows |
| --- | ---: |
| `2025-01-02` | 2745 |
| `2025-01-03` | 2745 |
| `2025-01-06` | 2745 |
| `2025-01-07` | 2745 |
| `2025-01-08` | 2744 |
| `2025-01-09` | 2744 |
| `2025-01-10` | 2744 |
| `2025-01-13` | 2744 |
| `2025-01-14` | 2744 |
| `2025-01-15` | 2744 |
| `2025-01-16` | 2744 |
| `2025-01-17` | 2744 |
| `2025-01-20` | 2744 |
| `2025-01-21` | 2744 |
| `2025-01-22` | 2744 |
| `2025-01-23` | 2746 |
| `2025-01-24` | 2749 |
| `2025-01-31` | 2749 |
| `2025-02-03` | 2750 |
| `2025-02-04` | 2751 |
| `2025-02-05` | 2752 |
| `2025-02-06` | 2752 |
| `2025-02-07` | 2752 |

## Guardrails

- Duplicate date/code keys across inputs are a hard failure.
- This output still lacks complete historical status coverage by itself.
- Backtest readiness remains `hold` until `Point-in-Time` status replay and broader historical coverage are validated.
