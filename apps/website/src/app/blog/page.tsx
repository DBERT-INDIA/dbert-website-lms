import React from 'react';
import Link from 'next/link';
import { pageMetadata } from '@/lib/seo';
import { getAllPosts } from '@/lib/blog';
import HandNote from '@/components/ui/HandNote';
import s from './blog.module.css';

import BlogClientView from '@/components/blog/BlogClientView';

export const metadata = pageMetadata('/blog');

export default function BlogIndexPage() {
  const articles = getAllPosts();

  return (
    <div className="container pad-block">
      <div className="mb-lg">
        <div className="doclabel">
          § 01 — TECHNICAL INSIGHTS &amp; RESEARCH <span className="rev">rev: 2026.2</span>
        </div>
        <div className="stack-h align-baseline gap-3 flex-wrap">
          <h1>AI Engineering Blog India</h1>
          <HandNote tone="amber">
            benchmarks &amp; architectures ✍
          </HandNote>
        </div>
        <p className="body-copy">
          Verified research notes, implementation workflows, architectural diagrams, and Indian AI engineering benchmarks published directly by DBERT Labs staff.
        </p>
      </div>

      <BlogClientView initialArticles={articles} />
    </div>
  );
}

