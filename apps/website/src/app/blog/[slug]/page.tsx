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
        certId={dynamicPost?.certId}
        domain={dynamicPost?.domain}
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

        {/* ── High-Authority Trust Mesh & Ecosystem Cross-Linking ── */}
        <div style={{
          background: 'linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(20, 26, 35, 0.95) 100%)',
          border: '1.5px solid rgba(226, 185, 111, 0.3)',
          borderRadius: '16px',
          padding: '1.75rem',
          marginTop: '2.5rem',
          boxShadow: '0 12px 30px rgba(0, 0, 0, 0.5), 0 0 20px rgba(226, 185, 111, 0.08)'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', color: '#E2B96F', fontSize: '0.8125rem', fontWeight: 800, textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: '0.75rem' }}>
            <span>🛡️</span> DBERT Institutional Quality Guarantee &bull; Academic Peer Review
          </div>
          <p style={{ color: '#E2E8F0', fontSize: '0.9375rem', lineHeight: '1.6', margin: '0 0 1.25rem' }}>
            This technical publication represents an authenticated production milestone engineered during the DBERT Incubation Fellowship. The underlying codebase, automated test suites, and system architecture have undergone independent rubric evaluation with Turnitin originality validation (&lt; 3.0% similarity index).
          </p>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: '1rem', borderTop: '1px solid rgba(255, 255, 255, 0.08)', paddingTop: '1.25rem' }}>
            <div style={{ background: 'rgba(255, 255, 255, 0.03)', border: '1px solid rgba(255, 255, 255, 0.08)', borderRadius: '12px', padding: '1.25rem' }}>
              <div style={{ color: '#38BDF8', fontSize: '0.75rem', fontWeight: 800, textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: '0.35rem' }}>
                For Aspiring Engineers
              </div>
              <h4 style={{ color: '#fff', fontSize: '1.05rem', margin: '0 0 0.5rem', fontWeight: 700 }}>
                Build Production Systems
              </h4>
              <p style={{ color: '#94A3B8', fontSize: '0.8125rem', lineHeight: '1.5', margin: '0 0 1rem' }}>
                Join the next cohort, receive 1:1 mentorship from industry staff, and publish verified capstone case studies.
              </p>
              <Link href="/enroll/1999" style={{ color: '#E2B96F', fontSize: '0.8125rem', fontWeight: 700, textDecoration: 'none', display: 'inline-flex', alignItems: 'center', gap: '0.3rem' }}>
                Apply for Fellowship &rarr;
              </Link>
            </div>

            <div style={{ background: 'rgba(255, 255, 255, 0.03)', border: '1px solid rgba(255, 255, 255, 0.08)', borderRadius: '12px', padding: '1.25rem' }}>
              <div style={{ color: '#34D399', fontSize: '0.75rem', fontWeight: 800, textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: '0.35rem' }}>
                For Tech Recruiters &amp; Employers
              </div>
              <h4 style={{ color: '#fff', fontSize: '1.05rem', margin: '0 0 0.5rem', fontWeight: 700 }}>
                Hire Pre-Vetted Fellows
              </h4>
              <p style={{ color: '#94A3B8', fontSize: '0.8125rem', lineHeight: '1.5', margin: '0 0 1rem' }}>
                Discover engineers with verified code rubrics, live deployment URLs, and zero recruiter markup fees.
              </p>
              <Link href="/verify/directory" style={{ color: '#34D399', fontSize: '0.8125rem', fontWeight: 700, textDecoration: 'none', display: 'inline-flex', alignItems: 'center', gap: '0.3rem' }}>
                Browse Pre-Vetted Directory &rarr;
              </Link>
            </div>
          </div>
        </div>

        <div className={s.postFoot}>
          <Link href="/blog" className="accent-note">
            &larr; Back to AI Engineering Blog Index
          </Link>
        </div>
      </div>
    </div>
  );
}
