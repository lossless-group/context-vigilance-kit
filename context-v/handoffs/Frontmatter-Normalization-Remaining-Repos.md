---
title: "Frontmatter Normalization — Remaining Repos"
lede: "Four repos and 256 files are done; 652 files across 47 repos are not. Everything the sweep learned the hard way now lives in the two skills, so the next session can point agents at the spec instead of re-deriving the rules — but three traps are repo-specific and will bite anyone who assumes the standard applies uniformly."
publish: true
date_created: 2026-08-15
date_modified: 2026-08-15
date_authored_initial_draft: 2026-08-15
date_authored_current_draft: 2026-08-15
date_authored_final_draft:
authors:
  - Michael Staton
augmented_with:
  - Claude Code on Claude Opus 5 (1M context)
at_semantic_version: 0.0.1.0
status: In-Progress
tags:
  - Frontmatter
  - Normalization
  - Handoff
  - Context-Vigilance
  - Agent-Sweeps
  - Publish-Gate
---

# Frontmatter Normalization — Remaining Repos

## Why care?

A tree-wide audit found **461 markdown files** missing `date_created` or lacking
frontmatter entirely. Four repos have since been swept and pushed. This document
hands off the rest.

The important part is not the file list — it's the **three repo-specific traps**
below. Each was discovered by nearly breaking something, and none is inferable
from the standard.

## Current state

**Done and pushed** — 256 files across four repos:

| Repo | Files | Commit |
|---|---|---|
| `ai-labs/context-vigilance-kit` | 12 | `b5c3673` |
| `ai-labs/dididecks-ai` | 85 | `c68bd8c` |
| `ai-labs/memopop-ai/apps/memopop-orchestrator` | 100 | `e35d919` |
| `astro-knots/sites/fullstack-vc` | 58 | `d3da15f` |

**Remaining: 652 files across 47 repos** — 63 with no frontmatter at all, 61
needing a legacy key rename.

**Excluded by operator decision:** `ai-labs/augment-it` and `content/` (handled
separately). `context-v/agent-skills/` is out of scope everywhere — those are
vendored copies of the canonical skills, and `SKILL.md` frontmatter is a machine
contract Claude Code parses.

## The standard

Do not restate it from this document — **read the source**, which is now
accurate:

- `context-v/skills/context-vigilance/references/frontmatter-spec.md`
- `context-v/skills/changelog-conventions/references/frontmatter-spec.md`

Both skills auto-load in a fresh session. Point agents at those file paths as the
authority rather than pasting rules into prompts — inconsistent restatement
between batches is what produced the only real errors in this sweep.

Required keys, in brief:

| Scope | Keys |
|---|---|
| `context-v/**.md` | `date_created`, `date_modified`, `publish` |
| `changelog/**.md` | `date_authored_initial_draft`, `date_authored_current_draft`, `publish` |

## The three traps

### 1. A key rename can break a build — grep for consumers first

`date:` → `date_authored_initial_draft:` is sanctioned **for changelog entries
only**, and even then it is not universally safe.

- In `memopop-orchestrator` the rename silently degraded two Chroma ingesters
  that read `date` as a metadata field and a temporal anchor. Both were fixed.
- In `astro-knots/sites/fullstack-vc` the rename would have **failed the build
  outright**: `src/content.config.ts` declares `date: z.coerce.date()` as a
  *required* field on the changelog collection, and `src/pages/changelog/index.astro`
  reads `entry.data.date` in four places for sorting and display. That repo got a
  documented exception — `date:` stays, editorial keys are added alongside it.

**Before renaming anything in an Astro site, check `src/content.config.ts`.**
Adding keys is safe there (Zod strips unknowns; verify with `pnpm exec astro sync`).
Renaming is not.

### 2. Filesystem dates lie — `stat` is the last resort

Whole directories in this tree carry a birthtime from a bulk copy or machine
recovery rather than from authorship. Observed: ~100 changelog entries spanning
five months all reporting `created=2026-05-06`, and release-notes files reporting
the birthtime of *the day the sweep ran* while git dated them nine months earlier.

Source precedence, per the spec:

1. existing frontmatter on the file
2. a date in the filename or parent directory name
3. a date stated in the document body
4. `git log --diff-filter=A --follow --format=%ad --date=short -- <file> | tail -1`
5. `stat` — and treat the result as suspect

The tell is a uniform birthtime across files of obviously different ages.

### 3. `publish` is a judgment, and its default is repo-specific

There is **no safe tree-wide default.** Tree-wide the split runs roughly 2:1
toward `true`, but individual repos run the other way, deliberately. Count before
deciding:

```bash
grep -rh '^publish:' --include='*.md' context-v/ | sort | uniq -c
```

Two calibration points from this sweep:

- **`memopop-orchestrator` ran 47 `false` to 5 `true`.** A content-only rule
  ("real content → true") marked 26 documents publishable; a screened re-read
  kept 3. Substance and sensitivity run in the *same* direction — the meatier a
  `context-v/` doc is, the more client detail it tends to carry.
- **`fullstack-vc`'s members-only session narratives are deliberately public.**
  Participants consent; their headshots are already served by the site. Marking
  those `false` was wrong.

The rule is **genericize rather than hide**, and the document's job comes first:
if it is materially better with the specific names in it, keep them and set
`publish: false`. It stays in the repo for us. Variable and env-var *names*,
architecture, schemas, and candid post-mortems are all fine to publish.

## Suggested order

**Start here — mechanical, no publish judgment required:**

