# Search First: Finding Prior Work Before Creating New

Concrete recipes for the "walk up, then search" routine in `SKILL.md`.

## Contents

- Why it matters
- Find the tree's root and every context-v/
- Topic search
- Reading and reporting results
- When to skip
- Logging refactor debt
- Anti-patterns

## Why it matters

A new spec that ignores three related ones isn't progress; it's noise that the next
reader has to reconcile. Disconnected work is the failure this practice exists to prevent.

## Find the tree's root and every context-v/

```bash
# Every context-v/ from the current directory up to the filesystem root
walk_up_context_v() {
  local dir="$PWD"
  while [ "$dir" != "/" ]; do
    [ -d "$dir/context-v" ] && echo "$dir/context-v"
    dir="$(dirname "$dir")"
  done
}

# The outermost repo in the chain (the tree's root)
tree_root() {
  local dir="$PWD" root=""
  while [ "$dir" != "/" ]; do
    [ -e "$dir/.git" ] && root="$dir"
    dir="$(dirname "$dir")"
  done
  echo "$root"
}

# Every context-v/ anywhere under the root
ROOT="$(tree_root)"
find "$ROOT" -type d -name context-v -not -path '*/node_modules/*' 2>/dev/null
```

If `tree_root` lands on something too broad (like a home directory that happens to be a
repo), use the topmost directory that also has a `context-v/`.

## Topic search

Pick 1–3 keywords that capture the task, then search filenames, content, and tags:

```bash
ROOT="$(tree_root)"
DIRS=$(find "$ROOT" -type d -name context-v -not -path '*/node_modules/*' 2>/dev/null)

# Filenames
for d in $DIRS; do find "$d" -type f -iname '*keyword*'; done

# Content (case-insensitive)
grep -ril 'keyword' $DIRS

# Frontmatter tags (adjust to the tag style the tree uses)
grep -rliE '^\s*-\s*keyword\s*$' $DIRS
```

With ripgrep: `rg -il keyword --glob '**/context-v/**' "$ROOT"`. It's faster and
respects `.gitignore`, which skips `context-v/extra/` if that's gitignored; search it
explicitly when scratch notes might matter.

## Reading and reporting results (shaped)

Don't dump raw hits. Triage:

1. **Direct match**: same topic, same level. Show first.
2. **Adjacent match**: related, possibly extendable. Show with a short why.
3. **Tangential match**: shared keywords, different intent. Mention only if hits are sparse.

Report format:

> Found related work:
> - `acme-platform/web/context-v/blueprints/Image-Pipeline.md` (direct: may extend)
> - `acme-platform/context-v/explorations/Cdn-Strategies.md` (adjacent: may inform)
> - `acme-platform/api/context-v/issues/Thumbnail-Cron.md` (tangential: different layer)
>
> Recommendation: extend the blueprint and link the exploration. Want me to draft that?

When nothing turns up, that's a real result. Say what you searched:

> Searched `context-v/` at `acme-platform`, `web`, `api`, `docs` for "rate limit" and
> "throttle": no prior work. Drafting new.

## When to skip (open)

- The user says "just ship," "don't search," or "we'll clean up later."
- The task is trivially small (typo, one-line change).
- You already searched this topic earlier in the same session.

Say that you're skipping, then leave a marker.

## Logging refactor debt

Two acceptable forms. Either way, include keywords so the next pass can search for them.

**In the file you just shipped** (frontmatter or a comment):

```yaml
refactor_debt: "Shipped without checking for prior patterns. Search: 'image pipeline', 'cdn'."
```

**As a one-liner in `context-v/issues/`:**

```markdown
---
title: "Refactor Debt: Upload flow shipped without prior-pattern search"
date_created: YYYY-MM-DD
tags:
  - Refactor-Debt
status: open
---

Shipped `web/src/upload/` without searching for prior work.
Search candidates: "upload", "image pipeline", "presigned url".
```

## Anti-patterns

- Silently writing a duplicate of an existing blueprint.
- "I didn't find anything" without saying where or what you searched.
- Refactor-debt markers with no keywords.
- Searching only the nearest `context-v/` and skipping the walk up.
