---
name: implement
description: Acts as a hands-on lead engineer to build a signed-off context-v spec or plan in one session, gating on checkable acceptance criteria, then implementing, verifying by running things, and iterating until every criterion passes or a real blocker appears. Closes the doc's status honestly. Use when the user asks to implement, build, or execute a specific spec or plan.
argument-hint: <path to a spec or plan>
disable-model-invocation: true
---

# implement: build a spec or plan

**Role: lead engineer, hands on.** The PM (`prep`) produced the doc; you build it without re-arguing the why. For larger work with subagents, use `loop` instead.

Target: `$ARGUMENTS`.

## Checklist

Copy this into your reply and tick as you go:

- [ ] Read the target in full, plus what it links as load-bearing (its spec, blueprints, reminders)
- [ ] **Gate:** it has acceptance criteria someone can check
      → if not, stop and send it back to `prep`. Building against an uncheckable doc is the failure this skill exists to prevent.
- [ ] Set `status: Implementing` and bumped `date_modified`
- [ ] For each phase or step, in order:
  - [ ] Built it, matching the surrounding code
  - [ ] **Verified by running it** (build, tests, run it and watch output, click through UI). "The code exists" isn't verification.
        → if it fails, fix and re-verify before moving on
  - [ ] Committed in the repo's style, if the user wants commits per step
- [ ] Every acceptance criterion re-checked at the end
      → any failing: back to the step that owns it
- [ ] Closed honestly:
  - all met → `status: Shipped`, `date_first_published`
  - stopping early → `status: Partially-Shipped` and `## Remaining work (as of YYYY-MM-DD)`
  - blocked → report the blocker; never mark shipped on hope
- [ ] Suggested `reflect` to write up, hand off, and ship

## Notes

- **Stay in scope.** Something the doc didn't anticipate goes back to `prep` as a question. Don't absorb it silently.
- **exact:** the gate, verification by running, honest status. **open:** how to build each step.
- In harnesses with a loop runner (e.g. Claude Code's `/loop`), this checklist works as the iteration body.
