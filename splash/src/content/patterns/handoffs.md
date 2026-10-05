---
title: "Handoffs between sessions"
lede: "The last thing a session writes is the first thing the next one reads."
maturity: Experimental
mode: journey
order: 12
date_created: 2026-10-05
date_modified: 2026-10-05
authors:
  - Michael Staton
augmented_with:
  - Claude Code on Claude Opus 5.5
tags:
  - Handoffs
  - Sessions
---
## What it is

A short doc in `context-v/handoffs/` at the end of a working session: what landed, what's mid-flight, what the next session must know, and which docs to load first.

## Why

Agents don't remember between sessions, and people forget over a weekend. Re-deriving the state of half-finished work is the most expensive way to start a session. The tooling world is converging on the handoff as a primitive.

## How

- Write it while the details are fresh, not tomorrow.
- *Load first* is the most valuable section: three to five links.
- Date-prefixed filenames sort themselves: `2026-10-05_Payment-Retry.md`.

## In the kit

`/cv:reflect` writes one. `/cv:kickoff` reads the newest one first.
