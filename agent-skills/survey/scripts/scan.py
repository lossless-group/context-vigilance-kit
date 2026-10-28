#!/usr/bin/env python3
"""Scan every context-v/ folder in a scope and write survey.json.

Stage one of the survey (spec: context-v/specs/Survey-a-Scoped-Dashboard-of-Context-V.md).
Deterministic and read-only: no judgment here, the renderers and the agent add that.

  python3 scan.py [PATH] [--scope repo|tree|lineage] [--repos a,b] [--out DIR]
                  [--include-studies] [--stale-days N]

PATH defaults to the current directory; the scope root is the nearest repo at or above it.
A repo is any directory with a `.git` entry (a folder for a clone, a file for a submodule).
Standard library only; PyYAML is used when present, else a top-level key scan.
"""
import argparse
import datetime as dt
import fnmatch
import json
import os
import re
import subprocess
import sys

SKIP_DIRS = {
    "node_modules", "dist", ".git", ".astro", ".venv", "venv", "__pycache__", ".next",
    "build", ".chroma", "graphify-out", ".pnpm-store", ".turbo", ".cache", ".vercel",
}
RESERVED = {"readme.md", "index.md", "log.md", "config.md"}
TASK_FOLDERS = {"plans", "prompts", "handoffs", "specs", "issues", "loops"}
REFERENCE_FOLDERS = {"blueprints", "reminders", "habits", "contracts", "agent-skills", "sitemap"}

# First word of the status (lowercased, punctuation stripped) -> lifecycle bucket.
BUCKETS = {
    "open": ["draft", "proposed", "open", "in-review", "review", "jotted", "idea", "stub",
             "exploring", "planned", "todo", "new", "undecided", "pre-draft", "pending"],
    "in_flight": ["signed-off", "ready", "implementing", "in-progress", "progress", "wip",
                  "building", "doing", "started"],
    "done": ["shipped", "partially-shipped", "resolved", "decided", "complete", "completed",
             "done", "fixed", "closed", "published", "accepted", "merged", "implemented"],
    "parked": ["deferred", "stale", "blocked", "untested", "paused", "on-hold", "parked"],
    "closed": ["superseded", "archived", "abandoned", "deprecated", "obsolete", "rejected"],
    "reference": ["reference", "as-observed-from-filesystem", "proven-once", "living",
                  "canonical", "evergreen", "stable", "authoritative", "as-observed"],
}
STATUS_TO_BUCKET = {word: bucket for bucket, words in BUCKETS.items() for word in words}
OPEN_BUCKETS = ("open", "in_flight")

STUB_MAX_CONTENT_LINES = 100     # same cut as context-v-corpus/scripts/build-corpus-manifest.py
WORKED_ON_MIN_CONTENT_LINES = 500
EMPTY_MAX_PROSE_WORDS = 40       # a title, headings, a placeholder line: delete or complete
ACCEPTANCE = re.compile(r"^#{2,4}\s+.*(acceptance|success criteria|definition of done|done when|exit criteria)", re.I)
ASSIGNABLE = {"signed-off", "ready", "approved", "accepted"}
NEEDS_DECISION = {"in-review", "review", "proposed", "in-discussion"}

CHECKBOX = re.compile(r"^\s*[-*+]\s+\[( |x|X)\]\s+(.*)$")
H1 = re.compile(r"^#\s+(.+?)\s*#*\s*$")


# ── repos and scope ─────────────────────────────────────────────────────────

def is_repo(path):
    return os.path.exists(os.path.join(path, ".git"))


def nearest_repo(path):
    path = os.path.abspath(path)
    while True:
        if is_repo(path):
            return path
        parent = os.path.dirname(path)
        if parent == path:
            return None
        path = parent


def ancestors(repo):
    """Repos above `repo`, nearest first."""
    out, path = [], os.path.dirname(repo)
    while True:
        r = nearest_repo(path)
        if r is None:
            return out
        out.append(r)
        parent = os.path.dirname(r)
        if parent == r:
            return out
        path = parent


