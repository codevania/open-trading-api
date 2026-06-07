# Point-in-Time Investable Universe 확보 계획

## Metadata

- 작성일: 2026-06-07
- 작성자: Codex
- 대상 Strategy: `001-strategy-universe-momentum`
- Universe Version: `v0`
- 현재 판정: hold
- 목적: `Survivorship Bias`를 줄이기 위해 과거 각 시점에 실제 투자 가능했던 `Investable Universe`를 재구성하는 계획을 고정한다.
- Raw sample audit: `_report/quant/research/2026-06-07-krx-raw-sample-audit.md`
- Manual snapshot 절차: `_report/quant/research/2026-06-08-krx-manual-snapshot-procedure.md`

## 1. Problem Statement

현재 Strategy v0는 `KRX common_stock + Listing Age + Liquidity Filter` 규칙을 고정했지만, 실제 과거 시점별 `Point-in-Time Investable Universe`는 아직 없다.

이 상태에서 현재 살아남은 종목 목록만으로 Backtest를 돌리면 다음 문제가 생긴다.

- 상장폐지 종목이 빠져 `Survivorship Bias`가 생긴다.
- 현재 KOSPI/KOSDAQ 상장 종목을 과거에 소급 적용하는 `Lookahead Bias`가 생긴다.
- 현재 관심종목이나 테마 대표주가 Universe에 들어가면 `Selection Bias`가 생긴다.
- 거래정지, 관리종목, 투자주의/경고/위험 종목을 무시하면 실제 체결 가능성이 과대평가된다.

따라서 이 문서가 완료되기 전까지 `001-strategy-universe-momentum`의 성과 해석은 `hold`다.

## 2. Required Point-in-Time Fields

각 Rebalance date별 Universe snapshot에는 최소한 다음 필드를 남긴다.

| Field | Required | Purpose |
| --- | --- | --- |
| `as_of_date` | yes | Snapshot 기준일 |
| `symbol` | yes | 종목 코드 |
| `isin` | preferred | 종목 식별 안정성 보강 |
| `name` | yes | 사람이 검토할 종목명 |
| `market` | yes | `KRX` |
| `venue` | yes | `KOSPI`, `KOSDAQ` |
| `security_type` | yes | `common_stock` 여부 확인 |
| `listing_date` | yes | `Listing Age` 계산 |
| `delisting_date` | preferred | 상장폐지 종목 포함 및 제외 시점 확인 |
| `trading_status` | yes | 정상 거래 가능 여부 |
| `managed_issue_flag` | yes | 관리종목 제외 |
| `market_alert_flag` | yes | 투자주의/경고/위험 제외 |
| `trading_halt_flag` | yes | 거래정지 제외 |
| `scheduled_delisting_flag` | preferred | 상장폐지 예정 종목 제외 |
| `ohlcv_start_date` | yes | `min_ohlcv_trading_days` 확인 |
| `ohlcv_end_date` | yes | 데이터 커버리지 확인 |
| `avg_trading_value_20d_krw` | yes | `Liquidity Filter` |
| `eligible_universe_v0` | yes | Inclusion/Exclusion 결과 |
| `source` | yes | 원천 출처 |
| `fetched_at_kst` | yes | 수집 시각 |
| `source_hash` | preferred | 원천 파일 변경 감지 |

## 3. Source Priority

### Tier 1: KRX Official Data

우선 원천은 KRX 공식 데이터로 둔다.

- KRX Data Marketplace: `Statistics > Basic Data > Stock > Issue > All listed issues`
- KRX Data Marketplace: `Statistics > Basic Data > Stock > Issue > Summary by issue`
- KRX Data Marketplace: `Statistics > Basic Data > Stock > Details > All listed companies`
- KRX Data Marketplace: `Statistics > Basic Data > Stock > Issue > Designated details of all issues`
- KRX Data Marketplace: `Statistics > Market Measures > Market alert issue > Investment risk issue`
- Global KRX Listing Statistics: `Newly Listed Company`, `Change Listing`, `Delisting`

