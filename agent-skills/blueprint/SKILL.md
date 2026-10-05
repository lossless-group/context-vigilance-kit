---
name: blueprint
description: "Starts a new blueprint in context-v/blueprints/: a pattern or design, and the reasoning behind it. Shortcut for `new blueprint`; same template, IDs, and checklist."
argument-hint: "<Title>"
disable-model-invocation: true
---

# blueprint: shortcut for `new blueprint`

Create a **blueprint** titled `$ARGUMENTS` by following the `new` skill exactly (`../new/SKILL.md`), with the type already set to `blueprint`. Don't ask for the type.

Everything else (finding `context-v/`, the template, minting `site_uuid` and `hex_code`, the filename, the checklist) is the `new` skill's job. This shortcut exists only so people can type `/cv:blueprint`.
