# KIS Raw Save Routine

## Purpose

이 routine은 KIS MCP에서 이미 받은 read-only market data JSON을 Quant smoke-test raw layout으로 저장한다.

이 routine은 market data 조회를 자동으로 수행하지 않고, 주문 API를 호출하지 않는다. 조회는 MCP에서 `find_api_detail` 확인 후 별도로 수행하고, 이 routine은 payload 저장과 manifest 작성만 담당한다.

## Scope

대상:

- `domestic_stock.inquire_daily_itemchartprice`
- `Data Pipeline Smoke Test`
- `_report/raw/YYYY/YYYY-MM-DD/quant/smoke-test/`

비대상:

- 주문 API
- 계좌/보유수량/토큰 저장
- Quant Universe 확정
- Backtest 성과 주장

## Required Preflight

KIS MCP 호출 전에는 반드시 API 상세를 확인한다.

```text
domestic_stock.find_api_detail
api_type: inquire_daily_itemchartprice
```

확인해야 할 core params:

- `env_dv`
- `fid_cond_mrkt_div_code`
- `fid_input_iscd`
- `fid_input_date_1`
- `fid_input_date_2`
- `fid_period_div_code`
- `fid_org_adj_prc`

## Capture Layout

```text
_report/raw/YYYY/YYYY-MM-DD/quant/smoke-test/
  005930.daily.raw.json
  000660.daily.raw.json
  035420.daily.raw.json
  manifest.yaml
```

`manifest.yaml`은 helper가 재작성한다. `_report/raw/`는 원천 응답 저장소이며 Git 추적 대상이 아니다.

## Save Command

MCP 응답 JSON을 파일로 확보했거나 stdin으로 전달할 수 있을 때 다음 helper를 사용한다.

```powershell
uv run python scripts/quant_kis_raw_save.py `
  --input captured-005930.json `
  --raw-dir _report/raw/YYYY/YYYY-MM-DD/quant/smoke-test `
  --symbol 005930 `
  --api-type inquire_daily_itemchartprice `
  --env-dv real `
  --market KRX `
  --start-date 20260501 `
  --end-date 20260605 `
  --period D
```

stdin 사용:

```powershell
Get-Content captured-005930.json -Raw | uv run python scripts/quant_kis_raw_save.py `
  --input - `
  --raw-dir _report/raw/YYYY/YYYY-MM-DD/quant/smoke-test `
  --symbol 005930
```

## Validate Command

저장 후 바로 validator를 실행한다.

```powershell
uv run python scripts/quant_smoke_validate.py `
  --raw-dir _report/raw/YYYY/YYYY-MM-DD/quant/smoke-test `
  --lookback 20 `
  --output _report/quant/research/YYYY-MM-DD-data-pipeline-smoke-test-result.md
```

## Acceptance

통과 기준:

- raw JSON 파일이 symbol별로 생성된다.
- `manifest.yaml`이 생성된다.
- validator가 raw directory를 읽는다.
- 최소 21개 daily rows가 있으면 `ROC`와 `Signal Candidate`가 계산된다.
- 21개 미만이면 `data-insufficient`가 기록된다.

해석 제한:

- `manual_smoke_test` 결과는 Quant Universe가 아니다.
- 결과는 Strategy 성과가 아니다.
- Point-in-Time Universe 확보 전 Backtest 판정은 `hold`로 둔다.
