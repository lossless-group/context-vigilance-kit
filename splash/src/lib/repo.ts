/** Where the kit's source lives, for "view on GitHub" links. */
export const REPO_URL = 'https://github.com/lossless-group/context-vigilance-kit';
export const REPO_BLOB = `${REPO_URL}/blob/master`;

/** Published = not explicitly held back. Matches the context-vigilance rule:
 *  `publish: false` or `private: true` keeps a doc off the site. */
export function isPublished(data: Record<string, any>): boolean {
  return data.publish !== false && data.private !== true;
}
