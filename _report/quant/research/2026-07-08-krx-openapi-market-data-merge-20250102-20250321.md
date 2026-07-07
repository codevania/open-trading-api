# KRX OpenAPI Market Data Merge Result

- Output: [[_report/raw/2026/2026-07-08/krx/openapi-market-data/20250102-20250321/market_data.csv|_report/raw/2026/2026-07-08/krx/openapi-market-data/20250102-20250321/market_data.csv]]
- Interpretation: joined market-data merge, not a `Point-in-Time Universe` or `Backtest` result
- Bias Control judgment: `hold`

## Inputs

| Input | Rows |
| --- | ---: |
| [[_report/raw/2026/2026-07-08/krx/openapi-market-data/20250102-20250307/market_data.csv|_report/raw/2026/2026-07-08/krx/openapi-market-data/20250102-20250307/market_data.csv]] | 115447 |
| [[_report/raw/2026/2026-07-08/krx/openapi-market-data/20250310-20250321/market_data.csv|_report/raw/2026/2026-07-08/krx/openapi-market-data/20250310-20250321/market_data.csv]] | 27543 |

## Summary

| Metric | Value |
| --- | ---: |
| Merged rows | 142990 |
| Date count | 52 |

## Market Counts

| Market | Rows |
| --- | ---: |
| `KOSDAQ` | 92994 |
| `KOSPI` | 49996 |

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
| `2025-02-10` | 2751 |
| `2025-02-11` | 2750 |
| `2025-02-12` | 2751 |
| `2025-02-13` | 2752 |
| `2025-02-14` | 2751 |
| `2025-02-17` | 2752 |
| `2025-02-18` | 2752 |
| `2025-02-19` | 2751 |
| `2025-02-20` | 2752 |
| `2025-02-21` | 2751 |
| `2025-02-24` | 2751 |
| `2025-02-25` | 2752 |
| `2025-02-26` | 2752 |
| `2025-02-27` | 2752 |
| `2025-02-28` | 2752 |
| `2025-03-04` | 2752 |
| `2025-03-05` | 2752 |
| `2025-03-06` | 2753 |
| `2025-03-07` | 2753 |
| `2025-03-10` | 2753 |
| `2025-03-11` | 2753 |
| `2025-03-12` | 2753 |
| `2025-03-13` | 2753 |
| `2025-03-14` | 2754 |
| `2025-03-17` | 2754 |
| `2025-03-18` | 2754 |
| `2025-03-19` | 2754 |
| `2025-03-20` | 2757 |
| `2025-03-21` | 2758 |

## Guardrails

- Duplicate date/code keys across inputs are a hard failure.
- This output still lacks complete historical status coverage by itself.
- Backtest readiness remains `hold` until `Point-in-Time` status replay and broader historical coverage are validated.
