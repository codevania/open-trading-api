# KIS OHLCV Queue Capture Result

- Request queue: `_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyfourth10.requests.jsonl`
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
| `005490` | POSCO홀딩스 | `saved` | `005490.daily.raw.json` | ok |
| `005500` | 삼진제약 | `saved` | `005500.daily.raw.json` | ok |
| `005610` | 삼립 | `saved` | `005610.daily.raw.json` | ok |
| `005670` | 푸드웰 | `saved` | `005670.daily.raw.json` | ok |
| `005680` | 삼영전자 | `saved` | `005680.daily.raw.json` | ok |
| `005690` | 파미셀 | `saved` | `005690.daily.raw.json` | ok |
| `005710` | 대원산업 | `saved` | `005710.daily.raw.json` | ok |
| `005720` | 넥센 | `saved` | `005720.daily.raw.json` | ok |
| `005740` | 크라운해태홀딩스 | `saved` | `005740.daily.raw.json` | ok |
| `005750` | 대림바스 | `saved` | `005750.daily.raw.json` | ok |

## Guardrails

- Raw responses are stored under `_report/raw/**` and should not be committed.
- Re-run `scripts/quant_liquidity_filter.py` only after non-dry-run raw files are saved.
- `api_error_saved` means the raw error response was preserved for diagnosis, not that the stock failed the Liquidity Filter.
