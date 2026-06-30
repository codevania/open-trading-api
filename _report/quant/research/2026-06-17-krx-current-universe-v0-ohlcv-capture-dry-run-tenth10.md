# KIS OHLCV Queue Capture Result

- Request queue: [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-tenth10.requests.jsonl|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-tenth10.requests.jsonl]]
- Raw directory: `_report/raw/2026/2026-06-15/quant/universe-ohlcv`
- Dry run: `true`
- API type: `inquire_daily_itemchartprice`
- Tool group: `domestic_stock`
- MCP preflight status: `tool_unavailable_in_current_codex_app_surface`
- Local API detail fallback: [[MCP/Kis Trading MCP/configs/domestic_stock.json|MCP/Kis Trading MCP/configs/domestic_stock.json]] + `examples_llm` sample
- Execution path: `direct_kis_openapi_sample_auth` / read-only quotation endpoint
- Interpretation: `current_snapshot` / `paper-smoke`; not Backtest evidence

## Status Counts

| Status | Count |
| --- | ---: |
| `dry_run` | 10 |

## Rows

| Code | Company | Status | Output File | Message |
| --- | --- | --- | --- | --- |
| `002020` | 코오롱 | `dry_run` | `002020.daily.raw.json` | validated queue row only |
| `002030` | 아세아 | `dry_run` | `002030.daily.raw.json` | validated queue row only |
| `002070` | 비비안 | `dry_run` | `002070.daily.raw.json` | validated queue row only |
| `002100` | 경농 | `dry_run` | `002100.daily.raw.json` | validated queue row only |
| `002140` | 고려산업 | `dry_run` | `002140.daily.raw.json` | validated queue row only |
| `002150` | 도화엔지니어링 | `dry_run` | `002150.daily.raw.json` | validated queue row only |
| `002170` | SYTS | `dry_run` | `002170.daily.raw.json` | validated queue row only |
| `002200` | 한국수출포장 | `dry_run` | `002200.daily.raw.json` | validated queue row only |
| `002210` | 동성제약 | `dry_run` | `002210.daily.raw.json` | validated queue row only |
| `002220` | 한일철강 | `dry_run` | `002220.daily.raw.json` | validated queue row only |

## Guardrails

- Raw responses are stored under `_report/raw/**` and should not be committed.
- Re-run [[scripts/quant_liquidity_filter.py|scripts/quant_liquidity_filter.py]] only after non-dry-run raw files are saved.
- `api_error_saved` means the raw error response was preserved for diagnosis, not that the stock failed the Liquidity Filter.
