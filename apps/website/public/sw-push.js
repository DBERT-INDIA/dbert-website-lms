// sw-push.js - DBERT Sovereign Native Web Push Service Worker (Website Root)
// Standards-compliant W3C Push API implementation
'use strict';

self.addEventListener('push', function(event) {
  if (!event.data) return;

  let payload = {};
  try {
    payload = event.data.json();
  } catch (e) {
    payload = {
      title: 'DBERT Update',
      body: event.data.text(),
      data: { url: 'https://dbert.in' }
    };
  }

  const title = payload.title || 'DBERT Notification';
  const options = {
    body: payload.body || 'You have an important update on DBERT.',
    icon: payload.icon || '/icon.png',
    badge: payload.badge || '/icon.png',
    data: payload.data || { url: payload.url || 'https://dbert.in' },
    vibrate: [150, 80, 150],
    requireInteraction: payload.requireInteraction || false,
    tag: payload.tag || 'dbert-website-notification',
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
    : 'https://dbert.in';

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
