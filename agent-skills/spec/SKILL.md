---
name: spec
description: "Starts a new spec in context-v/specs/: what to build, why, and how we'll know it works. Shortcut for `new spec`; same template, IDs, and checklist."
argument-hint: "<Title>"
disable-model-invocation: true
---

# spec: shortcut for `new spec`

Create a **spec** titled `$ARGUMENTS` by following the `new` skill exactly (`../new/SKILL.md`), with the type already set to `spec`. Don't ask for the type.

Everything else (finding `context-v/`, the template, minting `site_uuid` and `hex_code`, the filename, the checklist) is the `new` skill's job. This shortcut exists only so people can type `/cv:spec`.
