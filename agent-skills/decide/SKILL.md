---
name: decide
description: "Starts a new decision in context-v/decisions/: what was decided, by whom, when, and the alternatives passed over. Shortcut for `new decision`; same template, IDs, and checklist."
argument-hint: "<Title>"
disable-model-invocation: true
---

# decide: shortcut for `new decision`

Create a **decision** titled `$ARGUMENTS` by following the `new` skill exactly (`../new/SKILL.md`), with the type already set to `decision`. Don't ask for the type.

Everything else (finding `context-v/`, the template, minting `site_uuid` and `hex_code`, the filename, the index line, the checklist) is the `new` skill's job. This shortcut exists only so people can type `/cv:decide`.