| Repo | Files | Note |
|---|---|---|
| `astro-knots/sites/dark-matter/changelog` | 29 | **All 29 are renames.** Its own nested git repo. |
| `astro-knots/sites/banner-site` | 12 | **All 12 are renames.** |

Both are rename-only, so they are the cheapest way to verify the next session's
agent briefing works before spending on judgment-heavy repos. **Check for an
Astro content collection reading `date` first** — see trap 1.

**Then by size.** Columns are: files needing work / no frontmatter / renames /
changelog / context-v.

| Repo path | Need | No-FM | Ren | CL | CV |
|---|---|---|---|---|---|
| `astro-knots` | 98 | 22 | 0 | 12 | 86 |
| `ai-labs` | 53 | 2 | 1 | 13 | 40 |
| `ai-labs/dididecks-ai/client-sites/calmstorm-decks` | 41 | 2 | 0 | 19 | 22 |
| `content-farm` | 36 | 0 | 0 | 8 | 28 |
| `self-host-stack` | 36 | 0 | 0 | 22 | 14 |
| `ai-labs/dididecks-ai/client-sites/reach-edu-hub` | 32 | 1 | 0 | 0 | 32 |
| `ai-labs/memopop-ai` | 31 | 6 | 0 | 4 | 27 |
| `astro-knots/sites/dark-matter/changelog` | 29 | 0 | 29 | 29 | 0 |
| `content-farm/plugin-modules/perplexed` | 29 | 4 | 2 | 19 | 10 |
| `content-farm/plugin-modules/cite-wide` | 23 | 4 | 0 | 12 | 11 |
| `.` (lossless-monorepo root) | 23 | 4 | 0 | 0 | 23 |
| `ai-labs/dididecks-ai/client-sites/chroma-decks` | 21 | 3 | 0 | 7 | 14 |
| `ai-labs/studies/memory-layers-for-agents` | 18 | 0 | 0 | 0 | 18 |
| `content-farm/plugin-modules/image-gin` | 16 | 1 | 8 | 10 | 6 |
| `ai-labs/corpora-builder` | 15 | 0 | 0 | 2 | 13 |
| `ai-labs/studies/open-specs-and-standards` | 14 | 0 | 0 | 0 | 14 |
| `astro-knots/sites/banner-site` | 12 | 0 | 12 | 12 | 0 |
| `ai-labs/studies/agent-harnesses` | 11 | 0 | 0 | 0 | 11 |
| `ai-labs/id-didi-sh` | 10 | 0 | 0 | 7 | 3 |
| `context-v/skills` | 10 | 0 | 0 | 10 | 0 |
| `lfm` | 9 | 0 | 4 | 9 | 0 |

The remaining 26 repos are 8 files or fewer each — 88 files total. Worth batching
several small repos into one agent once the pattern is proven.

**Note the client-site repos.** `calmstorm-decks`, `reach-edu-hub`,
`chroma-decks`, `humain-vc-decks`, `lossless-decks` and `eventcut-ai` are named
client engagements. Apply the confidentiality screen there with the same care
`dididecks-ai` needed — that sweep moved 34 of 66 documents to internal.

## Operational notes

- **Edit originals, never rollups.** `context-vigilance-kit/corpus/`,
  `astro-knots/sites/lossless-changelog/src/stream/` and `splash/src/rollup/` are
  derived. A naive `find` for a repo name will surface the corpus copy first —
  resolve paths through `sources.md` or the changelog walker instead.
- **Stage path-scoped.** Every repo swept so far had unrelated dirt — submodule
  pointers, lockfiles, untracked scripts. `git add -A` would have committed
  moved submodule pointers.
- **A mid-flight `publish` correction cannot be delegated.** The permission
  classifier blocks a subagent from flipping `false` → `true` on relayed
  authority, correctly. Whoever holds the operator's actual instruction must
  apply those edits directly.
- **Known spec defect:** *"never flip `publish` false → true"* cannot distinguish
  a standing decision from a value the current sweep wrote minutes earlier. It
  wants an explicit carve-out for values written by the running sweep.

## Known issues surfaced, not fixed

These change existing values rather than adding keys, so each needs its own
directed pass:

- **Broken ledes.** Seven were repaired by hand in `memopop-orchestrator`. More
  exist: `lede: "---"` where an extractor captured a horizontal rule, ledes
  truncated mid-sentence on the period inside `e.g.`, and six files whose `title`
  is `"Summary"` or `"Overview"` taken from the first `##`. A lede is written,
  never extracted — see the spec.
- **`summary:` used where `lede:` belongs** across most of `fullstack-vc`'s older
  changelog entries. There is no `summary` field in the standard.
- **Three `memopop-orchestrator` entries dated 2025-04 appear to be 2026 entries**
  with a year typo propagated from filename into frontmatter. Fixing means
  renaming files.
- **Credential values committed:** `dididecks-ai/context-v/reminders/Auth-Loose-Ends.md`
  carries plaintext passcodes and a production database hostname. `publish: false`
  does not fix that — those want rotating.
- **Two unfixed access-control weaknesses** described in
  `dididecks-ai/context-v/specs/Calmstorm-Auth-Inventory.md`. Engineering bugs,
  not disclosure settings.

## See also

- [[Graphiti-Over-The-Lossless-Corpus]] — the other thread in this session; the
  frontmatter work directly improved its temporal anchors (undated changelog
  entries fell from 77 to 26).
- `context-v/skills/context-vigilance/references/frontmatter-spec.md`
- `context-v/skills/changelog-conventions/references/frontmatter-spec.md`
