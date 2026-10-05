# Branch Alignment Across Submodules

How to keep a parent repo and its submodules on consistent branches, and how to fix
the common ways they drift apart.

## Contents

- Pick a tier model
- The alignment expectation
- When a submodule lacks a tier
- When a tier is behind
- When a tier is ahead
- Sync .gitmodules after changes
- Pushing to protected branches
- Drift

## Pick a tier model (open)

Use whatever branch model the team already has. If there is none, these are common:

| Model | Branches | Fits |
|---|---|---|
| Trunk | `main` only, short-lived feature branches | Small teams, continuous deploy |
| Two-tier | `development` → `main` | Work-in-progress separate from releasable |
| Three-tier | `development` → `main` → `master` (or `stable`) | Separate "noteworthy" from "settled" |

In the three-tier example: most commits land on `development`; it's promoted to `main`
when something noteworthy is ready; `main` is promoted to `master`/`stable` only once
it has proven stable. In practice the top tier is often the stalest branch, and that's
fine.

## The alignment expectation (shaped)

When the parent is on a given tier, each submodule should be on the same tier:

```
parent on development  →  every submodule on development
parent on main         →  every submodule on main
```

Mixed tiers make the parent's gitlinks hard to reason about and break any "switch every
child to X" script. Check the parent's root or `scripts/` folder for such a script before
writing one.

To see where everything currently sits:

```bash
git branch --show-current
git submodule foreach --quiet 'echo "$sm_path: $(git branch --show-current || echo DETACHED)"'
```

## When a submodule lacks a tier

Repos often have only `main` or only `master`. When a tier is needed, create it from the
leading branch. This is non-destructive (a new branch, no force push):

```bash
# inside the submodule: development is missing, main is leading
git fetch origin
git branch development origin/main
git push -u origin development
```

## When a tier is behind

If the submodule's `development` is behind `main`, the parent expects `development`, and
the branches have not diverged, fast-forward `development`:

```bash
# confirm it is a pure fast-forward first
git rev-list --count origin/development..origin/main   # > 0: main has new commits
git rev-list --count origin/main..origin/development   # must be 0
git push origin origin/main:development                 # fast-forward on the remote
```

- → If both counts are non-zero, the branches have diverged. Stop and report; don't merge
  or force on your own.
- Switching the submodule to a stale branch instead would roll the parent's gitlink
  backward. Don't do that without explicit direction.

## When a tier is ahead

`development` ahead of `main` just means unpromoted work. Leave it. Promotion between
tiers is a human decision.

## Sync .gitmodules after changes (exact)

When a submodule starts tracking a different branch:

```bash
git config -f .gitmodules submodule.<path>.branch development
git submodule sync
git add .gitmodules <path>
```

Then commit the `.gitmodules` change and the submodule pointer together. An entry with
no `branch =` line means `git submodule update --remote` falls back to the remote's
default branch, which may not be what the team intends.

## Pushing to protected branches

Default branches are often protected. Push to the working tier or a feature branch and
let a human merge upward. If WIP needs a safe home before a risky operation (such as a
relocation), push it to the working tier or a `wip/` branch, fast-forwarding first if needed.

## Drift

Trees drift out of alignment over time. Observe and report, but don't realign as a side
effect of unrelated work: realignment touches shared remotes and can break other people's
(or other sessions') work. Treat it as its own, explicitly authorized task.