def load_ignore(root):
    path = os.path.join(root, ".surveyignore")
    if not os.path.isfile(path):
        return []
    with open(path, encoding="utf-8") as f:
        return [ln.strip().rstrip("/") for ln in f if ln.strip() and not ln.startswith("#")]


def ignored(rel, patterns):
    return any(fnmatch.fnmatch(rel, p) or rel.startswith(p + "/") for p in patterns)


def walk_tree(root, include_studies, patterns):
    """Yield (repo_path, context_v_path) for every context-v/ under root, plus the repo list."""
    repos, cvs = [], []
    for dirpath, dirnames, _ in os.walk(root):
        rel = os.path.relpath(dirpath, root)
        rel = "" if rel == "." else rel
        if is_repo(dirpath):
            in_studies = "studies" in rel.split(os.sep)
            if in_studies and not include_studies and dirpath != root:
                dirnames[:] = []
                continue
            repos.append(dirpath)
        keep = []
        for d in dirnames:
            child_rel = os.path.join(rel, d) if rel else d
            if d in SKIP_DIRS or ignored(child_rel, patterns):
                continue
            # The corpus's collated copies duplicate every doc in the tree.
            if d == "corpus" and os.path.exists(os.path.join(dirpath, "corpus-manifest.md")):
                continue
            # Splash roll-ups (`splash/src/rollup/context-v/...`) are copies of child docs.
            if d == "rollup":
                continue
            if d == "context-v":
                if "src" in child_rel.split(os.sep):
                    continue
                cvs.append(os.path.join(dirpath, d))
            keep.append(d)
        dirnames[:] = sorted(keep)
    return repos, cvs


def repo_only(repo):
    """context-v/ folders in `repo` without descending into child repos."""
    cvs = []
    for dirpath, dirnames, _ in os.walk(repo):
        keep = []
        for d in dirnames:
            full = os.path.join(dirpath, d)
            if d in SKIP_DIRS or d == "rollup" or is_repo(full):
                continue
            if d == "context-v":
                if "src" in os.path.relpath(full, repo).split(os.sep):
                    continue
                cvs.append(full)
            keep.append(d)
        dirnames[:] = sorted(keep)
    return cvs


def owner(path, repos):
    """The deepest repo containing `path`."""
    best = None
    for r in repos:
        if path == r or path.startswith(r + os.sep):
            if best is None or len(r) > len(best):
                best = r
    return best


# ── frontmatter ─────────────────────────────────────────────────────────────

def split_frontmatter(text):
    if not text.startswith("---"):
        return None, text, 0
    lines = text.split("\n")
    for i in range(1, len(lines)):
        if lines[i].rstrip() == "---":
            return "\n".join(lines[1:i]), "\n".join(lines[i + 1:]), i + 1
    return None, text, 0


def parse_yaml(yaml_text):
    try:
        import yaml  # type: ignore
    except ImportError:
        data = {}
        for line in yaml_text.split("\n"):
            m = re.match(r"^([A-Za-z0-9_\-]+):\s*(.*)$", line)
            if m:
                value = re.sub(r"\s+#.*$", "", m.group(2)).strip().strip("'\"")
                data[m.group(1)] = value or None
        return data, None
    try:
        data = yaml.safe_load(yaml_text)
    except Exception as e:  # noqa: BLE001 - any YAML error is a health flag, not a crash
        return {}, str(e).split("\n")[0]
    return (data if isinstance(data, dict) else {}), None


def as_date(value):
    if value is None or value == "":
        return None
    if isinstance(value, (dt.date, dt.datetime)):
        return value.isoformat()[:10]
    m = re.match(r"^(\d{4}-\d{2}-\d{2})", str(value).strip())
    return m.group(1) if m else None


def as_text(value):
    if value is None:
        return None
    if isinstance(value, list):
        return ", ".join(str(v) for v in value)
    text = str(value).strip()
    return text or None


