---
title: "Handoff: TITLE HERE"
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
status: Active
tags:
  - Handoff
site_uuid: GENERATE                 # run: uuidgen | tr 'A-Z' 'a-z'   (never type one)
hex_code: GENERATE                  # run: LC_ALL=C tr -dc 'a-z0-9' </dev/urandom | head -c6
---

# Handoff: TITLE HERE

> For the next session, human or agent. Read this first, then the docs listed under *Load first*.

## Where things stand

One paragraph: what this work is and how far it got.

## What landed

- ... (link commits, changelog entries)

## Mid-flight

- ... (half-done work, uncommitted changes, open branches)

## What the next session must know

- Decisions made and why, gotchas, anything that would cost time to rediscover.

## Load first

- [[Spec-or-Plan]]
- [[...]]

## Next steps

1. ...
