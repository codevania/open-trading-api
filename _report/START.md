# 포트폴리오 리포트 시작페이지

이 파일은 `_report/`의 시작페이지입니다. 매일 리포트를 작성하거나 이전 판단을 되짚을 때 여기서 출발합니다.

## 바로가기

| 목적 | 파일 |
| --- | --- |
| 최신 일일 리포트 | [daily/2026/2026-06-04.md](daily/2026/2026-06-04.md) |
| 결정 로그 | [decisions/decision-log.md](decisions/decision-log.md) |
| 일일 리포트 생성 루틴 | [routines/daily-report-routine.md](routines/daily-report-routine.md) |
| Codex 자동화 등록 프롬프트 | [routines/codex-automation-prompt.md](routines/codex-automation-prompt.md) |
| 일일 리포트 템플릿 | [templates/daily-report.md](templates/daily-report.md) |
| 리포트 운영 설명 | [README.md](README.md) |
| 공개 가능한 관찰종목 예시 | [watchlist.example.yaml](watchlist.example.yaml) |

## 현재 관찰종목

| 종목코드 | 종목명 | 시장 | 상태 | 메모 |
| --- | --- | --- | --- | --- |
| 005930 | 삼성전자 | KRX | 관찰중 | 국내 반도체 대표 관찰 종목 |
| 000660 | SK하이닉스 | KRX | 관찰중 | HBM/메모리 사이클 핵심 관찰 종목 |
| NAS:NVDA | NVIDIA | NASDAQ | 관찰중 | 글로벌 AI 가속기 기준 종목 |
| 확인필요 | 현대 로보틱스 | KRX | 종목 확인 | 정확한 상장 종목코드 확인 필요 |

## 매일 작성 흐름

1. [일일 리포트 생성 루틴](routines/daily-report-routine.md)을 기준으로 작업한다.
2. `_report/watchlist.yaml`에서 오늘 추적할 종목을 확인한다.
3. KIS MCP로 현재가, 일봉, 수급, 뉴스/공시 데이터를 조회한다.
4. 필요하면 원천 JSON을 `_report/raw/YYYY/YYYY-MM-DD/SYMBOL/`에 저장한다.
5. `_report/templates/daily-report.md`를 복사해 `_report/daily/YYYY/YYYY-MM-DD.md`를 작성한다.
6. 매수/매도/관망/확인 필요 판단은 `_report/decisions/decision-log.md`에 누적한다.

## 작성 원칙

- 사실과 해석을 분리한다.
- 매수/매도 후보에는 항상 실행 조건과 무효화 조건을 적는다.
- 확실하지 않은 종목명은 임의로 매칭하지 않는다.
- 계좌번호, 토큰, API 키, 실제 보유수량 같은 민감 정보는 커밋하지 않는다.
- 리포트 워크플로우에서는 주문 API를 호출하지 않는다.

## 다음 개선 후보

- `watchlist.yaml`을 읽어 매일 리포트 초안을 생성하는 스크립트 추가
- 원천 JSON 자동 저장 규칙 확정
- 월간 요약 템플릿 추가
- 종목별 장기 투자 thesis 문서 추가