def bucket_for(status, folder):
    """Bucket from the status's lead clause: the whole token (`partially-shipped`), else
    its first word (`open-deliberately-deferred` -> open). Unknowns stay unmapped, verbatim."""
    if not status:
        return "none", None, None
    lead = re.split(r"[·|,/;(]+", status.strip().lower())[0].strip(" .:!")
    lead = lead.replace("_", "-").replace(" ", "-")
    for word in (lead, "-".join(lead.split("-")[:2]), lead.split("-")[0]):
        if word == "active":
            return ("reference" if folder in REFERENCE_FOLDERS else "in_flight"), None, word
        if word in ("partially", "partial"):
            return "done", None, "partially-shipped"
        if word in STATUS_TO_BUCKET:
            return STATUS_TO_BUCKET[word], None, word
    return "unmapped", status, None


# ── git activity ────────────────────────────────────────────────────────────

AGENT_HINTS = ("anthropic.com", "claude", "codex", "copilot", "cursor", "openai.com", "gemini")


def person(trailer):
    """`Claude Opus 5.5 (1M context) <noreply@anthropic.com>` -> ("Claude Opus 5.5", True)."""
    name = re.sub(r"\s*<[^>]*>\s*$", "", trailer).strip()
    is_agent = any(h in trailer.lower() for h in AGENT_HINTS)
    if is_agent:
        name = re.sub(r"\s*\([^)]*\)", "", name).strip()
    return name, is_agent


def real_doc(fpath):
    """A context-v doc path, not a roll-up copy (`splash/src/rollup/context-v/...`)."""
    parts = fpath.split("/")
    return "context-v" in parts and "src" not in parts and "rollup" not in parts


def git_activity(repo, window_days, today):
    """One `git log` over the window: commit counts, who committed, agent co-authors, and
    the last-change / added date of every file touched. None when git isn't usable here."""
    since = (today - dt.timedelta(days=window_days)).isoformat()
    fmt = "%x1e%ad%x1f%an%x1f%(trailers:key=Co-Authored-By,valueonly,separator=%x1d)"
    try:
        log = subprocess.run(
            ["git", "-C", repo, "log", f"--since={since}", "--no-merges", "--date=short",
             "--name-status", f"--format={fmt}"],
            capture_output=True, text=True, timeout=30, check=True).stdout
        last = subprocess.run(["git", "-C", repo, "log", "-1", "--date=short", "--format=%ad"],
                              capture_output=True, text=True, timeout=10).stdout.strip() or None
        origin = subprocess.run(["git", "-C", repo, "remote", "get-url", "origin"],
                                capture_output=True, text=True, timeout=10).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return None

    d7, d30 = (today - dt.timedelta(days=7)).isoformat(), (today - dt.timedelta(days=30)).isoformat()
    # `git@github.com:owner/repo.git` or `https://github.com/owner/repo` -> owner
    m = re.search(r"[:/]([^/:]+)/[^/]+?(?:\.git)?$", origin)
    act = {"last_commit": last, "origin_owner": m.group(1) if m else None, "commits_7": 0, "commits_30": 0, f"commits_{window_days}": 0,
           "authors_30": {}, "agents_30": {}, "agent_assisted_30": 0, "cv_commits_30": 0,
           "docs_added_30": 0, "files": {}}
    for chunk in log.split("\x1e")[1:]:
        head, _, names = chunk.partition("\n")
        date, author, trailers = (head.split("\x1f") + ["", ""])[:3]
        act[f"commits_{window_days}"] += 1
        recent = date >= d30
        if date >= d7:
            act["commits_7"] += 1
        touched_cv = False
        for line in names.strip().split("\n"):
            cols = line.split("\t")
            if len(cols) < 2:
                continue
            code, fpath = cols[0], cols[-1]
            touched_cv = touched_cv or real_doc(fpath)
            f = act["files"].setdefault(fpath, {"last": date, "added": None})
            if code.startswith("A"):
                f["added"] = date
                if recent and real_doc(fpath) and fpath.endswith(".md"):
                    act["docs_added_30"] += 1
        if not recent:
            continue
        act["commits_30"] += 1
        act["authors_30"][author] = act["authors_30"].get(author, 0) + 1
        agents = [n for n, is_agent in (person(t) for t in trailers.split("\x1d") if t.strip()) if is_agent]
        for n in agents:
            act["agents_30"][n] = act["agents_30"].get(n, 0) + 1
        act["agent_assisted_30"] += 1 if agents else 0
        act["cv_commits_30"] += 1 if touched_cv else 0
    return act


