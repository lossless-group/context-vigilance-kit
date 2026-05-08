---
title: Preference for Shortcuts in Config to Absolute Paths
source_root: /Users/mpstaton/code/lossless-monorepo/astro-knots/context-v
source_relative_path: reminders/Preference-for-Shortcuts-in-Config-to-Absolute-Paths.md
source_repo_slug: astro-knots
collated_at: '2026-05-08'
source_path: "astro-knots/context-v/reminders/Preference-for-Shortcuts-in-Config-to-Absolute-Paths.md"
---

```shell
⏺ Write(splash/tsconfig.json)
  ⎿  Added 12 lines, removed 1 line
       1  {
       2    "extends": "astro/tsconfigs/strict",
       3    "include": [".astro/types.d.ts", "**/*"],
       4 -  "exclude": ["dist"]
       4 +  "exclude": ["dist"],
       5 +  "compilerOptions": {
       6 +    "baseUrl": ".",
       7 +    "paths": {
       8 +      "@/*": ["src/*"],
       9 +      "@components/*": ["src/components/*"],
      10 +      "@layouts/*": ["src/layouts/*"],
      11 +      "@loaders/*": ["src/loaders/*"],
      12 +      "@content/*": ["src/content/*"],
      13 +      "@pages/*": ["src/pages/*"]
      14 +    }
      15 +  }
      16  }
```