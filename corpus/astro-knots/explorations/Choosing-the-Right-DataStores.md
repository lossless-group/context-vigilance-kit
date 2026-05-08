---
source_root: /Users/mpstaton/code/lossless-monorepo/astro-knots/context-v
source_relative_path: explorations/Choosing-the-Right-DataStores.md
source_repo_slug: astro-knots
collated_at: '2026-05-08'
source_path: "astro-knots/context-v/explorations/Choosing-the-Right-DataStores.md"
---





```txt
views:
  - type: table
    name: Table
    filters:
      and:
        - file.inFolder("organizations")
    order:
      - file.name
      - date_created
      - for_clients
      - file.size

```