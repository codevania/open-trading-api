# KIS OHLCV Queue Capture Result

- Request queue: `_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-thirteenth10.requests.jsonl`
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
| `002760` | 보락 | `dry_run` | `002760.daily.raw.json` | validated queue row only |
| `002780` | 진흥기업 | `dry_run` | `002780.daily.raw.json` | validated queue row only |
| `002790` | 아모레퍼시픽홀딩스 | `dry_run` | `002790.daily.raw.json` | validated queue row only |
| `002800` | 신신제약 | `dry_run` | `002800.daily.raw.json` | validated queue row only |
| `002810` | 삼영무역 | `dry_run` | `002810.daily.raw.json` | validated queue row only |
| `002820` | SUN&L | `dry_run` | `002820.daily.raw.json` | validated queue row only |
| `002840` | 미원상사 | `dry_run` | `002840.daily.raw.json` | validated queue row only |
| `002870` | 신풍 | `dry_run` | `002870.daily.raw.json` | validated queue row only |
| `002880` | 디와이에이 | `dry_run` | `002880.daily.raw.json` | validated queue row only |
| `002900` | TYM | `dry_run` | `002900.daily.raw.json` | validated queue row only |

## Guardrails

- Raw responses are stored under `_report/raw/**` and should not be committed.
- Re-run `scripts/quant_liquidity_filter.py` only after non-dry-run raw files are saved.
- `api_error_saved` means the raw error response was preserved for diagnosis, not that the stock failed the Liquidity Filter.
