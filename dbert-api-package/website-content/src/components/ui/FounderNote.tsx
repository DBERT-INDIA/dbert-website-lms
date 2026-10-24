import React from 'react';
import styles from './FounderNote.module.css';
import Reveal from './Reveal';

type FounderNoteProps = {
  /** Small label above the heading, e.g. "A note from the founder". */
  label: string;
  heading: string;
  /** Body paragraphs. Nodes rather than strings so a word can be emphasised. */
  paragraphs: React.ReactNode[];
  /** Handwritten signature line, e.g. "— Abhinav". */
  signature: string;
  /** Mono attribution beneath the signature. */
  attribution: React.ReactNode;
};

/**
 * The founder's letter: taped to the page, very slightly rotated, signed in
 * Caveat. Deliberately reads as a letter rather than a marketing section.
 */
export default function FounderNote({
  label,
  heading,
  paragraphs,
  signature,
  attribution,
}: FounderNoteProps) {
  return (
    <Reveal className={styles.card}>
      <div className="doclabel">{label}</div>
      <h2>{heading}</h2>
      <div className={styles.body}>
        {paragraphs.map((paragraph, index) => (
          <p key={index}>{paragraph}</p>
        ))}
      </div>
      <div className={styles.sign}>
        <span className={styles.sig}>{signature}</span>
        <span className={styles.attribution}>{attribution}</span>
      </div>
    </Reveal>
  );
}
