# Bringing an existing context-v/ into compliance

**Contents:** When to use this · What compliant means · The two rules that matter most · Phase 1: OKF · Phase 2: the frontmatter template · Status decisions · Things that look wrong but aren't · Across many repos

A repo that has had a `context-v/` for a while won't match the current conventions: docs without a `type`, folders without an `index.md`, statuses nobody can group by. This is the method for fixing that without breaking anything, proven on a sweep of 60-plus bundles.

## When to use this

- The `upgrade` skill's check found differences and the user said yes.
- Someone asks to "make context-v OKF compliant", "fix the frontmatter", or "clean up the statuses".
- A survey or dashboard shows untyped docs or unmapped statuses.

Never as a side effect of other work: the drift policy applies. A sweep is something the user asks for.

## What compliant means

A `context-v/` bundle is compliant when:

1. **Every doc declares `type`**: the folder's name in Train-Case (`specs/` → `Specs`, `narratives/` → `Narratives`). A folder README that has frontmatter counts as a doc; a plain README doesn't. See `okf.md`.
2. **The bundle root has `index.md`** with `okf_version: "0.2"`, and **every folder has an `index.md`**, one line per doc: `* [Title](File.md) - text`, the text being the description, else the lede, else nothing.
3. **Baseline frontmatter is filled from facts**: `title`, `date_created`, `date_modified`, `authors`, `site_uuid`, `hex_code` (see `frontmatter-spec.md`).
4. **`status` is on the vocabulary and true** (see `status-discipline.md`).
5. **Values are normalized**: list fields are lists, tags and statuses are Train-Case, tags are topics (not repo or package names), placeholder dates are empty.
6. **Nothing renders an index as a page**: any site or splash that loads `context-v/` skips `index.md`.

Docs sitting directly in the bundle root, outside every folder, aren't typed: list them and file them in a folder later.

A repo's root `README.md` isn't part of the bundle. If it has frontmatter (or gets some), its `type` is `Repo-Readme`, the same in every repo. GitHub renders frontmatter as a table above the README, so keep it to the baseline identity keys.

## The two rules that matter most

- **Edit by hand, one file at a time, frontmatter only.** Read the file, make the edit, read the diff. Never let a script write a `.md` file and never round-trip frontmatter through a YAML library: either one reorders keys, collapses multi-line ledes, or re-quotes values, and a small parser difference can break a static-site build or an Obsidian vault across hundreds of files at once. Scripts may *read* (scan, count, grep, git log); they never write docs.
- **A compliance change is not a content change.** Never write today's date into an existing doc: don't bump `date_modified`, the draft dates, or the version. Never touch a body line. Never flip `publish`. Never delete a key you don't recognize.

## Phase 1: OKF (one commit)

- [ ] Add `type:` (folder name, Train-Case) to every doc without one, as one added line. Correct a `type` that doesn't match its folder (`type: issue` in `issues/` becomes `Issues`).
- [ ] Type folder READMEs that have frontmatter, and list them in their folder's index.
- [ ] Write the root `index.md` (`okf_version: "0.2"`, one line per folder) and one `index.md` per folder. Keep an existing index's shape; make sure it lists every doc.
- [ ] If a site loads `context-v/` into pages, make its loader skip `index.md`, and build to prove it.
- [ ] Read the whole diff: it should be only added `type:` lines, new index files, and any loader change.
- [ ] Run the conformance check in `okf.md`. No output means done.
- [ ] Changelog entry, then commit.

## Phase 2: the frontmatter template (a second commit, only if something changed)

**Add missing keys, from facts only:**

| Key | Fact it comes from |
|---|---|
| `title` | the doc's H1 |
| `date_created` | `date_authored_initial_draft`, else the file's first commit |
| `date_modified` | the file's last commit before the sweep (not today) |
| `authors` | the only human committer, in the byline spelling the repo already uses |
| `site_uuid`, `hex_code` | minted by command, one pair at a time, each `hex_code` searched for across the tree before use |

Don't add `lede`, `description`, `publish`, or `augmented_with` values: those need a human reading.

**Normalize, and only these:**

| Found | Becomes |
|---|---|
| `version:` (with no `at_semantic_version`) | `at_semantic_version:`, same value, after checking no code reads `version` |
| a bare string in `authors`, `augmented_with`, `tags` | a one-item list, the string unchanged |
| lowercase or kebab-case tags and statuses | Train-Case |
| a package or tool name in `tags` that isn't the doc's subject | removed (mention it in the body if it's absent) |
| a repo name in `tags`, where the body already names the repo | removed |
| a status written as a tag (`Draft`, `Stub`) | removed; `status:` carries it |
| `"[]"` in a date key | an empty value, key kept |

Leave alone: a quoted date (it parses the same), `semantic_version:` (a permanent alias), author spelling variants, and every key you don't recognize.

**Statuses:** see the next section.

## Status decisions

`status-discipline.md` has the vocabulary and a table of common variants. Apply it like this:

1. **Plain renames** (`In-Progress` → `Implementing`, `Authoritative` → `Active`): just change them.
2. **Everything else off the list, and any on-list value the repo contradicts**: decide by evidence, not by queueing a question. Read the doc, then check git log and the code. A plan marked `Draft` whose work is in the commits isn't `Draft`; an issue marked `Open` that a commit fixed is `Resolved`.
3. **Pick the family by what the doc is.** Issues are `Open`/`Resolved`; decisions `Decided`; reminders, habits, contracts, standing loops `Active`; explanations, profiles, sitemap pages `Reference`; consumed handoffs `Archived`; explorations are planned work (`Draft`, never `Open`).
4. **Add the companion field only with evidence.** `Shipped` and `Partially-Shipped` get `date_first_published` from the commit that shipped the work; `Deferred` gets a `deferral_note` in the doc's own words; `Superseded` gets `superseded_by` when the doc names its successor. If there's no clean date, leave the field out rather than guess.
5. **Write the reason in the commit message**, with the commit hash that's the evidence.

A doc with no `status` gets one when its kind makes it obvious (a reminder is `Active`, a profile is `Reference`) or the evidence does.

## Things that look wrong but aren't

- **Frontmatter that is live data.** Some docs keep data a site renders (deck narratives with slide content in their frontmatter, for example). Type and index them, but add nothing else: a new key there lands in a page.
- **A legacy key a site still reads** (`date:` read by a splash's date picker). Don't rename it until the reader changes.
- **`Partially-Shipped` without `## Remaining work`.** The section is a body edit, so a sweep doesn't write it. The doc's own status notes carry it until someone next works on it.
- **A doc's `date_modified` older than its last commit.** Leave it: the field is filesystem-ish and the sweep doesn't correct history.

## Across many repos

- **Only sweep a repo whose branches agree.** If `development`, `main`, and `master` (or whatever the repo's tiers are) point at different commits, bring them to one line first, or sweep only the branch the repo actually lives on, and say so.
- **Commit any uncommitted work in the checkout first** as its own commit, except secrets and nested repos, so the sweep sits on top of it.
- **Work in a scratch worktree, then push all tiers at once** (`git push --atomic origin HEAD:development HEAD:main HEAD:master`), then fast-forward the local branches so nobody has to pull. If the push is rejected because someone else pushed, re-apply on the new tip; never force.
- **Each agent mints its own IDs** at the moment it writes them. A shared pool of pre-minted IDs puts the same pair into two repos.
- **Bump the parent's submodule pointer** once each child is pushed, and only to commits that are on the remote.
- **Verify, don't trust.** After agents report, re-check each repo yourself: tiers equal on the remote, zero untyped docs, every status on the list, and only frontmatter lines in the diff.
