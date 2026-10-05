#!/usr/bin/env python3
"""PreToolUse hook: check the frontmatter of context-v docs before they're written.

Blocks (exit 2, reason on stderr, which the agent sees) only on the exact basics:
  - the YAML between the opening `---` lines parses
  - `title` is present
  - `date_created` / `date_modified` are YYYY-MM-DD, and modified isn't earlier
  - `site_uuid` is a lowercase UUID v4; `hex_code` is 6 chars of [a-z0-9]
  - `site_uuid` / `hex_code` don't change on edit
New files need all five fields; existing files are checked only for fields present.
Non-snake_case keys produce a note on stderr (visible in verbose mode), never a block.
The hook never approves anything: permission prompts are untouched.

Scope: *.md under a `context-v/` folder, except `extra/`, `agent-skills/`, and README.md.
Anything unexpected (bad input, unreadable file) lets the write through: this hook
must never be the reason work can't happen.
"""
import json
import os
import re
import sys

UUID_V4 = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$")
HEX_CODE = re.compile(r"^[a-z0-9]{6}$")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SNAKE = re.compile(r"^[a-z0-9]+(_[a-z0-9]+)*$")
REQUIRED = ("title", "date_created", "date_modified", "site_uuid", "hex_code")

UUID_HELP = "generate it with `uuidgen | tr 'A-Z' 'a-z'` (never type one)"
HEX_HELP = "generate it with `LC_ALL=C tr -dc 'a-z0-9' </dev/urandom | head -c6`"


def in_scope(path):
    parts = os.path.normpath(path).split(os.sep)
    if not path.endswith(".md") or "context-v" not in parts:
        return False
    after = parts[len(parts) - 1 - parts[::-1].index("context-v") + 1:]
    if not after or after[0] in ("extra", "agent-skills"):
        return False
    return os.path.basename(path).lower() != "readme.md"


def split_frontmatter(text):
    """Return the YAML text between the first two `---` lines, or None."""
    if not text.startswith("---"):
        return None
    lines = text.split("\n")
    for i in range(1, len(lines)):
        if lines[i].rstrip() == "---":
            return "\n".join(lines[1:i])
    return None


def parse(yaml_text):
    """Return (dict, error). Uses PyYAML when available, else a top-level key scan."""
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
    except yaml.YAMLError as exc:
        return None, str(exc).replace("\n", " ")
    if data is None:
        return {}, None
    if not isinstance(data, dict):
        return None, "frontmatter is not a set of `key: value` pairs"
    return data, None


def as_text(value):
    return None if value is None else str(value).strip()


def resulting_content(tool, tool_input, old_text):
    if tool == "Write":
        return tool_input.get("content")
    if old_text is None:
        return None
    edits = tool_input.get("edits") if tool == "MultiEdit" else [tool_input]
    text = old_text
    for e in edits or []:
        old, new = e.get("old_string", ""), e.get("new_string", "")
        if not old or old not in text:
            return None  # the edit itself will fail; nothing for us to judge
        text = text.replace(old, new) if e.get("replace_all") else text.replace(old, new, 1)
    return text


def check(path, new_text, old_text):
    problems, notes = [], []
    is_new = old_text is None
    fm = split_frontmatter(new_text)
    if fm is None:
        if is_new:
            problems.append("new context-v docs need YAML frontmatter between `---` lines (start from a template)")
        return problems, notes
    data, err = parse(fm)
    if err:
        return [f"frontmatter YAML doesn't parse: {err}. (Common cause: an unquoted `: ` inside a value; wrap it in quotes.)"], notes

    old_data = {}
    if old_text is not None:
        old_fm = split_frontmatter(old_text)
        if old_fm is not None:
            old_data = parse(old_fm)[0] or {}

    for key in REQUIRED:
        if key not in data or as_text(data.get(key)) in (None, ""):
            if is_new:
                problems.append(f"`{key}` is missing")

    created, modified = as_text(data.get("date_created")), as_text(data.get("date_modified"))
    for key, val in (("date_created", created), ("date_modified", modified)):
        if val and not DATE.match(val):
            problems.append(f"`{key}` is `{val}`; it must be YYYY-MM-DD")
    if created and modified and DATE.match(created) and DATE.match(modified) and modified < created:
        problems.append(f"`date_modified` ({modified}) is earlier than `date_created` ({created})")

    uid = as_text(data.get("site_uuid"))
    if uid and not UUID_V4.match(uid):
        problems.append(f"`site_uuid` `{uid}` isn't a lowercase UUID v4; {UUID_HELP}")
    hx = as_text(data.get("hex_code"))
    if hx and not HEX_CODE.match(hx):
        problems.append(f"`hex_code` `{hx}` isn't 6 characters of a-z/0-9; {HEX_HELP}")

    for key in ("site_uuid", "hex_code"):
        before, after = as_text(old_data.get(key)), as_text(data.get(key))
        if before and after != before:
            problems.append(f"`{key}` changed from `{before}` to `{after}`; it's minted once and never changes. Restore it.")

    odd = [k for k in data if isinstance(k, str) and not SNAKE.match(k)]
    if odd:
        notes.append("non-snake_case frontmatter keys: " + ", ".join(odd))
    return problems, notes


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0
    tool = payload.get("tool_name", "")
    tool_input = payload.get("tool_input") or {}
    path = tool_input.get("file_path") or ""
    if tool not in ("Write", "Edit", "MultiEdit") or not path or not in_scope(path):
        return 0
    old_text = None
    if os.path.exists(path):
        try:
            with open(path, encoding="utf-8") as fh:
                old_text = fh.read()
        except Exception:
            return 0
    new_text = resulting_content(tool, tool_input, old_text)
    if new_text is None:
        return 0
    problems, notes = check(path, new_text, old_text)
    if problems:
        rel = os.path.relpath(path)
        sys.stderr.write(
            f"context-v frontmatter check blocked this write to {rel}:\n"
            + "\n".join(f"  - {p}" for p in problems)
            + "\nFix these and write again. (Only these basics are checked; everything else is judgment.)\n"
        )
        return 2
    if notes:
        # A note, not a decision: never answer the permission question for the user.
        sys.stderr.write("context-v note: " + "; ".join(notes) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
