'use client';

import React, { useState, useMemo } from 'react';
import Link from 'next/link';
import s from './directory.module.css';
import {
  CANONICAL_DOMAINS,
  normalizeDomainToSlug,
  type DomainMeta,
} from '@/data/domains.config';

export interface CandidateDirectoryItem {
  certId: string;
  internId?: string;
  holderName: string;
  domain: string;
  duration: string;
  score: number;
  grade: string;
  isProvisional: boolean;
  status: string;
  firstLetter: string;
  verifyUrl: string;
  linkedinUrl?: string;
  linkedinVerified?: boolean;
}

interface DirectoryClientProps {
  candidates: CandidateDirectoryItem[];
  currentDomainSlug?: string;
  customHeadline?: string;
  customDescription?: string;
  customBadge?: string;
}

const DOMAIN_SKILLS: Record<string, string[]> = {
  'Full Stack Development': ['Next.js', 'React 19', 'TypeScript', 'Node.js', 'PostgreSQL', 'Tailwind CSS'],
  'Full Stack Web Development': ['Next.js', 'React 19', 'TypeScript', 'Node.js', 'PostgreSQL'],
  'Data Analyst': ['SQL', 'Python Pandas', 'Power BI', 'Data Modeling', 'ETL Pipelines'],
  'Data Analytics': ['SQL', 'Python Pandas', 'Power BI', 'Tableau', 'Data Modeling'],
  'Artificial Intelligence & Machine Learning': ['PyTorch', 'LangChain', 'FastAPI', 'RAG Pipelines', 'OpenCV'],
  'Artificial Intelligence (AI) & Machine Learning (ML)': ['PyTorch', 'LangChain', 'FastAPI', 'RAG Pipelines', 'Transformers'],
  'Artificial Intelligence (AI) and Machine Learning (ML)': ['PyTorch', 'LangChain', 'FastAPI', 'CrewAI', 'Transformers'],
  'Python Automation': ['Playwright', 'Selenium', 'Celery', 'Redis', 'Web Scraping'],
  'UI/UX Design': ['Figma', 'Auto-Layout', 'Design Systems', 'Wireframing', 'WCAG'],
  'UI and UX Internship': ['Figma', 'Auto-Layout', 'Design Systems', 'Prototyping'],
  'UI & UX Design': ['Figma', 'Auto-Layout', 'Design Systems', 'User Journeys'],
  'DevOps & Cloud': ['Docker', 'Kubernetes', 'AWS', 'CI/CD Pipelines', 'Linux'],
  'Mobile App Development': ['Flutter', 'Dart', 'React Native', 'Firebase', 'REST APIs'],
  'Digital Brand Building': ['GA4 Analytics', 'Technical SEO', 'Google Ads', 'Meta Ads']
};

