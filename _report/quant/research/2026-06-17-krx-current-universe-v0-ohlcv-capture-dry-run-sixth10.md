# KIS OHLCV Queue Capture Result

- Request queue: `_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-sixth10.requests.jsonl`
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
| `001070` | 대한방직 | `dry_run` | `001070.daily.raw.json` | validated queue row only |
| `001080` | 만호제강 | `dry_run` | `001080.daily.raw.json` | validated queue row only |
| `001120` | LX인터내셔널 | `dry_run` | `001120.daily.raw.json` | validated queue row only |
| `001130` | 대한제분 | `dry_run` | `001130.daily.raw.json` | validated queue row only |
| `001200` | 유진투자증권 | `dry_run` | `001200.daily.raw.json` | validated queue row only |
| `001210` | 금호전기 | `dry_run` | `001210.daily.raw.json` | validated queue row only |
| `001230` | 동국홀딩스 | `dry_run` | `001230.daily.raw.json` | validated queue row only |
| `001250` | GS글로벌 | `dry_run` | `001250.daily.raw.json` | validated queue row only |
| `001260` | 남광토건 | `dry_run` | `001260.daily.raw.json` | validated queue row only |
| `001270` | 부국증권 | `dry_run` | `001270.daily.raw.json` | validated queue row only |

## Guardrails

- Raw responses are stored under `_report/raw/**` and should not be committed.
- Re-run `scripts/quant_liquidity_filter.py` only after non-dry-run raw files are saved.
- `api_error_saved` means the raw error response was preserved for diagnosis, not that the stock failed the Liquidity Filter.
