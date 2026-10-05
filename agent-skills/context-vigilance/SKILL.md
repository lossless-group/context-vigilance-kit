---
name: context-vigilance
description: Manages a project's context-v/ folder, the living documentation that humans and agents share (specs, plans, prompts, blueprints, reminders, explorations, issues, agent-skills, plus extra/, sitemap/, and the experimental loops/, handoffs/, decisions/, habits/, contracts/). Use whenever creating, editing, or organizing any file under a context-v/ folder, choosing which folder a doc belongs in, writing doc frontmatter, or when the user asks about context engineering, AI co-development workflow, or "context-v". Covers folder roles, frontmatter, four-part versioning, status lifecycle, and cross-linking.
---

# Context Vigilance

**Treat context with the same vigilance as code.** Agents don't remember between sessions, and people forget too. So each repo keeps a `context-v/` folder: what we're building and why, how the system is designed, what went wrong and how it was fixed. Written so that the user, a future agent session, and a stranger can each pick up where the work left off.

**Norms, not rules.** Most of this is judgment. Be generous reading existing files (they may predate these norms, or be experiments) and careful writing new ones. The parts that have exactly one right answer are marked **exact** below; see *Degrees of freedom*.

**Drift policy.** When you find inconsistencies (odd frontmatter, off-pattern filenames, half-adopted conventions), **note them and tell the user. Don't fix them as a side effect of other work.** People run several agent sessions at once, and silent cleanup collides with their work.

## Contents

