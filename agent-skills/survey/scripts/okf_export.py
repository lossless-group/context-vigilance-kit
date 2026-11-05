#!/usr/bin/env python3
"""Copy a scope's context-v/ bundles out as strict OKF v0.2, for tools and people outside.

The docs themselves never change: context-v keeps its own status values and wikilinks, and
this writes only to --out, which must be empty and outside any bundle's tracked folders.

  python3 okf_export.py [PATH] --out DIR [--scope repo|tree|lineage] [--include-private]

In the copies:

  status   Mapped to draft | stable | deprecated, with the original kept in context_v_status.
           A doc with no status, or one the survey can't place, exports as `draft`: OKF reads
           a missing status as `stable`, a claim nobody made about that doc.
  links    Wikilinks become markdown links: relative inside the bundle, a GitHub URL to
           another bundle. Relative, because OKF's own viewer skips `/`-rooted links though
           its spec allows them. Ambiguous and unwritten links become plain text, as do links
           to private docs. Frontmatter links stay as they are; OKF keeps unknown keys.

Left out and listed in okf-export.json: docs with no parseable frontmatter or no `type`
(they'd break conformance), and, unless --include-private, docs marked `private: true` or
`publish: false` and everything under client-sites/, collaborations/, client-stacks/ or clients/.
"""
import argparse
import collections
import json
import os
import re
import subprocess
import sys
from urllib.parse import quote

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import links as L  # noqa: E402
import scan  # noqa: E402

OKF_STATUS = {"open": "draft", "in_flight": "stable", "done": "stable", "reference": "stable",
              "parked": "deprecated", "closed": "deprecated", "unmapped": "draft", "none": "draft"}
RESERVED = {"index.md", "log.md"}
URL_SAFE = "/&+,=@'!~"  # readers match these paths literally, so encode only what would break a link


def okf_status(status, folder):
    return OKF_STATUS[scan.bucket_for(status, folder)[0]]


def is_private_path(path):
    return bool(scan.PRIVATE_SEGMENTS & set(path.split(os.sep)))


def is_private_doc(fm):
    return fm.get("publish") is False or fm.get("private") is True


def rewrite_status(yaml_text, status, folder):
    """Frontmatter with `status` mapped; the original value rides along in context_v_status."""
    lines, kept, skipping = yaml_text.split("\n"), [], False
    for line in lines:
        if skipping and line.startswith((" ", "\t")):
            continue  # the rest of a multi-line status
        skipping = False
        if re.match(r"^status:(\s|$)", line):
            skipping = True
            continue
        kept.append(line)
    kept.append(f"status: {okf_status(status, folder)}")
    if status:
        kept.append(f"context_v_status: {json.dumps(status, ensure_ascii=False)}")
    return "\n".join(kept)


def slug(heading):
    return re.sub(r"\s+", "-", re.sub(r"[^\w\s-]", "", heading.lower())).strip("-")


def display(link_text, path, heading):
    if link_text:
        return link_text
    if not path:
        return heading or ""
    name = os.path.basename(path)
    name = name[:-3] if name.endswith(".md") else name
    return name.replace("-", " ").replace("_", " ")


class Remotes:
    """GitHub URLs for files in other repos, one git lookup per repo."""

    def __init__(self):
        self.cache = {}

    def _git(self, repo, *args):
        done = subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True)
        return done.stdout.strip() if done.returncode == 0 else ""

    def base(self, repo):
        if repo not in self.cache:
            m = re.search(r"github\.com[:/](.+?)(?:\.git)?/?$", self._git(repo, "remote", "get-url", "origin"))
            head = self._git(repo, "symbolic-ref", "--short", "refs/remotes/origin/HEAD")
            branch = head.split("/", 1)[1] if "/" in head else "main"
            self.cache[repo] = f"https://github.com/{m.group(1)}/blob/{branch}" if m else None
        return self.cache[repo]

    def url(self, path, index):
        repo = scan.owner(path, index.repos) or index.anchor
        base = self.base(repo)
        return f"{base}/{quote(os.path.relpath(path, repo))}" if base else None


def render_link(m, source, cv, index, remotes, exported, include_private, counts):
    parsed = L.parse_match(m)
    if not parsed:
        return m.group(0)
    syntax, target, alias = parsed
    path, heading = L.split_heading(target)
    result = L.resolve(syntax, target, source, cv, index)
    text = display(alias, path, heading)
    anchor = f"#{slug(heading)}" if heading else ""

    def as_text(reason):
        counts[reason] += 1
        return text

    if result["state"] != L.RESOLVED:
        return as_text(f"text:{result['state']}")
    if result["method"] == "self":
        counts["self"] += 1
        return f"[{text}]({anchor})"
    landed = result["resolved"]
    if landed in exported:
        # A markdown link that already finds its file inside the bundle is fine as written.
        if syntax == "markdown" and result["method"] == "path":
            counts["kept"] += 1
            return m.group(0)
        counts["bundle"] += 1
        return f"[{text}]({quote(os.path.relpath(landed, os.path.dirname(source)), safe=URL_SAFE)}{anchor})"
    if landed.startswith(cv + os.sep) or (not include_private and is_private_target(landed)):
        return as_text("text:not-exported")
    url = remotes.url(landed, index)
    if not url:
        return as_text("text:no-remote")
    counts["url"] += 1
    return f"[{text}]({url}{anchor})"


