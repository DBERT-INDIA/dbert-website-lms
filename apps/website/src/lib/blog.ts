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
  const staticSlugs = fs
    .readdirSync(BLOG_DIR)
    .filter((file) => file.endsWith('.md') || file.endsWith('.mdx'))
    .map((file) => file.replace(/\.mdx?$/, ''));

  // Ensure published dynamic posts are recognized as valid static slugs
  const knownDynamicSlugs = [
    'architecting-gayatri-exam-portal-production-ai-agent-develop',
    'architecting-gayatri-exam-portal-production-ai-agent-development',
  ];

  return Array.from(new Set([...staticSlugs, ...knownDynamicSlugs]));
}

/**
 * Retrieves the raw markdown content for an individual blog post, with YAML frontmatter stripped.
 */
export function getPostContent(slug: string): string | null {
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
  const { content } = matter(fileContents);
  return content;
}

/**
 * Retrieves combined static + dynamic LMS blog posts for server-rendered listings.
 */
export async function getAllBlogPostsWithDynamic(): Promise<BlogPostMeta[]> {
  const staticPosts = getAllPosts();
  try {
    const res = await fetch('https://lms.dbert.in/api/public/blog-posts', {
      headers: { Accept: 'application/json' },
      next: { revalidate: 120 },
      signal: AbortSignal.timeout(3500),
    });
    if (res.ok) {
      const data = await res.json();
      if (data.status === 'success' && Array.isArray(data.posts) && data.posts.length > 0) {
        const existingSlugs = new Set(staticPosts.map((p) => p.slug));
        const dynamicPosts: BlogPostMeta[] = [];
        data.posts.forEach((p: any) => {
          if (!existingSlugs.has(p.slug)) {
            dynamicPosts.push({
              slug: p.slug,
              title: p.title,
              desc: p.desc || '',
              readTime: p.readTime || '5 min read',
              date: p.date || '2026-11-01',
              author: p.author || 'DBERT Fellow',
              authorRole: p.authorRole || 'Engineering Contributor',
              authorBio: 'Technical publication by DBERT engineering contributor.',
              tags: Array.isArray(p.tags) ? p.tags : ['Engineering', 'Technical Guide'],
              canonicalUrl: p.canonicalUrl,
            });
          }
        });
        return [...dynamicPosts, ...staticPosts].sort(
          (a, b) => new Date(b.date).getTime() - new Date(a.date).getTime()
        );
      }
    }
  } catch (err) {
    // Graceful fallback to static posts if offline or during build
  }
  return staticPosts;
}
