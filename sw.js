// Offline: the network first (a new version at once), the cache without network. Audio clips (names = content hash)
// come from the cache once played. Made by scripts/build_web.py, do not edit by hand.
const C='ge-4bb899747dc7',A='ge-audio',F=["index.html", "manifest.webmanifest", "icons/icon-192.png", "icons/icon-512.png"];
self.addEventListener('install',e=>{e.waitUntil(caches.open(C).then(c=>c.addAll(['./',...F])));self.skipWaiting()});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(x=>x!==C&&x!==A).map(x=>caches.delete(x)))).then(()=>self.clients.claim()))});
self.addEventListener('fetch',e=>{const r=e.request,u=new URL(r.url);if(r.method!=='GET'||u.origin!==location.origin)return;
  if(/\/audio\/[^/]+\.mp3$/.test(u.pathname)){e.respondWith(caches.open(A).then(c=>c.match(u.pathname).then(x=>x||fetch(u.pathname).then(y=>{if(y.status===200)c.put(u.pathname,y.clone());return y}))));return}
  e.respondWith(fetch(r).then(x=>{if(x.status===200){const y=x.clone();caches.open(C).then(c=>c.put(r,y))}return x})
    .catch(()=>caches.match(r,{ignoreSearch:true}).then(x=>x||caches.match('index.html'))))});
