# context-vigilance-kit

> Treat context files with the same vigilance as code, and *context becomes the code*.

**Context Vigilance** is a practice for working with AI agents: keep a `context-v/` directory in every repo — specs, plans, prompts, blueprints, reminders, explorations, issues — written so that a human, a future agent session, and an outside reader can all pick up where the work left off. It is agent memory you can read, edit, and version like code.

This repo is the **installable kit**: a Claude Code plugin (`cv`) carrying the practice's skill, a handful of `/cv:*` commands, document templates, a starter scaffold, and neutral examples. Installing it should give you the practice and nothing else — no corpus, no vector database, no Python environment.

## Status: pre-release

Nothing is installable yet. The design is settled and the build has not started:

- **What the plugin is and isn't:** [`context-v/specs/MVP-to-Claude-Code-Plugin.md`](context-v/specs/MVP-to-Claude-Code-Plugin.md)
- **The full command catalog**, including the later tiers: [`context-v/specs/Commands-and-Agent-Skills-for-Context-V.md`](context-v/specs/Commands-and-Agent-Skills-for-Context-V.md)
- **Making frontmatter status checkable:** [`context-v/explorations/Context-V-as-a-Claude-Code-Plugin.md`](context-v/explorations/Context-V-as-a-Claude-Code-Plugin.md)
- **Installing into any agent, and where Claude Code mods fit:** [`context-v/explorations/Context-V-as-a-Portable-Plugin-Any-Agent-Can-Install.md`](context-v/explorations/Context-V-as-a-Portable-Plugin-Any-Agent-Can-Install.md)
- **Why this repo is separate from the corpus:** [`context-v/issues/Plugin-Install-Would-Clone-the-Whole-Corpus.md`](context-v/issues/Plugin-Install-Would-Clone-the-Whole-Corpus.md)

## What will live here

```
context-vigilance-kit/
├── .claude-plugin/marketplace.json   ← install source
├── plugin/                           ← skills, /cv:* commands, templates
├── starters/                         ← what /cv:init lays down in your repo
├── examples/                         ← a fictional project, walked through the practice
├── context-v/                        ← this kit's own specs and decisions
└── changelog/
```

**One rule for this repo:** nothing generated from real project content is committed here. Examples are synthetic, and vendored skills are stripped of anything specific to one organization. That rule is the reason this repo exists separately.

## Related

- **[`context-v-corpus`](https://github.com/lossless-group/context-v-corpus):** The Lossless Group's own collated `context-v/` corpus across ~40 repos, with the manifests, Chroma and Graphiti ingesters, and a [public catalog](https://lossless-group.github.io/context-v-corpus/). This kit grew out of it. You don't need it to use the kit.
- **[`lossless-agent-skills`](https://github.com/lossless-group/lossless-agent-skills):** the upstream source of the `context-vigilance` skill this plugin will vendor.

## License

[MPL-2.0](LICENSE), with an additional permission: what you make with the kit is yours. Copies of its templates and starters, and the `context-v/` docs you write, carry no license obligations. See [LICENSING.md](LICENSING.md).

Branch tiers: `development` → `main` → `master`.
