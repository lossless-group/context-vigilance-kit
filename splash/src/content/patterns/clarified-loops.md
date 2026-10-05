---
title: "Clarified loops"
lede: "Every developer has their own process. Write it down once, and an agent runs it the same way every time."
maturity: Experimental
mode: reflection
order: 13
date_created: 2026-10-05
date_modified: 2026-10-05
authors:
  - Michael Staton
augmented_with:
  - Claude Code on Claude Opus 5.5
tags:
  - Loops
  - Process
  - Subagents
---
## What it is

A doc in `context-v/loops/` that defines a recurring process: when it applies, its entry gate, the steps of one iteration, and when it ends. Its status goes `Draft` → `Proven-Once` after one clean run.

## Why

"Follow my loop" doesn't work when the loop lives in someone's head. Imposing a standard loop doesn't work either: teams differ on review depth, what counts as verified, and where the human checks in. The answer is to *clarify* the developer's own loop and save it.

## How

- Start from a default (brief → build → independent review → verify → integrate) and change only what this team does differently.
- Tool choices go in config, not in the loop. The loop says "file it in the tracker", not which tracker.
- Problems found during a run go back into the loop doc's *Lessons from runs*.

## In the kit

`/cv:loop` finds a matching loop or helps write one, then runs it as VP of Engineering with subagents.
