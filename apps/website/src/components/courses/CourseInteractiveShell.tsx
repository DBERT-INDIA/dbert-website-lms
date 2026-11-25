'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { 
  ShieldCheck, 
  Award, 
  GitPullRequest, 
  Zap, 
  CheckCircle2, 
  BookOpen, 
  ArrowRight,
  Clock,
  Briefcase,
  Layers,
  Banknote,
  Cpu,
  Star,
  Users
} from 'lucide-react';
import TrackLeadCaptureForm from '@/components/forms/TrackLeadCaptureForm';
import s from '../../app/courses/courses.module.css';

export interface VerifiedAlum {
  certId: string;
  holderName: string;
  domain: string;
  score: number;
  grade: string;
  verifyUrl: string;
}

export interface DomainCourseData {
  slug: string;
  title: string;
  badge: string;
  headline: string;
  lede: string;
  salaryRange: string;
  placement: string;
  skills: string[];
  tools: string[];
  partnerRepo: {
    name: string;
    repo: string;
    focus: string;
  };
  fellowshipWeeks: { period: string; title: string; tasks: string[] }[];
  courseWeeks: { period: string; title: string; topics: string[] }[];
  faqs: { question: string; answer: string }[];
}

interface CourseInteractiveShellProps {
  course: DomainCourseData;
  domain: string;
  alumni?: VerifiedAlum[];
}

