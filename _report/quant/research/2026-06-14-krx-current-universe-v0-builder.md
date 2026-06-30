# KRX Current Universe v0 Builder

- Date: 2026-06-14
- Scope: current snapshot Universe for paper/smoke validation
- Status: builder ready, `listed_issues_current` raw missing
- Bias Control judgment: `hold`

## Purpose

Build a current KRX Universe v0 from official manual CSV snapshots:

1. Start from `listed_issues_current.raw.csv`.
2. Keep KOSPI/KOSDAQ common-stock-like rows.
3. Exclude SPAC, REIT, preferred share, ETF, ETN, ELW style instruments by type/name.
4. Exclude every code in `managed_issues_current.raw.csv`.
5. Exclude rows with less than `365` calendar days since listing date.

This does not solve `Point-in-Time Universe`. It is only a current snapshot for paper/smoke work.

## Required Raw Files

| Dataset | KRX menu path | Save as |
| --- | --- | --- |
| Listed issues current | `KRX Data Marketplace > 통계 > 기본 통계 > 주식 > 종목정보 > 전종목 기본정보` | [[_report/raw/2026/2026-06-13/krx/universe/listed_issues_current.raw.csv|_report/raw/2026/2026-06-13/krx/universe/listed_issues_current.raw.csv]] |
| Managed issues current | `KRX Data Marketplace > 통계 > 이슈 통계 > 관리종목 > 관리종목 현황` | [[_report/raw/2026/2026-06-13/krx/universe/managed_issues_current.raw.csv|_report/raw/2026/2026-06-13/krx/universe/managed_issues_current.raw.csv]] |

`managed_issues_current.raw.csv` is already present locally and has been verified. `listed_issues_current.raw.csv` is still missing.

## Build Command

After `listed_issues_current.raw.csv` is saved:

```powershell
uv run python scripts\quant_krx_current_universe_build.py `
  --listed-raw _report\raw\2026\2026-06-13\krx\universe\listed_issues_current.raw.csv `
  --managed-raw _report\raw\2026\2026-06-13\krx\universe\managed_issues_current.raw.csv `
  --as-of-date 2026-06-13 `
  --output _report\quant\research\2026-06-14-krx-current-universe-v0.md `
  --csv-output _report\quant\research\2026-06-14-krx-current-universe-v0.rows.csv
```

## Expected Output

- Markdown summary: [[_report/quant/research/2026-06-14-krx-current-universe-v0|_report/quant/research/2026-06-14-krx-current-universe-v0.md]]
- Machine-readable rows: [[_report/quant/research/2026-06-14-krx-current-universe-v0.rows.csv|_report/quant/research/2026-06-14-krx-current-universe-v0.rows.csv]]

## Guardrails

- Do not treat this as Backtest-ready.
- Do not treat current listed issues as historical membership.
- Listing Age is represented by a current-snapshot calendar-day guard, not exact historical trading-day age.
- Liquidity Filter, trading suspension, market-alert, and delisting history remain unresolved.
- Keep Strategy interpretation at `hold`.
