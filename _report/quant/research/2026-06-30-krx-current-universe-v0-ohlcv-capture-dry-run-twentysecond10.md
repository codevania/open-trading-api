# KIS OHLCV Queue Capture Result

- Request queue: [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentysecond10.requests.jsonl|_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentysecond10.requests.jsonl]]
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
| `004910` | 조광페인트 | `dry_run` | `004910.daily.raw.json` | validated queue row only |
| `004920` | 씨아이테크 | `dry_run` | `004920.daily.raw.json` | validated queue row only |
| `004960` | 한신공영 | `dry_run` | `004960.daily.raw.json` | validated queue row only |
| `004970` | 신라교역 | `dry_run` | `004970.daily.raw.json` | validated queue row only |
| `004980` | 성신양회 | `dry_run` | `004980.daily.raw.json` | validated queue row only |
| `004990` | 롯데지주 | `dry_run` | `004990.daily.raw.json` | validated queue row only |
| `005010` | 휴스틸 | `dry_run` | `005010.daily.raw.json` | validated queue row only |
| `005070` | 코스모신소재 | `dry_run` | `005070.daily.raw.json` | validated queue row only |
| `005090` | SGC에너지 | `dry_run` | `005090.daily.raw.json` | validated queue row only |
| `005160` | 동국산업 | `dry_run` | `005160.daily.raw.json` | validated queue row only |

## Guardrails

- Raw responses are stored under `_report/raw/**` and should not be committed.
- Re-run [[scripts/quant_liquidity_filter.py|scripts/quant_liquidity_filter.py]] only after non-dry-run raw files are saved.
- `api_error_saved` means the raw error response was preserved for diagnosis, not that the stock failed the Liquidity Filter.
