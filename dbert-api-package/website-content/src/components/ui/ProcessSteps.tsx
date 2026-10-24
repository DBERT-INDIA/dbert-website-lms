import React from 'react';
import styles from './ProcessSteps.module.css';
import Reveal from './Reveal';

export type ProcessStep = {
  /** Two-digit label, e.g. "01". */
  n: string;
  title: string;
  description: string;
  /** Duration hint, e.g. "≈ 5 working days". */
  duration?: string;
};

type ProcessStepsProps = {
  steps: ProcessStep[];
  /**
   * Optional honest-disclosure block rendered beneath the pipeline with an
   * amber left border. Leading label (e.g. "Honest disclosure:") is separate so
   * it can be emphasised.
   */
  disclosure?: {
    label: string;
    text: string;
  };
};

/**
 * Numbered pipeline with a connecting hairline — used for "application to
 * first sprint in four steps" and equivalents.
 */
export default function ProcessSteps({ steps, disclosure }: ProcessStepsProps) {
  return (
    <>
      <div className={styles.proc}>
        {steps.map((step) => (
          <Reveal key={step.n} className={styles.step}>
            <div className={styles.n}>{step.n}</div>
            <h3>{step.title}</h3>
            <p>{step.description}</p>
            {step.duration && <span className={styles.dur}>{step.duration}</span>}
          </Reveal>
        ))}
      </div>

      {disclosure && (
        <Reveal className={styles.honest}>
          <b>{disclosure.label}</b> {disclosure.text}
        </Reveal>
      )}
    </>
  );
}
