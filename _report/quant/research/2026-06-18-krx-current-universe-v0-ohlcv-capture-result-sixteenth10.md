# KIS OHLCV Queue Capture Result

- Request queue: [[_report/quant/research/2026-06-18-krx-current-universe-v0-ohlcv-batch-plan-sixteenth10.requests.jsonl|_report/quant/research/2026-06-18-krx-current-universe-v0-ohlcv-batch-plan-sixteenth10.requests.jsonl]]
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
| `003350` | 한국화장품제조 | `saved` | `003350.daily.raw.json` | ok |
| `003380` | 하림지주 | `saved` | `003380.daily.raw.json` | ok |
| `003460` | 유화증권 | `saved` | `003460.daily.raw.json` | ok |
| `003470` | 유안타증권 | `saved` | `003470.daily.raw.json` | ok |
| `003480` | 한진중공업홀딩스 | `saved` | `003480.daily.raw.json` | ok |
| `003490` | 대한항공 | `saved` | `003490.daily.raw.json` | ok |
| `003520` | 영진약품 | `saved` | `003520.daily.raw.json` | ok |
| `003530` | 한화투자증권 | `saved` | `003530.daily.raw.json` | ok |
| `003540` | 대신증권 | `saved` | `003540.daily.raw.json` | ok |
| `003550` | LG | `saved` | `003550.daily.raw.json` | ok |

## Guardrails

- Raw responses are stored under `_report/raw/**` and should not be committed.
- Re-run [[scripts/quant_liquidity_filter.py|scripts/quant_liquidity_filter.py]] only after non-dry-run raw files are saved.
- `api_error_saved` means the raw error response was preserved for diagnosis, not that the stock failed the Liquidity Filter.
