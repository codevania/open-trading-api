# KIS OHLCV Queue Capture Result

- Request queue: `_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyeighth10.requests.jsonl`
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
| `006620` | 동구바이오제약 | `dry_run` | `006620.daily.raw.json` | validated queue row only |
| `006650` | 대한유화 | `dry_run` | `006650.daily.raw.json` | validated queue row only |
| `006660` | 삼성공조 | `dry_run` | `006660.daily.raw.json` | validated queue row only |
| `006730` | 서부T&D | `dry_run` | `006730.daily.raw.json` | validated queue row only |
| `006740` | 블루산업개발 | `dry_run` | `006740.daily.raw.json` | validated queue row only |
| `006800` | 미래에셋증권 | `dry_run` | `006800.daily.raw.json` | validated queue row only |
| `006840` | AK홀딩스 | `dry_run` | `006840.daily.raw.json` | validated queue row only |
| `006880` | 신송홀딩스 | `dry_run` | `006880.daily.raw.json` | validated queue row only |
| `006890` | 태경케미컬 | `dry_run` | `006890.daily.raw.json` | validated queue row only |
| `006910` | 보성파워텍 | `dry_run` | `006910.daily.raw.json` | validated queue row only |

## Guardrails

- Raw responses are stored under `_report/raw/**` and should not be committed.
- Re-run `scripts/quant_liquidity_filter.py` only after non-dry-run raw files are saved.
- `api_error_saved` means the raw error response was preserved for diagnosis, not that the stock failed the Liquidity Filter.
