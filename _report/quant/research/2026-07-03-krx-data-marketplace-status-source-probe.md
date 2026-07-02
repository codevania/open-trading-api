# KRX Data Marketplace Status Source Probe

- Captured at KST: `2026-07-03T04:55:48+09:00`
- Scope: official KRX Data Marketplace status screen endpoint discovery
- Interpretation: source-access probe only, not a `Point-in-Time Universe` or `Backtest` result

## Raw Evidence

- [[_report/raw/2026/2026-07-03/krx/data-marketplace/status-source-probe.raw.json|_report/raw/2026/2026-07-03/krx/data-marketplace/status-source-probe.raw.json]]

## Probe Results

| keyword | screen | bld | result | rows |
| --- | --- | --- | --- | ---: |
| 전종목 지정내역 | `MDCSTAT020` | `dbms/MDC/STAT/standard/MDCSTAT02001` | `auth_required` | - |
| 관리종목 현황 | `MDCSTAT214` | `dbms/MDC/STAT/issue/MDCSTAT21401` | `auth_required` | - |
| 매매거래정지종목 현황 | `MDCSTAT212` | `dbms/MDC/STAT/issue/MDCSTAT21201` | `auth_required` | - |
| 상장폐지종목 현황 | `MDCSTAT238` | `dbms/MDC/STAT/issue/MDCSTAT23801` | `auth_required` | - |
| 정리매매종목 현황 | `MDCSTAT237` | `dbms/MDC/STAT/issue/MDCSTAT23701` | `auth_required` | - |
| 투자주의종목 현황 | `MDCSTAT228` | `dbms/MDC/STAT/issue/MDCSTAT22801` | `auth_required` | - |
| 투자경고종목 현황 | `MDCSTAT231` | `dbms/MDC/STAT/issue/MDCSTAT23101` | `auth_required` | - |
| 투자위험종목 현황 | `MDCSTAT234` | `dbms/MDC/STAT/issue/MDCSTAT23401` | `auth_required` | - |

## Current Judgment

- KRX official menu/search metadata can identify status candidate screens and their `bld` identifiers.
- A `LOGOUT` classification means the endpoint is official but not usable as unattended raw input without an authenticated KRX session or manual official download.
- `Backtest` readiness remains `hold` until at least one official status raw sample can be saved, normalized, validated, and replayed.
