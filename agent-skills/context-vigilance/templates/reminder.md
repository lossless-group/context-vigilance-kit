---
type: Reminders                         # exact: the folder's name (OKF requires it)
title: "Reminder: TITLE HERE"
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
status: Active
tags:
  - Reminder
related_blueprint: "[[Blueprint-Name]]"
site_uuid: GENERATE                 # run: uuidgen | tr 'A-Z' 'a-z'   (never type one)
hex_code: GENERATE                  # run: LC_ALL=C tr -dc 'a-z0-9' </dev/urandom | head -c6
---

# Reminder: TITLE HERE

**Don't:** ...

**Do:** ...

## Why

One or two sentences. The full reasoning lives in the blueprint: [[Blueprint-Name]].

## Triggers

When loading this reminder helps:

- ...
