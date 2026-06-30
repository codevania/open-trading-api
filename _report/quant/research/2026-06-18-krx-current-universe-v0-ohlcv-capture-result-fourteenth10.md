# KIS OHLCV Queue Capture Result

- Request queue: `_report/quant/research/2026-06-18-krx-current-universe-v0-ohlcv-batch-plan-fourteenth10.requests.jsonl`
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
| `002920` | 유성기업 | `saved` | `002920.daily.raw.json` | ok |
| `002960` | 한국쉘석유 | `saved` | `002960.daily.raw.json` | ok |
| `002990` | 금호건설 | `saved` | `002990.daily.raw.json` | ok |
| `003000` | 부광약품 | `saved` | `003000.daily.raw.json` | ok |
| `003010` | 혜인 | `saved` | `003010.daily.raw.json` | ok |
| `003030` | 세아제강지주 | `saved` | `003030.daily.raw.json` | ok |
| `003060` | 에이프로젠바이오로직스 | `saved` | `003060.daily.raw.json` | ok |
| `003070` | 코오롱글로벌 | `saved` | `003070.daily.raw.json` | ok |
| `003080` | SB성보 | `saved` | `003080.daily.raw.json` | ok |
| `003090` | 대웅 | `saved` | `003090.daily.raw.json` | ok |

## Guardrails

- Raw responses are stored under `_report/raw/**` and should not be committed.
- Re-run `scripts/quant_liquidity_filter.py` only after non-dry-run raw files are saved.
- `api_error_saved` means the raw error response was preserved for diagnosis, not that the stock failed the Liquidity Filter.
