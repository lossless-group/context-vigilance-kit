#!/usr/bin/env python3
"""Resolve every link in a scope's context-v/ docs to the file it points at.

Read-only on the docs: writes links.json and LINKS.md to --out, nothing else. Reads every
form `context-v/config.md` allows, plus markdown links, so nothing downstream has to.

  python3 links.py [PATH] [--scope repo|tree|lineage] [--out DIR] [--include-studies]

Order, per `resolve_by: path-then-filename` in the config:

  1. The path, if the link has one. Wikilinks read from context-v/ (a leading `context-v/`
     is accepted), then the doc's folder, repo root, and tree root. Markdown links read
     from the doc's folder, or context-v/ when they start with `/`.
  2. A unique filename: in the doc's bundle, then its repo, then the whole tree.
  3. Otherwise the link is `ambiguous` (several matches, never guessed at) or `unwritten`
     (no match, which the config allows: `unresolved: keep-as-text`).

Targets always come from the whole tree, whatever the scope, so narrowing the scope changes
which docs get checked and not what their links resolve to. Skills resolve by folder name
and changelog entries by filename. Standard library only.
"""
import argparse
import collections
import json
import os
import re
import sys
from urllib.parse import unquote

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import scan  # noqa: E402

# Inline code comes first, so a link shown as `[[an example]]` is passed over, not resolved.
LINK = re.compile(
    r"(?P<code>`[^`\n]*`)"
    r"|(?P<wembed>!?)\[\[(?P<wiki>[^\[\]\n]+?)\]\]"
    r"|(?P<membed>!?)\[(?P<text>[^\]\n]*)\]\((?P<href>[^)\s]+)(?:\s+\"[^\"\n]*\")?\)"
)
FENCE = re.compile(r"^\s*(```|~~~)")
SCHEME = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.\-]*:")
RESOLVED = "resolved"
AMBIGUOUS = "ambiguous"
UNWRITTEN = "unwritten"


# ── parsing ─────────────────────────────────────────────────────────────────

def parse_match(m):
    """(syntax, target, alias) for a link match, or None for code, embeds, and web links."""
    if m.group("code") or m.group("wembed") or m.group("membed"):
        return None
    if m.group("wiki") is not None:
        target, _, alias = m.group("wiki").replace("\\|", "|").partition("|")
        return "wikilink", target.strip(), alias.strip() or None
    href = m.group("href")
    if SCHEME.match(href) or href.startswith("#") or not href.split("#")[0].endswith(".md"):
        return None
    return "markdown", unquote(href), m.group("text").strip() or None


def split_heading(target):
    path, _, heading = target.partition("#")
    return path.strip(), heading.strip() or None


def form_of(syntax, path, alias):
    """The link's shape, for the report: `[[path.md|alias]]` -> `path+.md+alias`."""
    if syntax == "markdown":
        return "markdown"
    shape = "path" if "/" in path else "bare" if path else "heading"
    return shape + ("+.md" if path.endswith(".md") else "") + ("+alias" if alias else "")


def map_lines(lines, fn):
    """Apply fn(line_number, match) to each link outside code; yields the rewritten lines."""
    in_fence = False
    for number, line in enumerate(lines, 1):
        if FENCE.match(line):
            in_fence = not in_fence
        if in_fence or FENCE.match(line):
            yield line
        else:
            yield LINK.sub(lambda m: fn(number, m), line)


# ── the tree ────────────────────────────────────────────────────────────────

class Index:
    """Every file a link can land on, by lowercase name. Obsidian matches names the same way."""

    def __init__(self, anchor, cvs, repos):
        self.anchor, self.cvs, self.repos = anchor, cvs, repos
        self.by_name = collections.defaultdict(set)
        for cv in cvs:
            self._add_tree(cv, skip_top={"extra"})
            changelog = os.path.join(scan.owner(cv, repos) or anchor, "changelog")
            if os.path.isdir(changelog):
                self._add_tree(changelog)

    def _add_tree(self, top, skip_top=()):
        for dirpath, dirnames, filenames in os.walk(top):
            at_top = dirpath == top
            dirnames[:] = [d for d in dirnames if d not in scan.SKIP_DIRS and not (at_top and d in skip_top)]
            for name in filenames:
                if not name.endswith(".md"):
                    continue
                full = os.path.join(dirpath, name)
                self.by_name[name[:-3].lower()].add(full)
                if name == "SKILL.md":
                    self.by_name[os.path.basename(dirpath).lower()].add(full)

    def bundle_of(self, path):
        best = None
        for cv in self.cvs:
            if path.startswith(cv + os.sep) and (best is None or len(cv) > len(best)):
                best = cv
        return best


