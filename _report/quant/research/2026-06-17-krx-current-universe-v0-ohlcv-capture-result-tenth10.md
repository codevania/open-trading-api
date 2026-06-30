# KIS OHLCV Queue Capture Result

- Request queue: `_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-tenth10.requests.jsonl`
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
| `002020` | 코오롱 | `saved` | `002020.daily.raw.json` | ok |
| `002030` | 아세아 | `saved` | `002030.daily.raw.json` | ok |
| `002070` | 비비안 | `saved` | `002070.daily.raw.json` | ok |
| `002100` | 경농 | `saved` | `002100.daily.raw.json` | ok |
| `002140` | 고려산업 | `saved` | `002140.daily.raw.json` | ok |
| `002150` | 도화엔지니어링 | `saved` | `002150.daily.raw.json` | ok |
| `002170` | SYTS | `saved` | `002170.daily.raw.json` | ok |
| `002200` | 한국수출포장 | `saved` | `002200.daily.raw.json` | ok |
| `002210` | 동성제약 | `saved` | `002210.daily.raw.json` | ok |
| `002220` | 한일철강 | `saved` | `002220.daily.raw.json` | ok |

## Guardrails

- Raw responses are stored under `_report/raw/**` and should not be committed.
- Re-run `scripts/quant_liquidity_filter.py` only after non-dry-run raw files are saved.
- `api_error_saved` means the raw error response was preserved for diagnosis, not that the stock failed the Liquidity Filter.
