# 12-Week Daily Quant Study Plan

## Plan Summary

Period: 12 weeks, 84 calendar days.

Expected pace: 60-90 minutes per study day. Weekend days are lighter review days, not heavy implementation days.

Target outcome after 12 weeks:

- You can explain what the current Quant project is trying to build.
- You can read a Strategy spec and separate `Universe`, `Signal`, `Position`, `Risk`, and `Backtest`.
- You can inspect a small OHLCV dataset with Python/pandas.
- You can identify common `Backtest` traps: `Survivorship Bias`, `Lookahead Bias`, `Data Snooping`, `Overfitting`, missing costs, missing `Point-in-Time` evidence.
- You can write a daily note that separates facts, assumptions, questions, and next actions.

## Daily Method

Every day follows the same loop.

1. Explain one sentence in your own words.
2. Read one small artifact or reference.
3. Do one small repo-local practice task.
4. Write one daily log.

Stop condition: when today's log has at least one clear explanation, one unknown term, and one next action.

## Week 1 - Quant Mindset And Project Map

| Day | Topic | Read | Practice | Daily Output |
| --- | --- | --- | --- | --- |
| 1 | What Quant is in this repo | [[_report/quant/README|_report/quant/README.md]], [[_report/quant/implementation-roadmap|_report/quant/implementation-roadmap.md]] metadata and stage table | Write a 5-line explanation of the project without using trading jargon | Daily log with "what we are building" |
| 2 | DI vs Quant | [[_report/di/README|_report/di/README.md]], [[_report/quant/universe|_report/quant/universe.md]] | List 3 reasons a watchlist is not a Quant `Universe` | Daily log with DI/Quant difference |
| 3 | `Universe` | [[_report/quant/universe|_report/quant/universe.md]] | Write inclusion/exclusion examples for Korean common stocks | Daily log with your own `Universe` definition |
| 4 | `Signal` vs order | [[_report/quant/strategies/001-strategy-universe-momentum|_report/quant/strategies/001-strategy-universe-momentum.md]] | Find where the Strategy creates a candidate but not an order | Daily log with Signal/order distinction |
| 5 | `Benchmark` and risk | [[_report/quant/glossary|_report/quant/glossary.md]] | Pick KOSPI/KOSDAQ/KOSPI200 and explain which comparison each fits | Daily log with Benchmark notes |
| 6 | Review | This week's logs | Rewrite the 5 hardest terms in simple Korean | Weekly checkpoint section |
| 7 | Rest and questions | No new reading | List the top 5 questions for AI or future repo work | Question backlog |

## Week 2 - Market Data Basics

| Day | Topic | Read | Practice | Daily Output |
| --- | --- | --- | --- | --- |
| 8 | OHLCV | Existing raw daily price files under `_report/raw/**` | Identify date, open, high, low, close, volume in one saved response or CSV | OHLCV explanation |
| 9 | Adjusted price | `../research/` files mentioning adjusted or normalized market data | Write why splits/dividends can break naive returns | Data quality memo |
| 10 | Trading value | `../research/*liquidity*` | Explain price x volume and why liquidity matters | Liquidity note |
| 11 | Missing data | [[_report/quant/implementation-roadmap|_report/quant/implementation-roadmap.md]] data pipeline sections | Find one artifact that says `hold`, `missing`, or `data-insufficient` | Missing-data example |
| 12 | Raw vs interpreted data | `_report/raw/README` if present, else raw folder structure | Describe why raw evidence and conclusions are separated | Raw-data rule note |
| 13 | Review | Days 8-12 | Build a checklist for "can I trust this dataset?" | Weekly checkpoint |
| 14 | Rest and questions | No new reading | Add unknown data terms to the backlog | Question backlog |

## Week 3 - Python And pandas Basics

| Day | Topic | Read | Practice | Daily Output |
| --- | --- | --- | --- | --- |
| 15 | Python file reading | `scripts/` one small Quant script | Identify inputs, outputs, and main function | Script map |
| 16 | CSV shape | One `.rows.csv` under `../research/` | Count rows and columns with a simple command or editor | CSV shape note |
| 17 | DataFrame idea | A Quant script using pandas | Explain index, columns, rows | DataFrame note |
| 18 | Dates | A script that parses dates | Explain why trading dates are not calendar dates | Date handling note |
| 19 | Basic returns | Existing return smoke artifact | Define simple return: today close / yesterday close - 1 | Return note |
| 20 | Review | Days 15-19 | Write what you can now inspect without AI | Weekly checkpoint |
| 21 | Rest and questions | No new reading | Add Python questions to backlog | Question backlog |

