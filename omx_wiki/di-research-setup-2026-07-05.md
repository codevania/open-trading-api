# DI Research Setup - 2026-07-05

## Implemented Candidate Comparison

- [[scripts/di_etf_compare.py|di_etf_compare.py]]: renders Core ETF, Korea-listed ETF verification queue, and US tech satellite candidates from [[_report/di/candidates/core-satellite-candidates.yaml|core-satellite-candidates.yaml]]
- [[scripts/di_candidate_evidence_check.py|di_candidate_evidence_check.py]]: checks whether each candidate has enough issuer, fee, tax/account, thesis, and decision evidence before watchlist promotion
- [[scripts/di_etf_source_collect.py|di_etf_source_collect.py]]: preserves official ETF issuer source pages from the candidate manifest under ignored raw storage before any facts are copied into research notes
- [[scripts/di_satellite_decision_prep.py|di_satellite_decision_prep.py]]: checks primary satellite equities before `decision.md` so valuation, latest price, ETF overlap, tax/account route, position sizing, add/trim rules, and source freshness are not skipped
- Stock thesis and decision evidence must contain filled research content; placeholder templates and unchecked decisions remain blocked.
- Stock valuation evidence must also be filled; TODO-heavy valuation templates remain blocked.
- Account-specific and portfolio-specific decision inputs should be kept in [[_report/private/di/satellite-decision-inputs.yaml|satellite-decision-inputs.yaml]], using [[_report/di/templates/satellite-decision-inputs.example.yaml|satellite-decision-inputs.example.yaml]] as the copy source.
- Suggested output: [[_report/di/research/ETF-COMPARISON/etf-checklist|etf-checklist.md]]
- Evidence gate output: [[_report/di/research/ETF-COMPARISON/evidence-gate|evidence-gate.md]]
- Satellite decision-prep output: [[_report/di/research/ETF-COMPARISON/satellite-decision-prep|satellite-decision-prep.md]]
- Domestic ETF source URL checks: [[_report/di/research/ETF-COMPARISON/domestic-etf-source-url-check|domestic-etf-source-url-check.md]]
- The candidate manifest is a research queue, not a buy list. Move candidates into [[_report/di/watchlist.yaml|_report/di/watchlist.yaml]] only after checklist and decision notes exist.

## Remaining DI Research Setup Work

1. Store issuer factsheet, NAV, fee, distribution, and tax-account evidence for each ETF candidate.
2. Automate a Korea-listed ETF versus US-direct ETF tax/account comparison table.
3. Promote only approved candidates into [[_report/di/watchlist.yaml|_report/di/watchlist.yaml]].

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

- [[_report/di/templates/research/thesis|thesis.md]]
- [[_report/di/templates/research/financials|financials.md]]
- [[_report/di/templates/research/valuation|valuation.md]]
- [[_report/di/templates/research/decision|decision.md]]
- [[_report/di/templates/research/etf-checklist|etf-checklist.md]]

## 다음 구현 후보

1. ETF 비교 스크립트: KIS ETF/ETN API와 운용사 수동 입력을 합친 체크리스트 생성
2. DI watchlist에 미국 기술주와 Core ETF 후보 추가

## 구현된 수집 스크립트

- [[scripts/di_opendart_collect.py|di_opendart_collect.py]]: OpenDART 회사 고유번호, 공시목록, 기업개황, 전체 재무제표 raw 저장
- [[scripts/di_sec_edgar_collect.py|di_sec_edgar_collect.py]]: SEC ticker-CIK, submissions, companyfacts, 주요 companyconcept raw 저장
- [[scripts/di_sec_filing_summary.py|di_sec_filing_summary.py]]: SEC raw JSON에서 최근 10-K/10-Q/8-K와 XBRL concept snapshot을 Markdown으로 요약
- [[scripts/di_sec_filing_document_collect.py|di_sec_filing_document_collect.py]]: SEC raw submissions에서 최신 filing 원문 HTML을 `_report/raw/`에 저장하고 source map Markdown 생성
- [[scripts/di_sec_filing_section_extract.py|di_sec_filing_section_extract.py]]: 저장된 SEC filing HTML에서 Business, Risk Factors, MD&A 섹션을 ignored raw text로 추출하고 source map Markdown 생성
- [[scripts/di_sec_financials_summary.py|di_sec_financials_summary.py]]: SEC companyfacts에서 연간/분기 손익, 현금흐름, 재무상태 요약 Markdown 생성
- [[scripts/di_etf_source_collect.py|di_etf_source_collect.py]]: ETF 후보의 공식 운용사 페이지 HTML과 메타데이터를 `_report/raw/YYYY/YYYY-MM-DD/di/etf-sources/` 아래에 저장
