# KIS OHLCV Queue Capture Result

- Request queue: `_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-batch-plan-next10.requests.jsonl`
- Raw directory: `_report/raw/2026/2026-06-15/quant/universe-ohlcv`
- Dry run: `false`
- API type: `inquire_daily_itemchartprice`
- Tool group: `domestic_stock`
- MCP preflight status: `tool_unavailable_in_current_codex_app_surface`
- Local API detail fallback: `MCP/Kis Trading MCP/configs/domestic_stock.json` + `examples_llm` sample
- Execution path: `direct_kis_openapi_sample_auth` / read-only quotation endpoint
- Interpretation: `current_snapshot` / `paper-smoke`; not Backtest evidence

## Status Counts

| Status | Count |
| --- | ---: |
| `saved` | 10 |

## Rows

| Code | Company | Status | Output File | Message |
| --- | --- | --- | --- | --- |
| `000210` | DL | `saved` | `000210.daily.raw.json` | ok |
| `000220` | 유유제약 | `saved` | `000220.daily.raw.json` | ok |
| `000230` | 일동홀딩스 | `saved` | `000230.daily.raw.json` | ok |
| `000240` | 한국앤컴퍼니 | `saved` | `000240.daily.raw.json` | ok |
| `000250` | 삼천당제약 | `saved` | `000250.daily.raw.json` | ok |
| `000270` | 기아 | `saved` | `000270.daily.raw.json` | ok |
| `000300` | DH오토넥스 | `saved` | `000300.daily.raw.json` | ok |
| `000320` | 노루홀딩스 | `saved` | `000320.daily.raw.json` | ok |
| `000370` | 한화손해보험 | `saved` | `000370.daily.raw.json` | ok |
| `000390` | SP삼화 | `saved` | `000390.daily.raw.json` | ok |

## Guardrails

- Raw responses are stored under `_report/raw/**` and should not be committed.
- Re-run `scripts/quant_liquidity_filter.py` only after non-dry-run raw files are saved.
- `api_error_saved` means the raw error response was preserved for diagnosis, not that the stock failed the Liquidity Filter.
