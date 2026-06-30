# Quant KRX Current Universe v0

## Purpose

This page records how the current KRX Universe v0 is built and why it is not yet a `Point-in-Time Universe`.

## Inputs

Raw files are stored under `_report/raw/2026/2026-06-13/krx/universe/` and are intentionally ignored by git:

- `listed_issues_current.raw.csv`
- `managed_issues_current.raw.csv`
- `manifest.yaml`

Tracked derived outputs:

- [[_report/quant/research/2026-06-14-krx-current-universe-v0|_report/quant/research/2026-06-14-krx-current-universe-v0.md]]
- [[_report/quant/research/2026-06-14-krx-current-universe-v0.rows.csv|_report/quant/research/2026-06-14-krx-current-universe-v0.rows.csv]]
- [[_report/quant/research/2026-06-14-krx-current-universe-v0-liquidity-smoke|_report/quant/research/2026-06-14-krx-current-universe-v0-liquidity-smoke.md]]
- [[_report/quant/research/2026-06-14-krx-current-universe-v0-liquidity-smoke.rows.csv|_report/quant/research/2026-06-14-krx-current-universe-v0-liquidity-smoke.rows.csv]]
- [[_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-batch-plan|_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-batch-plan.md]]
- [[_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-batch-plan.requests.jsonl|_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-batch-plan.requests.jsonl]]
- [[_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-batch-plan-next10|_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-batch-plan-next10.md]]
- [[_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-batch-plan-next10.requests.jsonl|_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-batch-plan-next10.requests.jsonl]]
- [[_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-capture-dry-run|_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-capture-dry-run.md]]
- [[_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-capture-result|_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-capture-result.md]]
- [[_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-capture-dry-run-next10|_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-capture-dry-run-next10.md]]
- [[_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-capture-result-next10|_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-capture-result-next10.md]]
- [[_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-capture-validator-result|_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-capture-validator-result.md]]
- [[_report/quant/research/2026-06-15-krx-current-universe-v0-liquidity-smoke-expanded|_report/quant/research/2026-06-15-krx-current-universe-v0-liquidity-smoke-expanded.md]]
- [[_report/quant/research/2026-06-15-krx-current-universe-v0-liquidity-smoke-expanded.rows.csv|_report/quant/research/2026-06-15-krx-current-universe-v0-liquidity-smoke-expanded.rows.csv]]
- [[_report/quant/research/2026-06-16-quant-pipeline-gap-prep-list|_report/quant/research/2026-06-16-quant-pipeline-gap-prep-list.md]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-third10|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-third10.md]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-third10.requests.jsonl|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-third10.requests.jsonl]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-dry-run-third10|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-dry-run-third10.md]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-result-third10|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-result-third10.md]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-validator-result-third10|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-validator-result-third10.md]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-liquidity-smoke-expanded-third10|_report/quant/research/2026-06-17-krx-current-universe-v0-liquidity-smoke-expanded-third10.md]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-liquidity-smoke-expanded-third10.rows.csv|_report/quant/research/2026-06-17-krx-current-universe-v0-liquidity-smoke-expanded-third10.rows.csv]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-fourth10|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-fourth10.md]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-fourth10.requests.jsonl|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-fourth10.requests.jsonl]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-dry-run-fourth10|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-dry-run-fourth10.md]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-result-fourth10|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-result-fourth10.md]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-validator-result-fourth10|_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-validator-result-fourth10.md]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-liquidity-smoke-expanded-fourth10|_report/quant/research/2026-06-17-krx-current-universe-v0-liquidity-smoke-expanded-fourth10.md]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-liquidity-smoke-expanded-fourth10.rows.csv|_report/quant/research/2026-06-17-krx-current-universe-v0-liquidity-smoke-expanded-fourth10.rows.csv]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-fifth10|2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-fifth10.md]], [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-fifth10.requests.jsonl|2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-fifth10.requests.jsonl]], [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-dry-run-fifth10|2026-06-17-krx-current-universe-v0-ohlcv-capture-dry-run-fifth10.md]], [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-result-fifth10|2026-06-17-krx-current-universe-v0-ohlcv-capture-result-fifth10.md]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-sixth10|2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-sixth10.md]], [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-sixth10.requests.jsonl|2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-sixth10.requests.jsonl]], [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-dry-run-sixth10|2026-06-17-krx-current-universe-v0-ohlcv-capture-dry-run-sixth10.md]], [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-result-sixth10|2026-06-17-krx-current-universe-v0-ohlcv-capture-result-sixth10.md]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-seventh10|2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-seventh10.md]], [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-seventh10.requests.jsonl|2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-seventh10.requests.jsonl]], [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-dry-run-seventh10|2026-06-17-krx-current-universe-v0-ohlcv-capture-dry-run-seventh10.md]], [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-result-seventh10|2026-06-17-krx-current-universe-v0-ohlcv-capture-result-seventh10.md]], [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-validator-result-seventh10|2026-06-17-krx-current-universe-v0-ohlcv-capture-validator-result-seventh10.md]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-liquidity-smoke-expanded-seventh10|_report/quant/research/2026-06-17-krx-current-universe-v0-liquidity-smoke-expanded-seventh10.md]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-liquidity-smoke-expanded-seventh10.rows.csv|_report/quant/research/2026-06-17-krx-current-universe-v0-liquidity-smoke-expanded-seventh10.rows.csv]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-eighth10|2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-eighth10.md]], [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-eighth10.requests.jsonl|2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-eighth10.requests.jsonl]], [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-dry-run-eighth10|2026-06-17-krx-current-universe-v0-ohlcv-capture-dry-run-eighth10.md]], [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-result-eighth10|2026-06-17-krx-current-universe-v0-ohlcv-capture-result-eighth10.md]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-ninth10|2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-ninth10.md]], [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-ninth10.requests.jsonl|2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-ninth10.requests.jsonl]], [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-dry-run-ninth10|2026-06-17-krx-current-universe-v0-ohlcv-capture-dry-run-ninth10.md]], [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-result-ninth10|2026-06-17-krx-current-universe-v0-ohlcv-capture-result-ninth10.md]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-tenth10|2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-tenth10.md]], [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-tenth10.requests.jsonl|2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-tenth10.requests.jsonl]], [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-dry-run-tenth10|2026-06-17-krx-current-universe-v0-ohlcv-capture-dry-run-tenth10.md]], [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-result-tenth10|2026-06-17-krx-current-universe-v0-ohlcv-capture-result-tenth10.md]], [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-validator-result-tenth10|2026-06-17-krx-current-universe-v0-ohlcv-capture-validator-result-tenth10.md]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-liquidity-smoke-expanded-tenth10|_report/quant/research/2026-06-17-krx-current-universe-v0-liquidity-smoke-expanded-tenth10.md]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-liquidity-smoke-expanded-tenth10.rows.csv|_report/quant/research/2026-06-17-krx-current-universe-v0-liquidity-smoke-expanded-tenth10.rows.csv]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-eleventh10|2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-eleventh10.md]], [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-eleventh10.requests.jsonl|2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-eleventh10.requests.jsonl]], [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-dry-run-eleventh10|2026-06-17-krx-current-universe-v0-ohlcv-capture-dry-run-eleventh10.md]], [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-result-eleventh10|2026-06-17-krx-current-universe-v0-ohlcv-capture-result-eleventh10.md]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-twelfth10|2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-twelfth10.md]], [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-twelfth10.requests.jsonl|2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-twelfth10.requests.jsonl]], [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-dry-run-twelfth10|2026-06-17-krx-current-universe-v0-ohlcv-capture-dry-run-twelfth10.md]], [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-result-twelfth10|2026-06-17-krx-current-universe-v0-ohlcv-capture-result-twelfth10.md]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-thirteenth10|2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-thirteenth10.md]], [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-thirteenth10.requests.jsonl|2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-thirteenth10.requests.jsonl]], [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-dry-run-thirteenth10|2026-06-17-krx-current-universe-v0-ohlcv-capture-dry-run-thirteenth10.md]], [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-result-thirteenth10|2026-06-17-krx-current-universe-v0-ohlcv-capture-result-thirteenth10.md]], [[_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-validator-result-thirteenth10|2026-06-17-krx-current-universe-v0-ohlcv-capture-validator-result-thirteenth10.md]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-liquidity-smoke-expanded-thirteenth10|_report/quant/research/2026-06-17-krx-current-universe-v0-liquidity-smoke-expanded-thirteenth10.md]]
- [[_report/quant/research/2026-06-17-krx-current-universe-v0-liquidity-smoke-expanded-thirteenth10.rows.csv|_report/quant/research/2026-06-17-krx-current-universe-v0-liquidity-smoke-expanded-thirteenth10.rows.csv]]
- [[_report/quant/research/2026-06-18-krx-current-universe-v0-ohlcv-batch-plan-fourteenth10|2026-06-18-krx-current-universe-v0-ohlcv-batch-plan-fourteenth10.md]], [[_report/quant/research/2026-06-18-krx-current-universe-v0-ohlcv-batch-plan-fourteenth10.requests.jsonl|2026-06-18-krx-current-universe-v0-ohlcv-batch-plan-fourteenth10.requests.jsonl]], [[_report/quant/research/2026-06-18-krx-current-universe-v0-ohlcv-capture-dry-run-fourteenth10|2026-06-18-krx-current-universe-v0-ohlcv-capture-dry-run-fourteenth10.md]], [[_report/quant/research/2026-06-18-krx-current-universe-v0-ohlcv-capture-result-fourteenth10|2026-06-18-krx-current-universe-v0-ohlcv-capture-result-fourteenth10.md]]
- [[_report/quant/research/2026-06-18-krx-current-universe-v0-ohlcv-batch-plan-fifteenth10|2026-06-18-krx-current-universe-v0-ohlcv-batch-plan-fifteenth10.md]], [[_report/quant/research/2026-06-18-krx-current-universe-v0-ohlcv-batch-plan-fifteenth10.requests.jsonl|2026-06-18-krx-current-universe-v0-ohlcv-batch-plan-fifteenth10.requests.jsonl]], [[_report/quant/research/2026-06-18-krx-current-universe-v0-ohlcv-capture-dry-run-fifteenth10|2026-06-18-krx-current-universe-v0-ohlcv-capture-dry-run-fifteenth10.md]], [[_report/quant/research/2026-06-18-krx-current-universe-v0-ohlcv-capture-result-fifteenth10|2026-06-18-krx-current-universe-v0-ohlcv-capture-result-fifteenth10.md]]
- [[_report/quant/research/2026-06-18-krx-current-universe-v0-ohlcv-batch-plan-sixteenth10|2026-06-18-krx-current-universe-v0-ohlcv-batch-plan-sixteenth10.md]], [[_report/quant/research/2026-06-18-krx-current-universe-v0-ohlcv-batch-plan-sixteenth10.requests.jsonl|2026-06-18-krx-current-universe-v0-ohlcv-batch-plan-sixteenth10.requests.jsonl]], [[_report/quant/research/2026-06-18-krx-current-universe-v0-ohlcv-capture-dry-run-sixteenth10|2026-06-18-krx-current-universe-v0-ohlcv-capture-dry-run-sixteenth10.md]], [[_report/quant/research/2026-06-18-krx-current-universe-v0-ohlcv-capture-result-sixteenth10|2026-06-18-krx-current-universe-v0-ohlcv-capture-result-sixteenth10.md]], [[_report/quant/research/2026-06-18-krx-current-universe-v0-ohlcv-capture-validator-result-sixteenth10|2026-06-18-krx-current-universe-v0-ohlcv-capture-validator-result-sixteenth10.md]]
- [[_report/quant/research/2026-06-18-krx-current-universe-v0-liquidity-smoke-expanded-sixteenth10|_report/quant/research/2026-06-18-krx-current-universe-v0-liquidity-smoke-expanded-sixteenth10.md]]
- [[_report/quant/research/2026-06-18-krx-current-universe-v0-liquidity-smoke-expanded-sixteenth10.rows.csv|_report/quant/research/2026-06-18-krx-current-universe-v0-liquidity-smoke-expanded-sixteenth10.rows.csv]]
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-seventeenth10|2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-seventeenth10.md]], [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-seventeenth10.requests.jsonl|2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-seventeenth10.requests.jsonl]], [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-dry-run-seventeenth10|2026-06-30-krx-current-universe-v0-ohlcv-capture-dry-run-seventeenth10.md]], [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-result-seventeenth10|2026-06-30-krx-current-universe-v0-ohlcv-capture-result-seventeenth10.md]]
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-eighteenth10|2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-eighteenth10.md]], [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-eighteenth10.requests.jsonl|2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-eighteenth10.requests.jsonl]], [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-dry-run-eighteenth10|2026-06-30-krx-current-universe-v0-ohlcv-capture-dry-run-eighteenth10.md]], [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-result-eighteenth10|2026-06-30-krx-current-universe-v0-ohlcv-capture-result-eighteenth10.md]]
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-nineteenth10|2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-nineteenth10.md]], [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-nineteenth10.requests.jsonl|2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-nineteenth10.requests.jsonl]], [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-dry-run-nineteenth10|2026-06-30-krx-current-universe-v0-ohlcv-capture-dry-run-nineteenth10.md]], [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-result-nineteenth10|2026-06-30-krx-current-universe-v0-ohlcv-capture-result-nineteenth10.md]], [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-validator-result-nineteenth10|2026-06-30-krx-current-universe-v0-ohlcv-capture-validator-result-nineteenth10.md]]
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-liquidity-smoke-expanded-nineteenth10|_report/quant/research/2026-06-30-krx-current-universe-v0-liquidity-smoke-expanded-nineteenth10.md]]
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-liquidity-smoke-expanded-nineteenth10.rows.csv|_report/quant/research/2026-06-30-krx-current-universe-v0-liquidity-smoke-expanded-nineteenth10.rows.csv]]
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentieth10|2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentieth10.md]], [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentieth10.requests.jsonl|2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentieth10.requests.jsonl]], [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-dry-run-twentieth10|2026-06-30-krx-current-universe-v0-ohlcv-capture-dry-run-twentieth10.md]], [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-result-twentieth10|2026-06-30-krx-current-universe-v0-ohlcv-capture-result-twentieth10.md]]
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyfirst10|2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyfirst10.md]], [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyfirst10.requests.jsonl|2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyfirst10.requests.jsonl]], [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-dry-run-twentyfirst10|2026-06-30-krx-current-universe-v0-ohlcv-capture-dry-run-twentyfirst10.md]], [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-result-twentyfirst10|2026-06-30-krx-current-universe-v0-ohlcv-capture-result-twentyfirst10.md]]
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentysecond10|2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentysecond10.md]], [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentysecond10.requests.jsonl|2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentysecond10.requests.jsonl]], [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-dry-run-twentysecond10|2026-06-30-krx-current-universe-v0-ohlcv-capture-dry-run-twentysecond10.md]], [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-result-twentysecond10|2026-06-30-krx-current-universe-v0-ohlcv-capture-result-twentysecond10.md]]
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentythird10|2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentythird10.md]], [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentythird10.requests.jsonl|2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentythird10.requests.jsonl]], [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-dry-run-twentythird10|2026-06-30-krx-current-universe-v0-ohlcv-capture-dry-run-twentythird10.md]], [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-result-twentythird10|2026-06-30-krx-current-universe-v0-ohlcv-capture-result-twentythird10.md]]
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyfourth10|2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyfourth10.md]], [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyfourth10.requests.jsonl|2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyfourth10.requests.jsonl]], [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-dry-run-twentyfourth10|2026-06-30-krx-current-universe-v0-ohlcv-capture-dry-run-twentyfourth10.md]], [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-result-twentyfourth10|2026-06-30-krx-current-universe-v0-ohlcv-capture-result-twentyfourth10.md]], [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-validator-result-twentyfourth10|2026-06-30-krx-current-universe-v0-ohlcv-capture-validator-result-twentyfourth10.md]]
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-liquidity-smoke-expanded-twentyfourth10|_report/quant/research/2026-06-30-krx-current-universe-v0-liquidity-smoke-expanded-twentyfourth10.md]]
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-liquidity-smoke-expanded-twentyfourth10.rows.csv|_report/quant/research/2026-06-30-krx-current-universe-v0-liquidity-smoke-expanded-twentyfourth10.rows.csv]]
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyfifth10|2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyfifth10.md]], [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyfifth10.requests.jsonl|2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyfifth10.requests.jsonl]], [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-dry-run-twentyfifth10|2026-06-30-krx-current-universe-v0-ohlcv-capture-dry-run-twentyfifth10.md]], [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-result-twentyfifth10|2026-06-30-krx-current-universe-v0-ohlcv-capture-result-twentyfifth10.md]]
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentysixth10|2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentysixth10.md]], [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentysixth10.requests.jsonl|2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentysixth10.requests.jsonl]], [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-dry-run-twentysixth10|2026-06-30-krx-current-universe-v0-ohlcv-capture-dry-run-twentysixth10.md]], [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-result-twentysixth10|2026-06-30-krx-current-universe-v0-ohlcv-capture-result-twentysixth10.md]]
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyseventh10|2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyseventh10.md]], [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyseventh10.requests.jsonl|2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyseventh10.requests.jsonl]], [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-dry-run-twentyseventh10|2026-06-30-krx-current-universe-v0-ohlcv-capture-dry-run-twentyseventh10.md]], [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-result-twentyseventh10|2026-06-30-krx-current-universe-v0-ohlcv-capture-result-twentyseventh10.md]]
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyeighth10|2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyeighth10.md]], [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyeighth10.requests.jsonl|2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyeighth10.requests.jsonl]], [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-dry-run-twentyeighth10|2026-06-30-krx-current-universe-v0-ohlcv-capture-dry-run-twentyeighth10.md]], [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-result-twentyeighth10|2026-06-30-krx-current-universe-v0-ohlcv-capture-result-twentyeighth10.md]]
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyninth10|2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyninth10.md]], [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyninth10.requests.jsonl|2026-06-30-krx-current-universe-v0-ohlcv-batch-plan-twentyninth10.requests.jsonl]], [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-dry-run-twentyninth10|2026-06-30-krx-current-universe-v0-ohlcv-capture-dry-run-twentyninth10.md]], [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-result-twentyninth10|2026-06-30-krx-current-universe-v0-ohlcv-capture-result-twentyninth10.md]], [[_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-capture-validator-result-twentyninth10|2026-06-30-krx-current-universe-v0-ohlcv-capture-validator-result-twentyninth10.md]]
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-liquidity-smoke-expanded-twentyninth10|_report/quant/research/2026-06-30-krx-current-universe-v0-liquidity-smoke-expanded-twentyninth10.md]]
- [[_report/quant/research/2026-06-30-krx-current-universe-v0-liquidity-smoke-expanded-twentyninth10.rows.csv|_report/quant/research/2026-06-30-krx-current-universe-v0-liquidity-smoke-expanded-twentyninth10.rows.csv]]
- [[_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtieth10|2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtieth10.md]], [[_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtieth10.requests.jsonl|2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtieth10.requests.jsonl]], [[_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-capture-dry-run-thirtieth10|2026-07-01-krx-current-universe-v0-ohlcv-capture-dry-run-thirtieth10.md]], [[_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-capture-result-thirtieth10|2026-07-01-krx-current-universe-v0-ohlcv-capture-result-thirtieth10.md]], [[_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-capture-validator-result-thirtieth10|2026-07-01-krx-current-universe-v0-ohlcv-capture-validator-result-thirtieth10.md]]
- [[_report/quant/research/2026-07-01-krx-current-universe-v0-liquidity-smoke-expanded-thirtieth10|_report/quant/research/2026-07-01-krx-current-universe-v0-liquidity-smoke-expanded-thirtieth10.md]]
- [[_report/quant/research/2026-07-01-krx-current-universe-v0-liquidity-smoke-expanded-thirtieth10.rows.csv|_report/quant/research/2026-07-01-krx-current-universe-v0-liquidity-smoke-expanded-thirtieth10.rows.csv]]
- [[_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtyfirst10|2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtyfirst10.md]], [[_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtyfirst10.requests.jsonl|2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtyfirst10.requests.jsonl]], [[_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-capture-dry-run-thirtyfirst10|2026-07-01-krx-current-universe-v0-ohlcv-capture-dry-run-thirtyfirst10.md]], [[_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-capture-result-thirtyfirst10|2026-07-01-krx-current-universe-v0-ohlcv-capture-result-thirtyfirst10.md]]
- [[_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtysecond10|2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtysecond10.md]], [[_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtysecond10.requests.jsonl|2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtysecond10.requests.jsonl]], [[_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-capture-dry-run-thirtysecond10|2026-07-01-krx-current-universe-v0-ohlcv-capture-dry-run-thirtysecond10.md]], [[_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-capture-result-thirtysecond10|2026-07-01-krx-current-universe-v0-ohlcv-capture-result-thirtysecond10.md]]
- [[_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtythird10|2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtythird10.md]], [[_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtythird10.requests.jsonl|2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtythird10.requests.jsonl]], [[_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-capture-dry-run-thirtythird10|2026-07-01-krx-current-universe-v0-ohlcv-capture-dry-run-thirtythird10.md]], [[_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-capture-result-thirtythird10|2026-07-01-krx-current-universe-v0-ohlcv-capture-result-thirtythird10.md]]
- [[_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtyfourth10|2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtyfourth10.md]], [[_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtyfourth10.requests.jsonl|2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtyfourth10.requests.jsonl]], [[_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-capture-dry-run-thirtyfourth10|2026-07-01-krx-current-universe-v0-ohlcv-capture-dry-run-thirtyfourth10.md]], [[_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-capture-result-thirtyfourth10|2026-07-01-krx-current-universe-v0-ohlcv-capture-result-thirtyfourth10.md]]
- [[_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtyfifth10|2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtyfifth10.md]], [[_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtyfifth10.requests.jsonl|2026-07-01-krx-current-universe-v0-ohlcv-batch-plan-thirtyfifth10.requests.jsonl]], [[_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-capture-dry-run-thirtyfifth10|2026-07-01-krx-current-universe-v0-ohlcv-capture-dry-run-thirtyfifth10.md]], [[_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-capture-result-thirtyfifth10|2026-07-01-krx-current-universe-v0-ohlcv-capture-result-thirtyfifth10.md]], [[_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-capture-validator-result-thirtyfifth10|2026-07-01-krx-current-universe-v0-ohlcv-capture-validator-result-thirtyfifth10.md]]
- [[_report/quant/research/2026-07-01-krx-current-universe-v0-liquidity-smoke-expanded-thirtyfifth10|_report/quant/research/2026-07-01-krx-current-universe-v0-liquidity-smoke-expanded-thirtyfifth10.md]]
- [[_report/quant/research/2026-07-01-krx-current-universe-v0-liquidity-smoke-expanded-thirtyfifth10.rows.csv|_report/quant/research/2026-07-01-krx-current-universe-v0-liquidity-smoke-expanded-thirtyfifth10.rows.csv]]
- [[_report/quant/research/2026-07-01-user-action-items-temp|_report/quant/research/2026-07-01-user-action-items-temp.md]]
- [[_report/quant/research/2026-06-14-krx-managed-issues-current-exclusions|_report/quant/research/2026-06-14-krx-managed-issues-current-exclusions.md]]

