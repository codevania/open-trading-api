# Point-in-Time Status P1 Official Capture Checklist

- Fill packet: [[_report/quant/research/2026-07-10-point-in-time-status-source-manifest-fill-packet-20250102-20250418-merged-3snapshots-market-enriched-81d.rows.csv|_report/quant/research/2026-07-10-point-in-time-status-source-manifest-fill-packet-20250102-20250418-merged-3snapshots-market-enriched-81d.rows.csv]]
- KIS/KRX API call: `false`
- Order intent generated: `false`
- Backtest readiness impact: `hold`
- Interpretation: operator checklist only, not source coverage evidence

## Summary

| Metric | Value |
| --- | ---: |
| Checklist rows | 10 |
| Pending rows | 10 |
| Ready rows | 0 |

## Source Counts

| Source | Rows |
| --- | ---: |
| `kind` | 3 |
| `krx_data_marketplace` | 3 |
| `manual_snapshot` | 4 |

## Status Type Counts

| Status type | Rows |
| --- | ---: |
| `delisting` | 3 |
| `managed_issue` | 3 |
| `market_alert` | 2 |
| `trading_halt` | 2 |

## Capture Rows

### P1-001 `delisting` / `kind`

- Coverage window: `2025-01-02..2025-04-18`
- Capture state: `pending_official_capture`
- Candidate tables: `Managed issue event;Trading halt or resumption disclosure;Delisting disclosure`
- Source URL hint: `https://kind.krx.co.kr/`
- Raw path suggestion: `_report/raw/quant/status-source-manifest/20250102-20250418/p1-001-delisting-kind.json`
- [ ] Capture official raw evidence from the listed source.
- [ ] Save the raw file under `_report/raw/**`, using the suggestion as a naming aid.
- [ ] Fill `source_url_to_fill`, `raw_path_to_fill`, `confidence_to_fill`, and non-pending `evidence_capture_status` in the fill packet.

### P1-002 `delisting` / `krx_data_marketplace`

- Coverage window: `2025-01-02..2025-04-18`
- Capture state: `pending_official_capture`
- Candidate tables: `Designated details of all issues;Market alert issue;Delisting`
- Source URL hint: `https://data.krx.co.kr/`
- Raw path suggestion: `_report/raw/quant/status-source-manifest/20250102-20250418/p1-002-delisting-krx-data-marketplace.json`
- [ ] Capture official raw evidence from the listed source.
- [ ] Save the raw file under `_report/raw/**`, using the suggestion as a naming aid.
- [ ] Fill `source_url_to_fill`, `raw_path_to_fill`, `confidence_to_fill`, and non-pending `evidence_capture_status` in the fill packet.

### P1-003 `delisting` / `manual_snapshot`

- Coverage window: `2025-01-02..2025-04-18`
- Capture state: `pending_official_capture`
- Candidate tables: `Manual download captured from an official KRX or KIND page`
- Source URL hint: `https://data.krx.co.kr/`
- Raw path suggestion: `_report/raw/quant/status-source-manifest/20250102-20250418/p1-003-delisting-manual-snapshot.json`
- [ ] Capture official raw evidence from the listed source.
- [ ] Save the raw file under `_report/raw/**`, using the suggestion as a naming aid.
- [ ] Fill `source_url_to_fill`, `raw_path_to_fill`, `confidence_to_fill`, and non-pending `evidence_capture_status` in the fill packet.

### P1-004 `managed_issue` / `kind`

- Coverage window: `2025-01-02..2025-04-18`
- Capture state: `pending_official_capture`
- Candidate tables: `Managed issue event;Trading halt or resumption disclosure;Delisting disclosure`
- Source URL hint: `https://kind.krx.co.kr/`
- Raw path suggestion: `_report/raw/quant/status-source-manifest/20250102-20250418/p1-004-managed-issue-kind.json`
- [ ] Capture official raw evidence from the listed source.
- [ ] Save the raw file under `_report/raw/**`, using the suggestion as a naming aid.
- [ ] Fill `source_url_to_fill`, `raw_path_to_fill`, `confidence_to_fill`, and non-pending `evidence_capture_status` in the fill packet.

### P1-005 `managed_issue` / `krx_data_marketplace`

- Coverage window: `2025-01-02..2025-04-18`
- Capture state: `pending_official_capture`
- Candidate tables: `Designated details of all issues;Market alert issue;Delisting`
- Source URL hint: `https://data.krx.co.kr/`
- Raw path suggestion: `_report/raw/quant/status-source-manifest/20250102-20250418/p1-005-managed-issue-krx-data-marketplace.json`
- [ ] Capture official raw evidence from the listed source.
- [ ] Save the raw file under `_report/raw/**`, using the suggestion as a naming aid.
- [ ] Fill `source_url_to_fill`, `raw_path_to_fill`, `confidence_to_fill`, and non-pending `evidence_capture_status` in the fill packet.

