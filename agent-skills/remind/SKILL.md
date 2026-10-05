---
name: remind
description: "Starts a new reminder in context-v/reminders/: a short correction for a mistake agents keep making. Shortcut for `new reminder`; same template, IDs, and checklist."
argument-hint: "<Title>"
disable-model-invocation: true
---

# remind: shortcut for `new reminder`

Create a **reminder** titled `$ARGUMENTS` by following the `new` skill exactly (`../new/SKILL.md`), with the type already set to `reminder`. Don't ask for the type.

Everything else (finding `context-v/`, the template, minting `site_uuid` and `hex_code`, the filename, the checklist) is the `new` skill's job. This shortcut exists only so people can type `/cv:remind`.
