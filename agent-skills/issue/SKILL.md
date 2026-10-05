---
name: issue
description: "Starts a new issue: a hard problem's path, wrong guesses included. Goes to context-v/issues/ or the configured tracker. Shortcut for `new issue`; same template, IDs, and checklist."
argument-hint: "<Title>"
disable-model-invocation: true
---

# issue: shortcut for `new issue`

Create a **issue** titled `$ARGUMENTS` by following the `new` skill exactly (`../new/SKILL.md`), with the type already set to `issue`. Don't ask for the type.

Everything else (finding `context-v/`, the template, minting `site_uuid` and `hex_code`, the filename, the checklist) is the `new` skill's job. This shortcut exists only so people can type `/cv:issue`.
