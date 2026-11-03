---
type: Specs
title: "Integrating Docs & Changelog to Context-V"
description: "Spec for docs-v and changelog-v: optional docs and changelog folders that run on the context-v system across a repo and its submodules."
lede: "Docs stay docs and changelogs stay changelogs, now with the same frontmatter, wikilinks, search, and templates as context-v."
publish: false
date_created: 2026-11-02
date_modified: 2026-11-02
date_authored_initial_draft: 2026-11-02
date_authored_current_draft: 2026-11-02
date_authored_final_draft:
authors:
  - Michael Staton
augmented_with:
  - Claude Code on Claude Opus 5.5
at_semantic_version: 0.0.0.2
status: Draft
tags:
  - Context-Vigilance
  - Documentation
  - Changelogs
  - Pseudomonorepos
  - Scaffolding
summary: "Defines docs-v and changelog-v as opt-in surfaces of the kit. Read this before changing init, new, reflect, the frontmatter hook, the corpus ingesters, or the splash roll-up to handle docs. It also records why Starlight isn't part of the base system. LFM's docs-v folder is the first adopter."
site_uuid: 75141b57-0b2c-4a4f-986d-826fc70714cd
hex_code: 79jehl
---

# Integrating Docs & Changelog to Context-V

## Why care?

Most projects end up with three kinds of writing: `context-v/` for building the thing, docs for using it, and a changelog for what changed. Today only the first gets the full system. Docs have no shared shape, can't be searched from the vector database, and don't link cleanly to the specs behind them.

`docs-v/` and `changelog-v/` close that gap. New projects can choose them when they're set up. Agents treat them exactly as they would treat ordinary docs and a changelog, with the context-v twists on top: standard frontmatter, wikilinks, vector search, common templates, and roll-up across a family of submodules.

LFM's `docs-v/` is the first real one, created 2026-11-02.

## Goals

