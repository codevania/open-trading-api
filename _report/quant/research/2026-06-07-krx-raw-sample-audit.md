# KRX Raw Sample 확보 Audit

## Metadata

- 작성일: 2026-06-07
- 작성자: Codex
- 대상 계획: `_report/quant/research/2026-06-07-point-in-time-universe-plan.md`
- 대상 Strategy: `001-strategy-universe-momentum`
- 현재 판정: hold
- Manual snapshot 절차: `_report/quant/research/2026-06-08-krx-manual-snapshot-procedure.md`

## 1. 목적

`Point-in-Time Investable Universe` 구축을 위해 KRX 공식 원천에서 raw sample을 자동으로 확보할 수 있는지 확인했다.

이번 audit은 Backtest가 아니라 데이터 확보 가능성 점검이다.

## 2. 확인한 공식 Source

- KRX Data Marketplace: `https://data.krx.co.kr/contents/MDC/MAIN/main/index.cmd`
- KRX STAT page: `https://data.krx.co.kr/contents/MDC/STAT/issue/MDCSTAT214.jsp`
- KRX STAT page: `https://data.krx.co.kr/contents/MDC/STAT/issue/MDCSTAT215.jsp`
- Global KRX Delisting page: `https://global.krx.co.kr/contents/GLB/03/0306/0306050000/GLB0306050000.jsp`

## 3. Direct KRX Endpoint Result

### 확인된 bld

| Page | Purpose | bld |
| --- | --- | --- |
| `MDCSTAT214.jsp` | 관리종목 현황 | `dbms/MDC/STAT/issue/MDCSTAT21401` |
| `MDCSTAT215.jsp` | 관리종목 지정 내역 | `dbms/MDC/STAT/issue/MDCSTAT21501` |

### 시도한 Endpoint

- JSON: `https://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd`
- CSV OTP: `https://data.krx.co.kr/comm/fileDn/GenerateOTP/generate.cmd`

### 결과

- Direct JSON POST: blocked
- CSV OTP POST: blocked
- 관찰 에러: `LOGOUT` 또는 HTTP `400 Bad Request`
- 세션 쿠키를 잡기 위해 main page와 STAT page를 먼저 방문해도 동일하게 실패했다.

판정:

- 공식 웹 페이지는 접근 가능하다.
- 하지만 현재 비브라우저 자동 세션에서는 공식 raw POST endpoint 재현성이 확보되지 않았다.
- 이 상태로는 `Bias Control`의 `pass` 조건을 충족하지 못한다.

## 4. Wrapper Sample Result

공식 직접 endpoint가 막혀 있어 보조 경로로 `finance-datareader`를 `uv run --with finance-datareader` 방식으로 일회성 실행했다.

### 확인 결과

| Dataset | Status | Rows Total | Rows Saved | Notes |
| --- | --- | ---: | ---: | --- |
| `KRX` | sample available | 2877 | 20 | 현재 상장 종목 snapshot |
| `KRX-DELISTING` | sample available | 4134 | 20 | 상장폐지 종목 snapshot |

Wrapper 내부 확인:

- `FinanceDataReader` version: `0.9.202`
- `KRX` listing은 `kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13`와 KRX `finder_stkisu` endpoint를 사용한다.
- `KRX-DELISTING`은 wrapper 내부 `_krx_delisting` 경로를 사용한다.

저장 위치:

```text
_report/raw/2026/2026-06-07/krx/universe/
  fdr_krx_listing.sample.json
  fdr_krx_delisting.sample.json
  manifest.sample.json
```

주의:

- `_report/raw/**`는 git ignore 대상이다.
- 이 sample은 파이프라인 탐색에는 유용하지만 공식 KRX raw 직접 다운로드 재현성을 대체하지 않는다.
- 현재 상장 종목 snapshot은 `Point-in-Time` Backtest의 `pass` 근거가 아니다.

## 5. Bias Control 영향

현재 판정은 계속 `hold`다.

이유:

- Direct KRX official raw endpoint가 자동 세션에서 재현되지 않았다.
- Wrapper sample은 현재 상장 종목과 상장폐지 목록의 보조 원천일 뿐이다.
- 거래정지, 관리종목, 투자주의/경고/위험 이력의 날짜별 Point-in-Time snapshot은 아직 확보하지 못했다.
- `eligible_universe_v0` 산출에 필요한 `Source Snapshot` schema와 parser가 아직 없다.

`pass`로 올리려면 다음이 필요하다.

- 공식 KRX 데이터 다운로드를 브라우저/수동/공식 API 중 하나로 재현 가능하게 확보한다.
- 1일치 raw sample의 `manifest`에 source URL, 기준일, fetched_at, hash, column schema를 기록한다.
- `listed_issues`, `delisting_events`, `status_flags`를 같은 기준일 schema로 합친다.
- KIS OHLCV와 거래일 calendar 충돌 여부를 audit한다.

## 6. 다음 액션

1. KRX 웹 UI에서 사람이 수동 CSV를 내려받는다.
2. 수동 다운로드가 가능하면 같은 파일을 `_report/raw/YYYY/YYYY-MM-DD/krx/universe/`에 저장하고 `manifest`를 작성한다.
3. 수동 다운로드만 가능하면 `source_mode: manual_snapshot`으로 표시하고 자동 Backtest는 계속 `hold`로 둔다.
4. 공식 API 또는 안정적인 브라우저 자동화 경로가 확인되면 `source_mode: reproducible_official_snapshot`으로 승격한다.
5. 그 다음에만 `eligible_universe_v0` parser를 만든다.

추가 메모:

- KRX 공식 화면에는 다운로드 팝업 요소가 노출된다.
- 다만 Codex 인앱 Browser 런타임이 현재 환경에서 시작 단계에 종료되어 실제 다운로드 이벤트는 자동 검증하지 못했다.
- 따라서 현재 상태는 `manual_snapshot_procedure_ready`이며, `download_verified_by_codex: false`로 둔다.
