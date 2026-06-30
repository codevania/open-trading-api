# KIS OHLCV Queue Capture Result

- Request queue: `_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-ninth10.requests.jsonl`
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
| `001720` | 신영증권 | `saved` | `001720.daily.raw.json` | ok |
| `001740` | SK네트웍스 | `saved` | `001740.daily.raw.json` | ok |
| `001750` | 한양증권 | `saved` | `001750.daily.raw.json` | ok |
| `001770` | SHD | `saved` | `001770.daily.raw.json` | ok |
| `001780` | 알루코 | `saved` | `001780.daily.raw.json` | ok |
| `001790` | 대한제당 | `saved` | `001790.daily.raw.json` | ok |
| `001800` | 오리온홀딩스 | `saved` | `001800.daily.raw.json` | ok |
| `001810` | 무림SP | `saved` | `001810.daily.raw.json` | ok |
| `001820` | 삼화콘덴서 | `saved` | `001820.daily.raw.json` | ok |
| `001940` | KISCO홀딩스 | `saved` | `001940.daily.raw.json` | ok |

## Guardrails

- Raw responses are stored under `_report/raw/**` and should not be committed.
- Re-run `scripts/quant_liquidity_filter.py` only after non-dry-run raw files are saved.
- `api_error_saved` means the raw error response was preserved for diagnosis, not that the stock failed the Liquidity Filter.
