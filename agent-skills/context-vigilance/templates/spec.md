---
title: "TITLE HERE"
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
  - Spec
summary: ""                          # optional, agent-facing: what this doc is FOR and what it unblocks
# date_work_started: YYYY-MM-DD    # when the WORK happened; omit rather than guess
# date_work_completed: YYYY-MM-DD
site_uuid: GENERATE                 # run: uuidgen | tr 'A-Z' 'a-z'   (never type one)
hex_code: GENERATE                  # run: LC_ALL=C tr -dc 'a-z0-9' </dev/urandom | head -c6
---

# TITLE HERE

## Why care?

One paragraph an outsider can read: what this is, who it's for, why it matters now.

## Goals

- ...

## Non-goals

- ...

## Constraints and assumptions

- ...

## Design

The what and the why: architecture, data shapes, interfaces, behaviors.

## Phases

Each phase is a slice someone can build and check on its own.

### Phase 1: ...

**Done when:** a check anyone can run (a command, a test, a click-path), not "the code exists".

## Acceptance criteria

The spec is shipped when all of these are true:

- [ ] ...

## Open questions

- [ ] ...

## Related

- [[Exploration-This-Came-From]]

## Done when (for this document)

- [ ] Frontmatter: every `YYYY-MM-DD`, `AUTHOR`, `HARNESS on MODEL`, and `GENERATE` replaced (IDs minted by command)
- [ ] Every phase and the spec as a whole have checkable done-conditions
      → if any is "it works" or "looks good", rewrite it before asking for sign-off
- [ ] Open questions are either answered or explicitly deferred
- [ ] Linked back to the exploration it came from, if any
