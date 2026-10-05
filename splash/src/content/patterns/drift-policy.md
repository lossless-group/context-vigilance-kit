---
title: "Notice drift, don't fix it in passing"
lede: "Inconsistencies get reported, not silently cleaned up as a side effect of other work."
maturity: Canonical
mode: practice
order: 10
date_created: 2026-10-05
date_modified: 2026-10-05
authors:
  - Michael Staton
augmented_with:
  - Claude Code on Claude Opus 5.5
tags:
  - Drift
  - Collaboration
---
## What it is

When an agent finds mismatched frontmatter, off-pattern filenames, or a half-adopted convention while doing something else, it notes it and tells the user. It doesn't fix it.

## Why

People run several agent sessions at once. A "helpful" cleanup in one collides with real work in another, and nobody asked for it. Conventions here are norms, and consistency comes from focused passes, not ambient tidying.

## How

- Mention it once, plainly, with the paths.
- Fix it only when asked, in a pass of its own.
- When a convention changes, old files keep working: readers accept both the old and new spellings.
