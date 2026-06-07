# Data Pipeline Smoke Test Plan

## Metadata

- 작성일: 2026-06-08
- 작성자: Codex
- 대상 Strategy: `001-strategy-universe-momentum`
- 현재 판정: hold
- 목적: `Point-in-Time Investable Universe`가 없는 상태에서 성과 주장을 하지 않고 데이터 조회, 저장, 파싱, Signal 계산 흐름만 검증한다.

## 1. Smoke Test의 의미

`Data Pipeline Smoke Test`는 Backtest가 아니다.

허용되는 해석:

- KIS MCP market data call이 동작한다.
- raw response를 저장할 수 있다.
- OHLCV schema를 parser가 읽을 수 있다.
- `ROC`와 `Signal Candidate` 계산이 가능하다.
- 비용 모델이 결과 계산에 연결될 수 있다.

금지되는 해석:

- Strategy가 돈을 벌 수 있다는 주장.
- Alpha가 있다는 주장.
- Quant Universe가 완성됐다는 주장.
- Manual symbol set 결과를 과거 성과로 해석.

## 2. Preflight Result

2026-06-08에 다음 read-only KIS MCP preflight를 수행했다.

사전 확인:

- `domestic_stock.find_api_detail`
- 대상 API: `inquire_daily_itemchartprice`
- 확인된 필수 파라미터:
  - `env_dv`
  - `fid_cond_mrkt_div_code`
  - `fid_input_iscd`
  - `fid_input_date_1`
  - `fid_input_date_2`
  - `fid_period_div_code`
  - `fid_org_adj_prc`

실제 호출:

```yaml
api_type: inquire_daily_itemchartprice
params:
  env_dv: real
  fid_cond_mrkt_div_code: J
  fid_input_iscd: "005930"
  fid_input_date_1: "20260101"
  fid_input_date_2: "20260605"
  fid_period_div_code: D
  fid_org_adj_prc: "0"
```

결과:

- API call: success
- `output1`: current/summary quote structure 확인
- `output2`: daily OHLCV rows 확인
- 확인된 core fields:
  - `stck_bsop_date`
  - `stck_clpr`
  - `stck_oprc`
  - `stck_hgpr`
  - `stck_lwpr`
  - `acml_vol`
  - `acml_tr_pbmn`

제한:

- 이번 preflight 응답은 raw file로 저장하지 않았다.
- 다음 smoke test implementation은 반드시 `_report/raw/YYYY/YYYY-MM-DD/`에 원천 응답을 저장해야 한다.
- 수동 symbol 하나이므로 성과 해석은 금지한다.

## 2.1 Existing Raw Validator Result

2026-06-08에 기존 DI raw 요약 파일로 validator를 실행했다.

결과 문서:

- `_report/quant/research/2026-06-08-data-pipeline-smoke-test-result.md`

판정:

- `000660`, `005930`, `454910` raw JSON은 parser가 읽었다.
- 각 파일은 5개 row만 있어 `lookback=20`의 `ROC`를 계산하지 않았다.
- 결과는 모두 `data-insufficient`다.
- 이 결과는 pipeline의 parser와 insufficient-data 방어 경로만 검증한다.

제한:

- 기존 raw는 `_report/raw/2026/2026-06-05/` 아래 DI 리포트용 요약 파일이다.
- Quant 전용 raw 저장 위치인 `_report/raw/YYYY/YYYY-MM-DD/quant/smoke-test/`를 아직 만들지 않았다.
- 이 결과는 full smoke test 통과가 아니며 Backtest 증거가 아니다.

## 3. Minimal Smoke Test Scope

수동 symbol set은 pipeline 검증용으로만 사용한다.

초기 symbol 후보:

| Symbol | Name | Purpose |
| --- | --- | --- |
| `005930` | 삼성전자 | KOSPI large cap baseline |
| `000660` | SK하이닉스 | KOSPI semiconductor peer |
| `035420` | NAVER | KOSPI growth/tech |

주의:

- 이 symbol set은 Quant Universe가 아니다.
- 이 symbol set은 생존 편향과 선택 편향이 있다.
- 결과 문서 첫머리에 `Data Pipeline Smoke Test - Not Quant Validation`을 표시한다.

## 4. Acceptance Criteria

Smoke test는 다음을 만족하면 통과다.

1. Strategy YAML이 `StrategyFileLoader.validate()`에서 오류 없이 통과한다.
2. 각 symbol의 KIS MCP 호출 전에 `find_api_detail` 확인 로그가 있다.
3. 각 raw response가 `_report/raw/YYYY/YYYY-MM-DD/quant/smoke-test/` 아래에 저장된다.
4. raw response가 JSON parser로 다시 읽힌다.
5. `output2`에서 OHLCV와 거래대금 field를 표준 schema로 변환한다.
6. 최소 `lookback=20`에 대해 `ROC`를 계산한다.
7. `Signal Candidate` 상태를 `BUY candidate`, `SELL candidate`, `HOLD`, `data-insufficient` 중 하나로 표시한다.
8. 비용 모델 file을 결과에 연결한다.
9. 결과 문서에 `manual_smoke_test`와 `hold` 판정을 명시한다.

## 5. Stop Conditions

- KIS MCP API가 실패한다.
- raw response를 저장하지 못한다.
- `output2`가 비어 있다.
- 날짜가 정렬되지 않았거나 중복된다.
- 종가, 거래량, 거래대금 field가 없거나 숫자로 변환되지 않는다.
- `lookback`보다 데이터가 짧다.
- 사용자가 smoke test 결과를 Strategy 성과로 해석하려는 문구가 들어간다.

## 6. Next Implementation

다음 구현은 작은 script 또는 routine으로 한다.

현재 남은 blocker:

- KIS MCP 응답을 `scripts/quant_kis_raw_save.py`로 raw JSON 저장해야 한다.
- 각 symbol별로 최소 21개 daily rows가 필요하다.
- 저장 위치는 `_report/raw/YYYY/YYYY-MM-DD/quant/smoke-test/`로 고정한다.

필수 산출물:

```text
_report/raw/YYYY/YYYY-MM-DD/quant/smoke-test/
  005930.daily.raw.json
  000660.daily.raw.json
  035420.daily.raw.json
  manifest.yaml

_report/quant/research/YYYY-MM-DD-data-pipeline-smoke-test-result.md
```

결과 문서는 `_report/quant/templates/backtest-report.md`를 쓰되, `Universe 정의 방식`은 `manual_smoke_test`로 고정한다.

## 7. Validator

저장된 raw JSON 검증은 다음 script로 수행한다.

```powershell
uv run python scripts/quant_smoke_validate.py `
  --raw-dir _report/raw/YYYY/YYYY-MM-DD/quant/smoke-test `
  --lookback 20 `
  --output _report/quant/research/YYYY-MM-DD-data-pipeline-smoke-test-result.md
```

역할:

- KIS daily raw JSON을 읽는다.
- `output2` 또는 `latest_rows`에서 OHLCV row를 추출한다.
- `stck_bsop_date`, `stck_clpr`, `stck_oprc`, `stck_hgpr`, `stck_lwpr`, `acml_vol` 존재 여부를 확인한다.
- 충분한 row가 있으면 `ROC`와 `Signal Candidate`를 계산한다.
- 충분한 row가 없으면 `data-insufficient`로 표시한다.

이 script는 market data를 조회하지 않는다. 조회와 raw 저장은 MCP/routine 단계에서 별도로 수행한다.
