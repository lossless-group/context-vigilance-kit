# Developing a Spec

**Contents:** When to follow this · The rhythm (locate, stub, prior art, discuss-write-discuss, stale prior art, sign-off gate, pair with prompts) · Status values for specs · Anti-patterns

How to *develop* a spec with the user as a rhythm, not a single write-once act. Specs are the most discussion-heavy doc-type in `context-v/` and the one most likely to go off the rails into "spend 90 minutes editing a doc instead of building." This rhythm avoids that. It's scoped to specs; other doc-types have their own rhythms.

## When to follow this

- The user wants to build something non-trivial and there's no spec yet
- The user says "let's spec this", "draft a spec", "before we build", or similar
- You're about to start implementation that lacks a documented "what & why"
- A new project, package, or major feature is starting

## The rhythm (numbered, not rigid)

### 1. Locate the right `context-v/`

Walk up from the working directory to the nearest `context-v/`. If the repo sits inside a larger parent (a monorepo, or a parent repo holding several child repos as submodules) that has its own `context-v/`, the spec **may belong in the parent's `context-v/specs/`**, especially if it spans several children or starts a new one. Ask the user if it's not obvious.

### 2. Drop a stub, then return to discussion

**Create the file early with frontmatter only**, then *stop editing it* and keep talking.

```yaml
---
title: "Working title (will be revised)"
lede: "One-clause hook, under 140 characters, that makes a reader want to keep reading."
date_created: YYYY-MM-DD
date_modified: YYYY-MM-DD
authors:
  - User Name
augmented_with:
  - Claude Code on Claude Opus 5.5
at_semantic_version: 0.0.0.1
site_uuid: <generate with uuidgen, see frontmatter-spec.md>
hex_code: <generate with tr, see frontmatter-spec.md>
tags:
  - Spec
status: Draft
---

# Working title

<!-- developing -->
```

One H1, one HTML comment as a placeholder. Filename in Train-Case (`Auth-Session-Refresh.md`). Generate `site_uuid` and `hex_code` with a command, never by typing them (see `frontmatter-spec.md`).

**About the `lede`:** specs often end up published, where the lede is the only line a reader sees in a list view, preview card, or social unfurl before deciding to click. Write it as a *hook*, not a description: **140 characters maximum, target 90–130.** If it swells into a paragraph, that material belongs in a `## Why Care?` section in the body. `description` is accepted as an alternate field name; `lede` is preferred because the word signals the job.

**Why stub-first:** the file existing makes it findable by other agents and future-you. The empty body means you haven't committed to a structure prematurely. Discussion shapes the structure.

### 3. Receive prior art generously

The user will share `context-v/` files, code, or links as prior art. **Don't fret about its quality.** It may be outdated, stub-shaped, inconsistently named, or overlapping with other docs. That's normal: docs drift faster than they converge. Read prior art for **signal, not gospel**, and ask when something is ambiguous rather than reverse-engineering intent in silence.

### 4. Discuss → write → discuss

The dialog drives the spec. As discussion produces clarity, **append** without trying to make it narratively clean:

- Add sections (`## Goals`, `## Non-goals`, `## Constraints`, `## Phases`) as topics arise
- Add bullets as decisions get made
- Leave `// TBD` markers where consensus hasn't formed
- Don't reorder, don't rewrite for flow, don't polish prose

In chat, **summarize what just got captured in one line** rather than re-pasting the evolving doc. The user can open the file.

### 5. Handle stale prior art (the "intern" pattern)

If a prior-art `context-v/` file no longer reflects what the user is now saying, surface it:

> "The blueprint at `[[Some-Blueprint]]` says X, but you just described Y. Want to update that file too?"

If yes, the ideal is to **delegate the update to a background agent**, an "intern" that revises the stale doc as relevant content surfaces and returns only for decisions. That keeps the primary dialog on the new spec. Approximate it with whatever your tool supports:

- **If a parallel agent is feasible** (a subagent, a second session, another terminal): hand it the stale file and a brief on what's changing. Surface its output at natural pauses.
- **If not:** keep a running `## Stale prior art to update later` list inside the spec, noting which files need revision and in what direction. Batch the updates after sign-off.

Either way, **don't let stale-doc cleanup hijack the spec dialog.**

### 6. The sign-off gate

**Hard gate (exact):** do not start implementation prompts or code until the user says some version of "spec is good, let's build" ("approved," "ship it," "go," "looks good, proceed").

When the user signs off:

1. Set `status: Signed-Off`.
2. Update `date_modified` and bump `at_semantic_version` (typically to `0.0.1.0` or `0.1.0.0`; see `versioning.md`).
3. **Now** do the narrative pass: re-read the whole doc and revise for clarity, flow, and audience (the user, a future agent, an outside reader). Reorder sections, tighten prose, resolve `// TBD` markers or move them to `## Open questions`. Before sign-off, polish is wasted effort against a moving target.
4. Confirm the cleaned-up version with the user.

### 7. Pair the spec with prompts

A **spec** says *what & why*. A **prompt** says *how*, step by step, for one chunk of execution.

If the spec has Phases, Steps, Milestones, or any natural chunking, **pre-load matching prompts in `context-v/prompts/`** before implementation. One prompt per chunk. Each prompt:

- Has a `## Spec reference` linking back (`[[../specs/My-Spec]]`)
- Names the chunk it implements (Phase 1, Step 3, etc.)
- Lists verifiable success criteria for that chunk
- Can be invoked by pasting it, or by telling an agent "load this prompt," instead of re-explaining from scratch

If chunking isn't obvious at sign-off, write the prompt for the first chunk, ship it, and write the next when you get there.

## Status values for specs

Status is a Train-Case **display string, not a machine enum**; don't switch on it in code. (See `status-discipline.md` for the full lifecycle and companion fields.)

| Value | Meaning |
|---|---|
| `Draft` | Stub exists, frontmatter only or minimal body. Default for new specs. |
| `In-Discussion` | Actively being shaped through dialog (`In-Review` is an accepted equivalent). |
| `Signed-Off` | User explicitly approved; narrative pass done; ready for prompts. |
| `Implementing` | One or more prompts are executing this spec. |
| `Shipped` | Implementation complete; the spec is now reference. |
| `Stale` | No longer current thinking. Revise it or supersede it. |
| `Superseded` | Replaced. Pair with `superseded_by: [[New-Spec]]`. |

These are conventions, not enforced. If a project uses different values, respect them.

## Anti-patterns

- **Polishing the spec while still discussing.** Wait for sign-off.
- **Letting stale prior-art cleanup take over the dialog.** Note it, defer it, or delegate it.
- **Starting implementation before sign-off.** Even small implementation choices encode spec assumptions.
- **One giant prompt for a multi-phase spec.** Chunk it.
- **Pasting the whole evolving spec back every turn.** Summarize the change in one line.
- **Reverse-engineering intent from prior art when the user is right there.** Ask.

See also: `frontmatter-spec.md` (fields), `doc-type-guide.md` (spec vs. plan vs. prompt), `versioning.md` (bumps), `philosophy.md` (why).
