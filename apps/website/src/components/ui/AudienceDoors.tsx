import React from 'react';
import Link from 'next/link';
import styles from './AudienceDoors.module.css';
import Reveal from './Reveal';

export type AudienceKind = 'founder' | 'enterprise' | 'learner';

export type Door = {
  kind: AudienceKind;
  /** Small uppercase label, e.g. "Founders". */
  who: string;
  title: string;
  description: string;
  ctaLabel: string;
  href: string;
};

type AudienceDoorsProps = {
  doors: Door[];
};

const toneClass: Record<AudienceKind, string> = {
  founder: styles.founder,
  enterprise: styles.enterprise,
  learner: styles.learner,
};

/**
 * The three colour-coded router cards below the hero — the "who are you"
 * split that sends founders, enterprises, and learners down different paths.
 * Colour is carried by a --door-c custom property per card.
 */
export default function AudienceDoors({ doors }: AudienceDoorsProps) {
  return (
    <div className={styles.grid}>
      {doors.map((door) => (
        <Reveal key={door.href} as="div">
          <Link href={door.href} className={`${styles.door} ${toneClass[door.kind]}`}>
            <div className={styles.who}>{door.who}</div>
            <h3>{door.title}</h3>
            <p>{door.description}</p>
            <span className={styles.go}>
              {door.ctaLabel}{' '}
              <span className="arr" aria-hidden="true">
                →
              </span>
            </span>
          </Link>
        </Reveal>
      ))}
    </div>
  );
}
