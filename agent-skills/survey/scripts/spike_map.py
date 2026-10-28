#!/usr/bin/env python3
"""Spike C, Map: render survey.json as a tree-first page of where the thinking lives.

  python3 spike_map.py path/to/survey.json [--out file.html]

First screen answers "where is the thinking dense, thin, or stale across the tree?":
repos nested as they sit on disk, each with a status-mix bar, a freshness strip, and
its open-checkbox count; folders and docs one click down; a repo x folder heat grid below.
Standard library only. One self-contained HTML file, three modes (light/dark/vibrant).
Spec: context-v/specs/Survey-a-Scoped-Dashboard-of-Context-V.md
"""
import argparse

import copy_path
import datetime as dt
import html
import json
import math
import os
import sys
import urllib.parse

BUCKETS = [
    ("in_flight", "In flight"), ("open", "Open"), ("done", "Done"), ("reference", "Reference"),
    ("parked", "Parked"), ("closed", "Closed"), ("unmapped", "Unmapped"), ("none", "No status"),
]
FOLDER_ORDER = ["specs", "plans", "prompts", "blueprints", "reminders", "agent-skills",
                "explorations", "issues", "handoffs", "decisions", "loops", "habits",
                "contracts", "sitemap"]
GRID_COLUMNS = ["specs", "plans", "prompts", "blueprints", "reminders", "explorations",
                "issues", "handoffs", "decisions"]
FRESH = [(7, "week"), (30, "month"), (90, "quarter"), (None, "older")]

esc = html.escape


def age_band(updated, today):
    try:
        days = (today - dt.date.fromisoformat(updated)).days
    except (TypeError, ValueError):
        return "older"
    for limit, name in FRESH:
        if limit is not None and days <= limit:
            return name
    return "older"


def tally(docs, today):
    buckets = {b: 0 for b, _ in BUCKETS}
    fresh = {name: 0 for _, name in FRESH}
    tasks = stale = 0
    for d in docs:
        buckets[d["bucket"]] = buckets.get(d["bucket"], 0) + 1
        fresh[age_band(d["updated"], today)] += 1
        tasks += d.get("tasks_open_count", 0)
        stale += "stale" in d["flags"]
    return {"n": len(docs), "buckets": buckets, "fresh": fresh, "tasks": tasks, "stale": stale}


def status_bar(t, cls="bar"):
    if not t["n"]:
        return f'<span class="{cls} {cls}--empty" aria-hidden="true"></span>'
    segs = "".join(
        f'<i class="b-{b}" style="flex-grow:{t["buckets"][b]}" title="{label}: {t["buckets"][b]}"></i>'
        for b, label in BUCKETS if t["buckets"][b])
    alt = ", ".join(f'{t["buckets"][b]} {label.lower()}' for b, label in BUCKETS if t["buckets"][b])
    return f'<span class="{cls}" role="img" aria-label="{esc(alt)}">{segs}</span>'


def fresh_strip(t):
    if not t["n"]:
        return '<span class="fresh fresh--empty" aria-hidden="true"></span>'
    segs = "".join(
        f'<i class="f-{name}" style="flex-grow:{t["fresh"][name]}" title="updated this {name}: {t["fresh"][name]}"></i>'
        if name != "older" else
        f'<i class="f-older" style="flex-grow:{t["fresh"][name]}" title="older than 90 days: {t["fresh"][name]}"></i>'
        for _, name in FRESH if t["fresh"][name])
    recent = t["fresh"]["week"] + t["fresh"]["month"]
    return (f'<span class="fresh" role="img" aria-label="{recent} of {t["n"]} updated in the last 30 days">'
            f'{segs}</span>')


def folder_key(name):
    return (FOLDER_ORDER.index(name) if name in FOLDER_ORDER else len(FOLDER_ORDER),
            name == "(root)", name)