def anchor_of(path):
    """The top repo above `path`: the tree a link can land anywhere in."""
    root = scan.nearest_repo(path) or os.path.abspath(path)
    above = scan.ancestors(root)
    return above[-1] if above else root


def find_scope(path, scope, include_studies):
    """(anchor, index, the context-v/ folders whose docs get checked)."""
    root = scan.nearest_repo(path) or os.path.abspath(path)
    anchor = anchor_of(path)
    repos, cvs = scan.walk_tree(anchor, include_studies, scan.load_ignore(anchor))
    index = Index(anchor, cvs, repos)
    if scope == "repo":
        return anchor, index, scan.repo_only(root)
    if scope == "lineage":
        return anchor, index, [cv for r in [root] + scan.ancestors(root) for cv in scan.repo_only(r)]
    if root == anchor:
        return anchor, index, cvs
    return anchor, index, [cv for cv in cvs if cv.startswith(root + os.sep)]


def sources_in(cv):
    """Docs whose links get checked: the bundle's docs and its index and log files."""
    docs = [p for p in scan.docs_in(cv) if not p.startswith(os.path.join(cv, "agent-skills") + os.sep)]
    for dirpath, dirnames, filenames in os.walk(cv):
        rel = os.path.relpath(dirpath, cv).split(os.sep)[0]
        if rel in ("extra", "agent-skills"):
            dirnames[:] = []
            continue
        dirnames[:] = [d for d in dirnames if d not in scan.SKIP_DIRS]
        docs += [os.path.join(dirpath, n) for n in filenames if n in ("index.md", "log.md")]
    return sorted(set(docs))


# ── resolving ───────────────────────────────────────────────────────────────

def path_candidates(syntax, path, source, cv, repo, anchor):
    with_ext = path if path.endswith(".md") else path + ".md"
    doc_dir = os.path.dirname(source)
    if syntax == "markdown":
        return [os.path.join(cv, with_ext.lstrip("/"))] if path.startswith("/") else [os.path.join(doc_dir, with_ext)]
    if os.path.isabs(path):
        return [with_ext]
    if path.startswith("."):
        return [os.path.join(doc_dir, with_ext)]
    from_cv = with_ext[len("context-v/"):] if with_ext.startswith("context-v/") else with_ext
    return [os.path.join(cv, from_cv), os.path.join(doc_dir, with_ext), os.path.join(repo, with_ext),
            os.path.join(anchor, with_ext)]


def by_filename(path, cv, repo, index):
    """(method, matches) from the narrowest scope with any match."""
    name = os.path.basename(path)
    name = name[:-3] if name.endswith(".md") else name
    matches = index.by_name.get(name.lower(), set())
    in_bundle = sorted(p for p in matches if p.startswith(cv + os.sep))
    if in_bundle:
        return "filename-bundle", in_bundle
    # By owner, not by prefix: every child repo sits under its parent's path.
    in_repo = sorted(p for p in matches if scan.owner(p, index.repos) == repo)
    if in_repo:
        return "filename-repo", in_repo
    return "filename-tree", sorted(matches)


def resolve(syntax, target, source, cv, index):
    """Where one link lands: {state, method, resolved, candidates, stale_path, cross_bundle}."""
    path, heading = split_heading(target)
    out = {"heading": heading, "resolved": None, "method": None, "candidates": [],
           "stale_path": False, "cross_bundle": False}
    if not path:
        return {**out, "state": RESOLVED, "method": "self", "resolved": source}
    repo = scan.owner(source, index.repos) or index.anchor
    if syntax == "markdown" or "/" in path:
        for candidate in path_candidates(syntax, path, source, cv, repo, index.anchor):
            candidate = os.path.normpath(candidate)
            if os.path.isfile(candidate):
                return {**out, "state": RESOLVED, "method": "path", "resolved": candidate,
                        "cross_bundle": not candidate.startswith(cv + os.sep)}
        out["stale_path"] = True
    method, matches = by_filename(path, cv, repo, index)
    if len(matches) == 1:
        return {**out, "state": RESOLVED, "method": method, "resolved": matches[0],
                "cross_bundle": not matches[0].startswith(cv + os.sep)}
    if matches:
        return {**out, "state": AMBIGUOUS, "candidates": matches}
    # A bare name can still mean a root file such as DESIGN.md or AGENTS.md.
    at_root = os.path.join(repo, path if path.endswith(".md") else path + ".md")
    if "/" not in path and os.path.isfile(at_root):
        return {**out, "state": RESOLVED, "method": "repo-root", "resolved": at_root, "cross_bundle": True}
    return {**out, "state": UNWRITTEN}


