import React from 'react';
import { pageMetadata } from '@/lib/seo';
import CohortBanner from '@/components/ui/CohortBanner';
import AivaraApplySection from '@/components/cohorts/AivaraApplySection';
import {
  Laptop,
  Clock,
  Banknote,
  Globe2,
  GraduationCap,
  Wifi,
  CheckCircle2,
  Code2,
  BookOpen,
} from 'lucide-react';
import styles from './aivara.module.css';

export const metadata = pageMetadata('/cohorts/aivara');

export default function AivaraCohortLandingPage() {
  return (
    <>
      <CohortBanner deadlineDate="October 15, 2026 — Applications Open" />

      <div className="container pad-block">
        {/* Header / Hero Section */}
        <div className={styles.heroSection}>
          <div className="doclabel justify-center">
            § 02 — RECRUITMENT &amp; INCUBATION SPRINT <span className="rev">cohort: 2026.aivara</span>
          </div>
          <h1>Aivara Technologies Remote Internship Cohort</h1>
          <p className="measure-sm" style={{ margin: '0 auto var(--space-6)' }}>
            A production-level technical internship designed specifically for college students and emerging developers. Build real systems, receive senior engineering code reviews, and earn performance-linked stipends from anywhere in India.
          </p>

          {/* Expandable Application Form Section */}
          <AivaraApplySection />
        </div>

        {/* 6 Key Internship Pillar Cards */}
        <div className={styles.highlightsGrid}>
          {/* 1. 100% Remote */}
          <div className={styles.highlightCard}>
            <span className="icon-chip"><Globe2 size={18} aria-hidden="true" /></span>
            <span className={styles.tagBadge}>LOCATION INDEPENDENT</span>
            <h3>100% Remote Internship</h3>
            <p>
              Work from anywhere across India. Zero relocation costs, no daily travel, and no fixed office commutes. All squad pairing and code evaluations happen asynchronously online.
            </p>
          </div>

          {/* 2. Flexible Working Hours */}
          <div className={styles.highlightCard}>
            <span className="icon-chip"><Clock size={18} aria-hidden="true" /></span>
            <span className={styles.tagBadge}>SELF-PACED SPRINTS</span>
            <h3>Flexible Working Hours</h3>
            <p>
              Coordinate tasks around your daily college schedule, university lectures, and lab practicals. Deliver against weekly milestone goals rather than clocking rigid desk hours.
            </p>
          </div>

          {/* 3. Earning Opportunity up to 22k */}
          <div className={styles.highlightCard}>
            <span className="icon-chip"><Banknote size={18} aria-hidden="true" /></span>
            <span className={styles.tagBadge}>PERFORMANCE STIPEND</span>
            <h3>Earning Opportunity up to ₹22,000</h3>
            <p>
              Get paid for verified shipping velocity and code quality. Eligible interns unlock milestone-based performance stipends ranging up to ₹22,000 based on sprint outputs.
            </p>
          </div>

          {/* 4. Best for College Students */}
          <div className={styles.highlightCard}>
            <span className="icon-chip"><GraduationCap size={18} aria-hidden="true" /></span>
            <span className={styles.tagBadge}>CAMPUS COMPATIBLE</span>
            <h3>Best for College Students</h3>
            <p>
              Specifically tailored for B.Tech, BCA, MCA, M.Tech, and diploma students. Gain verifiable work experience that fulfills college internship requirements while preparing you for campus placements.
            </p>
          </div>

          {/* 5. 10 Hours a Week Commitment */}
          <div className={styles.highlightCard}>
            <span className="icon-chip"><Code2 size={18} aria-hidden="true" /></span>
            <span className={styles.tagBadge}>SUSTAINABLE COMMITMENT</span>
            <h3>10 Hours a Week Login</h3>
            <p>
              A minimum commitment of just 10 hours per week of active sprint contribution and code commits. Designed to easily integrate alongside rigorous semester coursework and exams.
            </p>
          </div>

          {/* 6. Hardware & Setup Requirements */}
          <div className={styles.highlightCard}>
            <span className="icon-chip"><Wifi size={18} aria-hidden="true" /></span>
            <span className={styles.tagBadge}>PREREQUISITES</span>
            <h3>Internet &amp; Laptop Connection</h3>
            <p>
              All development environments and vector indices are cloud-hosted. A working personal laptop (Windows, Mac, or Linux) and a dependable broadband/mobile internet connection are all you need.
            </p>
          </div>
        </div>

        {/* Requirements Banner */}
        <div className={styles.reqBanner}>
          <div className={styles.reqItem}>
            <Laptop size={22} color="var(--accent)" style={{ margin: '0 auto' }} />
            <h4>Working Personal Laptop</h4>
            <p>Any modern 64-bit OS with Git &amp; VS Code installed</p>
          </div>
          <div className={styles.reqItem}>
            <Wifi size={22} color="var(--accent)" style={{ margin: '0 auto' }} />
            <h4>Stable Internet Access</h4>
            <p>For Git commits, documentation sync, and squad huddles</p>
          </div>
          <div className={styles.reqItem}>
            <Clock size={22} color="var(--accent)" style={{ margin: '0 auto' }} />
            <h4>10 Hours / Week Minimum</h4>
            <p>Self-scheduled participation over 7 operational days</p>
          </div>
        </div>

        {/* SEO-Rich Informational Deep Dive */}
        <section className={styles.seoArticle}>
          <div className="center mb-md">
            <span className="doclabel justify-center">PROGRAM OVERVIEW</span>
            <h2>About the Aivara Technologies Internship</h2>
            <p className="measure-sm" style={{ margin: '0 auto' }}>
              Bridging academic computer science education and real-world industrial software delivery.
            </p>
          </div>

          <div className={styles.articleGrid}>
            <div className={styles.articleCard}>
              <h3>Why Choose This Remote Internship?</h3>
              <p>
                Most student internships in India fall into two traps: theoretical classroom tutorials that mimic college lectures, or unpaid data-entry roles without code reviews. The Aivara Technologies cohort solves this by giving you real responsibilities on active client repositories.
              </p>
              <ul>
                <li><strong>Production Pull Requests:</strong> Push real branches, write automated tests, and receive line-by-line feedback from senior engineers.</li>
                <li><strong>Independent Credential Verification:</strong> Earn an accredited experience letter with a unique SHA-256 validation ID checkable on <code>dbert.online/verify</code>.</li>
                <li><strong>Pre-Placement Opportunity (PPO):</strong> Exceptional interns are shortlisted for full-time engineering and mentor positions at Aivara Technologies and partner startups.</li>
              </ul>
            </div>

            <div className={styles.articleCard}>
              <h3>How It Works For College Students</h3>
              <p>
                We understand the demands of semester examinations, assignment submission deadlines, and campus schedules. Our asynchronous engineering workflow is crafted so you succeed academically while building a verified developer portfolio.
              </p>
              <ul>
                <li><strong>Sprint Planning:</strong> Receive weekly project deliverables broken down into bite-sized GitHub issues and tickets.</li>
                <li><strong>10-Hour Weekly Cadence:</strong> Complete your contributions on weekday evenings or weekends at your own pace.</li>
                <li><strong>Performance Stipends:</strong> As your milestone pull requests get approved and merged, you earn performance stipends up to ₹22,000.</li>
                <li><strong>Zero Sourcing Commission:</strong> 100% direct evaluation—no recruitment agencies, middlemen, or hidden fees.</li>
              </ul>
            </div>
          </div>
        </section>
      </div>
    </>
  );
}