def render(survey):
    gen = survey.get("generated_at", "")
    try:
        today = dt.date.fromisoformat(gen[:10])
    except ValueError:
        today = dt.date.today()
    docs = survey["docs"]
    repos = {r["path"]: r for r in survey["repos"]}
    by_repo = {}
    for d in docs:
        by_repo.setdefault(d["repo"], []).append(d)

    children = {}
    tops = []
    for path, r in repos.items():
        parent = r.get("parent")
        if parent and parent in repos and parent != path:
            children.setdefault(parent, []).append(path)
        else:
            tops.append(path)

    subtotal = {}

    def subtree(path):
        if path not in subtotal:
            subtotal[path] = len(by_repo.get(path, [])) + sum(subtree(c) for c in children.get(path, []))
        return subtotal[path]

    for p in repos:
        subtree(p)

    def order(paths):
        return sorted(paths, key=lambda p: (-subtotal[p], repos[p]["name"].lower()))

    def repo_html(path, depth):
        r = repos[path]
        own = by_repo.get(path, [])
        t = tally(own, today)
        kids = order(children.get(path, []))
        below = subtotal[path] - t["n"]
        empty = not r["context_v"]
        folders = {}
        for d in own:
            folders.setdefault(d["folder"], []).append(d)
        label = r["name"] if path != "." else f'{r["name"]} (scope root)'
        cls = "repo" + (" empty" if empty else "") + (" leaf" if not kids and not folders else "")
        open_attr = " open" if depth == 0 else ""
        out = [f'<details class="{cls}" data-path="{esc(path)}"{open_attr}>',
               '<summary class="row">',
               f'<span class="name" title="{esc(path)}">{esc(label)}</span>',
               f'<span class="count">{t["n"] or "–"}'
               + (f'<small title="docs in child repos">+{below}</small>' if below else "") + '</span>',
               status_bar(t), fresh_strip(t),
               f'<span class="tasks" title="open checkboxes">{t["tasks"] or ""}</span>',
               '</summary><div class="kids">']
        # A repo with child repos tucks its own folders into one collapsed context-v/ row,
        # so the first screen of a tree reads as repos, not the root's folders.
        grouped = bool(kids and folders)
        if grouped:
            out.append(
                f'<details class="cvgroup"><summary class="row row--folder row--group">'
                f'<span class="name">context-v/ · {len(folders)} folders</span><span class="count">{t["n"]}</span>'
                f'{status_bar(t)}{fresh_strip(t)}<span class="tasks">{t["tasks"] or ""}</span></summary>'
                '<div class="kids">')
        for name in sorted(folders, key=folder_key):
            ft = tally(folders[name], today)
            key = f"{path}|{name}"
            out.append(
                f'<details class="folder" data-key="{esc(key)}"><summary class="row row--folder">'
                f'<span class="name">{esc(name)}</span><span class="count">{ft["n"]}</span>'
                f'{status_bar(ft)}{fresh_strip(ft)}'
                f'<span class="tasks">{ft["tasks"] or ""}</span></summary>'
                f'<ol class="docs" data-key="{esc(key)}"></ol></details>')
        if grouped:
            out.append("</div></details>")
        for k in kids:
            out.append(repo_html(k, depth + 1))
        out.append("</div></details>")
        return "".join(out)

    tree = "".join(repo_html(p, 0) for p in order(tops))

    # Heat grid: repos with docs x canonical folders.
    grid_rows = []
    max_cell = 1
    cells = {}
    for path in repos:
        for d in by_repo.get(path, []):
            col = d["folder"] if d["folder"] in GRID_COLUMNS else "other"
            c = cells.setdefault((path, col), [0, 0])
            c[0] += 1
            c[1] += "stale" in d["flags"]
            max_cell = max(max_cell, c[0])
    for path in sorted((p for p in repos if by_repo.get(p)), key=lambda p: -len(by_repo[p])):
        tds = []
        for col in GRID_COLUMNS + ["other"]:
            n, stale = cells.get((path, col), [0, 0])
            if not n:
                tds.append('<td class="z"></td>')
                continue
            pct = round(12 + 78 * math.log1p(n) / math.log1p(max_cell))
            stale_cls = " stale" if stale * 2 > n else ""
            tds.append(f'<td class="h{stale_cls}" style="--pct:{pct}%" '
                       f'title="{esc(path)} / {col}: {n} docs, {stale} stale">{n}</td>')
        grid_rows.append(f'<tr><th scope="row" title="{esc(path)}">{esc(repos[path]["name"])}</th>{"".join(tds)}</tr>')
    grid_head = "".join(f"<th scope=\"col\"><span>{c}</span></th>" for c in GRID_COLUMNS + ["other"])

    total = tally(docs, today)
    n_cv = sum(len(r["context_v"]) for r in repos.values())
    n_empty = sum(1 for r in repos.values() if not r["context_v"])
    legend = "".join(f'<li><i class="sw b-{b}"></i>{label} <b>{total["buckets"][b]}</b></li>'
                     for b, label in BUCKETS if total["buckets"][b])
    fresh_legend = "".join(
        f'<li><i class="sw f-{name}"></i>{"≤ " + str(lim) + "d" if lim else "> 90d"} <b>{total["fresh"][name]}</b></li>'
        for lim, name in FRESH)

    slim = {}
    for d in docs:
        slim.setdefault(f'{d["repo"]}|{d["folder"]}', []).append([
            d["title"], "file://" + urllib.parse.quote(d.get("abs_path") or d["path"]),
            d["path"], d.get("status") or "", d["bucket"], d["updated"],
            d.get("tasks_open_count", 0), int("stale" in d["flags"]), d.get("abs_path") or d["path"]])
    data = {"parents": {p: r.get("parent") for p, r in repos.items()}, "docs": slim}
    data_json = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")

    stats = [("repos", len(repos)), ("context-v", n_cv), ("docs", total["n"]),
             ("in flight", total["buckets"]["in_flight"]), ("open tasks", total["tasks"]),
             ("stale", total["stale"])]
    stats_html = "".join(f'<div><dt>{k}</dt><dd>{v:,}</dd></div>' for k, v in stats)

    return TEMPLATE.format(
        title=esc(f'Survey map · {survey.get("root_name", "")}'),
        css=CSS, prepaint=PREPAINT, js=JS,
        root_name=esc(survey.get("root_name", "")), root=esc(survey.get("root", "")),
        scope=esc(survey.get("scope", "")), generated=esc(gen.replace("T", " ")),
        stale_days=survey.get("stale_days", 90), stats=stats_html,
        legend=legend, fresh_legend=fresh_legend, tree=tree, n_empty=n_empty,
        grid_head=grid_head, grid_rows="".join(grid_rows), data=data_json)


