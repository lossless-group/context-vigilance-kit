---
title: "Decisions as their own artifacts"
lede: "A spec says what we intend now. A decision doc says the moment that changed, and why."
maturity: Experimental
mode: prep
order: 14
date_created: 2026-10-05
date_modified: 2026-10-05
authors:
  - Michael Staton
augmented_with:
  - Claude Code on Claude Opus 5.5
tags:
  - Decisions
---
## What it is

A short doc in `context-v/decisions/`: what was decided, when, by whom, and which alternatives were passed over. Kin to Architecture Decision Records, but not limited to architecture.

## Why

Specs get rewritten as intent changes, which erases the record of *why* it changed. Six months later, someone proposes the rejected option again. A decision doc preserves the moment.

## How

- One decision per doc, short.
- Name the alternatives and why they lost. That's the part people need later.
- When the decisions are small, an append-only *decisions log* inside a long-running exploration works too.
