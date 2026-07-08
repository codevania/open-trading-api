# 프로젝트 에이전트 지침

## 목적

이 작업공간은 한국투자증권 Open API / KIS MCP를 활용한 투자 리서치와 포트폴리오 보조 프로젝트다. `_report/`는 장기 투자 일지이자 판단 근거 저장소로 취급한다.

## 리포트 작성 규칙

- 사용자가 "오늘 리포트", "데일리 리포트", "일일 리포트", "장마감 리포트", "루틴 돌려줘"처럼 요청하면 [[_report/di/routines/daily-report-routine|_report/di/routines/daily-report-routine.md]]를 따라 일일 투자 리포트를 생성한다.
- 사용자가 DI/재량 투자/투자 리서치 맥락에서 "오늘 학습", "오늘 공부할 내용", "DI 학습 루틴", "투자 공부 루틴", "매일 학습 내용 만들어줘"처럼 요청하면 [[_report/di/routines/daily-learning-routine|_report/di/routines/daily-learning-routine.md]]를 따라 오늘의 학습 콘텐츠를 만들고 `_report/di/learning/logs/YYYY-MM.md`에 누적한다.
- 일일 리포트는 `_report/di/daily/YYYY/YYYY-MM-DD.md`에 작성한다.
- 원천 MCP/API 응답은 `_report/raw/YYYY/YYYY-MM-DD/` 아래에 저장하고, 사람이 쓴 결론과 분리한다.
- 날짜는 기본적으로 한국시간(Asia/Seoul)을 사용한다. 해외시장 세션을 기준으로 작성할 때만 별도로 명시한다.
- `_report/`에는 계좌번호, 앱키, 토큰, `.env` 내용, 실제 보유수량 같은 민감 정보를 저장하지 않는다.
- 리포트 작성 흐름에서는 실제 주문을 넣지 않는다. 주문 가능 MCP API 호출은 사용자가 별도로 명확히 요청한 경우에만 다룬다.
- KIS MCP API를 호출하기 전에는 반드시 `find_api_detail`로 상세 파라미터를 확인하고, 문서화된 값만 사용한다.
- 모의/테스트 요청이면 지원되는 API에서 `env_dv: demo`를 명시한다.
- 리포트는 투자 판단 보조 자료다. 확정적 투자 조언처럼 쓰지 말고, 가정/불확실성/누락 데이터를 드러낸다.

## 일일 리포트 최소 항목

각 일일 리포트에는 다음을 포함한다.

- 리포트 메타데이터: 날짜, 시장, 관찰종목, 데이터 출처, 작성자
- 포트폴리오 현황 또는 `미기록`
- 시장 배경
- 관찰종목별 섹션
- 현재가, 일봉, 거래량 사실
- 가능한 경우 투자자 수급, 뉴스, 공시, 이상 움직임
- 상승/기본/하락 시나리오
- 행동 후보와 무효화 조건
- 데이터 품질 메모와 다음 확인 항목

## 기본 MCP 데이터 출처

국내주식은 다음 API부터 확인한다.

- `domestic_stock.inquire_price`: 현재가와 기본 시세
- `domestic_stock.inquire_daily_itemchartprice`: 일봉 OHLCV 이력
- `domestic_stock.investor_trade_by_stock_daily`: 종목별 투자자 매매동향
- `domestic_stock.news_title`: 뉴스/공시 제목 스캔

리포트 질문에 꼭 필요할 때만 다른 API를 추가한다.
