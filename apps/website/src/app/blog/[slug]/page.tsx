import React from 'react';
import type { Metadata } from 'next';
import Link from 'next/link';
import { notFound } from 'next/navigation';
import { getPostMeta, getPostContent, getBlogSlugs } from '@/lib/blog';
import AuthorBox from '@/components/blog/AuthorBox';
import AuthorDossierBox from '@/components/blog/AuthorDossierBox';
import StandardMarkdownRenderer from '@/components/blog/StandardMarkdownRenderer';
import ArticleSchema from '@/components/seo/ArticleSchema';
import HandNote from '@/components/ui/HandNote';
import AdSenseSlot from '@/components/ads/AdSenseSlot';
import s from '../blog.module.css';

export async function generateStaticParams() {
  const slugs = getBlogSlugs();
  return slugs.map((slug) => ({ slug }));
}

interface BlogPostProps {
  params: Promise<{ slug: string }>;
}

async function fetchDynamicPost(slug: string) {
  const trySlugs = [slug];
  if (slug.endsWith('-development')) {
    trySlugs.push(slug.replace(/-development$/, '-develop'));
  } else if (slug.endsWith('-develop')) {
    trySlugs.push(slug.replace(/-develop$/, '-development'));
  }

  for (const s of trySlugs) {
    try {
      const res = await fetch(`https://lms.dbert.in/api/public/blog-posts/${s}`, {
        next: { revalidate: 300 },
        headers: { Accept: 'application/json' },
      });
      if (!res.ok) continue;
      const data = await res.json();
      if (data.status === 'success' && data.post) {
        return data.post;
      }
    } catch (err) {
      // Continue to next candidate
    }
  }
  return null;
}

export async function generateMetadata({ params }: BlogPostProps): Promise<Metadata> {
  const { slug } = await params;
  let meta = getPostMeta(slug);

  if (!meta) {
    const dyn = await fetchDynamicPost(slug);
    if (dyn) {
      meta = {
        slug: dyn.slug,
        title: dyn.title,
        desc: dyn.desc,
        readTime: dyn.readTime || '5 min read',
        date: dyn.date,
        author: dyn.author,
        authorRole: dyn.authorRole,
        authorBio: dyn.authorBio || 'DBERT Engineering Fellow',
        tags: dyn.tags || ['Engineering', 'Research'],
        canonicalUrl: dyn.canonicalUrl,
      };
    }
  }

  if (!meta) {
    return {
      title: 'Insight Not Found | DBERT Labs',
      description: 'The requested technical insight could not be located in our research archive.',
    };
  }

  return {
    title: `${meta.title} | DBERT Engineering Blog`,
    description: meta.desc,
    openGraph: {
      title: meta.title,
      description: meta.desc,
      type: 'article',
      publishedTime: meta.date,
      authors: [meta.author],
    },
  };
}

export default async function BlogPostPage({ params }: BlogPostProps) {
  const { slug } = await params;
  let meta = getPostMeta(slug);
  let isDynamic = false;
  let dynamicPost: any = null;

  if (!meta) {
    dynamicPost = await fetchDynamicPost(slug);
    if (dynamicPost) {
      isDynamic = true;
      meta = {
        slug: dynamicPost.slug,
        title: dynamicPost.title,
        desc: dynamicPost.desc || '',
        readTime: dynamicPost.readTime || '5 min read',
        date: dynamicPost.date,
        author: dynamicPost.author,
        authorRole: dynamicPost.authorRole,
        authorBio: dynamicPost.authorBio || 'DBERT Engineering Fellow',
        tags: dynamicPost.tags || ['Engineering', 'Technical Guide'],
        canonicalUrl: dynamicPost.canonicalUrl,
      };
    }
  }

  if (!meta) {
    notFound();
  }

  // Obtain clean markdown content (stripped of frontmatter)
  let markdownBody = '';
  if (isDynamic && dynamicPost) {
    markdownBody = dynamicPost.content_markdown || '';
  } else {
    markdownBody = getPostContent(slug) || '';
  }

  if (!markdownBody && !isDynamic) {
    notFound();
  }

  return (
    <div className="container pad-block">
      <ArticleSchema
        title={meta.title}
        description={meta.desc}
        datePublished={meta.date}
        authorName={meta.author}
        slug={meta.slug}
      />
      <div className="measure">
        <div className={s.postHead}>
          <div className="stack-h justify-between align-center mb-2">
            <span className={s.readTime}>{meta.readTime}</span>
            <time dateTime={meta.date} className="faint-label">
              {meta.date}
            </time>
          </div>
          <h1 className={s.postTitle}>{meta.title}</h1>
          <p className={s.postDesc}>{meta.desc}</p>
          <div className="stack-h justify-between align-center flex-wrap gap-3">
            <div className={s.tagWrap}>
              {meta.tags &&
                meta.tags.map((tag, i) => (
                  <span key={i} className="tag-chip">
                    #{tag}
                  </span>
                ))}
            </div>
            <HandNote tone="blue">verified lab benchmark ✎</HandNote>
          </div>
        </div>

        {/* Dynamic Author Bento Dossier (Proof of Work) */}
        {isDynamic && dynamicPost && (
          <AuthorDossierBox
            name={dynamicPost.author}
            role={dynamicPost.authorRole}
            domain={dynamicPost.domain}
            certId={dynamicPost.certId}
            githubRepoUrl={dynamicPost.githubRepoUrl}
            liveDemoUrl={dynamicPost.liveDemoUrl}
            rubricScore={dynamicPost.rubricScore}
            stipendStatus={dynamicPost.stipendStatus}
            slug={meta.slug}
          />
        )}

        {/* Standardized, High-Contrast Reading Surface */}
        <article className={`card ${s.postBody} ${s.mdxContent}`}>
          {markdownBody ? (
            <StandardMarkdownRenderer
              content={markdownBody}
              titleToStrip={meta.title}
            />
          ) : (
            <p className="body-copy">Article content unavailable.</p>
          )}
        </article>

        <AdSenseSlot slotId="blog-post-bottom" />

        {isDynamic && dynamicPost ? (
          <AuthorDossierBox
            name={dynamicPost.author}
            role={dynamicPost.authorRole}
            domain={dynamicPost.domain}
            certId={dynamicPost.certId}
            githubRepoUrl={dynamicPost.githubRepoUrl}
            liveDemoUrl={dynamicPost.liveDemoUrl}
            rubricScore={dynamicPost.rubricScore}
            stipendStatus={dynamicPost.stipendStatus}
            slug={meta.slug}
          />
        ) : (
          <AuthorBox
            name={meta.author}
            role={meta.authorRole}
            bio={meta.authorBio}
          />
        )}

        <div className={s.postFoot}>
          <Link href="/blog" className="accent-note">
            &larr; Back to AI Engineering Blog Index
          </Link>
        </div>
      </div>
    </div>
  );
}
