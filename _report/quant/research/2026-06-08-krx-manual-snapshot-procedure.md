# KRX Manual Snapshot Procedure

## Metadata

- 작성일: 2026-06-08
- 작성자: Codex
- 대상 Strategy: `001-strategy-universe-momentum`
- 대상 Universe: `Universe v0`
- 현재 판정: hold
- Source Mode: `manual_snapshot_procedure_ready`
- 관련 문서:
  - `_report/quant/research/2026-06-07-point-in-time-universe-plan.md`
  - `_report/quant/research/2026-06-07-krx-raw-sample-audit.md`
  - `_report/quant/templates/krx-manual-snapshot-manifest.yaml`

## 1. 목적

KRX 공식 raw endpoint의 비브라우저 자동 POST가 `LOGOUT` 또는 HTTP `400`으로 막힌 상태에서, 수동 다운로드를 어떤 증거 수준으로 인정할지 고정한다.

이 문서는 Backtest를 허용하는 문서가 아니다. 수동 다운로드가 가능하더라도 결과는 `manual_snapshot`이며, 자동 재현 가능한 `Point-in-Time Investable Universe`가 확보되기 전까지 Strategy 판정은 `hold`다.

## 2. 현재 확인 상태

확인한 KRX 공식 화면:

| Dataset | KRX Page | 목적 | UI 확인 |
| --- | --- | --- | --- |
| `managed_issues_current` | `https://data.krx.co.kr/contents/MDC/STAT/issue/MDCSTAT214.jsp` | 관리종목 현황 | 다운로드 팝업 요소 노출 |
| `managed_issue_designation_history` | `https://data.krx.co.kr/contents/MDC/STAT/issue/MDCSTAT215.jsp` | 관리종목 지정 내역 | 다운로드 팝업 요소 노출 |
| `delisting_events` | `https://global.krx.co.kr/contents/GLB/03/0306/0306050000/GLB0306050000.jsp` | 상장폐지 통계/이벤트 확인 | 공식 Global KRX 페이지 확인 |

제한:

- Codex 인앱 Browser 런타임이 현재 환경에서 시작 단계에 종료되어 실제 다운로드 이벤트는 자동 검증하지 못했다.
- 따라서 이 문서는 `download_verified_by_codex: false`로 시작한다.
- 사람이 브라우저에서 다운로드한 파일을 저장하고 manifest를 작성해야 `manual_snapshot` sample로 인정한다.

## 3. Manual Snapshot 인정 조건

수동 다운로드 파일은 다음 조건을 모두 만족해야 한다.

1. KRX 공식 페이지에서 직접 받은 파일이어야 한다.
2. 파일명, 기준일, 다운로드 시각, 원천 URL을 manifest에 기록해야 한다.
3. SHA-256 hash를 남겨 원본 변경 여부를 확인할 수 있어야 한다.
4. column schema를 manifest에 그대로 적어야 한다.
5. 사람이 쓴 해석 문서와 섞지 않고 `_report/raw/YYYY/YYYY-MM-DD/krx/universe/` 아래에 저장해야 한다.
6. 수동 파일은 `source_mode: manual_snapshot`으로 표시해야 한다.
7. 수동 파일만으로는 Backtest 결과를 `pass`로 올리지 않는다.

## 4. Raw Storage Convention

예시 저장 위치:

```text
_report/raw/2026/2026-06-08/krx/universe/
  managed_issues_current.raw.csv
  managed_issue_designation_history.raw.csv
  delisting_events.raw.csv
  manifest.yaml
```

파일명 규칙:

| File | Required | Notes |
| --- | --- | --- |
| `managed_issues_current.raw.csv` | yes | KRX 관리종목 현황 |
| `managed_issue_designation_history.raw.csv` | yes | KRX 관리종목 지정 내역 |
| `delisting_events.raw.csv` | preferred | KRX 상장폐지 이벤트 또는 Global KRX equivalent |
| `manifest.yaml` | yes | source, fetched_at, hash, schema |

## 5. Manifest 작성 기준

Manifest는 `_report/quant/templates/krx-manual-snapshot-manifest.yaml` 형식을 따른다.

필수 필드:

| Field | Purpose |
| --- | --- |
| `as_of_date` | Snapshot 기준일 |
| `source_mode` | `manual_snapshot` |
| `download_verified_by_codex` | Codex가 다운로드 이벤트까지 검증했는지 |
| `datasets[].source_url` | KRX 공식 페이지 |
| `datasets[].downloaded_at_kst` | 사람이 다운로드한 시각 |
| `datasets[].raw_path` | `_report/raw/...` 상대 경로 |
| `datasets[].sha256` | 원천 파일 hash |
| `datasets[].columns` | 원천 column schema |
| `bias_judgment` | `hold` 유지 여부 |

## 6. Bias Control 판정

현재 판정은 계속 `hold`다.

이유:

- 수동 다운로드는 공식 원천 확인에는 도움이 되지만 자동 재현성은 없다.
- 현재 시점의 관리종목 현황만으로는 과거 Rebalance date별 거래 가능 Universe를 만들 수 없다.
- `Point-in-Time`을 위해서는 상장/상폐/거래정지/관리종목/투자주의 이력이 날짜별로 필요하다.
- OHLCV와 Universe snapshot의 거래일 calendar 충돌 검증도 아직 없다.

`pass`로 올리기 위한 최소 조건은 변하지 않는다.

- 최소 2년 이상 또는 `max_lookback * 10` 이상 기간의 `Point-in-Time` snapshot.
- 상장폐지와 거래정지 이력 누락 audit.
- KRX와 KIS OHLCV calendar 충돌 audit.
- DI watchlist가 Universe 생성 입력으로 섞이지 않았다는 검증 로그.

## 7. Next Action

1. 사람이 KRX 공식 화면에서 CSV를 내려받는다.
2. `_report/raw/YYYY/YYYY-MM-DD/krx/universe/`에 원천 파일을 저장한다.
3. PowerShell에서 `Get-FileHash -Algorithm SHA256`으로 hash를 계산한다.
4. 같은 폴더에 `manifest.yaml`을 작성한다.
5. Codex가 manifest와 raw file schema를 검토한다.
6. 검토가 통과하면 parser 작업으로 넘어가되, Strategy 판정은 계속 `hold`로 둔다.
