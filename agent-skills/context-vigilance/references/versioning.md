# Versioning: Three or Four Parts

> **Field name:** write **`at_semantic_version`**. It reads naturally as "this doc is *at* version X," and it's what the templates use.
>
> **`semantic_version` is a permanently-accepted alias** for the same property and value. It is not a legacy spelling awaiting cleanup, and no migration is wanted: resolving one extra key is free for a renderer, while rewriting files to unify the spelling buys nothing. Consumers read `at_semantic_version ?? semantic_version`.
>
> So: **write `at_`, read either, never rewrite a file just to change which name it uses.** Everything below applies to both.
>
> Bump it together with `date_authored_current_draft`: a version move and a substantive revision are the same event.

A version can have **three parts or four**. The user picks; neither is enforced. Your job is to read each one correctly and keep to the format a doc or repo already uses.

| Parts | Format | Example | Read it as | Where it comes from |
|---|---|---|---|---|
| Three | `major.minor.patch` | `0.1.0` | major 0, minor 1, patch 0 | [Semantic Versioning](https://semver.org/), the market standard. New work usually starts at `0.1.0`. |
| Four | `epoch.major.minor.patch` | `0.1.0.0` | epoch 0, major 1, minor 0, patch 0 | Our extension for documents, adding a number for a change bigger than a major one. New docs start at `0.0.0.1`. |

**Count the parts before you read the digits.** `0.1.0` and `0.1.0.0` look alike, but the `1` is a minor in the first and a major in the second.

**Which to use:**

- **Existing doc:** keep its format. Never convert a version from one format to the other.
- **New doc:** match the other docs in the repo. If there's nothing to match, use the template's default, unless the user prefers otherwise.
- **Published package:** always three parts. npm, JSR, and other semver tools don't accept four.

**Where epochs come from:** the idea is from Anthony Fu's [Epoch Semantic Versioning](https://antfu.me/posts/epoch-semver). His published format still has three numbers, so existing tools keep working: `{EPOCH * 1000 + MAJOR}.MINOR.PATCH`. So `1002.3.0` means epoch 1, major 2, minor 3, patch 0, and a first number of 1000 or more is the sign of it. Our four-part format writes the epoch as its own number, which he describes as the ideal but too late for package tools to adopt.

The bump rules are the same in both formats, except that only four-part has an epoch. The rest of this page shows four-part; for three-part, drop the first number.

## Four-part format

Integers only:

```
epoch . major . minor . patch
  │       │       │       │
  │       │       │       └── typo, clarification, small wording fix
  │       │       └────────── new section, additive content
  │       └────────────────── restructure of the document
  └────────────────────────── total pivot: fundamentally different direction
```

## Starting version

Four-part documents start at `0.0.0.1`; three-part work usually starts at `0.1.0`.

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
