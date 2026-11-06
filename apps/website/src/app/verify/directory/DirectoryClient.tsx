'use client';

import React, { useState, useMemo } from 'react';
import Link from 'next/link';
import s from './directory.module.css';

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
}

interface DirectoryClientProps {
  candidates: CandidateDirectoryItem[];
}

const ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('');

export default function DirectoryClient({ candidates }: DirectoryClientProps) {
  const [selectedLetter, setSelectedLetter] = useState<string>('A');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [selectedDomain, setSelectedDomain] = useState<string>('ALL');
  const [cohortFilter, setCohortFilter] = useState<'ALL' | 'VERIFIED' | 'PROVISIONAL'>('ALL');

  // Available unique domains
  const availableDomains = useMemo(() => {
    const set = new Set<string>();
    candidates.forEach((c) => {
      if (c.domain) set.add(c.domain.trim());
    });
    return Array.from(set).sort();
  }, [candidates]);

  // Overall counts
  const totalVerified = useMemo(() => candidates.filter((c) => !c.isProvisional).length, [candidates]);
  const totalProvisional = useMemo(() => candidates.filter((c) => c.isProvisional).length, [candidates]);

  // Candidates filtered by domain & cohort first (for letter count calculations)
  const baseFiltered = useMemo(() => {
    return candidates.filter((c) => {
      if (cohortFilter === 'VERIFIED' && c.isProvisional) return false;
      if (cohortFilter === 'PROVISIONAL' && !c.isProvisional) return false;
      if (selectedDomain !== 'ALL' && c.domain.trim() !== selectedDomain) return false;
      return true;
    });
  }, [candidates, cohortFilter, selectedDomain]);

  // Letter count mapping
  const letterCounts = useMemo(() => {
    const counts: Record<string, number> = { ALL: baseFiltered.length };
    ALPHABET.forEach((l) => (counts[l] = 0));
    counts['#'] = 0;

    baseFiltered.forEach((c) => {
      const fl = c.firstLetter?.toUpperCase() || '#';
      if (counts[fl] !== undefined) {
        counts[fl]++;
      } else {
        counts['#']++;
      }
    });

    return counts;
  }, [baseFiltered]);

  // Final filtered list
  const filteredCandidates = useMemo(() => {
    const q = searchQuery.trim().toLowerCase();

    // If searching, search across all letters
    if (q) {
      return baseFiltered.filter(
        (c) =>
          c.holderName.toLowerCase().includes(q) ||
          c.certId.toLowerCase().includes(q) ||
          (c.internId && c.internId.toLowerCase().includes(q))
      );
    }

    // Otherwise filter by selected letter
    if (selectedLetter === 'ALL') {
      return baseFiltered;
    }

    return baseFiltered.filter((c) => c.firstLetter.toUpperCase() === selectedLetter);
  }, [baseFiltered, searchQuery, selectedLetter]);

  const handleReset = () => {
    setSearchQuery('');
    setSelectedLetter('A');
    setSelectedDomain('ALL');
    setCohortFilter('ALL');
  };

  return (
    <div className={s.container}>
      {/* Header & Breadcrumb */}
      <div className={s.headerShell}>
        <Link href="/verify" className={s.breadcrumb}>
          &larr; Back to Single Certificate Verification
        </Link>

        <div className={s.titleBlock}>
          <div>
            <h1 className={s.titleMain}>
              DBERT Credential Directory
            </h1>
            <p className={s.titleSubtitle}>
              Official Sovereign Incubation &amp; Technical Fellowship Registry
            </p>
          </div>

          <div className={s.statsBar}>
            <span className={`${s.statBadge} ${s.statTotal}`}>
              Total Roster: {candidates.length}
            </span>
            <span className={`${s.statBadge} ${s.statVerified}`}>
              ✓ Verified: {totalVerified}
            </span>
            <span className={`${s.statBadge} ${s.statProvisional}`}>
              ⧗ Provisional: {totalProvisional}
            </span>
          </div>
        </div>
      </div>

      {/* Controls Block */}
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
            placeholder="Search candidate name or Certificate ID (e.g. CERT-DBERT-2026-DA-001)..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>

        {/* Domain Filter */}
        <select
          className={s.selectDropdown}
          value={selectedDomain}
          onChange={(e) => setSelectedDomain(e.target.value)}
        >
          <option value="ALL">All Technical Domains</option>
          {availableDomains.map((d) => (
            <option key={d} value={d}>
              {d}
            </option>
          ))}
        </select>

        {/* Cohort Filter */}
        <select
          className={s.selectDropdown}
          value={cohortFilter}
          onChange={(e) => setCohortFilter(e.target.value as any)}
        >
          <option value="ALL">All Cohort Statuses ({candidates.length})</option>
          <option value="VERIFIED">Verified Only ({totalVerified})</option>
          <option value="PROVISIONAL">Provisional Only ({totalProvisional})</option>
        </select>
      </div>

      {/* Alphabet Selector */}
      <div className={s.alphabetShell}>
        <div className={s.alphabetLabel}>
          <span>Filter by First Name Initial</span>
          {searchQuery && (
            <span style={{ color: '#E2B96F', textTransform: 'none' }}>
              (Search active: filtering across all letters)
            </span>
          )}
        </div>

        <div className={s.alphabetScroll}>
          <button
            type="button"
            className={`${s.letterBtn} ${selectedLetter === 'ALL' && !searchQuery ? s.letterBtnActive : ''}`}
            onClick={() => {
              setSelectedLetter('ALL');
              setSearchQuery('');
            }}
          >
            <span>All</span>
            <span className={s.letterCount}>{letterCounts['ALL'] || 0}</span>
          </button>

          {ALPHABET.map((letter) => {
            const count = letterCounts[letter] || 0;
            const isDisabled = count === 0;
            const isActive = selectedLetter === letter && !searchQuery;

            return (
              <button
                key={letter}
                type="button"
                disabled={isDisabled}
                className={`${s.letterBtn} ${isActive ? s.letterBtnActive : ''} ${isDisabled ? s.letterBtnDisabled : ''}`}
                onClick={() => {
                  setSelectedLetter(letter);
                  setSearchQuery('');
                }}
                title={isDisabled ? `No candidates starting with '${letter}'` : `${count} candidates starting with '${letter}'`}
              >
                <span>{letter}</span>
                <span className={s.letterCount}>{count}</span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Results Header */}
      <div className={s.resultsHeader}>
        <div>
          Showing <strong>{filteredCandidates.length}</strong> {filteredCandidates.length === 1 ? 'candidate' : 'candidates'}
          {searchQuery ? ` matching "${searchQuery}"` : selectedLetter !== 'ALL' ? ` under letter '${selectedLetter}'` : ''}
        </div>
        {(searchQuery || selectedLetter !== 'A' || selectedDomain !== 'ALL' || cohortFilter !== 'ALL') && (
          <button
            type="button"
            onClick={handleReset}
            style={{ background: 'none', border: 'none', color: '#E2B96F', cursor: 'pointer', fontSize: '0.82rem', fontWeight: 600 }}
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

            return (
              <div key={`${cand.certId}-${cand.internId || cand.holderName}`} className={s.candidateCard}>
                <div>
                  <div className={s.cardTop}>
                    <h3 className={s.candidateName}>
                      <Link href={verifyHref}>
                        {cand.holderName}
                      </Link>
                    </h3>

                    {cand.isProvisional ? (
                      <span className={`${s.cardStatusPill} ${s.pillProvisional}`} title="Action Required: Final Verification Form Pending">
                        Provisional Record
                      </span>
                    ) : (
                      <span className={`${s.cardStatusPill} ${s.pillVerified}`} title="Cryptographically Verified Active Credential">
                        ✓ Verified
                      </span>
                    )}
                  </div>

                  <div className={s.cardBody}>
                    <div className={s.certIdLine}>
                      <span>ID:</span>
                      <strong>{cand.certId}</strong>
                    </div>

                    <div className={s.infoRow}>
                      <span className={s.infoLabel}>Domain:</span>
                      <span className={s.infoValue}>{cand.domain}</span>
                    </div>

                    <div className={s.infoRow}>
                      <span className={s.infoLabel}>Tenure:</span>
                      <span className={s.infoValue}>{cand.duration}</span>
                    </div>

                    <div className={s.infoRow}>
                      <span className={s.infoLabel}>Evaluation:</span>
                      <span className={s.infoValue}>{cand.score}/100 ({cand.grade})</span>
                    </div>
                  </div>
                </div>

                <div className={s.cardFooter}>
                  <Link href={verifyHref} className={s.btnVerifyLink}>
                    Verify Credential &rarr;
                  </Link>
                </div>
              </div>
            );
          })}
        </div>
      ) : (
        <div className={s.emptyState}>
          <div className={s.emptyTitle}>No candidates found</div>
          <p>
            No registered interns match the selected letter or filter criteria.
          </p>
          <button type="button" className={s.resetBtn} onClick={handleReset}>
            Reset Filters
          </button>
        </div>
      )}
    </div>
  );
}
