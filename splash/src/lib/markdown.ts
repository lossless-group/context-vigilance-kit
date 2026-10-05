/**
 * Markdown bodies for every detail page, rendered through LFM
 * (@lossless-group/lfm). Pattern: lifted from the hope-ai splash.
 *
 * Each collection entry keeps its raw body; pages parse it here with
 * `parseMarkdown` and render the MDAST tree via
 * components/markdown/AstroMarkdown.astro, so callouts, hex-code citations,
 * code blocks, and images all follow LFM.
 *
 * Wikilinks (`[[Name]]`, `[[path/Name.md]]`, `[[Name|label]]`) are resolved
 * before parsing: a kit doc or pattern on this site links to its page; any
 * other path links to the file on GitHub; a bare name with no match stays as
 * plain text.
 */
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

export async function resolveWikilinks(body: string): Promise<string> {
  const idx = await siteIndex();
  const base = import.meta.env.BASE_URL;
  return body.replace(/\[\[([^\]|]+?)(?:\|([^\]]+))?\]\]/g, (_m, rawTarget: string, alias?: string) => {
    const target = rawTarget.trim().replace(/^(\.\.\/)+/, '').replace(/^\.\//, '');
    const noExt = target.replace(/\.md$/i, '');
    const name = noExt.split('/').pop()!;
    const label = (alias ?? name).trim();
    const key = noExt.replace(/^context-v\//, '').toLowerCase();
    const href = idx.get(key) ?? idx.get(name.toLowerCase());
    if (href) return `[${label}](${base}${href})`;
    // A path that exists in this repo links to GitHub; links into other
    // repos (../../other-repo/...) can't be resolved here, so stay as text.
    if (target.includes('/') && !rawTarget.trim().startsWith('..')) return `[${label}](${REPO_BLOB}/${target})`;
    return label;
  });
}

export async function renderable(body: string | undefined) {
  // The page header already shows the title, so drop a leading `# Title`.
  const text = (body ?? '').replace(/^\s*#\s+[^\n]*\n/, '');
  const tree = await parseMarkdown(await resolveWikilinks(text));
  const citations = ((tree as any)?.data?.citations?.ordered ?? []) as any[];
  return { tree, citations };
}
