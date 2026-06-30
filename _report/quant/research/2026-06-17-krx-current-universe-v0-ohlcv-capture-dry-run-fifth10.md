# KIS OHLCV Queue Capture Result

- Request queue: [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-fifth10.requests.jsonl|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-fifth10.requests.jsonl]]
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
| `000880` | 한화 | `dry_run` | `000880.daily.raw.json` | validated queue row only |
| `000890` | 보해양조 | `dry_run` | `000890.daily.raw.json` | validated queue row only |
| `000910` | 유니온 | `dry_run` | `000910.daily.raw.json` | validated queue row only |
| `000950` | 전방 | `dry_run` | `000950.daily.raw.json` | validated queue row only |
| `000970` | 한국주철관 | `dry_run` | `000970.daily.raw.json` | validated queue row only |
| `000990` | DB하이텍 | `dry_run` | `000990.daily.raw.json` | validated queue row only |
| `001000` | 신라섬유 | `dry_run` | `001000.daily.raw.json` | validated queue row only |
| `001020` | 페이퍼코리아 | `dry_run` | `001020.daily.raw.json` | validated queue row only |
| `001040` | CJ | `dry_run` | `001040.daily.raw.json` | validated queue row only |
| `001060` | JW중외제약 | `dry_run` | `001060.daily.raw.json` | validated queue row only |

## Guardrails

- Raw responses are stored under `_report/raw/**` and should not be committed.
- Re-run [[scripts/quant_liquidity_filter.py|scripts/quant_liquidity_filter.py]] only after non-dry-run raw files are saved.
- `api_error_saved` means the raw error response was preserved for diagnosis, not that the stock failed the Liquidity Filter.
