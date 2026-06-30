# KIS OHLCV Queue Capture Result

- Request queue: `_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtythird10.requests.jsonl`
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
| `008730` | 율촌화학 | `saved` | `008730.daily.raw.json` | ok |
| `008770` | 호텔신라 | `saved` | `008770.daily.raw.json` | ok |
| `008830` | 대동기어 | `saved` | `008830.daily.raw.json` | ok |
| `008870` | 금비 | `saved` | `008870.daily.raw.json` | ok |
| `008930` | 한미사이언스 | `saved` | `008930.daily.raw.json` | ok |
| `008970` | KBI동양철관 | `saved` | `008970.daily.raw.json` | ok |
| `009070` | KCTC | `saved` | `009070.daily.raw.json` | ok |
| `009140` | 경인전자 | `saved` | `009140.daily.raw.json` | ok |
| `009150` | 삼성전기 | `saved` | `009150.daily.raw.json` | ok |
| `009160` | SIMPAC | `saved` | `009160.daily.raw.json` | ok |

## Guardrails

- Raw responses are stored under `_report/raw/**` and should not be committed.
- Re-run `scripts/quant_liquidity_filter.py` only after non-dry-run raw files are saved.
- `api_error_saved` means the raw error response was preserved for diagnosis, not that the stock failed the Liquidity Filter.
