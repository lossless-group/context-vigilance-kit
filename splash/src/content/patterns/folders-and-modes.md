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
- The set is a start, not a limit. New folders are welcome when the work calls for one (`narratives/`, `profiles/`, `research-notes/`). Folder names are plural; `extra/` and `sitemap/` are the long-standing singular exceptions.
- Every doc's `type` is its folder's name, in Train-Case: `specs/` → `type: Specs`, `research-notes/` → `type: Research-Notes`. That one field is what makes any folder readable by [[okf-profile|Open Knowledge Format]] tools.
- Someone else's skill goes in `agent-skills/` as a git submodule; a whole pack of them goes in `skill-packs/`. Either way it's a link to the source, never a copy. See [[skill-packs|Skill packs]].
- What's running right now, such as a deployment or a service topology, goes in `mirrors/` (experimental). A mirror records when it was taken and from where, and is re-taken rather than edited when it drifts. `sitemap/` is the website version of the same idea.
- A folder outside the set is fine. Read it, name its mode, and decide with the team whether to keep it, fold it, or promote it.

## In the kit

`/cv:init` lays down the eight plus `extra/` and `sitemap/`. The `context-vigilance` skill carries the decision list.
