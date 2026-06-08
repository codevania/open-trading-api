# 퀀트 트레이딩 준비 로드맵

## 현재 원칙

이 폴더는 퀀트 Strategy를 바로 주문으로 연결하기 전에, Strategy 아이디어와 검증 근거를 남기는 준비 공간이다.

- 첫 단계는 자동 주문이 아니라 Signal 생성과 검증이다.
- Universe는 `_report/di/watchlist.yaml`을 기본값으로 사용하지 않는다.
- `_report/di/watchlist.yaml`의 Main, Game, 관심종목 그룹은 DI 리서치와 일일 관찰용이며 퀀트 후보군이 아니다.
- 퀀트 Universe는 `_report/quant/universe.md`와 Strategy별 Inclusion/Exclusion Rules에서 정의한다.
- KIS MCP/API 원천 응답은 `_report/raw/YYYY/YYYY-MM-DD/` 아래에 보관하고, 해석 문서와 분리한다.
- KIS MCP 데이터 호출 전에는 기존 리포트 규칙과 같이 `find_api_detail`로 파라미터를 확인한다.
- 주문 가능 API는 사용자가 명확히 요청하기 전까지 이 흐름에서 제외한다.
- Strategy 결론은 확정적 투자 조언이 아니라 가정, 데이터 품질, 무효화 조건을 포함한 판단 보조 자료로 쓴다.
- AI는 코딩, 정리, 검증 자동화 보조로 사용하고 직접 종목 예측 근거로 쓰지 않는다.
- 단일 Strategy Backtest가 좋아도 포트폴리오 Alpha로 주장하지 않는다. Strategy 간 실패 조건이 다른지 확인한다.
- 현재 관심종목을 과거에 소급 적용한 결과는 퀀트 성과가 아니라 Data Pipeline Smoke Test로만 해석한다.
- 모든 Strategy는 경제/금융 Domain Hypothesis, Position 제약, 전체 자산 내 역할을 함께 기록한다.

## 산출물 구조

```text
_report/quant/
  README.md                              # 준비 로드맵
  learning-roadmap.md                    # 초보자 학습 로드맵
  glossary.md                            # 핵심 용어 표준
  universe.md                            # Quant Universe 원칙
  research/
    2026-06-06-ai-quant-video-analysis.md # AI 퀀트 영상 분석과 Strategy 반영
    YYYY-MM-DD-market-regime-scan.md      # 시장 환경 스캔 결과
    2026-06-07-point-in-time-universe-plan.md # Point-in-Time Universe 확보 계획
    2026-06-07-krx-raw-sample-audit.md    # KRX raw sample 확보 가능성 audit
    2026-06-08-krx-manual-snapshot-procedure.md # KRX manual snapshot 절차
    2026-06-08-transaction-cost-slippage-assumptions.md # 비용/Slippage/Tax 가정
    2026-06-08-out-of-sample-walk-forward-plan.md # OOS/walk-forward 검증 구간
    2026-06-08-data-pipeline-smoke-test-plan.md # smoke test 기준
    2026-06-08-data-pipeline-smoke-test-result.md # 기존 DI raw 기반 validator 결과
    2026-06-08-position-sizing-capital-allocation-policy.md # Position/Capital 정책
  routines/
    kis-raw-save-routine.md              # KIS MCP raw 저장 절차
    quant-research-routine.md            # Strategy 검증 절차
    market-regime-scan-routine.md        # 시장 환경 필터 절차
  templates/
    strategy-spec.md                     # Strategy Spec 템플릿
    backtest-report.md                   # Backtest 결과 템플릿
    bias-control-checklist.md            # Bias Control 체크리스트
    krx-manual-snapshot-manifest.yaml    # KRX 수동 snapshot manifest 템플릿
    market-regime-scan.md                # 시장 환경 필터 템플릿
    study-log.md                         # 주간 학습 로그 템플릿
  strategies/
    001-strategy-universe-momentum.md    # 첫 후보 Strategy Spec
    001-strategy-universe-momentum.kis.yaml # Backtester/Strategy Builder용 Strategy config
    001-strategy-universe-momentum.bias-control.md # Strategy별 Bias Control 판정
    002-strategy-universe-short-term-reversal.md # 두 번째 후보 Strategy Spec
    002-strategy-universe-short-term-reversal.kis.yaml # mean_reversion 후보 config
    002-strategy-universe-short-term-reversal.bias-control.md # 002 Bias Control 판정
```

