# context-vigilance-kit

> Treat context files with the same vigilance as code, and *context becomes the code* — or the parent to it. Regenerating code, fixing bugs, refactoring, even migrating across languages or tech stacks — work that used to take days, weeks, or months — compresses to minutes.
>
> Generating a fully-featured splash page — search, three viewing modes, coherent theme CSS, full markdown rendering — now takes **5 minutes**. Only with context vigilance.

Tooling for the **Context Vigilance** practice — collating, indexing, and eventually publishing the `context-v/` directories scattered across [The Lossless Group](https://github.com/lossless-group) tree (and beyond) as a single, queryable corpus. Brand site: [contextvigilance.com](https://contextvigilance.com) (forthcoming). Scope, rationale, and decision history live in the parent exploration: [[Collate-Context-Files-into-Context-Vigilance-as-Repo-&-Project]] (under `ai-labs/context-v/explorations/`).

## What's in here (v0)

```
context-vigilance-kit/
├── README.md                          ← you are here
├── sources.md                         ← curated list of source dirs (generated, then human-curated)
├── scripts/
│   ├── assemble-context-v-sources.py  ← walks the tree, populates sources.md
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
#    add legacy-shaped directories by hand with `kind: legacy`.

# 3. Run the collator. Reads sources.md, copies files into corpus/ with provenance keys.
python scripts/collate.py
```

Optional flags on the assembler:

```bash
python scripts/assemble-context-v-sources.py --root /path/to/another/tree
python scripts/assemble-context-v-sources.py --output sources.md
```

## How sources.md works

`sources.md` is a Markdown file with YAML frontmatter. The frontmatter is the machine-consumable part (read by both scripts); the body is human curation rationale that the assembler preserves on re-run.

Each entry in the `sources:` list has:

- `path` — absolute filesystem path to a `context-v/` directory or a legacy root
- `kind` — `context-v` (canonical six-folder structure), `legacy` (pre-context-v notes), or `study-context-v` (lives inside a study)
- `include` — `true` to collate, `false` to skip
- `note` — free-form curation rationale (optional)
- `subdirs` — for `kind: legacy` only, a whitelist of subdirectories to walk

**Idempotency contract.** The assembler treats every entry already in `sources.md` as authoritative. New paths are appended with `include: false` and a dated note so the user opts them in deliberately. Removed paths (no longer on disk) are flagged as warnings to stdout but never silently dropped.

## Privacy / no-collision boundary

`corpus/` lives **outside** `context-v/` so the ai-labs splash rollup (which walks `context-v/` directories) does not pick up duplicates of files already collated from their original homes. This is the boundary by *location*, not by flag.

Per-file escape hatch: setting `private: true` in a file's frontmatter causes the collator to skip it. Reserved for edge cases the location-based boundary doesn't cover.

The kit's own `ai-labs/context-vigilance-kit/context-v/` is normal Lossless content (the kit's specs, plans, prompts, etc.) and **is** rolled up by the ai-labs splash — that's intentional.

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