# ── docs ────────────────────────────────────────────────────────────────────

def train_case(folder):
    return "-".join(w[:1].upper() + w[1:] for w in folder.split("-"))


def scan_doc(path, cv_dir, repo_rel, root, stale_cutoff):
    rel_in_cv = os.path.relpath(path, cv_dir)
    parts = rel_in_cv.split(os.sep)
    folder = parts[0] if len(parts) > 1 else "(root)"
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            text = f.read()
        st = os.stat(path)
    except OSError:
        return None

    yaml_text, body, body_offset = split_frontmatter(text)
    fm, yaml_error = parse_yaml(yaml_text) if yaml_text is not None else ({}, None)

    title = as_text(fm.get("title"))
    if not title:
        for line in body.split("\n"):
            m = H1.match(line)
            if m:
                title = m.group(1)
                break
    title_from_file = not title
    title = title or os.path.splitext(os.path.basename(path))[0].replace("-", " ")

    content_lines = len(body.split("\n")) if body else 0
    prose_words, headings, in_fence, has_acceptance = 0, 0, False, False
    for line in body.split("\n"):
        s = line.strip()
        if s.startswith("```") or s.startswith("~~~"):
            in_fence = not in_fence
            continue
        if in_fence or not s:
            continue
        if s.startswith("#"):
            headings += 1
            has_acceptance = has_acceptance or bool(ACCEPTANCE.match(s))
            continue
        prose_words += len(re.findall(r"[A-Za-z0-9][\w'’-]*", s))
    maturity = ("worked-on" if content_lines >= WORKED_ON_MIN_CONTENT_LINES
                else "idea-started" if content_lines >= STUB_MAX_CONTENT_LINES else "stub")

    status_raw = as_text(fm.get("status"))
    bucket, unmapped, status_key = bucket_for(status_raw, folder)

    mtime = dt.date.fromtimestamp(st.st_mtime).isoformat()
    updated = (as_date(fm.get("date_last_updated")) or as_date(fm.get("date_modified"))
               or as_date(fm.get("date_authored_current_draft")) or mtime)
    created = (as_date(fm.get("date_created")) or as_date(fm.get("date_authored_initial_draft"))
               or dt.date.fromtimestamp(getattr(st, "st_birthtime", st.st_mtime)).isoformat())

    tasks_open, tasks_done = [], 0
    if folder != "agent-skills":
        for i, line in enumerate(body.split("\n")):
            m = CHECKBOX.match(line)
            if not m:
                continue
            if m.group(1) == " ":
                if len(tasks_open) < 50:
                    tasks_open.append({"line": body_offset + i + 1, "text": m.group(2).strip()[:200]})
            else:
                tasks_done += 1

    flags = []
    if yaml_text is None:
        flags.append("no_frontmatter")
    if yaml_error:
        flags.append("yaml_error")
    if yaml_text is not None:
        declared = as_text(fm.get("type"))
        if not declared:
            flags.append("no_type")
        elif folder not in ("(root)", "agent-skills") and declared != train_case(folder):
            flags.append("type_mismatch")
        if not fm.get("lede") and not fm.get("description"):
            flags.append("no_lede")
        if "status" not in fm:
            flags.append("no_status")
    if unmapped:
        flags.append("unmapped_status")
    if bucket in OPEN_BUCKETS and updated < stale_cutoff:
        flags.append("stale")
    if folder != "agent-skills" and prose_words < EMPTY_MAX_PROSE_WORDS:
        flags.append("empty")
    if title_from_file:
        flags.append("no_title")
    # Status says open, but every checkbox is ticked: probably shipped and never closed.
    if bucket in OPEN_BUCKETS and tasks_done > 0 and not tasks_open:
        flags.append("maybe_done")

    rel_root = os.path.relpath(path, root)
    return {
        "id": as_text(fm.get("site_uuid")) or rel_root,
        "path": rel_root,
        "abs_path": path,
        "repo": repo_rel,
        "context_v": os.path.relpath(cv_dir, root),
        "folder": folder,
        "type": as_text(fm.get("type")),
        "title": title,
        "lede": as_text(fm.get("lede")) or as_text(fm.get("description")),
        "status": status_raw,
        "status_key": status_key,
        "bucket": bucket,
        "assignable": status_key in ASSIGNABLE,
        "needs_decision": status_key in NEEDS_DECISION,
        "partial": bool(status_raw and "partial" in status_raw.lower()),
        "publish": fm.get("publish") if isinstance(fm.get("publish"), bool) else None,
        "private": fm.get("private") is True,
        "tags": [str(t) for t in fm.get("tags", [])] if isinstance(fm.get("tags"), list) else [],
        "created": created,
        "updated": updated,
        "lines": text.count("\n") + 1,
        "content_lines": content_lines,
        "prose_words": prose_words,
        "headings": headings,
        "maturity": maturity,
        "has_acceptance": has_acceptance,
        "authors": [str(a) for a in fm["authors"]] if isinstance(fm.get("authors"), list)
        else ([str(fm["authors"])] if fm.get("authors") else []),
        "last_commit": None,      # filled from git, when the doc changed inside the window
        "added_in_window": None,
        "tasks_open": tasks_open,
        "tasks_open_count": sum(1 for ln in body.split("\n") if CHECKBOX.match(ln) and "[ ]" in ln)
        if folder != "agent-skills" else 0,
        "tasks_done": tasks_done,
        "task_folder": folder in TASK_FOLDERS,
        "flags": flags,
    }


