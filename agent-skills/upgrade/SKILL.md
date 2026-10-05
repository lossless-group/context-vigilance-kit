---
name: upgrade
description: "Pulls the latest Context Vigilance Kit, however it was installed (Claude Code plugin, a cloned skills folder, or the AGENTS.md snippet alone), says what changed since the installed version, and offers, never forces, to bring this repo's context-v/ up to new conventions. Use when the user says upgrade, update, or \"get the latest cv\"."
argument-hint: ""
disable-model-invocation: true
---

# upgrade: pull the latest kit

Two separate things, in this order: **update the kit**, then **offer** to update this repo's docs to any new conventions. The second is optional and never automatic.

## 1. Update the kit

Copy this into your reply and tick as you go:

- [ ] Found how the kit is installed:
  - **Claude Code plugin:** `claude plugin list` shows `cv@context-vigilance-kit`
  - **Cloned skills:** a `context-vigilance-kit` git clone whose `agent-skills/*` were copied into a skills folder (`~/.agents/skills/` or similar)
  - **AGENTS.md only:** the snippet in `AGENTS.md`, nothing installed
  → none of these: say so and offer the install steps from the kit's README
- [ ] Noted the installed version (the plugin's version, or `git -C <clone> log -1 --format=%h`)
- [ ] Updated:
  - **Plugin:**
    ```
    claude plugin marketplace update context-vigilance-kit
    ```
    then
    ```
    claude plugin update cv@context-vigilance-kit
    ```
    Then tell the user to run `/reload-plugins`, or restart Claude Code. The new version loads only after that.
  - **Cloned skills:** `git -C <clone> pull`, then copy `agent-skills/*` into the same skills folder again (overwrite only the kit's own skill folders, never others)
  - **AGENTS.md only:** compare the snippet with the latest `starters/AGENTS.snippet.md` on GitHub; offer the new text, don't replace it unasked
  → if a step fails (no network, a dirty clone), stop and report it. Don't half-upgrade.
- [ ] Read the kit's changelog entries newer than the installed version (`changelog/` in the repo: https://github.com/lossless-group/context-vigilance-kit/tree/master/changelog) and summarized what changed in a few lines, new commands first

## 2. Offer to bring this repo up to date

New kit versions sometimes add conventions, such as a required field or a new index file. Existing docs are **never** changed as a side effect (the drift policy). Instead:

- [ ] Checked this repo's `context-v/` against the current conventions and listed only what differs, with counts. Examples:
  - docs with no `type` (or a `type` that isn't the folder's name)
  - `context-v/README.md` with no `context-v/index.md`
  - folders with no `index.md`
  - new commands the repo's `AGENTS.md` snippet doesn't mention
- [ ] Offered each as its own choice: "Add `type` to 23 docs?" Do only what the user picks, as one focused pass per change.
- [ ] After any pass, re-checked that every touched doc's frontmatter parses

## Notes

- **exact:** never skip the reload step for the plugin; never rewrite docs without a yes.
- If the user only wants the kit updated, stop after part 1.
