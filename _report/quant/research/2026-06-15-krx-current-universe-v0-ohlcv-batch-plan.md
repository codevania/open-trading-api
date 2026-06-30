# KRX Current Universe v0 OHLCV Batch Plan

- As-of date: `2026-06-15`
- Source Universe rows: [[_report/quant/research/2026-06-14-krx-current-universe-v0.rows.csv|_report/quant/research/2026-06-14-krx-current-universe-v0.rows.csv]]
- API detail source: [[MCP/Kis Trading MCP/configs/domestic_stock.json|MCP/Kis Trading MCP/configs/domestic_stock.json]]
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
- Request queue JSONL: [[_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-batch-plan.requests.jsonl|_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-batch-plan.requests.jsonl]]

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
- Existing raw skipped: `0`
- Eligible after skip: `2390`
- Selected requests: `10`

## Request Sample

| Seq | Code | Company | Market | Start | End | Output File |
| ---: | --- | --- | --- | --- | --- | --- |
| 1 | `000020` | 동화약품 | KOSPI | 20260301 | 20260615 | `000020.daily.raw.json` |
| 2 | `000040` | KR모터스 | KOSPI | 20260301 | 20260615 | `000040.daily.raw.json` |
| 3 | `000050` | 경방 | KOSPI | 20260301 | 20260615 | `000050.daily.raw.json` |
| 4 | `000070` | 삼양홀딩스 | KOSPI | 20260301 | 20260615 | `000070.daily.raw.json` |
| 5 | `000080` | 하이트진로 | KOSPI | 20260301 | 20260615 | `000080.daily.raw.json` |
| 6 | `000100` | 유한양행 | KOSPI | 20260301 | 20260615 | `000100.daily.raw.json` |
| 7 | `000120` | CJ대한통운 | KOSPI | 20260301 | 20260615 | `000120.daily.raw.json` |
| 8 | `000140` | 하이트진로홀딩스 | KOSPI | 20260301 | 20260615 | `000140.daily.raw.json` |
| 9 | `000150` | 두산 | KOSPI | 20260301 | 20260615 | `000150.daily.raw.json` |
| 10 | `000180` | 성창기업지주 | KOSPI | 20260301 | 20260615 | `000180.daily.raw.json` |

## Guardrails

- This plan does not call KIS and does not place orders.
- Before live MCP execution, run `domestic_stock.find_api_detail` for `inquire_daily_itemchartprice` in a surface where the MCP tool is available.
- Save raw responses under `_report/raw/**`; do not commit raw response files.
- Use `--limit`, `--offset`, and `--skip-existing` for small resumable batches.
- This is still `current_snapshot` / paper-smoke work, not a Point-in-Time Universe or Backtest.
