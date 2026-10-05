---
name: plan
description: "Starts a new plan in context-v/plans/: ordered, scoped steps toward a spec, each one checkable. Shortcut for `new plan`; same template, IDs, and checklist."
argument-hint: "<Title>"
disable-model-invocation: true
---

# plan: shortcut for `new plan`

Create a **plan** titled `$ARGUMENTS` by following the `new` skill exactly (`../new/SKILL.md`), with the type already set to `plan`. Don't ask for the type.

Everything else (finding `context-v/`, the template, minting `site_uuid` and `hex_code`, the filename, the checklist) is the `new` skill's job. This shortcut exists only so people can type `/cv:plan`.
