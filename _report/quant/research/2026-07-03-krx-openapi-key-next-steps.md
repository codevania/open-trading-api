# KRX OpenAPI Key Next Steps

## Status

- User has obtained a KRX OpenAPI authentication key.
- User reported that the requested KRX OpenAPI services were approved.
- The key must not be pasted into chat, `_report/`, `omx_wiki/`, tracked scripts, or commit history.
- Local secret path: `.env.krx`
- Example template: `.env.krx.example`
- Read-only probe script: [[scripts/quant_krx_openapi_probe.py|scripts/quant_krx_openapi_probe.py]]
- Core read-only collector: [[scripts/quant_krx_openapi_collect.py|scripts/quant_krx_openapi_collect.py]]

## Why This Matters

KRX OpenAPI is the preferred source for reproducible official KRX market data in the Quant pipeline.
It can reduce dependence on current-snapshot KIS OHLCV collection, but it does not by itself solve the full `Point-in-Time Universe`.

The first objective is not a Backtest. The first objective is a read-only raw-data smoke test.

## User-Side Secret Handling

Create the ignored local file:

```powershell
Copy-Item .env.krx.example .env.krx
notepad .env.krx
```

Fill only this value:

```env
KRX_AUTH_KEY=your_key_here
```

Do not put the key in command arguments. Command history is easier to leak than an ignored local env file.

## KRX Service Approval Needed

KRX OpenAPI has two gates:

1. API authentication key.
2. API service usage approval for each dataset/product.

For the Quant pipeline, prioritize these stock services first:

- KOSPI daily trading data.
- KOSDAQ daily trading data.
- KOSPI basic issue data.
- KOSDAQ basic issue data.
- KOSPI index daily data.
- KOSDAQ index daily data.

The KRX service page provides the official sample/service URL after the service is available. Use that URL in the probe script.

Approved core service mapping:

| service id | KRX API name | endpoint |
| --- | --- | --- |
| `kospi_stock_daily` | 유가증권 일별매매정보 | `https://data-dbg.krx.co.kr/svc/apis/sto/stk_bydd_trd` |
| `kosdaq_stock_daily` | 코스닥 일별매매정보 | `https://data-dbg.krx.co.kr/svc/apis/sto/ksq_bydd_trd` |
| `kospi_issue_base` | 유가증권 종목기본정보 | `https://data-dbg.krx.co.kr/svc/apis/sto/stk_isu_base_info` |
| `kosdaq_issue_base` | 코스닥 종목기본정보 | `https://data-dbg.krx.co.kr/svc/apis/sto/ksq_isu_base_info` |
| `kospi_index_daily` | KOSPI 시리즈 일별시세정보 | `https://data-dbg.krx.co.kr/svc/apis/idx/kospi_dd_trd` |
| `kosdaq_index_daily` | KOSDAQ 시리즈 일별시세정보 | `https://data-dbg.krx.co.kr/svc/apis/idx/kosdaq_dd_trd` |

## Read-Only Smoke Command Shape

```powershell
uv run python scripts/quant_krx_openapi_probe.py `
  --url "OFFICIAL_KRX_SAMPLE_URL" `
  --param basDd=YYYYMMDD `
  --output _report/raw/YYYY/YYYY-MM-DD/krx/openapi/smoke.raw.json
```

The script sends the key as request header `AUTH_KEY` and writes:

- raw response: the `--output` path
- metadata sidecar: `smoke.raw.json.meta.json`

After the core service mapping is known, collect all core raw files with:

```powershell
.venv\Scripts\python.exe scripts/quant_krx_openapi_collect.py --bas-dd YYYYMMDD
```

If `uv run` fails with a local cache permission error, use `.venv\Scripts\python.exe`.

Smoke result on `2025-01-02`:

| service id | row count |
| --- | ---: |
| `kospi_stock_daily` | 961 |
| `kosdaq_stock_daily` | 1784 |
| `kospi_issue_base` | 961 |
| `kosdaq_issue_base` | 1784 |
| `kospi_index_daily` | 51 |
| `kosdaq_index_daily` | 40 |

Smoke result on `2026-07-02`:

- HTTP `200` for all six services.
- `OutBlock_1` row count was `0` for all six services.
- Treat `2026-07-02` as not usable for schema validation yet; use known historical trading days for parser development.

## Interpretation Gate

Passing one KRX OpenAPI smoke test changes the status to:

- KRX OpenAPI access: `usable_for_raw_collection`
- Backtest readiness: still `hold`
- Live trading readiness: still `blocked`

Backtest interpretation remains blocked until the pipeline can reproduce `Point-in-Time` status fields by Rebalance date, including listing status, managed issue status, trading suspension, and delisting events.

## Agent Next Steps

After `.env.krx` is filled and a KRX service URL is available:

1. Run one dry-run probe to confirm the request shape.
2. Run one read-only smoke call for a single date.
3. Save raw response under `_report/raw/**`.
4. Inspect schema and write a parser only after the official raw shape is known.
5. Add KRX raw parser tests before using the data in `Universe` or `Backtest` code.
