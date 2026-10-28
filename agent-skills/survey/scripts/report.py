#!/usr/bin/env python3
"""Write SURVEY.md, the agent-readable report, from a survey.json.

  python3 report.py path/to/survey.json [--out SURVEY.md]

Stage two of the survey, the text half (the HTML renderers are the other half).
Bounded on purpose: caps every list so a whole-tree report stays under ~600 lines.
"""
import argparse
import collections
import datetime as dt
import json
import os
import sys

BUCKETS = ["open", "in_flight", "done", "parked", "closed", "reference", "unmapped", "none"]
LABEL = {"open": "Open", "in_flight": "In flight", "done": "Done", "parked": "Parked",
         "closed": "Closed", "reference": "Reference", "unmapped": "Unmapped", "none": "No status"}


def cell(text):
    return str(text or "").replace("|", "\\|").replace("\n", " ")


def link(doc):
    return f"[{cell(doc['title'])}]({doc['path']})"


def days_ago(date, today):
    try:
        return (today - dt.date.fromisoformat(date)).days
    except (TypeError, ValueError):
        return None


def changed(doc):
    """Best date the doc last moved: its last commit inside the git window, else frontmatter."""
    return doc.get("last_commit") or doc["updated"]


def ours(s):
    """Repos where the operator (`git config user.name` at the scope root) committed in the
    last 30 days. Forks and pinned upstream repos carry other people's commits and would
    distort "who's moving"; a remote's owner can't tell them apart from client-owned repos."""
    me = s.get("operator")
    return {r["path"] for r in s["repos"]
            if r.get("activity") and (me is None or me in r["activity"]["authors_30"])}


def momentum(s, by_repo, d30):
    mine = ours(s)
    rows = [r for r in s["repos"] if r["path"] in mine and r["activity"]["commits_30"]]
    rows.sort(key=lambda r: -r["activity"]["commits_30"])
    out = ["## Momentum (last 30 days)", "",
           "Who is moving, by commits. Agent-assisted means a `Co-Authored-By` agent trailer.", "",
           "| Repo | 7d | 30d | Agent-assisted | context-v commits | Docs added | Docs closed | In flight |",
           "|---|---:|---:|---:|---:|---:|---:|---:|"]
    for r in rows[:25]:
        a, ds = r["activity"], by_repo.get(r["path"], [])
        closed = sum(1 for d in ds if d["bucket"] == "done" and changed(d) >= d30)
        out.append(f"| `{r['path']}` | {a['commits_7']} | {a['commits_30']} | "
                   f"{round(100 * a['agent_assisted_30'] / a['commits_30'])}% | {a['cv_commits_30']} | "
                   f"{a['docs_added_30']} | {closed} | {sum(1 for d in ds if d['bucket'] == 'in_flight')} |")
    quiet = [r["path"] for r in s["repos"] if r.get("activity") and r["docs"] and not r["activity"]["commits_30"]]
    if quiet:
        out += ["", f"Quiet for 30 days, with docs: " + ", ".join(f"`{p}`" for p in quiet[:20])
                + (f", …{len(quiet) - 20} more" if len(quiet) > 20 else "") + "."]
    people, agents = collections.Counter(), collections.Counter()
    for r in s["repos"]:
        if r["path"] in mine:
            people.update(r["activity"]["authors_30"])
            agents.update(r["activity"]["agents_30"])
    out += ["", "People: " + (", ".join(f"{n} ({c})" for n, c in people.most_common(10)) or "none") + ". "
            "Agents: " + (", ".join(f"{n} ({c})" for n, c in agents.most_common(5)) or "none") + "."]
    upstream = [r["path"] for r in s["repos"] if r.get("activity") and r["path"] not in mine
                and r["activity"]["commits_30"]]
    if upstream:
        out.append(f"Left out, active without {s.get('operator') or 'the operator'} (forks, pinned upstream): "
                   + ", ".join(f"`{p}`" for p in upstream[:10]) + ".")
    return out + [""]


