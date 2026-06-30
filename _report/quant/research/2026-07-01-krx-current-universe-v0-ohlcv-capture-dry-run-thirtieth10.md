# KIS OHLCV Queue Capture Result

- Request queue: [[_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtieth10.requests.jsonl|_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtieth10.requests.jsonl]]
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
| `007340` | DN오토모티브 | `dry_run` | `007340.daily.raw.json` | validated queue row only |
| `007370` | 진양제약 | `dry_run` | `007370.daily.raw.json` | validated queue row only |
| `007390` | 네이처셀 | `dry_run` | `007390.daily.raw.json` | validated queue row only |
| `007460` | 에이프로젠 | `dry_run` | `007460.daily.raw.json` | validated queue row only |
| `007530` | 와이엠 | `dry_run` | `007530.daily.raw.json` | validated queue row only |
| `007540` | 샘표 | `dry_run` | `007540.daily.raw.json` | validated queue row only |
| `007570` | 일양약품 | `dry_run` | `007570.daily.raw.json` | validated queue row only |
| `007590` | 동방아그로 | `dry_run` | `007590.daily.raw.json` | validated queue row only |
| `007610` | 선도전기 | `dry_run` | `007610.daily.raw.json` | validated queue row only |
| `007660` | 이수페타시스 | `dry_run` | `007660.daily.raw.json` | validated queue row only |

## Guardrails

- Raw responses are stored under `_report/raw/**` and should not be committed.
- Re-run [[scripts/quant_liquidity_filter.py|scripts/quant_liquidity_filter.py]] only after non-dry-run raw files are saved.
- `api_error_saved` means the raw error response was preserved for diagnosis, not that the stock failed the Liquidity Filter.
