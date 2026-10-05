---
name: kickoff
description: Loads the right context-v documents at the start of a working session. Reads the latest handoff, asks which docs are known to be relevant, and on request searches context-v/ (and a graphify map, if one exists) to propose a short reading list sorted into must-read, keep-handy, and ignore. Use at the start of a session, after a context reset, or when the user says "get up to speed", "load context", or "where were we".
---

# kickoff: load the right context

The goal is a session that starts *informed* with a small reading list, not one that reads everything.

## Checklist

Copy this into your reply and tick as you go:

- [ ] Found `context-v/` (walk up; in a tree of repos, note parent and child `context-v/` folders too, per `pseudomonorepos`)
- [ ] Read `context-v/index.md`, and the `index.md` of any folder that looks relevant: they list every doc with a one-line description, so you can see what exists before opening anything
- [ ] Read the newest file in `context-v/handoffs/`, if any, and summarized it in three lines
- [ ] Asked: "Any docs you already know are relevant?" Then one of:
  - **The user lists files** → read them; skip to the last step
  - **"Help me find"** → continue below
  - **"No context needed"** → stop here
- [ ] If `graphify-out/GRAPH_REPORT.md` exists, read it first: it's a map of the codebase
- [ ] Searched `context-v/` for the topic: index entries first, then filenames, `type`, titles, `description`, `tags`, and `status` (frontmatter is cheap to scan; don't read whole bodies yet)
- [ ] If `context-v/config.md` names a `context.retrieval` tool (e.g. Chroma) and it's available, queried it too
- [ ] Proposed three buckets, a few files each, with one line on why:
  - **Must read**: load now
  - **Keep handy**: load when the work touches it
  - **Ignore**: looked relevant, isn't
- [ ] Read the must-reads the user confirmed; said what's loaded and what the next step looks like

## Notes

- **open:** what counts as relevant; bucket sizes. Prefer five good files over twenty.
- `status: Superseded` or `Archived` docs go in Ignore unless the user is asking about history; point at `superseded_by` instead.
- If nothing matches, say so plainly. Don't pad the list.
- If `graphify-out/` is missing and the repo has real code, mention once that the optional `graphify` companion builds a codebase map (see the kit's README, "Recommended companions"). Don't install it unasked.
