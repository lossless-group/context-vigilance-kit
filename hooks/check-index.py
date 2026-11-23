#!/usr/bin/env python3
"""PostToolUse hook: after a context-v doc is written, check that the indexes list it.

Two rules, both exact:
  - the doc's folder has an `index.md` that links the doc (`* [Title](File.md) - …`)
  - every folder between the doc and `context-v/` is linked from its parent's
    `index.md`, ending at `context-v/index.md` (`* [Specs](specs/) - …`)

When something is missing it exits 2 with the exact lines to add on stderr, which
the agent sees right after its write, so it fixes the index in the same turn. The
hook never edits an index itself: the description line is the agent's to write.

Scope matches check-frontmatter.py: *.md under a `context-v/` folder, except
`extra/`, `agent-skills/`, and README/index/log/config files.

Audit mode, for CI, a pre-commit hook, or a subagent's sweep:
    python3 check-index.py --all path/to/context-v
prints every missing entry and exits 1 if there are any.

Anything unexpected lets the write through: this hook must never be the reason
work can't happen.
"""
import json
import os
import re
import sys
import urllib.parse

RESERVED = ("readme.md", "index.md", "log.md", "config.md")
SKIP_DIRS = ("extra", "agent-skills")


def context_root(path):
    """The `context-v` directory above `path`, or None."""
    parts = os.path.normpath(os.path.abspath(path)).split(os.sep)
    if "context-v" not in parts:
        return None
    i = len(parts) - 1 - parts[::-1].index("context-v")
    return os.sep.join(parts[: i + 1]) or os.sep


def in_scope(path):
    root = context_root(path)
    if not root or not path.endswith(".md"):
        return False
    rel = os.path.relpath(os.path.abspath(path), root).split(os.sep)
    if rel[0] in SKIP_DIRS or rel[0].startswith("."):
        return False
    return os.path.basename(path).lower() not in RESERVED


def frontmatter_field(text, *names):
    """First of `names` found as a one-line YAML scalar in the frontmatter."""
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    block = text[3:end] if end != -1 else ""
    for name in names:
        m = re.search(r"^" + re.escape(name) + r":\s*(.+)$", block, re.M)
        if m:
            value = m.group(1).strip()
            if value and value not in (">", ">-", "|", "|-"):
                return value.strip("'\"")
    return None


def links_to(index_text, target):
    """Does the index link `target` (a filename, or a folder name)?"""
    forms = {target, urllib.parse.quote(target), target.replace(" ", "%20")}
    for f in forms:
        for suffix in ("", "/", "/index.md"):
            if f"]({f}{suffix})" in index_text or f"](./{f}{suffix})" in index_text or f"](<{f}{suffix}>)" in index_text:
                return True
    return False


def read(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return fh.read()
    except OSError:
        return None


def train_case(name):
    return "-".join(w[:1].upper() + w[1:] for w in name.split("-"))


def missing_for(doc_path):
    """List of (index_path, line_to_add) for one doc."""
    root = context_root(doc_path)
    problems = []

    doc_dir = os.path.dirname(os.path.abspath(doc_path))
    doc_name = os.path.basename(doc_path)
    text = read(doc_path) or ""
    title = frontmatter_field(text, "title") or os.path.splitext(doc_name)[0]
    desc = frontmatter_field(text, "description", "lede") or "<one-line description>"
    index_path = os.path.join(doc_dir, "index.md")
    index_text = read(index_path)
    if index_text is None or not links_to(index_text, doc_name):
        problems.append((index_path, f"* [{title}]({urllib.parse.quote(doc_name)}) - {desc}", index_text is None))

    # Each folder up to context-v/ must be listed in its parent's index.
    d = doc_dir
    while os.path.abspath(d) != os.path.abspath(root):
        parent = os.path.dirname(d)
        name = os.path.basename(d)
        parent_index = os.path.join(parent, "index.md")
        parent_text = read(parent_index)
        if parent_text is None or not links_to(parent_text, name):
            label = train_case(name).replace("-", " ")
            problems.append((parent_index, f"* [{label}]({urllib.parse.quote(name)}/) - <what this folder holds>", parent_text is None))
        d = parent
    return problems


def report(problems, root):
    lines = ["context-v index out of date. Add these lines (keep each description to one plain sentence):"]
    for index_path, line, absent in problems:
        where = os.path.relpath(index_path, os.path.dirname(root))
        if not absent:
            note = ""
        elif os.path.dirname(index_path) == os.path.abspath(root):
            note = ' (create it, with frontmatter `okf_version: "0.2"`)'
        else:
            note = " (create it, with frontmatter `type` set to the folder name in Train-Case)"
        lines.append(f"  {where}{note}:\n    {line}")
    return "\n".join(lines)


def audit(root):
    root = os.path.abspath(root)
    problems = []
    for dirpath, dirnames, filenames in os.walk(root):
        rel = os.path.relpath(dirpath, root)
        top = rel.split(os.sep)[0]
        if top in SKIP_DIRS or (top.startswith(".") and top != "."):
            dirnames[:] = []
            continue
        for f in filenames:
            p = os.path.join(dirpath, f)
            if in_scope(p):
                problems.extend(missing_for(p))
    seen, unique = set(), []
    for p in problems:
        key = (p[0], p[1])
        if key not in seen:
            seen.add(key)
            unique.append(p)
    if unique:
        print(report(unique, root))
        return 1
    print("context-v indexes are complete.")
    return 0


def main():
    if len(sys.argv) >= 3 and sys.argv[1] == "--all":
        return audit(sys.argv[2])
    try:
        payload = json.load(sys.stdin)
        path = payload.get("tool_input", {}).get("file_path") or ""
        if not path:
            return 0
        if not os.path.isabs(path):
            path = os.path.join(payload.get("cwd") or os.getcwd(), path)
        if not in_scope(path) or not os.path.exists(path):
            return 0
        problems = missing_for(path)
        if problems:
            print(report(problems, context_root(path)), file=sys.stderr)
            return 2
        return 0
    except Exception:
        return 0


if __name__ == "__main__":
    sys.exit(main())