- [The folders](#the-folders) · [Which folder?](#which-folder) · [Degrees of freedom](#degrees-of-freedom)
- [Frontmatter](#frontmatter) · [Status](#status) · [Writing the doc](#writing-the-doc)
- [Creating a doc: checklist](#creating-a-doc-checklist) · [Templates](#templates) · [References](#references) · [Related skills and tools](#related-skills-and-tools)

## The folders

**Prep: deciding what to build** (highest altitude first)

- **`specs/`**: what we're building and why. Living, updated as decisions change. The source of truth that plans and prompts point at.
- **`plans/`**: sequenced, scoped work, closer to execution than a spec. Plan-mode output belongs here so it doesn't vanish when the session ends.
- **`prompts/`**: step-by-step implementation documents (not single chat messages), each step verifiable before the next.

> A prompt without a spec is a vibe. A prompt within a spec is engineering.

**Reflective: how the system works**

- **`blueprints/`**: patterns, architecture, and the reasoning behind them: what an agent must respect to fit in.
- **`reminders/`**: short corrections born from mistakes an agent keeps making ("we don't use X; use Y").
- **`agent-skills/`**: skills specific to this repo (`<name>/SKILL.md`), born next to the code they serve.

**Journey: finding out**

- **`explorations/`**: the destination is unclear: research, options, tradeoffs. Ends when you know enough to write a spec, or decide you don't need one.
- **`issues/`**: the winding path through a hard problem, wrong guesses included, so nobody retraces it. (If the team uses a ticket system, see the `tracker` role in `context-v/config.md`.)

**Utility, any project**

- **`extra/`**: scratch, pasted transcripts, not-yet-docs. **Gitignored**: add `context-v/extra/` to `.gitignore` when scaffolding.
- **`sitemap/`**: what exists where: pages, routes, endpoints, screens, so an agent doesn't have to crawl the source.

**Experimental: shape not settled; expect variation and don't normalize it**

- **`loops/`**: recurring processes written down so an agent runs them the same way each time (scope, per-iteration steps, exit conditions).
- **`handoffs/`**: end-of-session state for the next session: what landed, what's mid-flight, what to load first.
- **`decisions/`**: the moment a decision was made: what, when, by whom, alternatives passed over.
- **`habits/`**: recurring maintenance with a trigger and a scope ("keep the README true", "sweep stale statuses monthly").
- **`contracts/`**: things that must never be violated: standing rules for agents, or exact data and API interfaces.

**Found a folder that isn't listed?** Don't fight it. Read it, work out which mode it serves, and ask the user whether to keep it, fold it into an existing folder, or promote it to a convention. When unsure, keep it.

## Which folder?

- What to build, with scope and criteria → `specs/`
- Ordered work toward it → `plans/`
- Step-by-step execution with checks → `prompts/`
- How or why the system is designed → `blueprints/`
- A correction the agent keeps needing → `reminders/`
- Know-how an agent should load and follow → `agent-skills/`
- Don't know yet; weighing options → `explorations/`
- Debugging something painful → `issues/`
- Scratch → `extra/` · What exists where → `sitemap/`
- A recurring process → `loops/` · State for the next session → `handoffs/` · A decision → `decisions/` · Recurring upkeep → `habits/` · Inviolable rules → `contracts/`

More detail: [references/doc-type-guide.md](references/doc-type-guide.md).

## Degrees of freedom

Every step in this practice sits at one of three levels. Match your rigor to the level.

| Level | Meaning | In this practice |
|---|---|---|
| **open** | Judgment. Several good answers. | Writing explorations and the body of any doc; naming next steps; whether to fork a long doc |
| **shaped** | A template or pattern is the default; departing is fine with a reason | Doc structure (the templates); which folder; changelog entries; loop docs |
| **exact** | One right answer. Don't improvise. | Frontmatter key names and formats; minted IDs; filenames in Train-Case; dates as `YYYY-MM-DD`; the four-part version |

Written-down loops in `loops/` record the level a team chose for each step of their own process.

## Frontmatter

New docs start with this baseline. When editing, **respect what's there**: never delete a key you don't recognize, and don't add keys without a reason.

```yaml
---
title: "Human-readable title"
lede: "One hook line, 140 characters max."
publish: false
date_created: 2026-10-05
date_modified: 2026-10-05
date_authored_initial_draft: 2026-10-05
date_authored_current_draft: 2026-10-05
date_authored_final_draft:
authors:
  - Jane Doe
augmented_with:
  - Claude Code on Claude Opus 5.5
at_semantic_version: 0.0.0.1
status: Draft
tags:
  - Train-Case-Tag
site_uuid: 3f1c9a2e-7b4d-4e8a-9c1f-2d6b8e0a5c47
hex_code: k3x9q2
---
```

**Exact:**

- **Property names are `snake_case`.** Dates are `YYYY-MM-DD`.
- **`site_uuid` and `hex_code` are minted once, by a command, and never changed.** Never type one; models produce UUID-shaped strings that aren't valid.
  - `site_uuid`: `uuidgen | tr 'A-Z' 'a-z'` (or `python3 -c "import uuid; print(uuid.uuid4())"`)
  - `hex_code`: `LC_ALL=C tr -dc 'a-z0-9' </dev/urandom | head -c6`
- **`at_semantic_version` is four-part `epoch.major.minor.patch`**, starting at `0.0.0.1`. `semantic_version` is an accepted alias; never rewrite a file just to change which name it uses. See [references/versioning.md](references/versioning.md).
- **`authors` is humans only**, always a list. Agents go under `augmented_with`.
- **Tags and status values are Train-Case** (`Issue-Resolution`, `In-Review`).

**Shaped and open:**

- **`date_modified`** moves on every edit. **`date_authored_current_draft`** and the version move only on a *substantive* revision. Leave an empty `date_authored_final_draft` empty until the doc really is final.
- **`publish`** is a decision, not a default. Never flip an existing value; decide it on a new file by reading the finished doc. Prefer genericizing sensitive specifics over hiding a whole doc.
- **`lede`** says why someone would care, in one line of 140 characters or less. If it wants to grow, put the long version in a `## Why care?` section under the title. Write it after reading the doc; never extract it. A stub gets no lede.
- **`summary`** (optional) is for agents: what the doc is *for* and what it unblocks.

**The `cv` plugin's hook** checks only the **exact** basics before a write to `context-v/` (outside `extra/`): the YAML parses, `title` exists, the two dates are valid and in order, `site_uuid` and `hex_code` are well-formed and unchanged. New files need all five fields; older files are checked only for the fields they have. If it blocks a write, fix what it names and retry. Full field reference: [references/frontmatter-spec.md](references/frontmatter-spec.md).

## Status

`status` says where a doc is in its life, and it has to be true. A folder of `Draft` plans, half of which shipped, can't be trusted.

`Draft` → `In-Review` → `Signed-Off` → `Implementing` → `Shipped` · `Partially-Shipped` · `Deferred` · `Stale` · `Superseded` · `Archived`

Fields that move with it:

- **`Shipped`**: set `date_first_published`.
- **`Partially-Shipped`**: add `## Remaining work (as of YYYY-MM-DD)` listing what's done and what's left.
- **`Deferred`**: add `deferral_note`.
- **`Superseded`**: add `superseded_by: "[[Successor-Doc]]"`.

Change status when something real happened (shipped, deferred, superseded), never as tidying, and ask before changing a doc someone else owns. Details: [references/status-discipline.md](references/status-discipline.md).

## Writing the doc

- **Lead with why, for an outsider.** The first paragraph should make sense to someone with no context. Technical depth comes later.
- **Fork early.** When you notice yourself scrolling past sections to reach the one that matters, split: the pattern into a blueprint, the build into a spec, a debugging trail into an issue, each linked from the parent. The parent keeps the map; children carry the detail. See [references/philosophy.md](references/philosophy.md).
- **Cross-link.** `[[Wikilinks]]` (best if the folder is opened in Obsidian), relative Markdown links, or backtick paths: whichever serves the reader. Prompts link their spec; reminders link their blueprint; plans link their spec.
- **Filenames are Train-Case:** `Payment-Retry-Policy.md`.
- **Specs have a rhythm**: stub first, discuss then write, sign-off gate before building. Load [references/developing-a-spec.md](references/developing-a-spec.md) whenever starting or developing a spec with the user.

## Creating a doc: checklist

Copy this into your reply and tick as you go:

- [ ] Found the right `context-v/` (walk up from the current folder; a repo can have several)
- [ ] Read two or three sibling docs to match tone and frontmatter
- [ ] Picked the folder (decision list above)
- [ ] Started from the matching template
- [ ] Minted `site_uuid` and `hex_code` by command; filled dates, author, `augmented_with`
- [ ] Wrote the why first; linked related docs
- [ ] Re-read the frontmatter: it parses, and nothing like `YYYY-MM-DD`, `AUTHOR`, or `GENERATE` is left
      → if anything is left or it doesn't parse, fix it before saying you're done
- [ ] Worked through the template's own "Done when" list, if it has one

## Templates

Start every new doc from its template in `templates/`. Each one ends with a "Done when" list for that kind of doc.

- [templates/spec.md](templates/spec.md)
- [templates/plan.md](templates/plan.md)
- [templates/prompt.md](templates/prompt.md)
- [templates/blueprint.md](templates/blueprint.md)
- [templates/reminder.md](templates/reminder.md)
- [templates/exploration.md](templates/exploration.md)
- [templates/issue.md](templates/issue.md)
- [templates/loop.md](templates/loop.md)
- [templates/handoff.md](templates/handoff.md)

## References

Load the one you need; each stands alone.

- [references/doc-type-guide.md](references/doc-type-guide.md): each folder in depth, with edge cases
- [references/frontmatter-spec.md](references/frontmatter-spec.md): every field, date families, IDs, sensitivity
- [references/status-discipline.md](references/status-discipline.md): the lifecycle and when to move it
- [references/versioning.md](references/versioning.md): four-part versions and when to bump which part
- [references/developing-a-spec.md](references/developing-a-spec.md): the spec rhythm, from stub to sign-off
- [references/philosophy.md](references/philosophy.md): why the practice works the way it does

## Related skills and tools

- **Workflow skills in this kit:** `init` (scaffold), `new` (create a doc; shortcuts `explore`, `spec`, `plan`, `prompt`, `blueprint`, `remind`, `issue`, `handoff`), `kickoff` (load context at session start), `prep` (explore → spec → plan), `implement` and `loop` (build), `reflect` (close out, hand off, ship).
- **`pseudomonorepos`**: when the project is a tree of repos, each with its own `context-v/`.
- **Optional companions** (see the kit's `DEPENDENCIES.md`): if `graphify-out/GRAPH_REPORT.md` exists, read it before scanning folders. It's a map of the codebase. Archify draws diagrams checked against the repo. The Chroma skills cover semantic search over `context-v/`. Use them when present; never require them.
- **`context-v/config.md`**, if present, says which tools fill roles like `tracker`, `chat`, and `docs`. Without it, everything stays in `context-v/`.