## Build Script

Use:

```powershell
uv run python scripts\quant_krx_current_universe_build.py `
  --listed-raw _report\raw\2026\2026-06-13\krx\universe\listed_issues_current.raw.csv `
  --managed-raw _report\raw\2026\2026-06-13\krx\universe\managed_issues_current.raw.csv `
  --as-of-date 2026-06-13 `
  --output _report\quant\research\2026-06-14-krx-current-universe-v0.md `
  --csv-output _report\quant\research\2026-06-14-krx-current-universe-v0.rows.csv
```

Universe-based OHLCV batch plan dry-run:

```powershell
uv run python scripts\quant_kis_ohlcv_batch_plan.py `
  --universe-csv _report\quant\research\2026-06-14-krx-current-universe-v0.rows.csv `
  --raw-dir _report\raw\2026\2026-06-15\quant\universe-ohlcv `
  --as-of-date 2026-06-15 `
  --start-date 20260301 `
  --end-date 20260615 `
  --limit 10 `
  --skip-existing `
  --output _report\quant\research\2026-06-15-krx-current-universe-v0-ohlcv-batch-plan.md `
  --jsonl-output _report\quant\research\2026-06-15-krx-current-universe-v0-ohlcv-batch-plan.requests.jsonl
```

Universe-based OHLCV queue capture dry-run:

