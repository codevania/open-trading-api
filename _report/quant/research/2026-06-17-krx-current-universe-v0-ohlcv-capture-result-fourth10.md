# KIS OHLCV Queue Capture Result

- Request queue: [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-fourth10.requests.jsonl|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-fourth10.requests.jsonl]]
- Raw directory: `_report/raw/2026/2026-06-15/quant/universe-ohlcv`
- Dry run: `false`
- API type: `inquire_daily_itemchartprice`
- Tool group: `domestic_stock`
- MCP preflight status: `tool_unavailable_in_current_codex_app_surface`
- Local API detail fallback: [[MCP/Kis Trading MCP/configs/domestic_stock.json|MCP/Kis Trading MCP/configs/domestic_stock.json]] + `examples_llm` sample
- Execution path: `direct_kis_openapi_sample_auth` / read-only quotation endpoint
- Interpretation: `current_snapshot` / `paper-smoke`; not Backtest evidence

## Status Counts

| Status | Count |
| --- | ---: |
| `saved` | 10 |

## Rows

| Code | Company | Status | Output File | Message |
| --- | --- | --- | --- | --- |
| `000650` | 천일고속 | `saved` | `000650.daily.raw.json` | ok |
| `000660` | SK하이닉스 | `saved` | `000660.daily.raw.json` | ok |
| `000670` | 영풍 | `saved` | `000670.daily.raw.json` | ok |
| `000680` | LS네트웍스 | `saved` | `000680.daily.raw.json` | ok |
| `000700` | 유수홀딩스 | `saved` | `000700.daily.raw.json` | ok |
| `000720` | 현대건설 | `saved` | `000720.daily.raw.json` | ok |
| `000760` | 이화산업 | `saved` | `000760.daily.raw.json` | ok |
| `000810` | 삼성화재 | `saved` | `000810.daily.raw.json` | ok |
| `000850` | 화천기공 | `saved` | `000850.daily.raw.json` | ok |
| `000860` | 강남제비스코 | `saved` | `000860.daily.raw.json` | ok |

## Guardrails

- Raw responses are stored under `_report/raw/**` and should not be committed.
- Re-run [[scripts/quant_liquidity_filter.py|scripts/quant_liquidity_filter.py]] only after non-dry-run raw files are saved.
- `api_error_saved` means the raw error response was preserved for diagnosis, not that the stock failed the Liquidity Filter.
