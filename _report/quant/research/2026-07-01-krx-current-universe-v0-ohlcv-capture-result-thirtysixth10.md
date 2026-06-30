# KIS OHLCV Queue Capture Result

- Request queue: [[_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtysixth10.requests.jsonl|_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtysixth10.requests.jsonl]]
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
| `009770` | 삼정펄프 | `saved` | `009770.daily.raw.json` | ok |
| `009780` | 엠에스씨 | `saved` | `009780.daily.raw.json` | ok |
| `009810` | 플레이그램 | `saved` | `009810.daily.raw.json` | ok |
| `009830` | 한화솔루션 | `saved` | `009830.daily.raw.json` | ok |
| `009900` | 명신산업 | `saved` | `009900.daily.raw.json` | ok |
| `009970` | 영원무역홀딩스 | `saved` | `009970.daily.raw.json` | ok |
| `010040` | 한국내화 | `saved` | `010040.daily.raw.json` | ok |
| `010060` | OCI홀딩스 | `saved` | `010060.daily.raw.json` | ok |
| `010100` | 한국무브넥스 | `saved` | `010100.daily.raw.json` | ok |
| `010120` | LS ELECTRIC | `saved` | `010120.daily.raw.json` | ok |

## Guardrails

- Raw responses are stored under `_report/raw/**` and should not be committed.
- Re-run [[scripts/quant_liquidity_filter.py|scripts/quant_liquidity_filter.py]] only after non-dry-run raw files are saved.
- `api_error_saved` means the raw error response was preserved for diagnosis, not that the stock failed the Liquidity Filter.
