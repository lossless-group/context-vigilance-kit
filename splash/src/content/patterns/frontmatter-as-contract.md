---
title: "Frontmatter is a contract"
lede: "A small block of YAML lets tools, sites, and agents read a doc without reading all of it."
maturity: Canonical
mode: practice
order: 2
date_created: 2026-10-05
date_modified: 2026-10-05
authors:
  - Michael Staton
augmented_with:
  - Claude Code on Claude Opus 5.5
tags:
  - Frontmatter
  - Metadata
---
## What it is

Every doc starts with YAML frontmatter: `type`, `title`, `lede`, dates, `authors`, `augmented_with`, `at_semantic_version`, `status`, `tags`, and two identity fields.

## Why

Frontmatter is what list views, search, share cards, retrieval tools, and an agent triaging fifty files all read *instead of* the body. Treat it as an interface. Change a key's meaning and every reader breaks quietly.

## How

- **Exact:** keys are `snake_case`, dates are `YYYY-MM-DD`, tags and status values are Train-Case.
- **Exact:** `type` is the doc's folder name in Train-Case (`type: Specs`, `type: Decisions`). It's the one field the [[okf-profile|Open Knowledge Format]] requires.
- **Respect what's there.** Never delete a key you don't recognize. Not knowing what it does is a reason to leave it.
- `authors` is humans only; agents go in `augmented_with`.

```yaml
type: Specs
title: "Payment Retry Policy"
lede: "Failed charges retry on a schedule customers can predict."
status: Draft
at_semantic_version: 0.0.0.1
```

## In the kit

The templates carry the baseline. The plugin's hook checks the few fields with one right answer before any write to `context-v/`.