def read_doc(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.read()


def is_private_target(path):
    """Checked on the file itself: the target may sit in a repo outside the export's scope."""
    if is_private_path(path):
        return True
    yaml_text, _, _ = scan.split_frontmatter(read_doc(path))
    return yaml_text is not None and is_private_doc(scan.parse_yaml(yaml_text)[0])


def plan_bundle(cv, include_private):
    """(paths to copy, {path: why it was left out}) for one bundle."""
    keep, left_out = [], {}
    for path in L.sources_in(cv):
        name = os.path.basename(path)
        if name in RESERVED:
            keep.append(path)
            continue
        yaml_text, _, _ = scan.split_frontmatter(read_doc(path))
        if yaml_text is None:
            left_out[path] = "no frontmatter"
            continue
        fm, error = scan.parse_yaml(yaml_text)
        if error:
            left_out[path] = "unparseable frontmatter"
        elif not fm.get("type"):
            left_out[path] = "no type"
        elif not include_private and is_private_doc(fm):
            left_out[path] = "private"
        else:
            keep.append(path)
    return keep, left_out


def export_doc(path, cv, index, remotes, exported, include_private, counts):
    text = read_doc(path)
    yaml_text, _, body_start = scan.split_frontmatter(text)
    lines = text.split("\n")
    name = os.path.basename(path)
    relative = os.path.relpath(path, cv)
    head, body = lines[:body_start], lines[body_start:]
    if name not in RESERVED:
        folder = relative.split(os.sep)[0] if os.sep in relative else ""
        fm, _ = scan.parse_yaml(yaml_text)
        status = scan.as_text(fm.get("status"))
        counts[f"status:{okf_status(status, folder)}"] += 1
        counts["status:no-value" if not status else "status:had-value"] += 1
        head = ["---", *rewrite_status(yaml_text, status, folder).split("\n"), "---"]
    elif relative == "index.md" and yaml_text is None:
        head = ["---", 'okf_version: "0.2"', "---", ""]
        counts["root-index-marked"] += 1
    body = list(L.map_lines(body, lambda _, m: render_link(m, path, cv, index, remotes, exported, include_private, counts)))
    return "\n".join(head + body)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("path", nargs="?", default=".")
    ap.add_argument("--out", required=True, help="an empty or new directory")
    ap.add_argument("--scope", choices=["repo", "tree", "lineage"], default="repo")
    ap.add_argument("--include-private", action="store_true",
                    help="also export private docs and client or collaborator bundles")
    ap.add_argument("--include-studies", action="store_true")
    args = ap.parse_args(argv)

    anchor, index, cvs = L.find_scope(args.path, args.scope, args.include_studies)
    out = os.path.realpath(args.out)
    for cv in index.cvs:
        inside = out == os.path.realpath(cv) or out.startswith(os.path.realpath(cv) + os.sep)
        if inside and not out.startswith(os.path.join(os.path.realpath(cv), "extra") + os.sep):
            sys.exit(f"error: {out} is inside {cv}; export outside it, or under its extra/")
    if os.path.isdir(out) and os.listdir(out):
        sys.exit(f"error: {out} isn't empty; nothing is overwritten, so pick a new directory")

    if not args.include_private:
        cvs = [cv for cv in cvs if not is_private_path(os.path.relpath(cv, anchor))]
    plans = {cv: plan_bundle(cv, args.include_private) for cv in cvs}

    counts, remotes, left_out = collections.Counter(), Remotes(), {}
    for cv, (keep, left) in plans.items():
        left_out.update({os.path.relpath(p, anchor): why for p, why in left.items()})
        exported = set(keep)
        for path in keep:
            dest = os.path.join(out, os.path.relpath(path, anchor))
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            with open(dest, "w", encoding="utf-8") as f:
                f.write(export_doc(path, cv, index, remotes, exported, args.include_private, counts))
            counts["files"] += 1

    report = {"bundles": len(plans), "counts": dict(sorted(counts.items())),
              "left_out_counts": dict(collections.Counter(left_out.values())), "left_out": left_out}
    with open(os.path.join(out, "okf-export.json"), "w", encoding="utf-8") as f:
        json.dump(report, f, indent=1)
    print(json.dumps({k: v for k, v in report.items() if k != "left_out"}, indent=1))


if __name__ == "__main__":
    main()
