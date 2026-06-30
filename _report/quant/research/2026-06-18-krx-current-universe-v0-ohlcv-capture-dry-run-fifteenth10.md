# KIS OHLCV Queue Capture Result

- Request queue: [[_report/quant/research/2026-06-18-krx-current-universe-v0-ohlcv-batch-plan-fifteenth10.requests.jsonl|_report/quant/research/2026-06-18-krx-current-universe-v0-ohlcv-batch-plan-fifteenth10.requests.jsonl]]
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
| `003100` | 선광 | `dry_run` | `003100.daily.raw.json` | validated queue row only |
| `003120` | 일성아이에스 | `dry_run` | `003120.daily.raw.json` | validated queue row only |
| `003160` | 디아이 | `dry_run` | `003160.daily.raw.json` | validated queue row only |
| `003200` | 일신방직 | `dry_run` | `003200.daily.raw.json` | validated queue row only |
| `003220` | 대원제약 | `dry_run` | `003220.daily.raw.json` | validated queue row only |
| `003230` | 삼양식품 | `dry_run` | `003230.daily.raw.json` | validated queue row only |
| `003240` | 태광산업 | `dry_run` | `003240.daily.raw.json` | validated queue row only |
| `003280` | 흥아해운 | `dry_run` | `003280.daily.raw.json` | validated queue row only |
| `003300` | 한일홀딩스 | `dry_run` | `003300.daily.raw.json` | validated queue row only |
| `003310` | 대주산업 | `dry_run` | `003310.daily.raw.json` | validated queue row only |

## Guardrails

- Raw responses are stored under `_report/raw/**` and should not be committed.
- Re-run [[scripts/quant_liquidity_filter.py|scripts/quant_liquidity_filter.py]] only after non-dry-run raw files are saved.
- `api_error_saved` means the raw error response was preserved for diagnosis, not that the stock failed the Liquidity Filter.
