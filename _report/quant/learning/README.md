# Quant Learning Journal

## Purpose

This folder is the daily learning journal for the Quant project.

The goal is not to become a professional quant researcher in one pass. The goal is to understand enough to ask better questions, read the project artifacts, and avoid trusting a `Backtest` or AI-generated signal too quickly.

## How To Use

Use this folder every study day.

When the user asks for daily Quant learning content, follow [[_report/quant/routines/daily-learning-routine|_report/quant/routines/daily-learning-routine.md]].

1. Open [[_report/quant/learning/12-week-daily-plan|12-week-daily-plan.md]].
2. Find the next unfinished day.
3. Copy [[_report/quant/learning/templates/daily-log|templates/daily-log.md]] into `daily/YYYY/YYYY-MM-DD.md`.
4. Fill in only what you actually understood.
5. Leave unknown terms visible instead of guessing.

Recommended daily time box:

- Reading: 20-30 minutes
- Practice: 30-45 minutes
- Journal: 10-15 minutes

If a day is missed, do not rewrite the calendar. Continue from the next unfinished day.

## Folder Structure

```text
_report/quant/learning/
  README.md
  12-week-daily-plan.md
  daily/
    YYYY/
      YYYY-MM-DD.md
  templates/
    daily-log.md
```

## Current Start

- Start date: 2026-07-08
- First daily log: [[_report/quant/learning/daily/2026/2026-07-08|daily/2026/2026-07-08.md]]
- Plan length: 12 weeks / 84 calendar days
- Main output rhythm: one daily note, one weekly checkpoint

## Study Rules

- Keep these core terms in English: `Universe`, `Liquidity Filter`, `Backtest`, `Point-in-Time`, `Signal`, `Benchmark`, `Slippage`, `Out-of-Sample`.
- AI can explain and generate practice code, but AI output is not evidence.
- A good-looking `Backtest` is not proof of a tradable strategy.
- Do not connect learning work to live orders.
- Keep raw market/API responses under `_report/raw/**`, not in this folder.
- Do not record account numbers, app keys, tokens, actual holdings, or private position size here.

## Link To Existing Quant Work

- Existing beginner roadmap: [[_report/quant/learning-roadmap|../learning-roadmap.md]]
- Current implementation state: [[_report/quant/implementation-roadmap|../implementation-roadmap.md]]
- Glossary: [[_report/quant/glossary|../glossary.md]]
- Quant routines: `../routines/`
- Strategy specs: `../strategies/`
