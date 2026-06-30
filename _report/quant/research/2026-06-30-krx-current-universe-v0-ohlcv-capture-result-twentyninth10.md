# KIS OHLCV Queue Capture Result

- Request queue: [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyninth10.requests.jsonl|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyninth10.requests.jsonl]]
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
| `006920` | 모헨즈 | `saved` | `006920.daily.raw.json` | ok |
| `006980` | 우성 | `saved` | `006980.daily.raw.json` | ok |
| `007070` | GS리테일 | `saved` | `007070.daily.raw.json` | ok |
| `007110` | 일신석재 | `saved` | `007110.daily.raw.json` | ok |
| `007120` | 미래아이앤지 | `saved` | `007120.daily.raw.json` | ok |
| `007160` | 사조산업 | `saved` | `007160.daily.raw.json` | ok |
| `007210` | 벽산 | `saved` | `007210.daily.raw.json` | ok |
| `007280` | 한국특강 | `saved` | `007280.daily.raw.json` | ok |
| `007310` | 오뚜기 | `saved` | `007310.daily.raw.json` | ok |
| `007330` | 푸른저축은행 | `saved` | `007330.daily.raw.json` | ok |

## Guardrails

- Raw responses are stored under `_report/raw/**` and should not be committed.
- Re-run [[scripts/quant_liquidity_filter.py|scripts/quant_liquidity_filter.py]] only after non-dry-run raw files are saved.
- `api_error_saved` means the raw error response was preserved for diagnosis, not that the stock failed the Liquidity Filter.
