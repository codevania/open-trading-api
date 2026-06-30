# KIS OHLCV Queue Capture Result

- Request queue: `_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentythird10.requests.jsonl`
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
| `005180` | 빙그레 | `saved` | `005180.daily.raw.json` | ok |
| `005250` | 녹십자홀딩스 | `saved` | `005250.daily.raw.json` | ok |
| `005290` | 동진쎄미켐 | `saved` | `005290.daily.raw.json` | ok |
| `005300` | 롯데칠성 | `saved` | `005300.daily.raw.json` | ok |
| `005320` | 온타이드 | `saved` | `005320.daily.raw.json` | ok |
| `005360` | 모나미 | `saved` | `005360.daily.raw.json` | ok |
| `005380` | 현대차 | `saved` | `005380.daily.raw.json` | ok |
| `005420` | 코스모화학 | `saved` | `005420.daily.raw.json` | ok |
| `005430` | 한국공항 | `saved` | `005430.daily.raw.json` | ok |
| `005440` | 현대지에프홀딩스 | `saved` | `005440.daily.raw.json` | ok |

## Guardrails

- Raw responses are stored under `_report/raw/**` and should not be committed.
- Re-run `scripts/quant_liquidity_filter.py` only after non-dry-run raw files are saved.
- `api_error_saved` means the raw error response was preserved for diagnosis, not that the stock failed the Liquidity Filter.
