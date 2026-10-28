#!/usr/bin/env python3
"""Spike B, Board: render survey.json as a task-first kanban page.

  python3 spike_board.py path/to/survey.json [--out file.html]

First screen answers "what should I work on?": a stat strip, columns by lifecycle
bucket (Open, In flight, Done in the last 30 days, Parked) with a collapsed rail for
Closed / Reference / None, and the open checkboxes from task-bearing docs.
One self-contained file, three modes (light / dark / vibrant). Standard library only.
"""
import argparse

import copy_path
import datetime as dt
import html
import json
import os
import sys

COLUMNS = [("open", "Open"), ("in_flight", "In flight"), ("done", "Done · 30d"), ("parked", "Parked")]
RAIL = [("closed", "Closed"), ("reference", "Reference"), ("none", "No status"), ("unmapped", "Unmapped")]
SSR_CARDS = 10
DONE_DAYS = 30


def esc(s):
    return html.escape(str(s if s is not None else ""), quote=True)


def days_ago(date_str, today):
    try:
        return (today - dt.date.fromisoformat(date_str)).days
    except (TypeError, ValueError):
        return None


def rel(n):
    if n is None:
        return "?"
    if n <= 0:
        return "today"
    if n < 60:
        return f"{n}d ago"
    if n < 730:
        return f"{n // 30}mo ago"
    return f"{n // 365}y ago"


def slim(doc):
    out = {k: doc.get(k) for k in ("path", "abs_path", "repo", "folder", "title", "status",
                                   "bucket", "updated", "tasks_open_count", "task_folder")}
    out["stale"] = "stale" in doc.get("flags", [])
    out["tasks"] = doc.get("tasks_open", []) if doc.get("task_folder") else []
    return out


def sort_column(docs, bucket):
    """Newest first; in Open, stale docs sink below live ones (stable sort keeps newest-first)."""
    docs = sorted(docs, key=lambda d: d["updated"] or "", reverse=True)
    if bucket == "open":
        docs = sorted(docs, key=lambda d: d["stale"])
    return docs


def column_docs(docs, bucket, today):
    col = [d for d in docs if d["bucket"] == bucket]
    if bucket == "done":
        col = [d for d in col if (days_ago(d["updated"], today) or 9999) <= DONE_DAYS]
    return sort_column(col, bucket)


def card_html(d, today):
    crumb = d["folder"] if d["repo"] == "." else f'{d["repo"]} / {d["folder"]}'
    badges = []
    if d["stale"]:
        badges.append('<span class="badge badge--stale">stale</span>')
    if d["tasks_open_count"]:
        badges.append(f'<span class="badge badge--tasks">☐ {d["tasks_open_count"]}</span>')
    return (
        f'<article class="card{" card--stale" if d["stale"] else ""}">'
        f'<a class="card__title" href="file://{esc(d["abs_path"])}">{esc(d["title"])}</a>{copy_path.button(d["abs_path"])}'
        f'<div class="card__crumb">{esc(crumb)}</div>'
        f'<div class="card__meta"><span class="card__status">{esc(d["status"] or "—")}</span>'
        f'<span class="card__age">{rel(days_ago(d["updated"], today))}</span>{"".join(badges)}</div>'
        f'</article>'
    )


