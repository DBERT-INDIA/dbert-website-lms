import React from 'react';
import Link from 'next/link';
import styles from './CareerLadder.module.css';
import Reveal from './Reveal';

export interface LadderStep {
  /** Node label on the rail, e.g. "R1". */
  num: string;
  /** Phase label, e.g. "Foundation". Hidden when a featured tag is shown. */
  tag: string;
  title: string;
  price?: string;
  /** Description of who the rung is for. */
  forText: string;
  outcome: string;
  /** CTA is optional — the approved homepage ladder has none. */
  ctaText?: string;
  ctaHref?: string;
  isFeatured?: boolean;
  /** Text of the amber pill on a featured rung, e.g. "most popular". */
  featuredLabel?: string;
}

interface CareerLadderProps {
  steps: LadderStep[];
}

/**
 * The four-rung career ladder, rebuilt horizontally per the v2 reference:
 * an amber rail across the top, nodes hanging from it, connectors down to
 * equal-height cards. Collapses to 2×2 below 1020px and to a vertical
 * node-beside-card layout below 620px.
 *
 * The CTA per rung is optional so this serves both the approved homepage
 * ladder (no CTAs) and /learners, which still links out per rung.
 */
export default function CareerLadder({ steps }: CareerLadderProps) {
  return (
    <div className={styles.ladder}>
      {steps.map((step) => (
        <Reveal key={step.title} className={styles.rung}>
          <div className={styles.node}>{step.num}</div>
          <div className={styles.body}>
            <div className={styles.top}>
              <h3>{step.title}</h3>
              {step.isFeatured && step.featuredLabel ? (
                <span className={styles.featuredTag}>{step.featuredLabel}</span>
              ) : (
                <span className={styles.phase}>{step.tag}</span>
              )}
            </div>

            <p className={styles.desc}>{step.forText}</p>
            {step.price && <p className={styles.price}>{step.price}</p>}

            <div className={styles.out}>
              <svg
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2.4"
                strokeLinecap="round"
                strokeLinejoin="round"
                aria-hidden="true"
              >
                <path d="M20 6L9 17l-5-5" />
              </svg>
              Outcome: {step.outcome}
            </div>

            {step.ctaText && step.ctaHref && (
              <Link
                href={step.ctaHref}
                className={`btn btn-sm ${step.isFeatured ? 'btn-primary' : 'btn-outline'} ${styles.cta}`}
              >
                {step.ctaText}
              </Link>
            )}
          </div>
        </Reveal>
      ))}
    </div>
  );
}
