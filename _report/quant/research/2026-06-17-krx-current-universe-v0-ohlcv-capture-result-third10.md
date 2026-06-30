# KIS OHLCV Queue Capture Result

- Request queue: [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-third10.requests.jsonl|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-third10.requests.jsonl]]
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
| `000400` | 롯데손해보험 | `saved` | `000400.daily.raw.json` | ok |
| `000430` | 대원강업 | `saved` | `000430.daily.raw.json` | ok |
| `000440` | 중앙에너비스 | `saved` | `000440.daily.raw.json` | ok |
| `000480` | CR홀딩스 | `saved` | `000480.daily.raw.json` | ok |
| `000490` | 대동 | `saved` | `000490.daily.raw.json` | ok |
| `000500` | 가온전선 | `saved` | `000500.daily.raw.json` | ok |
| `000520` | 삼일제약 | `saved` | `000520.daily.raw.json` | ok |
| `000540` | 흥국화재 | `saved` | `000540.daily.raw.json` | ok |
| `000590` | CS홀딩스 | `saved` | `000590.daily.raw.json` | ok |
| `000640` | 동아쏘시오홀딩스 | `saved` | `000640.daily.raw.json` | ok |

## Guardrails

- Raw responses are stored under `_report/raw/**` and should not be committed.
- Re-run [[scripts/quant_liquidity_filter.py|scripts/quant_liquidity_filter.py]] only after non-dry-run raw files are saved.
- `api_error_saved` means the raw error response was preserved for diagnosis, not that the stock failed the Liquidity Filter.
