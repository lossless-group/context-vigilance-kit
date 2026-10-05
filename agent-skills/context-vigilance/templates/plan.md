---
title: "Plan: TITLE HERE"
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
  - Plan
spec_reference: "[[Spec-File-Name]]"   # the spec this plan carries out, if any
site_uuid: GENERATE                 # run: uuidgen | tr 'A-Z' 'a-z'   (never type one)
hex_code: GENERATE                  # run: LC_ALL=C tr -dc 'a-z0-9' </dev/urandom | head -c6
---

# Plan: TITLE HERE

> Carries out: [[Spec-File-Name]]

## Why care?

One paragraph: what this plan gets done and why now.

## Steps

Ordered. Each step is small enough to verify before the next one starts.

1. **...** Files: `...`. **Done when:** ...
2. **...** Files: `...`. **Done when:** ...

## Risks and rollback

- ...

## Acceptance criteria

- [ ] ...

## Done when (for this document)

- [ ] Frontmatter: every `YYYY-MM-DD`, `AUTHOR`, `HARNESS on MODEL`, and `GENERATE` replaced (IDs minted by command)
- [ ] Every step names its files and a done-condition someone can check
      → if a step can't be verified on its own, split it or merge it with the next
- [ ] Links to its spec (and the spec links back)