```powershell
uv run python scripts\quant_kis_ohlcv_capture.py `
  --queue _report\quant\research\2026-06-15-krx-current-universe-v0-ohlcv-batch-plan.requests.jsonl `
  --raw-dir _report\raw\2026\2026-06-15\quant\universe-ohlcv `
  --dry-run `
  --limit 10 `
  --output _report\quant\research\2026-06-15-krx-current-universe-v0-ohlcv-capture-dry-run.md
```

First read-only KIS capture subset:

```powershell
uv run python scripts\quant_kis_ohlcv_capture.py `
  --queue _report\quant\research\2026-06-15-krx-current-universe-v0-ohlcv-batch-plan.requests.jsonl `
  --raw-dir _report\raw\2026\2026-06-15\quant\universe-ohlcv `
  --limit 10 `
  --skip-existing `
  --stop-on-error `
  --output _report\quant\research\2026-06-15-krx-current-universe-v0-ohlcv-capture-result.md
```

Second read-only KIS capture subset:

```powershell
uv run python scripts\quant_kis_ohlcv_batch_plan.py `
  --universe-csv _report\quant\research\2026-06-14-krx-current-universe-v0.rows.csv `
  --raw-dir _report\raw\2026\2026-06-15\quant\universe-ohlcv `
  --as-of-date 2026-06-15 `
  --start-date 20260301 `
  --end-date 20260615 `
  --limit 10 `
  --skip-existing `
  --output _report\quant\research\2026-06-15-krx-current-universe-v0-ohlcv-batch-plan-next10.md `
  --jsonl-output _report\quant\research\2026-06-15-krx-current-universe-v0-ohlcv-batch-plan-next10.requests.jsonl

uv run python scripts\quant_kis_ohlcv_capture.py `
  --queue _report\quant\research\2026-06-15-krx-current-universe-v0-ohlcv-batch-plan-next10.requests.jsonl `
  --raw-dir _report\raw\2026\2026-06-15\quant\universe-ohlcv `
  --limit 10 `
  --skip-existing `
  --stop-on-error `
  --output _report\quant\research\2026-06-15-krx-current-universe-v0-ohlcv-capture-result-next10.md
```

