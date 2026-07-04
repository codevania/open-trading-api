# DI Company Research Routine

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
4. 10-K에서 Business, Risk Factors, MD&A를 읽는다.
5. 10-Q에서 최근 분기 추세와 가이던스 변화를 확인한다.
6. 8-K에서 실적발표, 주요 계약, 리스크 이벤트를 확인한다.
7. 회사 IR 페이지의 shareholder letter, earnings release, presentation을 보조 자료로 사용한다.
8. `_report/di/templates/research/`의 템플릿을 채운다.

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
```

두 스크립트 모두 `--dry-run`을 지원하며, 키와 User-Agent는 출력하지 않는다.

## 완료 기준

- 투자 논리와 반대 논리가 둘 다 적혀 있다.
- 재무제표 핵심 지표가 최소 3개년 또는 가능한 최신 기간으로 정리되어 있다.
- 밸류에이션은 확정값이 아니라 범위와 가정으로 적혀 있다.
- 매수/보류/제외 판단과 무효화 조건이 있다.
- 원천 출처와 확인일을 남긴다.
