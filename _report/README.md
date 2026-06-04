# 일일 투자 리포트 저장소

`_report/`는 포트폴리오 판단을 매일 누적하는 작업 공간입니다. 목표는 오늘 읽기 쉬운 리포트와 나중에 다시 검증할 수 있는 기록을 함께 남기는 것입니다.

## 폴더 구성

```text
_report/
  START.md                         # 시작페이지
  README.md                        # 운영 설명
  watchlist.example.yaml           # 공개 가능한 관찰종목 예시
  templates/
    daily-report.md                # 일일 리포트 템플릿
  routines/
    daily-report-routine.md        # 매일 리포트 작성 절차
    codex-automation-prompt.md     # Codex Automations 등록용 프롬프트
  daily/
    YYYY/
      YYYY-MM-DD.md                # 날짜별 일일 리포트
  raw/
    YYYY/
      YYYY-MM-DD/
        SYMBOL/
          inquire_price.json
          daily_itemchartprice.json
          investor_trade_by_stock_daily.json
          news_title.json
  summaries/
    monthly/
      YYYY-MM.md                   # 월간 요약
    quarterly/
      YYYY-QN.md                   # 분기 요약
  decisions/
    decision-log.md                # 매수/매도/관망 판단 누적
  research/
    SYMBOL/
      thesis.md                    # 종목별 장기 투자 가설
```

## 매일 작성 흐름

1. 장 마감 전후로 관찰종목을 확인한다.
2. KIS MCP로 현재가, 일봉, 투자자 수급, 뉴스/공시 데이터를 조회한다.
3. 원천 데이터가 필요하면 `_report/raw/YYYY/YYYY-MM-DD/SYMBOL/`에 저장한다.
4. 사람에게 읽히는 리포트는 `_report/daily/YYYY/YYYY-MM-DD.md`에 작성한다.
5. 실제 판단은 `_report/decisions/decision-log.md`에 한 줄로 누적한다.
6. 반복되는 관찰은 월간/분기 요약으로 올린다.

Codex 앱의 Automations에 등록할 때는 `_report/routines/codex-automation-prompt.md`를 사용한다.

## 기본 수집 데이터

국내주식 일일 리포트의 기본 수집 범위는 다음과 같습니다.

- 현재가: 가격, 등락, 거래량, 시가총액 관련 필드
- 일봉: 최소 20거래일, 가능하면 60거래일
- 투자자 수급: 외국인, 기관, 개인 순매수/순매도
- 뉴스/공시 제목: 당일 및 직전 거래일
- 포트폴리오 상태: 보유수량, 평균단가, 목표비중, 리스크 메모

## 파일 이름 규칙

- 일일 리포트: `_report/daily/YYYY/YYYY-MM-DD.md`
- 원천 데이터 폴더: `_report/raw/YYYY/YYYY-MM-DD/SYMBOL/`
- 국내 종목코드: 6자리 숫자, 예: `005930`
- 해외 종목코드: 시장 접두어를 함께 사용, 예: `NAS-NVDA`

## 리포트 품질 기준

- 사실과 해석을 분리한다.
- 누락 데이터는 조용히 건너뛰지 말고 명시한다.
- 매수/매도/관망 후보에는 실행 조건과 무효화 조건을 함께 적는다.
- 나중에 고칠 때는 원문을 몰래 바꾸지 말고 정정 이력을 남긴다.
- 리포트는 투자 판단 보조 자료이며, 확정적인 투자 조언처럼 쓰지 않는다.
