# The Philosophy Behind Context Vigilance

**Contents:** Why `context-v/` exists · The cognitive modes · The count is not the answer · Audience: User + Agent + Reader · Cross-references and human context windows · Capability is not wisdom-to-use-it · Consistency vs. generativity · Obsidian (optional) · Rules vs. norms · Building in public

Read this when you need the *why* behind the patterns, not just the patterns.

## Why `context-v/` exists

Every AI session starts from zero. Without externalized memory, you re-explain your project to every new session, every collaborator, every model, and vibe-coded work drifts into spaghetti because nothing holds the decisions.

`context-v/` turns that knowledge into loadable files that survive session boundaries and serve humans, agents, and outside readers at once.

## The cognitive modes

The folders aren't a count for its own sake. They map to two paired cognitive modes plus a journey mode:

- **Planning** (specs → plans → prompts): forward motion. *"What shall we build and how?"*
- **Reflection** (blueprints ↔ reminders, agent-skills): backward motion. *"What have we learned and how do we keep doing it well?"*
- **Journey** (explorations, issues): exploratory motion. *"We don't know where this ends yet."*

When something doesn't fit, that's interesting: discuss it, give it a folder, see if it earns its place.

## The count is not the answer

The canonical set is convention, not law. Folders show up that no one planned (`notes/`, `research/`, etc.), and the convention grows by exactly that path: `plans/` and `agent-skills/` started as unplanned folders and were promoted to canon after wide adoption; `loops/`, `handoffs/`, `decisions/`, `habits/`, and `contracts/` sit in the experimental tier now. When you find an unplanned folder:

1. Ask what kind of cognitive activity it represents.
2. Discuss whether it deserves to become a norm or merge into an existing folder.
3. Either **assimilate** (promote it) or **fold** (move its contents into an existing folder).
4. **Default to keeping it** if unsure. Reorganizing someone's mental model mid-session is rude.

## Audience: User + Agent + Reader

Many `context-v/` docs end up public (a docs site, a project blog, a repo people browse). Every doc therefore balances three audiences:

1. **The User** writing or editing it (the project owner, today)
2. **The Agent** that will load it as context in some future session
3. **The Reader** who finds it with no prior context

Practical implications:

- **Lead with why, in plain language.** Technical detail goes deeper in the doc.
- The first paragraph should be readable by an outsider; the rest can be specialized.
- If a doc gets too long, **split it**: why → top of doc or its own short doc; pattern/architecture → blueprint; thing being built → spec; how to build it → prompt. The split is a feature, not a failure.

## Cross-references and human context windows

Humans have context windows too. Cross-referencing lets humans and agents focus on a limited scope at a time.

- `[[wikilinks]]` are preferred where your tooling resolves them (Obsidian and many static-site pipelines do).
- Standard Markdown links work fine everywhere.
- Backtick paths (`` `context-v/specs/X.md` ``) suit references you don't expect the reader to click.

The goal isn't link consistency. It's **scope discipline**: each doc should fit in one head (or one context window).

## Capability is not wisdom-to-use-it

Long-context models make it tempting to let documents grow because "the model can handle it." That conflates two things:

- **Technical capacity:** the model accepts a huge doc without truncating.
- **Working quality:** creativity, cross-referencing, and human-agent cooperation all suffer as a single document gets long, whatever the model can ingest.

Humans skim long docs; agents make vaguer suggestions inside them; multi-session work loses its thread re-locating the relevant part.

**The trigger to split is anxiety about length, not a word count.** When you (or the user) scroll past sections to find the one that matters, split. **Fork and cross-reference pre-emptively:**

- A self-contained sub-system → its own spec, linked from the parent.
- A reusable pattern → a blueprint, linked from the spec.
- A specific debugging journey → its own issue, linked from where it surfaced.

The parent keeps the *map*; the children carry the *detail*. Specs grow fastest, so this bites them hardest, but it applies to every doc-type.

## Consistency vs. generativity

Teams generate first; consistency emerges where attention focuses. To live with that tension:

- **Be generous reading existing files.** They may be older, experimental, or written under different assumptions.
- **Be thoughtful writing new ones.** Match conventions you know; ask about ones you don't.
- **When you notice drift, surface it.** Open an issue, write a blueprint, draft a reminder. Don't silently re-impose your preferences across a codebase.

## Obsidian (optional)

Some teams open `context-v/` as (or symlink it into) an Obsidian vault for backlinks, graph view, and search. If yours does, that's the reason behind several conventions:

- Frontmatter keys are `snake_case` (Obsidian's property panel indexes them cleanly).
- Tags are Train-Case (Obsidian treats `#Markdown-Rendering` as one tag; other separators behave inconsistently).
- Cross-references prefer `[[wikilinks]]`, and `aliases` in frontmatter add alternate link targets.

The conventions hold without Obsidian. The files are plain Markdown and render in any editor, on the web, and to any agent that reads text.

## Rules vs. norms

Almost everything here is a norm with a rationale, not a hard rule. (The few exact formats, like date and ID shapes, are called out in `frontmatter-spec.md`.)

If a norm isn't working on a specific doc, **break it**, and say why in the doc or in a new exploration. The next person (human or AI) learns from the deviation; that's how the framework evolves.

## Building in public

Imperfect docs in public beat perfect docs in private. If you find a sharper way to express a convention, propose the change; if you disagree with one, surface it.
