---
name: new
description: Creates a new context-v document from the matching template, with a Train-Case filename, minted site_uuid and hex_code, today's dates, and the author from git config. Types are spec, plan, prompt, blueprint, reminder, exploration, issue, loop, and handoff. Use when the user asks to start, create, or write a new spec, plan, exploration, issue, or other context-v doc.
argument-hint: <type> "<Title>"
---

# new: create a context-v doc

Arguments: `$ARGUMENTS`, as `<type> "<Title>"`. If the type or title is missing, ask for it in one short question.

Templates are in the `context-vigilance` skill's `templates/` folder. Follow that skill's frontmatter rules; this skill only covers the mechanics.

## Checklist

Copy this into your reply and tick as you go:

- [ ] Type is one of: spec, plan, prompt, blueprint, reminder, exploration, issue, loop, handoff
      → if not, suggest the closest and ask
- [ ] Found `context-v/` (walk up from the current folder)
      → if none exists, offer to run `init` first; don't create a stray folder
- [ ] **Issue only:** if `context-v/config.md` sets `tracker.issues` to `tracker` or `both`, also file (or offer to file) a ticket through the configured tool, and put its URL in `tracker_url`. Ask before posting unless the config says `confirm: never`.
- [ ] Filename: the title in Train-Case, `.md`, in the type's folder (`issues/`, `specs/`…). Handoffs: prefix with the date, `YYYY-MM-DD_Title.md`.
      → if the file exists, stop and ask; never overwrite
- [ ] Copied the template and filled the frontmatter:
  - `title`; today's date for all four `date_*` fields that take one
  - `authors` from `git config user.name`
  - `augmented_with`: your harness and model
  - `site_uuid`: run `uuidgen | tr 'A-Z' 'a-z'` · `hex_code`: run `LC_ALL=C tr -dc 'a-z0-9' </dev/urandom | head -c6`
- [ ] Removed or filled every placeholder (`TITLE HERE`, `YYYY-MM-DD`, `AUTHOR`, `HARNESS on MODEL`, `GENERATE`)
      → re-read the frontmatter; if any placeholder remains or the YAML doesn't parse, fix it
- [ ] Wrote what you already know into the body (the user's words, the why). Left the rest as the template's prompts. Don't invent content.
- [ ] Linked it to related docs, and told the user the path

## Notes

- **exact:** filename casing, IDs by command, never overwrite.
- **shaped:** the template's sections; drop ones that don't apply.
- A brand-new doc usually stays `publish: false` and gets no `lede` until it has a body worth hooking.