export default function CourseInteractiveShell({ course, domain, alumni = [] }: CourseInteractiveShellProps) {
  const [activeTrack, setActiveTrack] = useState<'fellowship' | 'course'>('fellowship');

  return (
    <div className={s.pageWrapper}>
      <div className={s.glowSpot}></div>

      {/* Top Announcement & Social Proof Bar */}
      <div className={s.announcementBar}>
        <span className={s.pulseDot}></span>
        <strong>December 2026 Cohort Admissions Active</strong>
        <span>·</span>
        <span>Limited to 25 Vetted Fellows</span>
        <span>·</span>
        <span style={{ color: '#fbbf24', fontWeight: 600 }}>🏛️ Govt. of India MSME Registered</span>
        <span>·</span>
        <span style={{ color: '#34d399', fontWeight: 600 }}>⭐ 4.9/5 Rating from 465+ Fellows</span>
      </div>

      <div className={s.container}>
        {/* Hero Header Section */}
        <section className={s.heroSection}>
          <div className={s.metaRow}>
            <span className={s.badgePill}>
              <Cpu size={13} /> {course.badge}
            </span>
            <span className={`${s.badgePill} ${s.badgeAccredited}`}>
              <ShieldCheck size={13} /> MSME Accredited Certification
            </span>
            <span style={{ fontSize: '0.78rem', color: '#94a3b8', fontFamily: 'monospace' }}>
              BATCH CODE: 2026-T4
            </span>
          </div>

          <h1 className={s.heroTitle}>{course.title}</h1>
          <p className={s.heroHeadline}>{course.headline}</p>
          <p className={s.heroLede}>{course.lede}</p>

          {/* Value & Compensation Ribbon */}
          <div className={s.outcomeRibbon}>
            <div className={s.outcomeCard}>
              <div className={s.outcomeIcon} style={{ color: '#38bdf8' }}>
                <Banknote size={18} />
              </div>
              <div>
                <div className={s.outcomeLabel}>Verified Compensation</div>
                <div className={s.outcomeValue}>{course.salaryRange}</div>
              </div>
            </div>

            <div className={s.outcomeCard}>
              <div className={s.outcomeIcon} style={{ color: '#10b981' }}>
                <Zap size={18} />
              </div>
              <div>
                <div className={s.outcomeLabel}>Career Outcome</div>
                <div className={s.outcomeValue}>100% Guaranteed Production Internship with Dedicated Placement Assistance</div>
              </div>
            </div>

            <div className={s.outcomeCard}>
              <div className={s.outcomeIcon} style={{ color: '#f59e0b' }}>
                <Award size={18} />
              </div>
              <div>
                <div className={s.outcomeLabel}>Credentials Issued</div>
                <div className={s.outcomeValue}>3-Document Verifiable Packet</div>
              </div>
            </div>

            <div className={s.outcomeCard}>
              <div className={s.outcomeIcon} style={{ color: '#a855f7' }}>
                <GitPullRequest size={18} />
              </div>
              <div>
                <div className={s.outcomeLabel}>Code Review</div>
                <div className={s.outcomeValue}>Upstream GitHub PR Review</div>
              </div>
            </div>
          </div>

          {/* Quick Technical Competency Chips */}
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8, marginTop: 22 }}>
            {course.skills.map((skill) => (
              <span
                key={skill}
                style={{
                  fontSize: '0.78rem',
                  fontFamily: 'monospace',
                  background: 'rgba(255, 255, 255, 0.04)',
                  border: '1px solid rgba(255, 255, 255, 0.1)',
                  padding: '4px 10px',
                  borderRadius: 6,
                  color: '#e2e8f0'
                }}
              >
                {skill}
              </span>
            ))}
          </div>
        </section>

        {/* Interactive Dual-Track Switcher */}
        <section className={s.switcherSection}>
          <div className={s.trackSwitcher}>
            <button
              type="button"
              className={`${s.trackTabBtn} ${activeTrack === 'fellowship' ? s.trackTabBtnActive : ''}`}
              onClick={() => setActiveTrack('fellowship')}
            >
              <div className={s.trackTabTitle}>
                <Zap size={15} style={{ color: '#10b981' }} /> ⚡ Structure 1: 2-Month Fellowship
              </div>
              <div className={s.trackTabSubtitle}>
                Venture Sprints · 100% Guaranteed Production Internship with Dedicated Placement Assistance · ₹1,999
              </div>
            </button>

            <button
              type="button"
              className={`${s.trackTabBtn} ${activeTrack === 'course' ? s.trackTabBtnActive : ''}`}
              onClick={() => setActiveTrack('course')}
            >
              <div className={s.trackTabTitle}>
                <BookOpen size={15} style={{ color: '#38bdf8' }} /> 🎓 Structure 2: 3-Month Comprehensive Course
              </div>
              <div className={s.trackTabSubtitle}>
                Foundations to Enterprise Mastery · 12 Modules · Zero-Cost EMI
              </div>
            </button>
          </div>

          <div className={s.guaranteeBanner}>
            <i className="fa-solid fa-code-commit" />
            <span>100% Guaranteed Production Internship with Dedicated Placement Assistance</span>
          </div>
        </section>

        {/* Main 2-Column Content Layout */}
        <div className={s.mainLayout}>
          
          {/* Left Column: Academic Rigor & Curricular Details */}
          <div>
            
            {/* Active Track Highlight Box */}
            <div className={s.structureBox}>
              <div className={s.structureHeader}>
                <div>
                  <span className={s.structureBadge}>
                    {activeTrack === 'fellowship' ? 'FELLOWSHIP SPRINT PATHWAY' : 'COMPREHENSIVE LEARNER PATHWAY'}
                  </span>
                  <h2 style={{ fontSize: '1.25rem', fontWeight: 800, color: '#ffffff', marginTop: 8 }}>
                    {activeTrack === 'fellowship' 
                      ? '2-Month Applied Engineering Fellowship' 
                      : '3-Month Comprehensive Professional Course'}
                  </h2>
                </div>
                <div style={{ textAlign: 'right' }}>
                  <div style={{ fontSize: '0.75rem', color: '#94a3b8', textTransform: 'uppercase' }}>Program Investment</div>
                  <div style={{ fontSize: '1.35rem', fontWeight: 800, color: activeTrack === 'fellowship' ? '#10b981' : '#38bdf8', fontFamily: 'monospace' }}>
                    {activeTrack === 'fellowship' ? '₹1,999 Total' : 'Flexible Monthly EMI'}
                  </div>
                </div>
              </div>

              <p style={{ fontSize: '0.88rem', color: '#cbd5e1', lineHeight: 1.6, marginBottom: 16 }}>
                {activeTrack === 'fellowship'
                  ? 'Designed for engineers with foundational syntax competence. Work directly on production codebases, receive senior pull-request evaluations, and secure 100% guaranteed production internship with dedicated placement assistance across internal DBERT portfolio ventures (Gayatri AI, Alkame, Aivara) or verified corporate hiring partners.'
                  : 'An intensive, structured journey from foundational computer systems to large-scale enterprise deployment. Includes guided hands-on laboratories, live code walkthroughs, and guaranteed interview preparation sprints.'}
              </p>

              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 12 }}>
                <div style={{ padding: 12, background: 'rgba(255, 255, 255, 0.03)', borderRadius: 8, border: '1px solid rgba(255, 255, 255, 0.06)' }}>
                  <div style={{ fontSize: '0.72rem', color: '#94a3b8', textTransform: 'uppercase', fontWeight: 700 }}>Duration</div>
                  <div style={{ fontSize: '0.95rem', fontWeight: 700, color: '#ffffff', marginTop: 2 }}>
                    {activeTrack === 'fellowship' ? '8 Weeks (2 Months)' : '12 Weeks (3 Months)'}
                  </div>
                </div>
                <div style={{ padding: 12, background: 'rgba(255, 255, 255, 0.03)', borderRadius: 8, border: '1px solid rgba(255, 255, 255, 0.06)' }}>
                  <div style={{ fontSize: '0.72rem', color: '#94a3b8', textTransform: 'uppercase', fontWeight: 700 }}>Commitment</div>
                  <div style={{ fontSize: '0.95rem', fontWeight: 700, color: '#ffffff', marginTop: 2 }}>
                    {activeTrack === 'fellowship' ? '10–12 Hours / Week' : '8–10 Hours / Week'}
                  </div>
                </div>
                <div style={{ padding: 12, background: 'rgba(255, 255, 255, 0.03)', borderRadius: 8, border: '1px solid rgba(255, 255, 255, 0.06)' }}>
                  <div style={{ fontSize: '0.72rem', color: '#94a3b8', textTransform: 'uppercase', fontWeight: 700 }}>Outcome</div>
                  <div style={{ fontSize: '0.95rem', fontWeight: 700, color: '#ffffff', marginTop: 2 }}>
                    {activeTrack === 'fellowship' ? '100% Guaranteed Production Internship with Dedicated Placement Assistance' : 'Enterprise Placement Ready'}
                  </div>
                </div>
              </div>

              {activeTrack === 'fellowship' && (
                <ul className={s.trackFeaturesList}>
                  <li>
                    <CheckCircle2 size={16} style={{ color: '#10b981', flexShrink: 0, marginTop: 2 }} />
                    <span><strong>Active Production Repositories:</strong> Hands-on commits and architect PR reviews on Gayatri AI &amp; Alkame.</span>
                  </li>
                  <li>
                    <CheckCircle2 size={16} style={{ color: '#10b981', flexShrink: 0, marginTop: 2 }} />
                    <span><strong>Placement Assistance:</strong> Direct indexing on <code>/verify/directory</code> and recruiter pipeline matching.</span>
                  </li>
                </ul>
              )}
            </div>

            {/* Dynamic Curriculum Timeline */}
            <div style={{ marginBottom: 36 }}>
              <div className={s.sectionHeading}>
                {activeTrack === 'fellowship' ? (
                  <>
                    <Clock size={20} style={{ color: '#10b981' }} />
                    <span>2-Month Fellowship Sprint Milestones</span>
                  </>
                ) : (
                  <>
                    <BookOpen size={20} style={{ color: '#38bdf8' }} />
                    <span>3-Month Comprehensive Syllabus</span>
                  </>
                )}
              </div>

              <div className={s.milestoneList}>
                {(activeTrack === 'fellowship' ? course.fellowshipWeeks : course.courseWeeks).map((item, idx) => (
                  <div key={idx} className={s.milestoneCard}>
                    <div className={s.milestoneTop}>
                      <span className={s.milestonePeriod}>{item.period}</span>
                      <span className={s.milestoneTitle}>{item.title}</span>
                    </div>
                    <ul className={s.milestoneBullets}>
                      {'tasks' in item ? (
                        item.tasks.map((t, tIdx) => <li key={tIdx}>{t}</li>)
                      ) : (
                        item.topics.map((t, tIdx) => <li key={tIdx}>{t}</li>)
                      )}
                    </ul>
                  </div>
                ))}
              </div>
            </div>

            {/* Verified Alumni Social Proof Strip */}
            {alumni.length > 0 && (
              <section className={s.alumniSection}>
                <div className={s.sectionHeading}>
                  <Users size={20} style={{ color: '#10b981' }} />
                  <span>Verified Alumni &amp; Evaluated Fellows</span>
                </div>
                <p style={{ fontSize: '0.85rem', color: '#94a3b8', marginBottom: 16 }}>
                  Graduates evaluated under senior review and cryptographically verified on our ledger:
                </p>

                <div className={s.alumniGrid}>
                  {alumni.slice(0, 4).map((alum) => (
                    <div key={alum.certId} className={s.alumniCard}>
                      <div className={s.alumniName}>{alum.holderName}</div>
                      <div className={s.alumniMeta}>Score: {alum.score}/100 · {alum.grade}</div>
                      <div className={s.alumniChip}>Domain: {alum.domain}</div>
                      <div style={{ marginTop: 10 }}>
                        <Link href={alum.verifyUrl} className={s.verifyLink} target="_blank">
                          Inspect Dossier →
                        </Link>
                      </div>
                    </div>
                  ))}
                </div>
              </section>
            )}

            {/* Upstream Production Partner Repository */}
            <div className={s.repoBox}>
              <div className={s.repoTitle}>
                <GitPullRequest size={18} style={{ color: '#10b981' }} />
                <span>Official Upstream Partner Repository</span>
              </div>
              <p className={s.repoDesc}>
                Fellows contribute production code directly to <strong>{course.partnerRepo.name}</strong>. Personal forks without upstream PR merges are rejected by the CI grading daemon.
              </p>
              <div style={{ fontSize: '0.8rem', color: '#94a3b8', marginBottom: 8 }}>
                Repository Focus: {course.partnerRepo.focus}
              </div>
              <a 
                href={course.partnerRepo.repo} 
                target="_blank" 
                rel="noopener noreferrer" 
                className={s.repoLink}
              >
                View Repository on GitHub ↗
              </a>
            </div>

            {/* Frequently Asked Questions */}
            <div>
              <div className={s.sectionHeading}>
                <span>Admissions &amp; Verification FAQs</span>
              </div>
              <div className={s.faqList}>
                {course.faqs.map((faq, idx) => (
                  <div key={idx} className={s.faqItem}>
                    <div className={s.faqQuestion}>{faq.question}</div>
                    <div className={s.faqAnswer}>{faq.answer}</div>
                  </div>
                ))}
              </div>
            </div>

          </div>

          {/* Right Column: Embedded Dynamic Lead Capture Form */}
          <div className={s.stickyFormWrap}>
            <TrackLeadCaptureForm
              initialDomain={domain}
              initialProgram={activeTrack}
              title={`Apply for ${course.title}`}
              subtitle="Submit details below to access syllabus documentation, standup times, and counselor consultation."
            />

            {/* Direct Instant Confirmation Card */}
            <div style={{ marginTop: 20, padding: 18, background: 'rgba(15, 23, 42, 0.75)', border: '1px solid rgba(255, 255, 255, 0.08)', borderRadius: 10 }}>
              <div style={{ fontSize: '0.8rem', fontWeight: 700, color: '#fbbf24', textTransform: 'uppercase', marginBottom: 4 }}>
                ⚡ Fast-Track Seat Confirmation
              </div>
              <p style={{ fontSize: '0.82rem', color: '#cbd5e1', lineHeight: 1.5, margin: '0 0 12px' }}>
                Ready to confirm your December 2026 seat immediately? Complete program admission directly for ₹1,999.
              </p>
              <Link 
                href={`/enroll/1999?domain=${encodeURIComponent(course.title)}`}
                style={{
                  display: 'inline-flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  gap: 6,
                  width: '100%',
                  padding: '10px 14px',
                  background: 'linear-gradient(135deg, #fbbf24 0%, #d97706 100%)',
                  color: '#0b1120',
                  fontWeight: 700,
                  fontSize: '0.85rem',
                  borderRadius: 6,
                  textDecoration: 'none'
                }}
              >
                Confirm Program Seat (₹1,999) →
              </Link>
            </div>
          </div>

        </div>
      </div>
    </div>
  );
}
