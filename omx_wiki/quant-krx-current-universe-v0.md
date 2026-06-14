# Quant KRX Current Universe v0

## Purpose

This page records how the current KRX Universe v0 is built and why it is not yet a `Point-in-Time Universe`.

## Inputs

Raw files are stored under `_report/raw/2026/2026-06-13/krx/universe/` and are intentionally ignored by git:

- `listed_issues_current.raw.csv`
- `managed_issues_current.raw.csv`
- `manifest.yaml`

Tracked derived outputs:

- `_report/quant/research/2026-06-14-krx-current-universe-v0.md`
- `_report/quant/research/2026-06-14-krx-current-universe-v0.rows.csv`
- `_report/quant/research/2026-06-14-krx-managed-issues-current-exclusions.md`

## Build Script

Use:

```powershell
uv run python scripts\quant_krx_current_universe_build.py `
  --listed-raw _report\raw\2026\2026-06-13\krx\universe\listed_issues_current.raw.csv `
  --managed-raw _report\raw\2026\2026-06-13\krx\universe\managed_issues_current.raw.csv `
  --as-of-date 2026-06-13 `
  --output _report\quant\research\2026-06-14-krx-current-universe-v0.md `
  --csv-output _report\quant\research\2026-06-14-krx-current-universe-v0.rows.csv
```

## Current Filters

- Include KOSPI/KOSDAQ listed issues.
- Exclude non-common-stock-like instruments by type/name.
- Exclude current managed issues.
- Exclude rows with fewer than `365 calendar days` since listing date.

## Current Counts

- Total listed rows: `2875`
- Included rows: `2390`
- Excluded rows: `485`

Known exclusion reason counts:

- `market_not_allowed`: `107`
- `listing_age_calendar_insufficient`: `102`
- `instrument_type_excluded`: `101`
- `managed_issue_current`: `101`
- `instrument_name_excluded`: `97`
- `preferred_share_name`: `15`

## Code Handling Rule

KRX short codes may be alphanumeric. Preserve values exactly after basic normalization.

Examples:

- `005930` is normal numeric.
- `0004V0` is valid alphanumeric and must not become `000040`.

## Guardrails

- This is a `current_snapshot` artifact for paper/smoke validation.
- It is not a historical `Point-in-Time Universe`.
- `Liquidity Filter`, trading suspension, market alert, delisting history, and exact trading-day Listing Age are not solved here.

