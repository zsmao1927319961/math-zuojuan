/* Service Worker：网络优先 + 静态壳缓存。支持 iPad PWA 主屏打开，断网时仍能显示界面壳。 */
const CACHE = 'shuxue-zuojuan-v15';
const SHELL = [
  './',
  './index.html',
  './style.css',
  './app.js',
  './ai_photo_module.js',
  './manifest.json',
  './icon-192.png',
  './icon-512.png'
];

self.addEventListener('install', (e) => {
  // 逐条缓存，单个失败不拖垮整个安装
  e.waitUntil(
    caches.open(CACHE).then((c) =>
      Promise.allSettled(SHELL.map((u) => c.add(u)))
    ).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

// 接收页面请求：立即接管（skipWaiting + claim），配合前端自动刷新
self.addEventListener('message', (e) => {
  if (e.data && e.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});

self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);

  // API、题库图片、外部 CDN：一律走网络，不缓存（避免旧数据/超大缓存）
  if (url.origin !== location.origin) return;
  if (url.pathname.startsWith('/api/') || url.pathname.startsWith('/data/')) return;

  // 静态资源：网络优先，成功则更新缓存；断网回退缓存
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