- `docs-v/` and `changelog-v/` come with the kit as options the user selects, individually or together.
- Anyone starting a docs or changelog folder is prompted to put it on the same system.
- Agents follow ordinary docs and changelog conventions, plus the twists listed under [The twists](#the-twists).
- Nested submodules with these folders count as one family of efforts.

## Non-goals

- **No renames needed.** An existing `docs/` or `changelog/` is already the same folder, so nothing has to move.
- **No site framework in the base system.** See [Starlight](#starlight-not-in-the-base-system).
- **No database in the kit.** The kit stays database-free; vector search lives in `context-v-corpus`.
- **No versioned docs.** A guide describes the current release.
- **No adopting vendored or third-party docs.** Their folders are never touched or indexed.

## Constraints and assumptions

- **Two skill copies exist.** `context-vigilance-kit/agent-skills/` and `lossless-agent-skills/` have diverged, and sessions on this machine load the second. Rule changes go in both.
- **Tools hardcode `changelog`.** `ingest-changelogs-to-chroma.py`, `rollup-sync.ts`, the splash loaders, `init`, and `reflect` all assume that name, and each needs to read both spellings. A crude count finds 134 directories named `changelog` in the tree, including vendored code.
- **The kit installs into any agent.** The rules must work from skills and `AGENTS.md` alone. Hooks are only a backstop.

## Design

### Three surfaces, one system

| | `context-v/` | `docs-v/` or `docs/` | `changelog-v/` or `changelog/` |
|---|---|---|---|
| Means | Living project context | Docs | Changelog |
| Reader | Builders and their agents | People using the thing | Anyone following along |
| Answers | What are we building, and why? | How do I use it now? | What changed, and when? |
| Lifecycle | Drafts move through statuses | Edited to stay true | Dated, and not rewritten after publishing |
| Files | Train-Case, by doc type | Named by topic | `YYYY-MM-DD_NN.md`, plus `releases/` |

**`docs-v` and `docs` are the same thing, and so are `changelog-v` and `changelog`.** Every agent, check, ingester, and roll-up reads both spellings identically. The spelling is only a preference. What makes a folder part of this system is the conventions below, not its name.

### What stays conventional

- **Docs** describe current behavior for a reader who wants to get something done. When behavior changes, the doc changes. A doc doesn't narrate its own history or explain internal debates. Those belong in the changelog and `context-v/`.
- **Changelogs** record what changed for the reader, by date. A correction is added as a dated note instead of silently rewriting the entry. The `changelog-conventions` skill remains the authority on entries and adds only the frontmatter below.
- **The README** stays a short front door that links into `docs-v/`.

### The twists

**Frontmatter.** Both surfaces use the context-v baseline: `title`, `lede`, `publish`, the date fields, `authors`, `augmented_with`, `site_uuid`, `hex_code`, and `tags`. The existing rules apply, including plain-text ledes of 140 characters or fewer and IDs minted by command. Only these fields differ:

| Field | Docs | Changelog |
|---|---|---|
| `type` | `Docs` | `Changelog`, including in `releases/` |
| `at_semantic_version` | Yes, tracks the doc | No, entries aren't revised |
| `applies_to_version` | Optional: the package version it describes | Not used |
| `files_changed` | Not used | Recommended, as today |

`type` is the same for both spellings: `docs/` and `docs-v/` both give `Docs`. Subfolders don't change it. This is a deliberate exception to context-v's rule that `type` is the folder's name.

**OKF.** Each folder is an OKF bundle with an `index.md`, the same as `context-v/`.

**Wikilinks.** Links use the style in `context-v/config.md` and run in every direction: a changelog entry links to the guide, the guide to its spec, and the spec back to its changelog entry. Files that get published outside the repo, like a README on JSR, use full URLs.

**Publish boundary.** A published doc can link to a private one, but the link must render as plain text. LFM's path resolver already handles an unresolved link this way. Private titles can still leak through the display text, so publishing a doc includes reading its links.

**Templates.** The kit adds these to `context-vigilance/templates/`:

| Template | Sections |
|---|---|
| `doc-guide.md` | What you'll do, steps, troubleshooting |
| `doc-reference.md` | What it is, options or API, examples |
| `changelog-entry.md` | Why care?, what changed, known gotchas, what's next |
| `changelog-release.md` | Highlights, upgrade notes |

The template sections are shaped defaults, so drop any that don't apply.

**The check.** The frontmatter hook's scope grows to all four spellings in any repo with a `context-v/`. As in `context-v/`, it holds new files to the rules without making existing files fail over fields they never had. Repos with no `context-v/` are never checked.

**Vector search.** `context-v-corpus` indexes both surfaces, in either spelling:

| Surface | Collection | Shape |
|---|---|---|
| Docs | New `lossless-docs` | Section-chunked, like `context-vigilance-corpus` |
| Changelog | Existing `lossless-changelog` | One file per document, as today |

Each record keeps `source_repo_slug`, `type`, `publish`, `site_uuid`, and `hex_code`. Vendored folders are excluded because they're outside the [family](#pseudomonorepo-family), never because of how a folder is spelled. The query skill and both `CLAUDE.md` files move from four collections to five.

### Prompting

**During `/cv:init`:** one question replaces the current `changelog/` offer. "Also set up docs and a changelog on this system?" The options are both, `docs-v/` only, `changelog-v/` only, or neither.

**When someone starts a folder later:** before creating a docs or changelog folder in a repo with `context-v/`, under either spelling, the agent asks whether to run it on this system. The rule lives in the skills and `AGENTS.snippet.md`. A hook can act as a backstop on the first write to a new folder.

**When a docs or changelog folder already exists:**

It's already the same folder, so it's read and indexed as one, and new files follow the conventions. Nothing needs renaming. Frontmatter on old entries isn't backfilled automatically; that stays a deliberate sweep.

The choice is stored in `context-v/config.md`, so nobody is asked twice:

```yaml
surfaces:
  docs: docs-v            # the folder's spelling: docs-v | docs, or none
  changelog: changelog-v  # the folder's spelling: changelog-v | changelog, or none
```

### Pseudomonorepo family

**A family is a parent repo and its nested submodules.** The `pseudomonorepos` skill's rules extend to these folders:

- **Search the family first.** Before writing a doc, look in this repo, then its parents and siblings. Link to what exists rather than writing a second copy.
- **The source stays in the child.** A child owns its own docs and changelog. A parent's `docs-v/` covers only what cuts across children, and links down to the rest.
- **Choices inherit.** `init` in a child starts from the nearest parent's `surfaces`, and the child can override them.
- **Wikilinks cross repos.** A repo-qualified link such as `[[lfm/docs-v/wikilinks|Wikilinks]]` resolves against an index of the whole family. `site_uuid` stays unique across it.
- **Roll-up reads both spellings.** `pnpm rollup:sync` copies docs and changelogs into `splash/src/rollup/`, with `from` and `from_path` provenance. Either spelling lands in the same feed.
- **Survey counts them.** `/cv:survey` includes both surfaces beside `context-v/`.
- **Pointers bump at wrap-up,** in one commit, as today.

**Who isn't in the family:**

- Collaborator mounts and `studies/`, which are read-only.
- Vendored submodules, such as those in `self-host-stack/core/`.
- For public roll-up, `client-sites/` and any repo not provably public. `rollup-sync.ts` already fails closed on those, and `private: true` and `publish: false` files stay excluded.

A repo can opt out with `family: false` in its `context-v/config.md`.

### Starlight: not in the base system

**`docs-v/` stays plain Markdown, and the existing splash renders it through LFM.** Starlight is a site framework, while `docs-v/` is a source format, so nothing about the format should depend on it.

Read from Starlight's docs on 2026-11-02, and not run:

| Question | Finding | Effect |
|---|---|---|
| Can it read `docs-v/`? | Its default setup reads `src/content/docs`. Our splashes already use custom loaders to read `changelog/` and `context-v/` from outside `src/` | Not an obstacle |
| Does it accept our frontmatter? | Only `title` is required, and the schema is extendable | Workable |
| Does it run LFM? | It has its own Markdown pipeline, with Expressive Code for code blocks | Plugin wiring, and a second code highlighter beside `/highlight` |
| Does it fit our sites? | Earlier analysis found a theming fight with two-tier tokens and three modes | Overhead per site |
| Is the version stable? | Its own site runs Starlight 0.42.8 on Astro 7.4, and LFM's splash is on Astro ^6.3.1 | Another upgrade to track |

The earlier analysis reached the same conclusion for long-form content. See `astro-knots/context-v/prompts/Discuss-how-to-Publish-Long-Form-like-eBook.md`.

The splash needs a docs collection, pages rendered through LFM, a sidebar built from `docs-v/index.md`, and Pagefind, which splashes already use.

**Revisit this if** a project needs versioned docs or translations, or if the sidebar and page chrome become a real maintenance cost across several sites. Because the source stays plain Markdown with a `title`, a Starlight site could be added later as an optional renderer without changing the format.

## Phases

Each phase can ship on its own.

### Phase 1: The convention

Write the rules into both skill copies, add the templates, and bring LFM's `docs-v/` up to them. LFM's files currently lack `type: Docs`.

**Done when:** every file in `lfm/docs-v/` except `index.md` has `type: Docs`, and `grep -l docs-v` finds the rule in `context-vigilance` and `changelog-conventions` in both skill copies.

### Phase 2: Scaffolding and prompting

Update `init`, `new`, `upgrade`, `reflect`, `starters/`, and `config.md`.

**Done when:** in a scratch repo, `/cv:init` offers all four choices and creates what's selected, `/cv:new doc "Title"` passes the check, and asking for a docs folder under either spelling triggers the prompt once. After declining, a second request doesn't prompt.

### Phase 3: The check

Extend `hooks/check-frontmatter.py`.

**Done when:** tests show a new file with no `type` is blocked identically under all four spellings, an existing file's unrelated edit isn't blocked, and a repo with no `context-v/` is never checked.

### Phase 4: Rendering

Add docs pages to LFM's splash, then document the pattern in `maintain-splash-pages`.

**Done when:** a live `docs-v` page on LFM's splash shows its body text and a working wikilink, in a check of the page's text rather than its status code.

### Phase 5: Vector search

Add a docs ingester and `changelog-v` discovery, and update `ingest-all.sh`.

**Done when:** a dry run lists `lfm/docs-v/` and a family repo's `docs/`, lists no vendored folder, and after a real ingest, a query about Mermaid rendering returns `lfm/docs-v/code-fences.md`. The user runs the real ingest.

### Phase 6: The family

Extend `rollup-sync.ts`, survey, and cross-repo wikilink resolution.

**Done when:** a child's `changelog-v/` entry and a child's `changelog/` entry appear in one parent feed, a repo-qualified wikilink resolves on a live page, and a private fixture repo appears nowhere in the output.

## Acceptance criteria

The spec is shipped when all of these are true:

- [ ] A new project can select either surface, both, or neither during `/cv:init`.
- [ ] Starting a docs or changelog folder under either spelling prompts once, and the answer is remembered.
- [ ] Agents and tools treat `docs-v/` and `docs/` identically, and `changelog-v/` and `changelog/` identically.
- [ ] No existing folder needs renaming, and no existing file fails a check over fields it never had.
- [ ] Both surfaces are searchable in the corpus.
- [ ] A parent splash shows its children's docs and changelogs, with no private content.

## Open questions

- [ ] **Do wikilinks stay in docs that people read on GitHub?** GitHub shows `[[Page]]` as literal text, and `docs-v/` is what the LFM README links people to. Recommendation: use wikilinks in `context-v/` and `changelog-v/`, and relative Markdown links in `docs-v/`, which Obsidian and the LFM renderer both handle. This narrows "wikilinks all around", so it's Michael's call.
- [ ] **Should tools that expect standard names get a pointer?** Some tools look for `CHANGELOG.md` or `docs/`. A short `CHANGELOG.md` pointing to `changelog-v/` may be enough.

## Related

- [[decisions/Context-V-Is-an-OKF-Profile|Context-V Is an OKF Profile]]
- [[specs/Survey-a-Scoped-Dashboard-of-Context-V|Survey: a Scoped Dashboard of context-v]]
- [[specs/Commands-and-Agent-Skills-for-Context-V|Commands and Agent Skills for context-v]]
- The `pseudomonorepos` skill and its `references/content-rollup.md`
- The `changelog-conventions` and `maintain-splash-pages` skills
- `lfm/docs-v/index.md`, the first adopter
