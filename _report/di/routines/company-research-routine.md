# DI Company Research Routine

## Current Gate Order

For satellite equities, do not move directly from `thesis.md` to `decision.md`.

Required order:

1. Collect source evidence: SEC/DART filings, source documents, section maps, and financial summaries.
2. Write `thesis.md` with a clear invalidation rule.
3. Write `valuation.md` with latest price, valuation range, reverse DCF or scenario assumptions, ETF overlap, tax/account route, maximum position size, add/trim rule, and source freshness.
4. Copy [[_report/di/templates/satellite-decision-inputs.example.yaml|satellite-decision-inputs.example.yaml]] to [[_report/private/di/satellite-decision-inputs.yaml|satellite-decision-inputs.yaml]] and fill account-specific or portfolio-specific checks there.
5. Run [[scripts/di_satellite_decision_prep.py|di_satellite_decision_prep.py]] and confirm the candidate is no longer `needs_decision_inputs`.
6. Only then write a checked `decision.md`.
7. Run [[scripts/di_candidate_evidence_check.py|di_candidate_evidence_check.py]] before watchlist or active position review.

This process creates research notes only. It does not create buy, sell, hold, or order intent.

## 목적

재량투자 후보 기업을 같은 절차로 검토하기 위한 루틴이다. KIS MCP는 시세와 수급 확인에 사용하고, 재무제표와 공시는 DART 또는 SEC EDGAR 원문을 우선한다.

이 루틴은 투자 판단 보조 자료를 만드는 절차이며, 자동 주문을 실행하지 않는다.

## 사전 설정

로컬 환경 파일:

- `.env.krx`: KRX OpenAPI 키, 이미 기존 Quant/KRX 수집에서 사용
- `.env.dart`: OpenDART API 키
- `.env.sec`: SEC EDGAR 요청용 User-Agent

환경 변수 이름:

- `KRX_AUTH_KEY`
- `OPENDART_API_KEY`
- `SEC_USER_AGENT`

`.env.dart`와 `.env.sec`는 gitignored 파일이다. 예시 파일은 `.env.dart.example`, `.env.sec.example`을 사용한다.

## 데이터 소스 역할

| 목적 | 국내 기업 | 미국 기업 |
|---|---|---|
| 현재가/일봉/거래량 | KIS MCP `domestic_stock` | KIS MCP `overseas_stock` |
| 수급 | KIS MCP `investor_trade_by_stock_daily` | 기본 제외, 필요 시 별도 출처 |
| 상장/시장 기초정보 | KRX OpenAPI | SEC ticker-CIK 매핑, 거래소 정보 |
| 공시 원문 | DART | SEC EDGAR |
| 재무제표 | OpenDART 정기보고서 재무정보 | SEC XBRL `companyfacts` |
| 기업 설명/IR | 회사 IR, 사업보고서 | 회사 IR, 10-K/10-Q |

## 국내 기업 절차

1. 종목코드를 확정한다.
2. KIS MCP로 현재가, 일봉, 거래량, 수급을 확인한다.
3. KRX OpenAPI로 상장 기초정보와 시장 구분을 확인한다.
4. OpenDART에서 회사 고유번호, 최근 공시목록, 사업보고서, 반기/분기보고서를 확인한다.
5. OpenDART 정기보고서 재무정보에서 매출, 영업이익, 순이익, 자산, 부채, 자본, 현금흐름을 정리한다.
6. 회사 IR 자료가 있으면 최근 실적발표 자료와 사업 설명을 보완한다.
7. `_report/di/templates/research/`의 템플릿을 채운다.

## 미국 기업 절차

1. 티커를 CIK로 매핑한다.
2. SEC `submissions` API에서 최근 10-K, 10-Q, 8-K 제출 이력을 확인한다.
3. SEC `companyfacts` API에서 XBRL 재무데이터를 확인한다.
4. SEC 원문 HTML을 수집하고 10-K에서 Business, Risk Factors, MD&A를 읽는다.
5. 10-Q에서 최근 분기 추세와 가이던스 변화를 확인한다.
6. 8-K에서 실적발표, 주요 계약, 리스크 이벤트를 확인한다.
7. 회사 IR 페이지의 shareholder letter, earnings release, presentation을 보조 자료로 사용한다.
8. `_report/di/templates/research/`의 템플릿을 채운다.

