"""A "copy path" button beside every doc, shared by the survey renderers.

Copies the doc's absolute path, so it can be pasted straight to an agent ("work on <path>")
from any working directory. One delegated click handler; buttons carry the path in
`data-path`. Uses the Clipboard API, falling back to a hidden textarea where it's blocked.
"""
import html

CSS = """
.cp{display:inline-flex;align-items:center;justify-content:center;vertical-align:middle;
  margin-left:.4em;padding:.1em .45em;min-height:1.6em;border:1px solid var(--color-border-strong,currentColor);
  border-radius:3px;background:transparent;color:var(--color-text-dim,inherit);
  font:500 .68rem/1 var(--font__mono,ui-monospace,monospace);letter-spacing:.04em;cursor:pointer;
  text-transform:lowercase;white-space:nowrap}
.cp:hover,.cp:focus-visible{color:var(--color-accent,inherit);border-color:var(--color-accent,currentColor);outline:none}
.cp.is-copied{color:var(--color-thread,inherit);border-color:var(--color-thread,currentColor)}
"""

JS = """
(function(){
  function fallback(text){
    var t=document.createElement('textarea');t.value=text;t.setAttribute('readonly','');
    t.style.position='fixed';t.style.opacity='0';document.body.appendChild(t);t.select();
    try{document.execCommand('copy')}catch(e){}document.body.removeChild(t);
  }
  document.addEventListener('click',function(ev){
    var b=ev.target.closest&&ev.target.closest('.cp');if(!b)return;
    ev.preventDefault();ev.stopPropagation();
    var p=b.getAttribute('data-path'),done=function(){
      b.classList.add('is-copied');b.textContent='copied';
      setTimeout(function(){b.classList.remove('is-copied');b.textContent='copy path'},1200)};
    if(navigator.clipboard&&navigator.clipboard.writeText){
      navigator.clipboard.writeText(p).then(done,function(){fallback(p);done()});
    }else{fallback(p);done()}
  },true);
})();
"""

# For renderers that build rows in JS: `cpBtn(path)` returns the button's markup.
JS_HELPER = ("function cpBtn(p){return '<button type=\"button\" class=\"cp\" data-path=\"'+"
             "String(p).replace(/&/g,'&amp;').replace(/\"/g,'&quot;').replace(/</g,'&lt;')+"
             "'\" title=\"Copy '+String(p).replace(/\"/g,'&quot;')+'\" aria-label=\"Copy path\">copy path</button>'}")


def button(path):
    """The button's markup, for renderers that build rows in Python."""
    p = html.escape(path, quote=True)
    return f'<button type="button" class="cp" data-path="{p}" title="Copy {p}" aria-label="Copy path">copy path</button>'


def inject(page):
    """CSS and `cpBtn` go in <head>, so inline scripts that render rows during parse can call
    it; the click handler goes before </body>."""
    page = page.replace("</head>", f"<style>{CSS}</style>\n<script>{JS_HELPER}</script>\n</head>", 1)
    return page.replace("</body>", f"<script>{JS}</script>\n</body>", 1)
