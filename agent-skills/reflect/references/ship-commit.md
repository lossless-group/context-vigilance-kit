# The ship commit: the default shape

Use this when the repo has no commit convention of its own. If it has one, follow it.

## Header

```
ship(feature, <capability>): <what someone can now do>
```

- `ship` marks the commit that closes a cycle: docs, changelog, and handoff land together.
- `<capability>` is a short kebab-case name for what was built (`password-reset`, `csv-export`).
- The description says what a user or developer can now do, not which files changed.

Other commits in the cycle can use any style. A common one is `{action}({area}): {description}`, with actions like `feat`, `fix`, `doc`, `refactor`, `chore`, `test`.

## Body

1. A short paragraph on the impact: why this matters.
2. Links: the changelog entry, the spec or plan, the handoff.
3. Closed tickets, if any.
4. "Also included:" for small riders.

```
ship(feature, csv-export): Teams can export any report as CSV

Reports could only be viewed in the app, so finance re-typed numbers into
spreadsheets every week. Now any report exports to CSV in one click.

- Changelog: changelog/2026-10-05_01.md
- Spec: context-v/specs/Report-Export.md (now Shipped)
- Handoff: context-v/handoffs/2026-10-05_Report-Export.md

Closes #41, #42

Also included:
- Fix a typo in the reports empty state
```
