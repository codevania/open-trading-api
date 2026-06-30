# DI Daily Report Quant Signal Section Proposal

## Metadata

- 작성일: 2026-06-08
- 작성자: Codex
- 대상 문서: [[_report/di/templates/daily-report|_report/di/templates/daily-report.md]]
- 현재 판정: proposal
- 목적: DI 일일 리포트에서 Quant Signal을 관찰하되, 재량 투자 판단과 Strategy 검증을 섞지 않는다.

## 1. Decision Boundary

DI 리포트의 Main/Game/관심종목은 Quant Universe가 아니다.

Quant Signal 섹션은 다음 역할만 맡는다.

- Strategy Signal Candidate 관찰
- 데이터 품질 이슈 기록
- Signal와 실제 가격 흐름의 paper tracking
- Strategy 검증 단계의 진행 상황 기록

Quant Signal 섹션은 다음 역할을 맡지 않는다.

- 매수/매도 지시
- DI 관찰종목 추천
- 보유 종목 평가
- 현재 watchlist 성과 주장
- Quant Universe 확정

## 2. Recommended Section

DI 일일 리포트 템플릿에 추가한다면 다음 블록을 권장한다.

```markdown
## Quant Signal Candidates

> 검증 전 Quant Signal은 paper tracking 전용이다. Main/Game/DI watchlist는 Quant Universe가 아니다.

| Strategy | Universe Mode | Signal Status | Evidence | Invalidator | Action |
| --- | --- | --- | --- | --- | --- |
| `001-strategy-universe-momentum` | `manual_smoke_test` 또는 `point_in_time_pending` | BUY candidate / SELL candidate / HOLD / data-insufficient | ROC, close, volume, data source | data anomaly, ROC reversal, hypothesis break | paper tracking only |
| `002-strategy-universe-short-term-reversal` | `manual_smoke_test` 또는 `point_in_time_pending` | BUY candidate / SELL candidate / HOLD / data-insufficient | SMA divergence, close, volume, data source | falling knife, liquidity gap, data anomaly | paper tracking only |

Data Quality:

- raw source:
- missing rows:
- duplicated dates:
- Point-in-Time Universe status:

Decision:

- `no action`: 검증 전 실제 매매 없음
```

## 3. Required Language

다음 문구는 유지한다.

- `paper tracking only`
- `manual_smoke_test`
- `data-insufficient`
- `Point-in-Time Universe pending`
- `not investment advice`

다음 문구는 금지한다.

- `매수 추천`
- `확정 Signal`
- `성과 검증 완료`
- `Alpha 확인`
- `현재 watchlist backtest`

## 4. When To Add To DI Template

DI 템플릿에 실제 반영하는 시점은 다음 중 하나가 충족될 때로 둔다.

1. 사용자가 DI 템플릿의 현재 변경 내용을 정리하거나 merge한다.
2. Quant smoke-test raw가 최소 21개 daily rows로 저장된다.
3. 일일 리포트에서 paper Signal tracking을 실제로 시작한다.

현재는 [[_report/di/templates/daily-report|_report/di/templates/daily-report.md]]에 별도 사용자 변경이 있으므로, 이 제안 문서는 Quant 쪽에만 보관한다.

## 5. Current Recommendation

현재 권장:

- DI 템플릿 직접 수정: 보류
- Quant 쪽 제안 문서: 완료
- 다음 작업: full smoke-test raw 확보 후 DI 리포트에 `Quant Signal Candidates` 섹션을 추가할지 재검토