### P1-006 `managed_issue` / `manual_snapshot`

- Coverage window: `2025-01-02..2025-04-18`
- Capture state: `pending_official_capture`
- Candidate tables: `Manual download captured from an official KRX or KIND page`
- Source URL hint: `https://data.krx.co.kr/`
- Raw path suggestion: `_report/raw/quant/status-source-manifest/20250102-20250418/p1-006-managed-issue-manual-snapshot.json`
- [ ] Capture official raw evidence from the listed source.
- [ ] Save the raw file under `_report/raw/**`, using the suggestion as a naming aid.
- [ ] Fill `source_url_to_fill`, `raw_path_to_fill`, `confidence_to_fill`, and non-pending `evidence_capture_status` in the fill packet.

### P1-007 `market_alert` / `krx_data_marketplace`

- Coverage window: `2025-01-02..2025-04-18`
- Capture state: `pending_official_capture`
- Candidate tables: `Designated details of all issues;Market alert issue;Delisting`
- Source URL hint: `https://data.krx.co.kr/`
- Raw path suggestion: `_report/raw/quant/status-source-manifest/20250102-20250418/p1-007-market-alert-krx-data-marketplace.json`
- [ ] Capture official raw evidence from the listed source.
- [ ] Save the raw file under `_report/raw/**`, using the suggestion as a naming aid.
- [ ] Fill `source_url_to_fill`, `raw_path_to_fill`, `confidence_to_fill`, and non-pending `evidence_capture_status` in the fill packet.

### P1-008 `market_alert` / `manual_snapshot`

- Coverage window: `2025-01-02..2025-04-18`
- Capture state: `pending_official_capture`
- Candidate tables: `Manual download captured from an official KRX or KIND page`
- Source URL hint: `https://data.krx.co.kr/`
- Raw path suggestion: `_report/raw/quant/status-source-manifest/20250102-20250418/p1-008-market-alert-manual-snapshot.json`
- [ ] Capture official raw evidence from the listed source.
- [ ] Save the raw file under `_report/raw/**`, using the suggestion as a naming aid.
- [ ] Fill `source_url_to_fill`, `raw_path_to_fill`, `confidence_to_fill`, and non-pending `evidence_capture_status` in the fill packet.

### P1-009 `trading_halt` / `kind`

- Coverage window: `2025-01-02..2025-04-18`
- Capture state: `pending_official_capture`
- Candidate tables: `Managed issue event;Trading halt or resumption disclosure;Delisting disclosure`
- Source URL hint: `https://kind.krx.co.kr/`
- Raw path suggestion: `_report/raw/quant/status-source-manifest/20250102-20250418/p1-009-trading-halt-kind.json`
- [ ] Capture official raw evidence from the listed source.
- [ ] Save the raw file under `_report/raw/**`, using the suggestion as a naming aid.
- [ ] Fill `source_url_to_fill`, `raw_path_to_fill`, `confidence_to_fill`, and non-pending `evidence_capture_status` in the fill packet.

### P1-010 `trading_halt` / `manual_snapshot`

- Coverage window: `2025-01-02..2025-04-18`
- Capture state: `pending_official_capture`
- Candidate tables: `Manual download captured from an official KRX or KIND page`
- Source URL hint: `https://data.krx.co.kr/`
- Raw path suggestion: `_report/raw/quant/status-source-manifest/20250102-20250418/p1-010-trading-halt-manual-snapshot.json`
- [ ] Capture official raw evidence from the listed source.
- [ ] Save the raw file under `_report/raw/**`, using the suggestion as a naming aid.
- [ ] Fill `source_url_to_fill`, `raw_path_to_fill`, `confidence_to_fill`, and non-pending `evidence_capture_status` in the fill packet.

## Next Validation

1. Re-run [[scripts/quant_point_in_time_status_source_manifest_fill_progress.py|scripts/quant_point_in_time_status_source_manifest_fill_progress.py]].
2. Run [[scripts/quant_point_in_time_status_source_manifest_materialize.py|scripts/quant_point_in_time_status_source_manifest_materialize.py]] only after every row is ready.
3. Run [[scripts/quant_point_in_time_status_source_manifest_validate.py|scripts/quant_point_in_time_status_source_manifest_validate.py]] on the materialized manifest.

## Guardrails

- This checklist is not a source coverage manifest.
- `source_url_hint` and `raw_path_suggestion` are aids only; do not copy them into evidence fields before capture.
- Keep `Backtest readiness` at `hold` until official raw capture, manifest validation, coverage audit, lifecycle coverage, costs, OOS, and Bias Control pass.
