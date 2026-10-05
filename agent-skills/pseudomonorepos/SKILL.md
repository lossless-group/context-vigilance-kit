---
name: pseudomonorepos
description: "Recognizes and navigates \"pseudomonorepos\", parent repos that aggregate child repos (often as git submodules) mainly to host a shared parent-level context-v/ folder, as opposed to a true monorepo with a shared build. Use when working in a directory tree of nested repos or submodules, when starting a task that might overlap with prior specs, plans, or docs elsewhere in the tree, when scaffolding a new project and deciding where it belongs, when keeping submodule branches aligned, or when the user mentions \"pseudomonorepo\", \"submodule\", \"parent repo\", or \"context-v\". Always use it when the user proposes to move, relocate, re-clone, or re-nest a repo: that triggers a mandatory three-precondition safety checklist (local branches synced, remote branches catalogued, gitignored secrets backed up)."
---

# Pseudomonorepos

> Not a true monorepo, and not a loose folder of repos either. A parent repo that holds
> children (often as git submodules) mainly so the parent can host a `context-v/`
> that carries context *across* them.

## Contents

- When to use this skill
- The behavioral core: search before creating
- What a pseudomonorepo looks like
- Universal directories
- Relocating a repo (HARD STOP checklist)
- Branch alignment across submodules
- Pointer bumps are a wrap-up activity
- Lifecycle and content roll-up
- Drift policy
- Typical flow when starting a task
- Reference files

Degrees of freedom used below: **open** = use judgment; **shaped** = default
pattern, deviate with a stated reason; **exact** = one right answer, do not improvise.

## When to use this skill

- The working directory sits inside a tree of nested git repos, or the repo has a
  `.gitmodules` file and a `context-v/` folder.
- A task (code, spec, prompt, debugging) might overlap with prior work elsewhere in the tree.
- Scaffolding a new sub-project: where does it go, and does it deserve its own level?
- Deciding whether to add a folder as a submodule or inline.
- The user wants to move, rename, re-clone, or re-nest a repo. See the HARD STOP below.

Adopters may never have heard the word "pseudomonorepo." Recognize the shape anyway
(see [references/anatomy.md](references/anatomy.md)) and explain it in a sentence
when it helps.

## The behavioral core: search before creating (shaped)

Before writing a new spec, plan, prompt, blueprint, doc, or substantial code:

1. **Walk the tree up.** Find every ancestor directory that has a `context-v/`.
2. **Search prior work** in each of those `context-v/` folders (and siblings', when
   relevant): filenames, content, frontmatter tags.
3. **Surface what you find.** For example: "I see related work in
   `acme-platform/context-v/blueprints/Image-Pipeline.md` and
   `acme-platform/web/context-v/specs/Upload-Flow.md`. Extend, link, or write new?"
4. **Cross-reference, don't duplicate.** Link to prior work (wikilinks or relative
   links). Restating without linking is a smell.

Recipes for each step are in [references/search-first.md](references/search-first.md).

### Escape hatch: ship fast (open)

Searching sometimes costs more than the task is worth. When the user says "just ship it":

- Say plainly that you are skipping the search.
- Ship.
- Leave a one-line refactor-debt marker (in the file's frontmatter or in
  `context-v/issues/`) naming keywords to search later.
- Never claim you searched when you didn't.

Speed is allowed; amnesia is not.

## What a pseudomonorepo looks like

```
acme-platform/                # parent repo
├── .gitmodules               # children referenced as submodules (sometimes)
├── context-v/                # PARENT-level context spanning the children
│   ├── specs/  plans/  prompts/  blueprints/
│   ├── reminders/  explorations/  issues/  agent-skills/
│   └── extra/ (gitignored)  sitemap/
├── changelog/                # parent-level ship log
├── web/                      # child repo with its own context-v/ + changelog/
├── api/                      # child repo with its own context-v/ + changelog/
└── docs/                     # child; could itself be a pseudomonorepo (nesting)
```

Each level is authoritative for its own scope. Children own their internals; the
parent owns the *space between* children (cross-cutting specs, shared blueprints,
decisions that touch more than one child).

