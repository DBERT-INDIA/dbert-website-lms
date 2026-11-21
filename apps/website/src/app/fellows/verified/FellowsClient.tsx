'use client';

import React, { useState, useMemo } from 'react';
import Link from 'next/link';
import {
  Search,
  ShieldCheck,
  CheckCircle2,
  ExternalLink,
  BookOpen,
  Award,
  Globe,
  GraduationCap,
  Sparkles
} from 'lucide-react';
import styles from './fellows.module.css';

function LinkedInIcon({ size = 13 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="currentColor">
      <path d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14m-.5 15.5v-5.3a3.26 3.26 0 0 0-3.26-3.26c-.85 0-1.84.52-2.28 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 0 1 1.4 1.4v4.93h2.75M6.88 8.56a1.68 1.68 0 0 0 1.68-1.68c0-.93-.75-1.69-1.68-1.69a1.69 1.69 0 0 0-1.69 1.69c0 .93.76 1.68 1.69 1.68m1.39 9.94v-8.37H5.5v8.37h2.77z"/>
    </svg>
  );
}

function GithubIcon({ size = 13 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="currentColor">
      <path fillRule="evenodd" clipRule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.53 1.032 1.53 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z"/>
    </svg>
  );
}

export interface VerifiedFellowItem {
  certId: string;
  name: string;
  domain: string;
  college: string;
  score: number;
  grade: string;
  project: string;
  isVerified: boolean;
  verificationUrl: string;
  linkedinUrl?: string | null;
  articleTitle?: string | null;
  articleSlug?: string | null;
  articleUrl?: string | null;
  githubUrl?: string | null;
  demoUrl?: string | null;
  previewUrl?: string;
}

interface FellowsClientProps {
  fellows: VerifiedFellowItem[];
}

