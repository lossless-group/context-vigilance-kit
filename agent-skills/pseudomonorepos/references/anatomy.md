# Anatomy of a Pseudomonorepo

What makes a directory a pseudomonorepo, as opposed to a true monorepo or a plain
folder of repos.

## Contents

- Definition
- What it isn't
- How to identify one
- Submodules vs. plain folders
- When to create a new level
- Expect imperfection

## Definition

A **pseudomonorepo** is a parent git repo that:

1. **Owns a `context-v/`** that spans its children.
2. **Contains children**: often git submodules, sometimes plain folders, sometimes both.
3. **Does not** share builds, package manifests, or workspace tooling across children
   (that would make it a true monorepo).
4. **Is loosely structured but deliberately aware** of what its children are doing.

The defining feature is #1. Without a parent `context-v/`, it's just a folder of repos.

## What it isn't

| It's not... | Because... |
|---|---|
| A true monorepo | No shared package manifest, workspace config, or build pipeline |
| A pnpm / yarn / Cargo workspace | Children don't share dependencies |
| An Nx / Turborepo setup | No task orchestration across children |
| A loose folder of repos | The parent maintains intentional cross-cutting context |
| Just a git superproject | Submodules are the *means*; shared context is the *purpose* |

A pseudomonorepo may contain a true monorepo as one of its children. That's expected.

## How to identify one (shaped)

Check, in order:

1. Does the directory contain `context-v/`?
2. Does it contain child directories that are themselves git repos (a `.gitmodules`
   file, or nested `.git` entries)?
3. Is the directory itself a git repo?

```bash
is_pseudomonorepo() {
  [ -e "$1/.git" ] && [ -d "$1/context-v" ] && \
  { [ -f "$1/.gitmodules" ] || find "$1" -mindepth 2 -maxdepth 3 -name .git -not -path '*/node_modules/*' | grep -q .; }
}
```

- **All three:** a pseudomonorepo.
- **1 + 2, parent not a repo:** a *forming* pseudomonorepo. Mention it to the user.
- **2 + 3, no `context-v/`:** a folder of repos. If the children clearly share concerns,
  suggest adding a parent `context-v/`; don't create it unasked.

Note that a submodule's `.git` is a file, not a directory, which is why the check uses `-e`.

## Submodules vs. plain folders (open)

Submodules keep each child authoritative (no copy drift), let the parent pin children to
exact commits, and preserve each child's history. Their costs are real: updating is
clunky, detached HEAD inside a submodule is a frequent trap, pull requests don't span
repo boundaries, and collaborators forget `--recurse-submodules`.

A child may instead be a plain folder when it is still incubating, intentionally tied to
the parent's lifecycle, or when submodules were tried and abandoned for it. Both shapes
are valid; the parent `context-v/` covers both.

Before writing a script to manage submodules in bulk (re-attaching detached HEADs,
switching every child to one branch), **check the parent's root and `scripts/` folder**
for one that already exists.

## When to create a new level (open)

Create a new pseudomonorepo level when:

- there are roughly 3+ related projects that would benefit from shared context,
- each is substantial enough to warrant its own repo, and
- a parent `context-v/` would hold real content (cross-cutting blueprints, shared specs, decisions).

Don't create one when it's a single project with internal packages (use a true monorepo),
or when the "cross-cutting context" would be empty.

## Expect imperfection

Most real trees are maintained unevenly:

- parent `context-v/` folders are sparse,
- some children are stale or abandoned,
- cross-references between levels are inconsistent,
- the root README may not list the current children.

Treat the structure as a working sketch. The search-first habit is what fills the gaps,
and the drift policy in `SKILL.md` (observe and surface, don't silently fix) still applies.