Nesting is normal: a root pseudomonorepo can hold themed pseudomonorepos, which hold
true monorepos (npm/pnpm workspaces, Cargo workspaces), which hold packages. Not every
project sits at every level. **Walk up until you stop finding `context-v/`** before
concluding there's no prior context.

How to identify one, how it differs from a true monorepo, and when to create a new
level: [references/anatomy.md](references/anatomy.md).

## Universal directories (shaped)

Every repo level (parent, true monorepo, single project) ideally has two siblings at its root:

| Directory | Purpose |
|---|---|
| `context-v/` | Living documentation. Its folder roles and frontmatter come from the `context-vigilance` skill. |
| `changelog/` | Ship log: dated records of what changed and when. |

Some projects nest `changelog/` inside `context-v/`. Respect existing placement; only
normalize when asked. When scaffolding a new repo at any level, create both at the root.

## Relocating a repo: HARD STOP (exact)

Moving a repo from one parent path to another (e.g. `acme-platform/labs/search/` to
`acme-platform/api/services/search/`) is the riskiest routine operation in a
multi-repo tree. The usual method (re-clone at the new path, delete the old directory)
silently destroys whatever was never pushed: local-only branches, unpushed commits,
uncommitted edits, stashes, and gitignored `.env` / secrets files. Moves like this have
destroyed un-pushed branches and the only copy of a project's `.env` file.

**Do not go along with a relocation until all three preconditions are verified and
the user has acknowledged each one separately.** One acknowledgment per precondition,
never a bundled "looks good, proceeding." Bundled confirmations are how things get lost.

Run these inside the repo that is about to move. Copy the checklist into your reply
and tick it as you go:

```
Relocation preconditions for <repo>:
- [ ] 1. Every local branch is synced to its remote
- [ ] 2. Every local-only branch is pushed or declared disposable
- [ ] 3. Every gitignored secret has a confirmed backup
```

**Precondition 1: local branches synced.**

```bash
git fetch --all --prune
git branch -vv                                  # look for [ahead N] and [gone]
git log --branches --not --remotes --oneline    # commits that exist only locally
git status                                      # uncommitted changes
git stash list                                  # parked work
```

- → If any branch shows `[ahead N]`, stop: push it, or get explicit sign-off that it can be lost.
- → If the `--not --remotes` query prints anything, stop: those commits exist nowhere else.
- → If the working tree is dirty, stop: commit and push, or get sign-off to discard.
- → If any stash exists, stop: apply and commit it, or get sign-off to drop it.

**Precondition 2: remote branches catalogued.**

```bash
git ls-remote --heads origin    # the authoritative remote list
git branch -a                   # local + remote-tracking
diff <(git branch --format='%(refname:short)' | sort) \
     <(git ls-remote --heads origin | sed 's|.*refs/heads/||' | sort)
```

- → If a local branch has no remote counterpart, stop: push it, or have the user name it as disposable.
- → Also note which branch is the real tip (most recent work). The new clone must check
  out that branch, not just the remote default.

**Precondition 3: gitignored secrets backed up.**

```bash
cat .gitignore
find . -maxdepth 3 \( -name '.env*' -o -name '*.local' -o -name '.secrets*' -o -name 'secrets' \) \
  -not -path '*/node_modules/*' 2>/dev/null
```

Then list the variables the source code actually reads (recipes for several languages
in [references/relocation-safety.md](references/relocation-safety.md)). `.env.example`
is not authoritative; it lags behind the code.

- → If any `.env*` / secrets file exists and the user hasn't named where a recoverable
  copy lives (password manager, hosting provider's env panel, a backup outside the
  directory), stop.
- → If the code reads variables missing from both `.env` and `.env.example`, list them to the user.

Only after three separate acknowledgments: move, then verify the new clone (right
branch checked out, secrets restored, project builds) **before** deleting the old directory.

A ready-to-adapt message for the user, plus recovery steps for when a move already
went wrong: [references/relocation-safety.md](references/relocation-safety.md).

## Branch alignment across submodules (shaped)

When a parent tracks children as submodules, it helps if each repo uses the same
branch names for the same purpose, and the parent and its children sit on the same
tier at the same time. One workable model (an example, not a requirement) is three tiers:

