#!/usr/bin/env python3
"""Spike A, Ledger: render survey.json as a dense, table-first HTML dashboard.

  python3 spike_ledger.py path/to/survey.json [--out file.html]

One self-contained file: inline CSS, JS, and data. Three modes (light, dark, vibrant) per the
theme-system contract. Counts and the repo x bucket matrix are server-rendered so the page reads
with JavaScript off; JS adds the doc table, filters, sorting, and the task list.
Spec: context-v/specs/Survey-a-Scoped-Dashboard-of-Context-V.md
"""
import argparse

import copy_path
import collections
import html
import json
import os
import sys

BUCKETS = ["open", "in_flight", "done", "parked", "closed", "reference", "unmapped", "none"]
BUCKET_LABEL = {"open": "Open", "in_flight": "In flight", "done": "Done", "parked": "Parked",
                "closed": "Closed", "reference": "Reference", "unmapped": "Unmapped", "none": "None"}
FLAG_LABEL = {"no_frontmatter": "No frontmatter", "yaml_error": "YAML error", "no_type": "No type",
              "type_mismatch": "Type ≠ folder", "no_lede": "No lede", "no_status": "No status",
              "unmapped_status": "Unmapped status", "stale": "Stale (open, untouched)"}

e = html.escape


def shade(n, peak):
    """0..1 intensity on a soft curve so a 500-doc repo doesn't wash out the 5-doc ones."""
    if not n or not peak:
        return 0
    return round(min(1.0, (n / peak) ** 0.5), 3)


def matrix(survey):
    docs = survey["docs"]
    rows = collections.OrderedDict()
    for r in sorted(survey["repos"], key=lambda r: -r["docs"]):
        if r["docs"]:
            rows[r["path"]] = collections.Counter()
    for d in docs:
        c = rows.setdefault(d["repo"], collections.Counter())
        c[d["bucket"]] += 1
        c["_tasks"] += d["tasks_open_count"] if d["task_folder"] else 0
        c["_stale"] += "stale" in d["flags"]
        c["_total"] += 1
    peak = max([c[b] for c in rows.values() for b in BUCKETS] or [1])
    head = "".join(f'<th scope="col" class="b-{b}">{BUCKET_LABEL[b]}</th>' for b in BUCKETS)
    out = ['<table class="matrix"><thead><tr><th scope="col" class="rowh">Repo</th>'
           f'<th scope="col">Docs</th>{head}<th scope="col">Open tasks</th><th scope="col">Stale</th>'
           '</tr></thead><tbody>']
    totals = collections.Counter()
    for repo, c in rows.items():
        totals.update(c)
        cells = "".join(
            f'<td class="cell b-{b}" style="--i:{shade(c[b], peak)}">'
            f'<a href="#docs" data-repo="{e(repo)}" data-bucket="{b}">{c[b] or ""}</a></td>'
            for b in BUCKETS)
        out.append(f'<tr><th scope="row" class="rowh"><a href="#docs" data-repo="{e(repo)}">{e(repo)}</a></th>'
                   f'<td class="num">{c["_total"]}</td>{cells}'
                   f'<td class="num">{c["_tasks"] or ""}</td><td class="num warn">{c["_stale"] or ""}</td></tr>')
    foot = "".join(f'<td class="num">{totals[b]}</td>' for b in BUCKETS)
    out.append(f'</tbody><tfoot><tr><th scope="row" class="rowh">All repos</th><td class="num">{totals["_total"]}</td>'
               f'{foot}<td class="num">{totals["_tasks"]}</td><td class="num">{totals["_stale"]}</td></tr></tfoot></table>')
    return "".join(out), totals


def folders(docs):
    c = collections.Counter(d["folder"] for d in docs)
    peak = max(c.values() or [1])
    return "".join(
        f'<li><span class="lbl">{e(f)}</span><span class="bar" style="--w:{n / peak:.3f}"></span>'
        f'<span class="n">{n}</span></li>' for f, n in c.most_common())


