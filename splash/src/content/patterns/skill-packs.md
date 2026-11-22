---
title: "Skill packs: other people's skills, by the set"
lede: "One borrowed skill goes in agent-skills/. A whole pack, on a theme or from a developer whose way of working you admire, goes in skill-packs/: linked to its source, with a note on why it's there."
maturity: Experimental
mode: reflection
order: 22
date_created: 2026-11-21
date_modified: 2026-11-21
authors:
  - Michael Staton
augmented_with:
  - Claude Code on Claude Opus 5.5
tags:
  - Skill-Packs
  - Agent-Skills
  - Third-Party
---
## What it is

A `context-v/skill-packs/` folder for other people's multi-skill packs. A pack is a set of skills around one theme (SEO, design, testing), or one developer's whole setup. For example:

- [Garry Tan's gstack](https://github.com/garrytan/gstack): his Claude Code setup, with tools that act as CEO, designer, eng manager, release manager and QA.
- [Matt Pocock's skills](https://github.com/mattpocock/skills): "Skills for Real Engineers," straight from his own agent folder.
- [andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills): a single `CLAUDE.md` that others drew from Andrej Karpathy's notes on how coding agents go wrong.

Each pack sits in the folder as a **git submodule**: a pointer to its source repo at a pinned version, not a copy. Beside them, `skill-packs/README.md` says for each pack where it comes from, why you keep it, and what it does.

A single skill someone else wrote is different: it goes straight into `agent-skills/<name>/`, also as a submodule, and loads like one of yours.

## Why

The best skills are often someone else's. A strong developer's skills show how they actually work: what they ask agents to check, what they refuse to let an agent guess. That's worth reading closely, and worth borrowing from.

But a pack isn't your context. Copy its files into your repo and three things go wrong. Your agent starts treating someone else's conventions as yours. The copy stops tracking the source the day you make it. And anything that reads `context-v/` (search, a survey, a published roll-up) mixes their files in with your docs, broken image paths included. A submodule keeps the pack readable, current with one command, and clearly theirs.

## How

- Add a pack with `git submodule add <repo-url> context-v/skill-packs/<name>`. Never a plain clone, and never copied files.
- Write its entry in `skill-packs/README.md`: source, why it's here, what you've taken from it so far.
- To run a pack's skills, install them the way its author says (a plugin, an installer). To borrow one idea, write it into a skill of your own in your own words, and credit the source.
- Update a pack by moving its submodule pointer, not by editing inside it.

## In the kit

The `context-vigilance` skill tells agents what `skill-packs/` is for. The survey reads `skill-packs/README.md` and skips the packs themselves, so they never show up as your docs.
