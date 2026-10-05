---
title: "Four-part versions for docs"
lede: "epoch.major.minor.patch, because a doc's history has one more kind of change than code's."
maturity: Canonical
mode: practice
order: 11
date_created: 2026-10-05
date_modified: 2026-10-05
authors:
  - Michael Staton
augmented_with:
  - Claude Code on Claude Opus 5.5
tags:
  - Versioning
---
## What it is

`at_semantic_version: 0.0.0.1`, read as `epoch.major.minor.patch`. New docs start at `0.0.0.1`.

## Why

Docs change in more ways than software: a typo, a new section, a rewritten argument, a complete rethink. The extra digit leaves room for an epoch, a reset when a doc is reborn as something else, without inflating the major number.

## How

- Patch: wording, fixes. Minor: new sections or real additions. Major: the doc's position changed. Epoch: it's a different doc now.
- The version moves with `date_authored_current_draft`, on substantive revisions only.
- `semantic_version` is an accepted alias. Never rewrite a file just to change which spelling it uses.