주의: `thesis.md`와 `decision.md`는 파일 존재만으로 완료로 보지 않는다. 핵심 논리/반대 논리/리스크/무효화 조건이 실제 문장으로 채워져야 하며, `decision.md`는 결정 항목 중 하나가 체크되어 있어야 한다.

## SEC EDGAR 최소 조회 URL

SEC API는 인증키가 필요 없지만 `SEC_USER_AGENT`를 요청 헤더에 넣는다.

- 티커-CIK 매핑: `https://www.sec.gov/files/company_tickers.json`
- 제출 이력: `https://data.sec.gov/submissions/CIK##########.json`
- 전체 XBRL facts: `https://data.sec.gov/api/xbrl/companyfacts/CIK##########.json`
- 특정 XBRL concept: `https://data.sec.gov/api/xbrl/companyconcept/CIK##########/us-gaap/Revenues.json`

CIK는 10자리로 zero-padding한다.

## 산출물 위치

기업별 리서치 문서:

```text
_report/di/research/SYMBOL/
  thesis.md
  financials.md
  valuation.md
  decision.md
```

원천 데이터:

```text
_report/raw/YYYY/YYYY-MM-DD/
  dart/SYMBOL/
  sec/SYMBOL/
  krx/SYMBOL/
  kis/SYMBOL/
```

## 수집 스크립트

국내 기업 OpenDART raw 수집:

```bash
python scripts/di_opendart_collect.py --stock-code 005930 --business-year 2025
```

미국 기업 SEC EDGAR raw 수집:

```bash
python scripts/di_sec_edgar_collect.py --ticker MSFT
python scripts/di_sec_filing_summary.py --symbol MSFT --run-date YYYY-MM-DD
python scripts/di_sec_filing_document_collect.py --symbol MSFT --run-date YYYY-MM-DD --form 10-K --form 10-Q --limit-per-form 1
python scripts/di_sec_filing_section_extract.py --symbol MSFT --run-date YYYY-MM-DD
python scripts/di_sec_financials_summary.py --symbol MSFT --run-date YYYY-MM-DD
```

OpenDART/SEC raw 수집 스크립트는 `--dry-run`을 지원하며, 키와 User-Agent는 출력하지 않는다.

`di_sec_filing_summary.py`는 SEC raw JSON을 읽어 `_report/di/research/SYMBOL/sec-filing-summary.md`를 생성한다. 이 요약은 원천 준비 상태를 보는 용도이며 `thesis.md` 또는 `decision.md`를 대체하지 않는다.
XBRL concept snapshot에서 `stale`로 표시된 항목은 최신 10-K/10-Q보다 오래된 태그이므로 재무제표 작성에 그대로 사용하지 않는다.
`di_sec_filing_document_collect.py`는 SEC submissions raw를 읽어 최신 filing 원문 HTML을 `_report/raw/` 아래에 저장하고, `_report/di/research/SYMBOL/sec-filing-documents.md`에 GitHub-safe source map을 남긴다.
`di_sec_filing_section_extract.py`는 저장된 filing HTML에서 Business, Risk Factors, MD&A 텍스트를 `_report/raw/` 아래에 추출하고, `_report/di/research/SYMBOL/sec-filing-sections.md`에 섹션 source map을 남긴다.
`di_sec_financials_summary.py`는 SEC `companyfacts.raw.json`에서 연간/분기 손익, 현금흐름, 재무상태 핵심 지표를 `_report/di/research/SYMBOL/financials.md`로 요약한다.

## 완료 기준

- 투자 논리와 반대 논리가 둘 다 적혀 있다.
- 재무제표 핵심 지표가 최소 3개년 또는 가능한 최신 기간으로 정리되어 있다.
- 밸류에이션은 확정값이 아니라 범위와 가정으로 적혀 있다.
- 매수/보류/제외 판단과 무효화 조건이 있다.
- 원천 출처와 확인일을 남긴다.
- 미국 상장 위성주는 `sec-filing-summary.md`, `sec-filing-documents.md`, `sec-filing-sections.md`, `financials.md`가 먼저 있어야 한다.
- `di_candidate_evidence_check.py`가 빈 템플릿 또는 체크되지 않은 `decision.md`를 계속 `hold`로 판정한다.
