# 투자 리포트 저장소

`_report/`는 투자 판단과 검증 근거를 누적하는 작업 공간이다. 루트는 전체 인덱스와 공용 원천 데이터만 담당하고, 실제 투자 흐름은 `DI`와 `Quant`로 분리한다.

- `DI`: Discretionary Investing. 일반/재량 투자 리포트, watchlist, decision log, 종목별 리서치.
- `Quant`: Strategy, Universe, Backtest, Bias Control, Signal Candidate 검증.
- `raw`: DI와 Quant가 함께 참조할 수 있는 원천 데이터 저장소.

## 폴더 구성

```text
_report/
  START.md
  README.md
  di/
    README.md
    watchlist.example.yaml
    watchlist.yaml                  # 개인 관찰종목, git ignore
    templates/
      daily-report.md
    routines/
      daily-report-routine.md
      codex-automation-prompt.md
    daily/
      YYYY/
        YYYY-MM-DD.md
    decisions/
      decision-log.md
    research/
      SYMBOL/
        thesis.md
    summaries/
      monthly/
        YYYY-MM.md
      quarterly/
        YYYY-QN.md
    charts/
  quant/
    README.md
    universe.md
    learning-roadmap.md
    glossary.md
    routines/
      quant-research-routine.md
      market-regime-scan-routine.md
    strategies/
    templates/
    research/
  raw/
    YYYY/
      YYYY-MM-DD/
        SYMBOL/
          inquire_price.json
          daily_itemchartprice.json
          investor_trade_by_stock_daily.json
          news_title.json
```

## DI 작성 흐름

1. 장 마감 전후로 [[_report/di/watchlist.yaml|_report/di/watchlist.yaml]]의 관찰종목을 확인한다.
2. [[_report/di/routines/daily-report-routine|_report/di/routines/daily-report-routine.md]]를 따른다.
3. KIS MCP로 현재가, 일봉, 투자자 수급, 뉴스/공시 데이터를 조회한다.
4. 원천 데이터가 필요하면 `_report/raw/YYYY/YYYY-MM-DD/SYMBOL/`에 저장한다.
5. 사람에게 읽히는 리포트는 `_report/di/daily/YYYY/YYYY-MM-DD.md`에 작성한다.
6. 실제 판단은 [[_report/di/decisions/decision-log|_report/di/decisions/decision-log.md]]에 한 줄로 누적한다.
7. 반복되는 관찰은 `_report/di/summaries/`로 올린다.

Codex 앱의 Automations에 등록할 때는 [[_report/di/routines/codex-automation-prompt|_report/di/routines/codex-automation-prompt.md]]를 사용한다.

## Quant 작성 흐름

1. [[_report/quant/universe|_report/quant/universe.md]]에서 Strategy Universe 원칙을 확인한다.
2. [[_report/quant/routines/quant-research-routine|_report/quant/routines/quant-research-routine.md]]를 따른다.
3. Strategy Spec, Bias Control, Backtest 결과는 `_report/quant/` 안에 남긴다.
4. DI watchlist를 Quant Universe로 사용하지 않는다. 필요하면 Data Pipeline Smoke Test로만 기록한다.
5. 검증 전 항목은 매매 Signal이 아니라 `Signal Candidate`로만 다룬다.

## 공통 원칙

- 사실과 해석을 분리한다.
- 누락 데이터는 조용히 건너뛰지 말고 명시한다.
- 매수/매도/관망 후보에는 실행 조건과 무효화 조건을 함께 적는다.
- 나중에 고칠 때는 원문을 몰래 바꾸지 말고 정정 이력을 남긴다.
- 리포트는 투자 판단 보조 자료이며, 확정적인 투자 조언처럼 쓰지 않는다.
- 계좌번호, 앱키, 토큰, 실제 보유수량 같은 민감 정보는 `_report/`에 저장하지 않는다.
