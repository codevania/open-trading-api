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
- `_report/quant/research/2026-06-14-krx-current-universe-v0-liquidity-smoke.md`
- `_report/quant/research/2026-06-14-krx-current-universe-v0-liquidity-smoke.rows.csv`
- `_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-batch-plan.md`
- `_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-batch-plan.requests.jsonl`
- `_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-batch-plan-next10.md`
- `_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-batch-plan-next10.requests.jsonl`
- `_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-capture-dry-run.md`
- `_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-capture-result.md`
- `_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-capture-dry-run-next10.md`
- `_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-capture-result-next10.md`
- `_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-capture-validator-result.md`
- `_report/quant/research/2026-06-15-krx-current-universe-v0-liquidity-smoke-expanded.md`
- `_report/quant/research/2026-06-15-krx-current-universe-v0-liquidity-smoke-expanded.rows.csv`
- `_report/quant/research/2026-06-16-quant-pipeline-gap-prep-list.md`
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

Universe-based OHLCV batch plan dry-run:

```powershell
uv run python scripts\quant_kis_ohlcv_batch_plan.py `
  --universe-csv _report\quant\research\2026-06-14-krx-current-universe-v0.rows.csv `
  --raw-dir _report\raw\2026\2026-06-15\quant\universe-ohlcv `
  --as-of-date 2026-06-15 `
  --start-date 20260301 `
  --end-date 20260615 `
  --limit 10 `
  --skip-existing `
  --output _report\quant\research\2026-06-15-krx-current-universe-v0-ohlcv-batch-plan.md `
  --jsonl-output _report\quant\research\2026-06-15-krx-current-universe-v0-ohlcv-batch-plan.requests.jsonl
```

Universe-based OHLCV queue capture dry-run:

```powershell
uv run python scripts\quant_kis_ohlcv_capture.py `
  --queue _report\quant\research\2026-06-15-krx-current-universe-v0-ohlcv-batch-plan.requests.jsonl `
  --raw-dir _report\raw\2026\2026-06-15\quant\universe-ohlcv `
  --dry-run `
  --limit 10 `
  --output _report\quant\research\2026-06-15-krx-current-universe-v0-ohlcv-capture-dry-run.md
```

First read-only KIS capture subset:

```powershell
uv run python scripts\quant_kis_ohlcv_capture.py `
  --queue _report\quant\research\2026-06-15-krx-current-universe-v0-ohlcv-batch-plan.requests.jsonl `
  --raw-dir _report\raw\2026\2026-06-15\quant\universe-ohlcv `
  --limit 10 `
  --skip-existing `
  --stop-on-error `
  --output _report\quant\research\2026-06-15-krx-current-universe-v0-ohlcv-capture-result.md
```

Second read-only KIS capture subset:

```powershell
uv run python scripts\quant_kis_ohlcv_batch_plan.py `
  --universe-csv _report\quant\research\2026-06-14-krx-current-universe-v0.rows.csv `
  --raw-dir _report\raw\2026\2026-06-15\quant\universe-ohlcv `
  --as-of-date 2026-06-15 `
  --start-date 20260301 `
  --end-date 20260615 `
  --limit 10 `
  --skip-existing `
  --output _report\quant\research\2026-06-15-krx-current-universe-v0-ohlcv-batch-plan-next10.md `
  --jsonl-output _report\quant\research\2026-06-15-krx-current-universe-v0-ohlcv-batch-plan-next10.requests.jsonl

uv run python scripts\quant_kis_ohlcv_capture.py `
  --queue _report\quant\research\2026-06-15-krx-current-universe-v0-ohlcv-batch-plan-next10.requests.jsonl `
  --raw-dir _report\raw\2026\2026-06-15\quant\universe-ohlcv `
  --limit 10 `
  --skip-existing `
  --stop-on-error `
  --output _report\quant\research\2026-06-15-krx-current-universe-v0-ohlcv-capture-result-next10.md
```

Saved-raw Liquidity Filter smoke:

```powershell
uv run python scripts\quant_liquidity_filter.py `
  --universe-csv _report\quant\research\2026-06-14-krx-current-universe-v0.rows.csv `
  --raw-dir _report\raw\2026\2026-06-13\quant\paper-follow-up `
  --as-of-date 2026-06-13 `
  --output _report\quant\research\2026-06-14-krx-current-universe-v0-liquidity-smoke.md `
  --csv-output _report\quant\research\2026-06-14-krx-current-universe-v0-liquidity-smoke.rows.csv
```

Expanded saved-raw Liquidity Filter smoke:

```powershell
uv run python scripts\quant_liquidity_filter.py `
  --universe-csv _report\quant\research\2026-06-14-krx-current-universe-v0.rows.csv `
  --raw-dir _report\raw\2026\2026-06-13\quant\paper-follow-up `
  --raw-dir _report\raw\2026\2026-06-15\quant\universe-ohlcv `
  --as-of-date 2026-06-15 `
  --output _report\quant\research\2026-06-15-krx-current-universe-v0-liquidity-smoke-expanded.md `
  --csv-output _report\quant\research\2026-06-15-krx-current-universe-v0-liquidity-smoke-expanded.rows.csv
```

## Current Filters

- Include KOSPI/KOSDAQ listed issues.
- Exclude non-common-stock-like instruments by type/name.
- Exclude current managed issues.
- Exclude rows with fewer than `365 calendar days` since listing date.
- Apply saved-raw Liquidity Filter smoke where KIS daily OHLCV raw exists.

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

Expanded Liquidity smoke counts:

- Rows with raw OHLCV evaluated: `23`
- Included after saved-raw Liquidity Filter: `14`
- Failed below threshold: `9`
- `liquidity_raw_missing`: `2367`
- Passing evaluated rows include `000080 하이트진로`, `000100 유한양행`, `000120 CJ대한통운`, `000150 두산`, `000210 DL`, `000220 유유제약`, `000240 한국앤컴퍼니`, `000250 삼천당제약`, `000270 기아`, `000370 한화손해보험`, `000390 SP삼화`, `000660 SK하이닉스`, `005930 삼성전자`, `035420 NAVER`

OHLCV batch plan dry-run counts:

- Base included rows: `2390`
- Selected requests: `10`
- First request rows: `000020 동화약품`, `000040 KR모터스`, `000050 경방`

First OHLCV capture counts:

- Dry-run validated rows: `10`
- Live capture status counts: `saved` 9, `skipped_existing` 1
- Raw directory: `_report/raw/2026/2026-06-15/quant/universe-ohlcv/`
- Validator result after second capture: 20 raw files parsed, each with 71 daily rows and latest date `20260615`

Second OHLCV capture counts:

- Existing raw skipped by batch plan: `10`
- Selected requests: `10`
- Live capture status counts: `saved` 10
- First request rows: `000210 DL`, `000220 유유제약`, `000230 일동홀딩스`

## Code Handling Rule

KRX short codes may be alphanumeric. Preserve values exactly after basic normalization.

Examples:

- `005930` is normal numeric.
- `0004V0` is valid alphanumeric and must not become `000040`.

## Guardrails

- This is a `current_snapshot` artifact for paper/smoke validation.
- It is not a historical `Point-in-Time Universe`.
- Full-Universe `Liquidity Filter`, trading suspension, market alert, delisting history, and exact trading-day Listing Age are not solved here.
- `liquidity_raw_missing` means saved raw coverage is missing; it is not an illiquidity conclusion.
- The OHLCV batch plan does not call KIS. Direct capture used local API detail fallback because the current Codex App surface did not expose `domestic_stock.find_api_detail`; use the MCP preflight when available.
