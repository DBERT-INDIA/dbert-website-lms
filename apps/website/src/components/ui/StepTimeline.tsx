import React from 'react';
import f from './forms.module.css';
import s from './StepTimeline.module.css';

interface Step {
  number: string;
  title: string;
  description: string;
}

interface StepTimelineProps {
  steps: Step[];
}

export default function StepTimeline({ steps }: StepTimelineProps) {
  return (
    <div className="timeline-stepper">
      {steps.map((step, idx) => (
        <div key={idx} className="timeline-step-item">
          <div className="timeline-step-number">{step.number}</div>
          <div className="timeline-step-content bento-card">
            <h3 className={s.stepTitle}>
              {step.title}
            </h3>
            <p className={f.cardCopy}>
              {step.description}
            </p>
          </div>
        </div>
      ))}
    </div>
  );
}
