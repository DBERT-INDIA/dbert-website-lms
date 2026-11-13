'use client';

import { useState } from 'react';
import styles from './StudioInPractice.module.css';

export type StudioFocus = 'founders' | 'products' | 'learners';

const practices: Array<{
  id: StudioFocus;
  number: string;
  title: string;
  description: string;
  note: string;
}> = [
  {
    id: 'founders',
    number: '01',
    title: 'Back good founders',
    description: 'with engineering, not advice alone',
    note: 'Founders work alongside the engineering team and keep ownership of their product IP.',
  },
  {
    id: 'products',
    number: '02',
    title: 'Build useful software',
    description: 'from problems we meet ourselves',
    note: 'The products begin as tools for real work inside the studio, then are prepared for other teams.',
  },
  {
    id: 'learners',
    number: '03',
    title: 'Teach by doing the work',
    description: 'alongside the teams that ship it',
    note: 'Learners move from foundations into reviewed work on the software our teams build.',
  },
];

const audienceLabel: Record<StudioFocus, string> = {
  founders: 'For founders',
  products: 'For product teams',
  learners: 'For learners',
};

export default function StudioInPractice({
  focus = 'founders',
}: {
  focus?: StudioFocus;
}) {
  const [active, setActive] = useState<StudioFocus>(focus);
  const selected = practices.find((practice) => practice.id === active) ?? practices[0];

  return (
    <aside className={styles.panel} aria-label="The studio, in practice">
      <div className={styles.heading}>
        <span className={styles.overline}>How the work connects</span>
        <h2>The studio, in practice</h2>
      </div>

      <div className={styles.steps} aria-label="Studio practices">
        {practices.map((practice) => (
          <button
            key={practice.id}
            className={styles.step}
            type="button"
            aria-pressed={active === practice.id}
            onClick={() => setActive(practice.id)}
          >
            <span className={styles.number}>{practice.number}</span>
            <span className={styles.copy}>
              <strong>{practice.title}</strong>
              <small>{practice.description}</small>
            </span>
            <span className={styles.indicator} aria-hidden="true" />
          </button>
        ))}
      </div>

      <div className={styles.note} aria-live="polite" aria-atomic="true">
        <span>{audienceLabel[active]}</span>
        <p>{selected.note}</p>
      </div>
    </aside>
  );
}
