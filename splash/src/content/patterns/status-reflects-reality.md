---
title: "Status reflects reality"
lede: "A folder of Draft plans, half of which shipped, is a folder nobody can trust."
maturity: Canonical
mode: practice
order: 5
date_created: 2026-10-05
date_modified: 2026-10-05
authors:
  - Michael Staton
augmented_with:
  - Claude Code on Claude Opus 5.5
tags:
  - Status
  - Lifecycle
---
## What it is

```
Draft → In-Review → Signed-Off → Implementing → Shipped
        · Partially-Shipped · Deferred · Stale · Superseded · Archived
```

Companion fields move with it: `Shipped` sets `date_first_published`; `Partially-Shipped` adds a dated *Remaining work* section; `Deferred` adds `deferral_note`; `Superseded` adds `superseded_by`.

## Why

`status` is the one field everything else leans on. It's how an agent decides whether a spec is safe to build from, and how a person decides whether a plan is still live.

## How

- Change status when something real happened. Never as tidying.
- Ask before changing a doc someone else owns.
- `Signed-Off` comes from a person, out loud, not from silence.

## In the kit

`/cv:implement` refuses to build against a doc without checkable acceptance criteria, sets `Implementing`, and closes honestly. `/cv:reflect` writes the as-built state.
