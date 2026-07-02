# KRX OpenAPI Normalize Result

- Source: saved KRX OpenAPI raw JSON
- Interpretation: `parser_normalization_smoke`, not a `Point-in-Time Universe` or `Backtest` result
- Bias Control judgment: `hold`

## Inputs

- [[_report/raw/2026/2026-07-03/krx/openapi/kosdaq_index_daily_20250102.raw.json|_report/raw/2026/2026-07-03/krx/openapi/kosdaq_index_daily_20250102.raw.json]]
- [[_report/raw/2026/2026-07-03/krx/openapi/kosdaq_issue_base_20250102.raw.json|_report/raw/2026/2026-07-03/krx/openapi/kosdaq_issue_base_20250102.raw.json]]
- [[_report/raw/2026/2026-07-03/krx/openapi/kosdaq_stock_daily_20250102.raw.json|_report/raw/2026/2026-07-03/krx/openapi/kosdaq_stock_daily_20250102.raw.json]]
- [[_report/raw/2026/2026-07-03/krx/openapi/kospi_index_daily_20250102.raw.json|_report/raw/2026/2026-07-03/krx/openapi/kospi_index_daily_20250102.raw.json]]
- [[_report/raw/2026/2026-07-03/krx/openapi/kospi_issue_base_20250102.raw.json|_report/raw/2026/2026-07-03/krx/openapi/kospi_issue_base_20250102.raw.json]]
- [[_report/raw/2026/2026-07-03/krx/openapi/kospi_stock_daily_20250102.raw.json|_report/raw/2026/2026-07-03/krx/openapi/kospi_stock_daily_20250102.raw.json]]

## Output Tables

| Table | Rows | Output |
| --- | ---: | --- |
| `stock_daily` | 2745 | [[_report/raw/2026/2026-07-03/krx/openapi-normalized/20250102/stock_daily.csv|_report/raw/2026/2026-07-03/krx/openapi-normalized/20250102/stock_daily.csv]] |
| `issue_base` | 2745 | [[_report/raw/2026/2026-07-03/krx/openapi-normalized/20250102/issue_base.csv|_report/raw/2026/2026-07-03/krx/openapi-normalized/20250102/issue_base.csv]] |
| `index_daily` | 91 | [[_report/raw/2026/2026-07-03/krx/openapi-normalized/20250102/index_daily.csv|_report/raw/2026/2026-07-03/krx/openapi-normalized/20250102/index_daily.csv]] |

## Guardrails

- KRX raw fields are normalized into stable local column names but not yet joined into a historical Universe.
- Stock and issue rows preserve KRX short codes exactly, including leading zeros and any future alphanumeric short codes.
- Management designation, trading halt, market alert, and delisting event replay are not covered by these six core APIs.
- Backtest readiness remains `hold` until `Point-in-Time` status replay and historical coverage are validated.
