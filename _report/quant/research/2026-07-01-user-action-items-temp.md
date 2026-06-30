# Quant User Action Items - Temporary

## Purpose

This is a temporary decision checklist for items that require the user's authority, account access, or policy choice.

The agent should keep progressing reversible local work and read-only KIS data collection while these items are pending.

## User Action Items

### 1. KRX OpenAPI Access

Status: `needed`

What to do:

- Create or confirm access at the KRX OpenAPI site: https://openapi.krx.co.kr/contents/OPP/MAIN/main/index.cmd
- Apply for an API authentication key if the account does not already have one.
- Keep the key outside the repository. Do not paste it into `_report/`, `omx_wiki/`, tracked scripts, or chat logs intended for commit.

Why it matters:

- KRX OpenAPI is the preferred first source for reproducible daily KRX market data.
- KIS read-only OHLCV can continue as a smoke/current-snapshot feed, but it should not become the only historical Backtest data source.

### 2. Point-in-Time Data Source Policy

Status: `needed_before_backtest_interpretation`

Recommended policy:

- Primary: KRX OpenAPI for daily stock market data and basic stock data where available.
- Secondary: KRX Data Marketplace pages, especially `전종목 기본정보`, `전종목 지정내역`, and related stock status datasets.
- Event source: KIND for managed issue, trading suspension, market alert, and delisting disclosures/events where KRX Data Marketplace does not provide a clean historical table.
- Fallback: if historical status cannot be replayed reliably, label the Backtest scope as `pit_status_quality=limited` and restrict any Backtest to the period after local snapshots start.

Official entry points:

- KRX OpenAPI: https://openapi.krx.co.kr/contents/OPP/MAIN/main/index.cmd
- KRX Data Marketplace: https://data.krx.co.kr/contents/MDC/MAIN/main/index.cmd
- KIND: https://kind.krx.co.kr/main.do?method=loadInitPage

Decision needed from user:

- Use the recommended policy above unless there is a paid/vendor data source the user wants to use instead.

### 3. Backtest Default Conditions

Status: `default_recommended`

Use these defaults unless the user changes them:

- Strategy first: `001 Momentum`
- Rebalance: `monthly`
- Signal date: month-end close, calculated only from data known by that date
- Execution date: next trading day, not same close
- Initial Universe: KOSPI/KOSDAQ common stocks after instrument/status filters
- First practical scope: top-liquidity subset of roughly `300-500` names before full Universe
- Liquidity Filter: prior 20 trading days average trading value at least `1,000,000,000 KRW`
- Cost model base: round-trip `30 bp`
- Cost model stress: round-trip `60 bp` and `100 bp`
- Benchmarks: KOSPI, KOSDAQ, KOSPI200

Why Momentum first:

- It matches the existing `001` strategy spec.
- It has lower implementation ambiguity than short-term Reversal for the first end-to-end Backtest pipeline.

### 4. Data Collection Scope

Status: `recommended_default`

Recommended choice:

- Continue KIS read-only OHLCV batch collection for the current-snapshot Universe.
- Use the full generated Universe as the long-run coverage target.
- For first Backtest engineering, use a top-liquidity subset until Point-in-Time status data is good enough.

Do not do yet:

- Do not use current-snapshot Universe membership as historical membership.
- Do not turn paper/smoke Signal Candidate output into live trading.

## Agent Can Continue Without User Input

The agent can safely continue:

- Generate the next `--skip-existing --limit 10` KIS OHLCV batch plan.
- Run dry-run validation for the queue.
- Run read-only KIS capture if credentials/network are available in the environment.
- Save raw responses under `_report/raw/**`.
- Re-run [[scripts/quant_smoke_validate.py|scripts/quant_smoke_validate.py]].
- Re-run [[scripts/quant_liquidity_filter.py|scripts/quant_liquidity_filter.py]].
- Update [[omx_wiki/quant-next-session-handoff-2026-06-14|omx_wiki/quant-next-session-handoff-2026-06-14.md]] after meaningful milestones.
- Update [[omx_wiki/quant-implementation-status-2026-06-14|omx_wiki/quant-implementation-status-2026-06-14.md]] after meaningful milestones.
- Update [[_report/quant/implementation-roadmap|_report/quant/implementation-roadmap.md]] after meaningful milestones.
- Add local schema/config scaffolding for Point-in-Time tables without fetching protected or credentialed KRX data.

## Current Readiness Gate

- Backtest readiness: `hold`
- Live trading readiness: `blocked`

The user does not need to do anything immediately for the agent to continue current-snapshot OHLCV coverage.
