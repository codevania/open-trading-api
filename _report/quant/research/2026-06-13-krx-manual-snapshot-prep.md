# KRX Manual Snapshot Prep

## Metadata

- Date: 2026-06-13
- Author: Codex
- Target Universe: `Universe v0`
- Source mode: `manual_snapshot_prep`
- Current status: `pending_manual_download`
- Bias Control judgment: `hold`
- Procedure reference: `_report/quant/research/2026-06-08-krx-manual-snapshot-procedure.md`
- Pending manifest: `_report/quant/research/2026-06-13-krx-manual-snapshot-manifest.pending.yaml`
- Chrome retry: `_report/quant/research/2026-06-13-krx-chrome-download-retry.md`

## Purpose

Prepare the exact checklist for a KRX manual snapshot without pretending the raw CSV files already exist.

This is a prep artifact. It does not upgrade Point-in-Time Universe readiness, Backtest readiness, or Bias Control.

## Required Manual Downloads

| Dataset ID | Required | Source URL | Target Raw Path | Status |
| --- | --- | --- | --- | --- |
| `listed_issues_current` | yes | `KRX Data Marketplace > 통계 > 기본 통계 > 주식 > 종목정보 > 전종목 기본정보` | `_report/raw/2026/2026-06-13/krx/universe/listed_issues_current.raw.csv` | `pending_manual_download` |
| `managed_issues_current` | yes | `https://data.krx.co.kr/contents/MDC/STAT/issue/MDCSTAT214.jsp` | `_report/raw/2026/2026-06-13/krx/universe/managed_issues_current.raw.csv` | `pending_manual_download` |
| `managed_issue_designation_history` | yes | `https://data.krx.co.kr/contents/MDC/STAT/issue/MDCSTAT215.jsp` | `_report/raw/2026/2026-06-13/krx/universe/managed_issue_designation_history.raw.csv` | `pending_manual_download` |
| `delisting_events` | preferred | `https://global.krx.co.kr/contents/GLB/03/0306/0306050000/GLB0306050000.jsp` | `_report/raw/2026/2026-06-13/krx/universe/delisting_events.raw.csv` | `pending_manual_download` |

## Manual Steps

1. Open each KRX source URL in a normal browser session.
2. Download CSV or Excel from the official KRX page.
3. Save the original file under `_report/raw/2026/2026-06-13/krx/universe/`.
4. Rename files to the target raw file names without editing their contents.
5. Compute SHA-256 with `Get-FileHash -Algorithm SHA256`.
6. Fill the pending manifest and save the final manifest next to the raw files as `_report/raw/2026/2026-06-13/krx/universe/manifest.yaml`.
7. Ask Codex to verify schema and hash after the files exist.
8. After `listed_issues_current` and `managed_issues_current` exist, build current snapshot Universe v0 with `scripts/quant_krx_current_universe_build.py`.

## Validation Rules

- `download_verified_by_codex` stays `false` unless Codex directly observes the download event.
- `schema_verified_by_codex` stays `false` until raw files are present and columns are inspected.
- `sha256` stays `TO_BE_FILLED` until raw files exist.
- A single current snapshot does not create a full `Point-in-Time` Universe.
- Strategy interpretation remains `hold`.
- Manifest verification uses `scripts/quant_krx_manifest_verify.py`.
- Manifest materialization uses `scripts/quant_krx_manifest_materialize.py`.

Verifier command:

```powershell
uv run python scripts/quant_krx_manifest_verify.py `
  --manifest _report/raw/2026/2026-06-13/krx/universe/manifest.yaml `
  --output _report/quant/research/YYYY-MM-DD-krx-manual-snapshot-verify-result.md
```

Materialize final raw manifest after downloads:

```powershell
uv run python scripts/quant_krx_manifest_materialize.py `
  --manifest _report/quant/research/2026-06-13-krx-manual-snapshot-manifest.pending.yaml `
  --output _report/raw/2026/2026-06-13/krx/universe/manifest.yaml
```

Pending prep manifest check:

```powershell
uv run python scripts/quant_krx_manifest_verify.py `
  --manifest _report/quant/research/2026-06-13-krx-manual-snapshot-manifest.pending.yaml `
  --allow-pending
```

## Done Criteria For This Prep Step

- Prep checklist exists.
- Pending manifest exists.
- Verifier exists and can produce a `pending` result while raw files are absent.
- Raw target paths are fixed.
- The next human/manual action is unambiguous.

## Not Done

- KRX CSV files are not downloaded.
- SHA-256 hashes are not computed.
- Column schema is not verified.
- Parser work is not started.
- Backtest interpretation is not upgraded.

## 2026-06-13 Chrome Retry Result

Codex retried the raw download path through the Chrome extension.

- Direct STAT page rendered `관리종목 현황`, but page scripts were incomplete in direct URL mode.
- Console evidence included `ReferenceError: mdc is not defined` and `ReferenceError: jQuery is not defined`.
- KRX main shell menu discovery found `MDC02020701` for `관리종목 현황` and `MDC02020702` for `관리종목 지정 내역(개별종목)`.
- Direct loader URL for `MDC02020701` redirected to the KRX login page.
- No raw CSV file was captured.

Result: `pending_manual_download` remains unchanged. Parser work is still blocked.
