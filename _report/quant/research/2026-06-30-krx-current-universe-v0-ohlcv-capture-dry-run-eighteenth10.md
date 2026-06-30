# KIS OHLCV Queue Capture Result

- Request queue: [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-eighteenth10.requests.jsonl|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-eighteenth10.requests.jsonl]]
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
| `003800` | 에이스침대 | `dry_run` | `003800.daily.raw.json` | validated queue row only |
| `003830` | 대한화섬 | `dry_run` | `003830.daily.raw.json` | validated queue row only |
| `003850` | 보령 | `dry_run` | `003850.daily.raw.json` | validated queue row only |
| `003920` | 남양유업 | `dry_run` | `003920.daily.raw.json` | validated queue row only |
| `003960` | 사조대림 | `dry_run` | `003960.daily.raw.json` | validated queue row only |
| `004000` | 롯데정밀화학 | `dry_run` | `004000.daily.raw.json` | validated queue row only |
| `004020` | 현대제철 | `dry_run` | `004020.daily.raw.json` | validated queue row only |
| `004060` | SG세계물산 | `dry_run` | `004060.daily.raw.json` | validated queue row only |
| `004080` | 신흥 | `dry_run` | `004080.daily.raw.json` | validated queue row only |
| `004090` | 한국석유 | `dry_run` | `004090.daily.raw.json` | validated queue row only |

## Guardrails

- Raw responses are stored under `_report/raw/**` and should not be committed.
- Re-run [[scripts/quant_liquidity_filter.py|scripts/quant_liquidity_filter.py]] only after non-dry-run raw files are saved.
- `api_error_saved` means the raw error response was preserved for diagnosis, not that the stock failed the Liquidity Filter.
