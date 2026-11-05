const CACHE_NAME = 'ada-atlas-v5';
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
  './data/drills.json'
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
    caches.match(event.request).then((cached) => {
      return cached || fetch(event.request).then((res) => {
        const clone = res.clone();
        caches.open(CACHE_NAME).then((cache) => cache.put(event.request, clone)).catch(() => {});
        return res;
      }).catch(() => cached);
    })
  );
});
