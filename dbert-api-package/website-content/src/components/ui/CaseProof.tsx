import React from 'react';
import styles from './CaseProof.module.css';
import Reveal from './Reveal';

export type KeyDatum = {
  label: string;
  value: string;
  /** Portion of the value to accent, rendered before the rest. */
  accent?: string;
};

type CaseProofProps = {
  /** Small uppercase kicker, e.g. "Case study · Alkame". */
  kicker: string;
  quote: string;
  authorName: string;
  authorRole: string;
  /** Letter shown in the avatar disc. Defaults to the name's initial. */
  authorInitial?: string;
  data: KeyDatum[];
  /** Stamp text. Omit to hide the stamp. */
  stamp?: string;
};

/**
 * Two-panel case study: the quote on the left, hard numbers on the right,
 * and a rotated rubber stamp over the corner.
 *
 * Only use this with a real, attributable quote. Statistics on the site are
 * founder-approved, but a testimonial puts words in a named third party's
 * mouth and needs that person's sign-off (CLAUDE-TASKS.md 8.5).
 */
export default function CaseProof({
  kicker,
  quote,
  authorName,
  authorRole,
  authorInitial,
  data,
  stamp,
}: CaseProofProps) {
  return (
    <Reveal className={styles.case}>
      {stamp && (
        <div className={styles.stamp} aria-hidden="true">
          {stamp}
        </div>
      )}

      <div className={styles.copy}>
        <span className={styles.kicker}>{kicker}</span>
        <blockquote className={styles.quote}>{quote}</blockquote>
        <div className={styles.who}>
          <div className={styles.av} aria-hidden="true">
            {authorInitial ?? authorName.charAt(0)}
          </div>
          <div>
            <div className={styles.nm}>{authorName}</div>
            <div className={styles.rl}>{authorRole}</div>
          </div>
        </div>
      </div>

      <div className={styles.data}>
        {data.map((datum) => (
          <div key={datum.label} className={styles.kd}>
            <span className={styles.k}>{datum.label}</span>
            <span className={styles.v}>
              {datum.accent && <em>{datum.accent} </em>}
              {datum.value}
            </span>
          </div>
        ))}
      </div>
    </Reveal>
  );
}
