'use client';

import React, { useState } from 'react';
import { ChevronDown } from 'lucide-react';
import type { CurriculumModule } from '@/data/courses.types';

interface CurriculumAccordionProps {
  trackId: string;
  modules: CurriculumModule[];
}

function trackCurriculumExpand(trackId: string, period: string) {
  if (typeof window !== 'undefined' && typeof (window as unknown as { gtag?: (...args: unknown[]) => void }).gtag === 'function') {
    (window as unknown as { gtag: (...args: unknown[]) => void }).gtag('event', 'curriculum_expand', {
      track_id: trackId,
      period,
    });
  }
}

export default function CurriculumAccordion({ trackId, modules }: CurriculumAccordionProps) {
  const [openIndex, setOpenIndex] = useState<number | null>(0);

  const toggle = (idx: number, period: string) => {
    const next = openIndex === idx ? null : idx;
    setOpenIndex(next);
    if (next !== null) {
      trackCurriculumExpand(trackId, period);
    }
  };

  return (
    <div className="space-y-3" role="region" aria-label="Week-by-week curriculum">
      {modules.map((mod, idx) => {
        const isOpen = openIndex === idx;
        const panelId = `curriculum-panel-${trackId}-${idx}`;
        const buttonId = `curriculum-btn-${trackId}-${idx}`;

        return (
          <div key={mod.period} className="card bg-card border border-line overflow-hidden">
            <button
              id={buttonId}
              type="button"
              aria-expanded={isOpen}
              aria-controls={panelId}
              onClick={() => toggle(idx, mod.period)}
              className="w-full text-left p-5 flex items-center justify-between gap-4 bg-transparent border-0 hover:bg-white/[0.02] focus-visible:outline focus-visible:outline-2 focus-visible:outline-accent transition-colors"
            >
              <div>
                <div className="text-xs font-mono text-accent uppercase tracking-wider mb-1">
                  {mod.period}
                </div>
                <div className="font-mono text-base font-bold text-white">
                  {mod.title}
                </div>
              </div>
              <ChevronDown
                size={18}
                aria-hidden="true"
                className={`shrink-0 text-muted transition-transform duration-200 ${isOpen ? 'rotate-180' : ''}`}
              />
            </button>

            {isOpen && (
              <div id={panelId} role="region" aria-labelledby={buttonId} className="px-5 pb-5 pt-1 border-t border-line/50">
                <ul className="list-disc pl-5 text-sm text-[var(--text-secondary)] space-y-1.5 my-3">
                  {mod.topics.map((topic) => (
                    <li key={topic}>{topic}</li>
                  ))}
                </ul>
                <div className="mt-3 p-3 rounded border border-line/70 bg-[var(--surface-base)] text-xs font-mono">
                  <span className="text-accent font-semibold">Deliverable: </span>
                  <span className="text-[var(--text-primary)]">{mod.deliverable}</span>
                </div>
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}
