# context-vigilance-kit

> Treat context files with the same vigilance as code, and *context becomes the code* — or the parent to it. Regenerating code, fixing bugs, refactoring, even migrating across languages or tech stacks — work that used to take days, weeks, or months — compresses to minutes.
>
> Generating a fully-featured splash page — search, three viewing modes, coherent theme CSS, full markdown rendering — now takes **5 minutes**. Only with context vigilance.

Tooling for the **Context Vigilance** practice — collating, indexing, and eventually publishing the `context-v/` directories scattered across [The Lossless Group](https://github.com/lossless-group) tree (and beyond) as a single, queryable corpus. Brand site: [contextvigilance.com](https://contextvigilance.com) (forthcoming). Scope, rationale, and decision history live in the parent exploration: [[Collate-Context-Files-into-Context-Vigilance-as-Repo-&-Project]] (under `ai-labs/context-v/explorations/`).

## Corpus state — May 2026

First full pass over the curated `sources.md`:

| metric | count |
|---|---:|
| total files | **787** |
| `worked-on` (≥500 content lines) | 138 |
| `idea-started` (100–499 content lines) | 353 |
| `stub` (<100 content lines) | 296 |
| without YAML frontmatter | 100 |

The *without YAML frontmatter* row is **orthogonal** to the three buckets — a file lands in exactly one bucket (by `content_lines`) and is *separately* tagged as missing frontmatter (`yaml_lines == 0`). The 100 frontmatter-less files are scattered across all three buckets; a doc can be `worked-on` and still be missing its frontmatter.

**Publishing strategy.** Ship the 138 `worked-on` docs first while building a systematic, agent-assisted process to fill out the 296 stubs and 353 idea-started entries. The corpus manifest is the gate that makes this triage tractable — re-run `python scripts/build-corpus-manifest.py` after every fill-out batch to track progress against this baseline.

## What's in here (v0)

```
context-vigilance-kit/
├── README.md                          ← you are here
├── sources.md                         ← curated list of source dirs (generated, then human-curated)
├── corpus-manifest.md                 ← per-file triage view (yaml & content line counts; auto-generated)
├── skills-manifest.md                 ← agent-skills inventory; tracked separately from corpus
├── scripts/
│   ├── assemble-context-v-sources.py  ← walks the tree, populates sources.md
│   ├── build-corpus-manifest.py       ← reads sources.md, emits per-file inventory with bucket labels
│   ├── build-skills-manifest.py       ← reads sources.md, inventories context-v/skills/* per source
│   └── collate.py                     ← reads sources.md, copies files into corpus/ with provenance
├── context-v/                         ← this kit's own specs/plans/etc. (rolled up by ai-labs splash)
└── corpus/                            ← collated output (gitignored; outside the splash rollup boundary)
```

## Quickstart

Run from the kit directory after dependencies are installed (handled at the `ai-labs/` root via `python-requirements.txt`):

```bash
# 1. Walk the tree and discover context-v/ directories.
#    First run creates sources.md; subsequent runs preserve curation and append new finds.
python scripts/assemble-context-v-sources.py

# 2. Open sources.md, flip `include: true` on entries you want, add notes,
#    add legacy/open-call directories by hand with `kind: legacy` (with `subdirs:`)
#    or `kind: open-call`.

# 3. Build the pre-collation manifest. Counts yaml-frontmatter and content lines
#    per file, buckets each into stub / idea-started / worked-on. Use it to triage
#    what needs agent fill-out BEFORE you commit to a corpus build.
python scripts/build-corpus-manifest.py

# 4. Inventory agent skills separately. Walks every context-v/skills/<skill>/ under
#    your included sources, parses each SKILL.md frontmatter, counts assets.
#    Skills are excluded from corpus-manifest so they don't pollute the to-do list,
#    but indexed downstream alongside the corpus.
python scripts/build-skills-manifest.py

# 5. Run the collator. Reads sources.md, copies files into corpus/ with provenance keys.
python scripts/collate.py
```

**Clickable paths.** Both manifests render file paths as markdown links with editor-relative paths. In VS Code, Cursor, Windsurf, and Trae's markdown preview, clicking the path opens the source file in the same editor window. Configured to relativize against the manifest's own directory; no editor-specific URI scheme required.

Optional flags on the assembler:

```bash
python scripts/assemble-context-v-sources.py --root /path/to/another/tree
python scripts/assemble-context-v-sources.py --output sources.md
```

## How sources.md works

`sources.md` is a Markdown file with YAML frontmatter. The frontmatter is the machine-consumable part (read by both scripts); the body is human curation rationale that the assembler preserves on re-run.

Each entry in the `sources:` list has:

- `path` — absolute filesystem path to a `context-v/` directory or a legacy root
- `kind` — one of:
  - `context-v` — canonical six-folder structure
  - `legacy` — pre-context-v notes; pair with `subdirs:` whitelist to scope what's collated
  - `study-context-v` — lives inside a `studies/<name>/` collection
  - `open-call` — published proposals in the Hyperloop-paper spirit ("we thought of this, someone please build it"); flat directories, whole tree collated
- `include` — `true` to collate, `false` to skip
- `note` — free-form curation rationale (optional)
- `subdirs` — for `kind: legacy` only, a whitelist of subdirectories to walk

**Idempotency contract.** The assembler treats every entry already in `sources.md` as authoritative. New paths are appended with `include: false` and a dated note so the user opts them in deliberately. Removed paths (no longer on disk) are flagged as warnings to stdout but never silently dropped.

## Privacy / no-collision boundary

`corpus/` lives **outside** `context-v/` so the ai-labs splash rollup (which walks `context-v/` directories) does not pick up duplicates of files already collated from their original homes. This is the boundary by *location*, not by flag.

Per-file escape hatch: setting `private: true` in a file's frontmatter causes the collator to skip it. Reserved for edge cases the location-based boundary doesn't cover.

The kit's own `ai-labs/context-vigilance-kit/context-v/` is normal Lossless content (the kit's specs, plans, prompts, etc.) and **is** rolled up by the ai-labs splash — that's intentional.

