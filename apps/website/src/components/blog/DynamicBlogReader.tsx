'use client';

import React, { useEffect, useState, useTransition } from 'react';
import Link from 'next/link';
import { useSearchParams } from 'next/navigation';
import AuthorBox from '@/components/blog/AuthorBox';
import HandNote from '@/components/ui/HandNote';
import AdSenseSlot from '@/components/ads/AdSenseSlot';
import s from '@/app/blog/blog.module.css';

interface DynamicPost {
  id: number;
  slug: string;
  title: string;
  desc: string;
  domain: string;
  author: string;
  authorRole: string;
  authorBio: string;
  date: string;
  readTime: string;
  tags: string[];
  canonicalUrl: string;
  content_markdown: string;
}

function parseMarkdownBlocks(md: string) {
  if (!md) return null;
  const sections = md.split(/\n\s*\n/);
  return sections.map((sec, idx) => {
    const trimmed = sec.trim();
    if (trimmed.startsWith('### ')) {
      return <h3 key={idx} style={{ marginTop: '28px', marginBottom: '12px' }}>{trimmed.replace('### ', '')}</h3>;
    }
    if (trimmed.startsWith('## ')) {
      return <h2 key={idx} style={{ marginTop: '36px', marginBottom: '14px', borderBottom: '1px solid rgba(255,255,255,0.08)', paddingBottom: '8px' }}>{trimmed.replace('## ', '')}</h2>;
    }
    if (trimmed.startsWith('# ')) {
      return <h1 key={idx} style={{ marginTop: '40px', marginBottom: '16px' }}>{trimmed.replace('# ', '')}</h1>;
    }
    if (trimmed.startsWith('```')) {
      const codeLines = trimmed.replace(/^```[a-z0-9_-]*\n/i, '').replace(/```$/, '');
      return (
        <pre key={idx} style={{ background: '#030712', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px', padding: '16px', overflowX: 'auto', margin: '20px 0', fontSize: '13px', color: '#38bdf8' }}>
          <code>{codeLines}</code>
        </pre>
      );
    }
    if (trimmed.startsWith('- ') || trimmed.startsWith('* ')) {
      const items = trimmed.split('\n').filter(Boolean);
      return (
        <ul key={idx} style={{ margin: '16px 0 20px 24px', padding: 0 }}>
          {items.map((item, i) => {
            const raw = item.replace(/^[-*]\s+/, '');
            const parts = raw.split(/(\*\*[^*]+\*\*|`[^`]+`)/g);
            return (
              <li key={i} style={{ marginBottom: '8px' }}>
                {parts.map((part, pIdx) => {
                  if (part.startsWith('**') && part.endsWith('**')) {
                    return <strong key={pIdx} style={{ color: '#fff' }}>{part.slice(2, -2)}</strong>;
                  }
                  if (part.startsWith('`') && part.endsWith('`')) {
                    return <code key={pIdx} style={{ background: 'rgba(255,255,255,0.08)', padding: '2px 6px', borderRadius: '4px', fontSize: '13px' }}>{part.slice(1, -1)}</code>;
                  }
                  return part;
                })}
              </li>
            );
          })}
        </ul>
      );
    }
    const parts = trimmed.split(/(\*\*[^*]+\*\*|`[^`]+`)/g);
    return (
      <p key={idx} className="body-copy" style={{ marginBottom: '18px', lineHeight: '1.8' }}>
        {parts.map((part, pIdx) => {
          if (part.startsWith('**') && part.endsWith('**')) {
            return <strong key={pIdx} style={{ color: '#fff' }}>{part.slice(2, -2)}</strong>;
          }
          if (part.startsWith('`') && part.endsWith('`')) {
            return <code key={pIdx} style={{ background: 'rgba(255,255,255,0.08)', padding: '2px 6px', borderRadius: '4px', fontSize: '13px' }}>{part.slice(1, -1)}</code>;
          }
          return part;
        })}
      </p>
    );
  });
}

export default function DynamicBlogReader() {
  const searchParams = useSearchParams();
  const [post, setPost] = useState<DynamicPost | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let slug = searchParams.get('slug');
    if (!slug && typeof window !== 'undefined') {
      const match = window.location.pathname.match(/\/blog\/([^/?#]+)/);
      if (match && match[1] && match[1] !== 'reader') {
        slug = match[1];
      }
    }

    if (!slug) {
      setError('No article specified.');
      setLoading(false);
      return;
    }

    let isMounted = true;
    async function fetchPost() {
      try {
        const res = await fetch(`https://internship.dbert.online/api/public/blog-posts/${slug}`);
        if (!res.ok) {
          if (isMounted) setError('Technical publication not found.');
          return;
        }
        const data = await res.json();
        if (data.status === 'success' && data.post) {
          if (isMounted) setPost(data.post);
        } else {
          if (isMounted) setError('Article data unavailable.');
        }
      } catch (e) {
        if (isMounted) setError('Could not connect to live publication service.');
      } finally {
        if (isMounted) setLoading(false);
      }
    }
    fetchPost();
    return () => {
      isMounted = false;
    };
  }, [searchParams]);

  if (loading) {
    return (
      <div className="container pad-block" style={{ minHeight: '60vh', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <div style={{ textAlign: 'center' }}>
          <div style={{ fontSize: '24px', color: 'var(--brand)', marginBottom: '12px' }}>
            <i className="fas fa-spinner fa-spin"></i>
          </div>
          <p className="body-copy">Loading technical article from DBERT Engineering Network...</p>
        </div>
      </div>
    );
  }

  if (error || !post) {
    return (
      <div className="container pad-block" style={{ minHeight: '60vh' }}>
        <div className="card text-center p-8 my-6" style={{ maxWidth: '600px', margin: '40px auto' }}>
          <h2>Insight Not Found</h2>
          <p className="body-copy my-4">{error || 'The requested technical insight could not be found.'}</p>
          <Link href="/blog" className="btn btn-primary btn-sm">
            &larr; Back to AI Engineering Blog Index
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="container pad-block">
      <div className="measure">
        <div className={s.postHead}>
          <div className="stack-h justify-between align-center mb-2">
            <span className={s.readTime}>{post.readTime}</span>
            <time dateTime={post.date} className="faint-label">
              {post.date}
            </time>
          </div>
          <h1 className={s.postTitle}>{post.title}</h1>
          <p className={s.postDesc}>{post.desc}</p>
          <div className="stack-h justify-between align-center flex-wrap gap-3">
            <div className={s.tagWrap}>
              {post.tags && post.tags.map((tag, i) => (
                <span key={i} className="tag-chip">
                  #{tag}
                </span>
              ))}
            </div>
            <HandNote tone="blue">verified lab benchmark ✎</HandNote>
          </div>
        </div>

        <article className={`card ${s.postBody} ${s.mdxContent}`}>
          {parseMarkdownBlocks(post.content_markdown)}
        </article>

        <AdSenseSlot slotId="blog-post-bottom" />

        <AuthorBox
          name={post.author}
          role={post.authorRole}
          bio={post.authorBio}
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
