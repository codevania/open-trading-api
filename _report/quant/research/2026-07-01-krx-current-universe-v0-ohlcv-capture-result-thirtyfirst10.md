# KIS OHLCV Queue Capture Result

- Request queue: `_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtyfirst10.requests.jsonl`
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
| `007680` | 대원 | `saved` | `007680.daily.raw.json` | ok |
| `007690` | 국도화학 | `saved` | `007690.daily.raw.json` | ok |
| `007700` | F&F홀딩스 | `saved` | `007700.daily.raw.json` | ok |
| `007720` | 소노스퀘어 | `saved` | `007720.daily.raw.json` | ok |
| `007770` | 한일화학 | `saved` | `007770.daily.raw.json` | ok |
| `007810` | 코리아써키트 | `saved` | `007810.daily.raw.json` | ok |
| `007820` | 엠엑스로보틱스 | `saved` | `007820.daily.raw.json` | ok |
| `007860` | 서연 | `saved` | `007860.daily.raw.json` | ok |
| `007980` | TP | `saved` | `007980.daily.raw.json` | ok |
| `008040` | 사조동아원 | `saved` | `008040.daily.raw.json` | ok |

## Guardrails

- Raw responses are stored under `_report/raw/**` and should not be committed.
- Re-run `scripts/quant_liquidity_filter.py` only after non-dry-run raw files are saved.
- `api_error_saved` means the raw error response was preserved for diagnosis, not that the stock failed the Liquidity Filter.
