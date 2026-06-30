# KIS OHLCV Queue Capture Result

- Request queue: `_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-seventh10.requests.jsonl`
- Raw directory: `_report/raw/2026/2026-06-15/quant/universe-ohlcv`
- Dry run: `true`
- API type: `inquire_daily_itemchartprice`
- Tool group: `domestic_stock`
- MCP preflight status: `tool_unavailable_in_current_codex_app_surface`
- Local API detail fallback: `MCP/Kis Trading MCP/configs/domestic_stock.json` + `examples_llm` sample
- Execution path: `direct_kis_openapi_sample_auth` / read-only quotation endpoint
- Interpretation: `current_snapshot` / `paper-smoke`; not Backtest evidence

## Status Counts

| Status | Count |
| --- | ---: |
| `dry_run` | 10 |

## Rows

| Code | Company | Status | Output File | Message |
| --- | --- | --- | --- | --- |
| `001290` | 상상인증권 | `dry_run` | `001290.daily.raw.json` | validated queue row only |
| `001340` | PKC | `dry_run` | `001340.daily.raw.json` | validated queue row only |
| `001360` | 삼성제약 | `dry_run` | `001360.daily.raw.json` | validated queue row only |
| `001380` | SG글로벌 | `dry_run` | `001380.daily.raw.json` | validated queue row only |
| `001390` | KG케미칼 | `dry_run` | `001390.daily.raw.json` | validated queue row only |
| `001420` | 태원물산 | `dry_run` | `001420.daily.raw.json` | validated queue row only |
| `001430` | 세아베스틸지주 | `dry_run` | `001430.daily.raw.json` | validated queue row only |
| `001440` | 대한전선 | `dry_run` | `001440.daily.raw.json` | validated queue row only |
| `001450` | 현대해상 | `dry_run` | `001450.daily.raw.json` | validated queue row only |
| `001460` | BYC | `dry_run` | `001460.daily.raw.json` | validated queue row only |

## Guardrails

- Raw responses are stored under `_report/raw/**` and should not be committed.
- Re-run `scripts/quant_liquidity_filter.py` only after non-dry-run raw files are saved.
- `api_error_saved` means the raw error response was preserved for diagnosis, not that the stock failed the Liquidity Filter.
