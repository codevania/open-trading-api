# 001-strategy-universe-momentum

## 메타데이터

- Strategy ID: `001-strategy-universe-momentum`
- Strategy Name: Strategy Universe Momentum Baseline v0
- 상태: draft
- 작성일: 2026-06-06
- 작성자: Codex
- 관련 YAML: `001-strategy-universe-momentum.kis.yaml`
- 연결 도구: Backtester `momentum` preset
- 참고 분석: `_report/quant/research/2026-06-06-ai-quant-video-analysis.md`
- Bias Control: `_report/quant/templates/bias-control-checklist.md`
- Strategy Portfolio 역할: 단독 운용 Strategy가 아니라 Signal 검증용 기준선

## 1. Economic/Financial Hypothesis

사전에 정의된 Investable Universe 안에서 일정 기간 Return이 양수이거나 상대적으로 강한 종목은 단기적으로 추세가 이어질 가능성이 있다.

- 도메인 근거: 투자자 추종 매수, 실적/테마 기대의 느린 반영, 수급 쏠림이 일정 기간 지속될 수 있다는 가정.
- 데이터로 관찰 가능한 현상: 일정 lookback의 Return, 거래량 변화, 시장 대비 상대강도.
- 기대 효과: 약한 하락 종목을 피하고, 강한 추세 종목만 Signal Candidate로 남긴다.
- 실패 가능성이 높은 시장: 급격한 추세 반전, 뉴스성 갭 하락, 거래대금이 얇은 종목.
- 유리한 시장: 반도체, AI, 대형 성장주처럼 테마 추세가 강하게 이어지는 구간.
- 가설 한계: 가격 모멘텀만으로는 경제/금융 설명력이 약하므로 v0는 Alpha Strategy가 아니라 단순 기준선이다.

## 2. Strategy Diversification 관점

- 이 Strategy는 단일 Strategy로 채택하지 않는다.
- 성과가 좋아도 같은 성장주/AI 테마와 같은 가격 데이터에 반복 노출될 수 있다.
- 다음 후보는 모멘텀과 실패 조건이 다른 Strategy여야 한다. 예: Volatility 축소/확대, 평균회귀, 이벤트 필터, 시장 레짐 필터.
- AI는 이 Strategy의 코드 작성과 검증 보조에만 사용한다. AI의 종목 상승/하락 예측을 진입 근거로 사용하지 않는다.
- 공개된 단순 모멘텀 규칙은 Alpha가 약하거나 이미 소멸했을 수 있으므로, 결과가 좋으면 반드시 Transaction Cost와 Out-of-Sample 검증으로 다시 확인한다.

## 3. Universe

- 기본 소스: `_report/quant/universe.md`
- 시장: 미정. 첫 후보는 KRX 보통주 기반 Rule-Based Universe로 검토한다.
- Inclusion Rule 초안:
  - 보통주
  - 최소 상장기간 충족
  - 최소 거래대금 또는 거래량 충족
  - 데이터 lookback 충족
- 제외 조건:
  - Main/Game/관심종목 그룹에서 수동 선택된 항목
  - 종목 코드가 확인되지 않은 항목
  - 일봉 데이터가 lookback보다 짧은 항목
  - 원천 데이터 응답이 비정상인 항목
- 종목 확인 필요 항목은 임의 티커로 대체하지 않는다.
- 현재 watchlist는 재량 관찰용이므로 Quant Universe가 아니다.
- watchlist만 사용한 실행은 Backtest가 아니라 Data Pipeline Smoke Test로만 해석한다.
- point-in-time Investable Universe가 확보되기 전까지 과거 지수 구성종목이나 현재 테마 대표주를 소급 적용하지 않는다.

## 4. 데이터 요구사항

- 필수 데이터: 일봉 종가, 거래량
- 선택 데이터: 투자자 수급, 뉴스/공시 제목
- 최소 기간: 60거래일 lookback 기준 최소 600거래일 권장
- 데이터 출처: KIS MCP 일봉 조회 또는 Backtester 데이터 수집 결과
- 원천 저장: `_report/raw/YYYY/YYYY-MM-DD/SYMBOL/`
- 공개 데이터만으로 검증 가능한 기준선 Strategy로 둔다.
- 투자자 수급이나 뉴스/공시를 붙일 경우 실제 진입 시점 전에 이용 가능했던 데이터만 사용한다.
- KRX의 상대적 비효율성은 기회일 수 있지만, Strategy Universe와 데이터가 부족하면 성과 주장이 아니라 연구 가설로만 남긴다.

## 5. 진입 규칙

