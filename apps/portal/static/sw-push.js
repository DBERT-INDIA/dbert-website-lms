// sw-push.js - DBERT Sovereign Native Web Push Service Worker
// Standards-compliant W3C Push API implementation
'use strict';

self.addEventListener('push', function(event) {
  if (!event.data) {
    console.warn('[DBERT Push] Received push event with empty payload');
    return;
  }

  let payload = {};
  try {
    payload = event.data.json();
  } catch (e) {
    payload = {
      title: 'DBERT Platform Update',
      body: event.data.text(),
      data: { url: 'https://lms.dbert.in' }
    };
  }

  const title = payload.title || 'DBERT Notification';
  const options = {
    body: payload.body || 'You have an important update on DBERT.',
    icon: payload.icon || '/static/img/dbert-logo-192.png',
    badge: payload.badge || '/static/img/dbert-badge-96.png',
    data: payload.data || { url: payload.url || 'https://lms.dbert.in' },
    vibrate: [150, 80, 150],
    requireInteraction: payload.requireInteraction || false,
    tag: payload.tag || 'dbert-lifecycle-notification',
    renotify: true
  };

  event.waitUntil(
    self.registration.showNotification(title, options)
  );
});

self.addEventListener('notificationclick', function(event) {
  event.notification.close();
  const targetUrl = (event.notification.data && event.notification.data.url) 
    ? event.notification.data.url 
    : 'https://lms.dbert.in';

  event.waitUntil(
    clients.matchAll({ type: 'window', includeUncontrolled: true }).then(function(clientList) {
      for (let i = 0; i < clientList.length; i++) {
        const client = clientList[i];
        if (client.url && client.url.includes('dbert.in') && 'focus' in client) {
          if ('navigate' in client) {
            client.navigate(targetUrl);
          }
          return client.focus();
        }
      }
      if (clients.openWindow) {
        return clients.openWindow(targetUrl);
      }
    })
  );
});
