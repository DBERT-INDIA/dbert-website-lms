import React from 'react';

type HandNoteProps = {
  children: React.ReactNode;
  /** Amber (default) or blue ink. */
  tone?: 'amber' | 'blue';
  className?: string;
};

/**
 * A handwritten margin annotation — the Caveat-set asides in the reference.
 *
 * Decorative by intent: the surrounding copy always carries the same meaning,
 * so these are hidden from assistive tech rather than read out as stray
 * fragments.
 */
export default function HandNote({ children, tone = 'amber', className }: HandNoteProps) {
  return (
    <span
      className={`handnote${tone === 'blue' ? ' blue' : ''}${className ? ` ${className}` : ''}`}
      aria-hidden="true"
    >
      {children}
    </span>
  );
}
