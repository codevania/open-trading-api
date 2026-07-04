# DI Research Setup - 2026-07-05

## 목적

재량투자에서 KIS MCP, KRX, DART, SEC EDGAR, ETF 원천자료를 역할별로 나눠 쓰기 위한 설정 메모다.

## 환경 파일

로컬 전용:

- `.env.krx`: `KRX_AUTH_KEY`
- `.env.dart`: `OPENDART_API_KEY`
- `.env.sec`: `SEC_USER_AGENT`

커밋 가능한 예시:

- `.env.krx.example`
- `.env.dart.example`
- `.env.sec.example`

실제 키와 개인 연락처는 커밋하지 않는다.

## 데이터 소스 구분

| 영역 | 기본 원천 |
|---|---|
| 시세/차트/수급 | KIS MCP |
| KRX 시장/상장/ETF 기초 데이터 | KRX OpenAPI |
| 국내 공시/재무제표 | OpenDART |
| 미국 공시/재무제표 | SEC EDGAR |
| ETF 구성/비용/분배 | 운용사, KRX, KIS 보조 |

## 루틴

- [[_report/di/routines/company-research-routine|_report/di/routines/company-research-routine.md]]
- [[_report/di/routines/etf-research-routine|_report/di/routines/etf-research-routine.md]]

## 템플릿

- `_report/di/templates/research/thesis.md`
- `_report/di/templates/research/financials.md`
- `_report/di/templates/research/valuation.md`
- `_report/di/templates/research/decision.md`
- `_report/di/templates/research/etf-checklist.md`

## 다음 구현 후보

1. OpenDART 수집 스크립트: 회사 고유번호, 공시목록, 전체 재무제표 저장
2. SEC EDGAR 수집 스크립트: ticker-CIK, submissions, companyfacts 저장
3. ETF 비교 스크립트: KIS ETF/ETN API와 운용사 수동 입력을 합친 체크리스트 생성
4. DI watchlist에 미국 기술주와 Core ETF 후보 추가
