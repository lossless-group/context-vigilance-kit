---
title: Context Vigilance Kit — Skills Manifest
description: Inventory of agent skills (Anthropic agent-skills spec) discovered under
  any context-v/skills/ directory in the curated sources. Tracked separately from
  the corpus manifest.
date_generated: '2026-05-07'
schema_version: 1
summary:
  total_skills: 12
  with_skill_md: 11
  without_skill_md: 1
  by_repo:
    lossless-monorepo: 12
  by_completeness:
    complete: 9
    skill-md-only: 2
    missing-required-fields: 0
    no-skill-md: 1
skills:
- name: astro-knots
  source_repo_slug: lossless-monorepo
  skill_dir_path: /Users/mpstaton/code/lossless-monorepo/context-v/skills/astro-knots
  path_from_monorepo_root: context-v/skills/astro-knots
  has_skill_md: true
  skill_md_frontmatter:
    name: astro-knots
    description: The Lossless Group's Astro Knots conventions — vision, tech hierarchy,
      approved frameworks, and hard prohibitions for the family of ~10+ Astro sites
      and the Lossless Flavored Markdown ecosystem. Use whenever working on an Astro
      project in the lossless-monorepo (or any sibling repo), scaffolding new sites,
      choosing dependencies, building components, integrating LFM, or when the user
      mentions "Astro Knots", "LFM", "Lossless Flavored Markdown", or "pseudomonorepo".
      Hard prohibitions on React, JSX, Angular, and unnecessary dependencies.
  skill_md_body_lines: 133
  missing_required_fields: []
  asset_counts:
    references_md: 7
    templates_files: 0
    scripts_files: 0
    total_md: 8
  completeness: complete
- name: changelog
  source_repo_slug: lossless-monorepo
  skill_dir_path: /Users/mpstaton/code/lossless-monorepo/context-v/skills/changelog
  path_from_monorepo_root: context-v/skills/changelog
  has_skill_md: false
  skill_md_frontmatter: {}
  skill_md_body_lines: 0
  missing_required_fields:
  - name
  - description
  asset_counts:
    references_md: 0
    templates_files: 0
    scripts_files: 0
    total_md: 2
  completeness: no-skill-md
- name: changelog-conventions
  source_repo_slug: lossless-monorepo
  skill_dir_path: /Users/mpstaton/code/lossless-monorepo/context-v/skills/changelog-conventions
  path_from_monorepo_root: context-v/skills/changelog-conventions
  has_skill_md: true
  skill_md_frontmatter:
    name: changelog-conventions
    description: How The Lossless Group writes and structures changelog/ entries across
      all repos (projects, true monorepos, pseudomonorepos). Use whenever shipping
      or pushing a coherent chunk of work, when scaffolding a new repo's changelog/
      directory, when authoring a product release message, when the user says "log
      this", "write a changelog", or "ship note", or when reviewing a changelog/ file.
      Encodes the strict frontmatter (publish, lede, ISO dates), filename pattern,
      "it exists" priority, and the show-don't-enforce ethos.
  skill_md_body_lines: 204
  missing_required_fields: []
  asset_counts:
    references_md: 5
    templates_files: 2
    scripts_files: 0
    total_md: 8
  completeness: complete
- name: context-vigilance
  source_repo_slug: lossless-monorepo
  skill_dir_path: /Users/mpstaton/code/lossless-monorepo/context-v/skills/context-vigilance
  path_from_monorepo_root: context-v/skills/context-vigilance
  has_skill_md: true
  skill_md_frontmatter:
    name: context-vigilance
    description: Lossless Group's framework for managing context-v/ directories in
      any project. Use whenever creating, updating, or organizing files in any context-v/
      folder (specs, prompts, blueprints, reminders, explorations, issues), or when
      the user asks about context engineering, AI co-development workflow, or the
      "context-v" convention. Enforces directory roles, the four-part epoch.major.minor.patch
      versioning, YAML frontmatter standard, wikilink cross-references, and the prep/reflective/journey
      cognitive modes.
  skill_md_body_lines: 161
  missing_required_fields: []
  asset_counts:
    references_md: 5
    templates_files: 6
    scripts_files: 0
    total_md: 12
  completeness: complete
