'use client';

import React, { useState, useMemo } from 'react';
import Link from 'next/link';
import { Search } from 'lucide-react';
import type { BlogPostMeta } from '@/lib/blog';
import s from '@/app/blog/blog.module.css';

interface BlogClientViewProps {
  initialArticles: BlogPostMeta[];
}

export default function BlogClientView({ initialArticles }: BlogClientViewProps) {
  const [articles, setArticles] = useState<BlogPostMeta[]>(initialArticles);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedTag, setSelectedTag] = useState<string>('all');
  const [isLiveSynced, setIsLiveSynced] = useState(false);

  React.useEffect(() => {
    let isMounted = true;
    async function syncDynamicArticles() {
      try {
        const res = await fetch('https://lms.dbert.in/api/public/blog-posts', {
          headers: { 'Accept': 'application/json' },
        });
        if (!res.ok) return;
        const data = await res.json();
        if (data.status === 'success' && Array.isArray(data.posts) && data.posts.length > 0) {
          if (!isMounted) return;
          setArticles((prev) => {
            const existingSlugs = new Set(prev.map((a) => a.slug));
            const newPosts: BlogPostMeta[] = [];
            data.posts.forEach((p: any) => {
              if (!existingSlugs.has(p.slug)) {
                newPosts.push({
                  slug: p.slug,
                  title: p.title,
                  desc: p.desc || '',
                  readTime: p.readTime || '5 min read',
                  date: p.date || new Date().toISOString().split('T')[0],
                  author: p.author || 'DBERT Fellow',
                  authorRole: p.authorRole || 'Engineering Contributor',
                  authorBio: 'Technical publication by DBERT engineering contributor.',
                  tags: Array.isArray(p.tags) ? p.tags : ['Engineering'],
                  canonicalUrl: p.canonicalUrl,
                });
              }
            });
            if (newPosts.length === 0) return prev;
            setIsLiveSynced(true);
            return [...newPosts, ...prev];
          });
        }
      } catch (err) {
        // Fallback silently to pre-rendered articles
      }
    }
    syncDynamicArticles();
    return () => {
      isMounted = false;
    };
  }, []);

  const allTags = useMemo(() => {
    const tagsSet = new Set<string>();
    articles.forEach((art) => {
      art.tags?.forEach((t) => tagsSet.add(t));
    });
    return Array.from(tagsSet);
  }, [articles]);

  const filteredArticles = useMemo(() => {
    return articles.filter((art) => {
      const matchesSearch =
        searchQuery === '' ||
        art.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        art.desc.toLowerCase().includes(searchQuery.toLowerCase());

      const matchesTag =
        selectedTag === 'all' || (art.tags && art.tags.includes(selectedTag));

      return matchesSearch && matchesTag;
    });
  }, [articles, searchQuery, selectedTag]);

  const featuredArticle = articles[0];

  return (
    <div>
      {/* Featured Insight Card */}
      {featuredArticle && searchQuery === '' && selectedTag === 'all' && (
        <div className="section-breath border-t border-line">
          <div className="doclabel mb-2">§ 02 — FEATURED RESEARCH PAPER</div>
          <div className="card card-lift my-4">
            <div className="stack-h justify-between align-center mb-2 flex-wrap gap-2">
              <span className="tag-chip">Featured Publication</span>
              <span className={s.readTime}>{featuredArticle.readTime} &bull; {featuredArticle.date}</span>
            </div>
            <h2 className="my-2">
              <Link href={`/blog/${featuredArticle.slug}`}>
                {featuredArticle.title}
              </Link>
            </h2>
            <p className="body-copy max-w-3xl my-3">{featuredArticle.desc}</p>
            <div className="stack-h justify-between align-center mt-4 pt-3 border-t border-line flex-wrap gap-2">
              <div className={s.tagWrap}>
                {featuredArticle.tags.slice(0, 4).map((tag, i) => (
                  <span key={i} className="tag-chip">
                    #{tag}
                  </span>
                ))}
              </div>
              <Link href={`/blog/${featuredArticle.slug}`} className="btn btn-primary btn-sm">
                Read Publication &rarr;
              </Link>
            </div>
          </div>
        </div>
      )}

      {/* Filter and Search Bar */}
      <div className="section-breath border-t border-line">
        <div className="stack-h justify-between align-center flex-wrap gap-4 mb-6">
          <div>
            <div className="doclabel mb-1">§ 03 — ARCHIVES &amp; ARTICLES</div>
            <h2>All Technical Insights</h2>
          </div>

          {/* Search Box */}
          <div className={s.searchWrap}>
            <Search
              size={16}
              className={s.searchIcon}
            />
            <input
              type="text"
              placeholder="Search research & guides..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className={s.searchInput}
            />
          </div>
        </div>

        {/* Tag Filters */}
        {allTags.length > 0 && (
          <div className="stack-h gap-2 flex-wrap mb-6">
            <button
              type="button"
              onClick={() => setSelectedTag('all')}
              className={`tag-chip ${s.filterBtn} ${selectedTag === 'all' ? s.filterBtnActive : ''}`}
            >
              All Topics ({articles.length})
            </button>
            {allTags.map((tag) => (
              <button
                key={tag}
                type="button"
                onClick={() => setSelectedTag(tag === selectedTag ? 'all' : tag)}
                className={`tag-chip ${s.filterBtn} ${selectedTag === tag ? s.filterBtnActive : ''}`}
              >
                #{tag}
              </button>
            ))}
          </div>
        )}

        {/* Article Grid */}
        {filteredArticles.length === 0 ? (
          <div className="card text-center p-8 my-6">
            <p className="body-copy">No articles found matching &quot;{searchQuery}&quot;.</p>
            <button
              type="button"
              onClick={() => {
                setSearchQuery('');
                setSelectedTag('all');
              }}
              className="btn btn-outline btn-sm mt-3"
            >
              Reset Filters
            </button>
          </div>
        ) : (
          <div className={`${s.indexGrid} stagger-grid`}>
            {filteredArticles.map((art) => (
              <div key={art.slug} className="card card-lift stack-between">
                <div>
                  <div className="stack-h justify-between align-center mb-2">
                    <span className={s.readTime}>{art.readTime}</span>
                    <time dateTime={art.date} className="faint-label">{art.date}</time>
                  </div>
                  <h3 className={s.cardTitle}>
                    <Link href={`/blog/${art.slug}`}>
                      {art.title}
                    </Link>
                  </h3>
                  <p className="body-copy mb-4 text-xs text-muted">{art.desc}</p>
                  <div className={s.tagWrap}>
                    {art.tags.slice(0, 3).map((tag, i) => (
                      <span key={i} className="tag-chip">
                        #{tag}
                      </span>
                    ))}
                  </div>
                </div>
                <Link href={`/blog/${art.slug}`} className="accent-label mt-4">
                  Read Technical Guide &rarr;
                </Link>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