def links_in(source, cv, index):
    """Every link in one doc, resolved."""
    with open(source, encoding="utf-8", errors="replace") as f:
        lines = f.read().split("\n")
    _, _, body_start = scan.split_frontmatter("\n".join(lines))
    found = []

    def record(number, m):
        parsed = parse_match(m)
        if parsed:
            syntax, target, alias = parsed
            path, _ = split_heading(target)
            found.append({"line": number, "raw": m.group(0), "syntax": syntax, "target": target, "alias": alias,
                          "form": form_of(syntax, path, alias), "where": "frontmatter" if number <= body_start else "body",
                          **resolve(syntax, target, source, cv, index)})
        return m.group(0)

    # Frontmatter first and on its own: a stray fence in the body must not hide it.
    for _ in map_lines(lines[:body_start], record):
        pass
    in_body = map_lines(lines[body_start:], lambda n, m: record(n + body_start, m))
    for _ in in_body:
        pass
    return found


def rel(path, anchor):
    return os.path.relpath(path, anchor) if path else None


# ── output ──────────────────────────────────────────────────────────────────

def summarize(links):
    return {
        "links": len(links),
        "by_state": dict(collections.Counter(l["state"] for l in links).most_common()),
        "by_method": dict(collections.Counter(l["method"] for l in links if l["method"]).most_common()),
        "by_form": dict(collections.Counter(l["form"] for l in links).most_common()),
        "stale_paths": sum(1 for l in links if l["stale_path"] and l["state"] == RESOLVED),
        "cross_bundle": sum(1 for l in links if l["cross_bundle"]),
    }


def count_table(title, counts):
    return [f"## {title}", "", "| | Links |", "|---|---:|"] + [f"| {k} | {v} |" for k, v in counts.items()] + [""]


def link_list(title, note, links, limit=200):
    if not links:
        return []
    out = [f"## {title} ({len(links)})", "", note, ""]
    for l in links[:limit]:
        where = f"`{l['source']}:{l['line']}`"
        extra = f" → `{l['resolved']}`" if l["resolved"] else ""
        extra += "".join(f"\n  - `{c}`" for c in l["candidates"])
        out.append(f"- {where} `{l['raw']}`{extra}")
    if len(links) > limit:
        out.append(f"- …{len(links) - limit} more in links.json")
    return out + [""]


def render(links, summary):
    out = ["# Links", "", f"{summary['links']} links. Only the links below need a person; the rest resolve.", ""]
    out += count_table("By state", summary["by_state"])
    out += count_table("By form", summary["by_form"])
    out += count_table("How they resolved", summary["by_method"])
    out += link_list("Ambiguous", "Several files match. Add a path to the link to say which.",
                     [l for l in links if l["state"] == AMBIGUOUS])
    out += link_list("Stale paths", "The path no longer exists, but the filename still finds the doc. Usually a moved file.",
                     [l for l in links if l["stale_path"] and l["state"] == RESOLVED])
    out += link_list("Unwritten", "No file matches. Fine for a doc not written yet (`unresolved: keep-as-text`); otherwise a typo or a deleted doc.",
                     [l for l in links if l["state"] == UNWRITTEN])
    return "\n".join(out)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("path", nargs="?", default=".")
    ap.add_argument("--scope", choices=["repo", "tree", "lineage"], default="tree")
    ap.add_argument("--out", help="output dir (default: <repo>/context-v/extra/links)")
    ap.add_argument("--include-studies", action="store_true")
    args = ap.parse_args(argv)

    anchor, index, cvs = find_scope(args.path, args.scope, args.include_studies)
    links = []
    for cv in cvs:
        for source in sources_in(cv):
            for link in links_in(source, cv, index):
                links.append({**link, "source": rel(source, anchor), "resolved": rel(link["resolved"], anchor),
                              "candidates": [rel(c, anchor) for c in link["candidates"]]})
    summary = summarize(links)

    root = scan.nearest_repo(args.path) or os.path.abspath(args.path)
    out_dir = args.out or os.path.join(root, "context-v", "extra", "links")
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "links.json"), "w", encoding="utf-8") as f:
        json.dump({"anchor": anchor, "summary": summary, "links": links}, f, indent=1)
    with open(os.path.join(out_dir, "LINKS.md"), "w", encoding="utf-8") as f:
        f.write(render(links, summary))
    print(json.dumps(summary, indent=1))
    print(f"wrote {out_dir}", file=sys.stderr)


if __name__ == "__main__":
    main()
