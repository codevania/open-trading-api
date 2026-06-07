# 투자 리포트 시작페이지

이 파일은 `_report/`의 시작페이지다. 일반/재량 투자는 `DI`, 퀀트 검증은 `Quant`, 원천 응답은 `raw`에서 출발한다.

## 바로가기

| 목적 | 파일 |
| --- | --- |
| DI 최신 일일 리포트 | [di/daily/2026/2026-06-05.md](di/daily/2026/2026-06-05.md) |
| DI 결정 로그 | [di/decisions/decision-log.md](di/decisions/decision-log.md) |
| DI 일일 리포트 생성 루틴 | [di/routines/daily-report-routine.md](di/routines/daily-report-routine.md) |
| DI 자동화 등록 프롬프트 | [di/routines/codex-automation-prompt.md](di/routines/codex-automation-prompt.md) |
| DI 일일 리포트 템플릿 | [di/templates/daily-report.md](di/templates/daily-report.md) |
| DI 공개 관찰종목 예시 | [di/watchlist.example.yaml](di/watchlist.example.yaml) |
| Quant 준비 로드맵 | [quant/README.md](quant/README.md) |
| Quant 리서치 루틴 | [quant/routines/quant-research-routine.md](quant/routines/quant-research-routine.md) |
| Market Regime Scan 루틴 | [quant/routines/market-regime-scan-routine.md](quant/routines/market-regime-scan-routine.md) |
| 공용 원천 데이터 | [raw/](raw/) |
| 리포트 운영 설명 | [README.md](README.md) |

## 영역 구분

| 영역 | 의미 | 주요 산출물 |
| --- | --- | --- |
| DI | Discretionary Investing, 일반/재량 투자 | watchlist, daily report, decision log, thesis |
| Quant | Strategy 검증 | Universe, Strategy Spec, Backtest, Bias Control |
| Raw | 공용 원천 데이터 | KIS/API JSON, 조회 요약 |

## DI 작성 흐름

1. [DI 일일 리포트 생성 루틴](di/routines/daily-report-routine.md)을 기준으로 작업한다.
2. `_report/di/watchlist.yaml`에서 오늘 추적할 종목을 확인한다.
3. KIS MCP로 현재가, 일봉, 수급, 뉴스/공시 데이터를 조회한다.
4. 필요하면 원천 JSON을 `_report/raw/YYYY/YYYY-MM-DD/SYMBOL/`에 저장한다.
5. `_report/di/templates/daily-report.md`를 복사해 `_report/di/daily/YYYY/YYYY-MM-DD.md`를 작성한다.
6. 매수/매도/관망/확인 필요 판단은 `_report/di/decisions/decision-log.md`에 누적한다.

## Quant 작성 흐름

1. [Quant 리서치 루틴](quant/routines/quant-research-routine.md)을 기준으로 작업한다.
2. DI watchlist를 Quant Universe로 사용하지 않는다.
3. Strategy, Universe, Backtest, Bias Control은 `_report/quant/` 아래에 남긴다.
4. 검증 전 Signal은 매매 Signal이 아니라 `Signal Candidate`로만 기록한다.

## 작성 원칙

- 사실과 해석을 분리한다.
- 매수/매도 후보에는 항상 실행 조건과 무효화 조건을 적는다.
- 확실하지 않은 종목명은 임의로 매칭하지 않는다.
- 계좌번호, 토큰, API 키, 실제 보유수량 같은 민감 정보는 커밋하지 않는다.
- 리포트 워크플로우에서는 주문 API를 호출하지 않는다.

## 다음 개선 후보

- `_report/di/watchlist.yaml`을 읽어 매일 리포트 초안을 생성하는 스크립트 추가
- 원천 JSON 자동 저장 규칙 확정
- DI 월간 요약 템플릿 추가
- DI 종목별 장기 투자 thesis 문서 추가
- Quant 첫 Universe 초안 확정
