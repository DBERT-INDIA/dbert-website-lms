'use client';

import { useEffect } from 'react';
import { usePathname } from 'next/navigation';

/**
 * One IntersectionObserver for every `.rv` element on the page.
 *
 * Mounted once in the root layout. Re-scans on route change so client-side
 * navigations pick up the new page's elements.
 */
export default function RevealObserver() {
  const pathname = usePathname();

  useEffect(() => {
    const elements = Array.from(document.querySelectorAll<HTMLElement>('.rv:not(.in)'));
    if (elements.length === 0) return;

    if (typeof IntersectionObserver === 'undefined') {
      elements.forEach((el) => el.classList.add('in'));
      return;
    }

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          entry.target.classList.add('in');
          observer.unobserve(entry.target);
        });
      },
      { threshold: 0.12 }
    );

    elements.forEach((el) => observer.observe(el));
    return () => observer.disconnect();
  }, [pathname]);

  return null;
}