사용 목적:

- 상장 종목 목록과 시장 구분 확인.
- 종목 유형과 보통주 여부 확인.
- 관리종목, 투자주의/경고/위험, 거래정지, 상장폐지 관련 상태 확인.
- 상장일, 상장폐지일, 편입/편출 이벤트 확인.

주의:

- 웹 화면 기준 스크래핑이 아니라, 재현 가능한 다운로드/API 호출 경로가 확인될 때만 자동화한다.
- KRX 화면 구조나 다운로드 포맷은 바뀔 수 있으므로 수집 스크립트에는 `source_hash`와 schema validation을 붙인다.
- 다운로드가 수동이면 해당 결과는 `manual_snapshot`으로 표시하고, 자동 Backtest 전에는 재현성 검토를 다시 한다.

### Tier 2: KIS MCP Validation Data

KIS MCP는 Universe 원천이라기보다 검증과 OHLCV 보강용으로 사용한다.

- `domestic_stock.search_stock_info`: 종목 기본 정보 검증.
- `domestic_stock.inquire_daily_itemchartprice`: 일봉 OHLCV, 거래량, 거래대금 계산용.
- `domestic_stock.chk_holiday`: 거래일/개장일 calendar 검증.

사용 규칙:

- KIS MCP API를 실제 호출하기 전에는 반드시 `find_api_detail`로 파라미터를 확인한다.
- KIS 응답은 `_report/raw/YYYY/YYYY-MM-DD/` 아래에 저장한다.
- KIS 데이터가 KRX 공식 상태 정보와 충돌하면 KRX 공식 상태 정보를 우선하고, 충돌 내용을 Data Quality 메모에 남긴다.

### Tier 3: Manual Watchlist Smoke Test

`_report/di/watchlist.yaml` 또는 사람이 고른 종목 목록은 Universe 원천으로 쓰지 않는다.

허용되는 경우:

- 데이터 파이프라인이 API 호출, 저장, 파싱, Signal 계산까지 연결되는지 확인하는 `Data Pipeline Smoke Test`.

금지되는 경우:

- Strategy 성과 주장.
- Alpha 주장.
- Backtest 결과의 `pass` 판정.
- 현재 관심종목을 과거에 소급 적용하는 실험.

## 4. Snapshot Storage Plan

원천 데이터와 사람이 쓴 해석은 분리한다.

```text
_report/raw/YYYY/YYYY-MM-DD/krx/universe/
  listed_issues.raw.*
  issue_summary.raw.*
  all_listed_companies.raw.*
  designated_issues.raw.*
  market_alert_issues.raw.*
  delisting.raw.*
  manifest.yaml
```

향후 자동화 산출물은 사람이 검토 가능한 요약만 `_report/quant/` 아래에 둔다.

```text
_report/quant/research/YYYY-MM-DD-point-in-time-universe-audit.md
_report/quant/data/README.md
```

`_report/quant/data/`는 실제 대량 원천 데이터를 저장하는 장소가 아니다. schema, manifest 예시, 작은 sample만 저장한다.

## 5. Eligibility Algorithm v0

각 Rebalance date마다 다음 순서로 계산한다.

1. KRX 기준 전체 listed issues snapshot을 읽는다.
2. `venue in {KOSPI, KOSDAQ}`만 남긴다.
3. `security_type == common_stock`만 남긴다.
4. `Listing Age >= 252 trading days` 조건을 적용한다.
5. 거래정지, 관리종목, 투자주의/경고/위험, 상장폐지 예정 상태를 제외한다.
6. 일봉 OHLCV가 최소 `600 trading days` 이상 있는 종목만 남긴다.
7. 최근 `20 trading days` 평균 거래대금이 `1,000,000,000 KRW` 이상인 종목만 남긴다.
8. 결측, 음수 거래량, 비정상 종가, 비정상 거래대금이 있으면 제외하고 원인을 기록한다.
9. 결과에 `eligible_universe_v0 = true`를 부여한다.

