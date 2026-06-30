# KIS OHLCV Queue Capture Result

- Request queue: `_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtyfourth10.requests.jsonl`
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
| `009180` | 한솔로지스틱스 | `dry_run` | `009180.daily.raw.json` | validated queue row only |
| `009190` | 대양금속 | `dry_run` | `009190.daily.raw.json` | validated queue row only |
| `009200` | 무림페이퍼 | `dry_run` | `009200.daily.raw.json` | validated queue row only |
| `009240` | 한샘 | `dry_run` | `009240.daily.raw.json` | validated queue row only |
| `009270` | 신원 | `dry_run` | `009270.daily.raw.json` | validated queue row only |
| `009290` | 광동제약 | `dry_run` | `009290.daily.raw.json` | validated queue row only |
| `009300` | 삼아제약 | `dry_run` | `009300.daily.raw.json` | validated queue row only |
| `009310` | 참엔지니어링 | `dry_run` | `009310.daily.raw.json` | validated queue row only |
| `009320` | 아진전자부품 | `dry_run` | `009320.daily.raw.json` | validated queue row only |
| `009410` | 태영건설 | `dry_run` | `009410.daily.raw.json` | validated queue row only |

## Guardrails

- Raw responses are stored under `_report/raw/**` and should not be committed.
- Re-run `scripts/quant_liquidity_filter.py` only after non-dry-run raw files are saved.
- `api_error_saved` means the raw error response was preserved for diagnosis, not that the stock failed the Liquidity Filter.
