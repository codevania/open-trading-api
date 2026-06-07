# 001-strategy-universe-momentum Bias Control

## Metadata

- Strategy ID: `001-strategy-universe-momentum`
- Strategy Name: Strategy Universe Momentum Baseline v0
- Backtest 결과 문서: 미작성
- 검토일: 2026-06-07
- 검토자: Codex
- 판정: hold
- Strategy Portfolio 내 역할: 단독 운용 Strategy가 아니라 Momentum 기준선 및 Signal 검증용
- AI 사용 범위: 문서화, Strategy Spec 정리, YAML 작성, 검증 체크리스트 작성 보조
- Point-in-Time 계획: `_report/quant/research/2026-06-07-point-in-time-universe-plan.md`
- Raw sample audit: `_report/quant/research/2026-06-07-krx-raw-sample-audit.md`
- Manual snapshot 절차: `_report/quant/research/2026-06-08-krx-manual-snapshot-procedure.md`
- 비용 가정: `_report/quant/research/2026-06-08-transaction-cost-slippage-assumptions.md`

## 1. Universe Bias

- [x] 현재 살아남은 종목만 사용한 Backtest인지 명시했다.
- [ ] 과거 시점에 실제 투자 가능했던 Investable Universe를 사용했는지 확인했다.
- [x] Main/Game/DI watchlist 그룹을 Quant Universe로 사용하지 않았다.
- [x] watchlist 기반 실행이면 성과 검증이 아니라 `Data Pipeline Smoke Test`로만 해석했다.
- [x] 상장폐지, 편입/편출, 거래정지 종목 누락 가능성을 기록했다.
- [x] 지수 구성종목, 관심종목, 테마 대표주를 현재 시점 기준으로 소급 적용하지 않았다.

판정: hold

메모: Universe v0 정책, Point-in-Time 확보 계획, KRX manual snapshot 절차는 고정했다. KRX raw sample audit에서 비브라우저 직접 endpoint는 blocked였고, wrapper 보조 sample만 확보했다. Codex 인앱 Browser 런타임도 현재 환경에서는 다운로드 이벤트 검증까지 진행하지 못했다. 따라서 공식 source snapshot, 거래정지 이력, 관리종목/투자주의 이력은 아직 확보하지 않은 것으로 판정한다. 성과 Backtest를 해도 투자 근거가 아니라 연구용 `hold` 판정이다.

## 2. Lookahead Bias

- [x] 진입/청산 시점보다 미래의 가격, 지표, 뉴스, 공시를 사용하지 않는 규칙을 적었다.
- [x] Signal 계산 시점은 장마감 후 end-of-day 데이터로 고정했다.
- [x] 실제 진입 가능 시점은 다음 거래 세션으로 고정했다.
- [ ] 해외시장 세션 차이와 한국시간 기준 해석을 분리했다.

판정: hold

메모: 현재 Strategy v0는 KRX 전용으로 둔다. 해외시장 비교를 수행하면 별도 Backtest 결과 문서에서 세션과 통화를 분리해야 한다.

## 3. Data Snooping and Overfitting

- [x] 파라미터 후보를 사전에 문서화했다.
- [x] 가장 좋은 파라미터만 고른 결과를 Strategy 성과로 주장하지 않는다고 명시했다.
- [x] `lookback`, `threshold`, `stop_loss_pct` 비교는 민감도 분석으로 기록한다고 명시했다.
- [ ] Out-of-Sample 또는 walk-forward 검증 구간을 정했다.
- [ ] 반복 Backtest 횟수와 폐기한 아이디어를 기록했다.
- [x] in-sample 성과와 Out-of-Sample 성과를 같은 의미로 해석하지 않는다고 명시했다.

판정: hold

메모: `lookback` 후보는 20, 60, 120, 252로 고정했다. 아직 Backtest 기간과 Out-of-Sample 구간이 정해지지 않았으므로 성과 해석은 보류한다.

## 4. Data Quality

