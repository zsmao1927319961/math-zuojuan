/* 学习工作台 Service Worker：网络优先 + 壳缓存，支持 iPad 主屏离线打开。 */
const CACHE = 'study-v1';
const SHELL = [
  './',
  './index.html',
  './pdf.min.js',
  './pdf.worker.min.js',
  './manifest.json',
  './icon-192.png',
  './icon-512.png',
  './katex/katex.min.css',
  './katex/katex.min.js',
  './katex/contrib/auto-render.min.js',
  '../katex/katex.min.css',
  '../katex/katex.min.js',
  '../katex/contrib/auto-render.min.js'
];

self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE).then((c) =>
      Promise.allSettled(SHELL.map((u) => c.add(u)))
    ).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin !== location.origin) return;          // AI API 请求不拦截
  e.respondWith(
    fetch(req).then((res) => {
      if (res.ok) {
        const copy = res.clone();
        caches.open(CACHE).then((c) => c.put(req, copy));
      }
      return res;
    }).catch(() => caches.match(req).then((hit) => hit || caches.match('./index.html')))
  );
});