Third read-only KIS capture subset:

```powershell
uv run python scripts\quant_kis_ohlcv_batch_plan.py `
  --universe-csv _report\quant\research\2026-06-14-krx-current-universe-v0.rows.csv `
  --raw-dir _report\raw\2026\2026-06-15\quant\universe-ohlcv `
  --as-of-date 2026-06-15 `
  --start-date 20260301 `
  --end-date 20260615 `
  --limit 10 `
  --skip-existing `
  --output _report\quant\research\2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-third10.md `
  --jsonl-output _report\quant\research\2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-third10.requests.jsonl

uv run python scripts\quant_kis_ohlcv_capture.py `
  --queue _report\quant\research\2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-third10.requests.jsonl `
  --raw-dir _report\raw\2026\2026-06-15\quant\universe-ohlcv `
  --limit 10 `
  --skip-existing `
  --stop-on-error `
  --output _report\quant\research\2026-06-17-krx-current-universe-v0-ohlcv-capture-result-third10.md
```

Fourth read-only KIS capture subset:

```powershell
uv run python scripts\quant_kis_ohlcv_batch_plan.py `
  --universe-csv _report\quant\research\2026-06-14-krx-current-universe-v0.rows.csv `
  --raw-dir _report\raw\2026\2026-06-15\quant\universe-ohlcv `
  --as-of-date 2026-06-15 `
  --start-date 20260301 `
  --end-date 20260615 `
  --limit 10 `
  --skip-existing `
  --output _report\quant\research\2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-fourth10.md `
  --jsonl-output _report\quant\research\2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-fourth10.requests.jsonl

uv run python scripts\quant_kis_ohlcv_capture.py `
  --queue _report\quant\research\2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-fourth10.requests.jsonl `
  --raw-dir _report\raw\2026\2026-06-15\quant\universe-ohlcv `
  --limit 10 `
  --skip-existing `
  --stop-on-error `
  --output _report\quant\research\2026-06-17-krx-current-universe-v0-ohlcv-capture-result-fourth10.md
```

