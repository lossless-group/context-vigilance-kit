# Relocation Safety

Supporting detail for the HARD STOP checklist in `SKILL.md`. The three preconditions
and their commands live there; this file covers what to say, how to find every secret,
how to do the move itself, and how to recover when a move already went wrong.

## Contents

- Why moves lose data
- The message to send the user
- Finding every variable the code reads
- A safe move sequence
- Recovery: when the move already happened

## Why moves lose data

Git only protects what has reached a remote. A relocation usually means "clone fresh at
the new path, delete the old directory," and everything that lived only in the old
directory goes with it:

| Lost with the old directory | Why it's easy to miss |
|---|---|
| Local-only branches | `git status` on the current branch looks clean |
| Unpushed commits on tracked branches | Only visible in `git branch -vv` as `[ahead N]` |
| Uncommitted edits and untracked files | Often in a branch nobody is looking at |
| Stashes | Invisible unless you run `git stash list` |
| `.env`, `.env.local`, `secrets/`, local config | Gitignored by design, so never on any remote |

A second, quieter failure: the fresh clone checks out the remote's default branch,
which may be weeks behind the branch where work actually happened. Everything looks
present until someone notices features are missing.

## The message to send the user (exact structure, adapt the values)

> Before I touch this: moving a repo is the riskiest routine operation in a multi-repo
> tree, because a fresh clone only brings back what was pushed. Three checks, and I'd
> like a separate yes on each:
>
> 1. **Local branches synced.** `git branch -vv` shows `feature/search` is `[ahead 3]`
>    and there is 1 stash. Push and commit those, or confirm they can be lost?
> 2. **Remote branches catalogued.** The remote has `main`, `development`. Locally there's
>    also `spike/ranking`, which was never pushed. Push it or confirm it's disposable?
>    (Most recent work is on `development`; the new clone should check that out.)
> 3. **Secrets backed up.** There's a `.env` here. The code reads `DATABASE_URL`,
>    `SESSION_SECRET`, `STRIPE_KEY`, `SEARCH_API_KEY`; `.env.example` only lists the
>    first two. Where is the copy you'd restore from?
>
> Once each of these is resolved I'll do the move, and I'll verify the new copy builds
> before anything is deleted.

Do not collapse this into "everything looks fine, proceeding." Even when all three
checks pass cleanly, report each result and wait for acknowledgment.

## Finding every variable the code reads

`.env.example` drifts. The source is the truth. Run what fits the project's languages
from the repo root, then compare against the keys in the actual `.env`:

```bash
# JavaScript / TypeScript (Node, Vite, Astro, Next, etc.)
grep -rhoE '(process\.env|import\.meta\.env)\.[A-Z_][A-Z0-9_]*' \
  --include='*.js' --include='*.ts' --include='*.mjs' --include='*.jsx' --include='*.tsx' \
  --exclude-dir=node_modules --exclude-dir=dist . | sort -u

# Python
grep -rhoE "os\.(environ(\.get)?\(|getenv\()['\"][A-Z_][A-Z0-9_]*|os\.environ\[['\"][A-Z_][A-Z0-9_]*" \
  --include='*.py' --exclude-dir=.venv . | sort -u

# Ruby, Go, Elixir, shell (broad net)
grep -rhoE "ENV\[['\"][A-Z_][A-Z0-9_]*|os\.Getenv\(\"[A-Z_][A-Z0-9_]*|System\.get_env\(\"[A-Z_][A-Z0-9_]*|\\\$\{?[A-Z_][A-Z0-9_]{2,}" \
  --exclude-dir=node_modules --exclude-dir=vendor . | sort -u

# Keys actually present in the local env file(s), values hidden
grep -hoE '^[A-Z_][A-Z0-9_]*' .env* 2>/dev/null | sort -u
```

Also check config files that read the environment indirectly (framework configs, docker
compose files, CI workflow files) and the hosting provider's environment panel.

Watch for **aliases**: the same value under several historical names (for example
`DATABASE_URL`, `DB_URL`, and `POSTGRES_URL` all pointing at one database). The source
shows all of them; the example file may show one.

## A safe move sequence (shaped)

1. Pass all three preconditions, each acknowledged separately.
2. Copy secrets to a location **outside** the directory being moved (or confirm the
   user's backup).
3. Create the new location: a fresh clone (`git clone`, or `git submodule add` in the
   new parent), or a plain `mv` of the whole working copy when the git history and
   gitignored files should travel together.
4. In the new copy: check out the tip branch, restore secrets, install, build, run tests.
5. If the repo was a submodule, update both parents: remove the old entry
   (`git submodule deinit`, `git rm`), add the new one, set `branch =` in `.gitmodules`,
   run `git submodule sync`.
6. Only after the new copy is verified, and with the user's go-ahead, delete the old directory.
   Prefer moving it to the trash or an archive folder over `rm -rf`.

## Recovery: when the move already happened

If you arrive after a move (fresh clone, no `.env`, missing work):

1. **Look for a surviving working copy.**
   ```bash
   find ~ -type d -name '<repo>' -not -path '*/node_modules/*' 2>/dev/null
   ls ~/.Trash 2>/dev/null | grep -i '<repo>'          # macOS trash
   ls ~/.local/share/Trash/files 2>/dev/null | grep -i '<repo>'   # Linux trash
   ```
   Editor and agent caches sometimes name directories after the old absolute path
   (for example Claude Code's `~/.claude/projects/`), which can reveal where the old
   copy lived.
2. **Rebuild the variable list from source** with the recipes above, then pull values
   from the hosting provider's env panel, a password manager, or teammates.
3. **Find the real tip branch.** The new clone may be on a stale default branch.
   ```bash
   git fetch --all
   git log --all --pretty=format:'%h %ad %d %s' --date=iso | head -40
   ```
   Check out whichever branch holds the most recent work.
4. **Tell the user what could not be recovered.** A clear list of gaps beats a silent
   partial restore.
