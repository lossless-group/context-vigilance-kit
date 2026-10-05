# Four-Part Versioning

> **Field name:** write **`at_semantic_version`**. It reads naturally as "this doc is *at* version X," and it's what the templates use.
>
> **`semantic_version` is a permanently-accepted alias** for the same property and value. It is not a legacy spelling awaiting cleanup, and no migration is wanted: resolving one extra key is free for a renderer, while rewriting files to unify the spelling buys nothing. Consumers read `at_semantic_version ?? semantic_version`.
>
> So: **write `at_`, read either, never rewrite a file just to change which name it uses.** Everything below applies to both.
>
> Bump it together with `date_authored_current_draft`: a version move and a substantive revision are the same event.

The version uses **four** integers, not three (**exact** format: `e.M.m.p`, integers only):

```
epoch . major . minor . patch
  │       │       │       │
  │       │       │       └── typo, clarification, small wording fix
  │       │       └────────── new section, additive content
  │       └────────────────── restructure of the document
  └────────────────────────── total pivot: fundamentally different direction
```

## Starting version

New documents start at `0.0.0.1`.

## Epoch semantics

- **`0.x.x.x`** = proposal, not yet adopted. The doc exists but the team hasn't bought in.
- **`1.0.0.0`** = first accepted version. Promote from epoch 0 to 1 when the doc describes how the project actually works.
- **`2.0.0.0`+** = total pivot. Not a restructure: the previous direction is being abandoned or replaced wholesale.

## When to bump which digit

| Change | Bump |
|---|---|
| Fix a typo, clarify a sentence, tighten wording | `patch` |
| Add a new section, add an example, append meaningful content | `minor` |
| Restructure sections, reorganize, merge/split docs | `major` |
| Total pivot: the doc now argues for a fundamentally different approach | `epoch` |

## Cascading reset

Semver-style cascading is **encouraged, not enforced** (shaped):

- Bumping `minor` *should* reset `patch` (`0.0.1.5` → `0.0.2.0`)
- Bumping `major` *should* reset `minor` and `patch` (`0.0.2.5` → `0.1.0.0`)
- Bumping `epoch` *should* reset everything (`0.3.2.5` → `1.0.0.0`)

Don't block on it. Consistency within a single file is the real goal: if a file has been climbing without resets, keep climbing rather than retroactively fixing.

## When you can't decide

Bump the **patch**. Under-signaling a change beats blocking on the question.

## Don't decrement

Versions only go up. If you made a mistake, fix forward with a patch bump.

## Example progression

```
0.0.0.1   # initial proposal
0.0.0.2   # fixed a typo
0.0.1.0   # added "Decision Tree" section
0.0.1.1   # clarified one bullet in the new section
0.0.2.0   # added a second new section
0.1.0.0   # restructured into 3 parts instead of running prose
1.0.0.0   # team adopted it; promoted from proposal to canonical
1.0.0.1   # typo fix on the canonical version
2.0.0.0   # approach abandoned; this doc now argues for the replacement
```

## What to do alongside the bump

Update `date_modified` in the same edit (and `date_authored_current_draft` when the change is substantive).
