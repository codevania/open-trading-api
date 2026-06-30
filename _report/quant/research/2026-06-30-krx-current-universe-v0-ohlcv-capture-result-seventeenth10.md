# KIS OHLCV Queue Capture Result

- Request queue: [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-seventeenth10.requests.jsonl|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-seventeenth10.requests.jsonl]]
- Raw directory: `_report/raw/2026/2026-06-15/quant/universe-ohlcv`
- Dry run: `false`
- API type: `inquire_daily_itemchartprice`
- Tool group: `domestic_stock`
- MCP preflight status: `tool_unavailable_in_current_codex_app_surface`
- Local API detail fallback: [[MCP/Kis Trading MCP/configs/domestic_stock.json|MCP/Kis Trading MCP/configs/domestic_stock.json]] + `examples_llm` sample
- Execution path: `direct_kis_openapi_sample_auth` / read-only quotation endpoint
- Interpretation: `current_snapshot` / `paper-smoke`; not Backtest evidence

## Status Counts

| Status | Count |
| --- | ---: |
| `saved` | 10 |

## Rows

| Code | Company | Status | Output File | Message |
| --- | --- | --- | --- | --- |
| `003570` | SNT다이내믹스 | `saved` | `003570.daily.raw.json` | ok |
| `003580` | HLB글로벌 | `saved` | `003580.daily.raw.json` | ok |
| `003610` | 방림 | `saved` | `003610.daily.raw.json` | ok |
| `003620` | KG모빌리티 | `saved` | `003620.daily.raw.json` | ok |
| `003650` | 미창석유 | `saved` | `003650.daily.raw.json` | ok |
| `003670` | 포스코퓨처엠 | `saved` | `003670.daily.raw.json` | ok |
| `003680` | 한성기업 | `saved` | `003680.daily.raw.json` | ok |
| `003690` | 코리안리 | `saved` | `003690.daily.raw.json` | ok |
| `003720` | 삼영 | `saved` | `003720.daily.raw.json` | ok |
| `003780` | 진양산업 | `saved` | `003780.daily.raw.json` | ok |

## Guardrails

- Raw responses are stored under `_report/raw/**` and should not be committed.
- Re-run [[scripts/quant_liquidity_filter.py|scripts/quant_liquidity_filter.py]] only after non-dry-run raw files are saved.
- `api_error_saved` means the raw error response was preserved for diagnosis, not that the stock failed the Liquidity Filter.
