---
title: "Name roles, bind tools in config"
lede: "Skills say “file it in the tracker.” One config file says which tracker."
maturity: Emerging
mode: practice
order: 19
date_created: 2026-10-05
date_modified: 2026-10-05
authors:
  - Michael Staton
augmented_with:
  - Claude Code on Claude Opus 5.5
tags:
  - Integrations
  - Config
---
## What it is

Workflows reach outside the repo: file a ticket, post a ship note, update the docs site. Skills and loops name **roles** (`tracker`, `chat`, `docs`, `design`, `memory`, …), and an optional `context-v/config.md` binds each role to the team's tool and how to reach it.

## Why

Teams differ completely on tools. A skill that names one tracker is useless to a team on another. Naming roles keeps one skill working everywhere.

## How

- No config means everything stays in `context-v/`: issues in `issues/`, nothing posted anywhere.
- Secrets never go in config. It names environment variables; their names go in `.env.example`.
- Anything outward-facing asks first by default.
