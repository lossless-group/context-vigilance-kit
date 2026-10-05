---
name: explore
description: "Starts a new exploration in context-v/explorations/: a question whose answer isn't clear yet, with options and findings. Shortcut for `new exploration`; same template, IDs, and checklist."
argument-hint: "<Title>"
disable-model-invocation: true
---

# explore: shortcut for `new exploration`

Create a **exploration** titled `$ARGUMENTS` by following the `new` skill exactly (`../new/SKILL.md`), with the type already set to `exploration`. Don't ask for the type.

Everything else (finding `context-v/`, the template, minting `site_uuid` and `hex_code`, the filename, the checklist) is the `new` skill's job. This shortcut exists only so people can type `/cv:explore`.