- name: deck-iteration-workflow
  source_repo_slug: lossless-monorepo
  skill_dir_path: /Users/mpstaton/code/lossless-monorepo/context-v/skills/deck-iteration-workflow
  path_from_monorepo_root: context-v/skills/deck-iteration-workflow
  has_skill_md: true
  skill_md_frontmatter:
    name: deck-iteration-workflow
    description: The Lossless Group's workflow for developing slides-only Astro sites
      for fundraise processes, aligned with the calmstorm-decks project patterns and
      the iterative approach from the "Develop a Slides-only Astro Site for a Fundraise
      Process" specification. Use when creating or modifying slide decks, managing
      slide variants, or implementing the structured iteration workflow for fundraise
      material development.
  skill_md_body_lines: 193
  missing_required_fields: []
  asset_counts:
    references_md: 1
    templates_files: 2
    scripts_files: 0
    total_md: 4
  completeness: complete
- name: git-conventions
  source_repo_slug: lossless-monorepo
  skill_dir_path: /Users/mpstaton/code/lossless-monorepo/context-v/skills/git-conventions
  path_from_monorepo_root: context-v/skills/git-conventions
  has_skill_md: true
  skill_md_frontmatter:
    name: git-conventions
    description: The Lossless Group's git commit message conventions — structured
      headers with action verbs and effort groupings, paragraph-spaced bodies that
      explain impact before implementation, and "Also included" riders for minor changes.
      Use when writing commit messages, reviewing commits, or when the user mentions
      "commit message format", "git conventions", or asks how to structure a commit.
  skill_md_body_lines: 264
  missing_required_fields: []
  asset_counts:
    references_md: 3
    templates_files: 0
    scripts_files: 0
    total_md: 4
  completeness: complete
- name: lossless-flavored-markdown
  source_repo_slug: lossless-monorepo
  skill_dir_path: /Users/mpstaton/code/lossless-monorepo/context-v/skills/lossless-flavored-markdown
  path_from_monorepo_root: context-v/skills/lossless-flavored-markdown
  has_skill_md: true
  skill_md_frontmatter:
    name: lossless-flavored-markdown
    description: The Lossless Group's extended-markdown flavor — what LFM is, when
      to use it, how its directives normalize across syntaxes (CommonMark, GFM, Obsidian
      callouts, remark-directive, Markdoc), how citations and link previews work,
      and how sites extend it via trigger maps and theme tokens. Use whenever authoring
      or rendering content in any Astro Knots site, integrating the @lossless-group/lfm
      package, building or registering custom components for markdown, debugging callouts/embeds/citations,
      or when the user mentions "LFM", "Lossless Flavored Markdown", "extended markdown",
      "directive syntax", "wikilink", "trigger map", "callout", or "hex-code citation".
  skill_md_body_lines: 153
  missing_required_fields: []
  asset_counts:
    references_md: 5
    templates_files: 0
    scripts_files: 0
    total_md: 6
  completeness: complete
- name: maintain-splash-pages
  source_repo_slug: lossless-monorepo
  skill_dir_path: /Users/mpstaton/code/lossless-monorepo/context-v/skills/maintain-splash-pages
  path_from_monorepo_root: context-v/skills/maintain-splash-pages
  has_skill_md: true
  skill_md_frontmatter:
    name: maintain-splash-pages
    description: The Lossless Group's pattern for repo-level splash pages — small
      Astro sites at <repo>/splash/ that ship to GitHub Pages on push to main, render
      the repo's changelog/ + context-v/ alongside curated marketing copy, and stay
      isolated from any package the repo also publishes. Use proactively whenever
      scaffolding a noteworthy new repo (every "important" repo wants one), when shipping
      a coherent chunk of work that an external reader would land on, when adding
      a feature (search, sort, tags row, theme mode) to an existing splash, when converting
      a legacy apps/<name>/ site to splash/, when troubleshooting a Pages deploy,
      or when the user mentions "splash", "GitHub Pages", "lossless-group.github.io",
      "Pagefind on our site", or working under a splash/ directory. Codifies the proven
      shape across three reference implementations (memopop-site, content-farm/splash,
      lfm/splash) and the package-isolation discipline that keeps splashes safe to
      add to repos that also publish to JSR/npm.
    status: Draft
  skill_md_body_lines: 423
  missing_required_fields: []
  asset_counts:
    references_md: 0
    templates_files: 0
    scripts_files: 0
    total_md: 1
  completeness: skill-md-only