- `development`: where most work lands
- `main`: promoted from `development` when something noteworthy is ready
- `master` (or `stable`): updated only once the dust settles

Whatever the team uses, the rules that matter:

- Record each submodule's tracked branch in `.gitmodules` (`branch = ...`), then run
  `git submodule sync`. An entry with no `branch =` line is a smell.
- When a submodule's working branch is *behind* the leading branch, fast-forward it
  forward rather than rolling the parent's gitlink backward.
- Never promote between tiers (e.g. development to main) on your own; promotion is a human decision.
- Don't realign branches as a side effect of unrelated work. Observe, report, get authorization.

Fast-forward mechanics, divergence checks, and creating a missing tier:
[references/branch-alignment.md](references/branch-alignment.md).

## Pointer bumps are a wrap-up activity (shaped)

Every commit inside a submodule makes the parent's gitlink show as modified
(` M <child>`). Bumping the parent after every child commit doubles the commit count
and buries the parent's history in "pointer moved" noise.

| When | What |
|---|---|
| During the session | Commit and push freely in the child. Leave the parent's gitlink dirty. |
| At wrap-up | Bump every moved pointer once, in a single commit such as `chore(submodule): bump web, api`. |

A dirty gitlink mid-session is expected, not an error; don't report it as a finding.
**Exception:** if other people pull the same parent, bump sooner. A stale pointer gives
their clone a child commit that doesn't match what you said you shipped.

## Lifecycle and content roll-up (open)

Work tends to move up the tree: framed in a project's `context-v/`, logged in the
project's `changelog/`, lifted into the parent's `context-v/` once it becomes a
cross-cutting pattern, announced in the parent's `changelog/`, and optionally
published somewhere public. The five-phase loop and when to skip phases:
[references/lifecycle-workflow.md](references/lifecycle-workflow.md).

A parent's docs site or changelog page can **roll up** its children's `changelog/` and
`context-v/` into one feed, tagged with which child each entry came from. Two
mechanisms (local filesystem vs. GitHub Contents API) and their tradeoffs:
[references/content-rollup.md](references/content-rollup.md).

## Drift policy (exact)

Multi-repo trees are rarely tidy. Parent `context-v/` folders are often sparse, some
children are stale, branch tiers drift, READMEs lag. When walking the tree:

- **Observe, note, surface.** Mention inconsistencies you see.
- **Do not auto-fix** them as a side effect of unrelated work. Normalization is its own
  task and needs the user's go-ahead. Other people (or other agent sessions) may be
  working in the same tree, and silent cleanup breaks their work.
- Treat what you find in `context-v/` as a starting point, not a complete or current record.

## Typical flow when starting a task

1. **Locate yourself.** `pwd`, then list the ancestors that have `context-v/`.
2. **Scan** each level's `context-v/` folder names.
3. **Topic search** by 1–3 keywords across every `context-v/` under the tree's root.
4. **Report findings**, including "searched X, Y, Z; found nothing" when that's the result.
5. **Ask:** extend, link, or write new?
6. **Proceed**, applying `context-vigilance` conventions to anything you write.
7. **If shipping fast,** leave a refactor-debt marker.

## Reference files

- [references/anatomy.md](references/anatomy.md): what makes a pseudomonorepo, identification
  heuristics, submodules vs. plain folders, when to create a new level
- [references/search-first.md](references/search-first.md): walk-up and topic-search recipes,
  triaging results, refactor-debt markers
- [references/relocation-safety.md](references/relocation-safety.md): the relocation message
  template, env-var discovery per language, safe move sequence, recovery after a bad move
- [references/branch-alignment.md](references/branch-alignment.md): tier models, missing or
  lagging branches, fast-forward checks, `.gitmodules` sync
- [references/lifecycle-workflow.md](references/lifecycle-workflow.md): the Start → Progress →
  Reflect → Publish → Market loop and when to skip phases
- [references/content-rollup.md](references/content-rollup.md): aggregating children's
  `changelog/` and `context-v/` into a parent feed

Related skill: `context-vigilance` defines what goes inside each `context-v/` folder.
This skill says where to look and when to look up; that one says what the documents
should look like.