연결 루틴: `_report/quant/routines/quant-research-routine.md`

KIS raw 저장 루틴: `_report/quant/routines/kis-raw-save-routine.md`

Smoke test validator: `scripts/quant_smoke_validate.py`

KIS raw 저장 helper: `scripts/quant_kis_raw_save.py`

시장 환경 루틴: `_report/quant/routines/market-regime-scan-routine.md`

학습 루틴: `_report/quant/learning-roadmap.md`

## 단계별 계획

### 0단계: Universe 기준 정리

- Main/Game/관심종목 그룹은 Quant Universe에서 제외한다.
- Strategy별 Universe는 종목명이 아니라 Inclusion/Exclusion Rules으로 정의한다.
- 첫 후보 Universe는 `KRX common_stock + Listing Age + Liquidity Filter`로 고정했다.
- 보유 수량, 계좌번호, 앱키, 토큰은 `_report/`에 기록하지 않는다.
- Backtest 전에는 종목 코드, 시장, 데이터 기간, 결측 여부를 확인한다.

완료 기준: Strategy가 사용할 Universe와 데이터 출처가 문서에 명시되어 있다.

현재 상태: 완료. Point-in-Time 확보 계획, KRX raw sample audit, manual snapshot 절차는 작성했지만, 재현 가능한 공식 source snapshot은 미확보이므로 Backtest 해석은 `hold` 이하로 둔다.

### 1단계: 첫 Strategy Spec

- 단순하고 설명 가능한 Strategy부터 시작한다.
- 첫 후보는 `001-strategy-universe-momentum`이다.
- 기존 Backtester의 `momentum` 프리셋과 호환되는 `.kis.yaml`을 함께 둔다.
- 첫 Strategy는 단독 운용 Strategy가 아니라 검증 절차를 세우는 기준선으로 둔다.

완료 기준: 진입, 청산, Risk, 파라미터, 무효화 조건이 문서화되어 있다.

### 1.25단계: Market Regime Scan 기준

- Market Regime은 Strategy Signal을 직접 만들지 않고 실행 환경과 Risk Filter만 설명한다.
- 기본 분류는 `risk-on`, `neutral`, `risk-off`, `high-volatility`, `event-driven`, `data-insufficient`로 둔다.
- Perplexity Finance 같은 요약 화면은 Idea Source 또는 News/Event Filter로만 사용한다.
- 수치 판단은 가능한 한 공식/브로커/검증 가능한 공개 데이터로 교차 확인한다.
- 일일 리포트에는 한 줄 요약과 Strategy 영향만 옮기고, 자세한 원천은 `_report/quant/research/YYYY-MM-DD-market-regime-scan.md`에 남긴다.

완료 기준: `_report/quant/templates/market-regime-scan.md` 형식으로 시장 환경 판단과 Strategy 영향이 기록되어 있다.

### 1.5단계: Strategy 다각화 기준

- Strategy 분산은 종목 분산과 다르다. 같은 데이터, 같은 테마, 같은 실패 조건이면 분산으로 보지 않는다.
- 두 번째 Strategy는 momentum과 다른 Domain Hypothesis를 가져야 한다.
- 후보군은 `volatility_breakout`, `mean_reversion`, `event_filter`, `regime_filter` 중 하나로 제한한다.

완료 기준: 두 번째 Strategy 후보의 가설과 실패 조건이 첫 Strategy와 다르다는 점이 문서화되어 있다.

### 2단계: 데이터 준비

- 일봉 OHLCV는 KIS MCP의 일봉 조회 또는 Backtester 데이터 수집 흐름으로 확보한다.
- 원천 응답을 `_report/raw/`에 저장할 때는 사람이 쓴 결론과 섞지 않는다.
- 결측, 거래정지, 상장기간 부족, 해외시장 세션 차이는 데이터 품질 메모에 남긴다.
- 역사적 투자 가능 유니버스 또는 point-in-time 대체 규칙이 없으면 성과 주장을 보류한다.
- 공개 데이터만으로 검증 가능한 가설인지, 비공개/유료 데이터가 필요한 가설인지 분리한다.

