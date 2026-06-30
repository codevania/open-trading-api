# KRX Chrome Download Retry

## Metadata

- Date: 2026-06-13
- Author: Codex
- Target Universe: `Universe v0`
- Tool path: Codex Chrome extension
- Current status: `pending_manual_download`
- Bias Control judgment: `hold`

## Purpose

Retry the KRX raw download path through the user's Chrome browser instead of the in-app Browser.

This artifact records browser-level evidence only. It does not create a raw snapshot and does not upgrade `Point-in-Time` readiness.

## Attempted Pages

| Dataset | Page | Result |
| --- | --- | --- |
| `managed_issues_current` | `https://data.krx.co.kr/contents/MDC/STAT/issue/MDCSTAT214.jsp` | Page rendered, but required app globals were missing |
| `managed_issues_current` | `https://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC02020701` | Redirected to KRX login page |
| `managed_issue_designation_history` | main menu discovery | Menu id found as `MDC02020702`; raw download not reached |

## Observations

Direct STAT page:

- The page title and DOM identified `[20012] 관리종목 현황`.
- The DOM exposed `조회`, `컬럼필터 팝업`, and `다운로드 팝업`.
- The grid headers were visible, but body rows were empty after `조회`.
- Chrome console logged missing app dependencies:
  - `ReferenceError: mdc is not defined`
  - `ReferenceError: jQuery is not defined`

Main shell:

- `https://data.krx.co.kr/contents/MDC/MAIN/main/index.cmd` loaded as `KRX Data Marketplace`.
- Menu discovery found:
  - `관리종목 현황` -> `MDC02020701`
  - `관리종목 지정 내역(개별종목)` -> `MDC02020702`
- Direct loader navigation to `MDC02020701` redirected to KRX login.
- A later main-shell retry timed out in the Chrome control session before download could be verified.

## Judgment

- Raw CSV files were not captured.
- `download_verified_by_codex` remains `false`.
- `schema_verified_by_codex` remains `false`.
- `sha256` remains `TO_BE_FILLED`.
- Strategy interpretation remains `hold`.

## Next Action

1. Use a normal Chrome session from the KRX main page if login or UI state is required.
2. Save required raw files to `_report/raw/2026/2026-06-13/krx/universe/`.
3. Create [[_report/raw/2026/2026-06-13/krx/universe/manifest.yaml|_report/raw/2026/2026-06-13/krx/universe/manifest.yaml]].
4. Run [[scripts/quant_krx_manifest_verify.py|scripts/quant_krx_manifest_verify.py]] against that manifest.
5. Start parser work only after required datasets pass hash and schema verification.
