# KIS OHLCV Queue Capture Result

- Request queue: `_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtyfifth10.requests.jsonl`
- Raw directory: `_report/raw/2026/2026-06-15/quant/universe-ohlcv`
- Dry run: `false`
- API type: `inquire_daily_itemchartprice`
- Tool group: `domestic_stock`
- MCP preflight status: `tool_unavailable_in_current_codex_app_surface`
- Local API detail fallback: `MCP/Kis Trading MCP/configs/domestic_stock.json` + `examples_llm` sample
- Execution path: `direct_kis_openapi_sample_auth` / read-only quotation endpoint
- Interpretation: `current_snapshot` / `paper-smoke`; not Backtest evidence

## Status Counts

| Status | Count |
| --- | ---: |
| `saved` | 10 |

## Rows

| Code | Company | Status | Output File | Message |
| --- | --- | --- | --- | --- |
| `009420` | 한올바이오파마 | `saved` | `009420.daily.raw.json` | ok |
| `009450` | 경동나비엔 | `saved` | `009450.daily.raw.json` | ok |
| `009460` | 한창제지 | `saved` | `009460.daily.raw.json` | ok |
| `009470` | 삼화전기 | `saved` | `009470.daily.raw.json` | ok |
| `009520` | 포스코엠텍 | `saved` | `009520.daily.raw.json` | ok |
| `009540` | HD한국조선해양 | `saved` | `009540.daily.raw.json` | ok |
| `009580` | 무림P&P | `saved` | `009580.daily.raw.json` | ok |
| `009620` | 삼보산업 | `saved` | `009620.daily.raw.json` | ok |
| `009680` | 모토닉 | `saved` | `009680.daily.raw.json` | ok |
| `009730` | 이렘 | `saved` | `009730.daily.raw.json` | ok |

## Guardrails

- Raw responses are stored under `_report/raw/**` and should not be committed.
- Re-run `scripts/quant_liquidity_filter.py` only after non-dry-run raw files are saved.
- `api_error_saved` means the raw error response was preserved for diagnosis, not that the stock failed the Liquidity Filter.
