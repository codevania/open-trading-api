# KIS Demo Trading Readiness

## Summary

- Date: `2026-07-03`
- Scope: KIS API demo trading readiness for Quant pipeline
- KIS API order execution in this document: `false`
- Demo trading readiness: `not_ready_but_preflight_started`
- Live trading readiness: `blocked`
- Latest local account preflight: `blocked_missing_kis_paper_stock`

The repo has read-only KIS/KRX market-data collection, status replay, and `Point-in-Time Universe` smoke plumbing. It does not yet have a safe order executor.

## Local API Surface Evidence

- Domestic stock cash order example exists at [[examples_llm/domestic_stock/order_cash/order_cash.py|examples_llm/domestic_stock/order_cash/order_cash.py]].
- Domestic stock buying-power lookup exists at [[examples_llm/domestic_stock/inquire_psbl_order/inquire_psbl_order.py|examples_llm/domestic_stock/inquire_psbl_order/inquire_psbl_order.py]].
- Domestic stock sellable-quantity lookup exists in the MCP config as `inquire_psbl_sell`.
- Domestic stock correction/cancel order exists at [[examples_llm/domestic_stock/order_rvsecncl/order_rvsecncl.py|examples_llm/domestic_stock/order_rvsecncl/order_rvsecncl.py]].
- Local README examples describe demo auth as `svr="vps"` and order examples with `env_dv="demo"`.

## Implemented Now

- Demo-only order intent preflight: [[scripts/quant_kis_demo_order_preflight.py|scripts/quant_kis_demo_order_preflight.py]]
- Tests: [[tests/test_quant_kis_demo_order_preflight.py|tests/test_quant_kis_demo_order_preflight.py]]
- Demo account config preflight without printing secrets: [[scripts/quant_kis_demo_account_preflight.py|scripts/quant_kis_demo_account_preflight.py]]
- Tests: [[tests/test_quant_kis_demo_account_preflight.py|tests/test_quant_kis_demo_account_preflight.py]]
- Latest local result: [[_report/quant/research/2026-07-04-kis-demo-account-preflight|_report/quant/research/2026-07-04-kis-demo-account-preflight.md]]

The preflight accepts only conservative demo order intents by default:

- `env_dv=demo`
- `dry_run=true`
- `order_type=limit`
- `quantity <= 1`
- `order_value_krw <= 100000`
- `order_side=buy`

Sell intents are intentionally invalid until a separate demo position check exists.

The local MCP `.env.kis` preflight found:

- demo app key: present
- demo app secret: present
- demo stock account: blocked because `KIS_PAPER_STOCK` is empty
- demo REST URL: warning only; KIS template default may apply

No credential or account values are stored in the report.

## Readiness Estimate

Fastest safe path to first KIS demo order:

| Work item | Estimate |
| --- | ---: |
| Demo auth/account preflight without printing secrets | 0.5-1 day |
| Buying-power and sellable-quantity read-only checks | 0.5-1 day |
| Demo order wrapper with kill switch, dry-run default, and explicit confirmation gate | 1-2 days |
| One-share limit-buy demo smoke, then immediate order-status/cancel workflow | 0.5-1 day |
| Logging, raw response storage, and regression tests | 1-2 days |

Practical estimate: `3-7 working days` for a controlled first demo order after credentials and account config are verified locally.

Current user-side action item:

- Fill `KIS_PAPER_STOCK` in the ignored local file `MCP/Kis Trading MCP/.env.kis`.

Quant-system demo trading from generated signals is longer:

| Work item | Estimate |
| --- | ---: |
| Strategy Candidate generation from `Point-in-Time Universe` rows | 2-4 days |
| Position sizing and portfolio constraints | 2-4 days |
| Backtest/OOS/Bias Control minimum pass | 1-3 weeks |
| Demo execution integration and monitoring | 1 week |

Practical estimate: `3-6 weeks` for demo trading driven by the Quant pipeline rather than a manual one-share smoke.

## Guardrails

- Do not place KIS orders from daily-report or research workflows.
- Use `find_api_detail` before any KIS order-capable API call in a KIS MCP-capable surface.
- Keep order execution disabled by default.
- Keep `env_dv=demo` hard-gated until Backtest/OOS/Bias Control pass.
- Do not move to live trading while `Live trading readiness` is `blocked`.