PREPAINT = """(function(){var m;try{m=localStorage.getItem('cv-survey-mode')}catch(e){}
var h=/mode=(light|dark|vibrant)/.exec(location.hash);if(h)m=h[1];
if(!/^(light|dark|vibrant)$/.test(m||''))m='dark';document.documentElement.setAttribute('data-mode',m)})();"""

CSS = """
:root{
--color__amber:#fbbf24;--color__amber-deep:#b45309;--color__amber-soft:#fde68a;
--color__sodium:#f97316;--color__sodium-deep:#9a3412;--color__sodium-soft:#fed7aa;
--color__lime:#a3e635;--color__lime-deep:#4d7c0f;--color__lime-soft:#d9f99d;
--color__neon-amber:#ffd60a;--color__neon-sodium:#ff7a1a;--color__iris:#818cf8;
--color__paper:#f7f6f1;--color__paper-soft:#efece2;--color__paper-deep:#e2dfd1;
--color__ink:#0a0c10;--color__ink-soft:#11141b;--color__ink-deep:#060709;--color__charcoal:#161a23;
--color__slate-700:#2a2f3a;--color__slate-600:#3b414f;--color__slate-500:#5b6273;--color__slate-400:#8b91a3;
--color__slate-300:#b4b9c7;--color__slate-200:#d4d8e0;--color__slate-100:#e8eaef;
--font__display:'JetBrains Mono',ui-monospace,SFMono-Regular,Menlo,monospace;
--font__sans:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;
--font__mono:'JetBrains Mono',ui-monospace,SFMono-Regular,Menlo,monospace;
--radius-sm:2px;--radius-md:3px;--radius-lg:6px;--grid-pitch:28px;
}
:root,:root[data-mode='dark']{
--color-bg:var(--color__ink);--color-bg-soft:var(--color__ink-soft);--color-bg-elevated:var(--color__charcoal);
--color-bg-card:rgba(22,26,35,.78);
--color-text:#e8eaef;--color-text-soft:var(--color__slate-200);--color-text-dim:var(--color__slate-400);
--color-text-dimmer:var(--color__slate-500);--color-text-faint:var(--color__slate-600);
--color-accent:var(--color__amber);--color-accent-soft:var(--color__amber-soft);
--color-accent-warm:var(--color__sodium);--color-accent-hot:var(--color__sodium-deep);
--color-thread:var(--color__lime);--color-thread-soft:var(--color__lime-soft);
--color-border:rgba(232,234,239,.08);--color-border-strong:rgba(232,234,239,.18);
--color-border-accent:rgba(251,191,36,.45);--color-grid-dot:rgba(232,234,239,.06);
--bucket-in_flight:var(--color__sodium);--bucket-open:var(--color__amber);--bucket-done:var(--color__lime);
--bucket-reference:var(--color__iris);--bucket-parked:var(--color__slate-400);--bucket-closed:var(--color__slate-600);
--bucket-unmapped:#f472b6;--bucket-none:var(--color__slate-700);
--fresh-week:var(--color__lime);--fresh-month:color-mix(in oklab,var(--color__lime) 55%,var(--color__slate-600));
--fresh-quarter:var(--color__slate-600);--fresh-older:var(--color__slate-700);
--heat:var(--color__amber);--track:rgba(232,234,239,.05);
color-scheme:dark;
}
:root[data-mode='light']{
--color-bg:var(--color__paper);--color-bg-soft:var(--color__paper-soft);--color-bg-elevated:#fffefa;
--color-bg-card:rgba(255,254,250,.9);
--color-text:var(--color__ink);--color-text-soft:var(--color__slate-700);--color-text-dim:var(--color__slate-500);
--color-text-dimmer:#6b7280;--color-text-faint:var(--color__slate-400);
--color-accent:var(--color__amber-deep);--color-accent-soft:var(--color__amber);
--color-accent-warm:var(--color__sodium-deep);--color-accent-hot:var(--color__sodium);
--color-thread:var(--color__lime-deep);--color-thread-soft:var(--color__lime);
--color-border:rgba(10,12,16,.10);--color-border-strong:rgba(10,12,16,.22);
--color-border-accent:rgba(180,83,9,.45);--color-grid-dot:rgba(10,12,16,.06);
--bucket-in_flight:var(--color__sodium);--bucket-open:#e0a100;--bucket-done:var(--color__lime-deep);
--bucket-reference:#5b63d3;--bucket-parked:var(--color__slate-400);--bucket-closed:var(--color__slate-600);
--bucket-unmapped:#db2777;--bucket-none:var(--color__slate-200);
--fresh-week:var(--color__lime-deep);--fresh-month:color-mix(in oklab,var(--color__lime-deep) 50%,var(--color__slate-300));
--fresh-quarter:var(--color__slate-300);--fresh-older:var(--color__slate-200);
--heat:var(--color__amber-deep);--track:rgba(10,12,16,.05);
color-scheme:light;
}
:root[data-mode='vibrant']{
--color-bg:var(--color__ink-deep);--color-bg-soft:#0a0a14;--color-bg-elevated:#14122a;
--color-bg-card:rgba(20,18,42,.74);
--color-text:#fff8e8;--color-text-soft:#f0e0b8;--color-text-dim:#c8b890;--color-text-dimmer:#807058;--color-text-faint:#4a4030;
--color-accent:var(--color__neon-amber);--color-accent-soft:#ffe55a;
--color-accent-warm:var(--color__neon-sodium);--color-accent-hot:var(--color__iris);
--color-thread:var(--color__lime);--color-thread-soft:#c8ff5a;
--color-border:rgba(255,214,10,.16);--color-border-strong:rgba(255,214,10,.36);
--color-border-accent:rgba(255,122,26,.6);--color-grid-dot:rgba(255,214,10,.10);
--bucket-in_flight:var(--color__neon-sodium);--bucket-open:var(--color__neon-amber);--bucket-done:#c8ff5a;
--bucket-reference:var(--color__iris);--bucket-parked:#807058;--bucket-closed:#4a4030;
--bucket-unmapped:#ff4fd8;--bucket-none:#2a2440;
--fresh-week:#c8ff5a;--fresh-month:color-mix(in oklab,#c8ff5a 50%,#4a4030);
--fresh-quarter:#4a4030;--fresh-older:#2a2440;
--heat:var(--color__neon-sodium);--track:rgba(255,214,10,.06);
color-scheme:dark;
}
*,*::before,*::after{box-sizing:border-box}*{margin:0;padding:0}
html{background:var(--color-bg)}
body{min-height:100vh;background:var(--color-bg);color:var(--color-text);font:15px/1.55 var(--font__sans);
-webkit-font-smoothing:antialiased;overflow-x:hidden;
background-image:radial-gradient(var(--color-grid-dot) 1px,transparent 1px);background-size:var(--grid-pitch) var(--grid-pitch)}
a{color:inherit}
.wrap{max-width:1180px;margin:0 auto;padding:28px 16px 80px}
header.top{display:flex;flex-wrap:wrap;gap:16px 24px;align-items:flex-start;justify-content:space-between;margin-bottom:20px}
h1{font:500 clamp(20px,3vw,28px)/1.2 var(--font__display);letter-spacing:-.02em}
h1 em{font-style:normal;color:var(--color-accent)}
h2{font:500 15px/1.3 var(--font__display);letter-spacing:.02em;text-transform:uppercase;color:var(--color-text-dim);margin:36px 0 12px}
.sub{font:12px/1.5 var(--font__mono);color:var(--color-text-dim);margin-top:6px;word-break:break-all}
.modes{display:inline-flex;border:1px solid var(--color-border-strong);border-radius:var(--radius-lg);padding:3px;gap:2px;background:var(--color-bg-card)}
.modes button{font:12px var(--font__mono);background:none;border:0;color:var(--color-text-dim);padding:5px 10px;border-radius:var(--radius-md);cursor:pointer}
.modes button[aria-checked='true']{background:var(--color-accent);color:var(--color-bg)}
dl.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:1px;background:var(--color-border);
border:1px solid var(--color-border);border-radius:var(--radius-lg);overflow:hidden;margin-bottom:18px}
dl.stats div{background:var(--color-bg-card);padding:12px 14px}
dt{font:11px var(--font__mono);text-transform:uppercase;letter-spacing:.06em;color:var(--color-text-dim)}
dd{font:500 22px/1.2 var(--font__display);color:var(--color-text)}
.controls{display:flex;flex-wrap:wrap;gap:10px 18px;align-items:center;margin:14px 0}
.controls input[type=search]{flex:1 1 260px;min-width:0;font:14px var(--font__mono);padding:8px 12px;border-radius:var(--radius-lg);
border:1px solid var(--color-border-strong);background:var(--color-bg-elevated);color:var(--color-text)}
.controls input[type=search]:focus{outline:2px solid var(--color-border-accent);outline-offset:1px}
.controls label{font:12px var(--font__mono);color:var(--color-text-dim);display:flex;gap:6px;align-items:center;cursor:pointer}
.legend{display:flex;flex-wrap:wrap;gap:6px 16px;list-style:none;font:12px var(--font__mono);color:var(--color-text-dim)}
.legend b{color:var(--color-text);font-weight:500}
.sw{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:6px;vertical-align:-1px}
.legends{display:grid;gap:8px;padding:12px 14px;border:1px solid var(--color-border);border-radius:var(--radius-lg);background:var(--color-bg-card)}
.legends .k{font:11px var(--font__mono);text-transform:uppercase;letter-spacing:.06em;color:var(--color-text-faint);margin-right:8px}
.b-in_flight{background:var(--bucket-in_flight)}.b-open{background:var(--bucket-open)}.b-done{background:var(--bucket-done)}
.b-reference{background:var(--bucket-reference)}.b-parked{background:var(--bucket-parked)}.b-closed{background:var(--bucket-closed)}
.b-unmapped{background:var(--bucket-unmapped)}.b-none{background:var(--bucket-none)}
.f-week{background:var(--fresh-week)}.f-month{background:var(--fresh-month)}.f-quarter{background:var(--fresh-quarter)}.f-older{background:var(--fresh-older)}
.colhead,.row{display:grid;grid-template-columns:minmax(0,1fr) 64px minmax(80px,220px) minmax(50px,90px) 44px;gap:12px;align-items:center}
.colhead{font:11px var(--font__mono);text-transform:uppercase;letter-spacing:.06em;color:var(--color-text-faint);padding:0 10px 6px 30px}
.colhead span:nth-child(n+2){text-align:right}.colhead span:nth-child(3),.colhead span:nth-child(4){text-align:left}
.tree{border:1px solid var(--color-border);border-radius:var(--radius-lg);background:var(--color-bg-card);padding:6px}
details>summary{list-style:none;cursor:pointer}details>summary::-webkit-details-marker{display:none}
.row{padding:6px 10px;border-radius:var(--radius-md);position:relative}
.row:hover{background:var(--color-border)}
.row .name{font:500 14px var(--font__display);overflow:hidden;text-overflow:ellipsis;white-space:nowrap;padding-left:20px;position:relative}
.row .name::before{content:'▸';position:absolute;left:2px;color:var(--color-text-faint);transition:transform .14s}
details[open]>.row .name::before{transform:rotate(90deg)}
.repo.leaf>.row .name::before{content:'·'}
.count{font:13px var(--font__mono);text-align:right;color:var(--color-text-soft)}
.count small{display:block;font-size:10px;color:var(--color-text-faint)}
.tasks{font:12px var(--font__mono);text-align:right;color:var(--color-accent-warm)}
.bar,.fresh{display:flex;height:10px;border-radius:2px;overflow:hidden;background:var(--track);gap:1px}
.fresh{height:6px}
.bar i,.fresh i{display:block;min-width:2px}
.kids{margin-left:18px;border-left:1px dashed var(--color-border-strong);padding-left:4px}
.repo.empty>.row{opacity:.42}
body:has(#hide-empty:checked) .repo.empty:not(:has(.repo:not(.empty))){display:none}
.row--folder .name{font:13px var(--font__mono);color:var(--color-text-soft)}
.row--folder .bar{height:7px}
.row--group .name{color:var(--color-accent)}
ol.docs{list-style:none;margin:2px 0 8px 30px;border-left:1px solid var(--color-border);padding-left:10px}
ol.docs li{display:grid;grid-template-columns:minmax(0,1fr) auto auto;gap:10px;align-items:baseline;padding:3px 4px;font-size:13px}
ol.docs li a{text-decoration:none;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
ol.docs li a:hover{color:var(--color-accent);text-decoration:underline}
.chip{font:11px var(--font__mono);padding:1px 7px;border-radius:999px;border:1px solid currentColor;white-space:nowrap;max-width:16ch;overflow:hidden;text-overflow:ellipsis}
.chip.c-in_flight{color:var(--bucket-in_flight)}.chip.c-open{color:var(--bucket-open)}.chip.c-done{color:var(--bucket-done)}
.chip.c-reference{color:var(--bucket-reference)}.chip.c-parked,.chip.c-closed,.chip.c-none{color:var(--color-text-dim)}.chip.c-unmapped{color:var(--bucket-unmapped)}
.date{font:11px var(--font__mono);color:var(--color-text-dim)}.date.stale{color:var(--color-accent-warm)}
.hidden{display:none!important}
mark{background:color-mix(in oklab,var(--color-accent) 35%,transparent);color:inherit;border-radius:2px}
.gridwrap{overflow-x:auto;border:1px solid var(--color-border);border-radius:var(--radius-lg);background:var(--color-bg-card)}
table.heat{border-collapse:separate;border-spacing:2px;font:12px var(--font__mono);width:100%;min-width:640px}
table.heat th{font-weight:400;color:var(--color-text-dim);padding:4px 6px}
table.heat thead th{text-align:center;font-size:11px;text-transform:uppercase;letter-spacing:.04em}
table.heat tbody th{text-align:left;white-space:nowrap;max-width:200px;overflow:hidden;text-overflow:ellipsis;color:var(--color-text-soft)}
table.heat td{text-align:center;padding:5px 0;border-radius:var(--radius-sm);min-width:44px}
td.z{background:var(--track)}
td.h{background:color-mix(in oklab,var(--heat) var(--pct),transparent);color:var(--color-text)}
td.h.stale{box-shadow:inset 0 0 0 2px var(--bucket-unmapped)}
.note{font:12px var(--font__mono);color:var(--color-text-dim);margin-top:8px}
@media (max-width:640px){
.row,.colhead{grid-template-columns:minmax(0,1fr) 56px 36px}
.row .bar,.row .fresh{grid-column:1 / -1}
.row .bar{order:4}.row .fresh{order:5}
.colhead span:nth-child(3),.colhead span:nth-child(4){display:none}
.kids{margin-left:8px}
}
"""

