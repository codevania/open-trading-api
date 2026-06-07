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
  charts/
```

## 기본 루틴

1. `_report/di/watchlist.yaml`이 있으면 우선 사용한다.
2. 없으면 `_report/di/watchlist.example.yaml`을 사용한다.
3. `_report/di/routines/daily-report-routine.md`를 따라 일일 리포트를 작성한다.
4. 원천 응답은 공용 저장소인 `_report/raw/YYYY/YYYY-MM-DD/SYMBOL/`에 저장한다.
5. 사람이 읽는 리포트는 `_report/di/daily/YYYY/YYYY-MM-DD.md`에 저장한다.
6. 판단 변경은 `_report/di/decisions/decision-log.md`에 누적한다.
