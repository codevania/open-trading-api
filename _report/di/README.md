# DI 리포트 저장소

`DI`는 `Discretionary Investing`의 약어다. 이 폴더는 일반/재량 투자 판단을 종목, 포트폴리오, 일일 리포트 중심으로 기록한다.

Quant와의 경계는 명확히 둔다.

- DI는 관찰종목, 시장 배경, 수급, 뉴스, 행동 후보를 다룬다.
- Quant는 Strategy, Universe, Backtest, Bias Control을 다룬다.
- DI watchlist는 Quant Universe가 아니다.
- DI 판단은 투자 보조 자료이며 자동 주문으로 이어지지 않는다.

## 구조

```text
_report/di/
  watchlist.example.yaml
  watchlist.yaml                  # 개인 관찰종목, git ignore
  templates/
    daily-report.md
    etf-overlap-inputs.example.yaml
    satellite-decision-inputs.example.yaml
  routines/
    daily-report-routine.md
    daily-learning-routine.md
    etf-research-routine.md
    company-research-routine.md
    codex-automation-prompt.md
  daily/
    YYYY/
      YYYY-MM-DD.md
  decisions/
    decision-log.md
  research/
    SYMBOL/
      thesis.md
  learning/
    learning-plan-YYYY-MM-DD.md
    logs/
      YYYY-MM.md
  summaries/
  charts/
```

## 기본 루틴

1. [[_report/di/watchlist.yaml|_report/di/watchlist.yaml]]이 있으면 우선 사용한다.
2. 없으면 [[_report/di/watchlist.example.yaml|_report/di/watchlist.example.yaml]]을 사용한다.
3. [[_report/di/routines/daily-report-routine|_report/di/routines/daily-report-routine.md]]를 따라 일일 리포트를 작성한다.
4. 원천 응답은 공용 저장소인 `_report/raw/YYYY/YYYY-MM-DD/SYMBOL/`에 저장한다.
5. 사람이 읽는 리포트는 `_report/di/daily/YYYY/YYYY-MM-DD.md`에 저장한다.
6. 판단 변경은 [[_report/di/decisions/decision-log|_report/di/decisions/decision-log.md]]에 누적한다.
7. ETF/개별주 후보 승격은 [[_report/di/routines/etf-research-routine|etf-research-routine.md]]와 [[_report/di/routines/company-research-routine|company-research-routine.md]]의 gate를 통과한 뒤에만 검토한다.

## 학습 일지

재량 투자 리서치를 공부하는 기록은 [[_report/di/learning/README|_report/di/learning/README.md]]에 둔다. 학습 일지는 매수/매도 판단이 아니라 개념 이해, 원천 확인, 아직 모르는 항목을 분리하기 위한 기록이다.

사용자가 "오늘 학습", "오늘 공부할 내용", "DI 학습 루틴", "투자 공부 루틴"처럼 요청하면 [[_report/di/routines/daily-learning-routine|_report/di/routines/daily-learning-routine.md]]를 따라 오늘의 학습 콘텐츠를 만들고 월별 로그에 누적한다.

## 작성 원칙

- 전문용어는 등장할 때마다 짧게 풀어 설명한다.
- 사실 주장은 공식 자료, 공시, IR 자료, 기업 보도자료, 거래소/감독기관 자료, 1차 보도를 우선 근거로 붙인다.
- 위키, 커뮤니티, 블로그 요약글은 판단 근거로 사용하지 않는다.
- 확인하지 못한 내용은 `확실하지 않음` 또는 `미확인`으로 표시한다.
- 종목별 해석에는 긍정적 측면, 부정적 측면, 주요 리스크를 항상 함께 둔다.
- 분석이나 리포트 끝에는 다음에 이어서 물어볼 만한 후속 질문 3개를 제안한다.
