"""A repo-tree scope picker, shared by the survey renderers.

One compact control: a button naming the current scope, opening a parent-child tree of the
repos as they nest (pseudomonorepo > child > grandchild), each with the docs at or below it.
Picking a repo scopes the page to it and everything under it. Indent is 10px a level, so the
tree stays tight on an already crowded dashboard.

The scope lives in the URL hash (`#scope=astro-knots`, beside `mode=`), so it survives a reload
and can be linked. Renderers listen for it:

    cvScope.get()            -> '' (all) or a repo path
    cvScope.has(repoPath)    -> true when repoPath is the scope or sits under it
    cvScope.set(path)        -> change it (fires the event)
    document.addEventListener('cv-scope', fn)
"""
import html


def _tree(survey):
    """Repos keyed by path, children per parent, and docs at-or-below each repo."""
    repos = {r["path"]: r for r in survey["repos"]}
    kids = {}
    for p, r in repos.items():
        parent = r.get("parent")
        if parent in repos and parent != p:
            kids.setdefault(parent, []).append(p)
    below = {}

    def total(p):
        if p not in below:
            below[p] = (repos[p]["docs"] or 0) + sum(total(c) for c in kids.get(p, []))
        return below[p]

    for p in repos:
        total(p)
    tops = [p for p, r in repos.items() if r.get("parent") not in repos or r.get("parent") == p]
    return repos, kids, below, tops


def picker(survey):
    """The control's markup. Repos with no docs at or below them are left out."""
    repos, kids, below, tops = _tree(survey)
    esc = lambda s: html.escape(str(s), quote=True)

    def name(p):
        return survey["root_name"] if p == "." else repos[p]["name"]

    def rows(paths, depth):
        out = []
        for p in sorted(paths, key=lambda p: name(p).lower()):
            if not below[p]:
                continue
            sub = [c for c in kids.get(p, []) if below[c]]
            # The anchor root's children read as top level; it's already "All repos".
            nested = depth if tops != ["."] else max(depth - 1, 0)
            if p == "." and tops == ["."]:
                out.extend(rows(sub, depth + 1))
                continue
            out.append(
                f'<li class="sp__node" data-path="{esc(p)}" style="--d:{nested}">'
                + (f'<button type="button" class="sp__tw" aria-label="Expand {esc(name(p))}" aria-expanded="false"></button>'
                   if sub else '<span class="sp__tw sp__tw--leaf"></span>')
                + f'<button type="button" class="sp__pick" data-scope="{esc(p)}">{esc(name(p))}'
                  f'<small>{below[p]}</small></button>'
                + (f'<ul class="sp__kids" hidden>{"".join(rows(sub, depth + 1))}</ul>' if sub else "")
                + "</li>")
        return out

    root_own = repos["."]["docs"] if "." in repos else 0
    root_row = (f'<li class="sp__node" data-path="." style="--d:0"><span class="sp__tw sp__tw--leaf"></span>'
                f'<button type="button" class="sp__pick" data-scope="." data-exact="1">{esc(survey["root_name"])} '
                f'<em>root only</em><small>{root_own}</small></button></li>') if tops == ["."] and root_own else ""
    total = sum(below[p] for p in tops)
    return (
        '<div class="sp" id="scope-picker">'
        '<button type="button" class="sp__btn" aria-haspopup="true" aria-expanded="false">'
        '<span class="sp__label">scope</span> <b class="sp__cur">All repos</b> <span aria-hidden="true">▾</span></button>'
        '<div class="sp__panel" hidden>'
        '<input type="search" class="sp__q" placeholder="find a repo…" aria-label="Find a repo">'
        f'<ul class="sp__tree"><li class="sp__node" style="--d:0"><span class="sp__tw sp__tw--leaf"></span>'
        f'<button type="button" class="sp__pick" data-scope="">All repos<small>{total}</small></button></li>'
        f'{root_row}{"".join(rows(tops, 0))}</ul></div></div>')


CSS = """
.sp{position:relative;display:inline-block;flex:0 0 auto}
.sp__btn{display:inline-flex;align-items:center;gap:.35em;background:var(--color-bg-elevated,transparent);
  color:var(--color-text,inherit);border:1px solid var(--color-border-strong,currentColor);border-radius:3px;
  padding:5px 8px;font:12px var(--font__display,var(--font__mono,ui-monospace,monospace));cursor:pointer;max-width:340px}
.sp__btn:hover,.sp__btn[aria-expanded=true]{border-color:var(--color-accent,currentColor)}
.sp__label{color:var(--color-text-dim,inherit)}
.sp__cur{font-weight:500;color:var(--color-accent,inherit);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.sp__panel{position:absolute;z-index:50;top:calc(100% + 3px);left:0;width:300px;max-width:calc(100vw - 32px);
  max-height:62vh;overflow:auto;background:var(--color-bg-elevated,#111);border:1px solid var(--color-border-strong,currentColor);
  border-radius:4px;padding:4px;box-shadow:0 14px 32px -16px rgba(0,0,0,.6)}
.sp__q{width:100%;margin:0 0 3px;padding:3px 6px;background:var(--color-bg,transparent);color:var(--color-text,inherit);
  border:1px solid var(--color-border,currentColor);border-radius:3px;font:12px var(--font__sans,inherit)}
.sp__tree,.sp__kids{list-style:none;margin:0;padding:0}
.sp__node{display:grid;grid-template-columns:12px 1fr;align-items:center;padding-left:calc(var(--d)*10px)}
.sp__node>.sp__kids{grid-column:1/-1;margin-left:calc(var(--d)*-10px)}
.sp__tw{width:12px;height:16px;padding:0;border:0;background:transparent;color:var(--color-text-dim,inherit);cursor:pointer;font-size:9px;line-height:16px}
.sp__tw::before{content:'▸'}.sp__tw[aria-expanded=true]::before{content:'▾'}.sp__tw--leaf::before{content:''}
.sp__pick{display:flex;align-items:baseline;gap:6px;width:100%;min-width:0;text-align:left;border:0;border-radius:2px;
  background:transparent;color:var(--color-text-soft,inherit);padding:1px 4px;line-height:1.35;
  font:12px var(--font__display,var(--font__mono,ui-monospace,monospace));cursor:pointer;overflow-wrap:anywhere}
.sp__pick small{margin-left:auto;color:var(--color-text-dimmer,inherit);font-size:10.5px}
.sp__pick em{font-style:normal;color:var(--color-text-dimmer,inherit);font-size:10.5px}
.sp__pick:hover,.sp__pick:focus-visible{background:var(--color-bg-soft,rgba(127,127,127,.15));color:var(--color-accent,inherit);outline:none}
.sp__pick[aria-current=true]{color:var(--color-accent,inherit);font-weight:600}
.sp__node.is-miss{display:none}
"""