def health(docs):
    flags = collections.Counter(f for d in docs for f in d["flags"])
    unmapped = collections.Counter(d["status"] for d in docs if d["bucket"] == "unmapped")
    rows = "".join(f'<li><a href="#docs" data-flag="{f}">{e(FLAG_LABEL.get(f, f))}</a><span class="n">{n}</span></li>'
                   for f, n in flags.most_common())
    um = "".join(f'<li><code>{e(s if len(s) < 90 else s[:87] + "…")}</code><span class="n">{n}</span></li>'
                 for s, n in unmapped.most_common(25))
    more = len(unmapped) - 25
    if more > 0:
        um += f'<li class="dim">…and {more} more</li>'
    return rows, um or '<li class="dim">None. Every status maps to a bucket.</li>'


CSS = r"""
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
  --radius-sm:2px;--radius-md:3px;--radius-lg:6px;
}
:root,:root[data-mode='dark']{
  --color-bg:var(--color__ink);--color-bg-soft:var(--color__ink-soft);--color-bg-elevated:var(--color__charcoal);
  --color-bg-card:rgba(22,26,35,.78);--color-bg-code:var(--color__ink-deep);
  --color-text:#e8eaef;--color-text-soft:var(--color__slate-200);--color-text-dim:var(--color__slate-400);
  --color-text-dimmer:var(--color__slate-500);--color-text-faint:var(--color__slate-600);
  --color-accent:var(--color__amber);--color-accent-soft:var(--color__amber-soft);
  --color-accent-warm:var(--color__sodium);--color-accent-hot:var(--color__sodium-deep);
  --color-thread:var(--color__lime);--color-thread-soft:var(--color__lime-soft);
  --color-border:rgba(232,234,239,.08);--color-border-strong:rgba(232,234,239,.18);--color-border-accent:rgba(251,191,36,.45);
  --heat:251,191,36;--b-open:#fbbf24;--b-in_flight:#a3e635;--b-done:#5eead4;--b-parked:#f97316;
  --b-closed:#8b91a3;--b-reference:#818cf8;--b-unmapped:#f472b6;--b-none:#5b6273;
  color-scheme:dark;
}
:root[data-mode='light']{
  --color-bg:var(--color__paper);--color-bg-soft:var(--color__paper-soft);--color-bg-elevated:#fffefa;
  --color-bg-card:rgba(255,254,250,.9);--color-bg-code:var(--color__paper-deep);
  --color-text:var(--color__ink);--color-text-soft:var(--color__slate-700);--color-text-dim:var(--color__slate-500);
  --color-text-dimmer:#6b7280;--color-text-faint:var(--color__slate-400);
  --color-accent:var(--color__amber-deep);--color-accent-soft:var(--color__amber);
  --color-accent-warm:var(--color__sodium-deep);--color-accent-hot:var(--color__sodium);
  --color-thread:var(--color__lime-deep);--color-thread-soft:var(--color__lime);
  --color-border:rgba(10,12,16,.10);--color-border-strong:rgba(10,12,16,.22);--color-border-accent:rgba(180,83,9,.45);
  --heat:217,119,6;--b-open:#b45309;--b-in_flight:#4d7c0f;--b-done:#0f766e;--b-parked:#9a3412;
  --b-closed:#5b6273;--b-reference:#4f46e5;--b-unmapped:#be185d;--b-none:#8b91a3;
  color-scheme:light;
}
:root[data-mode='vibrant']{
  --color-bg:var(--color__ink-deep);--color-bg-soft:#0a0a14;--color-bg-elevated:#14122a;
  --color-bg-card:rgba(20,18,42,.74);--color-bg-code:#050410;
  --color-text:#fff8e8;--color-text-soft:#f0e0b8;--color-text-dim:#c8b890;--color-text-dimmer:#807058;--color-text-faint:#4a4030;
  --color-accent:var(--color__neon-amber);--color-accent-soft:#ffe55a;
  --color-accent-warm:var(--color__neon-sodium);--color-accent-hot:var(--color__iris);
  --color-thread:var(--color__lime);--color-thread-soft:#c8ff5a;
  --color-border:rgba(255,214,10,.16);--color-border-strong:rgba(255,214,10,.36);--color-border-accent:rgba(255,122,26,.6);
  --heat:255,122,26;--b-open:#ffd60a;--b-in_flight:#c8ff5a;--b-done:#2ef2d0;--b-parked:#ff7a1a;
  --b-closed:#a8a0c8;--b-reference:#9aa5ff;--b-unmapped:#ff5ec8;--b-none:#807058;
  color-scheme:dark;
}
*,*::before,*::after{box-sizing:border-box}*{margin:0;padding:0}
html,body{background:var(--color-bg)}
body{color:var(--color-text);font:14px/1.5 var(--font__sans);-webkit-font-smoothing:antialiased;
  background-image:radial-gradient(var(--color-border) 1px,transparent 1px);background-size:28px 28px}
:root[data-mode='vibrant'] body{background-image:radial-gradient(ellipse at 8% 0%,rgba(255,214,10,.14),transparent 50%),
  radial-gradient(ellipse at 92% 6%,rgba(129,140,248,.18),transparent 55%);background-size:auto;background-repeat:no-repeat;background-attachment:fixed}
a{color:inherit}
h1,h2,h3{font-family:var(--font__display);font-weight:500;letter-spacing:-.01em}
code,.mono,.num,.n,time{font-family:var(--font__mono)}
.wrap{max-width:1400px;margin:0 auto;padding:20px 16px 64px}
header.top{display:flex;flex-wrap:wrap;gap:12px 24px;align-items:flex-end;justify-content:space-between;
  border-bottom:1px solid var(--color-border-strong);padding-bottom:14px;margin-bottom:18px}
.eyebrow{font:500 11px/1 var(--font__mono);text-transform:uppercase;letter-spacing:.12em;color:var(--color-accent)}
h1{font-size:clamp(20px,3vw,28px);margin:6px 0 4px}
h1 .root{color:var(--color-accent)}
.meta{font:12px/1.6 var(--font__mono);color:var(--color-text-dim);word-break:break-all}
.modes{display:inline-flex;border:1px solid var(--color-border-strong);border-radius:var(--radius-pill,999px);padding:2px;gap:2px}
.modes button{font:500 11px var(--font__mono);text-transform:uppercase;letter-spacing:.08em;background:none;border:0;
  color:var(--color-text-dim);padding:6px 10px;border-radius:999px;cursor:pointer}
.modes button[aria-checked='true']{background:var(--color-accent);color:var(--color-bg)}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(130px,100%),1fr));gap:8px;margin-bottom:18px}
.kpi{background:var(--color-bg-card);border:1px solid var(--color-border);border-radius:var(--radius-lg);padding:10px 12px}
.kpi b{display:block;font:500 22px/1.1 var(--font__display);color:var(--color-text)}
.kpi span{font:11px var(--font__mono);text-transform:uppercase;letter-spacing:.08em;color:var(--color-text-dim)}
.kpi.accent b{color:var(--color-accent)}.kpi.thread b{color:var(--color-thread)}.kpi.warm b{color:var(--color-accent-warm)}
nav.tabs{display:flex;gap:4px;border-bottom:1px solid var(--color-border-strong);margin:8px 0 14px;overflow-x:auto}
nav.tabs a{font:500 12px var(--font__mono);text-transform:uppercase;letter-spacing:.08em;text-decoration:none;
  padding:8px 12px;color:var(--color-text-dim);border-bottom:2px solid transparent;white-space:nowrap}
nav.tabs a[aria-selected='true']{color:var(--color-accent);border-bottom-color:var(--color-accent)}
section.panel{min-width:0;background:var(--color-bg-card);border:1px solid var(--color-border);border-radius:var(--radius-lg);padding:14px;margin-bottom:14px}
section.panel>h2{font-size:13px;text-transform:uppercase;letter-spacing:.1em;color:var(--color-text-soft);margin-bottom:10px;display:flex;flex-wrap:wrap;gap:4px 10px;align-items:baseline}
section.panel>h2 small{font:11px var(--font__mono);text-transform:none;letter-spacing:0;color:var(--color-text-dimmer)}
.scroll{overflow-x:auto;max-width:100%;min-width:0}
.wrap>*{min-width:0}
table{border-collapse:collapse;width:100%;font-size:12.5px}
th,td{padding:5px 8px;border-bottom:1px solid var(--color-border);text-align:left;white-space:nowrap}
thead th{font:500 10.5px var(--font__mono);text-transform:uppercase;letter-spacing:.06em;color:var(--color-text-dim);
  position:sticky;top:0;background:var(--color-bg-elevated);z-index:1}
.matrix .rowh{font:12px var(--font__mono);max-width:340px;overflow:hidden;text-overflow:ellipsis}
.matrix .rowh a{text-decoration:none}.matrix .rowh a:hover{color:var(--color-accent)}
.matrix td.cell{padding:0;text-align:center;min-width:56px;background:rgba(var(--heat),calc(var(--i) * .55))}
.matrix td.cell a{display:block;padding:5px 6px;text-decoration:none;font-family:var(--font__mono);color:var(--color-text)}
.matrix td.cell a:hover{outline:1px solid var(--color-accent);outline-offset:-1px}
.matrix tfoot td,.matrix tfoot th{border-top:1px solid var(--color-border-strong);font-weight:600}
.num{text-align:right}.warn{color:var(--color-accent-warm)}
thead th[class^='b-']::before{content:'';display:inline-block;width:7px;height:7px;border-radius:50%;margin-right:5px;background:var(--dot)}
.b-open{--dot:var(--b-open)}.b-in_flight{--dot:var(--b-in_flight)}.b-done{--dot:var(--b-done)}.b-parked{--dot:var(--b-parked)}
.b-closed{--dot:var(--b-closed)}.b-reference{--dot:var(--b-reference)}.b-unmapped{--dot:var(--b-unmapped)}.b-none{--dot:var(--b-none)}
.grid2{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(320px,100%),1fr));gap:14px}
ul.bars,ul.list{list-style:none;display:grid;gap:3px}
ul.bars li{display:grid;grid-template-columns:120px 1fr 48px;gap:8px;align-items:center;font:12px var(--font__mono)}
ul.bars .bar{height:8px;border-radius:var(--radius-sm);background:linear-gradient(90deg,var(--color-accent),var(--color-accent-warm));
  width:calc(var(--w) * 100%);min-width:2px}
ul.bars .lbl{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.n{color:var(--color-text-dim);text-align:right;font-size:12px}
ul.list li{display:flex;justify-content:space-between;gap:12px;font-size:12.5px;padding:3px 0;border-bottom:1px dashed var(--color-border)}
ul.list code{font-size:11.5px;color:var(--color-text-soft);overflow-wrap:anywhere}
.dim{color:var(--color-text-dimmer)}
.filters{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-bottom:10px}
.filters input,.filters select{font:12px var(--font__mono);background:var(--color-bg-soft);color:var(--color-text);
  border:1px solid var(--color-border-strong);border-radius:var(--radius-md);padding:6px 8px;max-width:100%}
.filters input{flex:1 1 220px}
.chip{font:500 10.5px var(--font__mono);text-transform:uppercase;letter-spacing:.05em;border:1px solid var(--color-border-strong);
  background:none;color:var(--color-text-soft);border-radius:999px;padding:4px 9px;cursor:pointer;display:inline-flex;align-items:center;gap:5px}
.chip::before{content:'';width:7px;height:7px;border-radius:50%;background:var(--dot)}
.chip[aria-pressed='true']{background:var(--color-bg-elevated);border-color:var(--dot);color:var(--color-text)}
span.chip{cursor:default;padding:2px 7px;font-size:10px}
.docs td.t{white-space:normal;min-width:260px;max-width:460px}
.docs td.t a{text-decoration:none;font-weight:500}.docs td.t a:hover{color:var(--color-accent);text-decoration:underline}
.docs td.t .lede{display:block;color:var(--color-text-dim);font-size:11.5px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;max-width:440px}
.docs td.repo{font:11.5px var(--font__mono);color:var(--color-text-soft);max-width:220px;overflow:hidden;text-overflow:ellipsis}
.docs td.st{font-size:11.5px;color:var(--color-text-soft);max-width:220px;overflow:hidden;text-overflow:ellipsis}
.docs th[data-k]{cursor:pointer;user-select:none}.docs th[data-k]:hover{color:var(--color-accent)}
.docs th[aria-sort='ascending']::after{content:' ↑'}.docs th[aria-sort='descending']::after{content:' ↓'}
.flag{font:10px var(--font__mono);color:var(--color-accent-warm);margin-right:4px}
.pager{display:flex;gap:8px;align-items:center;justify-content:space-between;margin-top:10px;font:12px var(--font__mono);color:var(--color-text-dim)}
.pager button{font:inherit;background:var(--color-bg-soft);color:var(--color-text);border:1px solid var(--color-border-strong);border-radius:var(--radius-md);padding:4px 10px;cursor:pointer}
.pager button:disabled{opacity:.4;cursor:default}
.tasks h3{font-size:13px;margin:16px 0 6px;color:var(--color-accent)}
.tasks .item{padding:6px 0;border-bottom:1px solid var(--color-border)}
.tasks .item a{text-decoration:none;font-weight:500}.tasks .item a:hover{color:var(--color-accent)}
.tasks .item .sub{font:11px var(--font__mono);color:var(--color-text-dim)}
.tasks ol{list-style:none;margin:4px 0 0}.tasks ol li{font-size:12.5px;padding:1px 0 1px 0;display:flex;gap:8px}
.tasks ol li .ln{font:11px var(--font__mono);color:var(--color-text-dimmer);min-width:46px;text-align:right}
.tasks ol li .ln a{text-decoration:none}
[hidden]{display:none!important}
.nojs-note{font:12px var(--font__mono);color:var(--color-text-dim);padding:8px 0}
@media (max-width:640px){ul.bars li{grid-template-columns:90px 1fr 40px}.matrix .rowh{max-width:160px}}
"""

