# KIS OHLCV Queue Capture Result

- Request queue: [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyfirst10.requests.jsonl|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyfirst10.requests.jsonl]]
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
| `004700` | 조광피혁 | `dry_run` | `004700.daily.raw.json` | validated queue row only |
| `004710` | 한솔테크닉스 | `dry_run` | `004710.daily.raw.json` | validated queue row only |
| `004720` | 팜젠사이언스 | `dry_run` | `004720.daily.raw.json` | validated queue row only |
| `004770` | 써니전자 | `dry_run` | `004770.daily.raw.json` | validated queue row only |
| `004780` | 대륙제관 | `dry_run` | `004780.daily.raw.json` | validated queue row only |
| `004800` | 효성 | `dry_run` | `004800.daily.raw.json` | validated queue row only |
| `004830` | 덕성 | `dry_run` | `004830.daily.raw.json` | validated queue row only |
| `004840` | DRB동일 | `dry_run` | `004840.daily.raw.json` | validated queue row only |
| `004870` | 티웨이홀딩스 | `dry_run` | `004870.daily.raw.json` | validated queue row only |
| `004890` | 동일산업 | `dry_run` | `004890.daily.raw.json` | validated queue row only |

## Guardrails

- Raw responses are stored under `_report/raw/**` and should not be committed.
- Re-run [[scripts/quant_liquidity_filter.py|scripts/quant_liquidity_filter.py]] only after non-dry-run raw files are saved.
- `api_error_saved` means the raw error response was preserved for diagnosis, not that the stock failed the Liquidity Filter.
