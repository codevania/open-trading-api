# KIS OHLCV Queue Capture Result

- Request queue: [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-eleventh10.requests.jsonl|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-eleventh10.requests.jsonl]]
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
| `002230` | 피에스텍 | `saved` | `002230.daily.raw.json` | ok |
| `002240` | 고려제강 | `saved` | `002240.daily.raw.json` | ok |
| `002290` | 삼일기업공사 | `saved` | `002290.daily.raw.json` | ok |
| `002310` | 아세아제지 | `saved` | `002310.daily.raw.json` | ok |
| `002320` | 한진 | `saved` | `002320.daily.raw.json` | ok |
| `002350` | 넥센타이어 | `saved` | `002350.daily.raw.json` | ok |
| `002360` | SH에너지화학 | `saved` | `002360.daily.raw.json` | ok |
| `002380` | KCC | `saved` | `002380.daily.raw.json` | ok |
| `002390` | 한독 | `saved` | `002390.daily.raw.json` | ok |
| `002420` | 세기상사 | `saved` | `002420.daily.raw.json` | ok |

## Guardrails

- Raw responses are stored under `_report/raw/**` and should not be committed.
- Re-run [[scripts/quant_liquidity_filter.py|scripts/quant_liquidity_filter.py]] only after non-dry-run raw files are saved.
- `api_error_saved` means the raw error response was preserved for diagnosis, not that the stock failed the Liquidity Filter.