export default function DirectoryClient({
  candidates,
  currentDomainSlug,
  customHeadline,
  customDescription,
  customBadge,
}: DirectoryClientProps) {
  const currentDomainMeta: DomainMeta | undefined = currentDomainSlug
    ? CANONICAL_DOMAINS[currentDomainSlug]
    : undefined;

  const [activeTab, setActiveTab] = useState<'VERIFIED' | 'PROVISIONAL'>('VERIFIED');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [selectedDomain, setSelectedDomain] = useState<string>(currentDomainSlug || 'ALL');
  const [minScore, setMinScore] = useState<string>('ALL');
  const [selectedSkills, setSelectedSkills] = useState<string[]>([]);
  const [linkedinOnly, setLinkedinOnly] = useState<boolean>(false);

  // Calculate candidate counts per canonical domain
  const domainCounts = useMemo(() => {
    const counts: Record<string, { total: number; verified: number }> = {};
    Object.keys(CANONICAL_DOMAINS).forEach((slug) => {
      counts[slug] = { total: 0, verified: 0 };
    });

    candidates.forEach((c) => {
      const slug = normalizeDomainToSlug(c.domain);
      if (slug && counts[slug]) {
        counts[slug].total += 1;
        if (!c.isProvisional) counts[slug].verified += 1;
      }
    });
    return counts;
  }, [candidates]);

  // Overall counts
  const totalVerified = useMemo(() => candidates.filter((c) => !c.isProvisional).length, [candidates]);
  const totalProvisional = useMemo(() => candidates.filter((c) => c.isProvisional).length, [candidates]);

  // Determine selectable skills for filter chips
  const availableSkillChips = useMemo(() => {
    if (currentDomainMeta) {
      return [...currentDomainMeta.primarySkills, ...currentDomainMeta.secondarySkills.slice(0, 4)];
    }
    // Top cross-stack skills across all domains
    return [
      'Next.js',
      'React 19',
      'TypeScript',
      'Python',
      'SQL',
      'Power BI',
      'PyTorch',
      'LangChain',
      'FastAPI',
      'Playwright',
      'Docker',
      'Figma',
      'Flutter'
    ];
  }, [currentDomainMeta]);

  // Toggle skill selection
  const handleToggleSkill = (skill: string) => {
    setSelectedSkills((prev) =>
      prev.includes(skill) ? prev.filter((s) => s !== skill) : [...prev, skill]
    );
  };

  const handleClearSkills = () => {
    setSelectedSkills([]);
  };

  // Filtered & Ranked Candidates
  const filteredCandidates = useMemo(() => {
    const q = searchQuery.trim().toLowerCase();

    // 1. Filter by active tab (Verified vs Provisional)
    let list = candidates.filter((c) => {
      if (activeTab === 'VERIFIED') return !c.isProvisional;
      return c.isProvisional;
    });

    // 2. Filter by domain (canonical slug comparison or raw string)
    if (selectedDomain !== 'ALL') {
      list = list.filter((c) => {
        const cSlug = normalizeDomainToSlug(c.domain);
        if (cSlug) return cSlug === selectedDomain;
        return c.domain.trim() === selectedDomain;
      });
    }

    // 3. Filter by minimum evaluation score
    if (minScore !== 'ALL') {
      const threshold = parseInt(minScore, 10);
      list = list.filter((c) => (Number(c.score) || 0) >= threshold);
    }

    // 4. Filter by selected skill chips (multi-select)
    if (selectedSkills.length > 0) {
      list = list.filter((c) => {
        const candSkills = (DOMAIN_SKILLS[c.domain] || []).map((s) => s.toLowerCase());
        return selectedSkills.some((sel) =>
          candSkills.some((cs) => cs.includes(sel.toLowerCase()) || sel.toLowerCase().includes(cs))
        );
      });
    }

    // 5. Filter by LinkedIn verified presence
    if (linkedinOnly) {
      list = list.filter((c) => Boolean(c.linkedinUrl));
    }

    // 6. Filter by text search query (Name, CertID, InternID, Domain, Skills)
    if (q) {
      list = list.filter((c) => {
        const skills = DOMAIN_SKILLS[c.domain] || [];
        const skillsMatch = skills.some((s) => s.toLowerCase().includes(q));
        return (
          c.holderName.toLowerCase().includes(q) ||
          c.certId.toLowerCase().includes(q) ||
          c.domain.toLowerCase().includes(q) ||
          (c.internId && c.internId.toLowerCase().includes(q)) ||
          skillsMatch
        );
      });
    }

    // 7. Hireability Ranking Mechanism:
    // Highest evaluation score descending, then alphabetical tie-breaker
    return [...list].sort((a, b) => {
      const scoreA = Number(a.score) || 0;
      const scoreB = Number(b.score) || 0;
      if (scoreB !== scoreA) {
        return scoreB - scoreA;
      }
      return a.holderName.localeCompare(b.holderName);
    });
  }, [candidates, activeTab, selectedDomain, minScore, selectedSkills, linkedinOnly, searchQuery]);

  const handleReset = () => {
    setSearchQuery('');
    if (!currentDomainSlug) {
      setSelectedDomain('ALL');
    }
    setMinScore('ALL');
    setSelectedSkills([]);
    setLinkedinOnly(false);
  };

  const heroHeadline = customHeadline || currentDomainMeta?.headline || 'Hire Pre-Vetted Software & AI Engineers';
  const heroDescription = customDescription || currentDomainMeta?.description ||
    'Browse certified engineering talent with verified production pull requests, 100-point academic rubrics, and proven capstones. Zero agency markup · 14-day risk-free trial.';
  const heroBadgeText = customBadge || currentDomainMeta?.badge || 'Pre-Vetted Technical Talent Roster · Batch 2026';

  return (
    <div className={s.container}>
      {/* Top Breadcrumb Hierarchy */}
      <div className={s.breadcrumbWrap}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flexWrap: 'wrap' }}>
          <Link href="/verify" className={s.breadcrumb}>
            &larr; Credential Verification
          </Link>
          {currentDomainMeta && (
            <>
              <span style={{ color: '#475569' }}>/</span>
              <Link href="/verify/directory" className={s.breadcrumb}>
                All Engineers Directory
              </Link>
              <span style={{ color: '#475569' }}>/</span>
              <span style={{ color: '#F1F5F9', fontWeight: 600 }}>{currentDomainMeta.shortName}</span>
            </>
          )}
        </div>
        <Link href="/hire/pre-vetted-engineers" className={s.vettingLink}>
          Learn about our 4-stage vetting process &rarr;
        </Link>
      </div>

      {/* Horizontal Domain Navigation Bar */}
      <div className={s.domainNavSection}>
        <div className={s.domainNavLabel}>
          <span>Specialized Domain Directories:</span>
        </div>
        <div className={s.domainNavScroll}>
          <Link
            href="/verify/directory"
            className={`${s.domainPillLink} ${!currentDomainSlug ? s.domainPillLinkActive : ''}`}
          >
            <span>All Domains</span>
            <span className={s.pillCount}>{candidates.length}</span>
          </Link>

          {Object.entries(CANONICAL_DOMAINS).map(([slug, meta]) => {
            const count = domainCounts[slug]?.total || 0;
            const isActive = currentDomainSlug === slug;
            return (
              <Link
                key={slug}
                href={`/verify/directory/${slug}`}
                className={`${s.domainPillLink} ${isActive ? s.domainPillLinkActive : ''}`}
              >
                <span>{meta.shortName}</span>
                <span className={s.pillCount}>{count}</span>
              </Link>
            );
          })}
        </div>
      </div>

      {/* Executive Employer Hero Banner */}
      <div className={s.employerHero}>
        <div className={s.heroMain}>
          <div className={s.heroBadge}>
            <span className={s.pulseDot}></span>
            <span>{heroBadgeText}</span>
          </div>
          <h1 className={s.heroTitle}>{heroHeadline}</h1>
          <p className={s.heroSubtitle}>{heroDescription}</p>

          <div className={s.metricsRow}>
            <div className={s.metricItem}>
              <strong>{currentDomainSlug ? (domainCounts[currentDomainSlug]?.verified || totalVerified) : totalVerified}</strong>
              <span>Verified Engineers</span>
            </div>
            <div className={s.metricDivider}></div>
            <div className={s.metricItem}>
              <strong>48h</strong>
              <span>Match Turnaround</span>
            </div>
            <div className={s.metricDivider}></div>
            <div className={s.metricItem}>
              <strong>Top 3%</strong>
              <span>Screening Bar</span>
            </div>
            <div className={s.metricDivider}></div>
            <div className={s.metricItem}>
              <strong>100%</strong>
              <span>Code Audited</span>
            </div>
          </div>
        </div>

        <div className={s.heroActions}>
          <a
            href="https://lms.dbert.in/company/signup"
            target="_blank"
            rel="noopener noreferrer"
            className={s.btnPrimaryCta}
          >
            Post Jobs &amp; Connect on LMS &rarr;
          </a>
          <span className={s.ctaNote}>Free employer signup · Instant candidate messaging</span>
        </div>
      </div>

      {/* Segregated Status Tabs */}
      <div className={s.tabShell}>
        <button
          type="button"
          className={`${s.tabBtn} ${activeTab === 'VERIFIED' ? s.tabActive : ''}`}
          onClick={() => setActiveTab('VERIFIED')}
        >
          <span className={s.tabIcon}>⭐</span>
          <span>Pre-Vetted Engineers (Ready to Hire)</span>
          <span className={`${s.tabBadge} ${activeTab === 'VERIFIED' ? s.tabBadgeActive : ''}`}>
            {currentDomainSlug ? (domainCounts[currentDomainSlug]?.verified || 0) : totalVerified}
          </span>
        </button>

        <button
          type="button"
          className={`${s.tabBtn} ${activeTab === 'PROVISIONAL' ? s.tabActive : ''}`}
          onClick={() => setActiveTab('PROVISIONAL')}
        >
          <span className={s.tabIcon}>⧗</span>
          <span>Incubation Fellows (Sprints in Progress)</span>
          <span className={`${s.tabBadge} ${activeTab === 'PROVISIONAL' ? s.tabBadgeActive : ''}`}>
            {currentDomainSlug ? ((domainCounts[currentDomainSlug]?.total || 0) - (domainCounts[currentDomainSlug]?.verified || 0)) : totalProvisional}
          </span>
        </button>
      </div>

      {/* Interactive Skills Filter Chips */}
      <div className={s.skillsSection}>
        <div className={s.skillsHeader}>
          <div className={s.skillsTitle}>
            <span>Filter by Verified Tech Stack:</span>
            {selectedSkills.length > 0 && (
              <span style={{ color: '#FBBF24', fontSize: '0.74rem' }}>
                ({selectedSkills.length} selected)
              </span>
            )}
          </div>
          {selectedSkills.length > 0 && (
            <button
              type="button"
              onClick={handleClearSkills}
              className={s.skillsClearBtn}
            >
              Clear Skills Filter
            </button>
          )}
        </div>

        <div className={s.skillsGrid}>
          {availableSkillChips.map((skill) => {
            const isSelected = selectedSkills.includes(skill);
            return (
              <button
                key={skill}
                type="button"
                onClick={() => handleToggleSkill(skill)}
                className={`${s.skillFilterChip} ${isSelected ? s.skillFilterChipActive : ''}`}
                aria-pressed={isSelected}
              >
                {isSelected && <span className={s.skillChipCheck}>✓</span>}
                <span>{skill}</span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Filter and Search Bar */}
      <div className={s.controlsBlock}>
        {/* Search Input */}
        <div className={s.searchWrap}>
          <svg className={s.searchIcon} width="16" height="16" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
            <circle cx="11" cy="11" r="8"></circle>
            <path strokeLinecap="round" strokeLinejoin="round" d="m21 21-4.35-4.35"></path>
          </svg>
          <input
            type="text"
            className={s.searchInput}
            placeholder="Search by engineer name, stack keyword (e.g. Next.js, SQL), or ID..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>

        {/* Domain Filter Dropdown */}
        <select
          className={s.selectDropdown}
          value={selectedDomain}
          onChange={(e) => setSelectedDomain(e.target.value)}
        >
          <option value="ALL">All Technical Domains</option>
          {Object.entries(CANONICAL_DOMAINS).map(([slug, meta]) => (
            <option key={slug} value={slug}>
              {meta.name}
            </option>
          ))}
        </select>

        {/* Score Ranking Filter */}
        <select
          className={s.selectDropdown}
          value={minScore}
          onChange={(e) => setMinScore(e.target.value)}
        >
          <option value="ALL">All Evaluation Scores</option>
          <option value="90">Top Tier: 90+ Score (Distinction)</option>
          <option value="85">High Merit: 85+ Score</option>
          <option value="80">Proficient: 80+ Score</option>
        </select>

        {/* LinkedIn Experience Verified Filter Button */}
        <button
          type="button"
          onClick={() => setLinkedinOnly(!linkedinOnly)}
          className={`${s.linkedinFilterBtn} ${linkedinOnly ? s.linkedinFilterActive : ''}`}
          title="Filter candidates with verified public LinkedIn experience profiles"
        >
          <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
            <path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/>
          </svg>
          <span>LinkedIn Verified Only</span>
          {linkedinOnly && <span className={s.linkedinCheck}>✓</span>}
        </button>
      </div>

      {/* Results Header */}
      <div className={s.resultsHeader}>
        <div>
          Showing <strong>{filteredCandidates.length}</strong> {activeTab === 'VERIFIED' ? 'pre-vetted engineers' : 'incubation fellows'}
          {searchQuery ? ` matching "${searchQuery}"` : ''}
          {selectedDomain !== 'ALL' ? ` in ${CANONICAL_DOMAINS[selectedDomain]?.shortName || selectedDomain}` : ''}
          {selectedSkills.length > 0 ? ` with skills [${selectedSkills.join(', ')}]` : ''}
          {minScore !== 'ALL' ? ` with score ${minScore}+` : ''}
          {linkedinOnly ? ' · LinkedIn Verified' : ''}
          <span className={s.rankTag}> (Ranked by Evaluation Score)</span>
        </div>
        {(searchQuery || selectedDomain !== 'ALL' || minScore !== 'ALL' || selectedSkills.length > 0 || linkedinOnly) && (
          <button
            type="button"
            onClick={handleReset}
            className={s.resetLink}
          >
            Reset Filters
          </button>
        )}
      </div>

      {/* Candidate Cards Grid */}
      {filteredCandidates.length > 0 ? (
        <div className={s.candidatesGrid}>
          {filteredCandidates.map((cand) => {
            const verifyHref = cand.isProvisional && cand.internId
              ? `/verify/${cand.certId}?internId=${encodeURIComponent(cand.internId)}`
              : `/verify/${cand.certId}`;

            const connectLmsHref = `https://lms.dbert.in/company/signup?ref=directory&candidate=${encodeURIComponent(cand.certId)}`;
            const skills = DOMAIN_SKILLS[cand.domain] || ['Production Sprints', 'Code Reviews', 'Git Architecture'];
            const scoreNum = Number(cand.score) || 0;

            return (
              <div key={`${cand.certId}-${cand.internId || cand.holderName}`} className={s.candidateCard}>
                <div>
                  <div className={s.cardTop}>
                    <div>
                      <h3 className={s.candidateName}>
                        <Link href={verifyHref}>
                          {cand.holderName}
                        </Link>
                      </h3>
                      <div className={s.certIdLine}>
                        <span>ID:</span>
                        <strong>{cand.certId}</strong>
                        {cand.linkedinUrl && (
                          <a
                            href={cand.linkedinUrl}
                            target="_blank"
                            rel="noopener noreferrer"
                            className={s.linkedinPill}
                            title={cand.linkedinVerified ? "Public LinkedIn Profile Verified by DBERT" : "Candidate Public LinkedIn Profile"}
                            onClick={(e) => e.stopPropagation()}
                          >
                            <svg width="11" height="11" viewBox="0 0 24 24" fill="currentColor">
                              <path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/>
                            </svg>
                            <span>LinkedIn</span>
                            {cand.linkedinVerified && <span className={s.linkedinCheck}>✓</span>}
                            <span className={s.externalArrow}>↗</span>
                          </a>
                        )}
                      </div>
                    </div>

                    {!cand.isProvisional ? (
                      <span className={`${s.cardStatusPill} ${s.pillVerified}`} title="Cryptographically Verified Active Credential · Ready for Placement">
                        ⭐ Available for Hire
                      </span>
                    ) : (
                      <span className={`${s.cardStatusPill} ${s.pillProvisional}`} title="Active Incubation Milestone In Progress">
                        ⧗ In Sprints
                      </span>
                    )}
                  </div>

                  <div className={s.cardBody}>
                    <div className={s.scoreChip}>
                      <span className={s.scoreNum}>{scoreNum}/100</span>
                      <span className={s.scoreGrade}>Grade {cand.grade}</span>
                      {scoreNum >= 90 && <span className={s.distinctionTag}>Top Tier</span>}
                    </div>

                    <div className={s.infoRow}>
                      <span className={s.infoLabel}>Domain:</span>
                      <span className={s.infoValue}>{cand.domain}</span>
                    </div>

                    <div className={s.infoRow}>
                      <span className={s.infoLabel}>Tenure:</span>
                      <span className={s.infoValue}>{cand.duration}</span>
                    </div>

                    {/* Verified Tech Skills */}
                    <div className={s.skillsWrap}>
                      {skills.slice(0, 4).map((skill) => (
                        <span key={skill} className={s.skillChip}>
                          {skill}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>

                <div className={s.cardFooter}>
                  <Link href={verifyHref} className={s.btnDossierLink}>
                    View Proof Dossier &rarr;
                  </Link>
                  <a
                    href={connectLmsHref}
                    target="_blank"
                    rel="noopener noreferrer"
                    className={s.btnConnectLms}
                    title="Connect with this engineer via LMS employer portal"
                  >
                    Connect on LMS
                  </a>
                </div>
              </div>
            );
          })}
        </div>
      ) : (
        <div className={s.emptyState}>
          <div className={s.emptyTitle}>No matching engineers found</div>
          <p>
            No candidates match the selected filters. Try broadening your score or tech stack criteria.
          </p>
          <button type="button" className={s.resetBtn} onClick={handleReset}>
            Reset All Filters
          </button>
        </div>
      )}

      {/* Sibling Domains Cross-Links (Bottom Link Equity) */}
      <div className={s.relatedDomainsBlock}>
        <h3 className={s.relatedDomainsTitle}>Explore Pre-Vetted Talent by Domain</h3>
        <p className={s.relatedDomainsDesc}>
          Browse specialized engineering rosters with evaluated code commits and verified Turnitin rubrics.
        </p>
        <div className={s.relatedDomainsGrid}>
          {Object.entries(CANONICAL_DOMAINS)
            .filter(([slug]) => slug !== currentDomainSlug)
            .map(([slug, meta]) => {
              const count = domainCounts[slug]?.total || 0;
              return (
                <Link
                  key={slug}
                  href={`/verify/directory/${slug}`}
                  className={s.relatedDomainCard}
                >
                  <div className={s.relatedDomainName}>{meta.name} &rarr;</div>
                  <div className={s.relatedDomainMeta}>
                    {count} pre-vetted engineers · {meta.primarySkills.slice(0, 3).join(', ')}
                  </div>
                </Link>
              );
            })}
        </div>
      </div>
    </div>
  );
}
