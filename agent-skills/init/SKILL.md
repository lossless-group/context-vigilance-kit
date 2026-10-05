---
name: init
description: Scaffolds a context-v/ folder at the root of the current repo (the canonical folders plus extra/ and sitemap/), adds context-v/extra/ to .gitignore, writes a short context-v/README.md, and offers an AGENTS.md pointer and an optional changelog/ folder. Use when the user asks to set up, initialize, or add context-v to a project.
disable-model-invocation: true
---

# init: scaffold context-v/

Lay down the practice in this repo. **Ask nothing up front** except the two offers at the end. No config files, no databases, no hooks.

The starter files live in this kit's `starters/` folder: find the kit by walking up from this skill's own folder (`../../starters/`).

## Checklist

Copy this into your reply and tick as you go:

- [ ] Found the repo root (`git rev-parse --show-toplevel`; if not a git repo, use the current folder and say so)
- [ ] Checked for an existing `context-v/` (or a lookalike: `docs/context`, `.context`, `ai-docs`)
      → if one exists, **stop scaffolding**: report what's there, and only add missing folders if the user says so
- [ ] Created the canonical folders, each with a `.gitkeep` so they commit: `specs/ plans/ prompts/ blueprints/ reminders/ agent-skills/ explorations/ issues/ extra/ sitemap/`
- [ ] Did **not** create the experimental folders (`loops/ handoffs/ decisions/ habits/ contracts/`); they appear when first used
- [ ] Copied `starters/context-v/README.md` to `context-v/README.md` (skip if one exists)
- [ ] Added `context-v/extra/` to `.gitignore` (create the file if missing; don't duplicate the line)
- [ ] Offered the agent pointer: "Add a short section to AGENTS.md so every agent knows about context-v?" On yes, append `starters/AGENTS.snippet.md` to `AGENTS.md`, creating it if needed. Never overwrite an existing file.
- [ ] Offered `changelog/` (a dated ship log at the repo root). On yes, create it with `starters/changelog/README.md`.
- [ ] Listed what was created, then suggested a first move: `new exploration "<what you're figuring out>"`, or `new spec` if the user already knows what to build

## Notes

- **exact:** folder names, the `.gitignore` line, never overwriting.
- **open:** wording of the final suggestion.
- If the user asked for a monorepo or a tree of repos, also load the `pseudomonorepos` skill: each child repo can get its own `context-v/`.
