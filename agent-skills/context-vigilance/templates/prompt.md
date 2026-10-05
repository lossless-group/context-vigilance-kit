---
title: "Prompt: TITLE HERE"
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
  - Prompt
implements_spec: "[[Spec-File-Name]]"
site_uuid: GENERATE                 # run: uuidgen | tr 'A-Z' 'a-z'   (never type one)
hex_code: GENERATE                  # run: LC_ALL=C tr -dc 'a-z0-9' </dev/urandom | head -c6
---

# Prompt: TITLE HERE

> Implements: [[Spec-File-Name]]
> Blueprints to load: [[Blueprint-1]]
> Reminders to load: [[Reminder-1]]

## Context

What the agent needs to know before starting: files, prior decisions, constraints.

## Steps

### Step 1: ...

**Goal:** ...

**Action:** ...

**Verify:** how to confirm this step succeeded before moving on.

### Step 2: ...

...

## Done when

- [ ] Every step's Verify passed
      → if one fails, fix it there; don't continue past a failed step
- [ ] ...

## Notes

What running this prompt taught us that should feed back into the spec or a blueprint.