def render(survey, today):
    docs = [slim(d) for d in survey["docs"]]
    counts = {b: sum(1 for d in docs if d["bucket"] == b) for b, _ in COLUMNS + RAIL}
    stats = [
        ("In flight", counts["in_flight"], "thread"),
        ("Open", counts["open"], "accent"),
        ("Stale", sum(1 for d in docs if d["stale"]), "warm"),
        ("Open checkboxes", sum(d["tasks_open_count"] or 0 for d in docs if d["task_folder"]), "accent"),
        ("Unmapped status", counts["unmapped"], "hot"),
    ]
    stat_html = "".join(
        f'<div class="stat stat--{tone}"><b>{n:,}</b><span>{esc(label)}</span></div>'
        for label, n, tone in stats)

    cols_html = []
    for bucket, label in COLUMNS:
        col = column_docs(docs, bucket, today)
        cards = "".join(card_html(d, today) for d in col[:SSR_CARDS])
        more = f'<p class="col__more">+{len(col) - SSR_CARDS} more</p>' if len(col) > SSR_CARDS else ""
        cols_html.append(
            f'<section class="col col--{bucket}" data-bucket="{bucket}">'
            f'<header class="col__head"><h2>{esc(label)}</h2><span class="col__count">{len(col)}</span></header>'
            f'<div class="col__cards">{cards}{more}</div></section>')
    rail_html = "".join(
        f'<details class="rail__group" data-bucket="{b}"><summary>{esc(label)} '
        f'<span class="col__count">{counts[b]}</span></summary><div class="rail__cards"></div></details>'
        for b, label in RAIL)

    repo_opts = ['<option value="">All repos</option>'] + [
        f'<option value="{esc(r["path"])}">{"  " * r["depth"]}{esc(r["name"] if r["path"] != "." else survey["root_name"])}'
        f' ({r["docs"]})</option>'
        for r in sorted(survey["repos"], key=lambda r: r["path"].split(os.sep) if r["path"] != "." else [])
        if r["docs"]]
    fcount = {}
    for d in docs:
        fcount[d["folder"]] = fcount.get(d["folder"], 0) + 1
    folders = sorted(fcount, key=lambda f: -fcount[f])

    def chip(f):
        return (f'<button type="button" class="chip" data-folder="{esc(f)}" aria-pressed="false">'
                f'{esc(f)} <small>{fcount[f]}</small></button>')
    chips = "".join(chip(f) for f in folders[:10])
    if len(folders) > 10:
        chips += (f'<details class="chips__more"><summary>+{len(folders) - 10} folders</summary>'
                  f'{"".join(chip(f) for f in folders[10:])}</details>')

    payload = json.dumps({"docs": docs, "today": today.isoformat()}, ensure_ascii=False,
                         separators=(",", ":")).replace("</", "<\\/")
    title = f'Survey · {survey["root_name"]}'
    meta = (f'{esc(survey["scope"])} scope · {len(survey["repos"])} repos · {len(docs):,} docs · '
            f'generated {esc(survey["generated_at"].replace("T", " "))}')

    return (TEMPLATE
            .replace("%%TITLE%%", esc(title))
            .replace("%%ROOT%%", esc(survey["root_name"]))
            .replace("%%META%%", meta)
            .replace("%%STATS%%", stat_html)
            .replace("%%REPOS%%", "".join(repo_opts))
            .replace("%%CHIPS%%", chips)
            .replace("%%COLUMNS%%", "".join(cols_html))
            .replace("%%RAIL%%", rail_html)
            .replace("%%DATA%%", payload))


