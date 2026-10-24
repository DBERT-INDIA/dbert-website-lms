'use client';

import React from 'react';
import styles from './RegionalOpportunityBento.module.css';
import { trackEvent } from '@/lib/analytics';
import { ExternalLink, Sparkles } from 'lucide-react';

export interface OpportunityItem {
  title: string;
  roleDescription: string;
  cityTag: string;
  location: string;
  stipend: string;
  href: string;
  tags: string[];
}

export interface RegionalOpportunityBentoProps {
  sectionNumber?: string;
  title: string;
  description: string;
  domainName: string;
  hubHref: string;
  jobsHref: string;
  opportunities: OpportunityItem[];
}

export default function RegionalOpportunityBento({
  sectionNumber = '§ 08',
  title,
  description,
  domainName,
  hubHref,
  jobsHref,
  opportunities,
}: RegionalOpportunityBentoProps) {
  return (
    <section className={styles.section} aria-label={`${domainName} Regional Opportunities`}>
      <div className="container">
        <div className={styles.header}>
          <span className={styles.doclabel}>
            {sectionNumber} — INDUSTRY INTERNSHIPS &amp; REGIONAL HIRING HUBS · 2026 COHORT
          </span>
          <h2 className={styles.title}>{title}</h2>
          <p className={styles.lede}>{description}</p>
        </div>

        <div className={styles.grid}>
          {opportunities.map((opp, idx) => (
            <a
              key={idx}
              href={opp.href}
              target="_blank"
              rel="noopener noreferrer"
              className={styles.card}
              onClick={() =>
                trackEvent('outbound_internship_click', {
                  role: opp.title,
                  city: opp.cityTag,
                  destination: opp.href,
                  domain: domainName,
                })
              }
            >
              <div>
                <div className={styles.metaRow}>
                  <span className={styles.cityTag}>{opp.cityTag}</span>
                  <span className={styles.stipendTag}>{opp.stipend}</span>
                </div>
                <h3 className={styles.roleTitle}>{opp.title}</h3>
                <p className={styles.roleDesc}>{opp.roleDescription}</p>
                <div className={styles.tagsRow}>
                  {opp.tags.map((tag, tIdx) => (
                    <span key={tIdx} className={styles.techChip}>
                      {tag}
                    </span>
                  ))}
                </div>
              </div>

              <div className={styles.actionRow}>
                <div className={styles.statusIndicator}>
                  <span className={styles.liveDot} aria-hidden="true" />
                  <span>Actively Accepting</span>
                </div>
                <span className={styles.actionText}>
                  View Role <ExternalLink size={12} aria-hidden="true" />
                </span>
              </div>
            </a>
          ))}
        </div>

        {/* Bottom Discovery Bar */}
        <div className={styles.bottomHubBar}>
          <div className={styles.hubPrompt}>
            <div className={styles.hubTitle}>
              Looking for roles in a specific Indian metro or global remote sprint?
            </div>
            <div className={styles.hubSub}>
              Explore verified startup project listings across Mumbai, Bengaluru, Delhi NCR, Pune, and Hyderabad.
            </div>
          </div>
          <div className={styles.hubLinks}>
            <a
              href={hubHref}
              target="_blank"
              rel="noopener noreferrer"
              className={`${styles.hubBtn} ${styles.hubBtnPrimary}`}
              onClick={() =>
                trackEvent('outbound_internship_hub_click', { domain: domainName, type: 'internships' })
              }
            >
              <Sparkles size={14} aria-hidden="true" />
              <span>Browse All {domainName} Sprints</span>
            </a>
            <a
              href={jobsHref}
              target="_blank"
              rel="noopener noreferrer"
              className={`${styles.hubBtn} ${styles.hubBtnOutline}`}
              onClick={() =>
                trackEvent('outbound_internship_hub_click', { domain: domainName, type: 'jobs' })
              }
            >
              <span>Verified Full-Time Placements ↗</span>
            </a>
          </div>
        </div>
      </div>
    </section>
  );
}
