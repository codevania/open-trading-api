# Point-in-Time P1 Official Capture Operator Guide

- Date: `2026-07-11`
- Scope: P1 source-manifest evidence capture for the `2025-01-02..2025-04-18` window
- Checklist: [[_report/quant/research/2026-07-11-point-in-time-status-p1-official-capture-checklist-20250102-20250418-merged-3snapshots-market-enriched-81d|2026-07-11-point-in-time-status-p1-official-capture-checklist-20250102-20250418-merged-3snapshots-market-enriched-81d.md]]
- Fill packet CSV: [[_report/quant/research/2026-07-10-point-in-time-status-source-manifest-fill-packet-20250102-20250418-merged-3snapshots-market-enriched-81d.rows.csv|2026-07-10-point-in-time-status-source-manifest-fill-packet-20250102-20250418-merged-3snapshots-market-enriched-81d.rows.csv]]
- Current progress: [[_report/quant/research/2026-07-10-point-in-time-status-source-manifest-fill-progress-20250102-20250418-merged-3snapshots-market-enriched-81d|2026-07-10-point-in-time-status-source-manifest-fill-progress-20250102-20250418-merged-3snapshots-market-enriched-81d.md]]
- Order intent generated: `false`
- Backtest readiness impact before capture: `hold`

## Current State

| Metric | Value |
| --- | ---: |
| P1 rows | 10 |
| Materializable rows | 0 |
| Blocked rows | 10 |
| Existing raw paths | 0 |

This is blocked because every P1 row still needs real official evidence fields:

- `source_url_to_fill`
- `raw_path_to_fill`
- `confidence_to_fill`
- `evidence_capture_status`

Do not copy `source_url_hint` or `raw_path_suggestion` into these fields until the official source file has actually been saved.

## Recommended Capture Order

Start with one row at a time. Finish the row, save the raw file, fill the CSV fields, then move to the next row.

| Order | Batch IDs | Source | Why first |
| ---: | --- | --- | --- |
| 1 | `P1-002`, `P1-005`, `P1-007` | `krx_data_marketplace` | Same official site and similar table workflow |
| 2 | `P1-001`, `P1-004`, `P1-009` | `kind` | Official disclosure source for event-style status evidence |
| 3 | `P1-003`, `P1-006`, `P1-008`, `P1-010` | `manual_snapshot` | Use only after the official page/export path is identified |

## What You Do For Each Row

1. Open the P1 checklist and pick one `batch_id`.
2. Open the `Source URL hint` shown for that row.
3. Search the candidate table names shown in `Candidate tables`.
4. Apply the coverage window if the site supports dates: `2025-01-02` through `2025-04-18`.
5. Export or save the official evidence exactly as provided by the source.
6. Put the file under this ignored raw folder:

```powershell
_report\raw\quant\status-source-manifest\20250102-20250418\
```

7. Use the suggested filename as a naming aid, but keep the real extension if the site downloads CSV, XLSX, HTML, PDF, or an image.
8. Open the fill packet CSV and fill only the row you captured.

## How To Fill The CSV

For the captured row:

| Column | What to enter |
| --- | --- |
| `source_url_to_fill` | The actual official page URL used for the capture, under the allowed KRX/KIND prefix |
| `raw_path_to_fill` | Repo-relative path to the saved raw file under `_report/raw/**` |
| `confidence_to_fill` | `high`, `medium`, or `low` |
| `evidence_capture_status` | `captured_official_raw` for an official export, or `captured_official_manual_snapshot` for an official page snapshot |

Use `high` when the official export directly covers the required status type and window. Use `medium` when the source is official but the evidence is page-level, manually filtered, or not a clean structured export. Use `low` only when the source is official but the capture is weak; tell me before relying on a `low` row for Backtest readiness.

Example shape:

```csv
source_url_to_fill,raw_path_to_fill,confidence_to_fill,evidence_capture_status
https://data.krx.co.kr/...,_report/raw/quant/status-source-manifest/20250102-20250418/p1-002-delisting-krx-data-marketplace.xlsx,high,captured_official_raw
```

## What You Should Not Do

- Do not edit the raw file contents after download.
- Do not put downloaded raw files outside `_report/raw/**`.
- Do not treat the current checklist, fill packet, or progress report as evidence.
- Do not fill all 10 rows from assumptions. Each row needs a saved official raw artifact.
- Do not use broker, blog, Naver, or news pages for P1. P1 is for KRX/KIND official evidence only.

## What I Do After You Save Files

After one or more rows are filled, I run:

```powershell
.venv\Scripts\python.exe scripts\quant_point_in_time_status_source_manifest_fill_progress.py --fill-packet _report\quant\research\2026-07-10-point-in-time-status-source-manifest-fill-packet-20250102-20250418-merged-3snapshots-market-enriched-81d.rows.csv --rows-output _report\quant\research\2026-07-10-point-in-time-status-source-manifest-fill-progress-20250102-20250418-merged-3snapshots-market-enriched-81d.rows.csv --report-output _report\quant\research\2026-07-10-point-in-time-status-source-manifest-fill-progress-20250102-20250418-merged-3snapshots-market-enriched-81d.md
```

When `Materializable rows` equals `10`, I then run materialization:

```powershell
.venv\Scripts\python.exe scripts\quant_point_in_time_status_source_manifest_materialize.py --fill-packet _report\quant\research\2026-07-10-point-in-time-status-source-manifest-fill-packet-20250102-20250418-merged-3snapshots-market-enriched-81d.rows.csv --output _report\quant\research\2026-07-11-point-in-time-status-source-coverage-manifest-20250102-20250418.rows.csv --report-output _report\quant\research\2026-07-11-point-in-time-status-source-coverage-manifest-20250102-20250418.md
```

Then I validate the materialized manifest and update the Point-in-Time readiness reports. Until that succeeds, `Backtest` readiness remains `hold`.

