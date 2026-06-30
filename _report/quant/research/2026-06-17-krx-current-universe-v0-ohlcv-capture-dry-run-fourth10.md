# KIS OHLCV Queue Capture Result

- Request queue: [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-fourth10.requests.jsonl|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-fourth10.requests.jsonl]]
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
| `000650` | 천일고속 | `dry_run` | `000650.daily.raw.json` | validated queue row only |
| `000660` | SK하이닉스 | `dry_run` | `000660.daily.raw.json` | validated queue row only |
| `000670` | 영풍 | `dry_run` | `000670.daily.raw.json` | validated queue row only |
| `000680` | LS네트웍스 | `dry_run` | `000680.daily.raw.json` | validated queue row only |
| `000700` | 유수홀딩스 | `dry_run` | `000700.daily.raw.json` | validated queue row only |
| `000720` | 현대건설 | `dry_run` | `000720.daily.raw.json` | validated queue row only |
| `000760` | 이화산업 | `dry_run` | `000760.daily.raw.json` | validated queue row only |
| `000810` | 삼성화재 | `dry_run` | `000810.daily.raw.json` | validated queue row only |
| `000850` | 화천기공 | `dry_run` | `000850.daily.raw.json` | validated queue row only |
| `000860` | 강남제비스코 | `dry_run` | `000860.daily.raw.json` | validated queue row only |

## Guardrails

- Raw responses are stored under `_report/raw/**` and should not be committed.
- Re-run [[scripts/quant_liquidity_filter.py|scripts/quant_liquidity_filter.py]] only after non-dry-run raw files are saved.
- `api_error_saved` means the raw error response was preserved for diagnosis, not that the stock failed the Liquidity Filter.
