---
title: 'Stenographer: an Obsidian Plugin that Transcribes Audio Content'
lede: Drop a YouTube, SoundCloud, or other listenable link into Obsidian and Stenographer
  turns it into a fully-frontmattered note with a streaming, AI-generated transcript
  — sources become searchable knowledge in one move.
date_created: 2026-05-07
date_modified: 2026-05-07
authors:
- Michael Staton
augmented_with:
- Pi on Claude Opus 4.7 (1M context)
semantic_version: 0.0.0.1
tags:
- Spec
- Obsidian-Plugins
- Content-Farm
- Audio-Transcription
- Streaming-AI
status: Draft
source_root: /Users/mpstaton/code/lossless-monorepo/content-farm/context-v
source_relative_path: specs/Stenographer-an-Obsidian-Plugin-that-transcribes-Audio-Content.md
source_repo_slug: content-farm
collated_at: '2026-05-08'
source_path: "content-farm/context-v/specs/Stenographer-an-Obsidian-Plugin-that-transcribes-Audio-Content.md"
---

# Stenographer: an Obsidian Plugin that Transcribes Audio Content

<!-- developing -->

## Summary

Stenographer is an Obsidian plugin that follows a "listenable link" — YouTube, SoundCloud, podcast episode, raw audio URL — and produces a single Markdown note: provider metadata as YAML frontmatter at the top, a faithful AI-generated transcript streamed into the body. The goal is to make ephemeral spoken content first-class material in an Obsidian vault, with no leaving the editor and no after-the-fact cleanup.

## Prior art

- [[Create-an-Audio-Transcriber-plus-Layered-Value]] — the broader vision spec that frames audio-to-note as a value-layered workflow (transcript + summary + citations + …). Stenographer is the focused first cut: provider metadata + accurate transcript, nothing more layered yet. References [`obra/Youtube2Webpage`](https://github.com/obra/Youtube2Webpage) as a working precedent for the YouTube-to-document shape.
- [[../explorations/Using-APIs-to-Ingest-More-Data]] — explores third-party fetchers (Jina Reader, Firecrawl, etc.) and the "metadata to frontmatter, body to note" pattern Metafetch already implements for OpenGraph. Stenographer is the audio-shaped sibling.
- `plugin-modules/metafetch/` — established pattern for "fetch from a URL → write frontmatter to a note" inside Obsidian.
- `plugin-modules/perplexed/` — established pattern for streaming AI responses into the editor in real time.

## Goals

- Accept a listenable link (YouTube first; SoundCloud, podcast feeds, direct audio URLs as targets). 
 - A Command triggers a Modal that can take a link and manage options.
 - A Command triggers the Modal from a selected link within the markdown file.
- Resolve provider metadata (title, channel/host, duration, publish date, description, thumbnail, canonical URL) and write it to frontmatter.
- Connects to either an ideal AI provider for transcripts (Whisper, ElevenLabs) or a low cost alternative (e.g., local whisper.cpp).
- Generate and stream a full, accurate transcript into the note body, visible token-by-token as it arrives.
- Live inside Obsidian's command palette / link context — same UX shape as Metafetch and Perplexed.
- Does with established configuration and settings patterns, that allow the in focus-document from which the commands were launched to accurately reference BOTH the Obsidian backlink to the transcript, as well as the source link of the audio content.
- Uses the Obsidian UI api to display the output in the document in a way that Obsidian can render, to enable features like linking to specific timestamps in the audio.
- Generates a syntax that can be used with "Lossless Flavored Markdown" - so that Astro-Knots sites can render similar component functionality. 

### Wish List / Nice-to-Haves

- When given a playlist or channel, 
 - [ ] an option to process all items in the playlist or channel.
 - [ ] an option to select some items from the playlist or channel, via search or scroll. (Might have to fetch the list first and add items either to the markdown document from which the command was called or to a separate queue)
 - [ ] an option to process items in parallel.

## Non-goals (at the moment)

- Summarization, chaptering, citation extraction, or any "layered value" beyond raw transcript (those belong to the broader spec).
- Hosting audio or shipping vault content anywhere beyond the chosen API providers.
- Recording from a microphone or processing local audio files (separate scope; revisit later).

## Constraints & Assumptions

- // TBD — provider strategy: which transcription model/service (Whisper API, AssemblyAI, Deepgram, Groq-hosted Whisper, local whisper.cpp, …) and whether streaming-token UX is achievable per provider.
- // TBD — audio acquisition path for YouTube / SoundCloud (yt-dlp invocation, server-side helper, provider's native URL ingest).
- Follows the established Content Farm plugin shape (esbuild bundle, `manifest.json`, `main.ts`, settings tab, modal commands, symbolic-linked dev loop).

## Design

// TBD — to be developed in dialog. Likely sections to populate: command surface, settings shape, file-creation rules (path, filename derivation, collision policy), frontmatter schema, transcript formatting (timestamps? speaker tags?), error handling, retry/resume on long transcripts.

## Open questions

- [ ] Where does the source URL come from — clipboard, modal input, current-line link, or all three?
- [ ] Single transcription provider at v1 or a Perplexed-style multi-provider settings tab from day one?
- [ ] Does Stenographer download the audio itself, or does it pass the URL through to a provider that ingests directly?
- [ ] Filename derivation: provider title slug? date prefix? user prompt?
- [ ] What happens on very long content (multi-hour podcasts) — chunking, resume, progress reporting?
- [ ] How much should overlap with the broader [[Create-an-Audio-Transcriber-plus-Layered-Value]] spec — does Stenographer subsume it, or stay strictly the "raw transcript" cut while the broader spec covers layered value?

## Related

- [[Create-an-Audio-Transcriber-plus-Layered-Value]]
- [[../explorations/Using-APIs-to-Ingest-More-Data]]
- `plugin-modules/metafetch/`
- `plugin-modules/perplexed/`
