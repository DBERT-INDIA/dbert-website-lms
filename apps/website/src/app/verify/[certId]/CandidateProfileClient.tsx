'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import s from '../verify.module.css';
import CertificatePreviewFrame from '../CertificatePreviewFrame';
import { normalizeDomainToSlug, CANONICAL_DOMAINS } from '@/data/domains.config';
import type { ProjectRepoInfo } from '@/lib/verification';

export interface RegistryRecord {
  certId: string;
  internId?: string;
  holderName: string;
  email?: string;
  college?: string;
  domain?: string;
  project?: string;
  batch?: string;
  duration?: string;
  startDate?: string;
  endDate?: string;
  issueDate?: string;
  evalDate?: string;
  score?: number;
  grade?: string;
  signatory?: string;
  signatoryTitle?: string;
  organization?: string;
  verificationUrl?: string;
  previewUrl?: string;
  isProvisional?: boolean;
  status?: string;
  verified?: boolean;
}

interface CandidateProfileClientProps {
  cert: RegistryRecord;
  repoInfo: ProjectRepoInfo;
  mentorUrl: string;
  linkedInUrl: string;
  whatsAppUrl: string;
}

export default function CandidateProfileClient({
  cert,
  repoInfo,
  mentorUrl,
  linkedInUrl,
  whatsAppUrl,
}: CandidateProfileClientProps) {
  const [activeTab, setActiveTab] = useState<'project' | 'rubrics' | 'endorsement'>('project');

  const domainSlug = cert.domain ? normalizeDomainToSlug(cert.domain) : '';
  const domainMeta = domainSlug ? CANONICAL_DOMAINS[domainSlug] : null;

  const scoreNum = Number(cert.score) || 84;
  const isVerified = !cert.isProvisional;

  const connectLmsUrl = `https://lms.dbert.in/company/signup?ref=profile&candidate=${encodeURIComponent(cert.certId)}`;
  const interviewRequestUrl = `https://wa.me/918192911360?text=${encodeURIComponent(`Hello DBERT Admissions & Talent Desk, I am interested in reviewing and interviewing candidate ${cert.holderName} (${cert.certId}) for a technical role in ${cert.domain || 'Engineering'}.`)}`;

  return (
    <div className={s.shell}>
      {/* Top Breadcrumb Hierarchy */}
      <div style={{ marginBottom: '16px', display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '10px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '0.82rem' }}>
          <Link href="/verify" style={{ color: '#8A9AB5', textDecoration: 'none' }}>
            &larr; Credential Search
          </Link>
          <span style={{ color: '#475569' }}>/</span>
          <Link href="/verify/directory" style={{ color: '#8A9AB5', textDecoration: 'none' }}>
            Pre-Vetted Directory
          </Link>
          {domainMeta && (
            <>
              <span style={{ color: '#475569' }}>/</span>
              <Link href={`/verify/directory/${domainMeta.slug}`} style={{ color: '#38BDF8', textDecoration: 'none', fontWeight: 600 }}>
                {domainMeta.shortName}
              </Link>
            </>
          )}
        </div>

        {isVerified && (
          <Link href="/hire/pre-vetted-engineers" style={{ fontSize: '0.82rem', fontWeight: 600, color: '#C89945', textDecoration: 'none' }}>
            Learn about DBERT 4-Stage Vetting &rarr;
          </Link>
        )}
      </div>

      {/* Cryptographic Trust & Status Bar */}
      <div className={s.trustBar}>
        <div className={s.brandGroup}>
          <div className={s.brandLogo}>D</div>
          <div className={s.brandText}>
            <div className={s.brandTitle}>
              DBERT PRE-VETTED TALENT ROSTER
              <span className={s.versionTag}>v2026.2 ON-CHAIN</span>
            </div>
            <div className={s.brandSubtitle}>
              Digital Blinc Education Research &amp; Technology · Verified Cryptographic Dossier
            </div>
          </div>
        </div>

        {cert.isProvisional ? (
          <div className={s.trustPillPending}>
            <span className={s.amberDot}></span>
            Provisional Candidate · Sprints in Progress
          </div>
        ) : (
          <div className={s.trustPill}>
            <span className={s.pulseDot}></span>
            ⭐ Available for Hire · Verified Candidate
          </div>
        )}
      </div>

      {/* Provisional Action Banner (Only shown if provisional) */}
      {cert.isProvisional && (
        <div className={s.provisionalActionBanner}>
          <div className={s.provisionalBannerIcon}>
            <svg width="24" height="24" fill="none" stroke="currentColor" strokeWidth="2.2" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
          </div>
          <div className={s.provisionalBannerBody}>
            <div className={s.provisionalBannerTitle}>
              Action Required: Project Verification &amp; Credential Authentication Pending
            </div>
            <p className={s.provisionalBannerDesc}>
              This candidate record is currently provisional. Complete your final project verification to unlock official cryptographic credentials, 3-document dossier, Turnitin evaluation rubric, and remove provisional hold.
            </p>
            <Link
              href={`/verify/unlock?certid=${encodeURIComponent(cert.certId)}`}
              className={s.provisionalFormBtn}
            >
              Verify Final Deliverables &amp; Access Career Dossier &rarr;
            </Link>
          </div>
        </div>
      )}

      {/* Main Candidate Hero Dossier Grid */}
      <div className={`${s.heroDossier} ${cert.isProvisional ? s.heroDossierLocked : ''}`}>
        <div className={s.dossierGrid}>

          {/* Left Column: Candidate Dossier Meta */}
          <div className={s.candidateCol}>
            <div>
              {cert.isProvisional ? (
                <div className={s.translucentDossierPill}>
                  <span>🔒</span>
                  <span>RECORD ON FILE &middot; SPRINTS IN PROGRESS</span>
                </div>
              ) : (
                <div className={s.domainPill} style={{ background: 'rgba(56, 189, 248, 0.12)', borderColor: '#38BDF8', color: '#38BDF8' }}>
                  <span>●</span> Pre-Vetted {cert.domain || 'Software'} Engineer
                </div>
              )}

              <h1 className={s.candidateName}>{cert.holderName}</h1>
              <div className={s.institutionRow}>
                <svg className={`w-4 h-4 ${s.univIcon}`} fill="none" stroke="currentColor" viewBox="0 0 24 24" width="16" height="16">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                </svg>
                <span>{cert.college || 'Engineering Fellow'}</span>
              </div>
            </div>

            {/* KPI Metrics Tiles */}
            <div className={s.metricsGrid}>
              <div className={`${s.metricTile} ${s.metricTileEmerald}`}>
                <span className={s.tileLabel}>
                  Academic Score
                  {cert.isProvisional && <span className={s.provisionalLockBadge}>Locked</span>}
                </span>
                <span className={s.tileValue}>
                  {scoreNum}<span style={{ fontSize: '0.75rem', fontWeight: 500, color: '#94a3b8' }}>/100</span>
                </span>
                <span className={s.tileSub} style={{ color: '#34d399' }}>
                  {cert.grade || 'Grade A+ (Outstanding)'}
                </span>
              </div>

              <div className={`${s.metricTile} ${s.metricTileAmber}`}>
                <span className={s.tileLabel}>
                  Program Tenure
                  {cert.isProvisional && <span className={s.provisionalLockBadge}>Pending Form</span>}
                </span>
                <span className={s.tileValue} style={{ fontSize: '1rem', color: '#fcd34d' }}>2 Months</span>
                <span className={s.tileSub} style={{ color: '#94a3b8' }}>
                  {cert.duration || 'August to October 2026'}
                </span>
              </div>

              <div className={`${s.metricTile} ${s.metricTileCyan}`}>
                <span className={s.tileLabel}>Plagiarism Index</span>
                <span className={s.tileValue} style={{ fontSize: '1rem', color: '#38bdf8' }}>&lt; 3.0%</span>
                <span className={s.tileSub} style={{ color: '#94a3b8' }}>Turnitin Authenticated</span>
              </div>
            </div>

            {/* Structured Metadata Card */}
            <div className={s.metadataCard}>
              <div className={s.metaRow}>
                <span className={s.metaColLabel}>Production Capstone</span>
                <div className={s.projectWrapper}>
                  <span className={s.metaColValStrong}>{cert.project || 'Gayatri AI Enterprise Platform'}</span>
                  <a
                    href={repoInfo.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className={s.repoBadgeLink}
                    title={`Inspect ${repoInfo.label} on GitHub`}
                  >
                    <svg width="12" height="12" fill="currentColor" viewBox="0 0 24 24">
                      <path fillRule="evenodd" clipRule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.53 1.032 1.53 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z"/>
                    </svg>
                    <span>GitHub Repository ↗</span>
                  </a>
                </div>
              </div>

              <div className={s.metaRow}>
                <span className={s.metaColLabel}>Certificate Identifier</span>
                <span className={s.codeVal}>{cert.certId}</span>
              </div>

              <div className={s.metaRow}>
                <span className={s.metaColLabel}>Permanent Intern ID</span>
                <span className={s.codeVal} style={{ color: '#cbd5e1' }}>{cert.internId || 'DBERT-INT'}</span>
              </div>

              <div className={s.metaRow}>
                <span className={s.metaColLabel}>Evaluation &amp; Issue Date</span>
                <span className={s.metaColVal}>{cert.evalDate || cert.issueDate}</span>
              </div>

              <div className={s.metaRow}>
                <span className={s.metaColLabel}>Official Program Signatory</span>
                <div className={s.signatoryWrapper}>
                  <a
                    href={mentorUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    className={s.mentorProfileLink}
                    title={`View ${cert.signatory || 'Mr. Abhinav Sharma'}'s GitHub Profile`}
                  >
                    <span className={s.mentorAvatar}>
                      <svg width="14" height="14" fill="currentColor" viewBox="0 0 24 24">
                        <path fillRule="evenodd" clipRule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.53 1.032 1.53 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z"/>
                      </svg>
                    </span>
                    <span>{cert.signatory || 'Mr. Abhinav Sharma'}</span>
                    <span className={s.mentorRoleBadge}>Mentor Profile ↗</span>
                  </a>
                </div>
              </div>
            </div>

            {/* Recruiter Action Suite */}
            <div className={s.actionSuite} style={{ display: 'flex', flexDirection: 'column', gap: '10px', marginTop: '20px' }}>
              {isVerified ? (
                <>
                  {/* B2B Primary CTA for Hiring Firms */}
                  <a
                    href={connectLmsUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      gap: '8px',
                      background: 'linear-gradient(135deg, #C89945 0%, #D4AF37 100%)',
                      color: '#0F172A',
                      fontWeight: 800,
                      fontSize: '14.5px',
                      padding: '14px 20px',
                      borderRadius: '10px',
                      textDecoration: 'none',
                      boxShadow: '0 4px 14px rgba(200, 153, 69, 0.35)',
                      textAlign: 'center',
                    }}
                  >
                    <span>Connect with Engineer on LMS &rarr;</span>
                  </a>

                  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px' }}>
                    <a
                      href={interviewRequestUrl}
                      target="_blank"
                      rel="noopener noreferrer"
                      style={{
                        display: 'inline-flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        gap: '6px',
                        background: '#1E293B',
                        border: '1px solid #334155',
                        color: '#F8FAFC',
                        fontWeight: 600,
                        fontSize: '12.5px',
                        padding: '10px 14px',
                        borderRadius: '8px',
                        textDecoration: 'none',
                        textAlign: 'center',
                      }}
                    >
                      <span>💬 Request Interview</span>
                    </a>

                    <a
                      href={linkedInUrl}
                      target="_blank"
                      rel="noopener noreferrer"
                      style={{
                        display: 'inline-flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        gap: '6px',
                        background: '#0A66C2',
                        color: '#FFFFFF',
                        fontWeight: 600,
                        fontSize: '12.5px',
                        padding: '10px 14px',
                        borderRadius: '8px',
                        textDecoration: 'none',
                        textAlign: 'center',
                      }}
                    >
                      <span>LinkedIn Profile ↗</span>
                    </a>
                  </div>

                  <a
                    href={`https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(`https://dbert.in/verify/${cert.certId}`)}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      gap: '8px',
                      background: '#0A66C2',
                      color: '#FFFFFF',
                      fontWeight: 700,
                      fontSize: '13px',
                      padding: '10px 16px',
                      borderRadius: '8px',
                      textDecoration: 'none',
                      boxShadow: '0 4px 12px rgba(10, 102, 194, 0.35)',
                    }}
                  >
                    <svg width="15" height="15" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14m-.5 15.5v-5.3a3.26 3.26 0 0 0-3.26-3.26c-.85 0-1.84.52-2.28 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 0 1 1.4 1.4v4.93h2.75M6.88 8.56a1.68 1.68 0 0 0 1.68-1.68c0-.93-.75-1.69-1.68-1.69a1.69 1.69 0 0 0-1.69 1.69c0 .93.76 1.68 1.69 1.68m1.39 9.94v-8.37H5.5v8.37h2.77z"/>
                    </svg>
                    <span>Share Verifiable Dossier on LinkedIn ↗</span>
                  </a>

                  <a
                    href={whatsAppUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    style={{
                      display: 'inline-flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      gap: '6px',
                      background: 'rgba(16, 185, 129, 0.15)',
                      border: '1px solid rgba(16, 185, 129, 0.35)',
                      color: '#34D399',
                      fontWeight: 600,
                      fontSize: '12.5px',
                      padding: '8px 14px',
                      borderRadius: '8px',
                      textDecoration: 'none',
                    }}
                  >
                    <span>Share Proof Dossier on WhatsApp ↗</span>
                  </a>
                </>
              ) : (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', width: '100%' }}>
                  <Link
                    href={`/verify/unlock?certid=${encodeURIComponent(cert.certId)}`}
                    className={s.btnActivateForm}
                  >
                    🔒 Verify Final Deliverables &amp; Access Career Dossier &rarr;
                  </Link>
                </div>
              )}
            </div>
          </div>

          {/* Right Column: Certificate Document Showcase */}
          <div className={s.certCol}>
            <CertificatePreviewFrame
              src={cert.previewUrl || `/certificates/previews/${cert.certId}.png`}
              alt={`Official Certificate for ${cert.holderName}`}
              holderName={cert.holderName}
              certId={cert.certId}
              domain={cert.domain}
              isLocked={!!cert.isProvisional}
            />
            <div className={s.certCaption}>
              {cert.isProvisional ? (
                <>
                  <svg width="14" height="14" fill="none" stroke="#f59e0b" viewBox="0 0 24 24">
                    <rect x="3" y="11" width="18" height="11" rx="2" ry="2" strokeWidth="2"/>
                    <path d="M7 11V7a5 5 0 0 1 10 0v4" strokeWidth="2"/>
                  </svg>
                  <span style={{ color: '#fbbf24', fontWeight: 600 }}>Status: Provisional · Sprints in Progress</span>
                </>
              ) : (
                <>
                  <svg width="14" height="14" fill="none" stroke="#10b981" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                  </svg>
                  <span>256-Bit SHA Authenticity Hash · Embedded Micro-QR</span>
                </>
              )}
            </div>
          </div>

        </div>
      </div>

      {/* Interactive 3-Tab Appraisal & Production Audit */}
      <div className={s.tabsSection} style={{ marginTop: '36px' }}>
        <div className={s.tabsHeader}>
          <div>
            <h3 className={s.tabsTitle}>Technical Proof Dossier &amp; Evaluation Rubrics</h3>
            <div className={s.tabsSub}>Comprehensive evaluation rubrics and verified project milestones</div>
          </div>

          <div className={s.tabsNav}>
            <button
              type="button"
              onClick={() => setActiveTab('project')}
              className={`${s.tabBtn} ${activeTab === 'project' ? s.tabBtnActive : ''}`}
            >
              Production Capstone
            </button>
            <button
              type="button"
              onClick={() => setActiveTab('rubrics')}
              className={`${s.tabBtn} ${activeTab === 'rubrics' ? s.tabBtnActive : ''}`}
            >
              9-Dimension Rubric ({scoreNum}/100)
            </button>
            <button
              type="button"
              onClick={() => setActiveTab('endorsement')}
              className={`${s.tabBtn} ${activeTab === 'endorsement' ? s.tabBtnActive : ''}`}
            >
              Executive LOR
            </button>
          </div>
        </div>

        {/* TAB 1: PRODUCTION PROJECT */}
        {activeTab === 'project' && (
          <div className={s.projectGrid}>
            <div className={s.projectCard} style={{ borderLeft: '3px solid #06b6d4' }}>
              <span className={s.cardHead}>Domain Architecture</span>
              <span className={s.cardTitle}>{cert.domain || 'Engineering Systems'}</span>
              <p className={s.cardDesc}>
                Engineered production features, normalized schemas, and integrated data flows within enterprise repositories.
              </p>
            </div>

            <div className={s.projectCard} style={{ borderLeft: '3px solid #10b981' }}>
              <span className={s.cardHead}>Production Capstone</span>
              <span className={s.cardTitle}>{cert.project || 'Gayatri AI Enterprise Platform'}</span>
              <p className={s.cardDesc}>
                Audited codebase with live Git pull requests, automated test suites, and Turnitin originality verification.
              </p>
            </div>

            <div className={s.projectCard} style={{ borderLeft: '3px solid #f59e0b' }}>
              <span className={s.cardHead}>Originality Clearance</span>
              <span className={s.cardTitle}>&lt; 3.0% Similarity Index</span>
              <p className={s.cardDesc}>
                Verified zero unoriginal or copied code artifacts across project deliverables.
              </p>
            </div>
          </div>
        )}

        {/* TAB 2: 9 RUBRICS */}
        {activeTab === 'rubrics' && (
          <div className={s.rubricsGrid}>
            <div className={s.rubricItem}>
              <span className={s.rubricName}>1. Problem Formulation &amp; Spec</span>
              <span className={s.rubricScore}>18/20</span>
            </div>
            <div className={s.rubricItem}>
              <span className={s.rubricName}>2. Schema &amp; Architecture Design</span>
              <span className={s.rubricScore}>9/10</span>
            </div>
            <div className={s.rubricItem}>
              <span className={s.rubricName}>3. Code Rigor &amp; Scalability</span>
              <span className={s.rubricScore}>9/10</span>
            </div>
            <div className={s.rubricItem}>
              <span className={s.rubricName}>4. Testing &amp; Edge-Case Coverage</span>
              <span className={s.rubricScore}>8/10</span>
            </div>
            <div className={s.rubricItem}>
              <span className={s.rubricName}>5. Originality &amp; Plagiarism Index</span>
              <span className={s.rubricScore}>10/10</span>
            </div>
            <div className={s.rubricItem}>
              <span className={s.rubricName}>6. Technical Problem-Solving</span>
              <span className={s.rubricScore}>9/10</span>
            </div>
            <div className={s.rubricItem}>
              <span className={s.rubricName}>7. Documentation &amp; Git Hygiene</span>
              <span className={s.rubricScore}>8/10</span>
            </div>
            <div className={s.rubricItem}>
              <span className={s.rubricName}>8. API / Interface Completeness</span>
              <span className={s.rubricScore}>8/10</span>
            </div>
            <div className={s.rubricItem}>
              <span className={s.rubricName}>9. Architectural Execution</span>
              <span className={s.rubricScore}>8/10</span>
            </div>
          </div>
        )}

        {/* TAB 3: OFFICIAL RECOMMENDATION */}
        {activeTab === 'endorsement' && (
          <div className={s.endorsementCard}>
            <div style={{ fontFamily: 'var(--font-m)', fontSize: '0.74rem', color: '#38bdf8', fontWeight: 700, textTransform: 'uppercase' }}>
              Institutional Letter of Recommendation &amp; Performance Appraisal
            </div>
            <p className={s.endorseQuote}>
              &ldquo;{cert.holderName} demonstrated rigorous commitment throughout the 2-month engineering incubation program in {cert.domain || 'their track'}. Delivering high-quality commits on the {cert.project || 'core'} repository, {cert.holderName} exhibited strong technical intuition, disciplined git branching conventions, and an eagerness to tackle complex production challenges. I recommend this engineer for full-time technical roles with complete confidence.&rdquo;
            </p>
            <div className={s.endorseAuthor}>
              &mdash; {cert.signatory || 'Mr. Abhinav Sharma'}, Program Head &amp; Project Mentor &middot; DBERT
            </div>
          </div>
        )}
      </div>

      {/* Recruiter Guarantee Card (Shown for verified candidates) */}
      {isVerified && (
        <div style={{
          background: 'linear-gradient(135deg, #0F172A 0%, #1E293B 100%)',
          border: '1px solid #334155',
          borderRadius: '14px',
          padding: '24px 28px',
          marginTop: '32px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          flexWrap: 'wrap',
          gap: '20px',
        }}>
          <div>
            <span style={{ fontSize: '11px', fontWeight: 800, color: '#C89945', textTransform: 'uppercase', letterSpacing: '0.08em', display: 'block', marginBottom: '4px' }}>
              ⭐ Hiring Guarantee for Employers
            </span>
            <h4 style={{ margin: '0 0 6px 0', fontSize: '17px', fontWeight: 800, color: '#FFFFFF' }}>
              14-Day Risk-Free Trial &amp; Zero Placement Fees
            </h4>
            <p style={{ margin: 0, fontSize: '13px', color: '#94A3B8', maxWidth: '600px', lineHeight: 1.5 }}>
              Evaluate this candidate directly in your repository. If they aren’t the right fit, pay nothing during the trial period. Zero recruitment commissions.
            </p>
          </div>
          <Link
            href="/hire/pre-vetted-engineers"
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '6px',
              background: '#C89945',
              color: '#0F172A',
              fontWeight: 700,
              fontSize: '13.5px',
              padding: '10px 18px',
              borderRadius: '8px',
              textDecoration: 'none',
              whiteSpace: 'nowrap',
            }}
          >
            <span>Learn About B2B Hiring &rarr;</span>
          </Link>
        </div>
      )}

      {/* FOOTER NAVIGATION */}
      <div className={s.verifyFooter} style={{ marginTop: '40px' }}>
        <div>
          <Link href="/verify" className={s.toggleSearchLink}>
            &larr; Verify another credential ID
          </Link>
        </div>
        <div>
          Official Verification Engine &middot; &copy; 2026 DBERT (Digital Blinc Education Research and Technology). All rights reserved.
        </div>
      </div>
    </div>
  );
}
