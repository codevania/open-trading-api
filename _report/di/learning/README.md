# DI Learning Journal

이 폴더는 재량 투자 리서치를 이해하기 위한 개인 학습 일지다. 목적은 매수 후보를 바로 고르는 것이 아니라, `_report/di` 리서치 문서가 왜 `hold`인지 스스로 설명할 수 있는 수준까지 올라가는 것이다.

## 위치와 역할

```text
_report/di/learning/
  README.md
  learning-plan-2026-07-08.md
  daily-log-template.md
  logs/
    2026-07.md
```

- [[_report/di/learning/learning-plan-2026-07-08|learning-plan-2026-07-08.md]]: 8주 학습 로드맵과 Day별 과제.
- [[_report/di/learning/daily-log-template|daily-log-template.md]]: 매일 복사해서 쓰는 일지 템플릿.
- `logs/YYYY-MM.md`: 월별 학습 기록. 공부 내용, 질문, 다음 행동을 남긴다.
- [[_report/di/routines/daily-learning-routine|daily-learning-routine.md]]: "오늘 학습" 요청을 처리하는 생성 루틴.

## 운영 원칙

- 하루 30~60분을 기본 단위로 한다.
- 모르는 단어는 넘어가지 말고 `오늘 배운 용어`에 한 줄로 풀어쓴다.
- AI 답변은 초안으로만 취급하고, 공식 자료나 원천 문서로 최소 1개 이상 확인한다.
- 학습 일지는 매수/매도 지시가 아니다. 실제 주문 의도는 기록하지 않는다.
- 후보 승격은 학습 일지가 아니라 `_report/di/research/...`, [[_report/di/research/ETF-COMPARISON/evidence-gate|evidence-gate.md]], [[_report/di/templates/research/decision|decision.md]] 절차를 통과해야 한다.

## 매일 루틴

1. 사용자가 "오늘 학습", "오늘 공부할 내용", "DI 학습 루틴"처럼 요청하면 [[_report/di/routines/daily-learning-routine|daily-learning-routine.md]]를 따른다.
2. 오늘의 Day 과제를 [[_report/di/learning/learning-plan-2026-07-08|learning-plan-2026-07-08.md]]에서 확인한다.
3. 25분 읽기, 15분 요약, 10분 질문 정리, 10분 repo 연결을 수행한다.
4. `logs/YYYY-MM.md`에 오늘 항목을 추가한다.
5. 이해가 안 된 부분은 `AI에게 물어볼 질문`에 적고, 다음 날 첫 10분에 다시 확인한다.
6. ETF/주식 후보를 다룰 때는 `매수 가능성`이 아니라 `무엇이 아직 미확인인지`를 먼저 쓴다.

## 권장 AI 프롬프트

```text
나는 재량 투자 초보자다. 아래 내용을 투자 추천이 아니라 학습용으로 설명해줘.
1) 핵심 개념을 쉬운 말로 설명
2) 내가 착각하기 쉬운 점
3) 공식 자료로 확인해야 할 항목
4) 내 _report/di 리서치 문서 어디와 연결되는지
```
