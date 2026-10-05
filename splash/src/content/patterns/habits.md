---
title: "Habits: recurring upkeep with a trigger"
lede: "A reminder fires when you happen to be doing something. A habit fires whether or not anything reminded you."
maturity: Experimental
mode: reflection
order: 15
date_created: 2026-10-05
date_modified: 2026-10-05
authors:
  - Michael Staton
augmented_with:
  - Claude Code on Claude Opus 5.5
tags:
  - Habits
  - Maintenance
---
## What it is

Docs in `context-v/habits/` named *Maintain [the thing] across [the scope]*, each with its trigger, procedure, and scope.

Two trigger shapes:

- **Event-driven:** update the README when a change makes it untrue.
- **Periodic sweep:** walk every `context-v/` and fix stale `status` values.

## Why

The practice decays without upkeep, and upkeep nobody owns doesn't happen. Most habits are addressed to the agent, and should say so.

## How

- Say what fires it and how far it reaches.
- Keep the procedure short enough to run in one sitting.
