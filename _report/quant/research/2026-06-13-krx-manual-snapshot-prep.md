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

## Purpose

Prepare the exact checklist for a KRX manual snapshot without pretending the raw CSV files already exist.

This is a prep artifact. It does not upgrade Point-in-Time Universe readiness, Backtest readiness, or Bias Control.

## Required Manual Downloads

| Dataset ID | Required | Source URL | Target Raw Path | Status |
| --- | --- | --- | --- | --- |
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

## Validation Rules

- `download_verified_by_codex` stays `false` unless Codex directly observes the download event.
- `schema_verified_by_codex` stays `false` until raw files are present and columns are inspected.
- `sha256` stays `TO_BE_FILLED` until raw files exist.
- A single current snapshot does not create a full `Point-in-Time` Universe.
- Strategy interpretation remains `hold`.
- Manifest verification uses `scripts/quant_krx_manifest_verify.py`.

Verifier command:

```powershell
uv run python scripts/quant_krx_manifest_verify.py `
  --manifest _report/raw/2026/2026-06-13/krx/universe/manifest.yaml `
  --output _report/quant/research/YYYY-MM-DD-krx-manual-snapshot-verify-result.md
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
