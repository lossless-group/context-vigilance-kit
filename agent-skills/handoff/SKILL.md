---
name: handoff
description: "Starts a new handoff in context-v/handoffs/: what landed, what's mid-flight, and what the next session must load first. Shortcut for `new handoff`; same template, IDs, and checklist."
argument-hint: "[<Title>]"
disable-model-invocation: true
---

# handoff: shortcut for `new handoff`

Create a **handoff** titled `$ARGUMENTS` by following the `new` skill exactly (`../new/SKILL.md`), with the type already set to `handoff`. Don't ask for the type.

No title given? Use a short name for the work this session was on.

Everything else (finding `context-v/`, the template, minting `site_uuid` and `hex_code`, the filename, the checklist) is the `new` skill's job. This shortcut exists only so people can type `/cv:handoff`.
