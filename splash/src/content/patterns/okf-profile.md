---
title: "Context-v is an OKF bundle"
lede: "Any tool that reads the Open Knowledge Format can read a context-v folder. It costs one frontmatter field and an index file."
maturity: Emerging
mode: practice
order: 21
date_created: 2026-10-05
date_modified: 2026-10-05
authors:
  - Michael Staton
augmented_with:
  - Claude Code on Claude Opus 5.5
tags:
  - OKF
  - Interoperability
  - Frontmatter
---

## What it is

The [Open Knowledge Format](https://github.com/GoogleCloudPlatform/open-knowledge-format) (OKF), an open spec from Google Cloud, is a folder of markdown files with YAML frontmatter, for knowledge that people write, agents generate, and organizations exchange. It deliberately leaves out taxonomy, lifecycle, and body structure. Context-v is exactly those things, so the two stack: **a `context-v/` folder is an OKF v0.2 bundle, and context-v is a profile of it.**

## Why

Conforming means OKF tools (visualizers, validators, other organizations' agents) can read your `context-v/` without knowing anything about context-v. You adopt a standard format with opinions on top, not a private one.

## How

OKF asks for three things:

1. **Every doc has frontmatter.** Context-v already requires it.
2. **Every doc has a `type`.** In context-v it's the folder's name, in Train-Case: `type: Specs`, `type: Explorations`, `type: Decisions`, `type: Research-Notes`. Any folder, new or old, stays conformant.
3. **`index.md` and `log.md` follow OKF's shape when present.** Context-v's root `index.md` is a linked list of what's inside, and declares `okf_version: "0.2"`; each folder's `index.md` lists its docs with a one-line description.

Context-v keeps its own fields and adds OKF ones only where they carry something new. `verified: { by: "human:<id>" }` records a spec's sign-off, which makes the doc *human-reviewed* in OKF's trust tiers. Hex-code citations already work the way OKF keys its sources: by a stable ID, not a position.

One clash, handled by mapping: OKF's `status` is `draft | stable | deprecated`, and context-v keeps its richer lifecycle.

| context-v | OKF |
|---|---|
| Draft, In-Review | `draft` |
| Signed-Off, Implementing, Shipped, Partially-Shipped | `stable` |
| Stale, Superseded, Archived, Deferred | `deprecated` |

## In the kit

The decision, with the alternatives passed over and what's still open, is the kit's first `decisions/` doc: [[Context-V-Is-an-OKF-Profile]]. Templates, `/cv:new`, and the shortcuts set `type`; the frontmatter check requires it; `/cv:init` writes the index. The kit's own `context-v/` passes OKF's conformance rules and renders in OKF's reference visualizer.
