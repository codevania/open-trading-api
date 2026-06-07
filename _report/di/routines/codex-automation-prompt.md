# Codex 자동화 등록 프롬프트

## 권장 자동화 유형

- 유형: 프로젝트 자동화 권장
- 주기: 평일 16:30
- 시간대: Asia/Seoul
- 실행 위치: 이 저장소의 로컬 프로젝트
- 사용자 지정 cron 후보: `30 16 * * 1-5`

매일 리포트는 파일에 기록이 남으므로 프로젝트 자동화가 기본 선택이다. 스레드의 누적 맥락을 계속 유지하고 싶을 때만 스레드 자동화를 사용한다.

## 자동화 프롬프트

아래 프롬프트를 Codex Automations 생성 화면에 넣는다.

```text
이 저장소에서 _report/di/routines/daily-report-routine.md의 절차를 따라 오늘 기준 데일리 투자 리포트를 작성해줘.

대상 종목은 _report/di/watchlist.yaml이 있으면 그 파일을 우선 사용하고, 없으면 _report/di/watchlist.example.yaml을 사용해줘.

KIS MCP로 조회 가능한 국내 주식은 현재가, 기간별 시세, 투자자 수급을 확인하고, 해외 주식은 가능한 현재가와 기간별 시세를 확인해줘. API 호출 전에는 해당 MCP 도구의 find_api_detail로 파라미터를 확인해줘.

결과는 _report/di/daily/YYYY/YYYY-MM-DD.md에 한국어로 작성하고, 종목별 판단 요약은 _report/di/decisions/decision-log.md에도 누적해줘.

종목명이 불명확하거나 API 데이터가 비정상적이면 추측해서 확정하지 말고 리포트의 데이터 한계 메모에 남겨줘.

실제 주문 API는 호출하지 마.
```

## 수동 테스트 프롬프트

자동화로 등록하기 전에 일반 Codex 스레드에서 아래처럼 한 번 실행해 검증한다.

```text
_report/di/routines/daily-report-routine.md에 따라 오늘 데일리 리포트를 한 번 수동 생성해줘.
```
