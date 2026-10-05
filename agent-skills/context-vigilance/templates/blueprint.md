---
title: "Blueprint: TITLE HERE"
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
  - Blueprint
site_uuid: GENERATE                 # run: uuidgen | tr 'A-Z' 'a-z'   (never type one)
hex_code: GENERATE                  # run: LC_ALL=C tr -dc 'a-z0-9' </dev/urandom | head -c6
---

# Blueprint: TITLE HERE

## What this is

One paragraph: the pattern, system, or convention this blueprint codifies.

## Why it exists

What problem it solves, what the alternatives were, and why this one.

## How it works

The mechanics: diagrams, code shapes, file layouts, data flows.

## How to follow it

What a contributor (human or agent) does to stay consistent with it.

## Anti-patterns

What it rules out, and why.

## Related reminders

- [[Reminder-Derived-From-This-Blueprint]]

## Done when (for this document)

- [ ] Frontmatter: every `YYYY-MM-DD`, `AUTHOR`, `HARNESS on MODEL`, and `GENERATE` replaced (IDs minted by command)
- [ ] "How to follow it" is concrete enough that an agent could follow it without asking
