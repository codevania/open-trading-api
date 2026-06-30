# KIS OHLCV Queue Capture Result

- Request queue: `_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-twelfth10.requests.jsonl`
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
| `002450` | 삼익악기 | `dry_run` | `002450.daily.raw.json` | validated queue row only |
| `002460` | HS화성 | `dry_run` | `002460.daily.raw.json` | validated queue row only |
| `002600` | 조흥 | `dry_run` | `002600.daily.raw.json` | validated queue row only |
| `002620` | 제일파마홀딩스 | `dry_run` | `002620.daily.raw.json` | validated queue row only |
| `002630` | 오리엔트바이오 | `dry_run` | `002630.daily.raw.json` | validated queue row only |
| `002680` | 한탑 | `dry_run` | `002680.daily.raw.json` | validated queue row only |
| `002690` | 동일제강 | `dry_run` | `002690.daily.raw.json` | validated queue row only |
| `002700` | 신일전자 | `dry_run` | `002700.daily.raw.json` | validated queue row only |
| `002710` | TCC스틸 | `dry_run` | `002710.daily.raw.json` | validated queue row only |
| `002720` | 국제약품 | `dry_run` | `002720.daily.raw.json` | validated queue row only |

## Guardrails

- Raw responses are stored under `_report/raw/**` and should not be committed.
- Re-run `scripts/quant_liquidity_filter.py` only after non-dry-run raw files are saved.
- `api_error_saved` means the raw error response was preserved for diagnosis, not that the stock failed the Liquidity Filter.
