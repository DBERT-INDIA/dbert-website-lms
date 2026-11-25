import React from 'react';
import type { Metadata } from 'next';
import Link from 'next/link';
import { notFound } from 'next/navigation';
import { getPostMeta, getPostContent, getBlogSlugs } from '@/lib/blog';
import AuthorBox from '@/components/blog/AuthorBox';
import AuthorDossierBox from '@/components/blog/AuthorDossierBox';
import StandardMarkdownRenderer from '@/components/blog/StandardMarkdownRenderer';
import ArticleSchema from '@/components/seo/ArticleSchema';
import Faq from '@/components/seo/Faq';
import HandNote from '@/components/ui/HandNote';
import TrackedLink from '@/components/ui/TrackedLink';
import AdSenseSlot from '@/components/ads/AdSenseSlot';
import { GEO_CITIES, GEO_ROLES } from '@/data/geo_domains.config';
import publishedArticles from '@/data/published_articles.json';
import s from '../blog.module.css';

function hashSlug(str: string): number {
  let h = 0;
  for (let i = 0; i < str.length; i++) {
    h = ((h << 5) - h + str.charCodeAt(i)) | 0;
  }
  return Math.abs(h);
}

function pickGeoLinksForSlug(slug: string, tags: string[], domain?: string) {
  const haystack = `${slug} ${tags.join(' ')} ${domain || ''}`.toLowerCase();
  let primaryRoleKey = 'ai-agent-development';
  if (haystack.includes('full-stack') || haystack.includes('saas') || haystack.includes('next')) primaryRoleKey = 'full-stack-development';
  else if (haystack.includes('data') || haystack.includes('nifty') || haystack.includes('analytics')) primaryRoleKey = 'data-analytics';
  else if (haystack.includes('python') || haystack.includes('qa') || haystack.includes('playwright') || haystack.includes('ocr') || haystack.includes('bot') || haystack.includes('fastapi')) primaryRoleKey = 'python-automation';
  else if (haystack.includes('vpc') || haystack.includes('cloud') || haystack.includes('devops') || haystack.includes('docker')) primaryRoleKey = 'devops-cloud';
  else if (haystack.includes('security') || haystack.includes('owasp') || haystack.includes('oauth')) primaryRoleKey = 'cybersecurity';
  else if (haystack.includes('ui') || haystack.includes('ux') || haystack.includes('design')) primaryRoleKey = 'ui-ux-design';
  else if (haystack.includes('mobile') || haystack.includes('flutter') || haystack.includes('android')) primaryRoleKey = 'mobile-app-development';
  else if (haystack.includes('ml') || haystack.includes('machine-learning') || haystack.includes('rag')) primaryRoleKey = 'machine-learning';
  else if (haystack.includes('marketing') || haystack.includes('seo') || haystack.includes('equity') || haystack.includes('startup')) primaryRoleKey = 'digital-marketing';

  const nonRemoteCities = Object.values(GEO_CITIES).filter((c) => c.slug !== 'remote');
  const h = hashSlug(slug);
  const rotatedCities = Array.from({ length: 4 }, (_, idx) => nonRemoteCities[(h + idx * 3) % nonRemoteCities.length]);

  const roleList = Object.values(GEO_ROLES);
  const recentPublications = (publishedArticles as Array<{ slug: string; title: string; author: string; domain: string; certId?: string }>)
    .filter((a) => a.slug !== slug && a.title && a.certId)
    .slice(0, 3);

  return {
    primaryRole: GEO_ROLES[primaryRoleKey] || roleList[0],
    allRoles: roleList,
    rotatedCities,
    recentPublications,
  };
}

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
        <article className={`${s.postBody} ${s.mdxContent}`}>
          {markdownBody ? (
            <StandardMarkdownRenderer
              content={markdownBody}
              titleToStrip={meta.title}
            />
          ) : (
            <p className="body-copy">Article content unavailable.</p>
          )}
        </article>

        {meta.faqs && meta.faqs.length > 0 && (
          <div style={{ marginTop: '2.5rem' }}>
            <Faq items={meta.faqs} heading="Frequently Asked Questions" id="blog-faq" />
          </div>
        )}

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
              <h2 style={{ color: '#fff', fontSize: '1.05rem', margin: '0 0 0.5rem', fontWeight: 700 }}>
                Build Production Systems
              </h2>
              <p style={{ color: '#94A3B8', fontSize: '0.8125rem', lineHeight: '1.5', margin: '0 0 1rem' }}>
                Join the next cohort, receive 1:1 mentorship from industry staff, and publish verified capstone case studies.
              </p>
              <TrackedLink
                href="/enroll/1999"
                eventName="blog_cta_click"
                eventParams={{ slug: meta.slug, destination: '/enroll/1999', label: 'apply_fellowship' }}
                style={{ color: '#E2B96F', fontSize: '0.8125rem', fontWeight: 700, textDecoration: 'none', display: 'inline-flex', alignItems: 'center', gap: '0.3rem' }}
              >
                Apply for Fellowship &rarr;
              </TrackedLink>
            </div>

            <div style={{ background: 'rgba(255, 255, 255, 0.03)', border: '1px solid rgba(255, 255, 255, 0.08)', borderRadius: '12px', padding: '1.25rem' }}>
              <div style={{ color: '#34D399', fontSize: '0.75rem', fontWeight: 800, textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: '0.35rem' }}>
                For Tech Recruiters &amp; Employers
              </div>
              <h2 style={{ color: '#fff', fontSize: '1.05rem', margin: '0 0 0.5rem', fontWeight: 700 }}>
                Hire Pre-Vetted Fellows
              </h2>
              <p style={{ color: '#94A3B8', fontSize: '0.8125rem', lineHeight: '1.5', margin: '0 0 1rem' }}>
                Discover engineers with verified code rubrics, live deployment URLs, and zero recruiter markup fees.
              </p>
              <TrackedLink
                href="/verify/directory"
                eventName="blog_cta_click"
                eventParams={{ slug: meta.slug, destination: '/verify/directory', label: 'browse_directory' }}
                style={{ color: '#34D399', fontSize: '0.8125rem', fontWeight: 700, textDecoration: 'none', display: 'inline-flex', alignItems: 'center', gap: '0.3rem' }}
              >
                Browse Pre-Vetted Directory &rarr;
              </TrackedLink>
            </div>
          </div>
        </div>

        {/* ── 9-Domain Remote Courses, Regional Internships & Intern Publications Mesh ── */}
        {(() => {
          const mesh = pickGeoLinksForSlug(meta.slug, meta.tags || [], dynamicPost?.domain);
          return (
            <section
              aria-label="Remote Courses and Regional Internship Hubs"
              style={{
                background: 'rgba(15, 23, 42, 0.85)',
                border: '1px solid rgba(56, 189, 248, 0.22)',
                borderRadius: '16px',
                padding: '1.5rem',
                marginTop: '2rem',
              }}
            >
              <div style={{ color: '#38BDF8', fontSize: '0.78rem', fontWeight: 800, textTransform: 'uppercase', letterSpacing: '0.07em', marginBottom: '0.65rem' }}>
                Remote Online Courses &amp; Hosted Internship Tracks (All 9+ Domains)
              </div>
              <p style={{ color: '#CBD5E1', fontSize: '0.88rem', lineHeight: 1.6, margin: '0 0 1rem' }}>
                Looking for a structured remote online course with a live production internship? Explore our remote tracks and regional tech hubs:
              </p>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem', marginBottom: '1.15rem' }}>
                {mesh.allRoles.map((role) => (
                  <TrackedLink
                    key={role.slug}
                    href={`/learners/courses/${role.slug}`}
                    eventName="blog_ecosystem_link_click"
                    eventParams={{ slug: meta.slug, targetType: 'remote_course', domain: role.slug }}
                    style={{
                      fontSize: '0.78rem',
                      padding: '0.35rem 0.7rem',
                      borderRadius: '999px',
                      background: 'rgba(56, 189, 248, 0.1)',
                      border: '1px solid rgba(56, 189, 248, 0.25)',
                      color: '#E2E8F0',
                      textDecoration: 'none',
                    }}
                  >
                    {role.title} Course
                  </TrackedLink>
                ))}
              </div>

              <div style={{ borderTop: '1px solid rgba(255,255,255,0.08)', paddingTop: '1rem', marginBottom: '1rem' }}>
                <div style={{ color: '#94A3B8', fontSize: '0.76rem', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: '0.5rem' }}>
                  {mesh.primaryRole.title} — Remote &amp; City Internship Hubs
                </div>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.65rem 1.1rem', fontSize: '0.84rem' }}>
                  <TrackedLink
                    href={`/internships/${mesh.primaryRole.slug}/remote`}
                    eventName="blog_ecosystem_link_click"
                    eventParams={{ slug: meta.slug, targetType: 'geo_internship', city: 'remote', domain: mesh.primaryRole.slug }}
                    style={{ color: '#38BDF8', textDecoration: 'underline' }}
                  >
                    Remote / Work From Home →
                  </TrackedLink>
                  {mesh.rotatedCities.map((city) => (
                    <TrackedLink
                      key={city.slug}
                      href={`/internships/${mesh.primaryRole.slug}/${city.slug}`}
                      eventName="blog_ecosystem_link_click"
                      eventParams={{ slug: meta.slug, targetType: 'geo_internship', city: city.slug, domain: mesh.primaryRole.slug }}
                      style={{ color: '#93C5FD', textDecoration: 'underline' }}
                    >
                      {city.name} →
                    </TrackedLink>
                  ))}
                </div>
              </div>

              {mesh.recentPublications.length > 0 && (
                <div style={{ borderTop: '1px solid rgba(255,255,255,0.08)', paddingTop: '1rem' }}>
                  <div style={{ color: '#E2B96F', fontSize: '0.76rem', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: '0.5rem' }}>
                    Verified Intern-Published Case Studies
                  </div>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '0.45rem', fontSize: '0.84rem' }}>
                    {mesh.recentPublications.map((pub) => (
                      <div key={pub.slug} style={{ color: '#CBD5E1' }}>
                        <TrackedLink
                          href={`/blog/${pub.slug}`}
                          eventName="blog_ecosystem_link_click"
                          eventParams={{ slug: meta.slug, targetType: 'intern_publication', targetSlug: pub.slug }}
                          style={{ color: '#F8FAFC', textDecoration: 'underline', fontWeight: 600 }}
                        >
                          {pub.title}
                        </TrackedLink>{' '}
                        <span style={{ color: '#94A3B8' }}>
                          — {pub.author} ({pub.domain} ·{' '}
                          <Link href={`/verify/${pub.certId}`} style={{ color: '#34D399', textDecoration: 'underline' }}>
                            {pub.certId}
                          </Link>
                          )
                        </span>
                      </div>
                    ))}
                    <div style={{ marginTop: '0.25rem' }}>
                      <Link href="/fellows/verified" style={{ color: '#E2B96F', fontSize: '0.82rem', fontWeight: 700, textDecoration: 'none' }}>
                        Explore 135+ Verified Fellows &amp; Publications &rarr;
                      </Link>
                    </div>
                  </div>
                </div>
              )}
            </section>
          );
        })()}

        <div className={s.postFoot}>
          <Link href="/blog" className="accent-note">
            &larr; Back to AI Engineering Blog Index
          </Link>
        </div>
      </div>
    </div>
  );
}