**Path-substring exclusions.** Files whose absolute paths match any entry in `SKIP_PATH_SUBSTRINGS` (in both `build-corpus-manifest.py` and `collate.py`) are skipped:

- `/context-v/extra/` — per-directory escape hatch for scratch, out-of-band, or work-in-progress notes that should not flow into the corpus.
- `/context-v/skills/` — agent skills are tracked by `build-skills-manifest.py` as a separate concern. They're indexed downstream (ChromaDB), but excluded from the corpus to-do list so they don't dilute the fill-out work queue.
- `/context-v/changelog/` and `/context-v/changelogs/` — ship-log entries follow the [[changelog-conventions]] skill and are a different artifact class than fill-out-needing context-v docs. They land in the ChromaDB stream alongside the corpus, but stay out of the "complete a bunch of context-v files soon after splash launch" workflow. Both singular and plural forms exist in the wild; both are excluded.

## Provenance keys added by the collator

The collator does not modify originals. It writes copies into `corpus/` with these frontmatter keys appended:

- `source_root` — the source entry's `path` from `sources.md`
- `source_relative_path` — the file's path relative to that source root
- `source_repo_slug` — short identifier derived from the source path (last meaningful component)
- `collated_at` — ISO date the copy was written

## Promotion to its own repo

This kit is currently a plain directory inside `ai-labs/`. The next step is promoting it to its own repository under `lossless-group/`, then re-attaching as a git submodule. The standard recipe:

```bash
# from ai-labs/context-vigilance-kit/
git init
git add .
git commit -m "init(context-vigilance-kit): scaffold + v0 collator"

# create the empty repo on GitHub and push (gh auth required)
gh repo create lossless-group/context-vigilance-kit --public --source=. --remote=origin --push

# back up one level, remove the directory, re-add as submodule
cd ..
rm -rf context-vigilance-kit
git submodule add git@github.com:lossless-group/context-vigilance-kit.git context-vigilance-kit
git submodule update --init --recursive

# stage the .gitmodules + submodule pointer change in ai-labs and commit
git add .gitmodules context-vigilance-kit
git commit -m "init(submodule): add context-vigilance-kit as submodule"
```

After promotion, future work happens inside the submodule; ai-labs only tracks the gitlink.

## Related

- [[Collate-Context-Files-into-Context-Vigilance-as-Repo-&-Project]] — the scoping exploration in `ai-labs/context-v/explorations/`
- [[context-vigilance]] skill — the practice this kit codifies into tooling
- [[pseudomonorepos]] skill — `references/content-rollup.md` informs how a future remote-fetcher fits in alongside the v0 filesystem walker
- [[open-specs-and-standards]] study — informs Track 4 (publishing context-vigilance as an open spec)
