# DI 초보자 8주 학습 플랜

- 작성일: 2026-07-08
- 권장 시작일: 2026-07-09
- 기간: 8주, 56일
- 기본 시간: 매일 30~60분
- 목표: `_report/di`의 core ETF, satellite ETF, satellite equity 후보가 왜 `hold`인지 스스로 설명하고, AI와 함께 원천 근거 기반 리서치 초안을 작성할 수 있게 된다.
- 범위 제외: 매수/매도 추천, 실제 주문, 수익률 약속, 세무 확정 판단.

## 왜 8주인가

완전 초보자는 용어, 상품 구조, 재무제표, 공시, 밸류에이션, 기록 습관을 한꺼번에 익히기 어렵다. 4주는 개념을 훑기에는 가능하지만 실제 DI 문서와 연결하기엔 짧고, 12주는 시작 장벽이 높다. 8주는 매일 30~60분으로 `기초 -> ETF -> 기업 -> 가치평가 -> 판단 보류 훈련`을 한 번 순환하기에 적절하다.

## 완료 기준

8주 후 다음을 할 수 있으면 1회차 학습을 완료로 본다.

- ETF 후보 3개 이상에 대해 추종지수, 비용, 유동성, 분배, 세금/계좌 확인 필요 항목을 구분한다.
- 개별주 후보 1개에 대해 사업, 매출원, 핵심 리스크, 재무제표 3개 지표, valuation 미확인 항목을 설명한다.
- [[_report/di/research/ETF-COMPARISON/evidence-gate|evidence-gate.md]]의 `hold` 사유를 자기 말로 풀어쓴다.
- AI 답변을 그대로 믿지 않고 공식 자료, 공시, 운용사 자료, SEC/DART/거래소 자료 중 최소 1개로 확인한다.
- `logs/YYYY-MM.md`에 최소 40일 이상 기록을 남긴다.

## 기본 참고 자료

- Local DI overview: [[_report/di/README|_report/di/README.md]]
- ETF routine: [[_report/di/routines/etf-research-routine|etf-research-routine.md]]
- Company routine: [[_report/di/routines/company-research-routine|company-research-routine.md]]
- Candidate queue: [[_report/di/candidates/core-satellite-candidates.yaml|core-satellite-candidates.yaml]]
- Current gate: [[_report/di/research/ETF-COMPARISON/evidence-gate|evidence-gate.md]]
- SEC Investor.gov ETF overview: `https://www.investor.gov/introduction-investing/investing-basics/investment-products/mutual-funds-and-exchange-traded-2`
- SEC Investor.gov Researching Investments: `https://www.investor.gov/introduction-investing/getting-started/researching-investments`
- SEC Investor.gov Understanding Fees: `https://www.investor.gov/introduction-investing/getting-started/understanding-fees`
- SEC Investor.gov Asset Allocation: `https://www.investor.gov/introduction-investing/investing-basics/glossary/asset-allocation`
- SEC Investor.gov Diversification: `https://www.investor.gov/introduction-investing/investing-basics/glossary/diversification`

## 매일 산출물

매일 `logs/YYYY-MM.md`에 아래 4가지만 반드시 남긴다.

1. 오늘 배운 핵심 3줄
2. 새 용어 1~3개
3. 공식/원천 자료로 확인한 사실 1개
4. 아직 판단을 미루는 이유 1개

## 1주차: 투자 언어와 안전장치

| Day | 주제 | 할 일 | 산출물 |
| ---: | --- | --- | --- |
| 1 | DI와 Quant 구분 | [[_report/di/README|_report/di/README.md]]를 읽고 DI가 다루는 것과 Quant가 다루는 것을 분리한다. | DI/Quant 차이 5줄 |
| 2 | 투자 목표와 시간축 | 투자 목표, 기간, 현금흐름, 부채/비상금의 의미를 정리한다. | 내 투자 전제 중 아직 모르는 것 5개 |
| 3 | 위험감내도 | 가격 하락, 손실 확정, 변동성, 유동성 위험을 구분한다. | 내가 견딜 수 없는 상황 3개 |
| 4 | 분산 | SEC diversification 글을 읽고 단일 종목 집중의 위험을 설명한다. | 분산이 필요한 이유 3줄 |
| 5 | 자산배분 | SEC asset allocation 글을 읽고 주식/채권/현금의 역할을 구분한다. | 자산군별 역할 표 |
| 6 | 수익률 착각 | 과거 수익률, 기대수익률, 실제 달성수익률을 구분한다. | 과거성과 관련 착각 3개 |
| 7 | 주간 복습 | Day 1~6 로그를 읽고 이해 안 된 용어를 모은다. | 질문 5개 |

## 2주차: ETF와 core 투자

