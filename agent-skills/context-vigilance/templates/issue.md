---
type: Issues                         # exact: the folder's name (OKF requires it)
title: "Issue: TITLE HERE"
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
status: Open
tags:
  - Issue
tracker_url:                         # if this issue also lives in a ticket system
site_uuid: GENERATE                 # run: uuidgen | tr 'A-Z' 'a-z'   (never type one)
hex_code: GENERATE                  # run: LC_ALL=C tr -dc 'a-z0-9' </dev/urandom | head -c6
---

# Issue: TITLE HERE

## Symptom

What was actually seen: exact errors, reproduction steps.

```
paste the exact error here
```

## Environment

- OS, runtime, versions
- Branch and commit

## Hypothesis log

Append-only. Wrong guesses stay; they're the value of this doc.

### H1: ...

**Reasoning:** ...
**Test:** ...
**Result:** ❌ / ✅
**Learned:** ...

## Root cause

(When found.) The actual cause, separated from contributing factors.

## Fix

What changed. Link the commit or PR.

## Prevention

A reminder, blueprint, or check that stops it recurring: [[...]]

## Done when (for this document)

- [ ] Frontmatter: every `YYYY-MM-DD`, `AUTHOR`, `HARNESS on MODEL`, and `GENERATE` replaced (IDs minted by command)
- [ ] Root cause is stated, not just the fix
      → if you only know what made the symptom go away, keep status Open
- [ ] Prevention is linked, or explicitly "none needed, because…"
