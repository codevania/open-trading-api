# KRX Managed Issue History Targets

- Date: 2026-06-14
- Snapshot as-of: 2026-06-13
- Source raw: `_report/raw/2026/2026-06-13/krx/universe/managed_issues_current.raw.csv`
- Raw status: local manual download verified for presence, hash, and CSV schema
- Interpretation: sample evidence for `관리종목 지정 내역(개별종목)`, not a full `Point-in-Time Universe`

## Current Managed Issues Snapshot

- Row count: 101
- Columns: `종목코드`, `종목명`, `현재가`, `등락구분코드`, `등락폭`, `등락률`, `거래량`, `거래대금`, `지정일자`
- Manifest result: `managed_issues_current` passed hash and schema checks
- Overall KRX manual snapshot remains `pending` because `managed_issue_designation_history` is still missing

## Query Period

Use the longest available range:

- Start date: `2000-01-01`
- End date: `2026-06-13`

Fallback if KRX rejects or times out:

- Start date: `2010-01-01`
- End date: `2026-06-13`

If that still fails, split by year and preserve each raw file separately.

## Control Targets

These are normal large-cap comparison targets. Their history queries help confirm whether the screen returns empty rows cleanly for non-managed control names.

| Code | Company | Save as |
| --- | --- | --- |
| `005930` | Samsung Electronics | `managed_issue_history_005930_samsung_electronics.raw.csv` |
| `000660` | SK hynix | `managed_issue_history_000660_sk_hynix.raw.csv` |
| `035420` | NAVER | `managed_issue_history_035420_naver.raw.csv` |

## Managed Issue Sample Targets

Chosen from the current managed issues CSV by recent designation date, excluding REIT/SPAC names for the default common-stock sample.

| Code | Company | Designation date | Save as |
| --- | --- | --- | --- |
| `121850` | 코이즈 | `2026/06/05` | `managed_issue_history_121850_koiz.raw.csv` |
| `017040` | 광명전기 | `2026/05/04` | `managed_issue_history_017040_kwangmyung_electric.raw.csv` |
| `106080` | 케이이엠텍 | `2026/04/20` | `managed_issue_history_106080_kemtec.raw.csv` |
| `024830` | 세원물산 | `2026/04/16` | `managed_issue_history_024830_sewon.raw.csv` |
| `032960` | 동일기연 | `2026/04/16` | `managed_issue_history_032960_dongil_technology.raw.csv` |

## Optional Instrument-Type Edge Cases

These were near the top of the current managed issues CSV but are better treated as separate `Instrument Type` tests, not default common-stock samples.

| Code | Company | Reason |
| --- | --- | --- |
| `348950` | 제이알글로벌리츠 | REIT |
| `464440` | 한국제13호스팩 | SPAC |

## Save Location

Save all history CSVs under:

`_report/raw/2026/2026-06-13/krx/universe/`

After download, rerun:

```powershell
uv run python scripts\quant_krx_manifest_materialize.py `
  --manifest _report\quant\research\2026-06-13-krx-manual-snapshot-manifest.pending.yaml `
  --output _report\raw\2026\2026-06-13\krx\universe\manifest.yaml `
  --allow-pending

uv run python scripts\quant_krx_manifest_verify.py `
  --manifest _report\raw\2026\2026-06-13\krx\universe\manifest.yaml `
  --allow-pending
```

