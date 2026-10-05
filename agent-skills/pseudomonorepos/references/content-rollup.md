# Content Roll-Up Across the Tree

How a parent's docs site, changelog page, or README index can show its children's
`changelog/` and `context-v/` entries alongside its own, in one feed.

## Contents

- What rolls up
- Two mechanisms
- Sync deliberately, build from files
- Output layout and provenance
- Schema leniency
- Failure modes
- Composing up the tree

## What rolls up

- **`changelog/`**: each child's dated entries merge into the parent's list, sorted by
  date across the whole set. Walk subdirectories too (e.g. `changelog/releases/1.2.0.md`).
- **`context-v/`**: specs, plans, blueprints, and so on from each child, grouped by
  type (all specs together) with the source child shown on each entry.

## Two mechanisms (open: pick by whether children are always checked out)

| Mechanism | Use when | How |
|---|---|---|
| **Local filesystem** | Children are always present on disk (cloned with `--recurse-submodules`, or plain folders) | A script reads each child's `changelog/` and `context-v/` directly. No auth, no network. |
| **GitHub Contents API** | Children are submodules that may *not* be checked out (CI, contributors who skip submodules) | For each entry in `.gitmodules`: derive `{owner}/{repo}` from `url =`, use `branch =` as `ref`, then recursively list `/repos/{owner}/{repo}/contents/changelog` and `/contents/context-v`, fetching each file. |

API notes: authenticate (unauthenticated calls are limited to 60/hour; a token gets
5,000/hour). In CI, the workflow's `GITHUB_TOKEN` covers repos it can read; private
children in other orgs need a broader token. Treat a 404 on a missing directory as "skip."

Both mechanisms should write the same output shape so everything downstream is identical.

## Sync deliberately, build from files (shaped)

Prefer an explicit sync step over fetching during every build:

```
sync step   ← fetches or copies children's files into a rollup/ folder
build       ← reads only local files; reproducible, no network
```

Fetching at build time makes every build slower, needs tokens in CI, and fails whenever
the API rate-limits. Commit the synced folder so the site always builds without network
access. Re-run the sync after bumping submodule pointers, when a child ships a notable
entry, on a schedule (a cron CI job that syncs, commits, and pushes), and right before deploying.

## Output layout and provenance

```
site/src/rollup/
├── README.md                 # auto-written: "synced content, edit at the source"
├── changelog/
│   ├── web/2026-03-02_01.md
│   ├── web/releases/1.2.0.md
│   └── api/2026-03-05_01.md
└── context-v/
    ├── web/specs/...
    └── api/blueprints/...
```

Every rolled-up file should carry where it came from: inject frontmatter such as
`from: web` and `from_path: changelog/releases/1.2.0.md`, and a one-line comment telling
editors to change the source, not the copy. Render the source child visibly on each card
and make it filterable (e.g. `/changelog?from=web`), so the parent never appears to have
authored its children's work.

## Schema leniency

Children's frontmatter won't be uniform. Coerce empty strings, placeholders like `TBD`,
and malformed dates to "missing" rather than failing the build. The point of the roll-up
is to surface what people actually wrote. Skip-with-warning beats a broken build.

## Failure modes

- Child lacks `changelog/` or `context-v/`: skip quietly.
- Rate limit or network error during sync: fail the sync loudly, and never overwrite a
  known-good `rollup/` folder with a partial one.
- Unknown frontmatter fields: keep them, ignore them in rendering.

## Composing up the tree

Each level only needs to know about its direct children. A parent rolls up its children;
the grandparent rolls up the parent's rolled-up feed along with its own other children.
Recursion falls out naturally when every level uses the same sync shape.