PREPAINT = r"""(function(){var m=null;try{var h=location.hash.match(/mode=(light|dark|vibrant)/);if(h)m=h[1];}catch(e){}
if(!m){try{m=localStorage.getItem('cv-survey-mode');}catch(e){}}
if(m!=='light'&&m!=='dark'&&m!=='vibrant')m='dark';document.documentElement.setAttribute('data-mode',m);})();"""

JS = r"""
(function(){
var S=JSON.parse(document.getElementById('survey-data').textContent);
var root=document.documentElement;
// mode toggle
var btns=document.querySelectorAll('.modes button');
function setMode(m){root.setAttribute('data-mode',m);btns.forEach(function(b){b.setAttribute('aria-checked',b.dataset.mode===m?'true':'false')});
  try{localStorage.setItem('cv-survey-mode',m)}catch(e){}}
btns.forEach(function(b){b.addEventListener('click',function(){setMode(b.dataset.mode)})});
setMode(root.getAttribute('data-mode')||'dark');

// tabs
var tabs=document.querySelectorAll('nav.tabs a'),views=document.querySelectorAll('[data-view]');
function show(v){tabs.forEach(function(t){t.setAttribute('aria-selected',t.dataset.tab===v?'true':'false')});
  views.forEach(function(p){p.hidden=p.dataset.view!==v})}
tabs.forEach(function(t){t.addEventListener('click',function(ev){ev.preventDefault();show(t.dataset.tab)})});
document.querySelectorAll('.nojs-note').forEach(function(n){n.hidden=true});
if(/tab=tasks/.test(location.hash))setTimeout(function(){show('tasks')},0);

var BL=%BUCKET_LABEL%, FL=%FLAG_LABEL%;
function esc(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function href(d){return 'file://'+encodeURI(d.abs_path)}

// doc table
var docs=S.docs, state={q:'',repo:'',flag:'',buckets:{},sort:'updated',dir:-1,page:0,per:100};
var qEl=document.getElementById('f-q'),rEl=document.getElementById('f-repo'),fEl=document.getElementById('f-flag');
var tbody=document.querySelector('.docs tbody'),info=document.getElementById('pg-info');
var chips=document.querySelectorAll('.chips .chip');
function filtered(){var q=state.q.toLowerCase(),anyB=Object.keys(state.buckets).length>0;
  return docs.filter(function(d){
    if(state.repo&&d.repo!==state.repo)return false;
    if(state.flag&&d.flags.indexOf(state.flag)<0)return false;
    if(anyB&&!state.buckets[d.bucket])return false;
    if(q&&(d.title+' '+d.path+' '+(d.status||'')+' '+(d.lede||'')+' '+d.tags.join(' ')).toLowerCase().indexOf(q)<0)return false;
    return true})}
function key(d,k){var v=d[k];if(k==='flags')return d.flags.length;if(k==='tasks_open_count')return d.task_folder?d.tasks_open_count:0;
  return v==null?'':(typeof v==='string'?v.toLowerCase():v)}
function render(){var rows=filtered(),k=state.sort,dir=state.dir;
  rows.sort(function(a,b){var x=key(a,k),y=key(b,k);return x<y?-dir:x>y?dir:0});
  var pages=Math.max(1,Math.ceil(rows.length/state.per));if(state.page>=pages)state.page=pages-1;
  var slice=rows.slice(state.page*state.per,(state.page+1)*state.per);
  tbody.innerHTML=slice.map(function(d){
    var fl=d.flags.map(function(f){return '<span class="flag" title="'+esc(FL[f]||f)+'">'+esc(f)+'</span>'}).join('');
    return '<tr><td class="t"><a href="'+href(d)+'" title="'+esc(d.path)+'">'+esc(d.title)+'</a>'+cpBtn(d.abs_path)+(d.lede?'<span class="lede">'+esc(d.lede)+'</span>':'')+'</td>'
      +'<td class="repo" title="'+esc(d.repo)+'">'+esc(d.repo)+'</td><td class="mono">'+esc(d.folder)+'</td>'
      +'<td><span class="chip b-'+d.bucket+'">'+esc(BL[d.bucket])+'</span></td>'
      +'<td class="st" title="'+esc(d.status||'')+'">'+esc(d.status||'—')+'</td>'
      +'<td><time>'+esc(d.updated)+'</time></td><td class="num">'+(d.task_folder&&d.tasks_open_count?d.tasks_open_count:'')+'</td><td>'+fl+'</td></tr>'}).join('')
    ||'<tr><td colspan="8" class="dim">No docs match.</td></tr>';
  info.textContent=rows.length+' docs · page '+(state.page+1)+' of '+pages;
  document.getElementById('pg-prev').disabled=state.page===0;document.getElementById('pg-next').disabled=state.page>=pages-1;
  document.querySelectorAll('.docs th[data-k]').forEach(function(th){th.setAttribute('aria-sort',th.dataset.k===k?(dir>0?'ascending':'descending'):'none')});
  chips.forEach(function(c){c.setAttribute('aria-pressed',state.buckets[c.dataset.bucket]?'true':'false')});
  rEl.value=state.repo;fEl.value=state.flag}
var t;qEl.addEventListener('input',function(){clearTimeout(t);t=setTimeout(function(){state.q=qEl.value;state.page=0;render()},120)});
rEl.addEventListener('change',function(){state.repo=rEl.value;state.page=0;render()});
fEl.addEventListener('change',function(){state.flag=fEl.value;state.page=0;render()});
chips.forEach(function(c){c.addEventListener('click',function(){var b=c.dataset.bucket;if(state.buckets[b])delete state.buckets[b];else state.buckets[b]=1;state.page=0;render()})});
document.querySelectorAll('.docs th[data-k]').forEach(function(th){th.addEventListener('click',function(){
  if(state.sort===th.dataset.k)state.dir=-state.dir;else{state.sort=th.dataset.k;state.dir=th.dataset.k==='updated'||th.dataset.k==='tasks_open_count'?-1:1}render()})});
document.getElementById('pg-prev').onclick=function(){state.page--;render()};
document.getElementById('pg-next').onclick=function(){state.page++;render()};
// matrix / health drill-down
document.querySelectorAll('a[data-repo],a[data-flag]').forEach(function(a){a.addEventListener('click',function(ev){ev.preventDefault();
  state.repo=a.dataset.repo||'';state.flag=a.dataset.flag||'';state.buckets={};if(a.dataset.bucket)state.buckets[a.dataset.bucket]=1;
  state.q='';qEl.value='';state.page=0;show('dash');render();document.getElementById('docs').scrollIntoView({behavior:'smooth'})})});
render();

// task list
var T=document.getElementById('tasks-body');
function docLine(d){return '<div class="item"><a href="'+href(d)+'">'+esc(d.title)+'</a>'+cpBtn(d.abs_path)+' <span class="chip b-'+d.bucket+'">'+esc(d.status||BL[d.bucket])+'</span>'
  +'<div class="sub">'+esc(d.repo)+' · '+esc(d.folder)+' · '+esc(d.updated)+(d.tasks_open_count&&d.task_folder?' · '+d.tasks_open_count+' open boxes':'')+'</div></div>'}
var inflight=docs.filter(function(d){return d.bucket==='in_flight'&&(d.folder==='specs'||d.folder==='plans'||d.folder==='prompts')})
  .sort(function(a,b){return a.updated<b.updated?1:-1});
var issues=docs.filter(function(d){return d.folder==='issues'&&(d.bucket==='open'||d.bucket==='in_flight')}).sort(function(a,b){return a.updated<b.updated?1:-1});
var hand={};docs.forEach(function(d){if(d.folder==='handoffs'&&(!hand[d.repo]||hand[d.repo].updated<d.updated))hand[d.repo]=d});
var handoffs=Object.keys(hand).map(function(k){return hand[k]}).sort(function(a,b){return a.updated<b.updated?1:-1});
var boxes=docs.filter(function(d){return d.task_folder&&d.tasks_open.length&&d.bucket!=='closed'&&d.bucket!=='done'})
  .sort(function(a,b){return a.updated<b.updated?1:-1});
var shownBoxes=0,MAXB=60;
var boxHtml=boxes.slice(0,MAXB).map(function(d){shownBoxes++;
  return '<div class="item"><a href="'+href(d)+'">'+esc(d.title)+'</a>'+cpBtn(d.abs_path)+'<div class="sub">'+esc(d.repo)+' · '+esc(d.folder)+' · '+esc(d.status||'no status')+' · '+esc(d.updated)+'</div><ol>'
  +d.tasks_open.slice(0,12).map(function(t){return '<li><span class="ln">L'+t.line+'</span><span>'+esc(t.text)+'</span></li>'}).join('')
  +(d.tasks_open_count>12?'<li class="dim"><span class="ln"></span>…'+(d.tasks_open_count-12)+' more</li>':'')+'</ol></div>'}).join('');
T.innerHTML='<h3>In flight · specs, plans, prompts ('+inflight.length+')</h3>'+(inflight.map(docLine).join('')||'<p class="dim">None.</p>')
  +'<h3>Open issues ('+issues.length+')</h3>'+(issues.slice(0,80).map(docLine).join('')||'<p class="dim">None.</p>')
  +'<h3>Newest handoff per repo ('+handoffs.length+')</h3>'+(handoffs.map(docLine).join('')||'<p class="dim">No handoffs in scope.</p>')
  +'<h3>Unchecked boxes in open work ('+boxes.length+' docs'+(boxes.length>MAXB?', newest '+MAXB+' shown':'')+')</h3>'+(boxHtml||'<p class="dim">None.</p>');
})();
"""


