import fs from 'fs';
import path from 'path';
import matter from 'gray-matter';

export interface BlogPostMeta {
  slug: string;
  title: string;
  desc: string;
  readTime: string;
  date: string;
  author: string;
  authorRole: string;
  authorBio: string;
  tags: string[];
  canonicalUrl?: string;
}

const BLOG_DIR = path.join(process.cwd(), 'src/content/blog');

/** Restores safe access to filesystem if directory hasn't been initialized yet. */
function ensureBlogDir() {
  if (!fs.existsSync(BLOG_DIR)) {
    fs.mkdirSync(BLOG_DIR, { recursive: true });
  }
}

/**
 * Retrieves metadata for all blog posts sorted by publishing date (newest first).
 * Uses gray-matter to parse MDX frontmatter cleanly at runtime/build without bundling heavy content strings.
 */
export function getAllPosts(): BlogPostMeta[] {
  ensureBlogDir();
  const files = fs.readdirSync(BLOG_DIR).filter((file) => file.endsWith('.md') || file.endsWith('.mdx'));

  const posts = files.map((filename) => {
    const slug = filename.replace(/\.mdx?$/, '');
    const filePath = path.join(BLOG_DIR, filename);
    const fileContents = fs.readFileSync(filePath, 'utf-8');
    const { data } = matter(fileContents);

    return {
      slug,
      title: data.title ?? 'Untitled Insight',
      desc: data.desc ?? '',
      readTime: data.readTime ?? '5 min read',
      date: data.date ?? '2026-07-27',
      author: data.author ?? 'DBERT Engineering',
      authorRole: data.authorRole ?? 'AI Systems Staff',
      authorBio: data.authorBio ?? 'Applied artificial intelligence research and incubation ecosystem.',
      tags: Array.isArray(data.tags) ? data.tags : [],
      canonicalUrl: data.canonicalUrl,
    } as BlogPostMeta;
  });

  return posts.sort((a, b) => (new Date(b.date).getTime() - new Date(a.date).getTime()));
}

/**
 * Retrieves frontmatter metadata for an individual blog slug.
 */
export function getPostMeta(slug: string): BlogPostMeta | null {
  ensureBlogDir();
  const filePathMdx = path.join(BLOG_DIR, `${slug}.mdx`);
  const filePathMd = path.join(BLOG_DIR, `${slug}.md`);

  const filePath = fs.existsSync(filePathMdx)
    ? filePathMdx
    : fs.existsSync(filePathMd)
    ? filePathMd
    : null;

  if (!filePath) return null;

  const fileContents = fs.readFileSync(filePath, 'utf-8');
  const { data } = matter(fileContents);

  return {
    slug,
    title: data.title ?? 'Untitled Insight',
    desc: data.desc ?? '',
    readTime: data.readTime ?? '5 min read',
    date: data.date ?? '2026-07-27',
    author: data.author ?? 'DBERT Engineering',
    authorRole: data.authorRole ?? 'AI Systems Staff',
    authorBio: data.authorBio ?? 'Applied artificial intelligence research and incubation ecosystem.',
    tags: Array.isArray(data.tags) ? data.tags : [],
    canonicalUrl: data.canonicalUrl,
  } as BlogPostMeta;
}

/**
 * Lists all valid blog slugs for static parameter building and XML sitmeap generation.
 */
export function getBlogSlugs(): string[] {
  ensureBlogDir();
  return fs
    .readdirSync(BLOG_DIR)
    .filter((file) => file.endsWith('.md') || file.endsWith('.mdx'))
    .map((file) => file.replace(/\.mdx?$/, ''));
}
