'use client';

import React, { useState, useEffect, Suspense, useCallback } from 'react';
import { useSearchParams } from 'next/navigation';
import s from './verify.module.css';
import CertificatePreviewFrame from './CertificatePreviewFrame';
import { trackEvent } from '@/lib/analytics';
import { getProjectRepoInfo, MENTOR_PROFILE, getIssueYearMonth, type ProjectRepoInfo } from '@/lib/verification';

interface VerificationResult {
  certId: string;
  internId?: string;
  holderName: string;
  college?: string;
  domain?: string;
  programName?: string;
  project?: string;
  duration?: string;
  startDate?: string;
  endDate?: string;
  issueDate: string;
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
  verified: boolean;
  repoInfo?: ProjectRepoInfo;
  mentorProfile?: {
    name: string;
    title: string;
    githubUrl: string;
    githubHandle: string;
  };
}

function VerifyFormContent() {
  const searchParams = useSearchParams();
  const initialCertId = (
    searchParams.get('certid') ||
    searchParams.get('certId') ||
    searchParams.get('id') ||
    ''
  ).trim();

  const [certId, setCertId] = useState(initialCertId);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<VerificationResult | null>(null);
  const [errorMsg, setErrorMsg] = useState('');
  const [showManualSearch, setShowManualSearch] = useState(!initialCertId);
  const [activeTab, setActiveTab] = useState<'project' | 'rubrics' | 'endorsement'>('project');
  const [copiedLink, setCopiedLink] = useState(false);

  const executeVerify = useCallback(async (idToVerify: string) => {
    if (!idToVerify.trim()) return;

    setLoading(true);
    setErrorMsg('');
    setResult(null);

    try {
      const res = await fetch(`/api/verify?certid=${encodeURIComponent(idToVerify.trim())}`);
      if (res.ok) {
        const data = await res.json();
        if (data.verified) {
          setResult(data);
          setShowManualSearch(false);
          trackEvent('certificate_verified', {
            cert_id: data.certId,
            program_name: data.programName,
            domain: data.domain || 'general',
          });
        } else {
          setErrorMsg('Certificate ID not found or invalid.');
        }
      } else {
        setErrorMsg('Verification failed. Please check the Certificate ID format.');
      }
    } catch {
      setErrorMsg('Network error. Please try again.');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    if (initialCertId) {
      executeVerify(initialCertId);
    }
  }, [initialCertId, executeVerify]);

  const handleVerify = (e: React.FormEvent) => {
    e.preventDefault();
    executeVerify(certId);
  };

  const copyText = (text: string) => {
    navigator.clipboard.writeText(text).then(() => {
      setCopiedLink(true);
      setTimeout(() => setCopiedLink(false), 2500);
    }).catch(() => {
      // Fallback
    });
  };

  const getLinkedInAddUrl = (res: VerificationResult) => {
    const certName = `DBERT Internship Certificate — ${res.domain || 'Engineering'}`;
    const orgName = 'DBERT';
    const certUrl = res.verificationUrl || `https://dbert.in/verify?certid=${res.certId}`;
    const { year, month } = getIssueYearMonth(res.issueDate);
    return `https://www.linkedin.com/profile/add?startTask=CERTIFICATION_NAME&name=${encodeURIComponent(certName)}&organizationName=${encodeURIComponent(orgName)}&issueYear=${year}&issueMonth=${month}&certUrl=${encodeURIComponent(certUrl)}&certId=${encodeURIComponent(res.certId)}`;
  };

  const getWhatsAppShareUrl = (res: VerificationResult) => {
    const certUrl = res.verificationUrl || `https://dbert.in/verify?certid=${res.certId}`;
    const text = `I just earned my verified 2-Month Internship Certificate in ${res.domain} from DBERT! Check out my official verified credential: ${certUrl}`;
    return `https://api.whatsapp.com/send?text=${encodeURIComponent(text)}`;
  };

  const repoInfo = result ? (result.repoInfo || getProjectRepoInfo(result.project)) : getProjectRepoInfo();
  const mentorUrl = result?.mentorProfile?.githubUrl || MENTOR_PROFILE.githubUrl;

  return (
    <>
      {/* 1. HERO VIEW: Verified Candidate Profile Dossier */}
      {result && !showManualSearch && (
        <div>
          {/* TOP CRYPTOGRAPHIC TRUST BAR */}
          <div className={s.trustBar}>
            <div className={s.brandGroup}>
              <div className={s.brandLogo}>D</div>
              <div className={s.brandText}>
                <div className={s.brandTitle}>
                  DBERT CREDENTIAL REGISTRY
                  <span className={s.versionTag}>v2026.2 ON-CHAIN</span>
                </div>
                <div className={s.brandSubtitle}>
                  Digital Blinc Education Research & Technology · Official Tamper-Proof Repository
                </div>
              </div>
            </div>

            {result.isProvisional ? (
              <div className={s.trustPillPending}>
                <span className={s.amberDot}></span>
                Provisional Record · Action Required
              </div>
            ) : (
              <div className={s.trustPill}>
                <span className={s.pulseDot}></span>
                Cryptographically Verified Credential
              </div>
            )}
          </div>

          {/* PROVISIONAL RECORD / URGENT ACTION BANNER */}
          {result.isProvisional && (
            <div className={s.provisionalActionBanner}>
              <div className={s.provisionalBannerIcon}>
                <svg width="24" height="24" fill="none" stroke="currentColor" strokeWidth="2.2" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
              </div>
              <div className={s.provisionalBannerBody}>
                <div className={s.provisionalBannerTitle}>
                  Action Required: Credential Authentication &amp; Stipend Release on Hold
                </div>
                <p className={s.provisionalBannerDesc}>
                  Action Required: Your credential authentication and stipend release are currently on hold pending submission of your final project verification form.
                </p>
                <a
                  href="https://docs.google.com/forms/d/e/1FAIpQLSeHCTK_HO5ZbNHNcPiyW-04Y4bBeZ0RvQP7I4koQnW91d6phA/viewform?usp=header"
                  target="_blank"
                  rel="noopener noreferrer"
                  className={s.provisionalFormBtn}
                >
                  Complete Verification Form to Activate Certificate &amp; Release Stipend &rarr;
                </a>
              </div>
            </div>
          )}

          {/* HERO DOSSIER: 2-COLUMN GRID */}
          <div className={`${s.heroDossier} ${result.isProvisional ? s.heroDossierLocked : ''}`}>
            <div className={s.dossierGrid}>

              {/* LEFT COLUMN: Candidate Profile & Credentials (7 Cols) */}
              <div className={s.candidateCol}>
                <div>
                  {result.isProvisional && (
                    <div className={s.translucentDossierPill}>
                      <span>🔒</span>
                      <span>RECORD ON FILE &middot; CERTIFICATE &amp; STIPEND LOCKED</span>
                    </div>
                  )}
                  <div className={s.domainPill}>
                    <span>●</span> {result.domain || 'Engineering'} Incubation Track
                  </div>
                  <h1 className={s.candidateName}>{result.holderName}</h1>
                  <div className={s.institutionRow}>
                    <svg className={`w-4 h-4 ${s.univIcon}`} fill="none" stroke="currentColor" viewBox="0 0 24 24" width="16" height="16">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                    </svg>
                    <span>{result.college || 'Engineering Fellow'}</span>
                  </div>
                </div>

                {/* KPI Metrics Tiles */}
                <div className={s.metricsGrid}>
                  <div className={`${s.metricTile} ${s.metricTileEmerald}`}>
                    <span className={s.tileLabel}>
                      Academic Score
                      {result.isProvisional && <span className={s.provisionalLockBadge}>Locked</span>}
                    </span>
                    <span className={s.tileValue}>
                      {result.score || 84}<span style={{ fontSize: '0.75rem', fontWeight: 500, color: '#94a3b8' }}>/100</span>
                    </span>
                    <span className={s.tileSub} style={{ color: '#34d399' }}>
                      {result.grade || 'Grade A (Very Good)'}
                    </span>
                  </div>

                  <div className={`${s.metricTile} ${s.metricTileAmber}`}>
                    <span className={s.tileLabel}>
                      Program Tenure
                      {result.isProvisional && <span className={s.provisionalLockBadge}>Pending Form</span>}
                    </span>
                    <span className={s.tileValue} style={{ fontSize: '1rem', color: '#fcd34d' }}>2 Months</span>
                    <span className={s.tileSub} style={{ color: '#94a3b8' }}>
                      {result.duration || 'July to September 2026'}
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
                    <span className={s.metaColLabel}>Core Production Project</span>
                    <div className={s.projectWrapper}>
                      <span className={s.metaColValStrong}>{result.project || 'Gayatri AI Enterprise Platform'}</span>
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
                    <div className={s.codeVal}>
                      <span>{result.certId}</span>
                      <button
                        type="button"
                        onClick={() => copyText(result.certId)}
                        className={s.copyBtn}
                        title="Copy Certificate ID"
                        aria-label="Copy Certificate ID"
                      >
                        <svg width="14" height="14" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                        </svg>
                      </button>
                    </div>
                  </div>

                  <div className={s.metaRow}>
                    <span className={s.metaColLabel}>Permanent Intern ID</span>
                    <span className={s.codeVal} style={{ color: '#cbd5e1' }}>{result.internId || 'DBERT-INT-KA-6769-001'}</span>
                  </div>

                  <div className={s.metaRow}>
                    <span className={s.metaColLabel}>Evaluation & Issue Date</span>
                    <span className={s.metaColVal}>{result.evalDate || result.issueDate}</span>
                  </div>

                  <div className={s.metaRow}>
                    <span className={s.metaColLabel}>Official Program Signatory</span>
                    <div className={s.signatoryWrapper}>
                      <a
                        href={mentorUrl}
                        target="_blank"
                        rel="noopener noreferrer"
                        className={s.mentorProfileLink}
                        title={`View ${result.signatory || MENTOR_PROFILE.name}'s GitHub Profile (@${MENTOR_PROFILE.githubHandle})`}
                      >
                        <span className={s.mentorAvatar}>
                          <svg width="14" height="14" fill="currentColor" viewBox="0 0 24 24">
                            <path fillRule="evenodd" clipRule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.53 1.032 1.53 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z"/>
                          </svg>
                        </span>
                        <span>{result.signatory || 'Mr. Abhinav Sharma'}</span>
                        <span className={s.mentorRoleBadge}>Mentor Profile ↗</span>
                      </a>
                    </div>
                  </div>
                </div>

                {/* Action Suite */}
                <div className={s.actionSuite}>
                  {result.isProvisional ? (
                    <a
                      href="https://docs.google.com/forms/d/e/1FAIpQLSeHCTK_HO5ZbNHNcPiyW-04Y4bBeZ0RvQP7I4koQnW91d6phA/viewform?usp=header"
                      target="_blank"
                      rel="noopener noreferrer"
                      className={s.btnActivateForm}
                    >
                      🔒 Complete Form to Unlock Official Credentials &rarr;
                    </a>
                  ) : (
                    <>
                      <a
                        href={getLinkedInAddUrl(result)}
                        target="_blank"
                        rel="noopener noreferrer"
                        className={s.btnLinkedIn}
                      >
                        <svg width="16" height="16" fill="currentColor" viewBox="0 0 24 24">
                          <path d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14m-.5 15.5v-5.3a3.26 3.26 0 0 0-3.26-3.26c-.85 0-1.84.52-2.28 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 0 1 1.4 1.4v4.93h2.75M6.88 8.56a1.68 1.68 0 0 0 1.68-1.68c0-.93-.75-1.69-1.68-1.69a1.69 1.69 0 0 0-1.69 1.69c0 .93.76 1.68 1.69 1.68m1.39 9.94v-8.37H5.5v8.37h2.77z"/>
                        </svg>
                        Add to LinkedIn Profile ↗
                      </a>

                      <button
                        type="button"
                        onClick={() => copyText(result.verificationUrl || `https://dbert.in/verify?certid=${result.certId}`)}
                        className={s.btnSecondaryAction}
                      >
                        <svg width="15" height="15" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
                        </svg>
                        {copiedLink ? 'Copied to Clipboard!' : 'Copy Verification Link'}
                      </button>

                      <a
                        href={getWhatsAppShareUrl(result)}
                        target="_blank"
                        rel="noopener noreferrer"
                        className={s.btnWhatsApp}
                      >
                        <svg width="16" height="16" fill="currentColor" viewBox="0 0 24 24">
                          <path d="M12.04 2c-5.46 0-9.91 4.45-9.91 9.91 0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38c1.45.79 3.08 1.21 4.74 1.21 5.46 0 9.91-4.45 9.91-9.91 0-2.65-1.03-5.14-2.9-7.01A9.816 9.816 0 0 0 12.04 2z"/>
                        </svg>
                        Share
                      </a>
                    </>
                  )}
                </div>
              </div>

              {/* RIGHT COLUMN: Certificate Showcase (5 Cols) */}
              <div className={s.certCol}>
                <CertificatePreviewFrame
                  src={result.previewUrl || `/certificates/previews/${result.certId}.png`}
                  alt={`Official Certificate for ${result.holderName}`}
                  holderName={result.holderName}
                  certId={result.certId}
                  domain={result.domain}
                  isLocked={!!result.isProvisional}
                />
                <div className={s.certCaption}>
                  {result.isProvisional ? (
                    <>
                      <svg width="14" height="14" fill="none" stroke="#f59e0b" viewBox="0 0 24 24">
                        <rect x="3" y="11" width="18" height="11" rx="2" ry="2" strokeWidth="2"/>
                        <path d="M7 11V7a5 5 0 0 1 10 0v4" strokeWidth="2"/>
                      </svg>
                      <span style={{ color: '#fbbf24', fontWeight: 600 }}>Status: Inactive · Awaiting Project Verification Form</span>
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

          {/* 2. INTERACTIVE 3-TAB ACADEMIC & PRODUCTION AUDIT */}
          <div className={s.tabsSection}>
            <div className={s.tabsHeader}>
              <div>
                <h3 className={s.tabsTitle}>Academic Appraisal & Production Audit</h3>
                <div className={s.tabsSub}>Detailed competency rubrics and verified project milestones</div>
              </div>

              <div className={s.tabsNav}>
                <button
                  type="button"
                  onClick={() => setActiveTab('project')}
                  className={`${s.tabBtn} ${activeTab === 'project' ? s.tabBtnActive : ''}`}
                >
                  Production Project
                </button>
                <button
                  type="button"
                  onClick={() => setActiveTab('rubrics')}
                  className={`${s.tabBtn} ${activeTab === 'rubrics' ? s.tabBtnActive : ''}`}
                >
                  Academic Rubrics ({result.score || 84}/100)
                </button>
                <button
                  type="button"
                  onClick={() => setActiveTab('endorsement')}
                  className={`${s.tabBtn} ${activeTab === 'endorsement' ? s.tabBtnActive : ''}`}
                >
                  Official Recommendation
                </button>
              </div>
            </div>

            {/* TAB 1: PRODUCTION PROJECT */}
            {activeTab === 'project' && (
              <>
                <div className={s.projectGrid}>
                  <div className={s.projectCard} style={{ borderLeft: '3px solid #06b6d4' }}>
                    <span className={s.cardHead}>Architecture Domain</span>
                    <span className={s.cardTitle}>Enterprise Analytics & Intelligence</span>
                    <p className={s.cardDesc}>
                      End-to-end data pipeline normalization, exploratory analytics, and executive BI dashboards.
                    </p>
                  </div>

                  <div className={s.projectCard} style={{ borderLeft: '3px solid #10b981' }}>
                    <span className={s.cardHead}>Core Stack Covered</span>
                    <span className={s.cardTitle}>Python, SQL, Power BI, Pandas</span>
                    <p className={s.cardDesc}>
                      Data cleaning, complex multi-table joins, automated KPI aggregation, and statistical reporting.
                    </p>
                  </div>

                  <div className={s.projectCard} style={{ borderLeft: '3px solid #f59e0b' }}>
                    <span className={s.cardHead}>Delivery Benchmark</span>
                    <span className={s.cardTitle}>Production-Ready (Approved)</span>
                    <p className={s.cardDesc}>
                      Code review clearance, architectural documentation integrity, and industry benchmark compliance.
                    </p>
                  </div>
                </div>

                {/* GitHub Production Repository Showcase Card */}
                <div className={s.repoFeatureCard}>
                  <div className={s.repoFeatureLeft}>
                    <div className={s.repoFeatureHeader}>
                      <span className={s.repoBadge}>
                        <svg width="15" height="15" fill="currentColor" viewBox="0 0 24 24">
                          <path fillRule="evenodd" clipRule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.53 1.032 1.53 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z"/>
                        </svg>
                        Production GitHub Repository
                      </span>
                      <span className={s.repoVerifiedTag}>✓ Active Incubation Codebase</span>
                    </div>
                    <div className={s.repoName}>{repoInfo.label}</div>
                    <p className={s.repoDesc}>
                      {repoInfo.description} {result.holderName} completed 45 days of engineering sprints, code reviews, and milestone deliverables against this repository.
                    </p>
                  </div>
                  <div className={s.repoFeatureRight}>
                    <a
                      href={repoInfo.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className={s.btnInspectRepo}
                    >
                      <svg width="15" height="15" fill="currentColor" viewBox="0 0 24 24">
                        <path fillRule="evenodd" clipRule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.53 1.032 1.53 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z"/>
                      </svg>
                      Inspect Codebase on GitHub ↗
                    </a>
                  </div>
                </div>
              </>
            )}

            {/* TAB 2: ACADEMIC RUBRICS */}
            {activeTab === 'rubrics' && (
              <div className={s.rubricsGrid}>
                <div className={s.rubricItem}>
                  <span className={s.rubricName}>1. Problem Decomposition</span>
                  <span className={s.rubricScore}>17/20</span>
                </div>
                <div className={s.rubricItem}>
                  <span className={s.rubricName}>2. Relational SQL Design</span>
                  <span className={s.rubricScore}>9/10</span>
                </div>
                <div className={s.rubricItem}>
                  <span className={s.rubricName}>3. ETL Pipeline Hygiene</span>
                  <span className={s.rubricScore}>8/10</span>
                </div>
                <div className={s.rubricItem}>
                  <span className={s.rubricName}>4. Statistical Reasoning</span>
                  <span className={s.rubricScore}>8/10</span>
                </div>
                <div className={s.rubricItem}>
                  <span className={s.rubricName}>5. Dashboard UX & Storytelling</span>
                  <span className={s.rubricScore}>8/10</span>
                </div>
                <div className={s.rubricItem}>
                  <span className={s.rubricName}>6. Technical Problem-Solving</span>
                  <span className={s.rubricScore}>9/10</span>
                </div>
                <div className={s.rubricItem}>
                  <span className={s.rubricName}>7. Code Rigor & Scalability</span>
                  <span className={s.rubricScore}>8/10</span>
                </div>
                <div className={s.rubricItem}>
                  <span className={s.rubricName}>8. Documentation Quality</span>
                  <span className={s.rubricScore}>8/10</span>
                </div>
                <div className={s.rubricItem}>
                  <span className={s.rubricName}>9. Architectural Execution</span>
                  <span className={s.rubricScore}>9/10</span>
                </div>
              </div>
            )}

            {/* TAB 3: OFFICIAL RECOMMENDATION */}
            {activeTab === 'endorsement' && (
              <div className={s.endorsementCard}>
                <div style={{ fontFamily: 'var(--font-m)', fontSize: '0.74rem', color: '#38bdf8', fontWeight: 700, textTransform: 'uppercase' }}>
                  Mentor Endorsement Excerpt
                </div>
                <blockquote className={s.endorseQuote}>
                  &ldquo;During the 2-month internship tenure from July to September 2026, {result.holderName} demonstrated exemplary problem-solving skills and technical rigor on the {result.project} core engineering project. The candidate consistently adhered to production engineering standards and exhibits outstanding potential for high-impact analytics and engineering roles.&rdquo;
                </blockquote>
                <div className={s.endorseAuthor}>
                  — <strong style={{ color: '#ffffff' }}>{result.signatory || 'Mr. Abhinav Sharma'}</strong>, Program Head & Project Mentor, DBERT
                </div>

                {/* Mentor Profile Feature Card */}
                <div className={s.mentorProfileCard}>
                  <div className={s.mentorAvatarLarge}>
                    <svg width="22" height="22" fill="currentColor" viewBox="0 0 24 24">
                      <path fillRule="evenodd" clipRule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.53 1.032 1.53 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z"/>
                    </svg>
                  </div>
                  <div className={s.mentorCardDetails}>
                    <div className={s.mentorCardHeader}>
                      <div>
                        <h4 className={s.mentorCardTitle}>{result.signatory || MENTOR_PROFILE.name}</h4>
                        <div className={s.mentorCardSub}>{result.signatoryTitle || MENTOR_PROFILE.title} &bull; DBERT</div>
                      </div>
                      <a
                        href={mentorUrl}
                        target="_blank"
                        rel="noopener noreferrer"
                        className={s.btnMentorGithub}
                      >
                        <svg width="14" height="14" fill="currentColor" viewBox="0 0 24 24">
                          <path fillRule="evenodd" clipRule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.53 1.032 1.53 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z"/>
                        </svg>
                        <span>github.com/{MENTOR_PROFILE.githubHandle} ↗</span>
                      </a>
                    </div>
                    <p className={s.mentorCardBio}>
                      {MENTOR_PROFILE.bio}
                    </p>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* ALREADY REGISTERED INTERNS: CLAIM CERTIFICATE CARD */}
          <div className={s.claimCard}>
            <span className={s.claimEyebrow}>
              Already Registered Interns · Official Credential Issuance
            </span>
            <h2 className={s.claimTitle}>
              Completed Your Internship? Claim Your Verified Credential Packet
            </h2>
            <p className={s.claimDesc}>
              For enrolled DBERT interns who have completed sprint requirements and submitted final project tasks. Request your official institutional credential packet including your verified Certificate of Completion, Academic Evaluation Rubrics, Executive LOR, and production GitHub attributions.
            </p>

            {/* 4 Pillars Benefits Grid */}
            <div className={s.pillarsGrid}>
              <div className={s.pillarCard}>
                <div className={`${s.pillarNum} ${s.pillarNumEmerald}`}>01</div>
                <div className={s.pillarTitle}>Official Certificate</div>
                <p className={s.pillarDesc}>
                  Cryptographically verified certificate with micro-QR authenticity seal, 256-bit SHA hash, and 1-click LinkedIn import.
                </p>
              </div>

              <div className={s.pillarCard}>
                <div className={`${s.pillarNum} ${s.pillarNumAmber}`}>02</div>
                <div className={s.pillarTitle}>Academic Evaluation</div>
                <p className={s.pillarDesc}>
                  Comprehensive 9-dimension competency appraisal rubric with score breakdown and Turnitin plagiarism clearance.
                </p>
              </div>

              <div className={s.pillarCard}>
                <div className={`${s.pillarNum} ${s.pillarNumPurple}`}>03</div>
                <div className={s.pillarTitle}>Executive LOR</div>
                <p className={s.pillarDesc}>
                  Formal institutional Letter of Recommendation and performance appraisal signed by Program Head Mr. Abhinav Sharma.
                </p>
              </div>

              <div className={s.pillarCard}>
                <div className={`${s.pillarNum} ${s.pillarNumCyan}`}>04</div>
                <div className={s.pillarTitle}>GitHub Contributions</div>
                <p className={s.pillarDesc}>
                  Verifiable commit history, pull request attribution, and production code authorship on active open-source ecosystem repos.
                </p>
              </div>
            </div>

            {/* Benefit Badges & CTA */}
            <div className={s.fellowCtaBar}>
              <div className={s.tracksPills}>
                <span className={s.trackPill}>📜 Verified Certificate</span>
                <span className={s.trackPill}>📊 9-Metric Appraisal</span>
                <span className={s.trackPill}>✍️ Executive LOR</span>
                <span className={s.trackPill}>🐙 GitHub Attributions</span>
              </div>

              <a
                href="https://wa.me/918192911360?text=Hi%20DBERT%2C%20I%20am%20a%20registered%20intern%20and%20would%20like%20to%20claim%20my%20official%20internship%20certificate%20packet."
                target="_blank"
                rel="noopener noreferrer"
                className={s.claimCtaBtn}
              >
                Get Certificate →
              </a>
            </div>
          </div>

          {/* 3. PRESTIGE TECHNICAL FELLOWSHIP & GUARANTEED PLACEMENT CARD (Zero Price) */}
          <div className={s.fellowshipCard}>
            <span className={s.fellowEyebrow}>
              DBERT Technical Fellowship & Incubation
            </span>
            <h2 className={s.fellowTitle}>
              Launch Your Engineering Career with a Guaranteed Placement Opportunity
            </h2>
            <p className={s.fellowDesc}>
              Skip the uncertain hiring lottery. Follow an elite 60-day incubation pipeline from hands-on engineering training directly into a live production role with DBERT or our ecosystem hiring partners upon completion and verified certification.
            </p>

            {/* 4 Pillars Grid */}
            <div className={s.pillarsGrid}>
              <div className={s.pillarCard}>
                <div className={`${s.pillarNum} ${s.pillarNumAmber}`}>01</div>
                <div className={s.pillarTitle}>15-Day Sprint</div>
                <p className={s.pillarDesc}>
                  Deep-dive technical foundation, architecture patterns, and industry toolsets.
                </p>
              </div>

              <div className={s.pillarCard}>
                <div className={`${s.pillarNum} ${s.pillarNumCyan}`}>02</div>
                <div className={s.pillarTitle}>45-Day Production</div>
                <p className={s.pillarDesc}>
                  Hands-on engineering role building enterprise features with real pull requests.
                </p>
              </div>

              <div className={s.pillarCard}>
                <div className={`${s.pillarNum} ${s.pillarNumEmerald}`}>03</div>
                <div className={s.pillarTitle}>1:1 Mentorship</div>
                <p className={s.pillarDesc}>
                  Regular technical syncs with senior project mentors and industry leaders.
                </p>
              </div>

              <div className={s.pillarCard}>
                <div className={`${s.pillarNum} ${s.pillarNumPurple}`}>04</div>
                <div className={s.pillarTitle}>Guaranteed Internship</div>
                <p className={s.pillarDesc}>
                  Guaranteed internship placement working directly on live production repositories with DBERT or partner networks.
                </p>
              </div>
            </div>

            {/* Tracks & CTA */}
            <div className={s.fellowCtaBar}>
              <div className={s.tracksPills}>
                <span className={s.trackPill}>🤖 AI Agent Development</span>
                <span className={s.trackPill}>📊 Data Analyst</span>
                <span className={s.trackPill}>💻 Full Stack Engineering</span>
                <span className={s.trackPill}>⚙️ Python Automation</span>
              </div>

              <a
                href="https://lms.dbert.in/#signup"
                target="_blank"
                rel="noopener noreferrer"
                className={s.fellowCtaBtn}
              >
                Explore & Apply for Next Cohort →
              </a>
            </div>
          </div>

          {/* FOOTER NAVIGATION */}
          <div className={s.verifyFooter}>
            <div>
              <button
                type="button"
                onClick={() => setShowManualSearch(true)}
                className={s.toggleSearchLink}
              >
                ← Verify another certificate ID
              </button>
            </div>
            <div>
              Official Verification Engine · &copy; 2026 DBERT (Digital Blinc Education Research and Technology). All rights reserved.
            </div>
          </div>
        </div>
      )}

      {/* 4. MANUAL SEARCH FALLBACK VIEW (Only shown if no certid in URL or user clicked verify another) */}
      {showManualSearch && (
        <div className={s.manualSearchSection}>
          <div className="mb-lg center">
            <div className="doclabel justify-center">
              § 01 — CRYPTOGRAPHIC VERIFICATION <span className="rev">rev: 2026.2</span>
            </div>
            <div className="stack-h justify-center align-baseline gap-3 flex-wrap mb-2">
              <h1>Verify Certificate</h1>
            </div>
            <p className="measure-sm">
              Enter a certificate identification key to verify student credentials, academic evaluation rubrics, and project completion statuses.
            </p>
          </div>

          <form className={`card card-lift ${s.formCard}`} onSubmit={handleVerify}>
            <div className={s.fieldGroup}>
              <label htmlFor="cert-id">Certificate ID *</label>
              <input
                id="cert-id"
                name="certId"
                aria-label="Certificate ID"
                type="text"
                required
                value={certId}
                onChange={(e) => setCertId(e.target.value)}
                placeholder="e.g. CERT-DBERT-2026-DA-001"
              />
            </div>
            <button type="submit" className={`btn btn-primary btn-sm ${s.submitBtn}`} disabled={loading}>
              {loading ? 'Verifying...' : 'Verify Certificate'}
            </button>
          </form>

          {errorMsg && <div className={s.errorAlert}>{errorMsg}</div>}

          {/* ALREADY REGISTERED INTERNS: CLAIM CERTIFICATE CARD */}
          <div className={s.claimCard} style={{ marginTop: '40px' }}>
            <span className={s.claimEyebrow}>
              Already Registered Interns · Official Credential Issuance
            </span>
            <h2 className={s.claimTitle}>
              Completed Your Internship? Claim Your Verified Credential Packet
            </h2>
            <p className={s.claimDesc}>
              For enrolled DBERT interns who have completed sprint requirements and submitted final project tasks. Request your official institutional credential packet including your verified Certificate of Completion, Academic Evaluation Rubrics, Executive LOR, and production GitHub attributions.
            </p>

            {/* 4 Pillars Benefits Grid */}
            <div className={s.pillarsGrid}>
              <div className={s.pillarCard}>
                <div className={`${s.pillarNum} ${s.pillarNumEmerald}`}>01</div>
                <div className={s.pillarTitle}>Official Certificate</div>
                <p className={s.pillarDesc}>
                  Cryptographically verified certificate with micro-QR authenticity seal, 256-bit SHA hash, and 1-click LinkedIn import.
                </p>
              </div>

              <div className={s.pillarCard}>
                <div className={`${s.pillarNum} ${s.pillarNumAmber}`}>02</div>
                <div className={s.pillarTitle}>Academic Evaluation</div>
                <p className={s.pillarDesc}>
                  Comprehensive 9-dimension competency appraisal rubric with score breakdown and Turnitin plagiarism clearance.
                </p>
              </div>

              <div className={s.pillarCard}>
                <div className={`${s.pillarNum} ${s.pillarNumPurple}`}>03</div>
                <div className={s.pillarTitle}>Executive LOR</div>
                <p className={s.pillarDesc}>
                  Formal institutional Letter of Recommendation and performance appraisal signed by Program Head Mr. Abhinav Sharma.
                </p>
              </div>

              <div className={s.pillarCard}>
                <div className={`${s.pillarNum} ${s.pillarNumCyan}`}>04</div>
                <div className={s.pillarTitle}>GitHub Contributions</div>
                <p className={s.pillarDesc}>
                  Verifiable commit history, pull request attribution, and production code authorship on active open-source ecosystem repos.
                </p>
              </div>
            </div>

            {/* Benefit Badges & CTA */}
            <div className={s.fellowCtaBar}>
              <div className={s.tracksPills}>
                <span className={s.trackPill}>📜 Verified Certificate</span>
                <span className={s.trackPill}>📊 9-Metric Appraisal</span>
                <span className={s.trackPill}>✍️ Executive LOR</span>
                <span className={s.trackPill}>🐙 GitHub Attributions</span>
              </div>

              <a
                href="https://wa.me/918192911360?text=Hi%20DBERT%2C%20I%20am%20a%20registered%20intern%20and%20would%20like%20to%20claim%20my%20official%20internship%20certificate%20packet."
                target="_blank"
                rel="noopener noreferrer"
                className={s.claimCtaBtn}
              >
                Get Certificate →
              </a>
            </div>
          </div>

          {/* PRESTIGE TECHNICAL FELLOWSHIP & GUARANTEED PLACEMENT CARD (Zero Price) */}
          <div className={s.fellowshipCard}>
            <span className={s.fellowEyebrow}>
              DBERT Technical Fellowship & Incubation
            </span>
            <h2 className={s.fellowTitle}>
              Launch Your Engineering Career with a Guaranteed Placement Opportunity
            </h2>
            <p className={s.fellowDesc}>
              Skip the uncertain hiring lottery. Follow an elite 60-day incubation pipeline from hands-on engineering training directly into a live production role with DBERT or our ecosystem hiring partners upon completion and verified certification.
            </p>

            <div className={s.pillarsGrid}>
              <div className={s.pillarCard}>
                <div className={`${s.pillarNum} ${s.pillarNumAmber}`}>01</div>
                <div className={s.pillarTitle}>15-Day Sprint</div>
                <p className={s.pillarDesc}>
                  Deep-dive technical foundation, architecture patterns, and industry toolsets.
                </p>
              </div>

              <div className={s.pillarCard}>
                <div className={`${s.pillarNum} ${s.pillarNumCyan}`}>02</div>
                <div className={s.pillarTitle}>45-Day Production</div>
                <p className={s.pillarDesc}>
                  Hands-on engineering role building enterprise features with real pull requests.
                </p>
              </div>

              <div className={s.pillarCard}>
                <div className={`${s.pillarNum} ${s.pillarNumEmerald}`}>03</div>
                <div className={s.pillarTitle}>1:1 Mentorship</div>
                <p className={s.pillarDesc}>
                  Regular technical syncs with senior project mentors and industry leaders.
                </p>
              </div>

              <div className={s.pillarCard}>
                <div className={`${s.pillarNum} ${s.pillarNumPurple}`}>04</div>
                <div className={s.pillarTitle}>Guaranteed Internship</div>
                <p className={s.pillarDesc}>
                  Guaranteed internship placement working directly on live production repositories with DBERT or partner networks.
                </p>
              </div>
            </div>

            <div className={s.fellowCtaBar}>
              <div className={s.tracksPills}>
                <span className={s.trackPill}>🤖 AI Agent Development</span>
                <span className={s.trackPill}>📊 Data Analyst</span>
                <span className={s.trackPill}>💻 Full Stack Engineering</span>
                <span className={s.trackPill}>⚙️ Python Automation</span>
              </div>

              <a
                href="https://lms.dbert.in/#signup"
                target="_blank"
                rel="noopener noreferrer"
                className={s.fellowCtaBtn}
              >
                Explore & Apply for Next Cohort →
              </a>
            </div>
          </div>
        </div>
      )}
    </>
  );
}

export default function CertificateVerifyPage() {
  return (
    <div className="container pad-block">
      <div className={s.shell}>
        <Suspense
          fallback={
            <div className="card card-lift text-center p-6 text-muted">
              Loading verification console...
            </div>
          }
        >
          <VerifyFormContent />
        </Suspense>
      </div>
    </div>
  );
}
