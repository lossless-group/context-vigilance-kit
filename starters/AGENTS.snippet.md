
## Context Vigilance (context-v/)

This repo keeps its living documentation in `context-v/`: specs, plans, blueprints, explorations, issues, and handoffs, written for people and agents alike.

- **Before starting work,** check `context-v/handoffs/` for the latest handoff, and look for a spec or plan that covers the task.
- **When creating or editing anything in `context-v/`,** follow the `context-vigilance` skill. If your tool can't load skills, read https://github.com/lossless-group/context-vigilance-kit/blob/master/agent-skills/context-vigilance/SKILL.md.
- **Never type IDs.** Generate `site_uuid` with `uuidgen | tr 'A-Z' 'a-z'` and `hex_code` with `LC_ALL=C tr -dc 'a-z0-9' </dev/urandom | head -c6`.
- **Don't fix unrelated inconsistencies** in passing. Note them and tell the user.
- **Workflow:** kickoff → prep (explore → spec → plan) → implement or loop → reflect (as-built, issues, changelog, handoff, ship).
