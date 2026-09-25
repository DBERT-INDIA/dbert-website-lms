import React from 'react';
import type { Metadata } from 'next';
import Link from 'next/link';
import { notFound } from 'next/navigation';
import { getPostMeta, getBlogSlugs } from '@/lib/blog';
import AuthorBox from '@/components/blog/AuthorBox';
import ArticleSchema from '@/components/seo/ArticleSchema';
import s from '../blog.module.css';

export async function generateStaticParams() {
  const slugs = getBlogSlugs();
  return slugs.map((slug) => ({ slug }));
}

interface BlogPostProps {
  params: Promise<{ slug: string }>;
}

export async function generateMetadata({ params }: BlogPostProps): Promise<Metadata> {
  const { slug } = await params;
  const meta = getPostMeta(slug);
  if (!meta) {
    return {
      title: 'Insight Not Found | DBERT Labs',
      description: 'The requested technical insight could not be located in our research archive.',
    };
  }
  return {
    title: `${meta.title} | DBERT Blog`,
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
  const meta = getPostMeta(slug);

  if (!meta) {
    notFound();
  }

  let ContentComponent: React.ComponentType | null = null;
  try {
    const imported = await import(`@/content/blog/${slug}.mdx`);
    ContentComponent = imported.default;
  } catch {
    try {
      const importedMd = await import(`@/content/blog/${slug}.md`);
      ContentComponent = importedMd.default;
    } catch {
      notFound();
    }
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
          <div className={s.tagWrap}>
            {meta.tags && meta.tags.map((tag, i) => (
              <span key={i} className="marker">
                #{tag}
              </span>
            ))}
          </div>
        </div>

        <article className={`card ${s.postBody} ${s.mdxContent}`}>
          {ContentComponent ? <ContentComponent /> : (
            <p className="body-copy">Error rendering MDX document contents.</p>
          )}
        </article>

        <AuthorBox
          name={meta.author}
          role={meta.authorRole}
          bio={meta.authorBio}
        />

        <div className={s.postFoot}>
          <Link href="/blog" className="accent-note">
            &larr; Back to AI Engineering Blog Index
          </Link>
        </div>
      </div>
    </div>
  );
}

