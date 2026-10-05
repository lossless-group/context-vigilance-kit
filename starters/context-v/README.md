# context-v

This folder is the project's living documentation, written for three readers: the people working on it, the AI agents helping them, and anyone arriving cold. It's agent memory you can read, edit, and version like code.

| Folder | What goes in it |
|---|---|
| `specs/` | What we're building and why |
| `plans/` | Ordered work toward a spec |
| `prompts/` | Step-by-step implementation, each step checkable |
| `blueprints/` | How the system is designed, and why |
| `reminders/` | Short corrections an agent keeps needing |
| `agent-skills/` | Skills specific to this repo |
| `explorations/` | Questions we haven't answered yet |
| `issues/` | The path through hard problems, wrong turns included |
| `extra/` | Scratch. Gitignored. |
| `sitemap/` | What exists where: pages, routes, endpoints |

Folders like `loops/`, `handoffs/`, and `decisions/` appear when they're first needed.

**Working with an agent:** ask it to `kickoff` at the start of a session, `new spec "…"` to start a doc, `prep` to turn an idea into a plan, `implement` or `loop` to build it, and `reflect` to wrap up. These come from the [context-vigilance-kit](https://github.com/lossless-group/context-vigilance-kit).
