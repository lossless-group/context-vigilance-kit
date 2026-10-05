# Changelog entry: the default shape

Use this when the repo keeps a `changelog/` folder and has no convention of its own. If it has one, follow it.

**Filename:** `changelog/YYYY-MM-DD_NN.md`, where `NN` is `01`, `02`… for that day.

```markdown
---
title: "What someone can now do, in a headline"
lede: "One hook line, 140 characters max."
date_created: YYYY-MM-DD
date_modified: YYYY-MM-DD
date_authored_initial_draft: YYYY-MM-DD
date_authored_current_draft: YYYY-MM-DD
authors:
  - Jane Doe
augmented_with:
  - HARNESS on MODEL
publish: true
tags:
  - Train-Case-Tag
files_changed:
  - path/to/file
site_uuid: GENERATE
hex_code: GENERATE
---

## Why Care?

One paragraph for someone who's never seen the project: what changed for them.

## What's New?

- **The capability**, in a sentence or two each.

## Known Gotchas

- What will trip someone up.

## What's Next?

- The next step, and a link to the doc that tracks it.
```

Rules:

- **It exists** is the priority. A short, true entry beats a polished one that never gets written.
- **Lead with what someone can do now**, not what files moved.
- **Absolute links for images** (a URL, not `./img.png`): entries often get copied into other sites, where relative paths break.