JS = r"""
(function(){
var root=document.documentElement,KEY='cv-survey-mode';
var btns=document.querySelectorAll('.modes button');
function set(m){root.setAttribute('data-mode',m);try{localStorage.setItem(KEY,m)}catch(e){}
  btns.forEach(function(b){b.setAttribute('aria-checked',String(b.dataset.mode===m))})}
btns.forEach(function(b){b.addEventListener('click',function(){set(b.dataset.mode)})});
set(root.getAttribute('data-mode')||'dark');

var DATA=JSON.parse(document.getElementById('survey-data').textContent);
function esc(s){return String(s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function hi(s,q){var t=esc(s);if(!q)return t;var i=t.toLowerCase().indexOf(esc(q).toLowerCase());
  return i<0?t:t.slice(0,i)+'<mark>'+t.slice(i,i+esc(q).length)+'</mark>'+t.slice(i+esc(q).length)}
function match(d,q){return !q||(d[0]+' '+d[2]+' '+d[3]).toLowerCase().indexOf(q)>=0}
function fill(ol,q){
  var rows=(DATA.docs[ol.dataset.key]||[]).filter(function(d){return match(d,q)});
  rows.sort(function(a,b){return a[5]<b[5]?1:-1});
  ol.innerHTML=rows.map(function(d){
    return '<li><a href="'+esc(d[1])+'" title="'+esc(d[2])+'">'+hi(d[0],q)+'</a>'+cpBtn(d[8])+
      '<span class="chip c-'+d[4]+'" title="'+esc(d[3])+'">'+esc(d[3]||'no status')+'</span>'+
      '<span class="date'+(d[7]?' stale':'')+'">'+esc(d[5])+(d[6]?' · ☐'+d[6]:'')+'</span></li>'}).join('');
  ol.dataset.filled=q||'*';
}
document.querySelectorAll('details.folder').forEach(function(f){
  f.addEventListener('toggle',function(){var ol=f.querySelector('ol.docs');
    if(f.open&&ol.dataset.filled!==(cur||'*'))fill(ol,cur)})});

var cur='',input=document.getElementById('q'),status=document.getElementById('q-status'),t;
var repos=document.querySelectorAll('details.repo'),folders=document.querySelectorAll('details.folder'),groups=document.querySelectorAll('details.cvgroup');
function apply(){
  cur=input.value.trim().toLowerCase();
  if(!cur){repos.forEach(function(r){r.classList.remove('hidden')});groups.forEach(function(g){g.classList.remove('hidden')});
    folders.forEach(function(f){f.classList.remove('hidden');var ol=f.querySelector('ol.docs');if(f.open)fill(ol,'');else ol.dataset.filled=''});
    status.textContent='';return}
  var hitRepos={},hitFolders={},n=0;
  Object.keys(DATA.docs).forEach(function(k){var c=DATA.docs[k].filter(function(d){return match(d,cur)}).length;
    if(c){n+=c;hitFolders[k]=1;var p=k.split('|')[0];while(p!=null&&!hitRepos[p]){hitRepos[p]=1;p=DATA.parents[p]}}});
  repos.forEach(function(r){var on=!!hitRepos[r.dataset.path];r.classList.toggle('hidden',!on);if(on)r.open=true});
  folders.forEach(function(f){var on=!!hitFolders[f.dataset.key];f.classList.toggle('hidden',!on);
    if(on){f.open=true;var g=f.closest('details.cvgroup');if(g)g.open=true;fill(f.querySelector('ol.docs'),cur)}});
  groups.forEach(function(g){g.classList.toggle('hidden',!g.querySelector('details.folder:not(.hidden)'))});
  status.textContent=n+' docs match';
}
input.addEventListener('input',function(){clearTimeout(t);t=setTimeout(apply,140)});
var hq=/[#&]q=([^&]*)/.exec(location.hash);if(hq){input.value=decodeURIComponent(hq[1]);apply()}
document.getElementById('expand').addEventListener('click',function(){
  var open=this.dataset.state!=='open';this.dataset.state=open?'open':'';this.textContent=open?'collapse all':'expand all';
  repos.forEach(function(r){r.open=open})});
})();
"""

