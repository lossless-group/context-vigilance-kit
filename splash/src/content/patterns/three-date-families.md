---
title: "Three families of dates"
lede: "When the file changed, when the thinking changed, and when the work happened are three different questions."
maturity: Canonical
mode: practice
order: 4
date_created: 2026-10-05
date_modified: 2026-10-05
authors:
  - Michael Staton
augmented_with:
  - Claude Code on Claude Opus 5.5
tags:
  - Dates
  - Frontmatter
---
## What it is

| Family | Keys | Answers |
|---|---|---|
| Filesystem | `date_created`, `date_modified` | When did these bytes appear and last change? |
| Editorial | `date_authored_initial_draft`, `date_authored_current_draft`, `date_authored_final_draft` | When was this really written, meaningfully revised, finished? |
| Lifecycle | `date_first_published`, `date_work_started`, `date_work_completed` | When did it ship? When did the work happen? |

## Why

Docs in `context-v/` keep evolving, and the filesystem lies in both directions. Opening a file in some editors bumps its modified time. A machine restore can reset creation dates. Telling a doc that moved last week from one stable since spring is the whole job, and one date can't do it.

## How

- `date_modified` moves on every edit.
- `date_authored_current_draft` and the version move only on a *substantive* revision.
- An empty `date_authored_final_draft` means "not final yet." Leave it empty; don't delete it.
- Work dates: omit rather than guess.
