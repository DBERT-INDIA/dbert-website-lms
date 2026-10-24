'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import styles from './FastCalculator.module.css';
import { trackEvent } from '@/lib/analytics';

export default function FastCalculator() {
  const [weeks, setWeeks] = useState(6);
  const [grant, setGrant] = useState(150000);

  // Dynamic calculations
  let calculatedEquity = 2.0 + (weeks - 4) * 0.4 + (grant / 100000) * 0.3;
  if (calculatedEquity > 8.0) calculatedEquity = 8.0;

  let squadSpec = '1 Lead Architect + 1 AI Fellow';
  if (weeks >= 8 && weeks < 12) squadSpec = '1 Lead Architect + 2 AI Fellows + DevOps Lead';
  if (weeks >= 12) squadSpec = '2 Senior Architects + 3 AI Fellows + DevOps Lead';

  const handleWeeksChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const val = parseInt(e.target.value, 10);
    setWeeks(val);
    trackEvent('fast_calculator_interaction', {
      sprint_weeks: val,
      grant_amount: grant,
      calculated_equity: calculatedEquity.toFixed(1),
    });
  };

  const handleGrantChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const val = parseInt(e.target.value, 10);
    setGrant(val);
    trackEvent('fast_calculator_interaction', {
      sprint_weeks: weeks,
      grant_amount: val,
      calculated_equity: calculatedEquity.toFixed(1),
    });
  };

  return (
    <div className={styles.calculatorCard}>
      <div className={styles.header}>
        <div>
          <div className="doclabel" style={{ marginBottom: '6px' }}>
            // INTERACTIVE TOOL // FULL TRANSPARENCY
          </div>
          <h2 className={styles.title}>FAST Equity Model Calculator</h2>
        </div>
        <div className={styles.sublabel}>
          <span>●</span> MODELLED ON YC SAFE &amp; FAST (FOUNDER ADVISORY SHARES)
        </div>
      </div>

      <div className={styles.grid}>
        <div className={styles.sliderGroup}>
          <div className={styles.sliderBlock}>
            <div className={styles.sliderHeader}>
              <span className={styles.sliderLabel}>Estimated Code Sprint Duration</span>
              <span className={styles.sliderValue}>
                {weeks} WEEKS ({Math.round(weeks / 2)} AGILE SPRINTS)
              </span>
            </div>
            <input
              type="range"
              min="4"
              max="16"
              step="2"
              value={weeks}
              onChange={handleWeeksChange}
              className={styles.rangeInput}
              aria-label="Sprint duration in weeks"
            />
            <div className={styles.rangeTicks}>
              <span>4 WEEKS (MVP)</span>
              <span>8 WEEKS (BETA)</span>
              <span>12 WEEKS (PROD)</span>
              <span>16 WEEKS (SCALE)</span>
            </div>
          </div>

          <div className={styles.sliderBlock}>
            <div className={styles.sliderHeader}>
              <span className={styles.sliderLabel}>Infrastructure Seed Grant Required</span>
              <span className={styles.sliderValueAmber}>
                ₹{(grant / 100000).toFixed(2)} LAKH (NON-DILUTIVE GPU CLOUD)
              </span>
            </div>
            <input
              type="range"
              min="50000"
              max="500000"
              step="50000"
              value={grant}
              onChange={handleGrantChange}
              className={`${styles.rangeInput} ${styles.rangeInputAmber}`}
              aria-label="Infrastructure seed grant amount"
            />
            <div className={styles.rangeTicks}>
              <span>₹50,000</span>
              <span>₹2,50,000</span>
              <span>₹5,00,000 (MAX SEED)</span>
            </div>
          </div>

          <div className={styles.guaranteeNote}>
            <strong style={{ color: 'var(--ok)' }}>Statutory Guarantee:</strong> You retain 100% of your Intellectual Property from Day 1. No board seats, no voting interference, and no cash clawbacks if the venture pivots or terminates.
          </div>
        </div>

        <div className={styles.outputHUD}>
          <div className={styles.hudHeader}>
            <span>TERMS AUDIT</span>
            <span className={styles.hudModelTag}>FAST v2.2 AGREEMENT</span>
          </div>

          <div className={styles.equityDisplay}>
            <div className={styles.equityLabel}>Advisory Equity Exchange</div>
            <div className={styles.equityBigNumber}>{calculatedEquity.toFixed(1)}%</div>
            <div className={styles.equityDesc}>Non-voting Advisory Shares / Standard Common Stock</div>
          </div>

          <div className={styles.hudSpecs}>
            <div className={styles.hudRow}>
              <span className={styles.hudKey}>Assigned Squad:</span>
              <span className={styles.hudVal}>{squadSpec}</span>
            </div>
            <div className={styles.hudRow}>
              <span className={styles.hudKey}>Cash Upfront Required:</span>
              <span className={styles.hudValGreen}>₹0.00 (Zero Burn)</span>
            </div>
            <div className={styles.hudRow}>
              <span className={styles.hudKey}>Weekly Code Commits:</span>
              <span className={styles.hudValAmber}>40–60 PR Merges Expected</span>
            </div>
          </div>

          <Link
            href="/startups/register"
            className={styles.applyButton}
            onClick={() =>
              trackEvent('incubation_apply_click', {
                location: 'fast_calculator',
                sprint_weeks: weeks,
                grant_amount: grant,
                calculated_equity: calculatedEquity.toFixed(1),
              })
            }
          >
            <span>Apply With These Sprint Parameters</span>
            <span aria-hidden="true">&rarr;</span>
          </Link>
        </div>
      </div>
    </div>
  );
}
