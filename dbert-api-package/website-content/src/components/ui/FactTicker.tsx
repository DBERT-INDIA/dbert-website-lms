import React from 'react';
import styles from './FactTicker.module.css';

type FactTickerProps = {
  /** Short, true statements. Kept as plain strings — this is a decorative strip. */
  facts: string[];
};

/**
 * The marquee strip of true things.
 *
 * The track is rendered twice so the -50% keyframe loops seamlessly; the
 * duplicate is what makes the loop invisible, not a styling accident. Hovering
 * pauses it. The whole strip is aria-hidden — it is ambient texture, and every
 * fact it shows is stated properly elsewhere on the page.
 */
export default function FactTicker({ facts }: FactTickerProps) {
  if (facts.length === 0) return null;

  return (
    <div className={styles.ticker} aria-hidden="true">
      <div className={styles.track}>
        {facts.map((fact, index) => (
          <span key={`a-${index}`} className={styles.item}>
            {fact}
          </span>
        ))}
        {facts.map((fact, index) => (
          <span key={`b-${index}`} className={styles.item}>
            {fact}
          </span>
        ))}
      </div>
    </div>
  );
}