def docs_in(cv_dir):
    for dirpath, dirnames, filenames in os.walk(cv_dir):
        rel = os.path.relpath(dirpath, cv_dir)
        top = rel.split(os.sep)[0]
        if top == "extra":
            dirnames[:] = []
            continue
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS and not is_repo(os.path.join(dirpath, d)))
        for name in sorted(filenames):
            if not name.endswith(".md"):
                continue
            if top == "agent-skills":
                if name != "SKILL.md":
                    continue
            elif name.lower() in RESERVED:
                continue
            yield os.path.join(dirpath, name)


# ── public mode ─────────────────────────────────────────────────────────────

# Path segments whose repos never appear in a published survey: client engagements and
# other people's code. Same boundary the roll-ups use (`rollup-sync.ts`, `collate.py`).
PRIVATE_SEGMENTS = {"client-sites", "collaborations"}


def publishable(repo_list, docs):
    """Drop what a public page must not show, and every absolute path."""
    def private_path(path):
        return bool(PRIVATE_SEGMENTS & set(path.split(os.sep)))

    docs = [d for d in docs if d["publish"] is not False and not d["private"] and not private_path(d["path"])]
    for d in docs:
        d["abs_path"] = d["path"]
    repos = [r for r in repo_list if not private_path(r["path"])]
    for r in repos:
        r["docs"] = sum(1 for d in docs if d["repo"] == r["path"])
    return repos, docs


