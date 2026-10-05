---
name: loop
description: Runs a signed-off spec or plan as a team. The primary agent acts as VP of Engineering, breaking the work into packages, briefing implementer subagents, getting independent reviews, verifying, and integrating, under the developer's own process. It first finds or clarifies that process and saves it as a loop doc in context-v/loops/, so later runs reuse it. Use when the user asks to loop, run a team, use subagents, or build a larger spec or plan end to end.
argument-hint: <path to a spec or plan>
disable-model-invocation: true
---

# loop: build it as a team, under a clarified process

**Role: VP of Engineering.** You break the work down, staff it, review it, integrate it, and escalate. You **don't write the code yourself**, apart from trivial glue. Subagents build, each following the `implement` checklist on its own slice.

**The process is the developer's, not ours.** Every team works differently, so this skill doesn't impose a loop. It finds the developer's, or helps them say it, writes it down, and then follows it.

Target: `$ARGUMENTS`.

## 1. Find or clarify the loop

- [ ] Looked in `context-v/loops/` for a loop that fits this work, and in `AGENTS.md` for stated process
      → if one fits, use it and skip to step 2
- [ ] Otherwise proposed the default loop ([references/default-loop.md](references/default-loop.md)) and asked only what changes it:
  - How deep should review go?
  - What counts as verified here (typecheck, tests, a browser click-through, a human walkthrough)?
  - One commit per package, or per phase?
  - Is parallel work allowed?
  - Where's the human gate?
- [ ] Wrote the result as `context-v/loops/<Name>.md` from the `loop` template, `status: Draft`, **before running it**
- [ ] Tool questions (where tickets go, where to post updates) went into `context-v/config.md` as roles, not into the loop doc

## 2. Run it

- [ ] **Gate:** the target has checkable acceptance criteria → if not, back to `prep`
- [ ] Set the target `Implementing`; broke it into work packages, each with a done-condition and a file scope; marked which are independent
- [ ] Per package, the loop doc's iteration: brief → build → independent review → verify → integrate. Copy its checklist per package.
- [ ] Held the rules:
  - the implementer never reviews its own work
  - parallel work only on packages that share no files
  - scope creep becomes a new package or goes back to `prep`
  - the same blocker twice in a row means stop and escalate to the user
- [ ] Wrote any process problem back into the loop doc's *Lessons from runs*. Don't just fix it in place.

## 3. Exit

- [ ] All criteria met, verification green, human gate passed (findings re-enter as packages)
- [ ] Loop doc promoted `Draft` → `Proven-Once` after its first clean run
- [ ] Handed off to `reflect`

## Without subagents

If your harness can't start subagents, run the same loop in one session with explicit role switches ("Now reviewing as the reviewer, from the diff, not my memory of writing it"). Say up front that this is weaker than a fresh reviewer.

## Notes

- **exact:** the gate, separate review, verification by running, the escalation rule. Everything else is whatever the loop doc says.
- Harness extras (worktrees, agent teams, Claude Code's `/loop` for pacing) are welcome when present and never required.
