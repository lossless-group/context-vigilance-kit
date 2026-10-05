# Status Discipline for `context-v/` Documents

**Contents:** The problem this addresses · The status values · The lifecycle · Companion fields · The `## Remaining work` section · When to update status · When NOT to update status · Sweep cadence · Anti-patterns

> The `status:` field is the load-bearing signal of where a document sits in its lifecycle. A directory full of `status: Draft` plans, half of which actually shipped, is a directory you can't trust.

## The problem this addresses

`context-v/` accumulates plans, specs, explorations, and prompts over months. Without a status convention, every doc stays at its authored-day default (`Draft`) forever, and an agent landing cold cannot tell what's shipped (historical), what's in flight (needs attention), what was deliberately deferred (*not* a gap), and what's stale.

The discipline: **every meaningful state change on a document is reflected in `status:`, with companion fields that explain when, why, and what's left.**

## The status values

`status:` is a **Train-Case display string** for humans, not a machine enum. Don't switch on its values in code; spelling and casing drift across files.

| Value | Meaning |
|---|---|
| `Draft` | Authored, not yet executed. Default for new files. |
| `In-Review` | Drafted and being discussed/refined before execution. Mostly specs. |
| `Signed-Off` | Sign-off received; execution authorized. Spec-specific. |
| `Implementing` | Execution in progress. |
| `Shipped` | All deliverables landed; nothing material remains. |
| `Partially-Shipped` | Some deliverables landed, others did not. Requires a `## Remaining work` section (below). |
| `Deferred` | Explicitly on hold for a named reason (a dependency, a pending decision). Not stale, not abandoned. Requires `deferral_note:`. |
| `Stale` | No longer reflects current direction, not yet retired. Use sparingly; `Superseded` or `Archived` is usually better. |
| `Superseded` | Replaced by a newer document. Requires `superseded_by:`. |
| `Archived` | Retired. Kept for the record, no longer load-bearing. |

Project-specific values are fine if they earn their keep. Use Train-Case and document the meaning in the project's agent instructions (`AGENTS.md`, `CLAUDE.md`) or a reference doc.

## The lifecycle

```
Draft → (In-Review →) (Signed-Off →) Implementing → Shipped        # happy path
Draft → Implementing → Partially-Shipped → … → Shipped            # partial outcome
Draft → Deferred → [later: Implementing → Shipped | Superseded | Archived]
```

**Status reflects reality**; not every doc passes through every value. A plan that ships in the session it was written goes straight from `Draft` to `Shipped`.

## Companion fields

When status changes, its companion fields change in the same edit.

| When status is | Required companion fields |
|---|---|
| `Draft` / `In-Review` | none |
| `Shipped` | `date_first_published: YYYY-MM-DD` (the ship date); optionally `post_ship_note:` for things learned after ship, and `date_work_completed:` if known |
| `Partially-Shipped` | `date_first_published:` for the first shipped slice; a `## Remaining work (as of YYYY-MM-DD)` section at the end of the body |
| `Deferred` | `deferral_note:` naming the reason and any expected unblocker |
| `Superseded` | `superseded_by: [[Successor-Doc]]` (and `supersedes:` on the successor) |
| `Stale` / `Archived` | optional `archive_note:` if context isn't obvious |

In every case, **update `date_modified` (and `date_last_updated` if the file uses it) in the same edit.** Status changes are meaningful edits.

## The `## Remaining work` section

For `Partially-Shipped` docs, append at the end of the body:

```markdown
## Remaining work (as of YYYY-MM-DD)

This plan is partially shipped. What's done and what's left:

### Shipped
- **Step / phase name.** One-line description of what landed.

### Not yet shipped
- **Step / phase name.** What it is, why it's still outstanding, any blocker.

### Side artifacts this plan produced
- Optional. Ancillary deliverables that ended up belonging elsewhere.
```

The heading date anchors the snapshot. When another slice ships, update the section in place (don't add a second one) and bump the date. When everything ships, set `status: Shipped`, optionally fold the section into `post_ship_note:`, and remove it.

## When to update status

1. **You ship a substantial portion** of the deliverables. Don't wait for 100%; `Partially-Shipped` exists for the in-between.
2. **You explicitly defer** a plan. Set `Deferred` and write the `deferral_note`.
3. **You replace** a doc. Set `Superseded` on the old one with `superseded_by:`, and `supersedes:` on the new one.
4. **You're doing a status sweep** (below) and find a doc whose status doesn't match reality.

## When NOT to update status

- **As a side effect of unrelated work.** Surface the gap to the user; don't silently normalize.
- **On docs someone else authored** whose ship-state you're unsure of. Ask first.
- **To "tidy up"** without confirming the work shipped. `Shipped` is a claim that should map to a real event: a commit, a release tag, a changelog entry.

## Sweep cadence

A periodic status sweep through a project's `context-v/` pays off, typically before authoring a new plan (to see what's already live) or after a coherent chunk of work lands. The procedure: list docs whose status is `Draft`, `In-Review`, `Implementing`, or `Partially-Shipped`; for each, check the commits, releases, or changelog for evidence of shipping; propose the status changes and companion fields to the user; apply the ones they confirm.

## Anti-patterns

- **`Draft` forever.** Plans that shipped weeks ago still say `Draft`. → Sweep and promote.
- **`Shipped` without `date_first_published`.** No anchor for "when." → Add the date.
- **`Partially-Shipped` without `## Remaining work`.** The point is to enumerate what's left. → Write the section.
- **`Deferred` with no `deferral_note`.** "Why, and for how long?" must be answerable. → Add the note.
- **Silent status changes during unrelated edits.** → Surface, don't normalize.
- **Promoting status without a ship event.** → Point to a real commit, release, or changelog entry.

See also `frontmatter-spec.md` (field definitions) and `developing-a-spec.md` (the spec-specific progression).