## Week 4 - Return And Risk

| Day | Topic | Read | Practice | Daily Output |
| --- | --- | --- | --- | --- |
| 22 | Daily return | Return smoke artifact | Calculate one simple return by hand | Calculation note |
| 23 | Cumulative return | Backtest/PnL smoke artifact | Explain compounding in one paragraph | Cumulative return note |
| 24 | Volatility | [[_report/quant/glossary|_report/quant/glossary.md]] | Explain volatility as instability, not just loss | Volatility note |
| 25 | MDD | [[_report/quant/glossary|_report/quant/glossary.md]] | Draw or describe peak-to-trough loss | MDD note |
| 26 | Turnover | Backtest assumptions or portfolio target artifact | Explain why frequent trading costs money | Turnover note |
| 27 | Review | Days 22-26 | Create a mini risk glossary | Weekly checkpoint |
| 28 | Rest and questions | No new reading | Add risk questions to backlog | Question backlog |

## Week 5 - Universe And Liquidity Filter

| Day | Topic | Read | Practice | Daily Output |
| --- | --- | --- | --- | --- |
| 29 | Rule-based `Universe` | [[_report/quant/universe|_report/quant/universe.md]] | Write a rule that does not name a specific stock | Rule note |
| 30 | Listing Age | [[_report/quant/implementation-roadmap|_report/quant/implementation-roadmap.md]] Stage 3-4 | Explain why newly listed stocks need care | Listing Age note |
| 31 | Managed issues and suspension | Point-in-Time status artifacts | Explain why current status is not enough for history | Status note |
| 32 | `Liquidity Filter` | Liquidity smoke artifact | Explain the 20-day average trading value threshold | Liquidity Filter note |
| 33 | Current snapshot limitation | Current Universe artifacts | Explain why current snapshot is not historical truth | Current snapshot warning |
| 34 | Review | Days 29-33 | Draft a `Universe` checklist | Weekly checkpoint |
| 35 | Rest and questions | No new reading | Add Universe questions to backlog | Question backlog |

## Week 6 - Strategy Spec

| Day | Topic | Read | Practice | Daily Output |
| --- | --- | --- | --- | --- |
| 36 | Strategy hypothesis | [[_report/quant/strategies/001-strategy-universe-momentum|_report/quant/strategies/001-strategy-universe-momentum.md]] | Restate the hypothesis in 3 plain sentences | Hypothesis note |
| 37 | Entry rule | Strategy spec | Find the entry condition | Entry note |
| 38 | Exit rule | Strategy spec | Find the exit or invalidation condition | Exit note |
| 39 | Parameters | Strategy config `.kis.yaml` | List each parameter and what it changes | Parameter note |
| 40 | Failure condition | Bias checklist for strategy 001 | Write how the strategy could fail | Failure note |
| 41 | Review | Days 36-40 | Summarize strategy 001 without claiming profit | Weekly checkpoint |
| 42 | Rest and questions | No new reading | Add Strategy questions to backlog | Question backlog |

## Week 7 - Signal Candidate Pipeline

| Day | Topic | Read | Practice | Daily Output |
| --- | --- | --- | --- | --- |
| 43 | Signal Candidate | Signal candidate smoke artifact | Explain why candidate is not an order | Candidate note |
| 44 | Rebalance date | Signal candidate rows | Explain what date the decision is made on | Rebalance note |
| 45 | Lookback | Strategy/spec docs | Explain 5-day or 20-day lookback | Lookback note |
| 46 | Forward return | Forward-return smoke artifact | Explain why forward return is only for evaluation | Forward-return note |
| 47 | Portfolio target | Portfolio target smoke artifact | Explain target weight vs actual holdings | Portfolio target note |
| 48 | Review | Days 43-47 | Draw the pipeline: Universe -> Liquidity -> Signal -> Evaluation | Weekly checkpoint |
| 49 | Rest and questions | No new reading | Add pipeline questions to backlog | Question backlog |

## Week 8 - Backtest Basics

| Day | Topic | Read | Practice | Daily Output |
| --- | --- | --- | --- | --- |
| 50 | What `Backtest` can prove | Backtest template | Write what a Backtest does and does not prove | Backtest definition |
| 51 | Input contract | Backtest input contract artifact | Explain why joinable data matters | Input contract note |
| 52 | Costs | Cost/benchmark assumptions artifact | List fee, tax, and `Slippage` assumptions | Cost note |
| 53 | Benchmark return | Benchmark return smoke artifact | Explain strategy return vs benchmark return | Benchmark return note |
| 54 | PnL smoke | Backtest PnL smoke artifact | Explain why `pass_smoke` is not production-ready | PnL smoke warning |
| 55 | Review | Days 50-54 | Create a "Backtest trust checklist" | Weekly checkpoint |
| 56 | Rest and questions | No new reading | Add Backtest questions to backlog | Question backlog |

