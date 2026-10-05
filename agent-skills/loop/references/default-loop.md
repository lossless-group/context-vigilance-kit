# The default loop

A professional baseline to start from, not a standard to impose. Propose it, ask what the developer would change, and save their version with the `loop` template. It's drawn from loops proven in practice and from public subagent-driven development patterns.

## Contents

- Setup · Per package · Rules · Exit · Why each piece is there

## Setup (once per run)

1. Load the target spec or plan and everything it marks as load-bearing.
2. Gate: checkable acceptance criteria exist. If not, back to `prep`.
3. Set the target `status: Implementing`.
4. Break the work into **packages**: each with a done-condition, a file scope, and what it must not touch. Mark which are independent.
5. If the repo keeps a changelog, open today's entry; package notes ("beats") get appended as the run goes.
6. If a tracker is configured, open or link one ticket per package.

## Per package

1. **Brief** a fresh implementer subagent: scope, files, done-condition, conventions, what not to touch. A fresh context per package keeps the work sharp.
2. **Build.** The implementer reports what it changed and how it checked it.
3. **Review**, by a separate reviewer subagent, from the diff, in two passes: does it meet the brief and the spec? Then, is the code good? The reviewer is told not to trust the implementer's report.
   → fails: back to Build with the reviewer's notes
4. **Verify by running things**, cheapest first: typecheck and lint → tests → run it and watch the output → click through any UI.
   → fails: back to Build. The same blocker twice in a row: stop, escalate.
5. **Integrate**: one commit per package in the repo's style; append a changelog beat while the details are fresh; close the ticket with the commit hash.

## Rules

- The implementer is never its own reviewer.
- Parallel packages only when they share no files (separate worktrees if the harness supports them). When unsure, go one at a time.
- Scope creep becomes a new package or goes back to `prep`. It never widens the current package.
- Evidence over claims: "tests pass" means the output was seen.

## Exit

1. All acceptance criteria met and verified.
2. **Human gate**: hand the user a short click-path or command list to judge usability. Their findings become packages.
3. Hand off to `reflect`.

## Why each piece is there

| Piece | Failure it prevents |
|---|---|
| Fresh subagent per package | Quality decay as one context fills up |
| Separate reviewer, told not to trust the report | "Done" that isn't |
| Verify by running | Code that compiles in the author's head only |
| One commit per package | History nobody can bisect or explain |
| Escalate on a repeated blocker | Burning a session on the same wall |
| Human gate | Software that works and nobody can use |
