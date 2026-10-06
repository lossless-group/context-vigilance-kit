---
# context-v/config.md: which tools fill which roles in this repo's workflows.
#
# Optional. With no config (or a role left out), everything stays in context-v/:
# issues go to context-v/issues/, nothing is posted anywhere.
# Skills and loop docs name ROLES (tracker, chat…); this file says which tool.
#
# Secrets NEVER go here. Name the environment variable (auth_env), list that name
# in .env.example, and keep the value in .env (gitignored).
#
# confirm: always | first-time | never. Anything outward-facing (posting, filing
# tickets) asks first unless you relax it here.
# via: mcp:<server> | cli:<tool> | api: how the agent reaches the tool.

type: Config                     # OKF requires a type on every .md; this is settings, not a doc
context_v_config: 1

# How docs link to each other. Agents write links this way; tools that read
# this file know how to resolve them.
links:
  style: wikilink                # wikilink | markdown (what new docs use)
  wikilink:
    # Preferred form (Obsidian): the file's path, then a pipe, then an alias:
    # the display text, usually the filename with - and _ turned into spaces.
    # Filenames stay space-free for filesystems, scrapers, and scripts;
    # readers see clean text.
    preferred: "[[specs/Payment-Retry-Policy.md|Payment Retry Policy]]"
    forms:                       # every form these docs may contain
      - "[[path/to/File-Name.md|Display Text]]"
      - "[[path/to/File-Name.md]]"
      - "[[File-Name|Display Text]]"
      - "[[File-Name]]"
      - "[[File-Name#Heading|Display Text]]"
    paths_from: context-v        # paths are relative to context-v/ (a leading "context-v/" is also accepted)
    resolve_by: path-then-filename   # try the path; if it doesn't match, find File-Name.md anywhere in context-v/
    unresolved: keep-as-text     # a link to a doc not written yet is fine
  markdown:
    form: relative               # relative ([x](../specs/x.md)) | bundle-root ([x](/specs/x.md))

integrations:
  tracker:
    provider: context-v          # context-v | github-issues | github-projects | plane | linear | jira
    # via: cli:gh
    # project: owner/repo
    # base_url_env: PLANE_BASE_URL
    # auth_env: PLANE_API_KEY
    issues: context-v            # context-v | tracker | both (both: the doc holds the reasoning, the ticket links to it)
    confirm: always
  chat:
    provider: none               # slack | teams | discord | buzz | none
    # via: mcp:slack
    # channel: "#dev"
    # post_on: [ship, release, blocked]
    confirm: always
  docs:
    provider: none               # notion | confluence | outline | google-docs | none
  design:
    provider: none               # design-md | figma | penpot | storybook | none
  code_host:
    provider: github             # github | gitlab | bitbucket
    # via: cli:gh
  deploy:
    provider: none               # vercel | netlify | railway | fly | none
  release:
    version_source: auto         # auto (find it) | package.json | pyproject.toml | tags
    notes_from: changelog
  memory:
    provider: none               # graphify | harness | graphiti | mem0 | letta | beads | none
    write: ask                   # may loop/reflect write lessons here? ask | allowed | never
  context:
    code_graph:
      provider: none             # graphify (recommended; see the kit README) | none
    retrieval:
      provider: none             # chroma | none
---

# Notes for agents

Anything the YAML can't say goes here. Examples:

- "Client work goes in the client's tracker project, not ours."
- "Never post to #general."
