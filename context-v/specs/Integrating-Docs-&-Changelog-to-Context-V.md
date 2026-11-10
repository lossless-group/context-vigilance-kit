---
type: Specs
title: "Integrating Docs & Changelog to Context-V"
description: "Spec for docs-v and changelog-v: optional docs and changelog folders that run on the context-v system across a repo and its submodules."
lede: "Docs stay docs and changelogs stay changelogs, now with the same frontmatter, wikilinks, search, and templates as context-v."
publish: false
date_created: 2026-11-02
date_modified: 2026-11-10
date_authored_initial_draft: 2026-11-02
date_authored_current_draft: 2026-11-10
date_authored_final_draft:
authors:
  - Michael Staton
augmented_with:
  - Claude Code on Claude Opus 5.5
at_semantic_version: 0.0.1.0
status: Draft
tags:
  - Context-Vigilance
  - Documentation
  - Changelogs
  - Pseudomonorepos
  - Scaffolding
summary: "Defines docs-v and changelog-v as opt-in surfaces of the kit. docs-v splits into user-docs, agent-docs and api-docs, is kept current by agents as an ongoing duty, and is served live at a path or subdomain by a Starlight site rendered through LFM in the product's branding (decided 2026-11-10, reversing the earlier no-Starlight call). Read this before changing init, new, reflect, the frontmatter hook, the corpus ingesters, or the splash roll-up to handle docs. First adopters: LFM's docs-v (user docs) and a realtime data API repo's api-docs."
site_uuid: 75141b57-0b2c-4a4f-986d-826fc70714cd
hex_code: 79jehl
---

# Integrating Docs & Changelog to Context-V

## Why care?

Most projects end up with three kinds of writing: `context-v/` for building the thing, docs for using it, and a changelog for what changed. Today only the first gets the full system. Docs have no shared shape, can't be searched from the vector database, and don't link cleanly to the specs behind them.

`docs-v/` and `changelog-v/` close that gap. New projects can choose them when they're set up. Agents treat them exactly as they would treat ordinary docs and a changelog, with the context-v twists on top: standard frontmatter, wikilinks, vector search, common templates, and roll-up across a family of submodules.

LFM's `docs-v/` is the first real one, created 2026-11-02.

**Revised 2026-11-10 (Michael).** Four changes to the first draft:

1. **`docs-v/` has three parts:** `user-docs/`, `agent-docs/` and `api-docs/`. API docs come first in practice: a realtime data API (game-day ingestion and updates over pub/sub) is about to get its own repo, and its docs need to exist from day one.
2. **Turning docs-v on gives agents a standing duty** to keep the docs true, not just a folder.
3. **Starlight is the default renderer**, run through LFM and dressed in the product's own branding. This reverses the first draft's call; the reasons it gave are kept below as the risks to manage.
4. **Docs are served live,** at a path or a subdomain of the product, from the first doc.

The kit ships the Lossless frontmatter standard with all of it. A project can change it, but nobody has to design one.

## Goals