- name: open-graph-share-seo-geo
  source_repo_slug: lossless-monorepo
  skill_dir_path: /Users/mpstaton/code/lossless-monorepo/context-v/skills/open-graph-share-seo-geo
  path_from_monorepo_root: context-v/skills/open-graph-share-seo-geo
  has_skill_md: true
  skill_md_frontmatter:
    name: open-graph-share-seo-geo
    description: How to make a page unfurl reliably in iMessage, WhatsApp, Slack,
      Discord, LinkedIn, and X — and stay legible to generative engines (GEO). Use
      when adding or debugging OpenGraph / Twitter Card metadata, picking an OG image
      format, choosing where to host the image, fixing pages that "won't unfurl",
      or auditing share previews on a marketing splash, blog post, plugin page, or
      product page. Encodes the JPEG-over-WebP rule, the ImageKit content-negotiation
      gotcha, the absolute-URL requirement, the og:image:type-must-match-bytes invariant,
      and the cache-busting recipe for forcing a re-unfurl.
  skill_md_body_lines: 180
  missing_required_fields: []
  asset_counts:
    references_md: 3
    templates_files: 0
    scripts_files: 0
    total_md: 4
  completeness: complete
- name: pseudomonorepos
  source_repo_slug: lossless-monorepo
  skill_dir_path: /Users/mpstaton/code/lossless-monorepo/context-v/skills/pseudomonorepos
  path_from_monorepo_root: context-v/skills/pseudomonorepos
  has_skill_md: true
  skill_md_frontmatter:
    name: pseudomonorepos
    description: The Lossless Group's coined term and pattern — parent repos that
      aggregate child repos (often as git submodules) primarily to host a parent-level
      context-v/. Use whenever working anywhere in lossless-monorepo or its descendants,
      when starting any new task that might overlap with prior work, when scaffolding
      a new project, or when the user mentions "pseudomonorepo", "submodule", "context-v",
      or names of the children (ai-labs, astro-knots, content-farm, tidyverse). Encodes
      the search-first-before-creating behavior and the tree-walking discipline.
  skill_md_body_lines: 215
  missing_required_fields: []
  asset_counts:
    references_md: 6
    templates_files: 0
    scripts_files: 0
    total_md: 7
  completeness: complete
- name: study-repos-first
  source_repo_slug: lossless-monorepo
  skill_dir_path: /Users/mpstaton/code/lossless-monorepo/context-v/skills/study-repos-first
  path_from_monorepo_root: context-v/skills/study-repos-first
  has_skill_md: true
  skill_md_frontmatter:
    name: study-repos-first
    description: The Lossless Group's discipline of pinning a curated collection of
      upstream repos (a "study") around a domain question *before* designing or coding
      in that domain. Use when starting work that touches conventions, file formats,
      schemas, protocols, or any decision where prior art exists; when the user mentions
      "study", "studies/", "reference collection", "prior art", "pin a submodule",
      or names of existing studies (open-specs-and-standards, memory-layers-for-agents,
      data-analytics-specifications-and-standards); when scaffolding a new study,
      extending one, or deciding whether something belongs in a study vs. a project.
      Encodes the "read upstream code, don't paraphrase from training data" behavior.
  skill_md_body_lines: 117
  missing_required_fields: []
  asset_counts:
    references_md: 0
    templates_files: 0
    scripts_files: 0
    total_md: 1
  completeness: skill-md-only
- name: theme-system
  source_repo_slug: lossless-monorepo
  skill_dir_path: /Users/mpstaton/code/lossless-monorepo/context-v/skills/theme-system
  path_from_monorepo_root: context-v/skills/theme-system
  has_skill_md: true
  skill_md_frontmatter:
    name: theme-system
    description: The Lossless Group's theme and mode architecture — two-tier token
      system, three-mode contract (light/dark/vibrant), theme.css organization, and
      design system conventions. Use when setting up themes/modes for any Astro Knots
      site, debugging mode toggles, working with CSS tokens, or when the user mentions
      "vibrant mode", "two-tier tokens", "theme.css", or design system patterns.
  skill_md_body_lines: 90
  missing_required_fields: []
  asset_counts:
    references_md: 3
    templates_files: 0
    scripts_files: 0
    total_md: 4
  completeness: complete
