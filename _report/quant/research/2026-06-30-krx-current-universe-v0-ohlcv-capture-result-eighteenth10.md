# KIS OHLCV Queue Capture Result

- Request queue: `_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-eighteenth10.requests.jsonl`
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
| `003800` | 에이스침대 | `saved` | `003800.daily.raw.json` | ok |
| `003830` | 대한화섬 | `saved` | `003830.daily.raw.json` | ok |
| `003850` | 보령 | `saved` | `003850.daily.raw.json` | ok |
| `003920` | 남양유업 | `saved` | `003920.daily.raw.json` | ok |
| `003960` | 사조대림 | `saved` | `003960.daily.raw.json` | ok |
| `004000` | 롯데정밀화학 | `saved` | `004000.daily.raw.json` | ok |
| `004020` | 현대제철 | `saved` | `004020.daily.raw.json` | ok |
| `004060` | SG세계물산 | `saved` | `004060.daily.raw.json` | ok |
| `004080` | 신흥 | `saved` | `004080.daily.raw.json` | ok |
| `004090` | 한국석유 | `saved` | `004090.daily.raw.json` | ok |

## Guardrails

- Raw responses are stored under `_report/raw/**` and should not be committed.
- Re-run `scripts/quant_liquidity_filter.py` only after non-dry-run raw files are saved.
- `api_error_saved` means the raw error response was preserved for diagnosis, not that the stock failed the Liquidity Filter.
