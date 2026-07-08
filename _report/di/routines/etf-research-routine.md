# DI ETF Research Routine

## 후보 매니페스트 작업 흐름

ETF를 [[_report/di/watchlist.yaml|_report/di/watchlist.yaml]]에 추가하기 전에는 GitHub에 올려도 안전한 후보 매니페스트인 [[_report/di/candidates/core-satellite-candidates.yaml|core-satellite-candidates.yaml]]을 먼저 사용한다.

```bash
python scripts/di_etf_compare.py --candidate-file _report/di/candidates/core-satellite-candidates.yaml --output _report/di/research/ETF-COMPARISON/etf-checklist.md
python scripts/di_candidate_evidence_check.py --candidate-file _report/di/candidates/core-satellite-candidates.yaml --output _report/di/research/ETF-COMPARISON/evidence-gate.md
python scripts/di_etf_source_collect.py --candidate-file _report/di/candidates/core-satellite-candidates.yaml --run-date YYYY-MM-DD --dry-run
python scripts/di_etf_holdings_collect.py --candidate-file _report/di/candidates/core-satellite-candidates.yaml --run-date YYYY-MM-DD --dry-run --output _report/di/research/ETF-COMPARISON/etf-holdings-source-status.md
python scripts/di_etf_overlap_check.py --candidate-file _report/di/candidates/core-satellite-candidates.yaml --input-file _report/private/di/etf-overlap-inputs.yaml --run-date YYYY-MM-DD
```

관련 파일:

명령어 코드블록은 실행 가능한 형태를 유지하기 위해 원문 경로를 그대로 두고, 실제 파일 참조는 아래 링크로 확인한다.

- [[scripts/di_etf_compare.py|di_etf_compare.py]]
- [[scripts/di_candidate_evidence_check.py|di_candidate_evidence_check.py]]
- [[scripts/di_etf_source_collect.py|di_etf_source_collect.py]]
- [[scripts/di_etf_holdings_collect.py|di_etf_holdings_collect.py]]
- [[scripts/di_etf_overlap_check.py|di_etf_overlap_check.py]]
- [[_report/di/templates/etf-overlap-inputs.example.yaml|etf-overlap-inputs.example.yaml]]
- [[_report/di/research/ETF-COMPARISON/etf-checklist|etf-checklist.md]]
- [[_report/di/research/ETF-COMPARISON/evidence-gate|evidence-gate.md]]
- [[_report/di/research/ETF-COMPARISON/etf-holdings-source-status|etf-holdings-source-status.md]]

## 규칙

- [[_report/di/candidates/core-satellite-candidates.yaml|core-satellite-candidates.yaml]]은 매수 목록이 아니라 리서치 대기열로 취급한다.
- 매수 판단을 검토하기 전에는 expense, AUM, spread, NAV gap, distribution, tax, account-wrapper 항목을 먼저 채운다.
- 국내상장 ETF 후보는 운용사 자료와 증권사/세금 근거가 기록될 때까지 `needs_issuer_and_tax_verification` 상태로 둔다.
- 후보를 active monitoring으로 승격하기 전에는 [[_report/di/research/ETF-COMPARISON/evidence-gate|evidence-gate.md]]를 blocker list로 확인한다.
- [[scripts/di_etf_source_collect.py|di_etf_source_collect.py]]는 먼저 `--dry-run`으로 실행한다. 공식 운용사 원천 페이지를 `_report/raw/YYYY/YYYY-MM-DD/di/etf-sources/` 아래에 보존해야 할 때만 live 수집을 실행한다.
- [[scripts/di_etf_holdings_collect.py|di_etf_holdings_collect.py]]는 공식 보유종목 API가 확인된 ETF만 live 수집한다. 현재 `QQQ`는 Invesco 공식 holdings API가 확인됐고, `VOO`/`VTI`/`VT`는 Vanguard 공식 profile page만 확인됐으므로 보유종목은 수동 공식 원천 확인 상태로 둔다.
- [[scripts/di_etf_overlap_check.py|di_etf_overlap_check.py]]는 [[_report/private/di/etf-overlap-inputs.yaml|etf-overlap-inputs.yaml]]에 공식 ETF 보유비중과 개인 ETF 비중을 채운 뒤 실행한다. 개인 비중이 들어가므로 private 파일만 사용한다.
- 국내 ETF 운용사 URL을 추가하거나 제외할 때는 [[_report/di/research/ETF-COMPARISON/domestic-etf-source-url-check|domestic-etf-source-url-check.md]]에 검증 결과를 기록한다.
- ETF를 [[_report/di/watchlist.yaml|_report/di/watchlist.yaml]]에 옮기는 것은 [[_report/di/research/ETF-COMPARISON/etf-checklist|etf-checklist.md]]와 [[_report/di/templates/research/decision|decision.md]]가 준비된 뒤에만 검토한다.

## 목적

장기 Core ETF와 보조 ETF를 고를 때 같은 기준으로 비교하기 위한 루틴이다.

ETF는 개별주보다 단순해 보이지만, 추종지수, 총보수, 환노출, 분배금, 세금, 괴리율, 유동성을 반드시 확인한다.

## 데이터 소스 역할

| 목적 | 우선 출처 |
|---|---|
| 현재가/거래량 | KIS MCP, 거래소 |
| NAV/괴리율 | KIS ETF/ETN API, KRX |
| 추종지수 | 운용사 상품 페이지, 투자설명서 |
| 보유종목 | 운용사 상품 페이지 |
| 총보수/기타비용 | 운용사 상품 페이지, 투자설명서 |
| 분배금 | 운용사, 거래소, 증권사 |
| 세금 | 국세청/증권사/세무 전문가 확인 |
| 국내상장 vs 미국직투 비교 | 증권사 세금/수수료 안내 + 상품 원문 |

## Core ETF 필수 체크

1. 추종지수
   - S&P 500, 미국 전체시장, 글로벌 주식 등
   - 지수 산출기관과 편입 기준
2. 상품 구조
   - 국내상장 해외 ETF인지, 미국 직투 ETF인지
   - 환헤지 여부
   - 합성/실물 여부
3. 비용
   - 총보수
   - 기타비용/매매중개비용 가능성
   - 환전수수료와 매매수수료
4. 유동성
   - 거래대금
   - 스프레드
   - 순자산/AUM
5. NAV/괴리
   - NAV 대비 프리미엄/디스카운트
   - 괴리율이 반복적으로 큰지
6. 분배
   - 분배 주기
   - 자동 재투자 여부
   - 세후 재투자 편의성
7. 세금
   - 매매차익 과세
   - 분배금 과세
   - 해외주식 양도세 신고 대상 여부
   - ISA/연금저축/IRP 편입 가능 여부

## Core ETF 제외 기준

- 레버리지/인버스
- 단일 테마 집중
- 거래량이 너무 적고 스프레드가 큰 상품
- 구조와 비용을 설명하기 어려운 상품
- 장기 보유 목적과 맞지 않는 단기 전술형 상품

## 산출물 위치

```text
_report/di/research/ETF-SYMBOL/
  etf-checklist.md
  decision.md
```

## 완료 기준

- 같은 자산군 후보를 최소 2개 이상 비교한다.
- 국내상장형과 미국직투형의 장단점을 따로 적는다.
- 세금은 확정하지 않고 증권사/세무 확인 필요 항목을 남긴다.
- 장기 Core 편입 여부와 제외 조건을 적는다.
