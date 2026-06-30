# KIS OHLCV Queue Capture Result

- Request queue: `_report/quant/research/2026-06-18-krx-current-universe-v0-ohlcv-batch-plan-sixteenth10.requests.jsonl`
- Raw directory: `_report/raw/2026/2026-06-15/quant/universe-ohlcv`
- Dry run: `true`
- API type: `inquire_daily_itemchartprice`
- Tool group: `domestic_stock`
- MCP preflight status: `tool_unavailable_in_current_codex_app_surface`
- Local API detail fallback: `MCP/Kis Trading MCP/configs/domestic_stock.json` + `examples_llm` sample
- Execution path: `direct_kis_openapi_sample_auth` / read-only quotation endpoint
- Interpretation: `current_snapshot` / `paper-smoke`; not Backtest evidence

## Status Counts

| Status | Count |
| --- | ---: |
| `dry_run` | 10 |

## Rows

| Code | Company | Status | Output File | Message |
| --- | --- | --- | --- | --- |
| `003350` | 한국화장품제조 | `dry_run` | `003350.daily.raw.json` | validated queue row only |
| `003380` | 하림지주 | `dry_run` | `003380.daily.raw.json` | validated queue row only |
| `003460` | 유화증권 | `dry_run` | `003460.daily.raw.json` | validated queue row only |
| `003470` | 유안타증권 | `dry_run` | `003470.daily.raw.json` | validated queue row only |
| `003480` | 한진중공업홀딩스 | `dry_run` | `003480.daily.raw.json` | validated queue row only |
| `003490` | 대한항공 | `dry_run` | `003490.daily.raw.json` | validated queue row only |
| `003520` | 영진약품 | `dry_run` | `003520.daily.raw.json` | validated queue row only |
| `003530` | 한화투자증권 | `dry_run` | `003530.daily.raw.json` | validated queue row only |
| `003540` | 대신증권 | `dry_run` | `003540.daily.raw.json` | validated queue row only |
| `003550` | LG | `dry_run` | `003550.daily.raw.json` | validated queue row only |

## Guardrails

- Raw responses are stored under `_report/raw/**` and should not be committed.
- Re-run `scripts/quant_liquidity_filter.py` only after non-dry-run raw files are saved.
- `api_error_saved` means the raw error response was preserved for diagnosis, not that the stock failed the Liquidity Filter.
