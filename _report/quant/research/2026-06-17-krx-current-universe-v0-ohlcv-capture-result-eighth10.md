# KIS OHLCV Queue Capture Result

- Request queue: `_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-eighth10.requests.jsonl`
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
| `001500` | 현대차증권 | `saved` | `001500.daily.raw.json` | ok |
| `001510` | SK증권 | `saved` | `001510.daily.raw.json` | ok |
| `001520` | 동양 | `saved` | `001520.daily.raw.json` | ok |
| `001530` | DI동일 | `saved` | `001530.daily.raw.json` | ok |
| `001540` | 안국약품 | `saved` | `001540.daily.raw.json` | ok |
| `001550` | 조비 | `saved` | `001550.daily.raw.json` | ok |
| `001560` | 제일연마 | `saved` | `001560.daily.raw.json` | ok |
| `001620` | 케이비아이동국실업 | `saved` | `001620.daily.raw.json` | ok |
| `001630` | 종근당홀딩스 | `saved` | `001630.daily.raw.json` | ok |
| `001680` | 대상 | `saved` | `001680.daily.raw.json` | ok |

## Guardrails

- Raw responses are stored under `_report/raw/**` and should not be committed.
- Re-run `scripts/quant_liquidity_filter.py` only after non-dry-run raw files are saved.
- `api_error_saved` means the raw error response was preserved for diagnosis, not that the stock failed the Liquidity Filter.