---

# Skills Manifest

Auto-generated inventory of agent skills (Anthropic agent-skills spec) found under any `context-v/skills/` directory in the curated sources. Tracked separately from `corpus-manifest.md` so skills don't pollute the fill-out to-do list — but indexed downstream alongside the corpus. Re-run `python scripts/build-skills-manifest.py` after editing skills or `sources.md`.

## Summary

- Total skills: **12**
- With `SKILL.md`: 11
- Without `SKILL.md`: 1

### By completeness

| state | count |
|---|---:|
| `complete` | 9 |
| `skill-md-only` | 2 |
| `missing-required-fields` | 0 |
| `no-skill-md` | 1 |

### By source repo

| source_repo_slug | count |
|---|---:|
| `lossless-monorepo` | 12 |

## Skills

| name | source | completeness | refs | templates | scripts | description |
|---|---|---|---:|---:|---:|---|
| [`astro-knots`](../../context-v/skills/astro-knots/SKILL.md) | `lossless-monorepo` | `complete` | 7 | 0 | 0 | The Lossless Group's Astro Knots conventions — vision, tech hierarchy, approved framewo… |
| [`changelog`](../../context-v/skills/changelog) | `lossless-monorepo` | `no-skill-md` | 0 | 0 | 0 |  |
| [`changelog-conventions`](../../context-v/skills/changelog-conventions/SKILL.md) | `lossless-monorepo` | `complete` | 5 | 2 | 0 | How The Lossless Group writes and structures changelog/ entries across all repos (proje… |
| [`context-vigilance`](../../context-v/skills/context-vigilance/SKILL.md) | `lossless-monorepo` | `complete` | 5 | 6 | 0 | Lossless Group's framework for managing context-v/ directories in any project. Use when… |
| [`deck-iteration-workflow`](../../context-v/skills/deck-iteration-workflow/SKILL.md) | `lossless-monorepo` | `complete` | 1 | 2 | 0 | The Lossless Group's workflow for developing slides-only Astro sites for fundraise proc… |
| [`git-conventions`](../../context-v/skills/git-conventions/SKILL.md) | `lossless-monorepo` | `complete` | 3 | 0 | 0 | The Lossless Group's git commit message conventions — structured headers with action ve… |
| [`lossless-flavored-markdown`](../../context-v/skills/lossless-flavored-markdown/SKILL.md) | `lossless-monorepo` | `complete` | 5 | 0 | 0 | The Lossless Group's extended-markdown flavor — what LFM is, when to use it, how its di… |
| [`maintain-splash-pages`](../../context-v/skills/maintain-splash-pages/SKILL.md) | `lossless-monorepo` | `skill-md-only` | 0 | 0 | 0 | The Lossless Group's pattern for repo-level splash pages — small Astro sites at <repo>/… |
| [`open-graph-share-seo-geo`](../../context-v/skills/open-graph-share-seo-geo/SKILL.md) | `lossless-monorepo` | `complete` | 3 | 0 | 0 | How to make a page unfurl reliably in iMessage, WhatsApp, Slack, Discord, LinkedIn, and… |
| [`pseudomonorepos`](../../context-v/skills/pseudomonorepos/SKILL.md) | `lossless-monorepo` | `complete` | 6 | 0 | 0 | The Lossless Group's coined term and pattern — parent repos that aggregate child repos … |
| [`study-repos-first`](../../context-v/skills/study-repos-first/SKILL.md) | `lossless-monorepo` | `skill-md-only` | 0 | 0 | 0 | The Lossless Group's discipline of pinning a curated collection of upstream repos (a "s… |
| [`theme-system`](../../context-v/skills/theme-system/SKILL.md) | `lossless-monorepo` | `complete` | 3 | 0 | 0 | The Lossless Group's theme and mode architecture — two-tier token system, three-mode co… |

