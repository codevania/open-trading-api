# KIS OHLCV Queue Capture Result

- Request queue: [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyfifth10.requests.jsonl|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyfifth10.requests.jsonl]]
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
| `005800` | 신영와코루 | `dry_run` | `005800.daily.raw.json` | validated queue row only |
| `005810` | 풍산홀딩스 | `dry_run` | `005810.daily.raw.json` | validated queue row only |
| `005820` | 원림 | `dry_run` | `005820.daily.raw.json` | validated queue row only |
| `005830` | DB손해보험 | `dry_run` | `005830.daily.raw.json` | validated queue row only |
| `005850` | 에스엘 | `dry_run` | `005850.daily.raw.json` | validated queue row only |
| `005860` | 한일사료 | `dry_run` | `005860.daily.raw.json` | validated queue row only |
| `005870` | 휴니드 | `dry_run` | `005870.daily.raw.json` | validated queue row only |
| `005880` | 대한해운 | `dry_run` | `005880.daily.raw.json` | validated queue row only |
| `005930` | 삼성전자 | `dry_run` | `005930.daily.raw.json` | validated queue row only |
| `005940` | NH투자증권 | `dry_run` | `005940.daily.raw.json` | validated queue row only |

## Guardrails

- Raw responses are stored under `_report/raw/**` and should not be committed.
- Re-run [[scripts/quant_liquidity_filter.py|scripts/quant_liquidity_filter.py]] only after non-dry-run raw files are saved.
- `api_error_saved` means the raw error response was preserved for diagnosis, not that the stock failed the Liquidity Filter.