def render(survey):
    docs = survey["docs"]
    mat, totals = matrix(survey)
    flags_html, unmapped_html = health(docs)
    n = len(docs)
    tasks = sum(d["tasks_open_count"] for d in docs if d["task_folder"])
    stale = sum("stale" in d["flags"] for d in docs)
    repos_with = sum(1 for r in survey["repos"] if r["docs"])
    kpis = [
        ("Docs", n, ""), ("Repos with context-v", repos_with, ""),
        ("Open", totals["open"], "accent"), ("In flight", totals["in_flight"], "thread"),
        ("Done", totals["done"], ""), ("Open boxes", tasks, "warm"), ("Stale", stale, "warm"),
    ]
    kpi_html = "".join(f'<div class="kpi {c}"><b>{v:,}</b><span>{e(l)}</span></div>' for l, v, c in kpis)
    repo_opts = "".join(f'<option value="{e(r["path"])}">{e(r["path"])} ({r["docs"]})</option>'
                        for r in sorted(survey["repos"], key=lambda r: r["path"]) if r["docs"])
    flag_counts = collections.Counter(f for d in docs for f in d["flags"])
    flag_opts = "".join(f'<option value="{f}">{e(FLAG_LABEL.get(f, f))} ({c})</option>' for f, c in flag_counts.most_common())
    chips = "".join(f'<button type="button" class="chip b-{b}" data-bucket="{b}" aria-pressed="false">{BUCKET_LABEL[b]}</button>'
                    for b in BUCKETS)
    # Slim the payload: the table and task list don't need everything scan.py keeps.
    keep = ("path", "abs_path", "repo", "folder", "title", "lede", "status", "bucket", "updated",
            "tags", "tasks_open", "tasks_open_count", "task_folder", "flags")
    data = {"docs": [{k: d.get(k) for k in keep} for d in docs]}
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    js = (JS.replace("%BUCKET_LABEL%", json.dumps(BUCKET_LABEL))
            .replace("%FLAG_LABEL%", json.dumps(FLAG_LABEL, ensure_ascii=False)))
    title = f"Survey · {survey['root_name']}"
    return f"""<!doctype html>
<html lang="en" data-mode="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title>
<script>{PREPAINT}</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500;600&display=swap">
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
<header class="top">
  <div>
    <div class="eyebrow">context-v survey · ledger · {e(survey['scope'])} scope</div>
    <h1>Survey of <span class="root">{e(survey['root_name'])}</span></h1>
    <div class="meta">{e(survey['root'])}<br>generated {e(survey['generated_at'])} · scanned in {survey['scan_seconds']}s · stale = open or in flight, untouched {survey['stale_days']}+ days</div>
  </div>
  <div class="modes" role="radiogroup" aria-label="Color mode">
    <button type="button" role="radio" data-mode="light" aria-checked="false" aria-label="Light mode">Light</button>
    <button type="button" role="radio" data-mode="dark" aria-checked="true" aria-label="Dark mode">Dark</button>
    <button type="button" role="radio" data-mode="vibrant" aria-checked="false" aria-label="Vibrant mode">Vibrant</button>
  </div>
</header>
<div class="kpis">{kpi_html}</div>
<nav class="tabs" role="tablist">
  <a href="#dash" role="tab" data-tab="dash" aria-selected="true">Dashboard</a>
  <a href="#tasks" role="tab" data-tab="tasks" aria-selected="false">Task list</a>
</nav>
<div data-view="dash">
<section class="panel"><h2>Repo × lifecycle <small>click a cell to filter the docs table</small></h2>
  <div class="scroll">{mat}</div></section>
<div class="grid2">
  <section class="panel"><h2>Folders</h2><ul class="bars">{folders(docs)}</ul></section>
  <section class="panel"><h2>Health <small>surfaced, never fixed</small></h2><ul class="list">{flags_html}</ul>
    <h2 style="margin-top:14px">Unmapped statuses <small>verbatim</small></h2><ul class="list">{unmapped_html}</ul></section>
</div>
<section class="panel" id="docs"><h2>Docs</h2>
  <p class="nojs-note">The doc table and task list need JavaScript; the counts above don't.</p>
  <div class="filters">
    <input id="f-q" type="search" placeholder="Search title, path, status, tags…" aria-label="Search docs">
    <select id="f-repo" aria-label="Repo"><option value="">All repos</option>{repo_opts}</select>
    <select id="f-flag" aria-label="Health flag"><option value="">Any health</option>{flag_opts}</select>
  </div>
  <div class="filters chips" role="group" aria-label="Lifecycle buckets">{chips}</div>
  <div class="scroll"><table class="docs"><thead><tr>
    <th data-k="title">Title</th><th data-k="repo">Repo</th><th data-k="folder">Folder</th><th data-k="bucket">Bucket</th>
    <th data-k="status">Status</th><th data-k="updated">Updated</th><th data-k="tasks_open_count" class="num">Boxes</th><th data-k="flags">Flags</th>
  </tr></thead><tbody></tbody></table></div>
  <div class="pager"><button id="pg-prev" type="button">← Prev</button><span id="pg-info"></span><button id="pg-next" type="button">Next →</button></div>
</section>
</div>
<div data-view="tasks" hidden>
<section class="panel tasks" id="tasks"><h2>Task list <small>in-flight work, open issues, handoffs, unchecked boxes</small></h2>
  <div id="tasks-body"><p class="nojs-note">Needs JavaScript.</p></div></section>
</div>
</div>
<script type="application/json" id="survey-data">{payload}</script>
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
    out = args.out or os.path.join(os.path.dirname(os.path.abspath(args.survey)), "survey-ledger.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(copy_path.inject(render(survey)))
    print(f"ledger: {len(survey['docs'])} docs -> {out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
