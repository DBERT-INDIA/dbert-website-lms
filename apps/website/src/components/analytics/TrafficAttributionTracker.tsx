'use client';

import { useEffect } from 'react';

export interface TrafficAttributionData {
  landingPage: string;
  referrer: string;
  referrerDomain: string;
  channel: 'ai_search' | 'organic_search' | 'whatsapp' | 'linkedin' | 'direct' | 'referral';
  aiSource?: string;
  utmSource?: string;
  utmMedium?: string;
  utmCampaign?: string;
  refCode?: string;
  device: 'Mobile' | 'Tablet' | 'Desktop';
  screenRes: string;
  timestamp: string;
}

export default function TrafficAttributionTracker() {
  useEffect(() => {
    if (typeof window === 'undefined') return;

    try {
      const STORAGE_KEY = 'dbert_first_touch_v1';
      const COOKIE_NAME = 'dbert_ft';

      // Function to check if attribution is already recorded
      const hasFirstTouch = !!localStorage.getItem(STORAGE_KEY);
      if (hasFirstTouch) {
        return; // First touch already secured
      }

      const ua = navigator.userAgent || '';
      let device: 'Mobile' | 'Tablet' | 'Desktop' = 'Desktop';
      if (/Tablet|iPad/i.test(ua)) {
        device = 'Tablet';
      } else if (/Mobile|Android|iPhone|iPod|webOS|BlackBerry|IEMobile|Opera Mini/i.test(ua)) {
        device = 'Mobile';
      }

      const rawReferrer = document.referrer || '';
      let referrerDomain = '';
      try {
        if (rawReferrer) {
          referrerDomain = new URL(rawReferrer).hostname.toLowerCase();
        }
      } catch (e) {
        referrerDomain = '';
      }

      const urlParams = new URLSearchParams(window.location.search);
      const utmSource = (urlParams.get('utm_source') || '').toLowerCase();
      const utmMedium = (urlParams.get('utm_medium') || '').toLowerCase();
      const utmCampaign = (urlParams.get('utm_campaign') || '').toLowerCase();
      const refCode = urlParams.get('ref') || '';

      // Multi-tier source classification
      let channel: TrafficAttributionData['channel'] = 'direct';
      let aiSource: string | undefined = undefined;

      // 1. AI Assistant Detection
      if (
        referrerDomain.includes('chatgpt.com') ||
        referrerDomain.includes('openai.com') ||
        utmSource.includes('chatgpt')
      ) {
        channel = 'ai_search';
        aiSource = 'ChatGPT';
      } else if (
        referrerDomain.includes('perplexity.ai') ||
        utmSource.includes('perplexity')
      ) {
        channel = 'ai_search';
        aiSource = 'Perplexity';
      } else if (
        referrerDomain.includes('claude.ai') ||
        referrerDomain.includes('anthropic.com') ||
        utmSource.includes('claude')
      ) {
        channel = 'ai_search';
        aiSource = 'Claude';
      } else if (
        referrerDomain.includes('gemini.google.com') ||
        utmSource.includes('gemini')
      ) {
        channel = 'ai_search';
        aiSource = 'Gemini';
      } else if (
        referrerDomain.includes('copilot.microsoft.com') ||
        utmSource.includes('copilot')
      ) {
        channel = 'ai_search';
        aiSource = 'Copilot';
      }
      // 2. WhatsApp Outreach
      else if (
        utmSource === 'whatsapp' ||
        referrerDomain.includes('whatsapp') ||
        referrerDomain.includes('wa.me')
      ) {
        channel = 'whatsapp';
      }
      // 3. LinkedIn Referral
      else if (
        utmSource === 'linkedin' ||
        referrerDomain.includes('linkedin.com') ||
        referrerDomain.includes('lnkd.in')
      ) {
        channel = 'linkedin';
      }
      // 4. Organic Search
      else if (
        referrerDomain.includes('google.') ||
        referrerDomain.includes('bing.') ||
        referrerDomain.includes('duckduckgo.') ||
        referrerDomain.includes('yahoo.') ||
        referrerDomain.includes('ecosia.')
      ) {
        channel = 'organic_search';
      }
      // 5. Direct / Self-Referral
      else if (
        !rawReferrer ||
        referrerDomain.includes('dbert.in') ||
        referrerDomain.includes('dbert.online')
      ) {
        channel = 'direct';
      }
      // 6. Generic Referral
      else {
        channel = 'referral';
      }

      const screenRes = `${window.screen?.width || 0}x${window.screen?.height || 0}`;
      const landingPage = window.location.pathname + window.location.search;

      const attribution: TrafficAttributionData = {
        landingPage,
        referrer: rawReferrer,
        referrerDomain,
        channel,
        aiSource,
        utmSource: utmSource || undefined,
        utmMedium: utmMedium || undefined,
        utmCampaign: utmCampaign || undefined,
        refCode: refCode || undefined,
        device,
        screenRes,
        timestamp: new Date().toISOString(),
      };

      // Store in localStorage
      localStorage.setItem(STORAGE_KEY, JSON.stringify(attribution));

      // Store in .dbert.in cookie for cross-subdomain access (website & LMS)
      const isDbertDomain = window.location.hostname.includes('dbert.in');
      const domainAttr = isDbertDomain ? ';domain=.dbert.in' : '';
      const cookieVal = encodeURIComponent(
        JSON.stringify({
          lp: landingPage.substring(0, 80),
          ch: channel,
          ai: aiSource,
          dev: device,
          ref: refCode || undefined,
          ts: Date.now(),
        })
      );
      document.cookie = `${COOKIE_NAME}=${cookieVal};max-age=2592000;path=/${domainAttr};SameSite=Lax`;

      // Non-blocking telemetry beacon to server
      const payload = JSON.stringify(attribution);
      if (navigator.sendBeacon) {
        navigator.sendBeacon('/api/telemetry/traffic', payload);
      } else {
        fetch('/api/telemetry/traffic', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: payload,
          keepalive: true,
        }).catch(() => {});
      }
    } catch (e) {
      // Non-intrusive error guard
    }
  }, []);

  return null;
}
