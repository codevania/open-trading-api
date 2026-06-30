# KIS OHLCV Queue Capture Result

- Request queue: [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-nineteenth10.requests.jsonl|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-nineteenth10.requests.jsonl]]
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
| `004100` | 태양금속 | `saved` | `004100.daily.raw.json` | ok |
| `004140` | 동방 | `saved` | `004140.daily.raw.json` | ok |
| `004150` | 한솔홀딩스 | `saved` | `004150.daily.raw.json` | ok |
| `004170` | 신세계 | `saved` | `004170.daily.raw.json` | ok |
| `004250` | NPC | `saved` | `004250.daily.raw.json` | ok |
| `004270` | 남성 | `saved` | `004270.daily.raw.json` | ok |
| `004310` | 현대약품 | `saved` | `004310.daily.raw.json` | ok |
| `004360` | 세방 | `saved` | `004360.daily.raw.json` | ok |
| `004370` | 농심 | `saved` | `004370.daily.raw.json` | ok |
| `004380` | 삼익THK | `saved` | `004380.daily.raw.json` | ok |

## Guardrails

- Raw responses are stored under `_report/raw/**` and should not be committed.
- Re-run [[scripts/quant_liquidity_filter.py|scripts/quant_liquidity_filter.py]] only after non-dry-run raw files are saved.
- `api_error_saved` means the raw error response was preserved for diagnosis, not that the stock failed the Liquidity Filter.
