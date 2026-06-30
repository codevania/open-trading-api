# KIS OHLCV Queue Capture Result

- Request queue: `_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-nineteenth10.requests.jsonl`
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
| `004100` | 태양금속 | `dry_run` | `004100.daily.raw.json` | validated queue row only |
| `004140` | 동방 | `dry_run` | `004140.daily.raw.json` | validated queue row only |
| `004150` | 한솔홀딩스 | `dry_run` | `004150.daily.raw.json` | validated queue row only |
| `004170` | 신세계 | `dry_run` | `004170.daily.raw.json` | validated queue row only |
| `004250` | NPC | `dry_run` | `004250.daily.raw.json` | validated queue row only |
| `004270` | 남성 | `dry_run` | `004270.daily.raw.json` | validated queue row only |
| `004310` | 현대약품 | `dry_run` | `004310.daily.raw.json` | validated queue row only |
| `004360` | 세방 | `dry_run` | `004360.daily.raw.json` | validated queue row only |
| `004370` | 농심 | `dry_run` | `004370.daily.raw.json` | validated queue row only |
| `004380` | 삼익THK | `dry_run` | `004380.daily.raw.json` | validated queue row only |

## Guardrails

- Raw responses are stored under `_report/raw/**` and should not be committed.
- Re-run `scripts/quant_liquidity_filter.py` only after non-dry-run raw files are saved.
- `api_error_saved` means the raw error response was preserved for diagnosis, not that the stock failed the Liquidity Filter.
