---
title: "Hooks for the exact rules only"
lede: "A rule written in capitals is followed most of the time. A hook is followed every time, so use it sparingly."
maturity: Emerging
mode: practice
order: 20
date_created: 2026-10-05
date_modified: 2026-10-05
authors:
  - Michael Staton
augmented_with:
  - Claude Code on Claude Opus 5.5
tags:
  - Hooks
  - Enforcement
---
## What it is

A hook is a small script the agent's harness runs at a fixed moment, such as just before a file is written. It runs whether or not the agent remembered the rule, and it can block the action with a reason.

## Why

Most of this practice is judgment, and judgment can't be enforced. But a few rules have exactly one right answer, and breaking them silently breaks tools: YAML that doesn't parse, a fake UUID, an ID that changed.

## How

- Enforce only the **exact** rules. Everything else stays prose.
- Block with a message that says how to fix it.
- Never let a hook approve anything on the user's behalf.

## In the kit

The `cv` plugin ships one hook: before a write to `context-v/`, it checks that the frontmatter parses, has a title, valid dates, and well-formed, unchanged IDs.
