# Point-in-Time Status Source Gap

## Summary

- Date: `2026-07-03`
- Scope: KRX `Point-in-Time` status replay source selection
- Current judgment: `kind_current_snapshot_validated_but_historical_gap_remains`
- Backtest readiness: `hold`

KRX OpenAPI is now usable for official KOSPI/KOSDAQ daily market data, issue base rows, index rows, continuity checks, and a date-scoped market-data join.
It still does not solve `Point-in-Time Universe` status replay.

## Official Source Check

KRX OpenAPI service list:

- URL: [KRX OpenAPI service list](https://openapi.krx.co.kr/contents/OPP/INFO/service/OPPINFO004.cmd)
- Official list says KRX OpenAPI data coverage is generally `2010` onward.
- The stock OpenAPI services visible in the official list are daily trading rows and issue base rows for KOSPI/KOSDAQ/KONEX and related instruments.
- I did not find a listed OpenAPI service for historical managed issue, trading halt, market alert, or delisting event replay.

KRX Data Marketplace:

- URL: [KRX Data Marketplace main](https://data.krx.co.kr/contents/MDC/MAIN/main/index.cmd)
- The main menu exposes stock `종목정보` pages including `전종목 기본정보` and `전종목 지정내역`.
- This is the best official next candidate for manual/downloadable status snapshots, but it is not yet a clean automated OpenAPI path in this repo.
- 2026-07-03 probe found official `bld` identifiers for core status screens, but unattended JSON calls returned `auth_required`/`LOGOUT` without a KRX Data Marketplace login session.
- Probe artifact: [[_report/quant/research/2026-07-03-krx-data-marketplace-status-source-probe|_report/quant/research/2026-07-03-krx-data-marketplace-status-source-probe.md]]

KIND:

- URL: [KIND main](https://kind.krx.co.kr/main.do?method=loadInitPage)
- KIND is now the official public fallback validated for one current status snapshot across managed issue, trading halt, market alert, and delisting rows.
- 2026-07-03 public download probe returned table downloads for `6/7` status sources without login.
- The captured KIND snapshot normalized into `344` valid status-event rows, then replayed against the 17-date KRX OpenAPI market-data join and marked `280/46659` rows as `exclude_by_status_event`.
- Local market enrichment from the 17-date KRX OpenAPI market-data join resolved `310/344` KIND event rows; `34` remain `UNKNOWN`.
- KIND still does not yet solve full historical status coverage for a selected Backtest range.
- Probe artifact: [[_report/quant/research/2026-07-03-kind-status-source-probe|_report/quant/research/2026-07-03-kind-status-source-probe.md]]
- Extract artifact: [[_report/quant/research/2026-07-03-kind-status-events-extract|_report/quant/research/2026-07-03-kind-status-events-extract.md]]
- Validation artifact: [[_report/quant/research/2026-07-03-kind-status-events-validation|_report/quant/research/2026-07-03-kind-status-events-validation.md]]
- Replay artifact: [[_report/quant/research/2026-07-03-kind-status-replay-on-openapi-20250102-20250124|_report/quant/research/2026-07-03-kind-status-replay-on-openapi-20250102-20250124.md]]
- Market enrichment artifact: [[_report/quant/research/2026-07-03-kind-status-events-market-enrich|_report/quant/research/2026-07-03-kind-status-events-market-enrich.md]]

## Existing Repo Evidence

- Current-snapshot managed issue exclusion exists through [[scripts/quant_krx_managed_issues_extract.py|scripts/quant_krx_managed_issues_extract.py]].
- Current Universe v0 uses current KRX listed issues and current managed issue exclusions only.
- Existing docs already warn that `관리종목 지정 내역(개별종목)` has range/UI constraints and is not a full historical Universe source.
- The new KRX OpenAPI market-data path gives clean market data but no status event replay.

## Recommended Source Policy

Use a three-lane source policy:

| Lane | Use | Status |
| --- | --- | --- |
| KRX OpenAPI | Official daily stock/index market data and issue base rows from `2010` onward | usable |
| KRX Data Marketplace | Official status snapshots/tables such as `전종목 지정내역` when downloadable | candidate |
| KIND | Event/disclosure fallback for managed issue, trading halt/resumption, market alert, and delisting events | current snapshot fallback validated; historical coverage incomplete |

## Minimal Schema Needed

Create local status-event rows before any Backtest interpretation:

| Column | Meaning |
| --- | --- |
| `event_date` | Effective or disclosed date |
| `code` | KRX short code, preserved exactly |
| `market` | KOSPI/KOSDAQ/KONEX where known |
| `status_type` | managed_issue, trading_halt, trading_resume, market_alert, delisting |
| `status_value` | designated, released, halted, resumed, warned, delisted, etc. |
| `source` | krx_data_marketplace, kind, manual_snapshot |
| `source_url` | Official page URL if available |
| `raw_path` | Saved raw evidence path under `_report/raw/**` |
| `confidence` | high/medium/low |
| `notes` | Parser or interpretation caveats |

## Follow-Up Implementation

Schema/config scaffolding now exists in [[_report/quant/research/2026-07-03-point-in-time-status-event-schema|_report/quant/research/2026-07-03-point-in-time-status-event-schema.md]].
One KIND current snapshot has been normalized, validated, market-enriched, and replayed. The next implementation step is to extend KIND or authenticated/manual KRX status coverage across the selected historical date range, resolve remaining `UNKNOWN` market rows where official evidence supports it, and only then wire status replay into `Universe`.

## Guardrails

- Do not treat the KRX OpenAPI market-data join as a `Point-in-Time Universe`.
- Do not start Backtest/OOS interpretation until status replay exists for the selected test scope.
- Preserve alphanumeric short codes exactly.
- Keep raw status evidence under `_report/raw/**`; commit only summaries, manifests, and parser code.
- Treat unattended KRX Data Marketplace status JSON as blocked until an authenticated or officially approved non-login path is confirmed.
- Do not treat one KIND current snapshot as full historical `Point-in-Time` coverage.
