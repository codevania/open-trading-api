# NVDA Thesis

## 메타

- Symbol: `NVDA`
- Company: NVIDIA
- 작성일: `2026-07-08`
- 기준 원천일: `2026-07-08`
- 원천: SEC 10-K, 10-Q section extracts and SEC XBRL companyfacts summary
- 해석: 재량투자 리서치 초안이며, 투자 추천 또는 주문 의도가 아니다.
- Order intent generated: `false`

## 핵심 thesis

NVDA는 단순 GPU 회사가 아니라 CUDA 소프트웨어 생태계, GPU/CPU/DPU, NVLink, InfiniBand/Ethernet, rack-scale system을 묶어 AI 데이터센터 인프라를 파는 플랫폼 기업이다. 위성 재량투자 후보로 보는 이유는 AI 학습과 추론 수요가 Data Center 매출과 영업이익으로 이미 크게 전환되었고, Blackwell 및 후속 Rubin 로드맵이 고객의 AI 인프라 투자 주기와 맞물려 있기 때문이다. 다만 현재 숫자는 매우 높은 기대를 반영하기 쉬우므로, thesis의 핵심은 "AI 인프라 수요가 고객집중, 공급망, 수출통제, 제품 전환 리스크를 이겨낼 만큼 지속되는가"다.

## 투자 관찰 포인트

1. 회사는 `Compute & Networking`과 `Graphics` 두 보고 세그먼트를 사용한다. FY2026 기준 Compute & Networking 매출은 $193.5B, Graphics 매출은 $22.5B로 Data Center 중심 회사가 되었다.
2. FY2026 매출은 $215.9B로 전년 대비 65% 증가했고, 영업이익은 $130.4B, 순이익은 $120.1B였다. 영업이익률은 60.4%, 단순 FCF margin은 44.8%였다.
3. 2026-04-26 분기, 즉 FY2027 Q1 매출은 $81.6B로 전년 동기 대비 85% 증가했다. Data Center 매출은 $75.2B로 전년 동기 대비 92% 증가했고, 분기 전체 매출의 대부분을 차지했다.
4. 2026-04-26 분기 gross margin은 74.9%, 영업이익률은 65.6%였다. 전년 동기에는 H20 관련 $4.5B charge가 있었기 때문에 margin 비교에는 일회성 기저 효과가 있다.
5. 2026-04-26 분기 직접 고객 3곳이 각각 전체 매출의 21%, 17%, 16%를 차지했다. 고객집중은 성장의 증거이면서 동시에 큰 리스크다.
6. 2026-04-26 기준 현금 및 현금성자산은 $13.2B, debt proxy는 $8.5B, 총자산은 $259.5B, 자본은 $195.5B였다. 다만 cash_and_investments는 XBRL 태그 선택상 현금성자산 중심이라 시장성증권 포함 여부를 10-Q 주석에서 확인해야 한다.

## 강세 논리

- AI 인프라 표준 지위: NVIDIA는 GPU, CUDA, networking, systems, software, algorithms를 묶어 데이터센터 규모의 AI 인프라를 제공한다. 고객 입장에서는 칩만 사는 것이 아니라 학습/추론을 빠르게 구축하는 전체 stack을 산다.
- Data Center 성장: FY2026 Data Center 성장은 accelerated computing과 AI가 주도했고, FY2027 Q1 Data Center 매출도 $75.2B까지 커졌다. 10-Q는 Blackwell 300 ramp와 InfiniBand, Spectrum-X Ethernet, NVLink 수요를 성장 동인으로 제시한다.
- 네트워킹 moat: AI cluster는 GPU만으로 완성되지 않는다. GB200/GB300 같은 rack-scale system에서는 NVLink, InfiniBand, Ethernet, DPU/NIC/switch가 함께 들어가므로 NVIDIA의 수익원이 더 넓어진다.
- CUDA와 개발자 생태계: 회사는 7.5M명 이상의 개발자가 CUDA 및 소프트웨어 도구를 사용한다고 공시한다. 소프트웨어 호환성과 개발자 생태계는 고객이 다른 chip으로 갈아타는 비용을 높인다.
- 수익성: FY2026 영업이익률 60.4%, FY2027 Q1 영업이익률 65.6%는 매우 높은 수준이다. 제품 mix와 공급망 문제가 없을 때 AI 인프라 수요가 강한 현금창출력으로 전환되고 있다.
- 제품 cadence: Blackwell, Blackwell Ultra, Rubin으로 이어지는 빠른 architecture cadence는 고객에게 성능 향상 경로를 제시한다. 추론 비용과 token throughput 개선은 AI 서비스 확산과 연결된다.