export default function FellowsClient({ fellows }: FellowsClientProps) {
  const [searchQuery, setSearchQuery] = useState('');
  const [activeDomain, setActiveDomain] = useState('ALL');
  const [filterWithLinkedIn, setFilterWithLinkedIn] = useState(false);
  const [filterWithArticle, setFilterWithArticle] = useState(false);
  const [filterDistinction, setFilterDistinction] = useState(false);

  // Extract unique domains
  const domainList = useMemo(() => {
    const set = new Set<string>();
    fellows.forEach(f => {
      if (f.domain) set.add(f.domain);
    });
    return Array.from(set).sort();
  }, [fellows]);

  // Filtered & searched fellows
  const filteredFellows = useMemo(() => {
    return fellows.filter(f => {
      // Domain filter
      if (activeDomain !== 'ALL' && f.domain !== activeDomain) {
        return false;
      }

      // Feature toggles
      if (filterWithLinkedIn && !f.linkedinUrl) return false;
      if (filterWithArticle && !f.articleUrl) return false;
      if (filterDistinction && (f.score || 0) < 85) return false;

      // Text search
      if (searchQuery.trim()) {
        const q = searchQuery.toLowerCase();
        const inName = f.name.toLowerCase().includes(q);
        const inCert = f.certId.toLowerCase().includes(q);
        const inCollege = (f.college || '').toLowerCase().includes(q);
        const inDomain = (f.domain || '').toLowerCase().includes(q);
        const inProject = (f.project || '').toLowerCase().includes(q);
        const inArticle = (f.articleTitle || '').toLowerCase().includes(q);
        if (!inName && !inCert && !inCollege && !inDomain && !inProject && !inArticle) {
          return false;
        }
      }

      return true;
    });
  }, [fellows, activeDomain, filterWithLinkedIn, filterWithArticle, filterDistinction, searchQuery]);

  return (
    <div className={styles.pageWrapper}>
      {/* HERO SECTION */}
      <section className={styles.heroSection}>
        <div className={styles.heroContent}>
          <div className={styles.badgePill}>
            <ShieldCheck size={16} />
            MSME Registered &bull; 100% Cryptographic Verification
          </div>
          <h1 className={styles.heroTitle}>
            Verified Fellows &amp; Published Engineering Case Studies
          </h1>
          <p className={styles.heroSubtitle}>
            Authentic graduate outcomes from DBERT Technical Incubation. Every fellow is verified through immutable QR credentials, 100-mark Turnitin evaluation rubrics, authentic LinkedIn peer shares, and production open-source architectures.
          </p>

          {/* STATS BENTO */}
          <div className={styles.statsGrid}>
            <div className={styles.statCard}>
              <div className={styles.statVal}>470+</div>
              <div className={styles.statLabel}>Incubation Fellows</div>
            </div>
            <div className={styles.statCard}>
              <div className={styles.statVal}>100%</div>
              <div className={styles.statLabel}>Cryptographic Integrity</div>
            </div>
            <div className={styles.statCard}>
              <div className={styles.statVal}>12+</div>
              <div className={styles.statLabel}>Published Case Studies</div>
            </div>
            <div className={styles.statCard}>
              <div className={styles.statVal}>Govt. MSME</div>
              <div className={styles.statLabel}>UDYAM-UP-29-0109046</div>
            </div>
          </div>
        </div>
      </section>

      {/* MAIN CONTENT AREA */}
      <main className={styles.container}>
        {/* CONTROLS */}
        <div className={styles.controlsWrapper}>
          {/* SEARCH INPUT */}
          <div className={styles.searchBarWrapper}>
            <Search className={styles.searchIcon} size={18} />
            <input
              type="text"
              className={styles.searchInput}
              placeholder="Search by candidate name, certificate ID, college, stack, or published paper..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>

          {/* DOMAIN STRIP */}
          <div className={styles.domainFilterStrip}>
            <button
              className={`${styles.domainFilterBtn} ${activeDomain === 'ALL' ? styles.domainFilterBtnActive : ''}`}
              onClick={() => setActiveDomain('ALL')}
            >
              All Domains ({fellows.length})
            </button>
            {domainList.map(domain => {
              const count = fellows.filter(f => f.domain === domain).length;
              return (
                <button
                  key={domain}
                  className={`${styles.domainFilterBtn} ${activeDomain === domain ? styles.domainFilterBtnActive : ''}`}
                  onClick={() => setActiveDomain(domain)}
                >
                  {domain} ({count})
                </button>
              );
            })}
          </div>

          {/* TOGGLES */}
          <div className={styles.toggleStrip}>
            <button
              className={`${styles.toggleBtn} ${filterWithLinkedIn ? styles.toggleBtnActive : ''}`}
              onClick={() => setFilterWithLinkedIn(!filterWithLinkedIn)}
            >
              <LinkedInIcon size={13} />
              With LinkedIn Profile
            </button>
            <button
              className={`${styles.toggleBtn} ${filterWithArticle ? styles.toggleBtnActive : ''}`}
              onClick={() => setFilterWithArticle(!filterWithArticle)}
            >
              <BookOpen size={13} style={{ display: 'inline', marginRight: 4 }} />
              With Published Article
            </button>
            <button
              className={`${styles.toggleBtn} ${filterDistinction ? styles.toggleBtnActive : ''}`}
              onClick={() => setFilterDistinction(!filterDistinction)}
            >
              <Award size={13} style={{ display: 'inline', marginRight: 4 }} />
              High Merit &amp; Distinction (Score 85+)
            </button>
          </div>
        </div>

        {/* RESULTS HEADER */}
        <div className={styles.resultsHeader}>
          <span>Showing <strong>{filteredFellows.length}</strong> verified fellows &amp; case studies</span>
          <span>Sovereign Platform Authority &bull; dbert.in</span>
        </div>

        {/* FELLOWS GRID */}
        <div className={styles.fellowsGrid}>
          {filteredFellows.map((fellow) => {
            const hasArticle = Boolean(fellow.articleTitle && fellow.articleUrl);
            const hasLinkedIn = Boolean(fellow.linkedinUrl);

            return (
              <div key={fellow.certId} className={styles.fellowCard}>
                {/* CARD HEADER */}
                <div className={styles.cardHeader}>
                  <span className={styles.domainBadge}>
                    {fellow.domain}
                  </span>
                  <span className={styles.scoreBadge}>
                    <Sparkles size={12} />
                    {fellow.score}/100
                  </span>
                </div>

                {/* NAME & COLLEGE */}
                <h3 className={styles.fellowName}>{fellow.name}</h3>
                <div className={styles.fellowCollege}>
                  <GraduationCap size={14} color="#64748b" />
                  <span>{fellow.college}</span>
                </div>

                {/* PROJECT BOX */}
                <div className={styles.projectBox}>
                  <div className={styles.projectLabel}>Incubation Project &bull; Verified Evaluation</div>
                  <div className={styles.projectName}>{fellow.project}</div>
                </div>

                {/* PUBLISHED ARTICLE SNIPPET (IF ANY) */}
                {hasArticle && (
                  <div className={styles.articleSnippet}>
                    <div className={styles.articleSnippetHeader}>
                      <BookOpen size={12} />
                      Published Technical Case Study
                    </div>
                    <div className={styles.articleSnippetTitle}>
                      {fellow.articleTitle}
                    </div>
                  </div>
                )}

                {/* ACTIONS */}
                <div className={styles.actionLinks}>
                  <Link
                    href={`/verify/${fellow.certId}`}
                    className={styles.btnPrimaryAction}
                    title="View Cryptographic Evaluation Rubric & Dossier"
                  >
                    <CheckCircle2 size={14} />
                    View Proof Dossier &bull; {fellow.certId}
                  </Link>

                  <div className={styles.socialRow}>
                    {hasLinkedIn ? (
                      <a
                        href={fellow.linkedinUrl!}
                        target="_blank"
                        rel="noopener noreferrer"
                        className={`${styles.btnSocial} ${styles.btnLinkedIn}`}
                      >
                        <LinkedInIcon size={13} />
                        LinkedIn ↗
                      </a>
                    ) : (
                      <span className={styles.btnSocial} style={{ opacity: 0.4, cursor: 'default' }}>
                        LinkedIn N/A
                      </span>
                    )}

                    {hasArticle ? (
                      <Link
                        href={fellow.articleUrl!}
                        className={`${styles.btnSocial} ${styles.btnArticle}`}
                        title="Read Peer-Reviewed Engineering Article"
                      >
                        <BookOpen size={13} />
                        Read Article ↗
                      </Link>
                    ) : fellow.githubUrl ? (
                      <a
                        href={fellow.githubUrl}
                        target="_blank"
                        rel="noopener noreferrer"
                        className={styles.btnSocial}
                      >
                        <GithubIcon size={13} />
                        GitHub ↗
                      </a>
                    ) : (
                      <Link
                        href={`/verify/${fellow.certId}`}
                        className={styles.btnSocial}
                      >
                        <Award size={13} />
                        Rubric ↗
                      </Link>
                    )}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </main>
    </div>
  );
}
