---
title: "Fork early, keep the map"
lede: "Split a growing doc before it hurts. The parent keeps the map; children carry the detail."
maturity: Canonical
mode: practice
order: 8
date_created: 2026-10-05
date_modified: 2026-10-05
authors:
  - Michael Staton
augmented_with:
  - Claude Code on Claude Opus 5.5
tags:
  - Writing
  - Cross-Linking
---
## What it is

When a doc grows, factor out the parts that stand alone: a pattern into a blueprint, a sub-system into its own spec, a debugging trail into an issue. Link each from the parent.

## Why

Long context windows can technically swallow huge docs. But creativity, cross-referencing, and human-agent cooperation all degrade as a single doc grows. Humans have context windows too.

## How

- The trigger is *anxiety about length*, not a word count: when you scroll past sections to reach the one that matters.
- The parent keeps the why and the map. Each child is readable on its own.
- Link with `[[Wikilinks]]`, relative links, or backtick paths, whichever serves the reader.