## 약세 논리와 리스크

- 기대치와 valuation 리스크: 재무 숫자가 이미 폭발적으로 좋아졌기 때문에 주가가 높은 성장 지속을 전제할 수 있다. 성장률이 정상화되거나 margin이 하락하면 valuation이 먼저 흔들릴 수 있다.
- 고객집중: FY2027 Q1 직접 고객 3곳이 매출의 54%를 차지했다. CSP, AI cloud, 대형 AI 모델 고객의 capex 축소, 주문 지연, 자체 ASIC 전환은 매출 변동성을 크게 만든다.
- 수출통제와 중국: H20/H200, 중국, D:5 국가, AI Diffusion replacement rule, GAIN AI Act, RASA 등 규제 불확실성이 크다. 회사는 중국 데이터센터 compute 시장에서 사실상 경쟁이 제한되어 있다고 설명한다.
- 공급망 의존: fabless 구조상 TSMC, Samsung, SK Hynix, Micron, CoWoS, 조립/테스트/계약제조 파트너에 의존한다. 긴 lead time과 non-cancellable purchase commitments는 수요 예측이 틀릴 때 inventory charge로 이어질 수 있다.
- 제품 전환 리스크: Blackwell, Blackwell Ultra, Rubin처럼 빠른 cadence는 경쟁력의 원천이지만, 고객 qualification, 데이터센터 준비, 수율, 품질, warranty, 이전 architecture 재고 문제를 동시에 키운다.
- 경쟁과 자체 칩: AMD, Intel, Broadcom, Marvell, Huawei, CSP 자체 ASIC, hyperscaler 내부 solution이 모두 경쟁 축이다. 일부 고객은 특정 workload에 최적화된 자체 칩으로 NVIDIA 의존도를 줄일 수 있다.
- 데이터센터 제약: 고객의 AI 인프라 buildout에는 데이터센터, 전력, 자본이 필요하다. 전력/인허가/자금 조달 제약이 deployment 속도를 늦추면 NVIDIA의 shipment timing도 흔들릴 수 있다.

## 포트폴리오 역할

- 분류: 위성 재량투자 후보.
- 코어 ETF와의 관계: S&P 500, Nasdaq 100, 미국 대형 성장주 ETF를 보유하면 NVDA 비중은 이미 상당히 크다. 단일주 추가는 AI 인프라 supply chain의 중심 회사에 ETF 평균보다 더 강하게 베팅하는 행동이다.
- MSFT/GOOGL/AMZN/META와의 차이: 이 네 종목은 AI를 사용해 소프트웨어, 광고, 클라우드, 리테일, 플랫폼 매출을 키우는 쪽이다. NVDA는 이들의 capex를 매출로 받는 AI 인프라 공급자에 가깝다. 그래서 같은 AI theme 안에서도 수익 구조가 다르지만, hyperscaler capex cycle에는 강하게 묶인다.
- 보류 이유: 최신 가격 valuation, ETF 중복 비중, 고객집중 허용치, 중국/수출통제 시나리오, AI capex cycle 둔화 가능성을 아직 `decision.md`에서 검증하지 않았다.

## 무효화 조건

다음 중 2개 이상이 동시에 확인되면 NVDA 위성 thesis를 재검토한다.

