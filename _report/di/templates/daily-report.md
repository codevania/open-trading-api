---
날짜: YYYY-MM-DD
시간대: Asia/Seoul
시장:
  - KRX
관찰종목:
  - "005930"
데이터출처:
  - domestic_stock.inquire_price
  - domestic_stock.inquire_daily_itemchartprice
  - domestic_stock.investor_trade_by_stock_daily
  - domestic_stock.news_title
포트폴리오_스냅샷: 미기록
작성자: codex
원천데이터_저장여부: false
---

# 일일 투자 리포트 - YYYY-MM-DD

## 1. 오늘의 결론

- 시장 판단:
- 포트폴리오 판단:
- 가장 중요한 후속 확인:
- 핵심 근거:
- 확실하지 않음:

## 2. 포트폴리오 현황

| 종목코드 | 종목명 | 보유수량 | 평균단가 | 현재가 | 평가손익 | 목표비중 | 메모 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| 005930 | 삼성전자 | - | - | - | - | - | - |

## 3. 시장 배경

- Market Regime: risk-on | neutral | risk-off | high-volatility | event-driven | data-insufficient
- Regime 근거:
- Strategy 영향:
- 지수/업종 흐름:
- 금리/환율/거시 변수:
- 시장 폭/거래대금:
- 확인하지 못한 데이터:

## 4. 관찰종목 요약

| 종목코드 | 종목명 | 현재가/종가 | 등락률 | 거래량 신호 | 수급 신호 | 뉴스/공시 신호 | 판단 |
| --- | --- | ---: | ---: | --- | --- | --- | --- |
| 005930 | 삼성전자 | - | - | - | - | - | 관망 |

## 5. 종목별 그래프와 읽는 법

그래프는 Obsidian Charts 플러그인의 Markdown `chart` 코드블록으로 작성한다. 가격 흐름과 핵심 판단 근거를 먼저 확인하기 위한 보조 자료이며, 종목별 해석은 아래 그래프를 참조해 작성한다.

### 그룹 상대수익률 비교

같은 그룹에 비교 가능한 종목이 2개 이상 있으면 기준일 종가를 100으로 맞춘 상대지수 표와 `chart` 코드블록을 추가한다. 110은 기준일 대비 +10%, 95는 -5%로 읽는다.

| 날짜 | 종목 A 지수 | 종목 B 지수 | 해석 |
| --- | ---: | ---: | --- |
| M/D | 100.00 | 100.00 | 기준일 |
| M/D | - | - | - |

```chart
type: line
labels: [M/D, M/D, M/D, M/D, M/D]
series:
  - title: 종목 A 상대지수
    data: [100, 0, 0, 0, 0]
  - title: 종목 B 상대지수
    data: [100, 0, 0, 0, 0]
xTitle: 거래일
yTitle: 지수 (기준일=100)
yMin: 95
yMax: 125
legendPosition: bottom
tension: 0
```

- 그룹 차트 해석:

### 판단형 차트 후보

아래 차트는 판단을 바꿀 수 있을 때만 선택해서 넣는다. 단순 종가 차트는 가격 기준선 설명에 필요할 때만 사용하고, 기본은 수급·거래량·낙폭처럼 행동 조건과 연결되는 차트를 우선한다.

#### 누적 수급

외국인과 기관 순매수를 합산하거나, 판단에 필요한 투자자 주체를 선택해 누적한다. 일별 막대보다 누적 방향이 중요한 경우 사용한다.

```chart
type: line
labels: [M/D, M/D, M/D, M/D]
series:
  - title: 종목 A 외국인+기관 누적
    data: [0, 0, 0, 0]
  - title: 종목 B 외국인+기관 누적
    data: [0, 0, 0, 0]
xTitle: 거래일
yTitle: 백만주
yMin: 0
yMax: 0
legendPosition: bottom
tension: 0
```

- 누적 수급 해석:

#### 거래량 배율

전일 거래량을 100으로 놓고 당일 거래량이 몇 %인지 표시한다. 하락일에 배율이 커지면 매도 압력 확대 신호로 본다.

```chart
type: line
labels: [M/D, M/D, M/D, M/D]
series:
  - title: 종목 A 거래량 배율
    data: [100, 0, 0, 0]
  - title: 종목 B 거래량 배율
    data: [100, 0, 0, 0]
xTitle: 거래일
yTitle: 전일 대비 %
yMin: 0
yMax: 200
legendPosition: bottom
tension: 0
```

- 거래량 배율 해석:

#### 최근 고점 대비 낙폭

조회 구간에서 각 종목의 고가를 갱신해가며, 당일 종가가 최근 고가 대비 몇 % 내려왔는지 표시한다.

```chart
type: line
labels: [M/D, M/D, M/D, M/D]
series:
  - title: 종목 A
    data: [0, 0, 0, 0]
  - title: 종목 B
    data: [0, 0, 0, 0]
xTitle: 거래일
yTitle: 최근 고가 대비 %
yMin: -20
yMax: 1
legendPosition: bottom
tension: 0
```

- 고점 대비 낙폭 해석:

### 단일 종목 가격 위치

```chart
type: line
labels: [M/D, M/D, M/D, M/D, M/D]
series:
  - title: 삼성전자 종가(만원)
    data: [0, 0, 0, 0, 0]
xTitle: 거래일
yTitle: 만원
yMin: 0
yMax: 100
legendPosition: bottom
tension: 0
```

- 그래프 해석:
- 가격 기준선:
- 거래량/수급 확인:

## 6. 종목별 메모

### 005930 - 삼성전자

**사실**

- 가격/등락:
- 일봉 흐름:
- 그래프 기준:
- 투자자 수급:
- 뉴스/공시:
- 상대강도:
- 근거 출처:

**해석**

- 전문용어 설명:
- 긍정적 측면:
- 부정적 측면:
- 상승 시나리오:
- 기본 시나리오:
- 하락 시나리오:

**행동 후보**

- 판단: 관망
- 진입/추가확인 조건:
- 무효화 조건:
- 주요 리스크:
- 다음 확인:

**후속 질문 후보**

1. 
2. 
3. 

## 7. 오늘의 결정

| 종목코드 | 판단 | 근거 | 실행 조건 | 무효화 조건 | 재검토일 |
| --- | --- | --- | --- | --- | --- |
| 005930 | 관망 | - | - | - | YYYY-MM-DD |

## 8. 원천 데이터 목록

| 종목코드 | API | 원천 파일 | 상태 |
| --- | --- | --- | --- |
| 005930 | inquire_price | `_report/raw/YYYY/YYYY-MM-DD/005930/inquire_price.json` | 대기 |

## 9. 데이터 품질 메모

- 누락 데이터:
- 신뢰도:
- 다음 자동화 후보:

## 10. 정정 이력

- 없음.
