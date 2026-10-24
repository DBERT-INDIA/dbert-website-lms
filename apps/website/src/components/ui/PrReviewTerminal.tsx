'use client';

import React from 'react';
import styles from './PrReviewTerminal.module.css';
import { trackEvent } from '@/lib/analytics';

export default function PrReviewTerminal() {
  return (
    <div
      className={styles.terminalCard}
      onMouseEnter={() => trackEvent('pr_review_view', { pr_number: '#148' })}
    >
      <div className={styles.header}>
        <div>
          <div className="doclabel" style={{ marginBottom: '6px' }}>
            // ACTUAL APPRENTICESHIP // PULL REQUEST #148
          </div>
          <h2 className={styles.title}>What Learning at DBERT Actually Feels Like</h2>
        </div>
        <div className={styles.repoTag}>
          <span>Repository:</span> <code style={{ color: 'var(--accent)' }}>dbert-labs/alkame-vector-cache</code>
        </div>
      </div>

      <div className={styles.terminalBox}>
        <div className={styles.prMeta}>
          <div>
            <span className={styles.prBadge}>CHANGES REQUESTED</span>
            <span className={styles.prTitle}>PR #148: Optimize Qdrant payload serialization</span>
          </div>
          <span className={styles.prMerged}>Merged 3 days ago &bull; commit 8f9b2a1</span>
        </div>

        {/* Comment 1: Lead Architect */}
        <div className={styles.commentBlock}>
          <div className={styles.avatarArchitect} aria-label="Abhinav Lead Architect">
            A
          </div>
          <div className={styles.commentBody}>
            <div className={styles.commentHeader}>
              <span className={styles.authorName}>abhinav (Lead Systems Architect)</span>
              <span className={styles.commentContext}>review comment on lines 42–58</span>
            </div>
            <p className={styles.commentText}>
              &ldquo;You&apos;re executing <code>json.loads()</code> inside the vector similarity loop for every single document chunk. At 50 concurrent requests, this will pin CPU core 0 at 100% and spike p99 latency past 1.2s. Pre-parse the metadata into a Pydantic struct once on ingest, and use <code>orjson</code> for faster deserialization.&rdquo;
            </p>
          </div>
        </div>

        {/* Comment 2: Fellow */}
        <div className={styles.commentBlock}>
          <div className={styles.avatarFellow} aria-label="Rohit Fellow">
            R
          </div>
          <div className={styles.commentBody}>
            <div className={styles.commentHeader}>
              <span className={styles.authorName}>rohit-k (Applied AI Fellow · Cohort 5)</span>
              <span className={styles.commentContext}>commit 8f9b2a1</span>
            </div>
            <p className={styles.commentText}>
              &ldquo;Good catch. Rewrote the chunk handler to use <code>orjson</code> with pre-validated Pydantic models. Benchmarked locally with Locust: p99 latency dropped from 1,240ms to 48ms (-96%). Added 12 unit tests in <code>/tests/vector_test.py</code>. Re-requesting review!&rdquo;
            </p>
          </div>
        </div>

        {/* Outcome Badge */}
        <div className={styles.outcomeBadge}>
          <span className={styles.outcomeCheck}>
            ✓ Approved &amp; Merged to Production Cluster
          </span>
          <span className={styles.outcomeReward}>
            Fellow earned ₹4,500 milestone stipend
          </span>
        </div>
      </div>
    </div>
  );
}
