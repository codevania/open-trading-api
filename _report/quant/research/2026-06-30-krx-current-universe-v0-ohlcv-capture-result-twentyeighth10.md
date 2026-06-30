# KIS OHLCV Queue Capture Result

- Request queue: [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyeighth10.requests.jsonl|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyeighth10.requests.jsonl]]
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
| `006620` | 동구바이오제약 | `saved` | `006620.daily.raw.json` | ok |
| `006650` | 대한유화 | `saved` | `006650.daily.raw.json` | ok |
| `006660` | 삼성공조 | `saved` | `006660.daily.raw.json` | ok |
| `006730` | 서부T&D | `saved` | `006730.daily.raw.json` | ok |
| `006740` | 블루산업개발 | `saved` | `006740.daily.raw.json` | ok |
| `006800` | 미래에셋증권 | `saved` | `006800.daily.raw.json` | ok |
| `006840` | AK홀딩스 | `saved` | `006840.daily.raw.json` | ok |
| `006880` | 신송홀딩스 | `saved` | `006880.daily.raw.json` | ok |
| `006890` | 태경케미컬 | `saved` | `006890.daily.raw.json` | ok |
| `006910` | 보성파워텍 | `saved` | `006910.daily.raw.json` | ok |

## Guardrails

- Raw responses are stored under `_report/raw/**` and should not be committed.
- Re-run [[scripts/quant_liquidity_filter.py|scripts/quant_liquidity_filter.py]] only after non-dry-run raw files are saved.
- `api_error_saved` means the raw error response was preserved for diagnosis, not that the stock failed the Liquidity Filter.
