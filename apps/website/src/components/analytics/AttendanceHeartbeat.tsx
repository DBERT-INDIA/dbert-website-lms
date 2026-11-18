'use client';

import { useEffect, useRef } from 'react';

/**
 * AttendanceHeartbeat Component for dbert.in
 * Accrues active learning/reading time across all public website pages
 * (articles, courses, project showcases, guides) and credits active time
 * directly into the intern's LMS 10 hours/week attendance ledger via
 * https://lms.dbert.in/attendance/ping using cross-domain credentials.
 */
export default function AttendanceHeartbeat() {
  const isPingingRef = useRef(false);

  useEffect(() => {
    if (typeof window === 'undefined') return;

    const TARGET_ACTIVE_SEC = 180; // 3 minutes = 180 active seconds
    const KEY_ACTIVE_SEC = 'dbert_att_active_sec';
    const KEY_LAST_TICK = 'dbert_att_last_tick_ms';
    const KEY_LAST_PING = 'dbert_att_last_ping_ms';
    const KEY_LAST_USER_ACT = 'dbert_att_user_act_ms';
    const IDLE_TIMEOUT_MS = 120000; // 2 minutes without user interaction pauses timer

    let lastLocalActivity = Date.now();

    function markUserActive() {
      lastLocalActivity = Date.now();
      try {
        localStorage.setItem(KEY_LAST_USER_ACT, lastLocalActivity.toString());
      } catch (e) {}
    }

    const activityEvents = ['mousemove', 'mousedown', 'keydown', 'scroll', 'touchstart', 'click'];
    activityEvents.forEach((evt) => {
      window.addEventListener(evt, markUserActive, { passive: true });
    });

    function isInternActive(): boolean {
      if (document.hidden) return false;
      const now = Date.now();
      let lastAct = lastLocalActivity;
      try {
        const stored = parseInt(localStorage.getItem(KEY_LAST_USER_ACT) || '0', 10);
        if (stored > lastAct) lastAct = stored;
      } catch (e) {}
      return now - lastAct < IDLE_TIMEOUT_MS;
    }

    async function sendAttendancePing() {
      if (isPingingRef.current) return;
      isPingingRef.current = true;

      try {
        const activeSec = parseInt(localStorage.getItem(KEY_ACTIVE_SEC) || '0', 10);
        if (activeSec < TARGET_ACTIVE_SEC) {
          isPingingRef.current = false;
          return;
        }

        const lastPing = parseInt(localStorage.getItem(KEY_LAST_PING) || '0', 10);
        const now = Date.now();
        if (now - lastPing < 170000) {
          isPingingRef.current = false;
          return;
        }

        const lmsBase =
          process.env.NEXT_PUBLIC_LMS_URL ||
          (window.location.hostname === 'localhost' ? 'http://localhost:5001' : 'https://lms.dbert.in');

        const res = await fetch(`${lmsBase}/attendance/ping`, {
          method: 'POST',
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json',
            Accept: 'application/json',
          },
        });

        if (res.status === 401) {
          // User is not signed in to LMS — silent no-op
          isPingingRef.current = false;
          return;
        }

        if (!res.ok) {
          isPingingRef.current = false;
          return;
        }

        const data = await res.json();
        if (data.status === 'ok') {
          try {
            localStorage.setItem(KEY_LAST_PING, Date.now().toString());
            const remainder = Math.max(0, activeSec - TARGET_ACTIVE_SEC);
            localStorage.setItem(KEY_ACTIVE_SEC, remainder.toString());
          } catch (e) {}
        }
      } catch (err) {
        // Silent failure if network or LMS offline
      } finally {
        isPingingRef.current = false;
      }
    }

    // 1-second interval loop tracking active presence
    const intervalId = window.setInterval(() => {
      const now = Date.now();
      const lastTick = parseInt(localStorage.getItem(KEY_LAST_TICK) || '0', 10);

      // Multi-tab coordination: only tick once per second across tabs
      if (now - lastTick < 900) return;

      try {
        localStorage.setItem(KEY_LAST_TICK, now.toString());
      } catch (e) {}

      if (isInternActive()) {
        try {
          const currentSec = parseInt(localStorage.getItem(KEY_ACTIVE_SEC) || '0', 10);
          const newSec = currentSec + 1;
          localStorage.setItem(KEY_ACTIVE_SEC, newSec.toString());

          if (newSec >= TARGET_ACTIVE_SEC) {
            sendAttendancePing();
          }
        } catch (e) {}
      }
    }, 1000);

    return () => {
      window.clearInterval(intervalId);
      activityEvents.forEach((evt) => {
        window.removeEventListener(evt, markUserActive);
      });
    };
  }, []);

  return null;
}