## Week 9 - Bias Control

| Day | Topic | Read | Practice | Daily Output |
| --- | --- | --- | --- | --- |
| 57 | `Survivorship Bias` | Bias control template | Explain using only surviving stocks as a mistake | Survivorship note |
| 58 | `Lookahead Bias` | Bias control template | Explain using future-known data too early | Lookahead note |
| 59 | `Data Snooping` | Bias control template | Explain repeated parameter hunting | Data snooping note |
| 60 | `Overfitting` | Bias control template | Explain past-fit vs future robustness | Overfitting note |
| 61 | Parameter freeze | Strategy spec/config | Write when parameters should stop changing | Parameter freeze note |
| 62 | Review | Days 57-61 | Add bias checks to Backtest trust checklist | Weekly checkpoint |
| 63 | Rest and questions | No new reading | Add bias questions to backlog | Question backlog |

## Week 10 - Out-of-Sample And Walk-Forward

| Day | Topic | Read | Practice | Daily Output |
| --- | --- | --- | --- | --- |
| 64 | `Out-of-Sample` | OOS/walk-forward plan | Explain train/test split in plain words | OOS note |
| 65 | Walk-forward | OOS/walk-forward plan | Explain rolling validation | Walk-forward note |
| 66 | Stress periods | Backtest template | Pick one stress market and say why it matters | Stress note |
| 67 | Regime | Market regime scan routine/template | Explain risk-on/risk-off without overusing it | Regime note |
| 68 | Hold states | Readiness check artifact | Explain why `hold` is a useful status | Hold status note |
| 69 | Review | Days 64-68 | Write when a strategy is still not ready | Weekly checkpoint |
| 70 | Rest and questions | No new reading | Add OOS questions to backlog | Question backlog |

## Week 11 - Paper Signal Tracking

| Day | Topic | Read | Practice | Daily Output |
| --- | --- | --- | --- | --- |
| 71 | Paper tracking | Paper signal routine/template | Explain paper tracking vs trading | Paper tracking note |
| 72 | Decision log relation | [[_report/decisions/decision-log|_report/decisions/decision-log.md]] structure | Explain what belongs in a decision log | Decision-log note |
| 73 | Data evidence | Raw folder plus one paper signal artifact | Link raw evidence to a signal note | Evidence chain note |
| 74 | Invalidation | Strategy spec | Write what would invalidate a Signal Candidate | Invalidation note |
| 75 | No live trading rule | Project guardrails | Explain why learning output cannot trigger orders | Safety note |
| 76 | Review | Days 71-75 | Draft a paper Signal tracking checklist | Weekly checkpoint |
| 77 | Rest and questions | No new reading | Add execution-safety questions to backlog | Question backlog |

## Week 12 - Integration And Personal Operating Manual

| Day | Topic | Read | Practice | Daily Output |
| --- | --- | --- | --- | --- |
| 78 | Project recap | [[_report/quant/implementation-roadmap|_report/quant/implementation-roadmap.md]] current judgment | Write a one-page state of the Quant project | Project recap |
| 79 | Explain the pipeline | Your Week 7 diagram | Rewrite the pipeline from memory | Pipeline recap |
| 80 | Explain blockers | Readiness check artifact | List blockers before real Backtest promotion | Blocker recap |
| 81 | Personal glossary | All daily logs | Consolidate 20 terms into your own glossary | Glossary draft |
| 82 | Operating manual | This folder and existing routines | Write your "how I study and verify Quant" manual | Operating manual draft |
| 83 | Final review | All weekly checkpoints | Mark concepts as clear / shaky / unknown | Final checkpoint |
| 84 | Next 12-week plan | Final checkpoint | Choose next track: implementation, math/statistics, or market microstructure | Next plan memo |

## Weekly Checkpoint Format

Add this section to the final log of each week.

```markdown
## Weekly Checkpoint

- Concepts I can explain:
- Concepts still unclear:
- Repo files I can now read:
- One mistake I am less likely to make:
- Next week's priority:
```

## Recommended Next Track After Week 12

Choose one path.

- Implementation track: tests, data contracts, reproducible pipelines.
- Statistics track: distributions, hypothesis testing, sampling error, factor exposure.
- Market microstructure track: spreads, order books, liquidity, execution cost.
