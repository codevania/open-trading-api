# KIS Demo Account Preflight

- Config source: [[MCP/Kis Trading MCP/.env.kis|MCP/Kis Trading MCP/.env.kis]]
- Domestic stock API config: [[MCP/Kis Trading MCP/configs/domestic_stock.json|MCP/Kis Trading MCP/configs/domestic_stock.json]]
- Mode: `local_config_preflight_only`
- KIS API call: `false`
- Secrets printed: `false`
- Ready for read-only demo account calls: `false`
- Backtest readiness: `hold`
- Live trading readiness: `blocked`

## Status Counts

| Status | Count |
| --- | ---: |
| `fail` | 1 |
| `pass` | 8 |
| `warn` | 1 |

## Checks

| Check | Status | Source key | Detail |
| --- | --- | --- | --- |
| `demo_app_key` | `pass` | `KIS_PAPER_APP_KEY` | present and non-placeholder |
| `demo_app_secret` | `pass` | `KIS_PAPER_APP_SECRET` | present and non-placeholder |
| `demo_stock_account` | `fail` | `KIS_PAPER_STOCK` | configured value is empty |
| `account_product_code` | `pass` | `KIS_PROD_TYPE` | domestic stock product code present |
| `demo_rest_url` | `warn` | `KIS_URL_REST_PAPER` | not configured; KIS template default demo REST URL may apply |
| `api_method:inquire_psbl_order` | `pass` | `inquire_psbl_order` | configured in domestic_stock.json |
| `api_method:inquire_psbl_sell` | `pass` | `inquire_psbl_sell` | configured in domestic_stock.json |
| `api_method:inquire_balance` | `pass` | `inquire_balance` | configured in domestic_stock.json |
| `api_method:order_cash` | `pass` | `order_cash` | configured in domestic_stock.json |
| `api_method:order_rvsecncl` | `pass` | `order_rvsecncl` | configured in domestic_stock.json |

## Guardrails

- This report contains no credential or account values.
- Passing this preflight does not authorize order execution.
- The next safe API step is read-only demo `inquire_psbl_order`, `inquire_psbl_sell`, and balance/status checks.
- A future order executor must still require explicit confirmation, kill switch, order status/cancel handling, and `env_dv=demo` hard gating.