def options(s, docs, d30):
    act = {r["path"]: (r.get("activity") or {}) for r in s["repos"]}

    def readiness(d):
        notes = []
        notes.append("criteria ✓" if d["has_acceptance"] else "no criteria")
        notes.append(d["maturity"])
        if d["tasks_open_count"]:
            notes.append(f"☐ {d['tasks_open_count']}")
        notes.append(f"repo {act.get(d['repo'], {}).get('commits_30', 0)}c/30d")
        return " · ".join(notes)

    def score(d):
        a = act.get(d["repo"], {})
        return ((2 if d["has_acceptance"] else 0) + {"worked-on": 2, "idea-started": 1}.get(d["maturity"], 0)
                + (1 if changed(d) >= d30 else 0) + (1 if a.get("commits_30") else 0)
                - (2 if "stale" in d["flags"] else 0))

    def block(title, items, n, blurb):
        items = sorted(items, key=lambda d: (score(d), changed(d)), reverse=True)
        lines = [f"### {title} ({len(items)})", "", blurb, ""]
        lines += [f"- {link(d)} · `{d['repo']}` {d['folder']} · {cell(d['status'])} · "
                  f"{changed(d)} · {readiness(d)}" for d in items[:n]]
        if len(items) > n:
            lines.append(f"- …and {len(items) - n} more")
        return lines + [""]

    work = [d for d in docs if d["folder"] in ("specs", "plans", "prompts", "issues", "explorations")]
    stalled = [d for d in work if d["bucket"] == "in_flight" and not d["assignable"]
               and (changed(d) < d30 or not act.get(d["repo"], {}).get("commits_30"))]
    out = ["## Option set: work you could assign", "",
           "Ranked by readiness: acceptance criteria, how developed the doc is, recent change, "
           "and whether its repo is moving.", ""]
    out += block("Ready to assign", [d for d in work if d["assignable"]], 15,
                 "Signed off or marked ready, nobody building yet.")
    out += block("Needs your decision", [d for d in work if d["needs_decision"]], 10,
                 "In review or proposed: a sign-off unlocks them.")
    out += block("Open issues", [d for d in work if d["folder"] == "issues" and d["bucket"] == "open"], 15,
                 "Unresolved problems, freshest and best-documented first.")
    out += block("Stalled in flight", stalled, 10,
                 "Marked in flight, but untouched for 30 days or in a quiet repo: reassign, or close honestly.")
    return out


def cleanup(docs):
    out = ["## Cleanup worklist", "",
           "The survey never edits a doc. These are candidates for a deliberate pass.", ""]

    def block(title, items, n, blurb, key=lambda d: changed(d)):
        items = sorted(items, key=key)
        lines = [f"### {title} ({len(items)})", "", blurb, ""]
        lines += [f"- {link(d)} · `{d['repo']}` · {cell(d['status']) or 'no status'} · {changed(d)} · "
                  f"{d['prose_words']} words" for d in items[:n]]
        if len(items) > n:
            lines.append(f"- …and {len(items) - n} more")
        return lines + [""]

    out += block("Empty: delete or complete", [d for d in docs if "empty" in d["flags"]], 15,
                 "A title and headings, almost no prose.")
    out += block("Stale stubs: close, defer, or finish",
                 [d for d in docs if d["maturity"] == "stub" and "stale" in d["flags"] and "empty" not in d["flags"]],
                 15, "Under 100 lines, open or in flight, untouched for the stale window. Oldest first.")
    out += block("Probably done, still open", [d for d in docs if "maybe_done" in d["flags"]], 15,
                 "Every checkbox is ticked but the status says open or in flight.")
    fixes = collections.Counter(f for d in docs for f in d["flags"]
                                if f in ("yaml_error", "no_frontmatter", "unmapped_status", "no_status",
                                         "type_mismatch", "no_title", "no_lede"))
    out += ["### Metadata fixes", ""]
    for f, n in fixes.most_common():
        examples = [d["path"] for d in docs if f in d["flags"]][:3]
        out.append(f"- `{f}` ×{n}: " + ", ".join(f"`{e}`" for e in examples))
    pre = sum(1 for d in docs if "no_type" in d["flags"])
    if pre:
        out.append(f"- Pre-OKF (no `type:`) ×{pre}: one scripted pass, since `type` is just the folder name.")
    return out + [""]


