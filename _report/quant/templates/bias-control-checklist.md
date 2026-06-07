# 퀀트 Backtest Bias Control 체크리스트

## 메타데이터

- Strategy ID:
- Backtest 결과 문서:
- 검토일:
- 검토자: Codex
- 판정: pass | hold | fail
- Strategy Portfolio 내 역할:
- AI 사용 범위:

## 1. Universe 편향

- [ ] 현재 살아남은 종목만 사용한 Backtest인지 명시했다.
- [ ] 과거 시점에 실제 투자 가능했던 Investable Universe를 사용했는지 확인했다.
- [ ] Main/Game/관심종목 그룹을 Quant Universe로 사용하지 않았다.
- [ ] watchlist 기반 실행이면 성과 검증이 아니라 "Data Pipeline Smoke Test"로만 해석했다.
- [ ] 상장폐지, 편입/편출, 거래정지 종목 누락 가능성을 기록했다.
- [ ] 지수 구성종목, 관심종목, 테마 대표주를 현재 시점 기준으로 소급 적용하지 않았다.

판정:

## 2. Lookahead Bias

- [ ] 진입/청산 시점보다 미래의 가격, 지표, 뉴스, 공시를 사용하지 않았다.
- [ ] 리밸런싱과 Signal 계산 시점이 실제 거래 가능 시점과 맞는다.
- [ ] 해외시장 세션 차이와 한국시간 기준 해석을 분리했다.

판정:

## 3. Data Snooping 및 Overfitting

- [ ] 파라미터 후보를 사전에 문서화했다.
- [ ] 가장 좋은 파라미터만 고른 결과를 Strategy 성과로 주장하지 않았다.
- [ ] lookback/threshold 비교는 민감도 분석으로 기록했다.
- [ ] out-of-sample 또는 walk-forward 검증 필요 여부를 기록했다.
- [ ] 반복 Backtest 횟수와 폐기한 아이디어를 기록했다.
- [ ] in-sample 성과와 out-of-sample 성과를 같은 의미로 해석하지 않았다.

판정:

## 4. 데이터 품질

- [ ] 원천 데이터 위치를 기록했다.
- [ ] 결측, 비정상 응답, 짧은 상장기간을 확인했다.
- [ ] KIS MCP/API 호출 시 필요한 경우 `find_api_detail` 확인을 기록했다.
- [ ] JSON/YAML 원천 파일 파싱 검증을 수행했다.
- [ ] 공개 데이터만으로 검증 가능한 가설인지, 비공개/유료 데이터가 필요한 가설인지 구분했다.
- [ ] 공개된 Alpha가 빠르게 소멸할 수 있다는 점을 해석 메모에 남겼다.

판정:

## 5. 시장 및 스트레스 구간

- [ ] 상승장, 횡보장, 하락장 결과를 분리했다.
- [ ] 급락 또는 정책/관세/금리/테마 붕괴 같은 stress period를 확인했다.
- [ ] 과거에 거의 없던 이상 사건에 취약할 수 있다는 out-of-sample 한계를 기록했다.
- [ ] KRX와 NASDAQ 결과를 같은 Benchmark로 섞지 않았다.
- [ ] 시장중립 또는 롱숏 주장은 실제 short 가능성과 비용 검토 전에는 하지 않았다.
- [ ] 매크로 환경 변화가 Strategy 가설을 깨는 조건을 적었다.

판정:

## 6. Position 및 개인 투자 적합성

- [ ] Position 크기와 현금 비중을 Strategy 성과와 분리했다.
- [ ] 개인 투자자가 전액 투입할 필요가 없다는 전제를 기록했다.
- [ ] 총자산 Return 관점에서 Strategy Signal의 비중 한도를 적었다.
- [ ] 정기 현금흐름이 있는 개인 투자자와 목돈 운용자의 차이를 기록했다.
- [ ] Transaction Cost, 세금, Slippage 가정을 명시했다.
- [ ] 주문 API 호출 또는 자동매매 연결이 없는지 확인했다.

판정:

## 7. Strategy 다각화 및 Domain Hypothesis

- [ ] 이 Strategy가 단일 독립 Strategy인지, 다른 Strategy를 보완하는 구성요소인지 명시했다.
- [ ] 같은 데이터와 같은 실패 조건을 가진 Strategy를 여러 개 붙여 분산으로 오해하지 않았다.
- [ ] 경제, 금융, 회계, 산업 구조, 투자자 행동 중 어떤 Domain Hypothesis에 기대는지 적었다.
- [ ] AI가 만든 코드와 투자 가설을 분리해 검토했다.
- [ ] Strategy 성과가 특정 테마, 특정 구간, 특정 종목에만 의존하지 않는지 확인했다.

판정:

## 최종 판정

- pass: 제한사항이 명확하고 결과를 해석할 수 있다.
- hold: 데이터 또는 검증 부족으로 Signal 추적만 가능하다.
- fail: 성과 해석이 편향되거나 단일 Strategy/AI 생성 로직을 과신할 가능성이 커서 Strategy 검토를 중단한다.

최종 판정:

메모:
