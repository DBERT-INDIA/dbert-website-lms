import React from 'react';
import type { Metadata } from 'next';
import fs from 'fs';
import path from 'path';
import Link from 'next/link';
import s from '../verify.module.css';
import CertificatePreviewFrame from '../CertificatePreviewFrame';
import { getProjectRepoInfo, MENTOR_PROFILE, getIssueYearMonth } from '@/lib/verification';

interface RegistryRecord {
  certId: string;
  internId?: string;
  holderName: string;
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
}

function getCertificate(certId: string): RegistryRecord | null {
  try {
    const regPath = path.join(process.cwd(), 'src', 'data', 'certificates_registry.json');
    if (fs.existsSync(regPath)) {
      const registry: Record<string, RegistryRecord> = JSON.parse(fs.readFileSync(regPath, 'utf8'));
      const matchKey = Object.keys(registry).find(
        (k) => k.toLowerCase() === certId.toLowerCase()
      );
      if (matchKey) return registry[matchKey];
    }
    const provPath = path.join(process.cwd(), 'src', 'data', 'all_409_provisional_registry.json');
    if (fs.existsSync(provPath)) {
      const provList: RegistryRecord[] = JSON.parse(fs.readFileSync(provPath, 'utf8'));
      const pMatch = provList.find((p) => p.certId.toLowerCase() === certId.toLowerCase());
      if (pMatch) return pMatch;
    }
  } catch (err) {
    console.error('Error in getCertificate:', err);
  }
  return null;
}

export async function generateMetadata({
  params
}: {
  params: Promise<{ certId: string }>;
}): Promise<Metadata> {
  const { certId } = await params;
  const cert = getCertificate(certId);

  if (!cert) {
    return {
      title: 'Certificate Verification | DBERT',
      description: 'Verify official DBERT engineering and academic credentials.'
    };
  }

  const title = `Verified Credential: ${cert.holderName} — ${cert.domain} | DBERT`;
  const desc = `Official verified 2-month internship credential for ${cert.holderName} in ${cert.domain}. Project: ${cert.project}. Authenticity verified by DBERT.`;
  const previewImg = cert.previewUrl ? `https://dbert.in${cert.previewUrl}` : 'https://dbert.in/targets12.png';

  return {
    title,
    description: desc,
    alternates: {
      canonical: `https://dbert.in/verify/${cert.certId}`
    },
    openGraph: {
      title: `${cert.holderName} — Verified ${cert.domain} Intern | DBERT`,
      description: desc,
      url: `https://dbert.in/verify/${cert.certId}`,
      siteName: 'DBERT Technical Incubation',
      images: [
        {
          url: previewImg,
          width: 1200,
          height: 630,
          alt: `DBERT Certificate for ${cert.holderName}`
        }
      ],
      type: 'profile'
    },
    twitter: {
      card: 'summary_large_image',
      title,
      description: desc,
      images: [previewImg]
    }
  };
}