완료 기준: 최소 2년 이상 또는 Strategy lookback의 10배 이상 데이터가 확보되어 있다.

### 3단계: Backtest

- Backtester의 preset 또는 `.kis.yaml` import 흐름으로 실행한다.
- 기본 지표는 Total Return, CAGR, MDD, Sharpe, 승률, 거래 횟수, Turnover를 기록한다.
- Benchmark는 KOSPI, KOSDAQ, 또는 해당 종목 buy-and-hold 중 Strategy 성격에 맞게 정한다.
- Bias Control 체크리스트를 붙이고, Survivorship Bias, Lookahead Bias, Data Snooping, Overfitting 여부를 먼저 판정한다.
- Manual Watchlist만 쓴 결과는 성과 증거가 아니라 Data Pipeline Smoke Test로만 해석한다.
- in-sample과 out-of-sample을 분리하지 못하면 결과 판정은 `hold` 이하로 둔다.
- 급락, 정책/관세 충격, 금리 충격, 테마 붕괴 같은 stress period를 별도 해석한다.

완료 기준: `_report/quant/templates/backtest-report.md` 형식으로 결과가 남아 있다.

### 4단계: 리포트 Signal 추적

- 검증 통과 전에는 매매가 아니라 일일 리포트의 "퀀트 Signal" 섹션으로만 추적한다.
- Signal이 발생한 날에는 근거 데이터, 행동 후보, 무효화 조건을 같이 적는다.
- 판단 변경만 `_report/di/decisions/decision-log.md`에 누적한다.

완료 기준: 최소 몇 주간 Signal와 실제 가격 흐름을 수동으로 비교했다.

### 5단계: 실행 검토

- 모의투자 또는 주문 API 연동은 별도 명시 요청이 있을 때만 다룬다.
- 자동 주문 전에 API 권한, 주문 단위, 호가 공백, Slippage, 실패 복구, 중복 주문 방지 조건을 별도 문서화한다.
- 개인 투자자의 Position 크기, 현금 비중, 정기 현금흐름은 Strategy Signal과 분리해 결정한다.

완료 기준: 주문 전 점검표와 장애 시 중지 조건이 문서화되어 있다.

## 다음 작업 큐

1. `learning-roadmap.md` 1주차를 진행하고 `templates/study-log.md`로 첫 학습 로그를 남긴다.
2. `templates/market-regime-scan.md`로 첫 Market Regime Scan을 작성한다.
3. KRX 웹 UI에서 사람이 수동 CSV를 내려받고 `_report/quant/templates/krx-manual-snapshot-manifest.yaml` 형식으로 `manual_snapshot` manifest를 작성한다.
4. Transaction Cost, Slippage, 세금 가정은 `_report/quant/research/2026-06-08-transaction-cost-slippage-assumptions.md`에 고정했다.
5. Out-of-Sample 또는 walk-forward 구간은 `_report/quant/research/2026-06-08-out-of-sample-walk-forward-plan.md`에 고정했다.
6. Manual symbol 기반 실행은 `_report/quant/research/2026-06-08-data-pipeline-smoke-test-plan.md`에 따라 smoke test로만 실행한다.
7. Smoke test raw validator 결과는 `_report/quant/research/2026-06-08-data-pipeline-smoke-test-result.md`에 기록했다. 기존 DI raw 요약은 5개 row라 모두 `data-insufficient`였고, 성과 해석은 금지한다.
8. KIS MCP raw 저장 routine과 helper는 `_report/quant/routines/kis-raw-save-routine.md`, `scripts/quant_kis_raw_save.py`로 만들었다.
9. 다음 실제 작업은 MCP 응답을 helper로 저장해 `_report/raw/YYYY/YYYY-MM-DD/quant/smoke-test/`에 최소 21개 daily rows를 확보하는 것이다.
10. 개인 투자용 Position 크기, 현금 비중, 전체 자산 내 Strategy 비중은 `_report/quant/research/2026-06-08-position-sizing-capital-allocation-policy.md`에 고정했다.
11. 두 번째 후보 Strategy는 momentum과 다른 가설을 가진 `short_term_reversal` mean_reversion으로 고정했다.
12. 일일 리포트 템플릿에 "퀀트 Signal" 섹션을 추가할지 검토한다.
