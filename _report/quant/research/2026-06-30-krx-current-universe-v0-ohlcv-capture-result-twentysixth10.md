# KIS OHLCV Queue Capture Result

- Request queue: [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentysixth10.requests.jsonl|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentysixth10.requests.jsonl]]
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
| `005950` | 이수화학 | `saved` | `005950.daily.raw.json` | ok |
| `005960` | 동부건설 | `saved` | `005960.daily.raw.json` | ok |
| `005990` | 매일홀딩스 | `saved` | `005990.daily.raw.json` | ok |
| `006040` | 동원산업 | `saved` | `006040.daily.raw.json` | ok |
| `006050` | 국영지앤엠 | `saved` | `006050.daily.raw.json` | ok |
| `006060` | 화승인더 | `saved` | `006060.daily.raw.json` | ok |
| `006090` | 사조오양 | `saved` | `006090.daily.raw.json` | ok |
| `006110` | 삼아알미늄 | `saved` | `006110.daily.raw.json` | ok |
| `006120` | SK디스커버리 | `saved` | `006120.daily.raw.json` | ok |
| `006140` | 피제이전자 | `saved` | `006140.daily.raw.json` | ok |

## Guardrails

- Raw responses are stored under `_report/raw/**` and should not be committed.
- Re-run [[scripts/quant_liquidity_filter.py|scripts/quant_liquidity_filter.py]] only after non-dry-run raw files are saved.
- `api_error_saved` means the raw error response was preserved for diagnosis, not that the stock failed the Liquidity Filter.