TEMPLATE = """<!doctype html>
<html lang="en" data-mode="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<script>{prepaint}</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap">
<style>{css}</style>
</head>
<body>
<div class="wrap">
<header class="top">
  <div>
    <h1>Survey map · <em>{root_name}</em></h1>
    <p class="sub">{scope} scope · {root} · generated {generated}</p>
  </div>
  <div class="modes" role="radiogroup" aria-label="Color mode">
    <button type="button" role="radio" data-mode="light" aria-checked="false">light</button>
    <button type="button" role="radio" data-mode="dark" aria-checked="true">dark</button>
    <button type="button" role="radio" data-mode="vibrant" aria-checked="false">vibrant</button>
  </div>
</header>

<dl class="stats">{stats}</dl>

<div class="legends">
  <ul class="legend"><li class="k">status</li>{legend}</ul>
  <ul class="legend"><li class="k">updated</li>{fresh_legend}<li class="k">stale = open or in flight, untouched {stale_days}d+</li></ul>
</div>

<h2>Where the thinking lives</h2>
<div class="controls">
  <input id="q" type="search" placeholder="filter docs by title, path, or status…" aria-label="Filter docs">
  <span id="q-status" class="sub" aria-live="polite"></span>
  <label><input type="checkbox" id="hide-empty"> hide {n_empty} repos without context-v</label>
  <button id="expand" type="button" class="modes" style="padding:5px 10px;font:12px var(--font__mono);color:var(--color-text-dim);cursor:pointer">expand all</button>
</div>
<div class="colhead" aria-hidden="true"><span>repo / folder</span><span>docs</span><span>status mix</span><span>freshness</span><span>☐</span></div>
<nav class="tree" aria-label="Repos and their context-v folders">{tree}</nav>

<h2>Heat grid · repo × folder</h2>
<div class="gridwrap"><table class="heat">
<thead><tr><th></th>{grid_head}</tr></thead>
<tbody>{grid_rows}</tbody>
</table></div>
<p class="note">Shade = doc count (log scale). Outlined cells: more than half the docs are stale.</p>
</div>
<script type="application/json" id="survey-data">{data}</script>
<script>{js}</script>
</body>
</html>
"""


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("survey")
    ap.add_argument("--out")
    args = ap.parse_args(argv)
    with open(args.survey, encoding="utf-8") as f:
        survey = json.load(f)
    out = args.out or os.path.join(os.path.dirname(os.path.abspath(args.survey)), "survey-map.html")
    page = render(survey)
    with open(out, "w", encoding="utf-8") as f:
        f.write(copy_path.inject(page))
    print(f"spike_map: {len(survey['docs'])} docs, {len(page) // 1024} KB -> {out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
