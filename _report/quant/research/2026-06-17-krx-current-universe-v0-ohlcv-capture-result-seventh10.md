# KIS OHLCV Queue Capture Result

- Request queue: [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-seventh10.requests.jsonl|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-seventh10.requests.jsonl]]
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
| `001290` | 상상인증권 | `saved` | `001290.daily.raw.json` | ok |
| `001340` | PKC | `saved` | `001340.daily.raw.json` | ok |
| `001360` | 삼성제약 | `saved` | `001360.daily.raw.json` | ok |
| `001380` | SG글로벌 | `saved` | `001380.daily.raw.json` | ok |
| `001390` | KG케미칼 | `saved` | `001390.daily.raw.json` | ok |
| `001420` | 태원물산 | `saved` | `001420.daily.raw.json` | ok |
| `001430` | 세아베스틸지주 | `saved` | `001430.daily.raw.json` | ok |
| `001440` | 대한전선 | `saved` | `001440.daily.raw.json` | ok |
| `001450` | 현대해상 | `saved` | `001450.daily.raw.json` | ok |
| `001460` | BYC | `saved` | `001460.daily.raw.json` | ok |

## Guardrails

- Raw responses are stored under `_report/raw/**` and should not be committed.
- Re-run [[scripts/quant_liquidity_filter.py|scripts/quant_liquidity_filter.py]] only after non-dry-run raw files are saved.
- `api_error_saved` means the raw error response was preserved for diagnosis, not that the stock failed the Liquidity Filter.
