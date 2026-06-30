# KIS OHLCV Queue Capture Result

- Request queue: [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentieth10.requests.jsonl|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentieth10.requests.jsonl]]
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
| `004410` | 서울식품 | `saved` | `004410.daily.raw.json` | ok |
| `004430` | 송원산업 | `saved` | `004430.daily.raw.json` | ok |
| `004440` | 삼일씨엔에스 | `saved` | `004440.daily.raw.json` | ok |
| `004450` | 삼화왕관 | `saved` | `004450.daily.raw.json` | ok |
| `004490` | 세방전지 | `saved` | `004490.daily.raw.json` | ok |
| `004540` | 깨끗한나라 | `saved` | `004540.daily.raw.json` | ok |
| `004560` | 현대비앤지스틸 | `saved` | `004560.daily.raw.json` | ok |
| `004590` | 한국가구 | `saved` | `004590.daily.raw.json` | ok |
| `004650` | 창해에탄올 | `saved` | `004650.daily.raw.json` | ok |
| `004690` | 삼천리 | `saved` | `004690.daily.raw.json` | ok |

## Guardrails

- Raw responses are stored under `_report/raw/**` and should not be committed.
- Re-run [[scripts/quant_liquidity_filter.py|scripts/quant_liquidity_filter.py]] only after non-dry-run raw files are saved.
- `api_error_saved` means the raw error response was preserved for diagnosis, not that the stock failed the Liquidity Filter.