- [x] 원천 데이터 위치를 기록했다.
- [x] 결측, 비정상 응답, 짧은 Listing Age를 확인해야 한다고 명시했다.
- [x] KIS MCP/API 호출 시 필요한 경우 `find_api_detail` 확인을 기록했다.
- [x] JSON/YAML 원천 파일 파싱 검증을 수행한다는 기준을 적었다.
- [x] 공개 데이터만으로 검증 가능한 기준선 Strategy로 분리했다.
- [x] 공개된 Alpha가 빠르게 소멸할 수 있다는 점을 해석 메모에 남겼다.

판정: hold

메모: YAML 파싱은 가능하지만 실제 KIS/KRX 데이터 수집은 아직 수행하지 않았다. Point-in-Time 데이터 원천을 정하기 전에는 `pass`로 올리지 않는다.

## 5. Market and Stress Period

- [ ] 상승장, 횡보장, 하락장 결과를 분리했다.
- [ ] 급락 또는 정책/관세/금리/테마 붕괴 같은 Stress Period를 확인했다.
- [x] 과거에 거의 없던 이상 사건에 취약할 수 있다는 Out-of-Sample 한계를 기록했다.
- [x] KRX와 NASDAQ 결과를 같은 Benchmark로 섞지 않는다고 명시했다.
- [x] Market Neutral 또는 Long-Short 주장은 실제 short 가능성과 비용 검토 전에는 하지 않는다고 명시했다.
- [x] 매크로 환경 변화가 Strategy 가설을 깨는 조건을 적었다.

판정: hold

메모: Stress Period는 Backtest 결과 문서에서 별도로 분리해야 한다. 현 단계에서는 필요한 항목만 정의했다.

## 6. Position and Personal Suitability

- [x] Position 크기와 현금 비중을 Strategy 성과와 분리했다.
- [x] 개인 투자자가 전액 투입할 필요가 없다는 전제를 기록했다.
- [ ] 총자산 Return 관점에서 Strategy Signal의 비중 한도를 적었다.
- [ ] 정기 현금흐름이 있는 개인 투자자와 목돈 운용자의 차이를 기록했다.
- [x] Transaction Cost, 세금, Slippage 가정을 명시했다.
- [x] 주문 API 호출 또는 자동매매 연결이 없는지 확인했다.

판정: hold

메모: 이 Strategy는 아직 `Signal Candidate` 추적용이다. Transaction Cost, Tax, Slippage 기본 가정은 고정했지만 실제 Portfolio 비중과 현금 비중은 별도 Risk 문서에서 정해야 한다.

## 7. Strategy Diversification and Domain Hypothesis

- [x] 이 Strategy가 단일 독립 Strategy가 아니라 기준선 Strategy임을 명시했다.
- [x] 같은 데이터와 같은 실패 조건을 가진 Strategy를 여러 개 붙여 분산으로 오해하지 않는다고 명시했다.
- [x] 투자자 행동과 추세 지속이라는 Domain Hypothesis에 기대고 있음을 적었다.
- [x] AI가 만든 코드와 투자 가설을 분리해 검토했다.
- [ ] Strategy 성과가 특정 테마, 특정 구간, 특정 종목에만 의존하지 않는지 확인했다.

판정: hold

메모: 성과 의존성은 Backtest 이후에만 확인 가능하다. 지금은 Domain Hypothesis와 실패 조건만 문서화한다.

## Final Judgment

최종 판정: hold

판정 근거:

- Universe v0의 Inclusion Rule, Exclusion Rule, Liquidity Filter, Listing Age, Signal Timing은 고정했다.
- DI watchlist와 Quant Universe를 분리했다.
- Survivorship Bias와 Lookahead Bias 방지 기준은 문서화했다.
- 그러나 reproducible official Point-in-Time source snapshot, Out-of-Sample 구간, Stress Period 검증은 아직 미완료다.

사용 가능 범위:

- Strategy Spec 검토: 가능
- Data Pipeline Smoke Test: 가능
- Paper Signal 후보 추적: 제한적으로 가능
- 성과 주장 또는 실매매 근거: 불가