def render(s):
    docs, today = s["docs"], dt.date.fromisoformat(s["generated_at"][:10])
    by_repo = collections.defaultdict(list)
    for d in docs:
        by_repo[d["repo"]].append(d)
    total = collections.Counter(d["bucket"] for d in docs)
    stale = [d for d in docs if "stale" in d["flags"]]
    open_tasks = sum(d["tasks_open_count"] for d in docs if d["task_folder"])

    out = [
        f"# Survey: {s['root_name']} ({s['scope']} scope)",
        "",
        f"Generated {s['generated_at']} from `{s['root']}`. "
        f"{len(docs)} docs in {sum(1 for r in s['repos'] if r['docs'])} repos with a `context-v/` "
        f"({len(s['repos'])} repos scanned). Stale means open or in flight and untouched for "
        f"{s['stale_days']}+ days.",
        "",
        "| " + " | ".join(LABEL[b] for b in BUCKETS) + " | Stale | Open checkboxes |",
        "|" + "---:|" * (len(BUCKETS) + 2),
        "| " + " | ".join(str(total.get(b, 0)) for b in BUCKETS) + f" | {len(stale)} | {open_tasks} |",
        "",
    ]

    rows = sorted((r for r in s["repos"] if r["docs"]), key=lambda r: -r["docs"])
    out += ["## Repos", "", "| Repo | Docs | Open | In flight | Done | Stale | Checkboxes | Last update |",
            "|---|---:|---:|---:|---:|---:|---:|---|"]
    for r in rows[:40]:
        ds = by_repo[r["path"]]
        c = collections.Counter(d["bucket"] for d in ds)
        out.append(f"| `{r['path']}` | {len(ds)} | {c['open']} | {c['in_flight']} | {c['done']} | "
                   f"{sum(1 for d in ds if 'stale' in d['flags'])} | "
                   f"{sum(d['tasks_open_count'] for d in ds if d['task_folder'])} | "
                   f"{max(d['updated'] for d in ds)} |")
    if len(rows) > 40:
        out.append(f"| …{len(rows) - 40} more | | | | | | | |")
    out.append("")

    flight = sorted((d for d in docs if d["bucket"] == "in_flight"), key=lambda d: d["updated"], reverse=True)
    d30 = (today - dt.timedelta(days=30)).isoformat()
    if s.get("window_days"):
        out += momentum(s, by_repo, d30)
    out += options(s, docs, d30)
    out += [f"## In flight ({len(flight)})", ""]
    out += [f"- {d['updated']} · `{d['repo']}` {d['folder']} · {link(d)} ({cell(d['status'])})" for d in flight[:30]]
    if len(flight) > 30:
        out.append(f"- …and {len(flight) - 30} more")
    out.append("")

    issues = sorted((d for d in docs if d["folder"] == "issues" and d["bucket"] in ("open", "in_flight")),
                    key=lambda d: d["updated"], reverse=True)
    out += [f"## Open issues ({len(issues)})", ""]
    out += [f"- {d['updated']} · `{d['repo']}` · {link(d)} ({cell(d['status'])})" for d in issues[:20]]
    if len(issues) > 20:
        out.append(f"- …and {len(issues) - 20} more")
    out.append("")

    handoffs = {}
    for d in docs:
        if d["folder"] == "handoffs" and (d["repo"] not in handoffs or d["updated"] > handoffs[d["repo"]]["updated"]):
            handoffs[d["repo"]] = d
    if handoffs:
        out += ["## Latest handoff per repo", ""]
        for d in sorted(handoffs.values(), key=lambda d: d["updated"], reverse=True)[:20]:
            out.append(f"- {d['updated']} · `{d['repo']}` · {link(d)}")
        out.append("")

    # In-flight docs first, newest first within each group (two stable sorts).
    with_tasks = sorted((d for d in docs if d["task_folder"] and d["tasks_open"] and d["bucket"] in ("open", "in_flight")),
                        key=lambda d: d["updated"], reverse=True)
    with_tasks.sort(key=lambda d: d["bucket"] != "in_flight")
    out += [f"## Open checkboxes in live docs ({sum(d['tasks_open_count'] for d in with_tasks)} in {len(with_tasks)} docs)", ""]
    for d in with_tasks[:15]:
        out.append(f"- {link(d)} · `{d['repo']}` · {d['tasks_open_count']} open, {d['tasks_done']} done")
        for t in d["tasks_open"][:3]:
            out.append(f"  - L{t['line']}: {cell(t['text'])[:140]}")
    if len(with_tasks) > 15:
        out.append(f"- …and {len(with_tasks) - 15} more docs")
    out.append("")

    out += cleanup(docs)
    out += [f"## Stale ({len(stale)})", ""]
    per_repo = collections.Counter(d["repo"] for d in stale)
    out.append("By repo: " + ", ".join(f"`{r}` {n}" for r, n in per_repo.most_common(12)) + ".")
    out.append("")
    out.append("Oldest:")
    for d in sorted(stale, key=lambda d: d["updated"])[:10]:
        out.append(f"- {d['updated']} ({days_ago(d['updated'], today)}d) · `{d['repo']}` · {link(d)} ({cell(d['status'])})")
    out.append("")

    flags = collections.Counter(f for d in docs for f in d["flags"] if f != "stale")
    unmapped = collections.Counter(d["status"] for d in docs if d["bucket"] == "unmapped")
    out += ["## Drift (surfaced, never auto-fixed)", ""]
    out += [f"- `{f}`: {n}" for f, n in flags.most_common()]
    if unmapped:
        out += ["", "Statuses that don't map to a lifecycle bucket:", ""]
        out += [f"- `{cell(st)[:120]}` ×{n}" for st, n in unmapped.most_common(20)]
    out.append("")
    return "\n".join(out)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("survey")
    ap.add_argument("--out")
    args = ap.parse_args(argv)
    with open(args.survey, encoding="utf-8") as f:
        s = json.load(f)
    text = render(s)
    target = args.out or os.path.join(os.path.dirname(os.path.abspath(args.survey)), "SURVEY.md")
    with open(target, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"report: {text.count(chr(10)) + 1} lines -> {target}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
