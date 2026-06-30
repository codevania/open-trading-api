# KIS OHLCV Queue Capture Result

- Request queue: `_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyseventh10.requests.jsonl`
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
| `006200` | 한국전자홀딩스 | `saved` | `006200.daily.raw.json` | ok |
| `006220` | 제주은행 | `saved` | `006220.daily.raw.json` | ok |
| `006260` | LS | `saved` | `006260.daily.raw.json` | ok |
| `006280` | 녹십자 | `saved` | `006280.daily.raw.json` | ok |
| `006340` | 대원전선 | `saved` | `006340.daily.raw.json` | ok |
| `006360` | GS건설 | `saved` | `006360.daily.raw.json` | ok |
| `006370` | 대구백화점 | `saved` | `006370.daily.raw.json` | ok |
| `006380` | 카프로 | `saved` | `006380.daily.raw.json` | ok |
| `006400` | 삼성SDI | `saved` | `006400.daily.raw.json` | ok |
| `006570` | 대림통상 | `saved` | `006570.daily.raw.json` | ok |

## Guardrails

- Raw responses are stored under `_report/raw/**` and should not be committed.
- Re-run `scripts/quant_liquidity_filter.py` only after non-dry-run raw files are saved.
- `api_error_saved` means the raw error response was preserved for diagnosis, not that the stock failed the Liquidity Filter.
