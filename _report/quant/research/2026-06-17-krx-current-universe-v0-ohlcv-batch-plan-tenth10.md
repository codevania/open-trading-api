# KRX Current Universe v0 OHLCV Batch Plan

- As-of date: `2026-06-15`
- Source Universe rows: `_report/quant/research/2026-06-14-krx-current-universe-v0.rows.csv`
- API detail source: `MCP/Kis Trading MCP/configs/domestic_stock.json`
- MCP preflight status: `tool_unavailable_in_current_codex_app_surface`
- Local API detail preflight: `pass`
- Tool group: `domestic_stock`
- API type: `inquire_daily_itemchartprice`
- API path: `/uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice`
- API note: one call returns up to `100` daily rows according to local KIS config/example docs.
- Raw output directory target: `_report/raw/2026/2026-06-15/quant/universe-ohlcv`
- Offset: `0`
- Limit: `10`
- Skip existing raw: `true`
- Request queue JSONL: `_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-tenth10.requests.jsonl`

## Required Params

| Param | Description |
| --- | --- |
| `env_dv` | [필수] 실전모의구분 (ex. real:실전, demo:모의) |
| `fid_cond_mrkt_div_code` | [필수] 조건 시장 분류 코드 (ex. J:KRX, NX:NXT, UN:통합) |
| `fid_input_iscd` | [필수] 입력 종목코드 (ex. 종목코드 (ex 005930 삼성전자)) |
| `fid_input_date_1` | [필수] 입력 날짜 1 (ex. 조회 시작일자) |
| `fid_input_date_2` | [필수] 입력 날짜 2 (ex. 조회 종료일자 (최대 100개)) |
| `fid_period_div_code` | [필수] 기간분류코드 (ex. D:일봉 W:주봉, M:월봉, Y:년봉) |
| `fid_org_adj_prc` | [필수] 수정주가 원주가 가격 여부 (ex. 0:수정주가 1:원주가) |

## Summary

- Total Universe rows: `2875`
- Base included rows: `2390`
- Preexisting excluded rows: `485`
- Existing raw skipped: `90`
- Eligible after skip: `2300`
- Selected requests: `10`

## Request Sample

| Seq | Code | Company | Market | Start | End | Output File |
| ---: | --- | --- | --- | --- | --- | --- |
| 1 | `002020` | 코오롱 | KOSPI | 20260301 | 20260615 | `002020.daily.raw.json` |
| 2 | `002030` | 아세아 | KOSPI | 20260301 | 20260615 | `002030.daily.raw.json` |
| 3 | `002070` | 비비안 | KOSPI | 20260301 | 20260615 | `002070.daily.raw.json` |
| 4 | `002100` | 경농 | KOSPI | 20260301 | 20260615 | `002100.daily.raw.json` |
| 5 | `002140` | 고려산업 | KOSPI | 20260301 | 20260615 | `002140.daily.raw.json` |
| 6 | `002150` | 도화엔지니어링 | KOSPI | 20260301 | 20260615 | `002150.daily.raw.json` |
| 7 | `002170` | SYTS | KOSPI | 20260301 | 20260615 | `002170.daily.raw.json` |
| 8 | `002200` | 한국수출포장 | KOSPI | 20260301 | 20260615 | `002200.daily.raw.json` |
| 9 | `002210` | 동성제약 | KOSPI | 20260301 | 20260615 | `002210.daily.raw.json` |
| 10 | `002220` | 한일철강 | KOSPI | 20260301 | 20260615 | `002220.daily.raw.json` |

## Guardrails

- This plan does not call KIS and does not place orders.
- Before live MCP execution, run `domestic_stock.find_api_detail` for `inquire_daily_itemchartprice` in a surface where the MCP tool is available.
- Save raw responses under `_report/raw/**`; do not commit raw response files.
- Use `--limit`, `--offset`, and `--skip-existing` for small resumable batches.
- This is still `current_snapshot` / paper-smoke work, not a Point-in-Time Universe or Backtest.
