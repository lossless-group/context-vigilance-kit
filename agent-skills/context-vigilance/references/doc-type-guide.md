# Which `context-v/` Folder? A Decision Guide

**Contents:** Quick decision tree · Folder-by-folder · Common confusions · When two folders both fit

Use this when the right folder isn't obvious. There are eight canonical folders (`specs/`, `plans/`, `prompts/`, `blueprints/`, `reminders/`, `agent-skills/`, `explorations/`, `issues/`), two universal utility folders (`extra/` for gitignored scratch, `sitemap/`), and an experimental tier (`loops/`, `handoffs/`, `decisions/`, `habits/`, `contracts/`) that some projects use.

Filenames are Train-Case: `Maintain-Embeddable-Slides.md`, `Auth-Session-Refresh-Spec.md`.

## Quick decision tree

```
Do you know what you're trying to build?
├── No → research / weigh tradeoffs?          → explorations/
└── Yes
    ├── Defining what & why & scope           → specs/
    ├── Sequenced work plan (roadmap,
    │   plan-mode output, migration)          → plans/
    ├── Step-by-step prompts referencing
    │   a spec or plan                        → prompts/
    ├── Codifying a pattern / architecture    → blueprints/
    ├── Short correction AI keeps needing     → reminders/
    ├── Executable know-how for agents
    │   (SKILL.md shape)                      → agent-skills/
    └── Documenting a debugging journey       → issues/
```

## Folder-by-folder

### `specs/`: living specifications

**Yes, if:** it defines what something is, why it exists, and what it does; prompts will reference it; it's kept current as the system evolves; multiple people or sessions treat it as the source of truth.

**No, if:** it's a one-time implementation plan (→ `plans/` or `prompts/`), a pattern observation rather than a thing being built (→ `blueprints/`), or still being figured out (→ `explorations/`).

### `plans/`: sequenced work

**Yes, if:** it orders work over time: a roadmap, a migration, the output of an agent's plan mode, a phased rollout.

**No, if:** it defines what to build (→ `specs/`) or is one executable chunk an agent follows top to bottom (→ `prompts/`).

### `prompts/`: step-by-step implementation docs

**Yes, if:** it's a structured plan to implement one chunk of a spec or plan, broken into discrete, verifiable steps an agent could follow top to bottom.

**No, if:** it's a single chat message you copy-pasted (ephemeral, don't commit it), it defines what rather than how (→ `specs/`), or it's a research scratchpad (→ `explorations/`).

### `blueprints/`: codified patterns

**Yes, if:** it explains how part of the system works (architecture, data flow, naming), future contributions should follow it, and it captures the "why we do it this way."

**No, if:** it's a project being built (→ `specs/`) or a one-line correction (→ `reminders/`).

### `reminders/`: battle scars turned into guardrails

**Yes, if:** it's short (often one paragraph), exists because an AI made the same mistake repeatedly, and gets loaded when an agent starts drifting.

**No, if:** it's longer than ~10 lines with structure, or explains a system rather than correcting behavior (→ `blueprints/`).

### `agent-skills/`: executable know-how

**Yes, if:** it's a `SKILL.md`-shaped package an agent loads to do a recurring task the project's way.

**No, if:** it's an explanation for humans (→ `blueprints/`).

### `explorations/`: journeys without a known destination

**Yes, if:** the answer isn't known when you start; you're surveying options, weighing tradeoffs, or thinking out loud. Ending with "we don't need this" is a valid outcome.

**No, if:** you already know the answer (→ spec or blueprint) or it's a debugging session (→ `issues/`).

### `issues/`: issue resolution journeys

**Yes, if:** it captures the path through a painful, non-obvious bug, including red herrings and the eventual root cause, so nobody retraces the trail.

**No, if:** the fix was an obvious one-liner (just commit), or it's general advice on avoiding bugs (→ `blueprints/`).

## Common confusions

| Confusion | Resolution |
|---|---|
| Spec vs. blueprint | Specs describe **what is being built**. Blueprints describe **how the existing system works**. |
| Spec vs. plan | A spec is the *what & why*. A plan is the *order of work* to get there. |
| Prompt vs. exploration | Prompt = "execute this plan." Exploration = "figure out what the plan should be." |
| Reminder vs. blueprint | Reminder is a sharp correction. Blueprint is the underlying explanation. A reminder often *links to* a blueprint. |
| Issue vs. exploration | Issues have a defined goal (fix the thing). Explorations have an open question. |

## When two folders both fit

Pick the one the document's *primary* reader needs:

- "Future me trying to implement something" → planning mode (`specs/`, `plans/`, `prompts/`)
- "Future me trying to understand the system" → reflective mode (`blueprints/`, `reminders/`, `agent-skills/`)
- "Future me trying not to retrace my steps" → journey mode (`explorations/`, `issues/`)

When still tied, ask the user.
