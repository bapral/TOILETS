// 資料與程式合一的 PWA 快取管理腳本
// 當 build_app.py 執行時，會自動更新此處的 CACHE_NAME 版本號
const CACHE_NAME = 'toilet-app-v20260419-013108'; 

const urlsToCache = [
  './',
  'index.html',
  'manifest.json',
  'toilets.json', // 全國公廁資料包 (清理後的 2.5 萬筆數據)
  'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css',
  'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js'
];

/** 
 * 安裝事件：下載並快取所有核心檔案
 */
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      console.log('[Service Worker] 正在快取所有資源包...');
      return cache.addAll(urlsToCache);
    })
  );
  // 立即接管，不需等待舊版 SW 結束
  self.skipWaiting();
});

/** 
 * 啟動事件：清理舊版快取
 */
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            console.log('[Service Worker] 正在移除舊版快取:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});

/** 
 * 攔截請求事件：優先從快取回傳，支援離線使用
 */
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request).then(response => {
      return response || fetch(event.request);
    })
  );
});
