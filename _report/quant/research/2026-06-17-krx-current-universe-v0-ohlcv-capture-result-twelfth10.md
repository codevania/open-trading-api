# KIS OHLCV Queue Capture Result

- Request queue: [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-twelfth10.requests.jsonl|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-twelfth10.requests.jsonl]]
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
| `002450` | 삼익악기 | `saved` | `002450.daily.raw.json` | ok |
| `002460` | HS화성 | `saved` | `002460.daily.raw.json` | ok |
| `002600` | 조흥 | `saved` | `002600.daily.raw.json` | ok |
| `002620` | 제일파마홀딩스 | `saved` | `002620.daily.raw.json` | ok |
| `002630` | 오리엔트바이오 | `saved` | `002630.daily.raw.json` | ok |
| `002680` | 한탑 | `saved` | `002680.daily.raw.json` | ok |
| `002690` | 동일제강 | `saved` | `002690.daily.raw.json` | ok |
| `002700` | 신일전자 | `saved` | `002700.daily.raw.json` | ok |
| `002710` | TCC스틸 | `saved` | `002710.daily.raw.json` | ok |
| `002720` | 국제약품 | `saved` | `002720.daily.raw.json` | ok |

## Guardrails

- Raw responses are stored under `_report/raw/**` and should not be committed.
- Re-run [[scripts/quant_liquidity_filter.py|scripts/quant_liquidity_filter.py]] only after non-dry-run raw files are saved.
- `api_error_saved` means the raw error response was preserved for diagnosis, not that the stock failed the Liquidity Filter.
