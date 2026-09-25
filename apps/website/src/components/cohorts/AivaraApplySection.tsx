'use client';

import React, { useState, useRef } from 'react';
import AivaraCohortForm from './AivaraCohortForm';
import { ArrowDownCircle, ChevronUp, Sparkles, Clock, Laptop, ShieldCheck } from 'lucide-react';
import s from './cohort.module.css';

export default function AivaraApplySection() {
  const [isExpanded, setIsExpanded] = useState<boolean>(false);
  const formRef = useRef<HTMLDivElement>(null);

  const handleOpenForm = () => {
    setIsExpanded(true);
    setTimeout(() => {
      formRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 50);
  };

  const handleToggleForm = () => {
    setIsExpanded(prev => !prev);
  };

  return (
    <div id="apply" ref={formRef} className={s.applySectionWrapper}>
      {!isExpanded ? (
        <div className={`card center ${s.applyCtaCard} ${s.applyCtaCardInner}`}>
          <div className={s.applyDoclabelWrap}>
            <span className="icon-chip"><Sparkles size={16} aria-hidden="true" /></span>
            <span className={`doclabel ${s.applyDoclabel}`}>
              BATCH OF 2026 • APPLICATIONS ACTIVE
            </span>
          </div>

          <h2 className={s.applyTitle}>
            Ready to Build With Aivara Technologies?
          </h2>
          <p className={`measure-sm ${s.applySubtitle}`}>
            The 3-step candidate application takes approximately 3 minutes. Choose your internship track, link your CV, and secure your place in the upcoming cohort sprint.
          </p>

          <div className={s.benefitPillsRow}>
            <div className={s.benefitPillItem}>
              <Clock size={15} color="var(--accent)" /> 10–15 hrs/week async sprints
            </div>
            <div className={s.benefitPillItem}>
              <Laptop size={15} color="var(--accent)" /> 100% Remote
            </div>
            <div className={s.benefitPillItem}>
              <ShieldCheck size={15} color="var(--accent)" /> Verified Certification
            </div>
          </div>

          <button
            onClick={handleOpenForm}
            className={`btn btn-primary btn-lg ${s.applyBtn}`}
          >
            Apply Now
            <ArrowDownCircle size={20} />
          </button>
          <p className={s.expandNotice}>
            Form will expand below
          </p>
        </div>
      ) : (
        <div>
          <div className={s.expandedHeader}>
            <div>
              <span className={`doclabel ${s.applyDoclabel}`}>APPLICATION GATEWAY OPEN</span>
              <h2 className={s.expandedTitle}>Candidate Application Form</h2>
            </div>
            <button
              onClick={handleToggleForm}
              className="btn btn-outline btn-xs inline-flex items-center gap-1"
            >
              <ChevronUp size={14} /> Collapse Form
            </button>
          </div>

          <AivaraCohortForm />
        </div>
      )}
    </div>
  );
}

