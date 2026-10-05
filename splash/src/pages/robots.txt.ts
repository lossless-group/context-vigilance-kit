/**
 * /robots.txt, generated so the sitemap URL is right on every host
 * (GitHub Pages under /context-vigilance-kit/, Vercel at the root).
 */
import type { APIRoute } from 'astro';

export const GET: APIRoute = () => {
  const site = import.meta.env.SITE ?? 'https://lossless-group.github.io';
  const base = import.meta.env.BASE_URL ?? '/';
  const sitemap = new URL(`${base.replace(/\/?$/, '/')}sitemap-index.xml`, site).toString();
  return new Response(`User-agent: *\nAllow: /\n\nSitemap: ${sitemap}\n`, {
    headers: { 'Content-Type': 'text/plain; charset=utf-8' },
  });
};
