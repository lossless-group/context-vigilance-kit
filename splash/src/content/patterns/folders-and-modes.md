---
title: "Eight folders, three modes"
lede: "Every doc has one obvious home, and the folder says what kind of thinking it holds."
maturity: Canonical
mode: practice
order: 1
date_created: 2026-10-05
date_modified: 2026-10-05
authors:
  - Michael Staton
augmented_with:
  - Claude Code on Claude Opus 5.5
tags:
  - Folders
  - Cognitive-Modes
---
## What it is

A `context-v/` folder at the root of each repo, with eight canonical subfolders sorted into three modes of thinking:

| Mode | Folders | The work |
|---|---|---|
| **Prep** | `specs/`, `plans/`, `prompts/` | Deciding what to build, at falling altitude |
| **Reflection** | `blueprints/`, `reminders/`, `agent-skills/` | Codifying how the system works and what keeps going wrong |
| **Journey** | `explorations/`, `issues/` | Finding out: research, and the painful path through bugs |

Plus two utility folders every project gets: `extra/` (scratch, gitignored) and `sitemap/` (what exists where).

## Why

An agent arriving cold needs to know where to look and where to write. A fixed vocabulary of folders answers both without a conversation. The mode tells it *how* to read: a spec is a promise, an exploration is a question, an issue is a story.

## How

- Not sure where a doc goes? Ask what kind of thinking it holds, not what topic it's about.
- A folder outside the set is fine. Read it, name its mode, and decide with the team whether to keep it, fold it, or promote it.

## In the kit

`/cv:init` lays down the eight plus `extra/` and `sitemap/`. The `context-vigilance` skill carries the decision list.
