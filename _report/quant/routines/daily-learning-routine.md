# Daily Quant Learning Routine

## Purpose

매일 사용자가 바로 공부할 수 있는 Quant 학습 노트를 생성한다.

이 routine은 학습, 복습, 질문 정리를 위한 것이다. 투자 조언, 종목 추천, 매매 Signal, 주문 실행을 만들지 않는다.

## Trigger Phrases

다음 요청이 오면 이 routine을 사용한다.

- "오늘 퀀트 학습"
- "퀀트 공부 루틴"
- "퀀트 매일 학습"
- "퀀트 학습 내용 만들어줘"
- "퀀트 공부할 것 만들어줘"
- "오늘 퀀트 공부할 내용 정리해줘"

일반적인 "오늘 학습" 요청은 DI 학습 루틴과 충돌할 수 있으므로, 같은 대화나 요청 문맥이 Quant임이 분명할 때만 이 routine으로 라우팅한다.

## Inputs

- 학습 계획: [[_report/quant/learning/12-week-daily-plan|_report/quant/learning/12-week-daily-plan.md]]
- 학습 폴더 설명: [[_report/quant/learning/README|_report/quant/learning/README.md]]
- 일일 템플릿: [[_report/quant/learning/templates/daily-log|_report/quant/learning/templates/daily-log.md]]
- 기존 일일 로그: `_report/quant/learning/daily/YYYY/*.md`
- 구현 상태: [[_report/quant/implementation-roadmap|_report/quant/implementation-roadmap.md]]
- 용어집: [[_report/quant/glossary|_report/quant/glossary.md]]
- Quant 원칙: [[_report/quant/universe|_report/quant/universe.md]]
- 필요할 때만 참고하는 기존 research artifact: `_report/quant/research/*.md`

## Output

```text
_report/quant/learning/daily/YYYY/YYYY-MM-DD.md
```

## Procedure

### 1. Date And Existing Log Check

1. 한국시간(Asia/Seoul) 기준 오늘 날짜를 확인한다.
2. `_report/quant/learning/daily/YYYY/YYYY-MM-DD.md`가 이미 있는지 확인한다.
3. 이미 있으면 새 파일을 만들지 말고 기존 파일을 보강한다.
4. 없으면 template 구조를 유지해 새 파일을 만든다.

### 2. Pick The Next Plan Day

1. `_report/quant/learning/daily/**.md`의 기존 로그를 확인한다.
2. 가장 최근 `Plan day:` 값을 찾는다.
3. 오늘은 그 다음 plan day를 사용한다.
4. 기존 로그가 없으면 Day 1부터 시작한다.
5. 날짜를 건너뛴 경우에도 calendar day로 억지 보정하지 말고 "다음 미완료 plan day"를 사용한다.

### 3. Build Today's Learning Note

학습 노트에는 반드시 다음을 포함한다.

- Metadata: 날짜, plan day, week, topic, study time, author
- Today I Should Be Able To Explain: 오늘 설명할 수 있어야 하는 한 문장
- Reading: 오늘 읽을 repo-local 문서 또는 공식 자료
- Practice: 30-45분 안에 끝나는 작은 실습
- Concepts Learned: 개념, 내 설명, 아직 불확실한 점
- Link To The Quant Project: `Universe`, `Liquidity Filter`, `Signal`, `Backtest`, `Point-in-Time` 또는 data quality와의 연결
- Questions For AI Or Future Study: 다음 질문 3개
- Next Action: 다음 학습 루틴의 시작점
- Caution: 학습 기록이며 투자 조언이 아니라는 문구

### 4. Beginner Explanation Rules

- 초보자가 읽는다고 가정하고 문장을 짧게 쓴다.
- 전문 용어는 처음 나온 곳에서 한 줄로 설명한다.
- 모르는 내용은 "불확실" 또는 "다음 확인"으로 남긴다.
- AI가 추정한 내용을 사실처럼 쓰지 않는다.
- 좋은 결과처럼 보이는 실습도 Strategy 검증으로 주장하지 않는다.

### 5. Safety And Data Rules

- 주문 API를 호출하지 않는다.
- 실제 주문, 계좌번호, app key, token, 실제 보유수량을 기록하지 않는다.
- KIS/MCP raw 응답이 필요하면 별도 요청 없이는 새로 호출하지 않고 저장된 artifact를 우선 읽는다.
- raw 응답을 쓰는 경우 `_report/raw/**` 위치를 링크하고, 해석 문서와 분리한다.
- `Backtest readiness: hold` 또는 `live trading readiness: blocked` 상태를 약하게 표현하지 않는다.

## Stop Conditions

- 오늘 날짜 파일을 만들 수 없다.
- 학습 계획 파일이 없다.
- 기존 로그의 plan day를 판단할 수 없고 Day 1로도 안전하게 시작할 수 없다.
- 요청이 학습 노트가 아니라 실제 종목 추천이나 주문 실행으로 바뀐다.
- 민감 정보 기록이 필요하다.

Stop condition이 발생하면 파일을 추정으로 채우지 말고, 막힌 이유와 필요한 다음 확인 항목을 짧게 남긴다.

## Obsidian Link Rules

- 학습자가 읽는 Markdown 본문에서는 구체적인 repo 내부 파일 참조를 Obsidian wikilink로 쓴다.
- Markdown 파일은 `[[path/without-md|file.md]]` 형식을 쓴다.
- Markdown이 아닌 내부 파일은 확장자를 포함해 `[[path/file.csv|file.csv]]`, `[[scripts/tool.py|tool.py]]`처럼 쓴다.
- 실행용 코드블록, glob 패턴, 템플릿 경로는 복사/패턴 의미가 깨지지 않도록 코드 형식을 유지한다.
