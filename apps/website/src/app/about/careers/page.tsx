import React from 'react';
import Link from 'next/link';
import { pageMetadata } from '@/lib/seo';
import { Briefcase, Sparkles, ArrowRight } from 'lucide-react';
import styles from '../about.module.css';


export const metadata = pageMetadata('/about/careers');

export default function CareersPage() {
  return (
    <div className="container pad-block">
      <div className="mb-lg">
        <div className="doclabel">
          § 01 — CAREERS &amp; RECRUITMENT <span className="rev">rev: 2026.2</span>
        </div>
        <h1>Careers &amp; Hiring Cohorts</h1>
        <p>Build the future of AI education, research, and technical incubation.</p>
      </div>

      <div className={styles.centeredNarrow}>
        {/* Active Aivara Technologies Hiring Cohort Card */}
        <div className={`card card-lift ${styles.pad6} mb-6 border-accent`}>
          <div className="stack-h align-center gap-2 mb-2">
            <span className="icon-chip"><Sparkles size={18} aria-hidden="true" /></span>
            <span className="doclabel text-accent border-accent">
              NOW RECRUITING • APPLICATIONS OPEN
            </span>
          </div>
          <h2 className="card-title">Aivara Technologies Hiring Cohort (2026)</h2>
          <p className={styles.bodyMuted}>
            Join our 3-month engineering sprint across 5 specialized domains: AI Agent Development, Full Stack, Python Automation, Data Analytics, and Data Engineering/ML. Direct production repos, senior review rubrics, and placement tracks.
          </p>
          <div className="mt-4">
            <Link href="/cohorts/aivara" className="btn btn-primary inline-flex align-center gap-2">
              Apply for Cohort <ArrowRight size={16} />
            </Link>
          </div>
        </div>

        <div className={`card ${styles.pad6}`}>
          <span className="icon-chip"><Briefcase aria-hidden="true" /></span>
          <h2 className="card-title">General Talent Network</h2>
          <p className={styles.bodyMuted}>
            We are always looking for passionate AI practitioners, researchers, and technical mentors. Feel free to reach out to us with your portfolio.
          </p>
          <a href="mailto:contactus@dbert.online" className="btn btn-outline">Submit Your Portfolio</a>
        </div>
      </div>
    </div>
  );
}
