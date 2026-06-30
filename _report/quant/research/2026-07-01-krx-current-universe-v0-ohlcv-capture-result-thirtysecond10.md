# KIS OHLCV Queue Capture Result

- Request queue: `_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtysecond10.requests.jsonl`
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
| `008060` | 대덕 | `saved` | `008060.daily.raw.json` | ok |
| `008250` | 이건산업 | `saved` | `008250.daily.raw.json` | ok |
| `008260` | NI스틸 | `saved` | `008260.daily.raw.json` | ok |
| `008290` | 원풍물산 | `saved` | `008290.daily.raw.json` | ok |
| `008350` | 남선알미늄 | `saved` | `008350.daily.raw.json` | ok |
| `008370` | 원풍 | `saved` | `008370.daily.raw.json` | ok |
| `008420` | 문배철강 | `saved` | `008420.daily.raw.json` | ok |
| `008470` | 부스타 | `saved` | `008470.daily.raw.json` | ok |
| `008490` | 서흥 | `saved` | `008490.daily.raw.json` | ok |
| `008700` | 아남전자 | `saved` | `008700.daily.raw.json` | ok |

## Guardrails

- Raw responses are stored under `_report/raw/**` and should not be committed.
- Re-run `scripts/quant_liquidity_filter.py` only after non-dry-run raw files are saved.
- `api_error_saved` means the raw error response was preserved for diagnosis, not that the stock failed the Liquidity Filter.
