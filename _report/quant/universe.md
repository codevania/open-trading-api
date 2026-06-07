# Quant Universe 원칙

## 메타데이터

- 기준일: 2026-06-06
- 상태: Universe v0 정책 정의 완료, 실제 Point-in-Time Universe 미구축
- 용도: 퀀트 Strategy가 사용할 Investable Universe 정의 원칙

## 핵심 원칙

- `_report/di/watchlist.yaml`의 Main, Game, sector watchlist, 관심종목 그룹은 DI 리서치와 일일 관찰용이다.
- 퀀트 Strategy는 기존 관심종목을 기본 Universe로 사용하지 않는다.
- 퀀트 Universe는 종목명에서 시작하지 않고, Strategy가 사전에 정한 Inclusion/Exclusion Rules에서 시작한다.
- 현재 시점에 좋아 보이는 종목을 과거로 소급 적용하면 생존/선택 편향이 생긴다.
- Manual Watchlist를 사용해야 하는 경우에는 "Strategy 검증"이 아니라 "Data Pipeline Smoke Test"로만 표시한다.

## 허용 가능한 Quant Universe 정의 방식

| 방식 | 사용 가능 조건 | 메모 |
| --- | --- | --- |
| 시장 전체 규칙 | KRX 보통주 전체, KOSPI/KOSDAQ 전체 등 사전 규칙이 명확할 때 | 실제 상장/상폐/거래정지 이력 확인 필요 |
| 지수 구성 규칙 | 과거 시점별 편입/편출 데이터가 있을 때 | 현재 구성종목을 과거에 소급 적용 금지 |
| Liquidity Filter | 거래대금, 거래량, 스프레드 기준이 사전에 정해졌을 때 | 결과가 좋은 필터를 사후 선택하지 않음 |
| 업종/테마 규칙 | 업종 분류 기준과 편입 시점이 문서화되어 있을 때 | 현재 유명 테마 대표주를 임의 선정하지 않음 |
| ETF/ETN Universe | 상품 유형과 상장 기간 조건이 명확할 때 | 레버리지/인버스는 별도 Risk 규칙 필요 |

## 금지 또는 제한

- Main/Game/관심종목 그룹을 Quant Universe로 사용하지 않는다.
- 삼성전자, SK하이닉스, NVIDIA, 두산로보틱스 같은 현재 관심종목만으로 Strategy Alpha를 주장하지 않는다.
- 현재 생존 종목, 현재 지수 구성종목, 현재 테마 대표주만으로 과거 Backtest를 수행하지 않는다.
- 종목명이 불명확한 항목을 임의 티커로 대체하지 않는다.
- 한 Strategy가 잘 맞는 종목만 골라 다시 Universe를 정의하지 않는다.

## 001-strategy-universe-momentum Universe v0

이 Strategy의 Universe v0는 "관심종목 모멘텀"이 아니라 "사전에 고정된 Rule-Based Universe에서의 Momentum 기준선"이다.

### Definition

- Universe Version: `v0`
- Market: `KRX`
- Venue: `KOSPI`, `KOSDAQ`
- Security Type: `common_stock`
- Manual Watchlist: 사용 안 함. 필요한 경우 `Data Pipeline Smoke Test`로만 표시한다.
- Interpretation Status: Point-in-Time Investable Universe 미구축으로 Backtest 성과 판정은 `hold` 이하.

### Inclusion Rule

- Rebalance date 기준 KRX `KOSPI` 또는 `KOSDAQ` 상장 보통주다.
- Rebalance date 기준 정상 거래 가능 상태다.
- Listing Age가 최소 `252 trading days` 이상이다.
- 최근 `20 trading days` 평균 거래대금이 최소 `1,000,000,000 KRW` 이상이다.
- 일봉 OHLCV가 최소 `600 trading days` 이상 확보되어 있다.
- 종가, 거래량, 거래대금 계산에 결측 또는 비정상 값이 없다.

### Exclusion Rule

- ETF, ETN, ELW, preferred share, SPAC, REIT, closed-end fund, infrastructure fund.
- 관리종목, 투자주의/경고/위험, 거래정지, 상장폐지 예정 등 거래 가능성이나 체결 품질이 훼손된 종목.
- Main/Game/DI watchlist에서 수동 선택되었다는 이유만으로 포함된 종목.
- 종목 코드가 확인되지 않은 항목.
- 원천 데이터 응답이 비정상인 항목.
- Lookback, Liquidity Filter, Listing Age 계산에 필요한 과거 데이터가 부족한 항목.

### Point-in-Time Rule

- Universe 포함 여부, Listing Age, 거래 가능 상태, Liquidity Filter는 모두 해당 Rebalance date 기준으로 계산해야 한다.
- 현재 생존 종목 목록이나 현재 테마 대표주를 과거에 소급 적용하지 않는다.
- 과거 상장폐지, 거래정지, 편입/편출 이력을 확보하지 못하면 결과 문서의 Bias Control 최종 판정은 `hold`로 둔다.
- 현재 기준 종목 목록으로 실행한 결과는 성과 증거가 아니라 `Data Pipeline Smoke Test`다.

### Signal Timing Rule

- Signal은 장마감 후 확정된 end-of-day 데이터로 계산한다.
- Entry/Exit 후보는 다음 거래 세션부터 실행 가능하다고 가정한다.
- 뉴스, 공시, 수급 데이터를 붙일 경우 Signal 계산 시점 전에 공개되어 실제로 사용 가능했던 데이터만 사용한다.

## 다음 확인

1. KRX 보통주 전체 또는 지수별 point-in-time 구성 데이터를 확보할 수 있는지 확인한다.
2. 상장폐지, 거래정지, 관리종목, 투자주의/경고/위험 이력을 어떤 원천에서 가져올지 정한다.
3. Manual Watchlist smoke test가 필요하면 결과 문서에 "퀀트 검증 아님"을 명시한다.
