# Quant Pipeline Gap / Prep List - 2026-06-16

## Scope

This note lists what remains insufficient after the first two KIS OHLCV Universe capture batches and what the user should prepare before this becomes `Backtest` evidence.

Interpretation remains `current_snapshot` / paper-smoke only.

## Current Evidence

- Current Universe rows: `2875`
- Base included rows before Liquidity Filter: `2390`
- Saved raw OHLCV evaluated by expanded Liquidity Filter: `23`
- Included after saved-raw Liquidity Filter: `14`
- Failed Liquidity Filter: `9`
- Missing raw coverage: `2367`
- Latest OHLCV raw date in captured Universe subset: `20260615`

## What Was Still Insufficient

1. KIS MCP preflight is still unavailable in the current Codex App surface.
   - `domestic_stock.find_api_detail` could not be called directly here.
   - The direct capture path used local `MCP/Kis Trading MCP/configs/domestic_stock.json` and `examples_llm` sample docs as fallback evidence.

2. OHLCV coverage is still far from full Universe coverage.
   - Only `23` rows have saved OHLCV raw out of `2390` base-included current Universe rows.
   - `liquidity_raw_missing` is a data coverage gap, not an illiquidity conclusion.

3. The artifact is not a `Point-in-Time Universe`.
   - Historical membership by Rebalance date is not reproducible.
   - Historical managed issue, trading suspension, market alert, and delisting status are not solved.

4. Listing Age is still a proxy.
   - The Strategy target is `252 trading days`.
   - Current artifact uses `365 calendar days` because a full trading-day calendar path is not built.

5. Data quality handling needs one more guard.
   - `000300 DH오토넥스` returned a `20D` average trading value of `0`, which should remain a low-liquidity/data-quality signal until trading status and suspension history are checked.

6. No `Backtest`, `Out-of-Sample`, or `Bias Control` pass has been run.
   - The current outputs are parser, queue, and Liquidity Filter smoke evidence only.

7. KRX source acquisition is still partly manual.
   - Current listed issue / managed issue snapshots were manually obtained.
   - A reproducible official download or scheduled snapshot routine is still missing.

8. Raw capture manifest is batch-scoped.
   - `_report/raw/.../manifest.yaml` is ignored and can be overwritten by the latest capture batch.
   - Durable batch evidence should remain in tracked capture result markdown files until a cumulative capture manifest is added.

## User Prep List

1. KIS execution surface
   - Prepare a surface where KIS MCP tools are available, or explicitly accept the local direct KIS sample-auth fallback for read-only quotation endpoints.
   - If using MCP, Docker/KIS MCP daemon should be running and `domestic_stock.find_api_detail` should be callable.

2. Batch size and schedule
   - Decide whether to continue in small batches such as `10`, larger batches such as `50` or `100`, or a full one-time current snapshot capture.
   - Larger batches may be faster but increase rate-limit and interruption risk.

3. Historical Universe source
   - Decide how to source historical KRX listed/delisted/managed/suspension/market-alert states.
   - Options include repeated official snapshots, a paid data vendor, or a documented manual archive process.

4. Backtest policy choices
   - Choose benchmark candidates such as KOSPI, KOSDAQ, KOSPI200, KRX300, or market-segment matched benchmarks.
   - Choose rebalance frequency and minimum holding period for the first Strategy test.

5. Data quality policy
   - Decide how to handle rows with zero trading value, trading suspension, new listings, ticker changes, mergers, and delistings before any Strategy result is reported.

6. Paper Signal integration
   - Decide whether Quant `Signal Candidate` sections should be added to the DI daily report template now, or kept as separate Quant research artifacts until the pipeline is more mature.

## Next Agent Actions

1. Continue OHLCV coverage with `scripts/quant_kis_ohlcv_batch_plan.py --skip-existing --limit N`.
2. Capture the queue with `scripts/quant_kis_ohlcv_capture.py`.
3. Re-run `scripts/quant_smoke_validate.py`.
4. Re-run `scripts/quant_liquidity_filter.py`.
5. Update wiki handoff and keep `Point-in-Time` / `Backtest` claims blocked.