- 60거래일 ROC가 `0%`를 초과하면 매수 후보로 분류한다.
- v0에서는 종목별 단일 Signal만 판단한다.
- 여러 종목 중 순위 선정과 equal weight 포트폴리오 구성은 v1에서 다룬다.
- Signal이 중복 발생하면 기존 보유 Signal을 유지하고 신규 진입으로 중복 기록하지 않는다.

## 6. 청산 규칙

- 60거래일 ROC가 `0%` 아래로 내려가면 청산 후보로 분류한다.
- 손절 기준은 `-10%`로 시작하되, Backtest 결과에 따라 조정한다.
- 뉴스/공시로 가설이 깨진 경우 정량 Signal과 별도로 무효화 조건을 기록한다.
- 손절 기준을 결과가 좋게 보이는 값으로 사후 선택하지 않는다.

## 7. Position 및 Risk

- Position 크기: Backtest 전까지 미정
- 최대 보유 종목 수: v0 미적용, v1에서 `상위 N개` 검토
- 전체 자산 내 목표 비중: 미정. Strategy Signal과 실제 자금 투입은 분리한다.
- 현금 비중: 개인 투자자는 기관처럼 항상 전액 투자할 필요가 없으므로 별도 Risk 문서에서 결정한다.
- Transaction Cost: Backtest 실행 시 명시
- Slippage: Backtest 실행 시 명시
- 주문 연동: 이 단계에서는 제외

## 8. Backtest 설정

- 엔진: Backtester
- Strategy 파일: `001-strategy-universe-momentum.kis.yaml`
- Benchmark: 종목별 buy-and-hold 또는 시장별 대표 지수
- 파라미터:
  - `lookback`: 20, 60, 120, 252
  - `threshold`: 0.0
  - `stop_loss_pct`: 10.0
- 파라미터 비교는 최적값 찾기가 아니라 민감도 분석으로 기록한다.
- KRX와 NASDAQ 결과는 통화, 거래일, 세션, Benchmark 차이를 분리해 해석한다.
- in-sample과 out-of-sample 구간을 분리할 수 없으면 결과 판정은 `hold`로 둔다.
- 반복 Backtest에서 폐기한 파라미터와 아이디어도 결과 문서에 남긴다.

## 9. 통과 기준

- Bias Control 체크리스트 판정이 `fail`이면 Strategy 해석을 중단한다.
- 체크리스트 판정이 `hold`이면 일일 리포트에는 "퀀트 Signal Candidate"로만 기록한다.
- 최소 거래 횟수가 너무 적어 해석 불가능하면 보류한다.
- MDD가 Benchmark보다 과도하게 크면 폐기 또는 Risk 규칙을 재설계한다.
- Return이 좋아도 특정 한 거래나 한 구간에만 의존하면 보류한다.
- 급락, 정책/관세 충격, 금리 충격, AI 테마 붕괴 같은 stress period에서 손실 통제 여부를 별도 확인한다.
- 영상 전문에서 언급된 2025년 상반기 관세 충격 같은 out-of-sample 성격의 사건은 별도 스트레스 메모로 다룬다.
- 단일 Strategy 성과만으로 포트폴리오 편입을 결정하지 않는다.
- 검증 전에는 일일 리포트에 "Signal Candidate"로만 표기한다.

## 10. 일일 리포트 연결

일일 리포트에 반영할 때는 다음 형식으로 기록한다.

```text
퀀트 Signal: 001-strategy-universe-momentum
상태: BUY 후보 | SELL 후보 | HOLD | 데이터 부족
근거: 60거래일 ROC, 종가, 거래량
무효화 조건: ROC 0% 하회, 데이터 오류, 가설 훼손 뉴스/공시
```

`_report/di/decisions/decision-log.md`에는 실제 판단 변경이 있을 때만 누적한다.

### Market Regime 연결

- Market Regime Scan은 이 Strategy의 Entry/Exit Signal을 직접 바꾸지 않는다.
- `risk-off` 또는 `high-volatility`에서는 BUY 후보를 실제 행동 후보가 아니라 `Signal Candidate`로만 추적한다.
- `event-driven`에서는 관련 뉴스/공시가 Momentum 가설을 훼손하는지 무효화 조건에 별도 기록한다.
- `data-insufficient`에서는 Signal 상태를 `데이터 부족`으로 둔다.

## 11. 다음 실험

1. KRX 보통주 기반 Rule-Based Universe 초안을 먼저 확정한다.
2. lookback 20/60/120/252를 비교하되, 최적값 선택이 아니라 민감도와 실패 조건으로 기록한다.
3. point-in-time Investable Universe 확보 계획을 별도 노트로 작성한다.
4. 결과가 의미 있으면 v1에서 상대강도 상위 N개 포트폴리오 규칙을 추가한다.
5. 두 번째 후보 Strategy는 모멘텀과 다른 Domain Hypothesis를 가진 Strategy로 만든다.
