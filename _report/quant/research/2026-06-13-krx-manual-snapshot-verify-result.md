# KRX Manual Snapshot Verify Result

- Manifest: `_report/raw/2026/2026-06-13/krx/universe/manifest.yaml`
- As-of date: `2026-06-13`
- Source mode: `manual_snapshot`
- Overall status: `pending`
- Interpretation: `manual snapshot verification only`, `not Backtest ready`
- Bias Control judgment: `hold`

| Dataset | Required | Raw Exists | Hash | Schema | Status | Message |
| --- | ---: | ---: | --- | --- | --- | --- |
| `listed_issues_current` | true | true | ok | ok | pass | ok |
| `managed_issues_current` | true | true | ok | ok | pass | ok |
| `managed_issue_designation_history` | true | false | pending | pending | pending | required raw file is missing |
| `delisting_events` | false | false | pending | pending | optional-missing | optional raw file is missing |

## Guardrails

- This verifier does not download KRX files.
- `pass` only means the manual snapshot files match the manifest hash and schema.
- A single manual snapshot does not create a reproducible `Point-in-Time` Universe.
- Keep Strategy interpretation at `hold` until historical Point-in-Time snapshots and calendar audits exist.

## Next Checks

1. Download the required KRX files manually if status is `pending`.
2. Fill `downloaded_at_kst`, `sha256`, and `columns` in the final raw-directory manifest.
3. Re-run this verifier against `_report/raw/YYYY/YYYY-MM-DD/krx/universe/manifest.yaml`.
