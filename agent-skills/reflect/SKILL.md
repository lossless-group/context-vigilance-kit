---
name: reflect
description: Closes a cycle of work so the next session can start cold. Discusses what happened with the user, then records the as-built state and honest status in the spec or plan, files the issues found (context-v/issues/ or the configured tracker), writes a changelog entry and a handoff, cuts a release when asked, and commits with a ship(feature, capability) header and pushes. Use after implement or loop, at the end of a working session, or when the user says "wrap up", "reflect", "write it up", or "ship it".
argument-hint: "[path to the spec or plan just built]"
disable-model-invocation: true
---

# reflect: close the cycle

**Role: the engineering lead closing out.** Everything below lands in **one** `ship()` commit, so the order matters.

Target: `$ARGUMENTS`, or the spec or plan this session worked on.

## Checklist

Copy this into your reply and tick as you go:

- [ ] **Discussed before writing.** Said what you observed: built vs. planned, workarounds, what broke. Then asked the user two or three questions: what felt awkward to use, what surprised them, what they'd do differently.
- [ ] **As built.** Added an as-built section to the spec or plan covering where reality diverged from the plan, and set status honestly (`Shipped` + `date_first_published`, or `Partially-Shipped` + `## Remaining work (as of YYYY-MM-DD)`)
- [ ] **Issues filed.** Each real problem hit, filed per `context-v/config.md`'s `tracker` (default: a `context-v/issues/` doc via `new issue`, with its hypothesis log). Usability problems the same way, or as explorations if they're open questions.
      → anything outward-facing (a ticket, a chat post): ask first unless the config says otherwise
- [ ] **Next steps** written into the doc's remaining-work section, or as stub explorations or plans. Not left only in chat.
- [ ] **Changelog entry** written, if the repo keeps `changelog/` (see [references/changelog-entry.md](references/changelog-entry.md)). If `loop` left beats, polish them.
- [ ] **Handoff** written with `new handoff`: what landed, what's mid-flight, what the next session must know, what to load first
- [ ] **Diagram (optional):** if Archify is installed and the system's shape changed, offered an as-built diagram
- [ ] **Graph (optional):** if `graphify-out/` exists, offered to refresh it
- [ ] **Release (only if asked, or the user agrees it's a release):** found where the repo keeps its version (package manifest, plugin manifest, tags); don't assume. Bumped it, wrote release notes from the changelog entries since the last tag, tagged.
- [ ] **Re-checked** that every new or edited doc's frontmatter parses and has no placeholders left
      → if not, fix it before committing
- [ ] **Commit**, using the repo's own convention if it has one, otherwise [references/ship-commit.md](references/ship-commit.md): `ship(feature, <capability>): <what someone can now do>`
      → if the changelog or handoff isn't staged, go back and stage it
- [ ] **Push.** Said which branch is going to which remote first. Never force-push. Confirm before pushing straight to a default or protected branch.
- [ ] If `context-v/config.md` has a `chat` role with `post_on` including `ship` or `release`, offered the post

## Notes

- **exact:** the order (docs before commit), honest status, ask before anything outward-facing, no force-push.
- **open:** what to say in the as-built, changelog, and handoff.
- `reflect` without a target works at the end of any session: skip the as-built step and write the handoff.
