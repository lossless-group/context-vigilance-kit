---
title: "Contracts: what must never break"
lede: "Not suggestions. Standing rules for agents, or exact interfaces data must follow."
maturity: Experimental
mode: reflection
order: 16
date_created: 2026-10-05
date_modified: 2026-10-05
authors:
  - Michael Staton
augmented_with:
  - Claude Code on Claude Opus 5.5
tags:
  - Contracts
  - Interfaces
---
## What it is

Docs in `context-v/contracts/`, in two flavors:

1. **Constitution contracts:** rules an agent must always follow, regardless of task or model.
2. **Interface contracts:** exact schemas, payload shapes, and ownership boundaries for data moving through a system.

## Why

A blueprint explains how a system is designed. A reminder corrects drift. A contract defines the boundary of acceptable behavior. Mixing them dilutes the ones that must hold.

## How

- Keep them few. A contract that's often broken isn't one.
- Where a harness supports it, back a constitution rule with a hook. Prose is followed most of the time; a hook, every time.
