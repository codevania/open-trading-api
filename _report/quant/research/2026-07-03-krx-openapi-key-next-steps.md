# KRX OpenAPI Key Next Steps

## Status

- User has obtained a KRX OpenAPI authentication key.
- The key must not be pasted into chat, `_report/`, `omx_wiki/`, tracked scripts, or commit history.
- Local secret path: `.env.krx`
- Example template: `.env.krx.example`
- Read-only probe script: [[scripts/quant_krx_openapi_probe.py|scripts/quant_krx_openapi_probe.py]]

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

The KRX service page provides the official sample/service URL after the service is available. Use that URL in the probe script.

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
