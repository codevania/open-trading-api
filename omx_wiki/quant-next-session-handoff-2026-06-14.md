# Quant Next Session Handoff - 2026-06-14

## Start Here

If a new Codex session starts, read these files first:

1. `omx_wiki/quant-implementation-status-2026-06-14.md`
2. `omx_wiki/quant-krx-current-universe-v0.md`
3. `_report/quant/implementation-roadmap.md`
4. `_report/quant/research/2026-06-14-krx-current-universe-v0.md`
5. `_report/quant/universe.md`

## First Commands

```powershell
git status --short
uv run python -m unittest discover tests
```

If thirtyfifth-capture local changes are still present, stage/commit them before expanding OHLCV coverage again.

Suggested commit intent:

`Capture thirtyfifth KIS OHLCV universe batch`

Use Lore commit protocol.

## Current Best Next Task

Continue generated Universe OHLCV coverage after the first 350 captured rows.

Already implemented in the latest local work:

- `scripts/quant_liquidity_filter.py`
- `tests/test_quant_liquidity_filter.py`
- `scripts/quant_kis_ohlcv_batch_plan.py`
- `tests/test_quant_kis_ohlcv_batch_plan.py`
- `scripts/quant_kis_ohlcv_capture.py`
- `tests/test_quant_kis_ohlcv_capture.py`
- `_report/quant/research/2026-06-14-krx-current-universe-v0-liquidity-smoke.md`
- `_report/quant/research/2026-06-14-krx-current-universe-v0-liquidity-smoke.rows.csv`
- `_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-batch-plan.md`
- `_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-batch-plan.requests.jsonl`
- `_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-batch-plan-next10.md`
- `_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-batch-plan-next10.requests.jsonl`
- `_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-capture-dry-run.md`
- `_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-capture-result.md`
- `_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-capture-dry-run-next10.md`
- `_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-capture-result-next10.md`
- `_report/quant/research/2026-06-15-krx-current-universe-v0-ohlcv-capture-validator-result.md`
- `_report/quant/research/2026-06-15-krx-current-universe-v0-liquidity-smoke-expanded.md`
- `_report/quant/research/2026-06-15-krx-current-universe-v0-liquidity-smoke-expanded.rows.csv`
- `_report/quant/research/2026-06-16-quant-pipeline-gap-prep-list.md`
- `_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-third10.md`
- `_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-third10.requests.jsonl`
- `_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-dry-run-third10.md`
- `_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-result-third10.md`
- `_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-validator-result-third10.md`
- `_report/quant/research/2026-06-17-krx-current-universe-v0-liquidity-smoke-expanded-third10.md`
- `_report/quant/research/2026-06-17-krx-current-universe-v0-liquidity-smoke-expanded-third10.rows.csv`
- `_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-fourth10.md`
- `_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-batch-plan-fourth10.requests.jsonl`
- `_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-dry-run-fourth10.md`
- `_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-result-fourth10.md`
- `_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-capture-validator-result-fourth10.md`
- `_report/quant/research/2026-06-17-krx-current-universe-v0-liquidity-smoke-expanded-fourth10.md`
- `_report/quant/research/2026-06-17-krx-current-universe-v0-liquidity-smoke-expanded-fourth10.rows.csv`
- `_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-*-fifth10*`
- `_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-*-sixth10*`
- `_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-*-seventh10*`
- `_report/quant/research/2026-06-17-krx-current-universe-v0-liquidity-smoke-expanded-seventh10.md`
- `_report/quant/research/2026-06-17-krx-current-universe-v0-liquidity-smoke-expanded-seventh10.rows.csv`
- `_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-*-eighth10*`
- `_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-*-ninth10*`
- `_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-*-tenth10*`
- `_report/quant/research/2026-06-17-krx-current-universe-v0-liquidity-smoke-expanded-tenth10.md`
- `_report/quant/research/2026-06-17-krx-current-universe-v0-liquidity-smoke-expanded-tenth10.rows.csv`
- `_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-*-eleventh10*`
- `_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-*-twelfth10*`
- `_report/quant/research/2026-06-17-krx-current-universe-v0-ohlcv-*-thirteenth10*`
- `_report/quant/research/2026-06-17-krx-current-universe-v0-liquidity-smoke-expanded-thirteenth10.md`
- `_report/quant/research/2026-06-17-krx-current-universe-v0-liquidity-smoke-expanded-thirteenth10.rows.csv`
- `_report/quant/research/2026-06-18-krx-current-universe-v0-ohlcv-*-fourteenth10*`
- `_report/quant/research/2026-06-18-krx-current-universe-v0-ohlcv-*-fifteenth10*`
- `_report/quant/research/2026-06-18-krx-current-universe-v0-ohlcv-*-sixteenth10*`
- `_report/quant/research/2026-06-18-krx-current-universe-v0-liquidity-smoke-expanded-sixteenth10.md`
- `_report/quant/research/2026-06-18-krx-current-universe-v0-liquidity-smoke-expanded-sixteenth10.rows.csv`
- `_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-*-seventeenth10*`
- `_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-*-eighteenth10*`
- `_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-*-nineteenth10*`
- `_report/quant/research/2026-06-30-krx-current-universe-v0-liquidity-smoke-expanded-nineteenth10.md`
- `_report/quant/research/2026-06-30-krx-current-universe-v0-liquidity-smoke-expanded-nineteenth10.rows.csv`
- `_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-*-twentieth10*`
- `_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-*-twentyfirst10*`
- `_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-*-twentysecond10*`
- `_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-*-twentythird10*`
- `_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-*-twentyfourth10*`
- `_report/quant/research/2026-06-30-krx-current-universe-v0-liquidity-smoke-expanded-twentyfourth10.md`
- `_report/quant/research/2026-06-30-krx-current-universe-v0-liquidity-smoke-expanded-twentyfourth10.rows.csv`
- `_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-*-twentyfifth10*`
- `_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-*-twentysixth10*`
- `_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-*-twentyseventh10*`
- `_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-*-twentyeighth10*`
- `_report/quant/research/2026-06-30-krx-current-universe-v0-ohlcv-*-twentyninth10*`
- `_report/quant/research/2026-06-30-krx-current-universe-v0-liquidity-smoke-expanded-twentyninth10.md`
- `_report/quant/research/2026-06-30-krx-current-universe-v0-liquidity-smoke-expanded-twentyninth10.rows.csv`
- `_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-*-thirtieth10*`
- `_report/quant/research/2026-07-01-krx-current-universe-v0-liquidity-smoke-expanded-thirtieth10.md`
- `_report/quant/research/2026-07-01-krx-current-universe-v0-liquidity-smoke-expanded-thirtieth10.rows.csv`
- `_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-*-thirtyfirst10*`
- `_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-*-thirtysecond10*`
- `_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-*-thirtythird10*`
- `_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-*-thirtyfourth10*`
- `_report/quant/research/2026-07-01-krx-current-universe-v0-ohlcv-*-thirtyfifth10*`
- `_report/quant/research/2026-07-01-krx-current-universe-v0-liquidity-smoke-expanded-thirtyfifth10.md`
- `_report/quant/research/2026-07-01-krx-current-universe-v0-liquidity-smoke-expanded-thirtyfifth10.rows.csv`
- `_report/quant/research/2026-07-01-user-action-items-temp.md`
- Target rule: `avg_trading_value_20d_krw >= 1,000,000,000`
- Saved raw coverage currently evaluates 351 unique rows. `174` pass and `177` fail the threshold.
- `2039` base-included rows are `liquidity_raw_missing`, which means raw coverage is missing, not that those stocks are illiquid.
- First OHLCV batch dry-run selected `10` requests from generated Universe `include` rows.
- First OHLCV direct capture saved 10 raw files under `_report/raw/2026/2026-06-15/quant/universe-ohlcv/`.
- Second OHLCV batch dry-run selected the next `10` requests after skipping existing raw.
- Second OHLCV direct capture saved 10 more raw files under `_report/raw/2026/2026-06-15/quant/universe-ohlcv/`.
- Third OHLCV batch dry-run selected the next `10` requests after skipping `20` existing raw files.
- Third OHLCV direct capture saved 10 more raw files under `_report/raw/2026/2026-06-15/quant/universe-ohlcv/`; the directory now has `30` Universe raw files.
- Fourth OHLCV batch dry-run selected the next `10` requests after skipping `30` existing raw files.
- Fourth OHLCV direct capture saved 10 more raw files under `_report/raw/2026/2026-06-15/quant/universe-ohlcv/`; the directory then had `40` Universe raw files. `000660 SK하이닉스` overlaps with an older paper-follow-up raw row, so the then-current Liquidity Filter had `42` unique evaluated rows, not `43`.
- Fifth, sixth, and seventh OHLCV batch dry-runs selected three additional `10` request queues after skipping `40`, `50`, and `60` existing raw files.
- Fifth, sixth, and seventh direct captures saved `30` more raw files under `_report/raw/2026/2026-06-15/quant/universe-ohlcv/`; the directory then had `70` Universe raw files. Because `000660 SK하이닉스` overlaps with an older paper-follow-up raw row, the then-current Liquidity Filter had `72` unique evaluated rows, not `73`.
- Eighth, ninth, and tenth OHLCV batch dry-runs selected three additional `10` request queues after skipping `70`, `80`, and `90` existing raw files.
- Eighth, ninth, and tenth direct captures saved `30` more raw files under `_report/raw/2026/2026-06-15/quant/universe-ohlcv/`; the directory then had `100` Universe raw files. Because `000660 SK하이닉스` overlaps with an older paper-follow-up raw row, the then-current Liquidity Filter had `102` unique evaluated rows, not `103`.
- Eleventh, twelfth, and thirteenth OHLCV batch dry-runs selected three additional `10` request queues after skipping `100`, `110`, and `120` existing raw files.
- Eleventh, twelfth, and thirteenth direct captures saved `30` more raw files under `_report/raw/2026/2026-06-15/quant/universe-ohlcv/`; the directory then had `130` Universe raw files. Because `000660 SK하이닉스` overlaps with an older paper-follow-up raw row, the then-current Liquidity Filter had `132` unique evaluated rows, not `133`.
- Fourteenth, fifteenth, and sixteenth OHLCV batch dry-runs selected three additional `10` request queues after skipping `130`, `140`, and `150` existing raw files.
- Fourteenth, fifteenth, and sixteenth direct captures saved `30` more raw files under `_report/raw/2026/2026-06-15/quant/universe-ohlcv/`; the directory then had `160` Universe raw files. Because `000660 SK하이닉스` overlaps with an older paper-follow-up raw row, the then-current Liquidity Filter had `162` unique evaluated rows, not `163`.
- Seventeenth, eighteenth, and nineteenth OHLCV batch dry-runs selected three additional `10` request queues after skipping `160`, `170`, and `180` existing raw files.
- Seventeenth, eighteenth, and nineteenth direct captures saved `30` more raw files under `_report/raw/2026/2026-06-15/quant/universe-ohlcv/`; the directory then had `190` Universe raw files. Because `000660 SK하이닉스` overlaps with an older paper-follow-up raw row, the then-current Liquidity Filter had `192` unique evaluated rows, not `193`.
- Twentieth through twentyfourth OHLCV batch dry-runs selected five additional `10` request queues after skipping `190`, `200`, `210`, `220`, and `230` existing raw files.
- Twentieth through twentyfourth direct captures saved `50` more raw files under `_report/raw/2026/2026-06-15/quant/universe-ohlcv/`; the directory then had `240` Universe raw files. Because `000660 SK하이닉스` overlaps with an older paper-follow-up raw row, the then-current Liquidity Filter had `242` unique evaluated rows, not `243`.
- Twentyfifth through twentyninth OHLCV batch dry-runs selected five additional `10` request queues after skipping `240`, `250`, `260`, `270`, and `280` existing raw files.
- Twentyfifth through twentyninth direct captures saved `50` more raw files under `_report/raw/2026/2026-06-15/quant/universe-ohlcv/`; the directory then had `290` Universe raw files. Because `000660 SK하이닉스` and `005930 삼성전자` overlap with older paper-follow-up raw rows while `035420 NAVER` remains extra, the then-current Liquidity Filter had `291` unique evaluated rows.
- Thirtieth OHLCV batch dry-run selected one additional `10` request queue after skipping `290` existing raw files.
- Thirtieth direct capture saved `10` more raw files under `_report/raw/2026/2026-06-15/quant/universe-ohlcv/`; the directory then had `300` Universe raw files. Because `000660 SK하이닉스` and `005930 삼성전자` overlap with older paper-follow-up raw rows while `035420 NAVER` remains extra, the then-current Liquidity Filter had `301` unique evaluated rows.
- Thirtyfirst through thirtyfifth OHLCV batch dry-runs selected five additional `10` request queues after skipping `300`, `310`, `320`, `330`, and `340` existing raw files.
- Thirtyfirst through thirtyfifth direct captures saved `50` more raw files under `_report/raw/2026/2026-06-15/quant/universe-ohlcv/`; the directory now has `350` Universe raw files. Because `000660 SK하이닉스` and `005930 삼성전자` overlap with older paper-follow-up raw rows while `035420 NAVER` remains extra, the latest Liquidity Filter has `351` unique evaluated rows.
- Current Codex App surface did not expose the KIS MCP tool, so `find_api_detail` was not callable here. Local `MCP/Kis Trading MCP/configs/domestic_stock.json` and `examples_llm` sample docs were used as the fallback API detail evidence, and only the read-only quotation endpoint was called.

