import React from 'react';
import Link from 'next/link';
import { pageMetadata } from '@/lib/seo';
import HandNote from '@/components/ui/HandNote';
import s from '../learners.module.css';
import Reveal from '@/components/ui/Reveal';
import CoursesCatalogueClient from '@/components/courses/CoursesCatalogueClient';
import { getPublishedTracks, FELLOWSHIP_FEE } from '@/data/courses.config';
import { GEO_CITIES } from '@/data/geo_domains.config';

export const metadata = pageMetadata('/learners/courses');

const publishedTracks = getPublishedTracks();

const jsonLd = {
  '@context': 'https://schema.org',
  '@graph': [
    {
      '@type': 'ItemList',
      name: 'DBERT Production AI & Engineering Fellowship Tracks',
      itemListElement: publishedTracks.map((track, idx) => ({
        '@type': 'Course',
        position: idx + 1,
        name: track.name,
        description: track.shortDescription,
        url: `https://dbert.in${track.canonicalPath}`,
        provider: { '@type': 'Organization', name: 'DBERT', url: 'https://dbert.in' },
      })),
    },
  ],
};

export default function CoursesHubPage() {
  return (
    <section className="section">
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />
      <div className="wrap">
        <Reveal className="section-head">
          <div className="doclabel">
            § 01 — COURSES <span className="rev">11 fellowship tracks</span>
          </div>
          <div className="stack-h align-baseline gap-3 flex-wrap">
            <h1>AI and engineering fellowship tracks with verifiable credentials</h1>
            <HandNote tone="amber">
              production code · real pull requests ✍
            </HandNote>
          </div>
          <p className="body-copy">
            Eleven focused technical tracks built around production engineering practices ({FELLOWSHIP_FEE.formattedTotal} total program fee · 2 months). Complete them through guided sprints, merge pull requests against real codebases, and verify your credentials on our registry. If you want the full sequence from beginner to fellowship, explore the{' '}
            <Link href="/learners" className={s.backLink}>
              career ladder
            </Link>{' '}
            first.
          </p>
        </Reveal>

        <CoursesCatalogueClient tracks={publishedTracks} formattedFee={FELLOWSHIP_FEE.formattedTotal} />

        {/* ₹1,999 Tiered Value Ladder Banner */}
        <div className="card p-6 bg-card border border-accent/40 mt-10 mb-8" style={{ background: 'linear-gradient(135deg, rgba(245,158,11,0.08), rgba(15,23,42,0.95))' }}>
          <div className="flex flex-col lg:flex-row justify-between items-start lg:items-center gap-6">
            <div>
              <span className="doclabel text-xs text-accent">₹1,999 TECHNICAL INCUBATION · 2027 COHORT</span>
              <h2 className="text-xl font-bold font-mono text-white mt-1">
                Verified Certificate &rarr; ₹5,000+ Stipend &rarr; 100% Placement Assistance
              </h2>
              <p className="text-xs text-[var(--text-secondary)] max-w-2xl mt-2 leading-relaxed">
                Every track shares the same transparent {FELLOWSHIP_FEE.formattedTotal} total program fee (2 months, 1:1 PR code reviews, Turnitin-verified 3-doc credential packet, Gate 1 stipend eligibility, and Round-1 hiring waivers). Already paid the ₹499 caution deposit? Your deposit is credited in full — only {FELLOWSHIP_FEE.formattedBalance} balance due.
              </p>
            </div>
            <div className="flex flex-wrap gap-3 shrink-0">
              <Link href="/enroll/1999" className="btn btn-primary text-xs">
                Complete Enrollment — {FELLOWSHIP_FEE.formattedTotal} &rarr;
              </Link>
              <Link href="/verify/directory" className="btn btn-outline text-xs">
                Inspect Verified Alumni
              </Link>
            </div>
          </div>
        </div>

        {/* Multi-City Target Hubs Strip */}
        <div className="card p-6 bg-card border border-line mt-8 mb-8">
          <div className="doclabel text-xs mb-2">§ 01B — MULTI-CITY SPRINT HUBS (18 TECH CORRIDORS)</div>
          <h2 className="text-lg font-bold font-mono text-white mb-2">
            Explore Courses &amp; Internships Across 18 Indian Tech Hubs
          </h2>
          <p className="text-xs text-muted mb-4">
            Every track operates 100% remotely and pairs with regional hiring hubs across India:
          </p>
          <div className="flex flex-wrap gap-2">
            {Object.values(GEO_CITIES).map((city) => (
              <Link
                key={city.slug}
                href={`/internships/${city.slug}`}
                className="tag-chip text-xs font-mono hover:border-accent hover:text-accent transition-colors"
              >
                📍 {city.name}
              </Link>
            ))}
          </div>
        </div>

        {/* Live Regional Opportunities Discovery Hub */}
        <div className="card p-6 bg-card border border-line mt-12 mb-8">
          <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-6">
            <div>
              <span className="doclabel text-xs">§ 02 — LIVE SPRINT DISCOVERY &amp; ENROLLMENT</span>
              <h2 className="text-xl font-bold font-mono text-white mt-1">
                Explore Domain Tracks Across Remote &amp; Metro Hubs
              </h2>
              <p className="text-xs text-muted max-w-2xl mt-1">
                Ready for hands-on production sprints with 100% Guaranteed Production Internship and Dedicated Placement Assistance across internal DBERT ventures or partner teams? Select your remote track or enroll directly for ₹1,999.
              </p>
            </div>
            <Link
              href="/enroll/1999"
              className="btn btn-primary text-xs shrink-0"
            >
              Confirm Fellowship Seat — ₹1,999 &rarr;
            </Link>
          </div>

          <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4 pt-4 border-t border-line">
            <Link
              href="/learners/courses/full-stack-development/remote"
              className="p-3 bg-[var(--surface-base)] border border-line rounded hover:border-accent transition-colors block text-left"
            >
              <div className="text-xs font-mono text-accent font-semibold mb-1">Full Stack Remote Track &rarr;</div>
              <div className="text-[11px] text-muted">Mumbai, Bengaluru, Remote Sprints</div>
            </Link>
            <Link
              href="/learners/courses/data-analytics/remote"
              className="p-3 bg-[var(--surface-base)] border border-line rounded hover:border-accent transition-colors block text-left"
            >
              <div className="text-xs font-mono text-accent font-semibold mb-1">Data Analytics Track &rarr;</div>
              <div className="text-[11px] text-muted">Excel, SQL, Python, Power BI</div>
            </Link>
            <Link
              href="/learners/courses/python-automation/remote"
              className="p-3 bg-[var(--surface-base)] border border-line rounded hover:border-accent transition-colors block text-left"
            >
              <div className="text-xs font-mono text-accent font-semibold mb-1">Python Automation Track &rarr;</div>
              <div className="text-[11px] text-muted">Playwright, QA, Bots &amp; OCR</div>
            </Link>
            <Link
              href="/learners/courses/ai-agent-development/remote"
              className="p-3 bg-[var(--surface-base)] border border-line rounded hover:border-accent transition-colors block text-left"
            >
              <div className="text-xs font-mono text-accent font-semibold mb-1">AI Agent Systems Track &rarr;</div>
              <div className="text-[11px] text-muted">LangGraph, RAG, Swarms, vLLM</div>
            </Link>
          </div>
        </div>

        <Reveal className="hub-cta-row text-center mt-10">
          <Link href="/learners" className="btn btn-outline">
            &larr; Return to Progressive Career Ladder
          </Link>
        </Reveal>
      </div>
    </section>
  );
}
