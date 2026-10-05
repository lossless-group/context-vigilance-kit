---
title: "Explore → spec → plan → prompt"
lede: "Work climbs down a ladder of altitude, and every rung is a doc that outlives the session."
maturity: Canonical
mode: prep
order: 7
date_created: 2026-10-05
date_modified: 2026-10-05
authors:
  - Michael Staton
augmented_with:
  - Claude Code on Claude Opus 5.5
tags:
  - Specs
  - Plans
  - Workflow
---
## What it is

The most common rhythm in practice:

1. An **exploration** asks the question and weighs options.
2. When it has learned enough, it's *adapted* into a **spec**: what we're building, why, and how we'll know it works.
3. The spec's phases become a **plan**: ordered, scoped, each step checkable.
4. Optionally, a **prompt** breaks the plan into steps to run across sessions.

## Why

> A prompt without a spec is a vibe. A prompt within a spec is engineering.

Each rung carries acceptance criteria down. Plan-mode output that would otherwise vanish when the session ends lands in `plans/` instead.

## How

- Promotion is an adaptation, not a move. The parent stays, linked both ways.
- Specs have a sign-off gate before anyone builds.
- Acceptance criteria are things someone can check: a command, a test, a click-path.

## In the kit

`/cv:prep` plays senior product manager on this ladder and writes no code. `/cv:implement` and `/cv:loop` take it from a signed-off doc.
