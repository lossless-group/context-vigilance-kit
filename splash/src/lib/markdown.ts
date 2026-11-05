/**
 * Markdown bodies for every detail page, rendered through LFM
 * (@lossless-group/lfm). Pattern: lifted from the hope-ai splash.
 *
 * Each collection entry keeps its raw body; pages parse it here with
 * `parseMarkdown` and render the MDAST tree via
 * components/markdown/AstroMarkdown.astro, so callouts, hex-code citations,
 * code blocks, and images all follow LFM.
 *
 * Links between docs are valid in any form: `[[Name]]`, `[[path/Name]]`,
 * `[[path/Name|alias]]`, `[[path/Name.md|alias]]`, `[[Name#Heading|alias]]`, and
 * markdown links like `[alias](../path/Name.md)`. They're resolved before parsing:
 * a kit doc or pattern on this site links to its page; a file in this repo links
 * to GitHub; anything else stays as plain text. Code is left as written.
 */
import { existsSync } from 'node:fs';
import { resolve } from 'node:path';
import { getCollection } from 'astro:content';
import { parseMarkdown } from '@lossless-group/lfm';
import { REPO_BLOB, isPublished } from './repo';

type Index = Map<string, string>;
let index: Index | null = null;

/** Lowercased name or id → site path (relative to BASE_URL). */
async function siteIndex(): Promise<Index> {
  if (index) return index;
  index = new Map();
  for (const e of await getCollection('context').catch(() => [])) {
    if (!isPublished(e.data as any)) continue;
    const href = `context-v/${e.id}/`;
    const fileName = ((e as any).filePath ?? e.id).split('/').pop()!.replace(/\.md$/i, '');
    index.set(fileName.toLowerCase(), href);
    index.set(e.id.toLowerCase(), href);
    index.set(e.id.split('/').pop()!.toLowerCase(), href);
  }
  for (const e of await getCollection('changelog').catch(() => [])) {
    if (!isPublished(e.data as any)) continue;
    index.set(e.id.toLowerCase(), `changelog/${e.id}/`);
  }
  for (const p of await getCollection('patterns').catch(() => [])) {
    index.set(p.id.toLowerCase(), `patterns/${p.id}/`);
  }
  return index;
}

/** The repo-relative file a link path names, or null. Doc paths are relative to context-v/. */
function fileInRepo(path: string): string | null {
  const noPrefix = path.replace(/^context-v\//, '');
  const candidates = [`context-v/${noPrefix}.md`, `context-v/${noPrefix}`, `${path}.md`, path];
  // The site builds from splash/, one level below the repo root.
  return candidates.find((file) => existsSync(resolve(process.cwd(), '..', file))) ?? null;
}

/** Matches the renderer's fallback heading id (AstroMarkdown.astro). */
function headingId(heading: string): string {
  return heading.toLowerCase().replace(/[^a-z0-9\s-]/g, '').trim().replace(/\s+/g, '-');
}

/** Code first, so a link shown as an example inside code is passed over. */
const LINK = /(```[\s\S]*?```|~~~[\s\S]*?~~~|`[^`\n]*`)|\[\[([^[\]\n]+?)\]\]|(?<!!)\[([^\]\n]*)\]\(((?![a-z][a-z0-9+.-]*:)[^)\s]*\.md(?:#[^)\s]*)?)\)/gi;

export async function resolveLinks(body: string): Promise<string> {
  const idx = await siteIndex();
  const base = import.meta.env.BASE_URL;
  const render = (target: string, alias?: string) => {
    const [rawPath, heading] = target.split('#');
    const path = rawPath.trim().replace(/^(\.\.?\/)+/, '').replace(/^\//, '').replace(/\.md$/i, '');
    const name = path.split('/').pop()!;
    const anchor = heading?.trim() ? `#${headingId(heading)}` : '';
    // No alias? Show the filename the way an alias would: - and _ as spaces.
    const label = (alias || name.replace(/[-_]+/g, ' ') || heading || '').trim();
    if (!path) return `[${label}](${anchor})`;
    const key = path.replace(/^context-v\//, '').toLowerCase();
    const href = idx.get(key) ?? idx.get(name.toLowerCase());
    if (href) return `[${label}](${base}${href}${anchor})`;
    // A file in this repo links to GitHub. Anything else (a doc not written
    // yet, a file in another repo) can't be linked from here, so stays as text.
    const file = path.includes('/') ? fileInRepo(path) : null;
    return file ? `[${label}](${REPO_BLOB}/${encodeURI(file)}${anchor})` : label;
  };
  return body.replace(LINK, (match, code, wiki, text, href) => {
    if (code) return match;
    if (href) return render(decodeURI(href), text);
    // Inside a table cell the pipe is written `\|`.
    const [target, ...alias] = wiki.replace(/\\\|/g, '|').split('|');
    return render(target, alias.join('|'));
  });
}

export async function renderable(body: string | undefined) {
  // The page header already shows the title, so drop a leading `# Title`.
  const text = (body ?? '').replace(/^\s*#\s+[^\n]*\n/, '');
  const tree = await parseMarkdown(await resolveLinks(text));
  const citations = ((tree as any)?.data?.citations?.ordered ?? []) as any[];
  return { tree, citations };
}
