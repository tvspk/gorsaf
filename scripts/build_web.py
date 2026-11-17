#!/usr/bin/env python3
"""Web version of the ENGLISH app for GitHub Pages (computer, or a tablet in the browser).

index.html = the same page as in the APK (apk/web-header.html with the offline fonts and the localStorage store,
then game-en/gorsaf-abercastell-en.html from its 3rd line) + install as an app (PWA) + Content-Security-Policy
(network only to api.github.com, for sync and nothing else). Audio: audio/<key>.mp3 next to index.html.
  python3 -I scripts/build_web.py           # writes index.html, sw.js, manifest.webmanifest, icons/, .nojekyll
  python3 -I scripts/build_web.py --check   # only checks they are up to date (GitHub Actions)
Re-run after every python3 -I mnemo/make_en.py.
"""
import hashlib, json, pathlib, sys

root = pathlib.Path(__file__).resolve().parent.parent
game = (root / 'game-en' / 'gorsaf-abercastell-en.html').read_text(encoding='utf-8').split('\n', 2)
assert game[0].startswith('<title>') and 'fonts.googleapis' in game[1], 'game-en should start with <title> then the Google Fonts <link>'
h = (root / 'apk' / 'web-header.html').read_text(encoding='utf-8') + game[2]

CSP = ("default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; "
       "img-src 'self' data: blob:; font-src 'self' data:; media-src 'self' blob:; connect-src 'self' https://api.github.com; "
       "worker-src 'self'; manifest-src 'self'; base-uri 'none'; form-action 'none'; object-src 'none'")
head = ('<meta charset="utf-8">'
        f'<meta http-equiv="Content-Security-Policy" content="{CSP}">'
        '<meta name="referrer" content="no-referrer">'
        '<meta name="theme-color" content="#0c131f">'
        '<link rel="manifest" href="manifest.webmanifest">'
        '<link rel="icon" href="icons/icon-192.png">'
        '<link rel="apple-touch-icon" href="icons/icon-192.png">')
assert h.count('<meta charset="utf-8">') == 1
h = h.replace('<meta charset="utf-8">', head)
h = h.replace('<title>Gorsaf Abercastell</title>', '<title>Gorsaf Abercastell EN</title>', 1)
assert h.rstrip().endswith('</script>')
h = h.rstrip() + ("\n<script>if('serviceWorker' in navigator&&location.protocol==='https:')"
                  "addEventListener('load',()=>navigator.serviceWorker.register('sw.js').catch(()=>{}))</script>\n")

manifest = json.dumps({
    'name': 'Gorsaf Abercastell EN', 'short_name': 'Gorsaf EN', 'lang': 'en-GB', 'start_url': './', 'scope': './',
    'display': 'standalone', 'background_color': '#0c131f', 'theme_color': '#0c131f',
    'icons': [{'src': 'icons/icon-192.png', 'sizes': '192x192', 'type': 'image/png'},
              {'src': 'icons/icon-512.png', 'sizes': '512x512', 'type': 'image/png', 'purpose': 'any'}]}, indent=1) + '\n'

icons = root / 'icons'
if not (icons / 'icon-512.png').exists() and '--check' not in sys.argv:
    from PIL import Image   # only the first time: the icons are committed
    icons.mkdir(exist_ok=True)
    big = Image.open(root / 'apk' / 'icon' / 'conwy-icon.png').convert('RGBA')
    big.save(icons / 'icon-512.png', optimize=True)
    big.resize((192, 192), Image.LANCZOS).save(icons / 'icon-192.png', optimize=True)

files = ['index.html', 'manifest.webmanifest', 'icons/icon-192.png', 'icons/icon-512.png']
ver = hashlib.sha256(h.encode() + manifest.encode() + b''.join((root / f).read_bytes() for f in files[2:] if (root / f).exists())).hexdigest()[:12]
swjs = f"""// Offline: the network first (a new version at once), the cache without network. Audio clips (names = content hash)
// come from the cache once played. Made by scripts/build_web.py, do not edit by hand.
const C='ge-{ver}',A='ge-audio',F={json.dumps(files)};
self.addEventListener('install',e=>{{e.waitUntil(caches.open(C).then(c=>c.addAll(['./',...F])));self.skipWaiting()}});
self.addEventListener('activate',e=>{{e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(x=>x!==C&&x!==A).map(x=>caches.delete(x)))).then(()=>self.clients.claim()))}});
self.addEventListener('fetch',e=>{{const r=e.request,u=new URL(r.url);if(r.method!=='GET'||u.origin!==location.origin)return;
  if(/\\/audio\\/[^/]+\\.mp3$/.test(u.pathname)){{e.respondWith(caches.open(A).then(c=>c.match(u.pathname).then(x=>x||fetch(u.pathname).then(y=>{{if(y.status===200)c.put(u.pathname,y.clone());return y}}))));return}}
  e.respondWith(fetch(r).then(x=>{{if(x.status===200){{const y=x.clone();caches.open(C).then(c=>c.put(r,y))}}return x}})
    .catch(()=>caches.match(r,{{ignoreSearch:true}}).then(x=>x||caches.match('index.html'))))}});
"""
out = {'index.html': h, 'sw.js': swjs, 'manifest.webmanifest': manifest, '.nojekyll': ''}
if '--check' in sys.argv:
    bad = [f for f, t in out.items() if not (root / f).exists() or (root / f).read_text(encoding='utf-8') != t]
    if bad:
        print('Out of date:', ', '.join(bad), '→ run python3 -I scripts/build_web.py'); sys.exit(1)
    print('index.html, sw.js and manifest are up to date')
else:
    for f, t in out.items():
        (root / f).write_text(t, encoding='utf-8')
    print('index.html', len(h) // 1024, 'kB; sw.js', ver)
