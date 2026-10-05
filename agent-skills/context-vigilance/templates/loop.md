---
type: Loops                         # exact: the folder's name (OKF requires it)
title: "Loop: TITLE HERE"
description: ""                     # one plain sentence: what this is (OKF indexes and search show it)
lede: ""                            # optional: one hook line, 140 characters max
publish: false                      # a decision: flip only after reading the finished doc
date_created: YYYY-MM-DD
date_modified: YYYY-MM-DD
date_authored_initial_draft: YYYY-MM-DD
date_authored_current_draft: YYYY-MM-DD   # bump only on a substantive revision
date_authored_final_draft:          # leave empty until it's actually final
authors:
  - AUTHOR                          # humans only
augmented_with:
  - HARNESS on MODEL                # e.g. Claude Code on Claude Opus 5.5
at_semantic_version: 0.0.0.1
status: Draft
tags:
  - Loop
site_uuid: GENERATE                 # run: uuidgen | tr 'A-Z' 'a-z'   (never type one)
hex_code: GENERATE                  # run: LC_ALL=C tr -dc 'a-z0-9' </dev/urandom | head -c6
---

# Loop: TITLE HERE

> This is a *clarified loop*: the developer's own process, written down so an agent can run it the same way every time. Status goes `Draft` → `Proven-Once` after one clean run.

## When to use this loop

What kind of work it's for, and its entry gate (e.g. "a Signed-Off spec or plan with acceptance criteria").

## Settings

| Setting | This repo's choice | Freedom |
|---|---|---|
| Review | e.g. separate reviewer: spec compliance, then code quality | exact |
| What counts as verified | e.g. typecheck + tests + one browser drive for UI | exact |
| Commit granularity | e.g. one commit per work package | shaped |
| Parallel work | e.g. only for packages touching no shared files | exact |
| Human gate | e.g. usability walkthrough before reflect | exact |
| Tools | named by role (tracker, chat…); bound in `context-v/config.md` | — |

## Setup (once per run)

1. ...

## The iteration (once per work package)

Copy this into the reply for each package and tick as you go:

- [ ] Brief: scope, files, done-condition, what not to touch
- [ ] Build
- [ ] Independent review
      → if review fails, back to Build with the review notes
- [ ] Verify by running it
      → if verification fails, back to Build; same blocker twice in a row, stop and escalate
- [ ] Integrate: commit, changelog beat, ticket closed with the commit hash

## Exit

All acceptance criteria met, verification green, human gate passed. Then hand off to `reflect`.

## Lessons from runs

Append-only: what each run taught us about this loop.
