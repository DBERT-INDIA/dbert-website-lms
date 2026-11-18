/**
 * dbert-push-client.js - Sovereign Native Web Push Client Controller
 * Connects browser Service Worker to DBERT VAPID Web Push Engine.
 * Active-by-default with transparent device tracking.
 */
(function(window) {
  'use strict';

  let _vapidPublicKey = null;
  let _swRegistration = null;

  function urlBase64ToUint8Array(base64String) {
    const padding = '='.repeat((4 - base64String.length % 4) % 4);
    const base64 = (base64String + padding).replace(/\-/g, '+').replace(/_/g, '/');
    const rawData = window.atob(base64);
    const outputArray = new Uint8Array(rawData.length);
    for (let i = 0; i < rawData.length; ++i) {
      outputArray[i] = rawData.charCodeAt(i);
    }
    return outputArray;
  }

  function detectDeviceInfo() {
    const ua = navigator.userAgent;
    let os = 'Unknown OS';
    if (ua.indexOf('Win') !== -1) os = 'Windows';
    else if (ua.indexOf('Mac') !== -1 && ua.indexOf('iPhone') === -1 && ua.indexOf('iPad') === -1) os = 'macOS';
    else if (ua.indexOf('Android') !== -1) os = 'Android';
    else if (ua.indexOf('iPhone') !== -1 || ua.indexOf('iPad') !== -1) os = 'iOS';
    else if (ua.indexOf('Linux') !== -1) os = 'Linux';

    let browser = 'Browser';
    if (ua.indexOf('Edg') !== -1) browser = 'Edge';
    else if (ua.indexOf('Chrome') !== -1 && ua.indexOf('Edg') === -1) browser = 'Chrome';
    else if (ua.indexOf('Safari') !== -1 && ua.indexOf('Chrome') === -1) browser = 'Safari';
    else if (ua.indexOf('Firefox') !== -1) browser = 'Firefox';

    const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(ua);
    const deviceType = isMobile ? 'mobile' : 'desktop';
    const deviceName = `${os} - ${browser}`;

    return { deviceName, deviceType, userAgent: ua };
  }

  function getCsrfToken() {
    const meta = document.querySelector('meta[name="csrf-token"]');
    if (meta && meta.content) return meta.content;
    const inp = document.querySelector('input[name="_csrf_token"]') || document.querySelector('input[name="csrf_token"]');
    if (inp && inp.value) return inp.value;
    return '';
  }

  async function getVapidPublicKey() {
    if (_vapidPublicKey) return _vapidPublicKey;
    try {
      const resp = await fetch('/api/push/vapid-public-key');
      const data = await resp.json();
      if (data.status === 'success' && data.publicKey) {
        _vapidPublicKey = data.publicKey;
        return _vapidPublicKey;
      }
    } catch (e) {
      console.warn('[DBERT Push] Failed to fetch VAPID public key:', e);
    }
    return null;
  }

  async function sendSubscriptionToServer(subscription, userEmail) {
    if (!subscription) return;
    const key = subscription.getKey ? subscription.getKey('p256dh') : null;
    const auth = subscription.getKey ? subscription.getKey('auth') : null;
    if (!key || !auth) return;

    const p256dh = btoa(String.fromCharCode.apply(null, new Uint8Array(key)));
    const authStr = btoa(String.fromCharCode.apply(null, new Uint8Array(auth)));
    const { deviceName, deviceType, userAgent } = detectDeviceInfo();
    const token = getCsrfToken();

    try {
      const resp = await fetch('/api/push/subscribe', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRF-Token': token,
          'X-CSRFToken': token
        },
        body: JSON.stringify({
          endpoint: subscription.endpoint,
          keys: {
            p256dh: p256dh,
            auth: authStr
          },
          user_email: userEmail || '',
          device_name: deviceName,
          device_type: deviceType,
          user_agent: userAgent
        })
      });
      const res = await resp.json();
      if (res.status === 'success') {
        console.log('[DBERT Push] Device registered successfully:', deviceName);
        window.dispatchEvent(new CustomEvent('dbert-push-updated', { detail: { subscription, deviceName } }));
      }
    } catch (e) {
      console.warn('[DBERT Push] Failed to record subscription on server:', e);
    }
  }

  const DBERTPush = {
    async init(userEmail) {
      if (!('serviceWorker' in navigator) || !('PushManager' in window)) {
        return false;
      }

      try {
        _swRegistration = await navigator.serviceWorker.register('/sw-push.js', { scope: '/' });
      } catch (e1) {
        console.warn('[DBERT Push] /sw-push.js registration failed, trying /static/sw-push.js fallback:', e1);
        try {
          _swRegistration = await navigator.serviceWorker.register('/static/sw-push.js', { scope: '/' });
        } catch (e2) {
          console.warn('[DBERT Push] Service worker registration failed completely:', e2);
          return false;
        }
      }

      try {
        // If permission is already granted, auto-subscribe silently
        if (Notification.permission === 'granted') {
          await this.autoSubscribe(userEmail);
        }
        return true;
      } catch (e) {
        console.warn('[DBERT Push] Service worker auto-subscribe error:', e);
        return false;
      }
    },

    async autoSubscribe(userEmail) {
      if (!_swRegistration) {
        await this.init(userEmail);
      }
      if (!_swRegistration || Notification.permission !== 'granted') {
        return null;
      }

      const pubKey = await getVapidPublicKey();
      if (!pubKey) return null;

      try {
        let sub = await _swRegistration.pushManager.getSubscription();
        if (!sub) {
          sub = await _swRegistration.pushManager.subscribe({
            userVisibleOnly: true,
            applicationServerKey: urlBase64ToUint8Array(pubKey)
          });
        }
        await sendSubscriptionToServer(sub, userEmail);
        return sub;
      } catch (e) {
        console.warn('[DBERT Push] autoSubscribe error:', e);
        return null;
      }
    },

    async requestPermissionAndSubscribe(userEmail) {
      if (!('Notification' in window)) return null;

      if (!_swRegistration) {
        await this.init(userEmail);
      }

      try {
        const permission = await Notification.requestPermission();
        if (permission === 'granted') {
          return await this.autoSubscribe(userEmail);
        }
      } catch (e) {
        console.warn('[DBERT Push] requestPermission error:', e);
      }
      return null;
    },

    async unsubscribe() {
      if (!_swRegistration) return;
      try {
        const sub = await _swRegistration.pushManager.getSubscription();
        if (sub) {
          const token = getCsrfToken();
          await fetch('/api/push/unsubscribe', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'X-CSRF-Token': token,
              'X-CSRFToken': token
            },
            body: JSON.stringify({ endpoint: sub.endpoint })
          });
          await sub.unsubscribe();
          console.log('[DBERT Push] Device unsubscribed successfully.');
          window.dispatchEvent(new CustomEvent('dbert-push-updated', { detail: { unsubscribed: true } }));
        }
      } catch (e) {
        console.warn('[DBERT Push] Unsubscribe failed:', e);
      }
    }
  };

  window.DBERTPush = DBERTPush;

  // Auto-init on page load if intern email is known in session
  document.addEventListener('DOMContentLoaded', function() {
    const metaEmail = document.querySelector('meta[name="user-email"]');
    const userEmail = metaEmail ? metaEmail.content : (window.__INTERN_EMAIL__ || '');
    DBERTPush.init(userEmail);
  });

})(window);
