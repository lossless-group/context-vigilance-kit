# Context-v and the Open Knowledge Format

A `context-v/` folder is an [Open Knowledge Format](https://github.com/GoogleCloudPlatform/open-knowledge-format) (OKF) v0.2 bundle. Context-v is a *profile* of OKF: OKF's few requirements, with context-v's folders, lifecycle, versions, and IDs on top. Any OKF tool can read a context-v folder.

## Contents

- What OKF requires · `type` · Index files · Field mapping · Status mapping · Sign-off as `verified` · Citations as `sources` · Outside the bundle · Checking conformance

## What OKF requires

A bundle conforms when:

1. Every `.md` file, except `index.md` and `log.md`, has parseable YAML frontmatter.
2. Every frontmatter block has a non-empty `type`.
3. `index.md` and `log.md`, when present, follow their shapes (below).

Everything else is optional, and OKF tools must keep keys they don't recognize. All of context-v's frontmatter rides along.

## `type`

**exact:** `type` is the doc's folder name in Train-Case.

| Folder | `type` |
|---|---|
| `specs/` | `Specs` |
| `plans/` | `Plans` |
| `explorations/` | `Explorations` |
| `decisions/` | `Decisions` |
| `loops/` | `Loops` |
| `research-notes/` (a new folder) | `Research-Notes` |

Folder names are plural. `extra/` and `sitemap/` are the long-standing singular exceptions (`sitemap/` → `type: Sitemap`; `extra/` sits outside the bundle). The kit's frontmatter check enforces this on new files: a missing or mismatched `type` is blocked with the right value in the message.

## Index files

`index.md` is a table of contents: headings, each with a list of links and one-line descriptions. **No frontmatter**, except the root `context-v/index.md`, which declares the OKF version.

```markdown
---
okf_version: "0.2"
---

# Prep: deciding what to build

* [Specs](specs/) - What we're building and why
* [Plans](plans/) - Ordered, scoped steps toward a spec
```

A folder's own `index.md` lists its docs, each line using the doc's `description`:

```markdown
# Specs

* [Payment Retry Policy](Payment-Retry-Policy.md) - When and how failed charges retry
* [Report Export](Report-Export.md) - Any report downloads as CSV
```

- `new` adds a doc's line when it creates the doc; `reflect` checks every doc touched in a cycle is listed; `kickoff` reads the indexes before opening anything.
- Keep superseded docs listed, marked `(superseded)`. Indexes are a record, not just a menu.
- `log.md` is optional: date headings `## YYYY-MM-DD`, newest first, then bullet entries. Context-v's `changelog/` usually covers the same need.

## Field mapping

Context-v keeps its own fields. OKF fields are added only where they carry something new.

| OKF | Context-v | Notes |
|---|---|---|
| `type` | the folder | Required; see above |
| `title` | `title` | Same |
| `description` | `description` | One plain sentence; indexes and search show it. Distinct from `lede` (a hook) and `summary` (for agents) |
| `tags` | `tags` | Same; context-v uses Train-Case |
| `status` | `status` | Different vocabularies; see the next section |
| `generated: { by, at }` | `authors`, `augmented_with`, `date_modified` | Optional. `by` is `human:<id>` or `<tool>/<version>`; `at` is a datetime with a UTC offset |
| `verified: { by, at }` | sign-off | See below |
| `sources[]` + footnotes | hex-code citations | Same idea; see below |
| `stale_after` | the `Stale` status | Optional; makes staleness machine-checkable |
| `timestamp` | — | Retired in OKF v0.2; don't add it |

**Datetimes:** OKF fields use full datetimes with a UTC offset (`2026-10-05T14:00:00Z`). Context-v's `date_*` fields stay date-only.

## Status mapping

OKF's `status` is `draft | stable | deprecated` (absent means `stable`). Context-v keeps its richer lifecycle; OKF readers map it:

| Context-v | OKF |
|---|---|
| `Draft`, `In-Review` | `draft` |
| `Signed-Off`, `Implementing`, `Shipped`, `Partially-Shipped` | `stable` |
| `Stale`, `Superseded`, `Archived`, `Deferred` | `deprecated` |

## Sign-off as `verified`

When someone signs off a spec or decision, record it twice: `status: Signed-Off`, and

```yaml
verified: { by: "human:jdoe", at: 2026-10-05T14:00:00Z }
```

OKF reads a `human:` verifier as **human-reviewed**, the highest of its trust tiers. More checks can be appended as a list.

## Citations as `sources`

OKF attributes claims with footnotes keyed to `sources[].id`, by stable key rather than position, because agents reorder lists. Hex-code citations already work that way: use the code as the `id`.

```yaml
sources:
  - id: k3x9q2
    resource: https://example.com/research
    title: The research the claim rests on
```

```markdown
Ageing accelerates toward 2.1B people over 60 by 2050.[^k3x9q2]

[^k3x9q2]: The research the claim rests on
```

## Outside the bundle

- **`agent-skills/`:** skills follow the Agent Skills spec, and their reference files have no frontmatter. Treat the folder as beside the bundle, the way OKF expects schemas to sit beside it.
- **`extra/`:** scratch, gitignored, so a cloned bundle never contains it.

## Checking conformance

```bash
# Every non-reserved .md under context-v/ (skipping extra/ and agent-skills/) needs frontmatter with a type.
find context-v -name '*.md' -not -path '*/extra/*' -not -path '*/agent-skills/*' \
  -not -name index.md -not -name log.md -not -name README.md |
while read -r f; do
  head -1 "$f" | grep -q '^---$' && sed -n '2,/^---$/p' "$f" | grep -q '^type: ' || echo "missing type: $f"
done
```

No output means conformant.
