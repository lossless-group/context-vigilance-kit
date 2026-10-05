---
type: Decisions                     # exact: the folder's name (OKF requires it)
title: "TITLE HERE"
description: ""                     # one plain sentence: what was decided
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
status: Draft                       # Signed-Off once the decider says so
tags:
  - Decisions
# verified: { by: "human:<id>", at: YYYY-MM-DDTHH:MM:SSZ }   # added at sign-off (OKF trust)
site_uuid: GENERATE                 # run: uuidgen | tr 'A-Z' 'a-z'   (never type one)
hex_code: GENERATE                  # run: LC_ALL=C tr -dc 'a-z0-9' </dev/urandom | head -c6
---

# TITLE HERE

## Why care?

One paragraph an outsider can read: what was at stake.

## The decision

What was decided, in a sentence or two. Then who decided, and when.

## What changes

- ...

## Alternatives passed over

- **Option:** why it lost. This is the part people need six months from now.

## Still open

- ...

## How we'll know it worked

- ...

## Related

- [[...]]

## Done when (for this document)

- [ ] Frontmatter: every `YYYY-MM-DD`, `AUTHOR`, `HARNESS on MODEL`, and `GENERATE` replaced (IDs minted by command)
- [ ] The decision is stated in one sentence, with who decided and when
- [ ] At least one alternative is named, with why it lost
      → if there were no alternatives, it may not be a decision; consider whether it belongs in a spec
