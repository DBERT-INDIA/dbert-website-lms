import React from 'react';
import Image from 'next/image';
import Link from 'next/link';
import { pageMetadata } from '@/lib/seo';
import styles from '../about.module.css';

export const metadata = pageMetadata('/about/team');

export default function TeamPage() {
  return (
    <div className="container pad-block">
      <div className="measure-lg">
        <div className="detail-header">
          <div className="doclabel">
            § 05 — ENGINEERING LEADERSHIP <span className="rev">rev: 2026.2</span>
          </div>
          <h1 className="page-title-sm">The Practitioners &amp; Architects Behind the Mission</h1>
          <p className="page-intro">
            Active software developers, research engineers, and legal compliance advisors guiding DBERT&apos;s venture incubation, sovereign AI architecture, and engineering fellowship ladders.
          </p>
        </div>

        <div className={styles.stack6}>
          <div className={`card card-lift ${styles.profile}`}>
            <div className={styles.portrait}>
              <Image src="/founder.jpg" alt="Abhinav Sharma - Founder and CTO of DBERT" fill className={styles.founderPhoto} />
            </div>
            <div>
              <span className="doclabel text-xs mb-1">§ PRINCIPAL ARCHITECT</span>
              <h2 className={styles.name}>Abhinav Sharma</h2>
              <p className={styles.role}>Founder, CTO &amp; Principal AI Architect</p>
              <p className={styles.bio}>
                Abhinav directs engineering sprints at <Link href="/labs" className="ink-link">DBERT Labs</Link> and oversees system architecture across our incubated startups. He focuses on production RAG systems, multi-agent frameworks, model quantization, and reproducible MLOps pipelines. Under his technical leadership, DBERT has open-sourced research benchmarks and deployed enterprise solutions for real-world operations.
              </p>
              <div className="stack-h gap-4 mt-4 pt-4 border-t border-line flex-wrap">
                <Link href="/labs/publications" className="accent-link text-sm font-medium">Read Technical Reports &rarr;</Link>
                <Link href="/blog" className="accent-link text-sm font-medium">Explore Engineering Articles &rarr;</Link>
                <Link href="/about/credentials" className="accent-link text-sm font-medium">View Lab Credentials &rarr;</Link>
              </div>
            </div>
          </div>

          {/* Domain Practice Leads */}
          <div className="section-breath">
            <div className="doclabel mb-2">§ 06 — CORE PRACTICE LEADS</div>
            <h2>Specialized Domain Mentors</h2>
            <p className="body-copy mb-4">
              Fellows and incubated startups work directly under senior domain leads who supervise code quality, PR reviews, and architectural milestones.
            </p>
            <div className="bento-grid-3">
              <div className="card card-lift">
                <span className="tag-chip mb-2">AI Systems</span>
                <h3 className="card-title text-base mb-1">Agent Architecture &amp; RAG</h3>
                <p className="text-xs text-muted">Directs multi-agent workflows, tool routing, fast vector embeddings, and LangChain/LlamaIndex production implementations.</p>
              </div>
              <div className="card card-lift">
                <span className="tag-chip mb-2">Full Stack</span>
                <h3 className="card-title text-base mb-1">Modern Web &amp; Distributed Systems</h3>
                <p className="text-xs text-muted">Guides Next.js 16 App Router systems, reactive UIs, PostgreSQL schemas, state machines, and high-concurrency API gates.</p>
              </div>
              <div className="card card-lift">
                <span className="tag-chip mb-2">Data &amp; Quant</span>
                <h3 className="card-title text-base mb-1">Data Pipelines &amp; Conformal ML</h3>
                <p className="text-xs text-muted">Supervises calibration layers, feature engineering, walk-forward validation gates, and compliance monitoring across financial models.</p>
              </div>
            </div>
          </div>

          <div className={`card card-lift ${styles.panel}`}>
            <div className="doclabel mb-1">§ PRACTITIONER NETWORK</div>
            <h2 className={styles.panelTitle}>Active Practitioner Mentor Network</h2>
            <p className={styles.bio}>
              DBERT maintains a selective network of practicing engineers, cloud architects, and legal compliance advisors who lead code reviews for our <Link href="/learners/fellowship" className="ink-link">Applied AI Fellows</Link> and incubated founders. Rather than theoretical lectures, candidates learn by shipping pull requests on real repositories.
            </p>
            <p className={styles.bio}>
              Mentors conduct weekly live PR reviews, system design mock sessions, and latency audits. You can also inspect the active roster of research contributors working on projects like Alkame.
            </p>
            <div className="mt-4 pt-3 border-t border-line stack-h justify-between align-center flex-wrap gap-2">
              <Link href="/startups/portfolio/alkame#team" className="accent-link text-sm font-medium">Inspect Alkame Research Contributors &rarr;</Link>
              <Link href="/labs/collaborate" className="btn btn-outline btn-sm">Join Advisor Network</Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

