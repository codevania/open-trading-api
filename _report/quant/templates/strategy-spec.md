# Strategy Spec 템플릿

## 메타데이터

- Strategy ID:
- Strategy Name:
- 상태: draft | backtesting | paper-signal | retired
- 작성일:
- 최종 수정일:
- 작성자: Codex
- 관련 파일:
- 연결 가능한 `.kis.yaml`:
- 참고 연구/영상:

## 1. Economic/Financial Hypothesis

이 Strategy가 포착하려는 시장 현상을 한 문장으로 적는다.

- 도메인 근거:
- 데이터로 관찰 가능한 현상:
- 기대 효과:
- 실패할 가능성이 높은 시장:
- Strategy가 유리한 시장:
- 가설 무효화 조건:

## 2. Strategy Portfolio 내 역할

- 단일 Strategy로 사용할 수 있는가:
- 보완해야 할 Strategy 유형:
- 기존 Strategy와 다른 실패 조건:
- 같은 테마/같은 데이터에 중복 노출되는 위험:
- 공개된 Alpha가 소멸할 가능성:

## 3. Universe

- 기본 소스: `_report/quant/universe.md`
- Inclusion Rule:
- Exclusion Rule:
- Manual Watchlist 사용 여부: 사용 안 함 | smoke test 전용
- 시장:
- 제외 조건:
- 종목 확인 필요 항목:
- Point-in-Time Investable Universe 확보 여부:
- Main/Game/관심종목 그룹을 사용하지 않는다는 확인:
- Manual Watchlist를 과거에 소급 적용할 때의 생존/선택 편향:

## 4. 데이터 요구사항

- 필수 데이터:
- 선택 데이터:
- 최소 기간:
- 결측 처리:
- 데이터 출처:
- 공개 데이터만으로 검증 가능한가:
- 비공개/유료 데이터 필요 여부:

## 5. 진입 규칙

- 조건:
- 확인 시점:
- 종목 선택 방식:
- 중복 진입 방지:

## 6. 청산 규칙

- 기본 청산:
- 손절:
- 익절:
- 시간 청산:
- 무효화 조건:

## 7. Position 및 Risk

- Position 크기:
- 최대 보유 종목 수:
- 종목당 최대 비중:
- 총 노출 한도:
- 전체 자산 내 목표 비중:
- 현금 비중 및 정기 현금흐름 고려:
- Transaction Cost 가정:
- Slippage 가정:

## 8. Backtest 설정

- 엔진:
- 시작일:
- 종료일:
- Benchmark:
- 리밸런싱 주기:
- 파라미터 범위:
- in-sample 구간:
- out-of-sample 구간:
- stress period:
- 반복 Backtest 및 폐기 아이디어 기록 위치:

## 9. AI 사용 범위

- AI 사용 목적:
- AI가 직접 판단하지 않는 항목:
- 사람이 검토해야 할 항목:

## 10. 통과 기준

- 필수 통과 조건:
- 거부 조건:
- 추가 검토 조건:
- Bias Control 체크리스트 판정:

## 11. 일일 리포트 연결

- Signal 표기 방식:
- 필요한 차트:
- `_report/di/decisions/decision-log.md` 기록 조건:

## 12. 한계와 다음 확인

- 알려진 한계:
- 다음 데이터 확인:
- 다음 실험:
