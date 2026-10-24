import React from 'react';
import Link from 'next/link';
import { pageMetadata } from '@/lib/seo';
import { getAllPosts } from '@/lib/blog';
import HandNote from '@/components/ui/HandNote';
import StudioConsole, { type FeedLine } from '@/components/ui/StudioConsole';
import FactTicker from '@/components/ui/FactTicker';
import s from './blog.module.css';

import BlogClientView from '@/components/blog/BlogClientView';

export const metadata = pageMetadata('/blog');

export default function BlogIndexPage() {
  const articles = getAllPosts();

  const blogTelemetryFeed: FeedLine[] = [
    {
      time: '09:15:30',
      tag: 'commit',
      message: 'fast-vs-safe-agreement-india.mdx published',
      detail: '· 2,340 words · MCA governance matrix',
    },
    {
      time: '09:22:18',
      tag: 'infer',
      message: 'cloud-llm-vs-private-vpc-costs.mdx verified',
      detail: '· 2,180 words · vLLM unit economics',
    },
    {
      time: '09:30:45',
      tag: 'deploy',
      message: 'ai-agent-frameworks-comparison.mdx live',
      detail: '· 2,410 words · LangGraph vs AutoGen',
    },
    {
      time: '09:44:12',
      tag: 'verify',
      message: 'Google AdSense & AdX crawler audit passed',
      detail: '· ads.txt & sitemap.xml verified',
    },
    {
      time: '09:51:00',
      tag: 'audit',
      message: 'Technical peer review completed for sprint 14 briefings',
      detail: '· 3 author signatures',
    },
  ];

  const blogFacts = [
    'in-depth architectural breakdowns',
    'zero AI-generated fluff or buzzwords',
    'empirical latency & compute cost spreadsheets',
    'Indian corporate governance & legal term sheets',
    'reproducible production code samples',
    'written directly by Delhi NCR practicing engineers',
  ];

  return (
    <>
      {/* ══════════ SECTION 1: HERO (2-COLUMN GRID) ══════════ */}
      <section className="section-subpage-hero">
        <div className="wrap subpage-hero-grid">
          <div>
            <div className="doclabel">
              § 01 — TECHNICAL INSIGHTS &amp; RESEARCH <span className="rev">rev: 2026.2</span>
            </div>
            <h1 className="relative inline-block">
              AI Engineering Blog India
              <HandNote className="absolute -right-12 -top-6 text-lg hidden md:block" tone="amber">
                benchmarks ✍
              </HandNote>
            </h1>
            <p className="intro-copy">
              Verified research notes, implementation workflows, architectural diagrams, and Indian AI engineering benchmarks published directly by DBERT Labs staff.
            </p>
          </div>

          <div>
            <StudioConsole
              title="dbert-editorial · engineering briefings telemetry"
              lines={blogTelemetryFeed}
              footLeft="peer-reviewed engineering publications"
              footRight="● 3 deep-dive architectural pillars"
            />
          </div>
        </div>
      </section>

      {/* ══════════ SECTION 2: FULL-BLEED AMBIENT FACT TICKER ══════════ */}
      <div className="section-ticker-ribbon">
        <FactTicker facts={blogFacts} />
      </div>

      {/* ══════════ SECTION 3: ARCHIVE & CASE STUDIES ══════════ */}
      <section className="subpage-section">
        <div className="wrap">
          <div className="section-head-sub">
            <div className="doclabel">§ 02 — ARCHIVE &amp; CASE STUDIES</div>
            <h2>Engineering Publications &amp; Benchmarks</h2>
            <p>In-depth architectural analysis across legal frameworks, sovereign VPC cost models, and multi-agent systems.</p>
          </div>
          <BlogClientView initialArticles={articles} />
        </div>
      </section>
    </>
  );
}

