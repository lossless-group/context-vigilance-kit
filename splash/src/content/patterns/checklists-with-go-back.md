---
title: "Checklists with go-back lines"
lede: "The agent copies the checklist into its reply and ticks it off, and a failed check sends it back a step."
maturity: Emerging
mode: practice
order: 18
date_created: 2026-10-05
date_modified: 2026-10-05
authors:
  - Michael Staton
augmented_with:
  - Claude Code on Claude Opus 5.5
tags:
  - Agent-Skills
  - Checklists
  - Feedback-Loops
---
## What it is

Multi-step skills carry a checklist the agent copies into its reply and ticks off as it goes. Checks that can fail carry a *go-back line*:

```markdown
- [ ] Every new doc's frontmatter parses (run the parser; don't eyeball it)
      → if any fails, fix it and re-run this check before continuing
```

## Why

Agents skip steps on long tasks, and a ticked box can wave through a wrong result. The go-back line turns a checklist into a feedback loop: check, fix, check again.

## How

- **Process checklists** live in the workflow skills.
- **Document checklists** ("done when") live at the end of each template.
- **Repo-specific additions** live in that repo's clarified loop doc, not in copies scattered through folders.
