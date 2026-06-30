# KIS OHLCV Queue Capture Result

- Request queue: [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyninth10.requests.jsonl|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyninth10.requests.jsonl]]
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
| `006920` | 모헨즈 | `dry_run` | `006920.daily.raw.json` | validated queue row only |
| `006980` | 우성 | `dry_run` | `006980.daily.raw.json` | validated queue row only |
| `007070` | GS리테일 | `dry_run` | `007070.daily.raw.json` | validated queue row only |
| `007110` | 일신석재 | `dry_run` | `007110.daily.raw.json` | validated queue row only |
| `007120` | 미래아이앤지 | `dry_run` | `007120.daily.raw.json` | validated queue row only |
| `007160` | 사조산업 | `dry_run` | `007160.daily.raw.json` | validated queue row only |
| `007210` | 벽산 | `dry_run` | `007210.daily.raw.json` | validated queue row only |
| `007280` | 한국특강 | `dry_run` | `007280.daily.raw.json` | validated queue row only |
| `007310` | 오뚜기 | `dry_run` | `007310.daily.raw.json` | validated queue row only |
| `007330` | 푸른저축은행 | `dry_run` | `007330.daily.raw.json` | validated queue row only |

## Guardrails

- Raw responses are stored under `_report/raw/**` and should not be committed.
- Re-run [[scripts/quant_liquidity_filter.py|scripts/quant_liquidity_filter.py]] only after non-dry-run raw files are saved.
- `api_error_saved` means the raw error response was preserved for diagnosis, not that the stock failed the Liquidity Filter.
