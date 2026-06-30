# KRX Managed Issue History Targets

- Date: 2026-06-14
- Snapshot as-of: 2026-06-13
- Source raw: [[_report/raw/2026/2026-06-13/krx/universe/managed_issues_current.raw.csv|_report/raw/2026/2026-06-13/krx/universe/managed_issues_current.raw.csv]]
- Raw status: local manual download verified for presence, hash, and CSV schema
- Interpretation: sample evidence for `관리종목 지정 내역(개별종목)`, not a full `Point-in-Time Universe`

## Current Managed Issues Snapshot

- Row count: 101
- Columns: `종목코드`, `종목명`, `현재가`, `등락구분코드`, `등락폭`, `등락률`, `거래량`, `거래대금`, `지정일자`
- Manifest result: `managed_issues_current` passed hash and schema checks
- Overall KRX manual snapshot remains `pending` because `managed_issue_designation_history` is still missing

## Query Period

Observed UI constraint:

- KRX rejects query ranges longer than 2 years.
- A broad 2-year window such as `20240612` to `20260612` may still return no rows on `관리종목 지정 내역(개별종목)`.
- Do not save a blank individual-history CSV as evidence.

Use event-anchored windows from the current managed issues CSV:

1. Select the target through the KRX stock finder popup, not by typing only.
2. Uncheck `시세정보` for the first query.
3. Check `지정일만` for the first query.
4. Query the exact `지정일자`: start date equals end date.
5. If no rows appear, retry a short window around the designation date.
6. If still no rows appear, record `individual history unavailable from KRX UI` and move on.

Do not use this page as a full historical Universe source. It is only a sample event-evidence screen.

## Control Evidence

Do not query these on `관리종목 지정 내역(개별종목)` if the KRX stock finder does not return them. The screen appears to be centered on names with managed-issue designation records, so large-cap normal controls may not be selectable there.

Use the current managed issues CSV as `Negative Control Evidence` instead: confirm these codes are absent from `managed_issues_current.raw.csv`.

| Code | Company | Evidence method |
| --- | --- | --- |
| `005930` | Samsung Electronics | Confirm absence from `managed_issues_current.raw.csv` |
| `000660` | SK hynix | Confirm absence from `managed_issues_current.raw.csv` |
| `035420` | NAVER | Confirm absence from `managed_issues_current.raw.csv` |

Verified result from the current CSV: `005930 Samsung Electronics`, `000660 SK hynix`, and `035420 NAVER` are all `ABSENT`.

## Managed Issue Sample Targets

Chosen from the current managed issues CSV by recent designation date, excluding REIT/SPAC names for the default common-stock sample.

| Code | Company | Designation date | First query | Retry window | Save as |
| --- | --- | --- | --- | --- | --- |
| `121850` | 코이즈 | `2026/06/05` | `20260605` to `20260605` | `20260529` to `20260612` | `managed_issue_history_121850_koiz.raw.csv` |
| `017040` | 광명전기 | `2026/05/04` | `20260504` to `20260504` | `20260427` to `20260511` | `managed_issue_history_017040_kwangmyung_electric.raw.csv` |
| `106080` | 케이이엠텍 | `2026/04/20` | `20260420` to `20260420` | `20260413` to `20260427` | `managed_issue_history_106080_kemtec.raw.csv` |
| `024830` | 세원물산 | `2026/04/16` | `20260416` to `20260416` | `20260409` to `20260423` | `managed_issue_history_024830_sewon.raw.csv` |
| `032960` | 동일기연 | `2026/04/16` | `20260416` to `20260416` | `20260409` to `20260423` | `managed_issue_history_032960_dongil_technology.raw.csv` |

## Optional Instrument-Type Edge Cases

These were near the top of the current managed issues CSV but are better treated as separate `Instrument Type` tests, not default common-stock samples.

| Code | Company | Reason |
| --- | --- | --- |
| `348950` | 제이알글로벌리츠 | REIT |
| `464440` | 한국제13호스팩 | SPAC |

## Save Location

Save all history CSVs under:

`_report/raw/2026/2026-06-13/krx/universe/`

After downloading the managed-issue sample histories, rerun:

```powershell
uv run python scripts\quant_krx_manifest_materialize.py `
  --manifest _report\quant\research\2026-06-13-krx-manual-snapshot-manifest.pending.yaml `
  --output _report\raw\2026\2026-06-13\krx\universe\manifest.yaml `
  --allow-pending

uv run python scripts\quant_krx_manifest_verify.py `
  --manifest _report\raw\2026\2026-06-13\krx\universe\manifest.yaml `
  --allow-pending
```
