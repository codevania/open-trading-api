# Paper Signal Log

## Metadata

- Date: 2026-06-09
- Author: Codex
- Source result: `_report/quant/research/2026-06-09-data-pipeline-smoke-test-result.md`
- Source raw: `_report/raw/2026/2026-06-09/quant/smoke-test/`
- Universe mode: `manual_smoke_test`
- Bias Control: `hold`
- Interpretation: `paper tracking only`, `not trade instruction`

## Signals

| Strategy | Symbol | Signal Date | Candidate State | Evidence | Data Source | Follow-Up Window | Invalidator | Action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `001-strategy-universe-momentum` | `000660 SK hynix` | 20260605 | BUY candidate | 20D ROC `29.2942%`, latest close `2070000`, avg trading value `12079720307940` KRW | `_report/raw/2026/2026-06-09/quant/smoke-test/000660.daily.raw.json` | next 1D, 5D, 20D paper observation | data anomaly, ROC reversal, Point-in-Time failure | paper tracking only |
| `001-strategy-universe-momentum` | `005930 Samsung Electronics` | 20260605 | BUY candidate | 20D ROC `23.6842%`, latest close `329000`, avg trading value `10431533672673` KRW | `_report/raw/2026/2026-06-09/quant/smoke-test/005930.daily.raw.json` | next 1D, 5D, 20D paper observation | data anomaly, ROC reversal, Point-in-Time failure | paper tracking only |
| `001-strategy-universe-momentum` | `035420 NAVER` | 20260605 | BUY candidate | 20D ROC `22.8365%`, latest close `255500`, avg trading value `657256761422` KRW | `_report/raw/2026/2026-06-09/quant/smoke-test/035420.daily.raw.json` | next 1D, 5D, 20D paper observation | data anomaly, ROC reversal, Point-in-Time failure | paper tracking only |

## Data Quality

- raw source: KIS MCP `domestic_stock.inquire_daily_itemchartprice`
- preflight: `domestic_stock.find_api_detail`
- rows: 21 per symbol
- missing fields: none detected by `scripts/quant_smoke_validate.py`
- duplicated dates: none detected by validator path
- Point-in-Time Universe status: pending

## Follow-Up Plan

- Next 1D check: compare next available close after 2026-06-05 against signal close.
- Next 5D check: record direction and whether ROC state persists.
- Next 20D check: record paper observation only, not Strategy performance.

## Notes

- Manual symbols are not a Quant Universe.
- Candidate states are not investment advice.
- Full Backtest interpretation remains blocked until Point-in-Time Universe, OOS, and Bias Control pass.