JS = """
(function(){
  var root=document.getElementById('scope-picker');
  var cur='',exact=false;
  function readHash(){var m=/(?:^|[#&])scope=([^&]*)/.exec(location.hash);return m?decodeURIComponent(m[1]):''}
  function writeHash(){
    var h=location.hash.replace(/^#/,'').split('&').filter(function(p){return p&&p.indexOf('scope=')!==0});
    if(cur)h.push('scope='+encodeURIComponent(cur)+(exact?'!':''));
    history.replaceState(null,'',location.pathname+location.search+(h.length?'#'+h.join('&'):''));
  }
  window.cvScope={
    get:function(){return cur},
    has:function(p){if(!cur||p===cur)return true;if(exact)return false;return cur==='.'||p.indexOf(cur+'/')===0},
    set:function(p,ex){cur=p||'';exact=!!ex;sync();writeHash();document.dispatchEvent(new CustomEvent('cv-scope',{detail:cur}))}
  };
  var h=readHash();if(h){exact=h.slice(-1)==='!';cur=exact?h.slice(0,-1):h}
  if(!root)return;
  var btn=root.querySelector('.sp__btn'),panel=root.querySelector('.sp__panel'),q=root.querySelector('.sp__q');
  function open(on){panel.hidden=!on;btn.setAttribute('aria-expanded',String(on));if(on){q.value='';filter('');q.focus()}}
  function expand(li,on){var k=li.querySelector(':scope>.sp__kids'),t=li.querySelector(':scope>.sp__tw');
    if(k){k.hidden=!on;t.setAttribute('aria-expanded',String(on))}}
  function sync(){
    var label='All repos';
    root.querySelectorAll('.sp__pick').forEach(function(b){
      var on=b.dataset.scope===cur&&(!!b.dataset.exact)===exact;b.setAttribute('aria-current',String(on));
      if(on&&cur)label=cur==='.'?b.firstChild.textContent.trim()+' (root)':cur;
    });
    root.querySelector('.sp__cur').textContent=label;root.querySelector('.sp__cur').title=label;
    var li=root.querySelector('.sp__node[data-path="'+(window.CSS&&CSS.escape?CSS.escape(cur):cur)+'"]');
    for(var p=li&&li.parentElement;p&&p!==root;p=p.parentElement)if(p.classList.contains('sp__node'))expand(p,true);
  }
  function filter(s){
    s=s.toLowerCase();
    root.querySelectorAll('.sp__tree .sp__node').forEach(function(li){
      var hit=!s||(li.dataset.path||'').toLowerCase().indexOf(s)>=0;li.classList.toggle('is-miss',!hit&&!li.querySelector('.sp__node[data-path*="'+s.replace(/"/g,'')+'"]'));
      if(s&&!li.classList.contains('is-miss'))expand(li,true);
    });
  }
  btn.addEventListener('click',function(){open(panel.hidden)});
  q.addEventListener('input',function(){filter(q.value.trim())});
  root.addEventListener('click',function(e){
    var t=e.target.closest('.sp__tw');if(t&&t.tagName==='BUTTON'){expand(t.parentElement,t.getAttribute('aria-expanded')!=='true');return}
    var b=e.target.closest('.sp__pick');if(b){window.cvScope.set(b.dataset.scope,!!b.dataset.exact);open(false)}
  });
  document.addEventListener('click',function(e){if(!panel.hidden&&!root.contains(e.target))open(false)});
  document.addEventListener('keydown',function(e){if(e.key==='Escape'&&!panel.hidden){open(false);btn.focus()}});
  sync();
})();
"""


def inject(page):
    """CSS in <head>; the picker's script runs before the page's own scripts read cvScope,
    so it goes right after the picker's markup is parsed: at the first page <script> in <body>."""
    page = page.replace("</head>", f"<style>{CSS}</style>\n</head>", 1)
    marker = '<div class="sp" id="scope-picker">'
    start = page.find(marker)
    if start < 0:
        return page
    end = _close_div(page, start)
    return page[:end] + f"<script>{JS}</script>" + page[end:]


def _close_div(page, start):
    """Index just past the </div> that closes the div opening at `start`."""
    depth, i = 0, start
    while True:
        o, c = page.find("<div", i), page.find("</div>", i)
        if o != -1 and o < c:
            depth, i = depth + 1, o + 4
        else:
            depth, i = depth - 1, c + 6
            if depth == 0:
                return i
