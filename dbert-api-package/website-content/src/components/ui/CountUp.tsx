'use client';

import React, { useEffect, useRef } from 'react';

type CountUpProps = {
  /** Final value to count to. */
  end: number;
  prefix?: string;
  suffix?: string;
  /** Animation length in ms. */
  duration?: number;
  /** Element to render. Defaults to a span. */
  as?: React.ElementType;
  className?: string;
};

/**
 * Counts from 0 to `end` the first time it scrolls into view, on the same
 * cubic ease-out and 1100ms duration as the reference file.
 *
 * Progressively enhanced: the SSR markup renders the approved `end` value
 * directly, ensuring web crawlers, search engines, and JS-deferred browsers
 * never display an uninitialized zero. When in view, client-side JS animates
 * the transition smoothly. Under prefers-reduced-motion, `end` remains static.
 */
export default function CountUp({
  end,
  prefix = '',
  suffix = '',
  duration = 1100,
  as: Tag = 'span',
  className,
}: CountUpProps) {
  const ref = useRef<HTMLElement>(null);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;

    const render = (value: number) => {
      el.textContent = `${prefix}${value}${suffix}`;
    };

    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    if (prefersReducedMotion || typeof IntersectionObserver === 'undefined') {
      render(end);
      return;
    }

    let frame = 0;

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          observer.unobserve(entry.target);

          // Reset to 0 just before triggering smooth count-up animation
          render(0);

          const start = performance.now();
          const tick = (now: number) => {
            const progress = Math.min((now - start) / duration, 1);
            // ease-out cubic
            render(Math.round(end * (1 - Math.pow(1 - progress, 3))));
            if (progress < 1) frame = requestAnimationFrame(tick);
          };
          frame = requestAnimationFrame(tick);
        });
      },
      { threshold: 0.2 }
    );

    observer.observe(el);

    return () => {
      observer.disconnect();
      if (frame) cancelAnimationFrame(frame);
    };
  }, [end, prefix, suffix, duration]);

  return (
    <Tag ref={ref} className={className}>
      {prefix}{end}{suffix}
    </Tag>
  );
}