TEMPLATE = r"""<!doctype html>
<html lang="en" data-mode="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%%TITLE%%</title>
<script>
(function () {
  var modes = ['light', 'dark', 'vibrant'], mode = null;
  var m = /(?:^|[#&])mode=(light|dark|vibrant)/.exec(location.hash);
  if (m) mode = m[1];
  if (!mode) { try { mode = localStorage.getItem('cv-survey-mode'); } catch (e) {} }
  if (modes.indexOf(mode) < 0) mode = 'dark';
  document.documentElement.setAttribute('data-mode', mode);
})();
</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500;700&display=swap">
<style>
:root {
  /* Tier 1: named, mode-invariant (from splash/src/styles/theme.css) */
  --color__amber: #fbbf24; --color__amber-deep: #b45309; --color__amber-soft: #fde68a;
  --color__sodium: #f97316; --color__sodium-deep: #9a3412; --color__sodium-soft: #fed7aa;
  --color__lime: #a3e635; --color__lime-deep: #4d7c0f; --color__lime-soft: #d9f99d;
  --color__neon-amber: #ffd60a; --color__neon-sodium: #ff7a1a; --color__iris: #818cf8;
  --color__paper: #f7f6f1; --color__paper-soft: #efece2; --color__paper-deep: #e2dfd1;
  --color__ink: #0a0c10; --color__ink-soft: #11141b; --color__ink-deep: #060709; --color__charcoal: #161a23;
  --color__slate-700: #2a2f3a; --color__slate-600: #3b414f; --color__slate-500: #5b6273;
  --color__slate-400: #8b91a3; --color__slate-300: #b4b9c7; --color__slate-200: #d4d8e0; --color__slate-100: #e8eaef;
  --font__display: 'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, monospace;
  --font__sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --radius-sm: 2px; --radius-md: 3px; --radius-lg: 6px;
  --transition-fast: 140ms ease;
}
/* Tier 2: dark ("operator", default) */
:root, :root[data-mode='dark'] {
  --color-bg: var(--color__ink); --color-bg-soft: var(--color__ink-soft);
  --color-bg-elevated: var(--color__charcoal); --color-bg-card: rgba(22, 26, 35, 0.78);
  --color-text: #e8eaef; --color-text-soft: var(--color__slate-200);
  --color-text-dim: var(--color__slate-400); --color-text-dimmer: var(--color__slate-500);
  --color-accent: var(--color__amber); --color-accent-soft: var(--color__amber-soft);
  --color-accent-warm: var(--color__sodium); --color-accent-hot: var(--color__sodium-deep);
  --color-thread: var(--color__lime);
  --color-border: rgba(232, 234, 239, 0.08); --color-border-strong: rgba(232, 234, 239, 0.18);
  --color-border-accent: rgba(251, 191, 36, 0.45);
  --shadow-card: 0 18px 36px -22px rgba(0, 0, 0, 0.72);
  --gradient-mesh: radial-gradient(ellipse at 8% 0%, color-mix(in oklab, var(--color__amber) 10%, transparent), transparent 55%);
  color-scheme: dark;
}
/* Tier 2: light ("daylight") */
:root[data-mode='light'] {
  --color-bg: var(--color__paper); --color-bg-soft: var(--color__paper-soft);
  --color-bg-elevated: #fffefa; --color-bg-card: rgba(255, 254, 250, 0.9);
  --color-text: var(--color__ink); --color-text-soft: var(--color__slate-700);
  --color-text-dim: var(--color__slate-500); --color-text-dimmer: #6b7280;
  --color-accent: var(--color__amber-deep); --color-accent-soft: var(--color__amber);
  --color-accent-warm: var(--color__sodium-deep); --color-accent-hot: var(--color__sodium);
  --color-thread: var(--color__lime-deep);
  --color-border: rgba(10, 12, 16, 0.10); --color-border-strong: rgba(10, 12, 16, 0.22);
  --color-border-accent: rgba(180, 83, 9, 0.45);
  --shadow-card: 0 1px 0 rgba(10, 12, 16, 0.05), 0 12px 24px -16px rgba(10, 12, 16, 0.16);
  --gradient-mesh: radial-gradient(ellipse at 8% 0%, color-mix(in oklab, var(--color__amber) 6%, transparent), transparent 55%);
  color-scheme: light;
}
/* Tier 2: vibrant ("demo") */
:root[data-mode='vibrant'] {
  --color-bg: var(--color__ink-deep); --color-bg-soft: #0a0a14;
  --color-bg-elevated: #14122a; --color-bg-card: rgba(20, 18, 42, 0.74);
  --color-text: #fff8e8; --color-text-soft: #f0e0b8;
  --color-text-dim: #c8b890; --color-text-dimmer: #807058;
  --color-accent: var(--color__neon-amber); --color-accent-soft: #ffe55a;
  --color-accent-warm: var(--color__neon-sodium); --color-accent-hot: var(--color__iris);
  --color-thread: var(--color__lime);
  --color-border: rgba(255, 214, 10, 0.16); --color-border-strong: rgba(255, 214, 10, 0.36);
  --color-border-accent: rgba(255, 122, 26, 0.6);
  --shadow-card: 0 22px 60px -28px rgba(255, 122, 26, 0.5);
  --gradient-mesh: radial-gradient(ellipse at 8% 0%, color-mix(in oklab, var(--color__neon-amber) 22%, transparent), transparent 55%),
                   radial-gradient(ellipse at 92% 8%, color-mix(in oklab, var(--color__iris) 20%, transparent), transparent 60%);
  color-scheme: dark;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body { background: var(--color-bg); }
body {
  color: var(--color-text); font: 15px/1.5 var(--font__sans);
  background-image: var(--gradient-mesh); background-attachment: fixed;
  min-height: 100vh; overflow-x: hidden; -webkit-font-smoothing: antialiased;
}
a { color: inherit; }
h1, h2, h3 { font-family: var(--font__display); font-weight: 500; letter-spacing: -0.01em; }
.wrap { max-width: 1680px; margin: 0 auto; padding: 20px 16px 48px; }

.top { display: flex; flex-wrap: wrap; gap: 12px 24px; align-items: flex-end; justify-content: space-between; }
.top h1 { font-size: 22px; }
.top h1 em { font-style: normal; color: var(--color-accent); }
.top p { color: var(--color-text-dim); font: 12px var(--font__display); margin-top: 2px; }

.modes { display: inline-flex; border: 1px solid var(--color-border-strong); border-radius: var(--radius-lg); overflow: hidden; }
.modes button {
  background: transparent; border: 0; color: var(--color-text-dim); cursor: pointer;
  font: 12px var(--font__display); padding: 6px 12px;
}
.modes button[aria-checked='true'] { background: var(--color-accent); color: var(--color-bg); }

.stats { display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap: 8px; margin: 18px 0 14px; }
.stat {
  background: var(--color-bg-card); border: 1px solid var(--color-border); border-left: 3px solid var(--tone);
  border-radius: var(--radius-md); padding: 8px 12px; display: flex; flex-direction: column;
}
.stat b { font: 600 22px var(--font__display); color: var(--tone); }
.stat span { font-size: 12px; color: var(--color-text-dim); }
.stat--thread { --tone: var(--color-thread); } .stat--accent { --tone: var(--color-accent); }
.stat--warm { --tone: var(--color-accent-warm); } .stat--hot { --tone: var(--color-accent-hot); }

.filters { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; margin-bottom: 14px; }
.filters select, .filters input[type=search] {
  background: var(--color-bg-elevated); color: var(--color-text); border: 1px solid var(--color-border-strong);
  border-radius: var(--radius-md); padding: 6px 8px; font: 13px var(--font__sans); max-width: 100%;
}
.filters select { font-family: var(--font__display); font-size: 12px; white-space: pre; }
.filters input[type=search] { flex: 1 1 200px; min-width: 0; }
.filters select { flex: 0 1 260px; min-width: 0; }
.filters label { font-size: 13px; color: var(--color-text-soft); display: inline-flex; gap: 6px; align-items: center; }
.chips { display: flex; flex-wrap: wrap; gap: 6px; width: 100%; }
.chip {
  font: 11px var(--font__display); padding: 3px 8px; border-radius: 999px; cursor: pointer;
  background: transparent; color: var(--color-text-dim); border: 1px solid var(--color-border-strong);
}
.chip small { opacity: 0.7; }
.chips__more { display: contents; }
.chips__more summary { font: 11px var(--font__display); color: var(--color-accent); cursor: pointer; padding: 3px 4px; list-style: none; }
.chips__more[open] summary { display: none; }
.chip[aria-pressed='true'] { background: var(--color-accent); border-color: var(--color-accent); color: var(--color-bg); }

.layout > * { min-width: 0; }
.layout { display: grid; grid-template-columns: minmax(0, 1fr) 360px; gap: 16px; align-items: start; }
.board { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 10px; }
.col {
  background: var(--color-bg-soft); border: 1px solid var(--color-border); border-radius: var(--radius-lg);
  padding: 8px; min-width: 0;
}
.col__head { display: flex; justify-content: space-between; align-items: baseline; padding: 2px 4px 8px; }
.col__head h2 { font-size: 13px; text-transform: uppercase; letter-spacing: 0.06em; }
.col--in_flight .col__head h2 { color: var(--color-thread); }
.col--open .col__head h2 { color: var(--color-accent); }
.col--parked .col__head h2 { color: var(--color-accent-warm); }
.col__count { font: 12px var(--font__display); color: var(--color-text-dim); }
.col__cards { display: flex; flex-direction: column; gap: 6px; }
.col__more, .more-btn {
  font: 12px var(--font__display); color: var(--color-accent); background: transparent; border: 1px dashed var(--color-border-strong);
  border-radius: var(--radius-md); padding: 6px; text-align: center; cursor: pointer; width: 100%;
}
.card {
  background: var(--color-bg-card); border: 1px solid var(--color-border); border-radius: var(--radius-md);
  padding: 8px 10px; box-shadow: var(--shadow-card); min-width: 0;
}
.card--stale { border-left: 2px solid var(--color-accent-warm); }
.card__title { display: block; font-weight: 500; font-size: 13.5px; line-height: 1.35; text-decoration: none; overflow-wrap: anywhere; }
.card__title:hover { color: var(--color-accent); }
.card__crumb { font: 11px var(--font__display); color: var(--color-text-dim); margin-top: 3px; overflow-wrap: anywhere; }
.card__meta { display: flex; flex-wrap: wrap; gap: 4px 8px; align-items: center; margin-top: 6px; font-size: 11px; color: var(--color-text-dim); }
.card__status { color: var(--color-text-soft); max-width: 100%; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.badge { font: 10.5px var(--font__display); padding: 0 5px; border-radius: var(--radius-sm); border: 1px solid; }
.badge--stale { color: var(--color-accent-warm); border-color: var(--color-accent-warm); }
.badge--tasks { color: var(--color-accent); border-color: var(--color-border-accent); }

.rail { margin-top: 12px; display: flex; flex-wrap: wrap; gap: 8px; }
.rail__group { flex: 1 1 220px; background: var(--color-bg-soft); border: 1px solid var(--color-border); border-radius: var(--radius-lg); padding: 6px 10px; min-width: 0; }
.rail__group summary { cursor: pointer; font: 12px var(--font__display); color: var(--color-text-soft); }
.rail__cards { display: flex; flex-direction: column; gap: 6px; margin-top: 8px; }

.todos { background: var(--color-bg-soft); border: 1px solid var(--color-border); border-radius: var(--radius-lg); padding: 10px 12px; position: sticky; top: 12px; max-height: calc(100vh - 24px); overflow: auto; }
.todos h2 { font-size: 13px; text-transform: uppercase; letter-spacing: 0.06em; color: var(--color-accent); display: flex; justify-content: space-between; }
.todo-doc { margin-top: 12px; }
.todo-doc a { font-weight: 500; font-size: 13px; text-decoration: none; }
.todo-doc a:hover { color: var(--color-accent); }
.todo-doc .card__crumb { margin-bottom: 4px; }
.todo-doc ul { list-style: none; }
.todo-doc li { font-size: 12.5px; color: var(--color-text-soft); padding: 2px 0 2px 18px; position: relative; overflow-wrap: anywhere; }
.todo-doc li::before { content: '☐'; position: absolute; left: 0; color: var(--color-accent); }
.todo-doc li code { font: 10.5px var(--font__display); color: var(--color-text-dimmer); margin-right: 4px; }
.empty { color: var(--color-text-dimmer); font-size: 12px; padding: 6px 4px; }

@media (max-width: 1200px) {
  .layout { grid-template-columns: minmax(0, 1fr); }
  .todos { position: static; max-height: none; }
}
@media (max-width: 860px) {
  .board { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .stats { grid-template-columns: repeat(3, minmax(0, 1fr)); }
}
@media (max-width: 560px) {
  .board { grid-template-columns: minmax(0, 1fr); }
  .stats { grid-template-columns: repeat(2, minmax(0, 1fr)); }
}
</style>
</head>
<body>
<div class="wrap">
  <header class="top">
    <div>
      <h1>survey · <em>%%ROOT%%</em></h1>
      <p>%%META%%</p>
    </div>
    <div class="modes" role="radiogroup" aria-label="Color mode">
      <button type="button" role="radio" data-set-mode="light" aria-checked="false">light</button>
      <button type="button" role="radio" data-set-mode="dark" aria-checked="false">dark</button>
      <button type="button" role="radio" data-set-mode="vibrant" aria-checked="false">vibrant</button>
    </div>
  </header>

  <div class="stats">%%STATS%%</div>

  <form class="filters" onsubmit="return false">
    <select id="f-repo" aria-label="Repo">%%REPOS%%</select>
    <input id="f-q" type="search" placeholder="Search titles, status, paths…" aria-label="Search">
    <label><input id="f-stale" type="checkbox"> hide stale</label>
    <div class="chips" role="group" aria-label="Folders">%%CHIPS%%</div>
  </form>

  <div class="layout">
    <main>
      <div class="board" id="board">%%COLUMNS%%</div>
      <div class="rail" id="rail">%%RAIL%%</div>
    </main>
    <aside class="todos" id="todos" aria-label="Open checkboxes">
      <h2><span>Open checkboxes</span><span class="col__count" id="todo-count"></span></h2>
      <p class="empty">Needs JavaScript to list.</p>
    </aside>
  </div>
</div>

<script type="application/json" id="survey-data">%%DATA%%</script>
<script>
(function () {
  var root = document.documentElement;
  var KEY = 'cv-survey-mode';
  function setMode(mode) {
    root.setAttribute('data-mode', mode);
    try { localStorage.setItem(KEY, mode); } catch (e) {}
    syncModes();
  }
  function syncModes() {
    var cur = root.getAttribute('data-mode');
    document.querySelectorAll('[data-set-mode]').forEach(function (b) {
      b.setAttribute('aria-checked', String(b.dataset.setMode === cur));
    });
  }
  document.querySelectorAll('[data-set-mode]').forEach(function (b) {
    b.addEventListener('click', function () { setMode(b.dataset.setMode); });
  });
  syncModes();

  var DATA = JSON.parse(document.getElementById('survey-data').textContent);
  var TODAY = new Date(DATA.today + 'T00:00:00');
  var PAGE = 12, TODO_PAGE = 25;
  var state = { repo: '', q: '', hideStale: false, folders: new Set(), expanded: {}, todoLimit: TODO_PAGE };

  function daysAgo(s) { if (!s) return null; return Math.round((TODAY - new Date(s + 'T00:00:00')) / 864e5); }
  function rel(n) {
    if (n == null) return '?'; if (n <= 0) return 'today'; if (n < 60) return n + 'd ago';
    if (n < 730) return Math.floor(n / 30) + 'mo ago'; return Math.floor(n / 365) + 'y ago';
  }
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
    return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }

  function matches(d) {
    if (state.repo && !(d.repo === state.repo || (state.repo !== '.' && d.repo.indexOf(state.repo + '/') === 0))) return false;
    if (state.folders.size && !state.folders.has(d.folder)) return false;
    if (state.hideStale && d.stale) return false;
    if (state.q) {
      var hay = (d.title + ' ' + (d.status || '') + ' ' + d.path).toLowerCase();
      if (hay.indexOf(state.q) < 0) return false;
    }
    return true;
  }
  function inColumn(d, bucket) {
    if (d.bucket !== bucket) return false;
    if (bucket === 'done') { var n = daysAgo(d.updated); return n != null && n <= 30; }
    return true;
  }
  function sortCol(list, bucket) {
    return list.sort(function (a, b) {
      if (bucket === 'open' && a.stale !== b.stale) return a.stale ? 1 : -1;
      return (b.updated || '').localeCompare(a.updated || '');
    });
  }
  function card(d) {
    var crumb = d.repo === '.' ? d.folder : d.repo + ' / ' + d.folder;
    var badges = (d.stale ? '<span class="badge badge--stale">stale</span>' : '') +
      (d.tasks_open_count ? '<span class="badge badge--tasks">☐ ' + d.tasks_open_count + '</span>' : '');
    return '<article class="card' + (d.stale ? ' card--stale' : '') + '">' +
      '<a class="card__title" href="file://' + esc(d.abs_path) + '">' + esc(d.title) + '</a>' + cpBtn(d.abs_path) +
      '<div class="card__crumb">' + esc(crumb) + '</div>' +
      '<div class="card__meta"><span class="card__status" title="' + esc(d.status) + '">' + esc(d.status || '—') + '</span>' +
      '<span class="card__age">' + rel(daysAgo(d.updated)) + '</span>' + badges + '</div></article>';
  }
  function fill(container, list, key) {
    var limit = state.expanded[key] ? list.length : PAGE;
    var out = list.slice(0, limit).map(card).join('');
    if (!list.length) out = '<p class="empty">Nothing here.</p>';
    if (list.length > limit) out += '<button type="button" class="more-btn" data-expand="' + key + '">show all ' + list.length + '</button>';
    else if (state.expanded[key] && list.length > PAGE) out += '<button type="button" class="more-btn" data-collapse="' + key + '">show top ' + PAGE + '</button>';
    container.innerHTML = out;
  }

  function render() {
    var docs = DATA.docs.filter(matches);
    document.querySelectorAll('#board .col').forEach(function (col) {
      var b = col.dataset.bucket;
      var list = sortCol(docs.filter(function (d) { return inColumn(d, b); }), b);
      col.querySelector('.col__count').textContent = list.length;
      fill(col.querySelector('.col__cards'), list, b);
    });
    document.querySelectorAll('#rail .rail__group').forEach(function (g) {
      var b = g.dataset.bucket;
      var list = sortCol(docs.filter(function (d) { return d.bucket === b; }), b);
      g.querySelector('.col__count').textContent = list.length;
      if (g.open) fill(g.querySelector('.rail__cards'), list, 'rail-' + b);
    });
    renderTodos(docs);
  }

  function renderTodos(docs) {
    var withTasks = docs.filter(function (d) { return d.task_folder && d.tasks.length; })
      .sort(function (a, b) { return (b.updated || '').localeCompare(a.updated || ''); });
    var total = withTasks.reduce(function (n, d) { return n + d.tasks_open_count; }, 0);
    var el = document.getElementById('todos');
    var html = '<h2><span>Open checkboxes</span><span class="col__count">' + total + ' in ' + withTasks.length + ' docs</span></h2>';
    var shown = 0;
    for (var i = 0; i < withTasks.length && shown < state.todoLimit; i++) {
      var d = withTasks[i];
      var crumb = (d.repo === '.' ? '' : d.repo + ' / ') + d.folder + ' · ' + rel(daysAgo(d.updated));
      var items = d.tasks.slice(0, Math.max(1, state.todoLimit - shown));
      shown += items.length;
      html += '<div class="todo-doc"><a href="file://' + esc(d.abs_path) + '">' + esc(d.title) + '</a>' + cpBtn(d.abs_path) +
        '<div class="card__crumb">' + esc(crumb) + '</div><ul>' +
        items.map(function (t) { return '<li><code>L' + t.line + '</code>' + esc(t.text) + '</li>'; }).join('') +
        (d.tasks_open_count > items.length ? '<li class="empty">+' + (d.tasks_open_count - items.length) + ' more in file</li>' : '') +
        '</ul></div>';
    }
    if (!withTasks.length) html += '<p class="empty">No open checkboxes in plans, prompts, specs, issues, handoffs, or loops.</p>';
    else if (shown < total) html += '<p style="margin-top:10px"><button type="button" class="more-btn" data-todo-more>show more</button></p>';
    el.innerHTML = html;
  }

  document.getElementById('f-repo').addEventListener('change', function (e) { state.repo = e.target.value; render(); });
  document.getElementById('f-q').addEventListener('input', function (e) { state.q = e.target.value.trim().toLowerCase(); render(); });
  document.getElementById('f-stale').addEventListener('change', function (e) { state.hideStale = e.target.checked; render(); });
  document.querySelectorAll('.chip').forEach(function (c) {
    c.addEventListener('click', function () {
      var f = c.dataset.folder, on = !state.folders.has(f);
      if (on) state.folders.add(f); else state.folders.delete(f);
      c.setAttribute('aria-pressed', String(on)); render();
    });
  });
  document.querySelectorAll('#rail details').forEach(function (g) { g.addEventListener('toggle', render); });
  document.addEventListener('click', function (e) {
    var t = e.target;
    if (t.dataset.expand) { state.expanded[t.dataset.expand] = true; render(); }
    else if (t.dataset.collapse) { state.expanded[t.dataset.collapse] = false; render(); }
    else if (t.hasAttribute('data-todo-more')) { state.todoLimit += TODO_PAGE * 2; render(); }
  });
  render();
})();
</script>
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
    today = dt.date.fromisoformat(survey["generated_at"][:10])
    out = args.out or os.path.join(os.path.dirname(os.path.abspath(args.survey)), "survey-board.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(copy_path.inject(render(survey, today)))
    print(f"board: {len(survey['docs'])} docs -> {out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
