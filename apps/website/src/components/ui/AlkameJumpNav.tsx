'use client';

import s from './AlkameJumpNav.module.css';

import React, { useEffect, useState } from 'react';

const NAV_ITEMS = [
  { id: 'research-question', label: 'Research Question' },
  { id: 'architecture', label: 'Architecture' },
  { id: 'challenges', label: 'Challenges' },
  { id: 'timeline', label: 'Timeline' },
  { id: 'team', label: 'Team' },
];

export default function AlkameJumpNav() {
  const [activeId, setActiveId] = useState(NAV_ITEMS[0].id);

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            setActiveId(entry.target.id);
          }
        });
      },
      // Treat a section as "active" once it's crossed roughly the upper-middle
      // of the viewport, so the highlight changes right as a section takes over.
      { rootMargin: '-15% 0px -70% 0px', threshold: 0 }
    );

    NAV_ITEMS.forEach((item) => {
      const el = document.getElementById(item.id);
      if (el) observer.observe(el);
    });

    return () => observer.disconnect();
  }, []);

  return (
    <div className={s.bar}>
      <div className={`container ${s.row}`}>
        <span className={s.label}>
          Jump to:
        </span>
        {NAV_ITEMS.map((item) => {
          const isActive = activeId === item.id;
          return (
            <a
              key={item.id}
              href={`#${item.id}`}
              className={`${s.link}${isActive ? ` ${s.linkActive}` : ''}`}
            >
              {item.label}
            </a>
          );
        })}
      </div>
    </div>
  );
}