| Day | 주제 | 할 일 | 산출물 |
| ---: | --- | --- | --- |
| 8 | ETF 구조 | SEC ETF overview를 읽고 ETF가 무엇을 보유하는지 설명한다. | ETF 구조 5줄 |
| 9 | Core ETF | `core ETF`가 장기 포트폴리오에서 맡는 역할을 정리한다. | core 후보 VOO/VTI/VT 차이 초안 |
| 10 | 지수 | S&P 500, total US market, total world의 차이를 조사한다. | 각 지수의 포함 범위 |
| 11 | 비용 | SEC Understanding Fees를 읽고 비용이 장기 성과에 미치는 영향을 정리한다. | 총보수만 보면 부족한 이유 |
| 12 | 유동성 | 거래량, 스프레드, AUM, NAV 괴리의 의미를 학습한다. | ETF 유동성 체크리스트 |
| 13 | 분배와 재투자 | 분배금, 배당, 자동재투자, 세후 재투자 편의성을 구분한다. | 분배 정책 질문 5개 |
| 14 | 주간 복습 | [[_report/di/routines/etf-research-routine|etf-research-routine.md]]와 연결한다. | ETF routine에서 이해한 항목/미이해 항목 |

## 3주차: 국내상장 ETF vs 미국직투 ETF

| Day | 주제 | 할 일 | 산출물 |
| ---: | --- | --- | --- |
| 15 | 후보 확인 | [[_report/di/candidates/core-satellite-candidates.yaml|core-satellite-candidates.yaml]]의 core ETF와 국내상장 ETF 후보를 읽는다. | 후보별 역할 표 |
| 16 | 환노출 | USD 자산, KRW 표시 상품, 환헤지/비헤지를 구분한다. | 환율이 수익률에 미치는 경로 |
| 17 | 세금/계좌 | 세금은 확정하지 말고 확인 질문으로 정리한다. | 세무/계좌 확인 질문 7개 |
| 18 | 운용사 자료 | 운용사 상품 페이지에서 확인해야 할 항목을 뽑는다. | 공식 상품 페이지 체크리스트 |
| 19 | NAV와 괴리율 | NAV, 시장가격, premium/discount를 학습한다. | 괴리율이 큰 ETF의 위험 3개 |
| 20 | ETF 비교 초안 | VOO, VTI, VT 중 하나와 국내상장 후보 하나를 비교한다. | 비교표 1개 |
| 21 | 주간 복습 | [[_report/di/research/ETF-COMPARISON/evidence-gate|evidence-gate.md]]의 ETF hold 사유를 자기 말로 번역한다. | ETF hold 사유 해설 |

## 4주차: 기업 분석 기초

| Day | 주제 | 할 일 | 산출물 |
| ---: | --- | --- | --- |
| 22 | 주식이란 무엇인가 | 주식이 기업 소유권이라는 점과 ETF와의 차이를 정리한다. | ETF vs 개별주 비교 |
| 23 | 사업 모델 | 매출원, 고객, 비용 구조, 경쟁우위를 구분한다. | MSFT 또는 GOOGL 사업 모델 5줄 |
| 24 | 손익계산서 | 매출, 매출총이익, 영업이익, 순이익을 학습한다. | 손익 지표 용어표 |
| 25 | 재무상태표 | 현금, 부채, 자본, 운전자본을 학습한다. | 부채가 위험해지는 조건 |
| 26 | 현금흐름표 | 영업현금흐름, 투자현금흐름, FCF를 구분한다. | FCF가 중요한 이유 |
| 27 | 성장과 마진 | 매출 성장, 영업마진, capex의 관계를 본다. | 성장 기업 질문 5개 |
| 28 | 주간 복습 | [[_report/di/routines/company-research-routine|company-research-routine.md]]와 연결한다. | 기업 routine 단계 요약 |

## 5주차: 공시와 원천 자료 읽기

| Day | 주제 | 할 일 | 산출물 |
| ---: | --- | --- | --- |
| 29 | 원천 우선 원칙 | SEC Researching Investments를 읽고 공시가 왜 중요한지 정리한다. | 1차 자료 우선 이유 |
| 30 | SEC/DART 역할 | 미국 기업은 SEC, 국내 기업은 DART를 우선한다는 원칙을 학습한다. | SEC/DART 차이 |
| 31 | 10-K/사업보고서 | Business, Risk Factors, MD&A가 각각 무엇인지 학습한다. | 공시 목차 지도 |
| 32 | 10-Q/분기보고서 | 최근 분기 변화와 연간 추세를 구분한다. | 분기 지표 질문 5개 |
| 33 | 8-K/수시공시 | 이벤트성 공시가 왜 중요한지 학습한다. | 이벤트 리스크 예시 |
| 34 | AI 요약 검증 | AI가 요약한 공시를 원문 문단으로 역검증하는 연습을 한다. | AI 검증 체크리스트 |
| 35 | 주간 복습 | 기존 `sec-filing-summary.md` 하나를 읽고 모르는 단어를 정리한다. | 공시 용어 10개 |

