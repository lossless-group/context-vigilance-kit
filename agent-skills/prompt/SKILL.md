---
name: prompt
description: "Starts a new prompt in context-v/prompts/: step-by-step implementation with a check after each step. Shortcut for `new prompt`; same template, IDs, and checklist."
argument-hint: "<Title>"
disable-model-invocation: true
---

# prompt: shortcut for `new prompt`

Create a **prompt** titled `$ARGUMENTS` by following the `new` skill exactly (`../new/SKILL.md`), with the type already set to `prompt`. Don't ask for the type.

Everything else (finding `context-v/`, the template, minting `site_uuid` and `hex_code`, the filename, the checklist) is the `new` skill's job. This shortcut exists only so people can type `/cv:prompt`.