## 6. Bias Judgment Gate

| Status | Condition | Allowed Interpretation |
| --- | --- | --- |
| `pass` | 상장/상폐/거래정지/관리종목/투자주의 이력과 OHLCV가 Rebalance date 기준으로 재현 가능하다. | Backtest 결과 해석 가능 |
| `hold` | Universe 정책은 있으나 Point-in-Time 이력 일부가 없다. | Paper Signal 또는 연구용 결과만 가능 |
| `fail` | 현재 생존 종목, 현재 지수 구성, DI watchlist를 과거에 소급 적용했다. | 성과 해석 중단 |

현재 상태는 `hold`다.

`pass`로 올리기 위한 최소 조건:

- 최소 2년 이상 또는 `max_lookback * 10` 이상 기간의 Point-in-Time snapshot 확보.
- 상장폐지와 거래정지 이력 누락 여부에 대한 audit 작성.
- KRX와 KIS OHLCV 기준일/거래일 calendar 충돌 여부 확인.
- Manual Watchlist가 결과 Universe에 섞이지 않았다는 검증 로그.

## 7. Implementation Sequence

1. KRX 공식 데이터 다운로드/API 경로를 수동으로 확인한다.
2. 필요한 메뉴별 raw sample 1일치를 `_report/raw/` 아래에 저장한다.
3. `manifest.yaml`에 source URL, 기준일, 다운로드 시각, column schema, hash를 기록한다.
4. 작은 parser를 만들어 `listed_issues`, `status_flags`, `delisting_events`, `daily_ohlcv`를 표준 schema로 맞춘다.
5. 1개 기준일에 대해 `eligible_universe_v0`를 산출한다.
6. 20거래일 구간으로 확장해 `Liquidity Filter`와 거래정지 처리가 일관되는지 확인한다.
7. 2년 이상 기간으로 확장한다.
8. Bias Control 문서에서 `Universe Bias`와 `Data Quality` 항목을 갱신한다.

## 8. Stop Conditions

- KRX 원천 데이터 다운로드/API 경로가 재현 불가능하다.
- 상장폐지 또는 거래정지 이력을 확보하지 못한다.
- 종목 유형 구분이 불명확해 `common_stock`을 검증할 수 없다.
- OHLCV와 Universe snapshot의 거래일 calendar가 맞지 않는다.
- 원천 데이터 schema가 바뀌었는데 parser가 이를 감지하지 못한다.
- DI watchlist가 Universe 생성 입력으로 들어간다.

Stop condition이 발생하면 Backtest를 계속하지 않고 Bias Control을 `hold` 또는 `fail`로 둔다.

## 9. Next Action

KRX 공식 데이터 raw sample 자동 확보 가능성은 `_report/quant/research/2026-06-07-krx-raw-sample-audit.md`에서 1차 확인했다.

결론:

- 공식 KRX 웹 페이지와 일부 `bld`는 확인했다.
- 비브라우저 자동 POST endpoint는 `LOGOUT` 또는 HTTP `400`으로 blocked 상태다.
- `finance-datareader` wrapper로 현재 KRX 상장 목록과 상장폐지 목록 보조 sample은 확보했다.
- 단, 이 보조 sample은 `pass` 근거가 아니며 현재 판정은 계속 `hold`다.

다음 실제 작업은 사람이 KRX 웹 UI에서 수동 CSV를 내려받고, `_report/quant/templates/krx-manual-snapshot-manifest.yaml` 형식으로 `manual_snapshot` manifest를 작성하는 것이다.

이 확인이 끝나기 전에는 `001-strategy-universe-momentum`을 성과 Strategy로 보지 않고, `Signal Candidate` 연구 대상으로만 둔다.
