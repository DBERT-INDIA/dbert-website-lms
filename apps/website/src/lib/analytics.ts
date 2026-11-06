// apps/website/src/lib/analytics.ts

declare global {
  interface Window {
    gtag?: (...args: unknown[]) => void;
    dataLayer?: unknown[];
  }
}

export type EventParams = Record<string, string | number | boolean | undefined>;

export const GA_MEASUREMENT_ID = process.env.NEXT_PUBLIC_GA_ID || 'G-MN7ME9X518';

/**
 * Fires a custom Google Analytics 4 event.
 * Safely guards against server-side rendering and missing gtag in static builds.
 */
export function trackEvent(eventName: string, params?: EventParams) {
  if (typeof window === 'undefined' || typeof window.gtag !== 'function') return;
  try {
    window.gtag('event', eventName, params);
  } catch (err) {
    if (process.env.NODE_ENV === 'development') {
      console.debug(`[GA4 Event Failed: ${eventName}]`, err);
    }
  }
}
