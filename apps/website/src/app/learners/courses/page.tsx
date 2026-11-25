import React from 'react';
import Link from 'next/link';
import { pageMetadata } from '@/lib/seo';
import HandNote from '@/components/ui/HandNote';
import s from '../learners.module.css';
import Reveal from '@/components/ui/Reveal';
import CoursesCatalogueClient from '@/components/courses/CoursesCatalogueClient';
import { getPublishedTracks, FELLOWSHIP_FEE } from '@/data/courses.config';

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

        {/* Live Regional Opportunities Discovery Hub */}
        <div className="card p-6 bg-card border border-line mt-12 mb-8">
          <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-6">
            <div>
              <span className="doclabel text-xs">§ 02 — LIVE SPRINT DISCOVERY PORTAL</span>
              <h2 className="text-xl font-bold font-mono text-white mt-1">
                Explore Live Industry Internships &amp; Placements
              </h2>
              <p className="text-xs text-muted max-w-2xl mt-1">
                Looking for immediate hands-on startup sprints with 100% Guaranteed Production Internship with Dedicated Placement Assistance across internal DBERT ventures or verified hiring partners? Our live portal matches candidates across Mumbai, Bengaluru, Delhi NCR, Pune, and remote teams.
              </p>
            </div>
            <a
              href="https://lms.dbert.in/"
              target="_blank"
              rel="noopener noreferrer"
              className="btn btn-primary text-xs shrink-0"
            >
              Launch Internship Portal ↗
            </a>
          </div>

          <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4 pt-4 border-t border-line">
            <a
              href="https://lms.dbert.in/internships/full-stack-development"
              target="_blank"
              rel="noopener noreferrer"
              className="p-3 bg-[var(--surface-base)] border border-line rounded hover:border-accent transition-colors block text-left"
            >
              <div className="text-xs font-mono text-accent font-semibold mb-1">Full Stack AI Track ↗</div>
              <div className="text-[11px] text-muted">Mumbai, Bengaluru, Remote Sprints</div>
            </a>
            <a
              href="https://lms.dbert.in/internships/data-analyst"
              target="_blank"
              rel="noopener noreferrer"
              className="p-3 bg-[var(--surface-base)] border border-line rounded hover:border-accent transition-colors block text-left"
            >
              <div className="text-xs font-mono text-accent font-semibold mb-1">Data Analytics Track ↗</div>
              <div className="text-[11px] text-muted">SQL, Power BI, Corporate Reporting</div>
            </a>
            <a
              href="https://lms.dbert.in/internships/python-automation"
              target="_blank"
              rel="noopener noreferrer"
              className="p-3 bg-[var(--surface-base)] border border-line rounded hover:border-accent transition-colors block text-left"
            >
              <div className="text-xs font-mono text-accent font-semibold mb-1">Python Automation Track ↗</div>
              <div className="text-[11px] text-muted">Scraping, QA Testing, Orchestration</div>
            </a>
            <a
              href="https://lms.dbert.in/internships/ai-agent-development"
              target="_blank"
              rel="noopener noreferrer"
              className="p-3 bg-[var(--surface-base)] border border-line rounded hover:border-accent transition-colors block text-left"
            >
              <div className="text-xs font-mono text-accent font-semibold mb-1">AI Agent Systems Track ↗</div>
              <div className="text-[11px] text-muted">LangGraph, RAG, Swarms, vLLM</div>
            </a>
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