- `docs-v/` and `changelog-v/` come with the kit as options the user selects, individually or together.
- `docs-v/` is split by reader: `user-docs/` and `api-docs/`, each turned on separately, plus an experimental `agent-docs/`.
- Once docs-v is on, agents keep it current as part of every change, without being asked.
- Docs are live on the web, at a path (`example.com/docs`) or a subdomain (`docs.example.com`), in a Starlight site that renders LFM and matches the product's branding.
- New projects get the Lossless frontmatter standard by default, editable per project.
- Anyone starting a docs or changelog folder is prompted to put it on the same system.
- Agents follow ordinary docs and changelog conventions, plus the twists listed under [The twists](#the-twists).
- Nested submodules with these folders count as one family of efforts.

## Non-goals

- **No renames needed.** An existing `docs/` or `changelog/` is already the same folder, so nothing has to move.
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

### The docs-v layout

```
docs-v/
  index.md          # the front page of the docs site
  user-docs/        # people using the product: step by step, assuming nothing
  api-docs/         # how the API works: endpoints, events, auth, errors
  agent-docs/       # experimental, off by default: the same product, written for agents
    openapi.yaml    # HTTP endpoints (OpenAPI 3.1), the source of truth for the reference
    asyncapi.yaml   # pub/sub channels and event payloads (AsyncAPI 3), when the API has them
  site/             # the Starlight app that serves all of it (see Serving)
```

- Each part is optional; `init` asks which ones. A product with no API has no `api-docs/`.
- **The parts differ by reader, and so by how they're written:**
  - **`user-docs/`** are for a person who knows nothing: one small step at a time, what they'll see after each, nothing assumed.
  - **`api-docs/`** say how the API works, plainly and completely: every endpoint and event, its inputs, outputs and errors. No hand-holding.
  - **`agent-docs/`** exist because agents need different information, at different lengths, than people do: denser, more complete, less narrative (an `llms.txt`, full reference in one file, task recipes). It's uncommon and unproven, so it's **experimental and off by default**; `init` doesn't offer it unless asked. Builder context still lives in `context-v/`.
- **`api-docs/` keeps the machine-readable spec files as the source of truth.** Reference pages are generated from them; the hand-written pages are the guides around them (authentication, first request, subscribing to events, rate limits, errors). For a pub/sub API, AsyncAPI is to channels and events what OpenAPI is to endpoints.
- A flat existing `docs/` is read as user docs until someone sorts it. Nothing moves on its own.

### Agents keep docs current

Turning docs-v on (`/cv:init`, or later with `/cv:docs`) writes `docs.maintain: true` to `context-v/config.md`. From then on, in that repo:

- **Same change, same commit.** A change that alters what a user, an agent or an API caller would see (a setting, a screen, an endpoint, an event, a payload, an error) updates the affected doc in the same change. An agent that can't tell says so in its summary rather than skipping it.
- **API spec first.** Adding or changing an endpoint or event updates `openapi.yaml` or `asyncapi.yaml` along with the code; the reference pages follow from it.
- **`/cv:reflect` checks for drift:** docs untouched while the code they describe changed, routes or channels in the code that aren't in the spec files, and pages that link to something removed. It reports them as a list and fixes what's in scope.
- **The site stays live.** A docs build that fails is treated like a failing test: fixed before the work is called done.

The duty lives in the `context-vigilance` skill and `starters/AGENTS.snippet.md`, so it works in any agent, not just one with hooks.

### What stays conventional

- **Docs** describe current behavior for a reader who wants to get something done. When behavior changes, the doc changes. A doc doesn't narrate its own history or explain internal debates. Those belong in the changelog and `context-v/`.
- **Changelogs** record what changed for the reader, by date. A correction is added as a dated note instead of silently rewriting the entry. The `changelog-conventions` skill remains the authority on entries and adds only the frontmatter below.
- **The README** stays a short front door that links into `docs-v/`.

### The twists

**Frontmatter.** The kit ships the Lossless standard as the default, the same one `context-v/` uses, refined over two years of use. A project can add or drop fields in `context-v/config.md` (`docs.frontmatter`), and templates and the check follow that. Both surfaces use the context-v baseline: `title`, `lede`, `publish`, the date fields, `authors`, `augmented_with`, `site_uuid`, `hex_code`, and `tags`. The existing rules apply, including plain-text ledes of 140 characters or fewer and IDs minted by command. Only these fields differ:

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

### Serving: Starlight, rendered through LFM, live

**Decided 2026-11-10 (Michael): every docs-v is served by a [Starlight](https://starlight.astro.build) site by default.** Starlight is Astro's docs framework, which fits a stack of Astro and Svelte: sidebar, search, page chrome and navigation come built, so a project gets a real docs site on day one instead of hand-building one per splash. A project can still choose another renderer; the source stays plain Markdown with frontmatter, so nothing about `docs-v/` depends on Starlight.

What the agent sets up and then maintains:

- **The site lives in `docs-v/site/`,** a small Astro app with Starlight, reading `user-docs/`, `agent-docs/` and `api-docs/` through a content loader pointed outside `src/` (the splashes already read `changelog/` and `context-v/` this way). Starlight's docs schema is extended with the frontmatter fields, all optional, never hard-validated.
- **LFM renders the Markdown.** `remarkLfm` (and the LFM rehype steps) are added to the Astro Markdown pipeline Starlight uses, so wikilinks, callouts, citations and code fences behave as on every other Lossless site. LFM elements that need components are mapped to Starlight-styled ones. Starlight's Expressive Code and LFM's `/highlight` both want code blocks: pick one per site and switch the other off.
- **The product's branding, not Starlight's.** The agent reads the product's `DESIGN.md` (or its theme CSS) and maps its tokens onto Starlight's CSS custom properties: colours, fonts, radius, logo, favicon. Light and dark map directly; any third mode (vibrant) is added as a custom theme. When the product's design changes, the docs theme is updated in the same change, under the same duty as the docs themselves.
- **API reference from the spec files.** OpenAPI pages are generated by a Starlight OpenAPI plugin; AsyncAPI pages by a plugin or a small generator if none fits (to check at Phase 4).
- **`llms.txt` from `agent-docs/`** is published at the site root, so agents find it where they look.

**Live at a path or a subdomain,** chosen at setup and recorded in `context-v/config.md`:

```yaml
docs:
  maintain: true
  parts: [user-docs, agent-docs, api-docs]
  url: https://example.com/docs      # or https://docs.example.com
  renderer: starlight
```

| | Path (`example.com/docs`) | Subdomain (`docs.example.com`) |
|---|---|---|
| Wiring | Starlight's `base: '/docs'`, plus a rewrite on the product's host that forwards `/docs/*` to the docs deployment | A separate deployment of `docs-v/site/` with its own domain and a DNS record |
| Good for | One product, one domain, shared sign-in pages linking back and forth | An API product, or several apps sharing one docs site |
| Watch for | The rewrite must keep assets and search working under `/docs` | Cookies and analytics are a separate site |

Either way the agent: deploys the docs site from the same branch tier as the product; links the docs from the product (nav, footer, API responses' error links where useful); checks after each deploy that a live page shows its body text, not just a 200; and keeps the sitemap, OG image and `llms.txt` current.

**Risks the first draft raised, still true:**

| Risk | How it's handled |
|---|---|
| Starlight has its own Markdown pipeline and code highlighter | LFM plugged into the Astro Markdown config; one highlighter per site |
| Theming fights two-tier tokens and three modes | Map Tier-2 tokens onto Starlight's variables; add the third mode as a custom theme; test all modes |
| Starlight's Astro version can trail or lead a site's | The docs site is its own app with its own `package.json`, so it upgrades on its own schedule |
| One more thing to keep upgraded | It's part of the agent's maintenance duty, and the dependency-upgrade loop covers it |

The first draft's analysis is in `astro-knots/context-v/prompts/Discuss-how-to-Publish-Long-Form-like-eBook.md`.

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

### Phase 4: The Starlight site

A `docs-v/site/` starter in `starters/`: Starlight, LFM in the Markdown pipeline, the frontmatter schema, the branding map from `DESIGN.md`, OpenAPI and AsyncAPI reference, `llms.txt`, and recipes for path and subdomain serving. A new skill (`docs-v`) covers setting it up and the ongoing duty.

**Done when:** in a scratch Astro and Svelte product with a `DESIGN.md`, `/cv:init` with docs-v on produces a live docs site, at a path on one deployment and at a subdomain on another, where a page shows its body text, a working wikilink and an LFM callout in the product's colours and fonts in every mode, and an `openapi.yaml` endpoint and an `asyncapi.yaml` channel each have a reference page. Checked by reading the live pages' text, not their status codes.

### Phase 4b: The duty

Write the maintenance duty into `context-vigilance`, `reflect` and `AGENTS.snippet.md`, with the drift check.

**Done when:** in the scratch product, an agent asked to add an endpoint also updates `openapi.yaml` and the guide without being told; `/cv:reflect` after a code-only change to a documented route reports the drift.

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
- [ ] A product with docs-v on has a live, branded Starlight docs site at its chosen path or subdomain, rendering LFM.
- [ ] An API repo's `api-docs/` has reference pages generated from its OpenAPI and AsyncAPI files.
- [ ] Agents update the docs in the same change as the behaviour, and `/cv:reflect` reports drift.

## Open questions

- [ ] **What shape should `agent-docs/` take?** Kept experimental (2026-11-10): agents clearly need information at different lengths and densities than people, but there's no settled pattern yet. Revisit when a project actually wants one.
- [ ] **AsyncAPI in Starlight:** is there a maintained plugin, or does the kit ship a small generator? Check at Phase 4.
- [ ] **Default: path or subdomain?** The draft asks every time. An API-first repo probably wants a subdomain (`api-docs.example.com` or `docs.example.com`); an app probably wants `/docs`.

- [ ] **Do wikilinks stay in docs that people read on GitHub?** GitHub shows `[[Page]]` as literal text, and `docs-v/` is what the LFM README links people to. Recommendation: use wikilinks in `context-v/` and `changelog-v/`, and relative Markdown links in `docs-v/`, which Obsidian and the LFM renderer both handle. This narrows "wikilinks all around", so it's Michael's call.
- [ ] **Should tools that expect standard names get a pointer?** Some tools look for `CHANGELOG.md` or `docs/`. A short `CHANGELOG.md` pointing to `changelog-v/` may be enough.

## Related

- [[decisions/Context-V-Is-an-OKF-Profile|Context-V Is an OKF Profile]]
- [[specs/Survey-a-Scoped-Dashboard-of-Context-V|Survey: a Scoped Dashboard of context-v]]
- [[specs/Commands-and-Agent-Skills-for-Context-V|Commands and Agent Skills for context-v]]
- The `pseudomonorepos` skill and its `references/content-rollup.md`
- The `changelog-conventions` and `maintain-splash-pages` skills
- `lfm/docs-v/index.md`, the first adopter
