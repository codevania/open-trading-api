# KIS OHLCV Queue Capture Result

- Request queue: [[_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-batch-plan.requests.jsonl|_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-batch-plan.requests.jsonl]]
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
| `000020` | 동화약품 | `dry_run` | `000020.daily.raw.json` | validated queue row only |
| `000040` | KR모터스 | `dry_run` | `000040.daily.raw.json` | validated queue row only |
| `000050` | 경방 | `dry_run` | `000050.daily.raw.json` | validated queue row only |
| `000070` | 삼양홀딩스 | `dry_run` | `000070.daily.raw.json` | validated queue row only |
| `000080` | 하이트진로 | `dry_run` | `000080.daily.raw.json` | validated queue row only |
| `000100` | 유한양행 | `dry_run` | `000100.daily.raw.json` | validated queue row only |
| `000120` | CJ대한통운 | `dry_run` | `000120.daily.raw.json` | validated queue row only |
| `000140` | 하이트진로홀딩스 | `dry_run` | `000140.daily.raw.json` | validated queue row only |
| `000150` | 두산 | `dry_run` | `000150.daily.raw.json` | validated queue row only |
| `000180` | 성창기업지주 | `dry_run` | `000180.daily.raw.json` | validated queue row only |

## Guardrails

- Raw responses are stored under `_report/raw/**` and should not be committed.
- Re-run [[scripts/quant_liquidity_filter.py|scripts/quant_liquidity_filter.py]] only after non-dry-run raw files are saved.
- `api_error_saved` means the raw error response was preserved for diagnosis, not that the stock failed the Liquidity Filter.