Likely needed work:

1. Preflight KIS daily OHLCV API with `domestic_stock.find_api_detail` in a surface where the MCP tool is available.
2. Generate the next small request queue with `scripts/quant_kis_ohlcv_batch_plan.py --skip-existing --limit 10` against `_report/raw/2026/2026-06-15/quant/universe-ohlcv/`; after the thirtyfifth capture this should skip `350` existing raw files.
3. Execute the next queue with `scripts/quant_kis_ohlcv_capture.py`.
4. Save raw KIS responses under `_report/raw/2026/2026-06-15/quant/universe-ohlcv/`; do not commit raw files.
5. Re-run `scripts/quant_smoke_validate.py` and `scripts/quant_liquidity_filter.py` on the expanded raw directory.
6. Keep result as paper/smoke only until `Point-in-Time` is solved.

## Current Blockers

- Git commit for latest OHLCV thirtyfifth-capture local changes may still be pending.
- Full generated Universe OHLCV coverage is still incomplete.
- Historical KRX status data is not available by Rebalance date.
- Backtest remains `hold`.

## User Preferences

- Korean responses.
- Core Quant terms should stay in English, for example `Universe`, `Liquidity Filter`, `Backtest`, `Point-in-Time`.
- When mentioning stocks, include code and company name, for example `005930 Samsung Electronics`.
- Keep DI/Main/Game watchlists separate from Quant.
- Preserve raw evidence under `_report/raw/**`; do not commit raw files.
