# DI Research Setup - 2026-07-05

## Implemented Candidate Comparison

- `scripts/di_etf_compare.py`: renders Core ETF, Korea-listed ETF verification queue, and US tech satellite candidates from `_report/di/candidates/core-satellite-candidates.yaml`
- `scripts/di_candidate_evidence_check.py`: checks whether each candidate has enough issuer, fee, tax/account, thesis, and decision evidence before watchlist promotion
- `scripts/di_etf_source_collect.py`: preserves official ETF issuer source pages from the candidate manifest under ignored raw storage before any facts are copied into research notes
- Stock thesis and decision evidence must contain filled research content; placeholder templates and unchecked decisions remain blocked.
- Suggested output: `_report/di/research/ETF-COMPARISON/etf-checklist.md`
- Evidence gate output: `_report/di/research/ETF-COMPARISON/evidence-gate.md`
- Domestic ETF source URL checks: `_report/di/research/ETF-COMPARISON/domestic-etf-source-url-check.md`
- The candidate manifest is a research queue, not a buy list. Move candidates into `_report/di/watchlist.yaml` only after checklist and decision notes exist.

## Remaining DI Research Setup Work

1. Store issuer factsheet, NAV, fee, distribution, and tax-account evidence for each ETF candidate.
2. Automate a Korea-listed ETF versus US-direct ETF tax/account comparison table.
3. Promote only approved candidates into `_report/di/watchlist.yaml`.

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

1. ETF 비교 스크립트: KIS ETF/ETN API와 운용사 수동 입력을 합친 체크리스트 생성
2. DI watchlist에 미국 기술주와 Core ETF 후보 추가

## 구현된 수집 스크립트

- `scripts/di_opendart_collect.py`: OpenDART 회사 고유번호, 공시목록, 기업개황, 전체 재무제표 raw 저장
- `scripts/di_sec_edgar_collect.py`: SEC ticker-CIK, submissions, companyfacts, 주요 companyconcept raw 저장
- `scripts/di_etf_source_collect.py`: ETF 후보의 공식 운용사 페이지 HTML과 메타데이터를 `_report/raw/YYYY/YYYY-MM-DD/di/etf-sources/` 아래에 저장