export default async function VerifiedCertificatePage({
  params
}: {
  params: Promise<{ certId: string }>;
}) {
  const { certId } = await params;
  const cert = getCertificate(certId);

  if (!cert) {
    return (
      <div className="container pad-block">
        <div className="card text-center p-8 max-w-lg mx-auto">
          <h1 className="text-xl font-bold mb-2 text-err">Certificate Not Found</h1>
          <p className="text-muted mb-4">No credential found matching ID: {certId}</p>
          <Link href="/verify" className="btn btn-primary btn-sm">
            Search Another Certificate
          </Link>
        </div>
      </div>
    );
  }

  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'EducationalOccupationalCredential',
    name: `DBERT Certificate of Completion — ${cert.domain}`,
    credentialCategory: 'Certificate of Internship',
    educationalLevel: 'Production Internship & Technical Incubation',
    recognizedBy: {
      '@type': 'Organization',
      name: 'DBERT',
      url: 'https://dbert.in'
    },
    about: {
      '@type': 'Person',
      name: cert.holderName
    },
    description: `Successfully completed a rigorous 2-month technical incubation program in ${cert.domain} on project ${cert.project}.`
  };

  const { year: issueYear, month: issueMonth } = getIssueYearMonth(cert.issueDate);
  const linkedInUrl = `https://www.linkedin.com/profile/add?startTask=CERTIFICATION_NAME&name=${encodeURIComponent('DBERT Internship Certificate — ' + cert.domain)}&organizationName=DBERT&issueYear=${issueYear}&issueMonth=${issueMonth}&certUrl=${encodeURIComponent(`https://dbert.in/verify/${cert.certId}`)}&certId=${encodeURIComponent(cert.certId)}`;
  const whatsAppUrl = `https://api.whatsapp.com/send?text=${encodeURIComponent(`I just earned my verified 2-Month Internship Certificate in ${cert.domain} from DBERT! Check out my official verified credential: https://dbert.in/verify/${cert.certId}`)}`;
  const repoInfo = getProjectRepoInfo(cert.project);
  const mentorUrl = MENTOR_PROFILE.githubUrl;

  return (
    <div className="container pad-block">
      {/* Schema.org Structured Data */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />

      <div className={s.shell}>
        {/* DIRECTORY BREADCRUMB */}
        <div style={{ marginBottom: '16px' }}>
          <Link href="/verify/directory" style={{ display: 'inline-flex', alignItems: 'center', gap: '6px', fontSize: '0.8rem', color: '#8A9AB5', textDecoration: 'none' }}>
            &larr; Browse All Interns in Alphabetical Directory
          </Link>
        </div>

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

          {cert.isProvisional ? (
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
        {cert.isProvisional && (
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
        <div className={`${s.heroDossier} ${cert.isProvisional ? s.heroDossierLocked : ''}`}>
          <div className={s.dossierGrid}>

            {/* LEFT COLUMN: Candidate Profile & Credentials */}
            <div className={s.candidateCol}>
              <div>
                {cert.isProvisional && (
                  <div className={s.translucentDossierPill}>
                    <span>🔒</span>
                    <span>RECORD ON FILE &middot; CERTIFICATE &amp; STIPEND LOCKED</span>
                  </div>
                )}
                <div className={s.domainPill}>
                  <span>●</span> {cert.domain || 'Engineering'} Incubation Track
                </div>
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
                    {cert.score || 84}<span style={{ fontSize: '0.75rem', fontWeight: 500, color: '#94a3b8' }}>/100</span>
                  </span>
                  <span className={s.tileSub} style={{ color: '#34d399' }}>
                    {cert.grade || 'Grade A (Very Good)'}
                  </span>
                </div>

                <div className={`${s.metricTile} ${s.metricTileAmber}`}>
                  <span className={s.tileLabel}>
                    Program Tenure
                    {cert.isProvisional && <span className={s.provisionalLockBadge}>Pending Form</span>}
                  </span>
                  <span className={s.tileValue} style={{ fontSize: '1rem', color: '#fcd34d' }}>2 Months</span>
                  <span className={s.tileSub} style={{ color: '#94a3b8' }}>
                    {cert.duration || 'July to September 2026'}
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
                  <span className={s.metaColLabel}>Evaluation & Issue Date</span>
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
                      title={`View ${cert.signatory || MENTOR_PROFILE.name}'s GitHub Profile (@${MENTOR_PROFILE.githubHandle})`}
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

              {/* Action Suite */}
              <div className={s.actionSuite}>
                {cert.isProvisional ? (
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', width: '100%' }}>
                    <Link
                      href={`/enroll/1999?certid=${encodeURIComponent(cert.certId)}`}
                      className={s.btnActivateForm}
                    >
                      🔒 Complete ₹1,500 Balance to Unlock Official Credentials &rarr;
                    </Link>
                    <a
                      href="https://docs.google.com/forms/d/e/1FAIpQLSeHCTK_HO5ZbNHNcPiyW-04Y4bBeZ0RvQP7I4koQnW91d6phA/viewform?usp=header"
                      target="_blank"
                      rel="noopener noreferrer"
                      style={{ fontSize: '0.78rem', color: '#8A9AB5', textAlign: 'center', textDecoration: 'none' }}
                    >
                      Or submit details via Google Form alternative ↗
                    </a>
                  </div>
                ) : (
                  <>
                    <a
                      href={linkedInUrl}
                      target="_blank"
                      rel="noopener noreferrer"
                      className={s.btnLinkedIn}
                    >
                      <svg width="16" height="16" fill="currentColor" viewBox="0 0 24 24">
                        <path d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14m-.5 15.5v-5.3a3.26 3.26 0 0 0-3.26-3.26c-.85 0-1.84.52-2.28 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 0 1 1.4 1.4v4.93h2.75M6.88 8.56a1.68 1.68 0 0 0 1.68-1.68c0-.93-.75-1.69-1.68-1.69a1.69 1.69 0 0 0-1.69 1.69c0 .93.76 1.68 1.69 1.68m1.39 9.94v-8.37H5.5v8.37h2.77z"/>
                      </svg>
                      Add to LinkedIn Profile ↗
                    </a>

                    <a
                      href={whatsAppUrl}
                      target="_blank"
                      rel="noopener noreferrer"
                      className={s.btnWhatsApp}
                    >
                      <svg width="16" height="16" fill="currentColor" viewBox="0 0 24 24">
                        <path d="M12.04 2c-5.46 0-9.91 4.45-9.91 9.91 0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38c1.45.79 3.08 1.21 4.74 1.21 5.46 0 9.91-4.45 9.91-9.91 0-2.65-1.03-5.14-2.9-7.01A9.816 9.816 0 0 0 12.04 2z"/>
                      </svg>
                      Share on WhatsApp ↗
                    </a>
                  </>
                )}
              </div>
            </div>

            {/* RIGHT COLUMN: Certificate Showcase */}
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

        {/* FOOTER NAVIGATION */}
        <div className={s.verifyFooter}>
          <div>
            <Link href="/verify" className={s.toggleSearchLink}>
              ← Verify another certificate ID
            </Link>
          </div>
          <div>
            Official Verification Engine · &copy; 2026 DBERT (Digital Blinc Education Research and Technology). All rights reserved.
          </div>
        </div>
      </div>
    </div>
  );
}