1. Data Center 매출 성장률이 빠르게 둔화되는데 gross margin 또는 operating margin도 같이 하락한다.
2. 대형 CSP/AI cloud 고객의 주문 지연, 자체 ASIC 전환, capex 축소가 여러 분기 반복된다.
3. Blackwell/Rubin 전환에서 수율, 품질, 공급, warranty, inventory charge 문제가 확대된다.
4. 미국 수출통제가 중국 외 지역까지 넓어져 Data Center 제품 판매와 networking 제품 판매를 동시에 제한한다.
5. TSMC/CoWoS/HBM/메모리/조립/테스트 공급 병목이 수요를 충족하지 못하거나 원가를 크게 밀어 올린다.
6. 경쟁 제품 또는 고객 자체 칩이 특정 workload에서 충분한 성능/비용 우위를 보여 NVIDIA의 pricing power를 낮춘다.
7. AI 모델 학습/추론 수요가 고객의 실제 매출화보다 빠르게 과잉 투자로 전환되어 주문 취소나 과잉 재고가 발생한다.

## 다음 확인 항목

1. 최신 가격 기준 valuation: P/E, EV/FCF, FCF yield, sales multiple, Data Center 성장률 대비 premium을 확인한다.
2. Data Center, Edge Computing 또는 보고 체계 변경 후 market platform별 매출을 분기별로 추적한다.
3. 직접 고객 concentration과 indirect customer concentration을 별도 표로 만든다.
4. H20/H200, 중국, D:5 국가, AI export control 관련 8-K/10-Q/10-K 변화를 추적한다.
5. gross margin에서 inventory provision, H20 charge, Blackwell mix, tariffs 영향을 분리한다.
6. 공급망 의존도: TSMC, CoWoS, HBM, SK Hynix/Micron/Samsung, contract manufacturer 관련 약정과 리스크를 주석에서 확인한다.
7. 내 포트폴리오의 S&P 500, Nasdaq 100, 미국 기술주 ETF 안에 이미 들어 있는 NVDA 중복 비중을 계산한다.
8. `decision.md`는 valuation, ETF 중복, 고객집중, 수출통제, 공급망, AI capex cycle 둔화 시나리오를 확인한 뒤 작성한다.

## 데이터 한계 메모

- NVIDIA의 fiscal year는 calendar year와 다르다. FY2026은 2026-01-25에 끝나며, 2026-04-26 분기는 FY2027 Q1이다.
- `financials.md`의 FCF는 SEC XBRL companyfacts에서 `operating cash flow - capex`로 단순 계산한 값이다. 회사 정의나 cash flow statement presentation과 차이가 있을 수 있다.
- 2026-04-26 분기 순이익률이 71.5%로 매우 높게 보이므로 세금, 투자손익, 일회성 항목을 10-Q 주석에서 추가 확인해야 한다.
- XBRL `cash_and_investments`는 현금성자산 중심으로 잡힌 것으로 보여, 시장성증권 포함 유동성은 10-Q balance sheet 주석을 별도로 확인해야 한다.

## 사용한 로컬 원천

- `_report/di/research/NVDA/sec-filing-summary.md`
- `_report/di/research/NVDA/sec-filing-documents.md`
- `_report/di/research/NVDA/sec-filing-sections.md`
- `_report/di/research/NVDA/financials.md`
- `_report/raw/2026/2026-07-08/sec/NVDA/sections/10-K_2026-02-25_000104581026000021_business.raw.txt`
- `_report/raw/2026/2026-07-08/sec/NVDA/sections/10-K_2026-02-25_000104581026000021_mda.raw.txt`
- `_report/raw/2026/2026-07-08/sec/NVDA/sections/10-K_2026-02-25_000104581026000021_risk_factors.raw.txt`
- `_report/raw/2026/2026-07-08/sec/NVDA/sections/10-Q_2026-05-20_000104581026000052_quarterly_mda.raw.txt`
- `_report/raw/2026/2026-07-08/sec/NVDA/sections/10-Q_2026-05-20_000104581026000052_risk_factors.raw.txt`
