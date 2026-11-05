const CACHE_NAME = 'ada-atlas-v5-3';
const CORE_ASSETS = [
  './',
  './index.html',
  './hub.html',
  './ladder.html',
  './manifest.json',
  './assets/site.css',
  './assets/store.js',
  './assets/site_shell.js',
  './data/ladder.json',
  './data/quizzes.json',
  './data/drills.json',
  './stops/ch0.html',
  './stops/b0.html',
  './stops/ch1.html',
  './stops/b1.html',
  './stops/ch2.html',
  './stops/b2.html',
  './stops/ch3.html',
  './stops/b3.html',
  './stops/ch4.html',
  './stops/b4.html',
  './stops/ch5.html',
  './stops/b5.html',
  './stops/ch6.html',
  './stops/b6.html',
  './stops/ch7.html',
  './stops/b7.html',
  './stops/ch8.html',
  './stops/b8.html',
  './stops/ch9.html',
  './stops/b9.html',
  './stops/ch10.html',
  './stops/b10.html',
  './stops/ch11.html',
  './stops/ch12.html',
  './stops/ch13.html',
  './stops/ch14.html',
  './stops/ch15.html',
  './stops/ch16.html',
  './stops/ch17.html',
  './exam/mock.html',
  './exam/drills.html',
  './exam/bugs.html',
  './exam/order.html',
  './exam/mistakes.html',
  './exam/practice.html',
  './exam/cards.html',
  './exam/cheat.html'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(CORE_ASSETS)).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => Promise.all(keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k)))).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;
  event.respondWith(
    fetch(event.request).then((res) => {
      const clone = res.clone();
      caches.open(CACHE_NAME).then((cache) => cache.put(event.request, clone)).catch(() => {});
      return res;
    }).catch(() => caches.match(event.request).then((cached) => cached || caches.match('./hub.html')))
  );
});