# ── main ────────────────────────────────────────────────────────────────────

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("path", nargs="?", default=".")
    ap.add_argument("--scope", choices=["repo", "tree", "lineage"])
    ap.add_argument("--repos", help="comma-separated repo paths, each scanned as `repo`")
    ap.add_argument("--out", help="output dir (default: <root>/context-v/extra/survey)")
    ap.add_argument("--include-studies", action="store_true")
    ap.add_argument("--stale-days", type=int, default=90)
    ap.add_argument("--window", type=int, default=90, help="days of git history to read")
    ap.add_argument("--no-git", action="store_true", help="skip git activity")
    ap.add_argument("--public", action="store_true",
                    help="safe to publish: drop private docs and client/collaborator repos, relative paths only")
    args = ap.parse_args(argv)

    started = dt.datetime.now()
    root = nearest_repo(args.path) or os.path.abspath(args.path)
    patterns = load_ignore(root)

    if args.repos:
        scope = "pick"
        repos = [nearest_repo(os.path.abspath(p)) or os.path.abspath(p) for p in args.repos.split(",") if p.strip()]
        cvs = [cv for r in repos for cv in repo_only(r)]
    else:
        scope = args.scope
        if scope in (None, "tree"):
            repos, cvs = walk_tree(root, args.include_studies, patterns)
            scope = scope or ("tree" if len(repos) > 1 else "repo")
        if scope == "repo":
            repos, cvs = [root], repo_only(root)
        elif scope == "lineage":
            repos = [root] + ancestors(root)
            cvs = [cv for r in repos for cv in repo_only(r)]
            root = repos[-1]  # paths read from the top of the lineage

    stale_cutoff = (dt.date.today() - dt.timedelta(days=args.stale_days)).isoformat()
    seen, docs, cv_by_repo = set(), [], {}
    for cv in cvs:
        real = os.path.realpath(cv)
        if real in seen:
            continue
        seen.add(real)
        repo = owner(cv, repos) or root
        repo_rel = os.path.relpath(repo, root)
        repo_rel = "." if repo_rel == "." else repo_rel
        cv_by_repo.setdefault(repo, []).append(os.path.relpath(cv, root))
        for path in docs_in(cv):
            doc = scan_doc(path, cv, repo_rel, root, stale_cutoff)
            if doc:
                docs.append(doc)

    today = dt.date.today()
    activity = {}
    if not args.no_git:
        for r in sorted(set(repos) | set(cv_by_repo)):
            activity[r] = git_activity(r, args.window, today)
        by_abs = {d["abs_path"]: d for d in docs}
        for d in docs:
            r = next((x for x in sorted(activity, key=len, reverse=True)
                      if d["abs_path"].startswith(x + os.sep)), None)
            f = activity.get(r) and activity[r]["files"].get(os.path.relpath(d["abs_path"], r))
            if f:
                d["last_commit"], d["added_in_window"] = f["last"], f["added"]
        del by_abs

    repo_list = []
    for r in sorted(set(repos) | set(cv_by_repo)):
        rel = os.path.relpath(r, root)
        act = activity.get(r)
        if act:
            act = {k: v for k, v in act.items() if k != "files"}
        parent = owner(os.path.dirname(r), [x for x in repos if x != r]) if r != root else None
        repo_list.append({
            "path": rel,
            "name": os.path.basename(r),
            "parent": os.path.relpath(parent, root) if parent else None,
            "depth": 0 if rel == "." else rel.count(os.sep) + 1,
            "context_v": sorted(cv_by_repo.get(r, [])),
            "docs": sum(1 for d in docs if d["repo"] == rel),
            "activity": act,
        })

    if args.public:
        repo_list, docs = publishable(repo_list, docs)

    survey = {
        "generator": "context-vigilance-kit/survey scan.py 0.0.1",
        "generated_at": started.isoformat(timespec="seconds"),
        "scope": scope,
        "root": os.path.basename(root) if args.public else root,
        "public": args.public,
        "root_name": os.path.basename(root),
        "stale_days": args.stale_days,
        "window_days": None if args.no_git else args.window,
        "operator": None if args.no_git else (subprocess.run(
            ["git", "-C", root, "config", "user.name"], capture_output=True, text=True).stdout.strip() or None),
        "scan_seconds": round((dt.datetime.now() - started).total_seconds(), 2),
        "repos": repo_list,
        "docs": docs,
    }
    out = args.out or os.path.join(root, "context-v", "extra", "survey")
    os.makedirs(out, exist_ok=True)
    target = os.path.join(out, "survey.json")
    with open(target, "w", encoding="utf-8") as f:
        json.dump(survey, f, indent=1, ensure_ascii=False)
    print(f"survey: {scope} scope, {len(repo_list)} repos, {len(cvs)} context-v folders, "
          f"{len(docs)} docs in {survey['scan_seconds']}s -> {target}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