Saved-raw Liquidity Filter smoke:

```powershell
uv run python scripts\quant_liquidity_filter.py `
  --universe-csv _report\quant\research\2026-06-14-krx-current-universe-v0.rows.csv `
  --raw-dir _report\raw\2026\2026-06-13\quant\paper-follow-up `
  --as-of-date 2026-06-13 `
  --output _report\quant\research\2026-06-14-krx-current-universe-v0-liquidity-smoke.md `
  --csv-output _report\quant\research\2026-06-14-krx-current-universe-v0-liquidity-smoke.rows.csv
```

Expanded saved-raw Liquidity Filter smoke:

```powershell
uv run python scripts\quant_liquidity_filter.py `
  --universe-csv _report\quant\research\2026-06-14-krx-current-universe-v0.rows.csv `
  --raw-dir _report\raw\2026\2026-06-13\quant\paper-follow-up `
  --raw-dir _report\raw\2026\2026-06-15\quant\universe-ohlcv `
  --as-of-date 2026-06-15 `
  --output _report\quant\research\2026-06-15-krx-current-universe-v0-liquidity-smoke-expanded.md `
  --csv-output _report\quant\research\2026-06-15-krx-current-universe-v0-liquidity-smoke-expanded.rows.csv
```

## Current Filters

- Include KOSPI/KOSDAQ listed issues.
- Exclude non-common-stock-like instruments by type/name.
- Exclude current managed issues.
- Exclude rows with fewer than `365 calendar days` since listing date.
- Apply saved-raw Liquidity Filter smoke where KIS daily OHLCV raw exists.

## Current Counts

- Total listed rows: `2875`
- Included rows: `2390`
- Excluded rows: `485`

Known exclusion reason counts:

- `market_not_allowed`: `107`
- `listing_age_calendar_insufficient`: `102`
- `instrument_type_excluded`: `101`
- `managed_issue_current`: `101`
- `instrument_name_excluded`: `97`
- `preferred_share_name`: `15`

Expanded Liquidity smoke counts:

- Rows with raw OHLCV evaluated: `351`
- Included after saved-raw Liquidity Filter: `174`
- Failed below threshold: `177`
- `liquidity_raw_missing`: `2039`
- Latest authoritative row set: [[_report/quant/research/2026-07-01-krx-current-universe-v0-liquidity-smoke-expanded-thirtyfifth10.rows.csv|_report/quant/research/2026-07-01-krx-current-universe-v0-liquidity-smoke-expanded-thirtyfifth10.rows.csv]]

OHLCV batch plan dry-run counts:

- Base included rows: `2390`
- Selected requests: `10`
- First request rows: `000020 동화약품`, `000040 KR모터스`, `000050 경방`

First OHLCV capture counts:

- Dry-run validated rows: `10`
- Live capture status counts: `saved` 9, `skipped_existing` 1
- Raw directory: `_report/raw/2026/2026-06-15/quant/universe-ohlcv/`
- Validator result after second capture: 20 raw files parsed, each with 71 daily rows and latest date `20260615`

Second OHLCV capture counts:

- Existing raw skipped by batch plan: `10`
- Selected requests: `10`
- Live capture status counts: `saved` 10
- First request rows: `000210 DL`, `000220 유유제약`, `000230 일동홀딩스`

Third OHLCV capture counts:

- Existing raw skipped by batch plan: `20`
- Selected requests: `10`
- Live capture status counts: `saved` 10
- First request rows: `000400 롯데손해보험`, `000430 대원강업`, `000440 중앙에너비스`
- Validator result after third capture: 30 raw files parsed, each with 71 daily rows and latest date `20260615`

Fourth OHLCV capture counts:

- Existing raw skipped by batch plan: `30`
- Selected requests: `10`
- Live capture status counts: `saved` 10
- First request rows: `000650 천일고속`, `000660 SK하이닉스`, `000670 영풍`
- Validator result after fourth capture: 40 raw files parsed, each with 71 daily rows and latest date `20260615`

Fifth through seventh OHLCV capture counts:

- Existing raw skipped by batch plan: `40`, `50`, and `60`
- Selected requests: `10` each
- Live capture status counts: `saved` 10 each
- Fifth first request rows: `000880 한화`, `000890 보해양조`, `000910 유니온`
- Sixth first request rows: `001070 대한방직`, `001080 만호제강`, `001120 LX인터내셔널`
- Seventh first request rows: `001290 상상인증권`, `001340 PKC`, `001360 삼성제약`
- Validator result after seventh capture: 70 raw files parsed, each with 71 daily rows and latest date `20260615`

Eighth through tenth OHLCV capture counts:

- Existing raw skipped by batch plan: `70`, `80`, and `90`
- Selected requests: `10` each
- Live capture status counts: `saved` 10 each
- Eighth first request rows: `001500 현대차증권`, `001510 SK증권`, `001520 동양`
- Ninth first request rows: `001720 신영증권`, `001740 SK네트웍스`, `001750 한양증권`
- Tenth first request rows: `002020 코오롱`, `002030 아세아`, `002070 비비안`
- Validator result after tenth capture: 100 raw files parsed, each with 71 daily rows and latest date `20260615`

Eleventh through thirteenth OHLCV capture counts:

- Existing raw skipped by batch plan: `100`, `110`, and `120`
- Selected requests: `10` each
- Live capture status counts: `saved` 10 each
- Eleventh first request rows: `002230 피에스텍`, `002240 고려제강`, `002290 삼일기업공사`
- Twelfth first request rows: `002450 삼익악기`, `002460 HS화성`, `002600 조흥`
- Thirteenth first request rows: `002760 보락`, `002780 진흥기업`, `002790 아모레퍼시픽홀딩스`
- Validator result after thirteenth capture: 130 raw files parsed, each with 71 daily rows and latest date `20260615`

Fourteenth through sixteenth OHLCV capture counts:

- Existing raw skipped by batch plan: `130`, `140`, and `150`
- Selected requests: `10` each
- Live capture status counts: `saved` 10 each
- Fourteenth first request rows: `002920 유성기업`, `002960 한국쉘석유`, `002990 금호건설`
- Fifteenth first request rows: `003100 선광`, `003120 일성아이에스`, `003160 디아이`
- Sixteenth first request rows: `003350 한국화장품제조`, `003380 하림지주`, `003460 유화증권`
- Validator result after sixteenth capture: 160 raw files parsed, each with 71 daily rows and latest date `20260615`

Seventeenth through nineteenth OHLCV capture counts:

- Existing raw skipped by batch plan: `160`, `170`, and `180`
- Selected requests: `10` each
- Live capture status counts: `saved` 10 each
- Seventeenth first request rows: `003570 SNT다이내믹스`, `003580 HLB글로벌`, `003610 방림`
- Eighteenth first request rows: `003800 에이스침대`, `003830 대한화섬`, `003850 보령`
- Nineteenth first request rows: `004100 태양금속`, `004140 동방`, `004150 한솔홀딩스`
- Validator result after nineteenth capture: 190 raw files parsed, each with 71 daily rows and latest date `20260615`

Twentieth through twentyfourth OHLCV capture counts:

- Existing raw skipped by batch plan: `190`, `200`, `210`, `220`, and `230`
- Selected requests: `10` each
- Live capture status counts: `saved` 10 each
- Twentieth first request rows: `004410 서울식품`, `004430 송원산업`, `004440 삼일씨엔에스`
- Twentyfirst first request rows: `004700 조광피혁`, `004710 한솔테크닉스`, `004720 팜젠사이언스`
- Twentysecond first request rows: `004910 조광페인트`, `004920 씨아이테크`, `004960 한신공영`
- Twentythird first request rows: `005180 빙그레`, `005250 녹십자홀딩스`, `005290 동진쎄미켐`
- Twentyfourth first request rows: `005490 POSCO홀딩스`, `005500 삼진제약`, `005610 삼립`
- Validator result after twentyfourth capture: 240 raw files parsed, each with 71 daily rows and latest date `20260615`

Twentyfifth through twentyninth OHLCV capture counts:

- Existing raw skipped by batch plan: `240`, `250`, `260`, `270`, and `280`
- Selected requests: `10` each
- Live capture status counts: `saved` 10 each
- Twentyfifth first request rows: `005800 신영와코루`, `005810 풍산홀딩스`, `005820 원림`
- Twentysixth first request rows: `005950 이수화학`, `005960 동부건설`, `005990 매일홀딩스`
- Twentyseventh first request rows: `006200 한국전자홀딩스`, `006220 제주은행`, `006260 LS`
- Twentyeighth first request rows: `006620 동구바이오제약`, `006650 대한유화`, `006660 삼성공조`
- Twentyninth first request rows: `006920 모헨즈`, `006980 우성`, `007070 GS리테일`
- Validator result after twentyninth capture: 290 raw files parsed, each with 71 daily rows and latest date `20260615`

Thirtieth OHLCV capture counts:

- Existing raw skipped by batch plan: `290`
- Selected requests: `10`
- Live capture status counts: `saved` 10
- Thirtieth first request rows: `007340 DN오토모티브`, `007370 진양제약`, `007390 네이처셀`
- Validator result after thirtieth capture: 300 raw files parsed, each with 71 daily rows and latest date `20260615`

Thirtyfirst through thirtyfifth OHLCV capture counts:

- Existing raw skipped by batch plan: `300`, `310`, `320`, `330`, and `340`
- Selected requests: `10` each
- Live capture status counts: `saved` 10 each
- Thirtyfifth first request rows: `009420 서울바이오시스`, `009450 경동나비엔`, `009460 한창제지`
- Validator result after thirtyfifth capture: 350 raw files parsed, each with 71 daily rows and latest date `20260615`

## Code Handling Rule

KRX short codes may be alphanumeric. Preserve values exactly after basic normalization.

Examples:

- `005930` is normal numeric.
- `0004V0` is valid alphanumeric and must not become `000040`.

## Guardrails

- This is a `current_snapshot` artifact for paper/smoke validation.
- It is not a historical `Point-in-Time Universe`.
- Full-Universe `Liquidity Filter`, trading suspension, market alert, delisting history, and exact trading-day Listing Age are not solved here.
- `liquidity_raw_missing` means saved raw coverage is missing; it is not an illiquidity conclusion.
- The OHLCV batch plan does not call KIS. Direct capture used local API detail fallback because the current Codex App surface did not expose `domestic_stock.find_api_detail`; use the MCP preflight when available.