## 6주차: valuation과 시나리오

| Day | 주제 | 할 일 | 산출물 |
| ---: | --- | --- | --- |
| 36 | 가격과 가치 | 주가, 시가총액, 기업가치, 내재가치를 구분한다. | 가격/가치 차이 5줄 |
| 37 | 밸류에이션 배수 | PER, P/S, EV/EBITDA가 무엇을 단순화하는지 학습한다. | 배수의 한계 3개 |
| 38 | DCF 감각 | 할인율, 성장률, FCF, terminal value를 큰 그림으로 이해한다. | DCF 입력값 표 |
| 39 | 역산 질문 | 현재 주가가 어떤 성장/마진을 전제하는지 묻는 법을 배운다. | reverse DCF 질문 5개 |
| 40 | Bull/Base/Bear | 상승/기본/하락 시나리오를 각각 쓴다. | 후보 1개 시나리오 초안 |
| 41 | 무효화 조건 | 어떤 사실이 나오면 내 thesis가 틀리는지 정의한다. | invalidation rule 3개 |
| 42 | 주간 복습 | [[_report/di/templates/research/valuation|valuation.md]] 템플릿을 읽고 빈칸의 의미를 이해한다. | valuation 미확인 항목 |

## 7주차: 의사결정 기록과 행동 규칙

| Day | 주제 | 할 일 | 산출물 |
| ---: | --- | --- | --- |
| 43 | 결정과 기록 | [[_report/di/templates/research/decision|decision.md]]와 [[_report/di/decisions/decision-log|decision-log.md]]의 차이를 이해한다. | 기록 위치 구분표 |
| 44 | 보류의 기술 | `hold`가 실패가 아니라 리스크 관리임을 정리한다. | 좋은 보류 사유 5개 |
| 45 | 포지션 크기 | 최대 비중, 추가매수, 손절/축소 조건을 개념으로 이해한다. | position sizing 질문 5개 |
| 46 | ETF 중복 | core ETF와 satellite equity의 보유 종목 중복을 학습한다. | 중복이 위험해지는 경우 |
| 47 | 행동 후보 | 매수/매도 대신 `추가 확인`, `관찰`, `제외`, `보류`로 표현한다. | 행동 후보 문장 5개 |
| 48 | 인지 편향 | 확증편향, FOMO, 손실회피, 앵커링을 학습한다. | 내게 위험한 편향 3개 |
| 49 | 주간 복습 | 이번 주 기록을 읽고 판단이 앞섰던 문장을 고친다. | 수정 전/후 문장 |

## 8주차: repo에 적용하는 캡스톤

| Day | 주제 | 할 일 | 산출물 |
| ---: | --- | --- | --- |
| 50 | 후보 1개 선택 | ETF 후보 1개 또는 개별주 후보 1개를 학습 대상으로 고른다. | 선택 이유와 제외 범위 |
| 51 | 원천 자료 수집 설계 | 어떤 공식 자료를 확인해야 하는지 목록화한다. | source checklist |
| 52 | 근거 요약 | 확인한 사실과 미확인 사실을 분리한다. | facts vs unknowns 표 |
| 53 | 장점/단점/리스크 | 긍정, 부정, 리스크를 같은 비중으로 쓴다. | balanced memo |
| 54 | valuation/비용 연결 | ETF면 비용/세금, 주식이면 valuation 질문을 연결한다. | 다음 evidence 5개 |
| 55 | AI 검토 | AI에게 내 메모의 허점과 과장 표현을 찾게 한다. | 수정 목록 |
| 56 | 최종 복습 | 8주 학습 내용을 1페이지로 요약한다. | `summaries/`로 옮길 수 있는 학습 요약 |

## 8주 후 다음 단계

1. core ETF 비교를 먼저 완성한다.
2. 국내상장 ETF의 세금/계좌 적합성은 확정하지 말고 증권사/세무 확인 질문으로 남긴다.
3. satellite equity는 [[_report/di/templates/research/thesis|thesis.md]]가 있어도 [[_report/di/templates/research/valuation|valuation.md]]와 [[_report/di/templates/research/decision|decision.md]]가 없으면 계속 `hold`로 둔다.
4. 후보를 watchlist에 올리기 전 [[scripts/di_candidate_evidence_check.py|di_candidate_evidence_check.py]]를 다시 돌린다.
