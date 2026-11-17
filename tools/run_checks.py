#!/usr/bin/env python3
"""Automatic checks for a game built on the Gorsaf engine. Run after every unit you add, before publishing.

  pip install playwright --break-system-packages   (Chromium: use the pre-installed one, or `playwright install chromium`)
  python3 tools/run_checks.py game/<game>.html            # data + generators + screens + saves (≈2 min)
  python3 tools/run_checks.py game/<game>.html --play     # + an autoplayer through every case (≈10–25 min)

What it does: serves the file locally (with a stand-in for the claude.ai `db`/`user` store, kept in localStorage), then
 1. integrity.js – every exercise / bank item / tag / example / card / exam / newsletter question; options unique;
    every rush & mutation generator fuzzed 1500×; station work orders ≥3 items; audio index vs. packs.
 2. screens.js   – every side screen (cards of each unit, lost property, all newsletter pieces, exam, trainer, shop,
    backup, restore, maintenance, review, grammar notes) at 320/375/768 px in both looks: script errors, sideways scroll.
 3. saves        – fresh save, reload, corrupted save not overwritten, backup round-trip, tampered code refused,
    HTML in a pasted code not executed.
 4. --play       – autoplay.js plays every case (story → puzzle → rush → station, 25 % wrong answers, buys repairs).
Exit code 1 if anything is wrong. Nothing here edits the game."""
import functools, http.server, json, os, socketserver, sys, tempfile, threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
SHIM = """window.claude={use:async function(n){
 if(n==='user')return{id:async function(){return 'local'}};
 if(n==='db')return{doc:function(p){var k='gorsaf:'+p;return{
  get:async function(){var v=localStorage.getItem(k);return{exists:!!v,data:function(){return v?Object.freeze(JSON.parse(v)):undefined}}},
  set:async function(d){localStorage.setItem(k,JSON.stringify(d))}}}};
 return null}};"""
KEY = 'gorsaf:data/users/local/save'

def serve(html):
    d = tempfile.mkdtemp(); (Path(d) / 'index.html').write_text('<meta charset="utf-8">' + html, encoding='utf8')
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a): pass
    h = functools.partial(Quiet, directory=d)
    srv = socketserver.TCPServer(('127.0.0.1', 0), h); threading.Thread(target=srv.serve_forever, daemon=True).start()
    return f'http://127.0.0.1:{srv.server_address[1]}/index.html'

def page(b, url, w=375, theme=None, pre=''):
    ctx = b.new_context(viewport={'width': w, 'height': 800}); pg = ctx.new_page(); errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.route('**/*', lambda r: r.abort() if 'googleapis' in r.request.url or 'gstatic' in r.request.url else r.continue_())
    pg.add_init_script(SHIM + pre + (f"localStorage.setItem('gorsaf-theme','{theme}');" if theme else ''))
    pg.goto(url); pg.wait_for_timeout(1500); return ctx, pg, errs

def main():
    game = Path(sys.argv[1]); play = '--play' in sys.argv; url = serve(game.read_text(encoding='utf8')); bad = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx, pg, e = page(b, url); r = pg.evaluate((HERE / 'integrity.js').read_text()); ctx.close()
        audio = r['audio']; packs_gaps = {k: v for k, v in r['packs'].items() if v[2]}
        checks = {k: r[k] for k in ['problems', 'gstat', 'wq', 'orderSetShort', 'exBad', 'exNoMark', 'cardDup', 'wbad', 'wdup', 'exm', 'nw', 'st']}
        if r['packs'] and (audio['miss2'] or audio['cmiss'] or audio['nmiss']): checks['audioMissing'] = audio
        if packs_gaps: checks['packGaps'] = packs_gaps
        for k, v in checks.items():
            if v: bad.append(f'integrity {k}: {json.dumps(v, ensure_ascii=False)[:1500]}')
        if e: bad.append(f'integrity page errors: {e[:5]}')
        print('1. integrity:', 'OK' if not [x for x in bad if x.startswith('integrity')] else 'PROBLEMS')
        for theme in ['station', 'rukopis']:
            for w in [320, 375, 768]:
                ctx, pg, e = page(b, url, w, theme); r = pg.evaluate((HERE / 'screens.js').read_text()); ctx.close()
                if r['over'] or r['errs'] or e: bad.append(f'screens {theme} {w}px: overflow {r["over"][:5]} errors {(r["errs"] + e)[:5]}')
        print('2. screens:', 'OK' if not [x for x in bad if x.startswith('screens')] else 'PROBLEMS')
        s = {}
        ctx, pg, e = page(b, url); s['fresh'] = pg.evaluate(f"!!localStorage.getItem('{KEY}')")
        pg.evaluate("S.credits=77;S.done.add(DATA.chapters[0].id);save()"); pg.wait_for_timeout(200); pg.reload(); pg.wait_for_timeout(1500)
        s['persist'] = pg.evaluate("S.credits===77&&S.done.size===1")
        s['backup'] = pg.evaluate("""(()=>{const c=encodeSave(),d=decodeSave(c);delete d.at;return JSON.stringify(d)===JSON.stringify(JSON.parse(JSON.stringify(snapshot())))&&!!decodeSave(c.slice(0,40)+'\\n '+c.slice(40))&&decodeSave(c.slice(0,-8)+'AAAAAAAA')===null})()""")
        pg.evaluate("""(()=>{const d=snapshot();d.at='<img src=x onerror="window.__x=1">';const j=JSON.stringify(d);window.__c=encodeSave().split('.')[0]+'.'+hash(j)+'.'+btoa(unescape(encodeURIComponent(j)))})()""")
        pg.evaluate("restore()"); pg.fill('textarea.code', pg.evaluate("window.__c")); pg.click('text=Check the code'); pg.wait_for_timeout(300)
        s['no_html'] = pg.evaluate("!document.querySelector('.restore img')&&!window.__x"); s['errors'] = e[:]; ctx.close()
        ctx, pg, e = page(b, url, pre=f"localStorage.setItem('{KEY}','{{broken');")
        s['corrupt_kept'] = pg.evaluate(f"localStorage.getItem('{KEY}')==='{{broken'&&!!document.querySelector('h1')"); ctx.close()
        if not all(v for k, v in s.items() if k != 'errors') or s['errors']: bad.append(f'saves: {s}')
        print('3. saves:', 'OK' if not [x for x in bad if x.startswith('saves')] else 'PROBLEMS')
        b.close()
    if play:
        def chunk(rng):
            with sync_playwright() as p:
                b = p.chromium.launch(); ctx, pg, e = page(b, url)
                r = pg.evaluate((HERE / 'autoplay.js').read_text(), list(rng)); b.close(); return r, e
        with sync_playwright() as p:
            b = p.chromium.launch(); ctx, pg, e = page(b, url); n = pg.evaluate("DATA.chapters.length"); b.close()
        parts = [(i, min(n, i + (n + 2) // 3)) for i in range(0, n, (n + 2) // 3)]
        with ThreadPoolExecutor(len(parts)) as ex:
            for (r, e) in ex.map(chunk, parts):
                if r['notOk'] or r['log'] or r['errs'] or e or r['hscroll']: bad.append(f'autoplay: {json.dumps(r, ensure_ascii=False)[:1500]} {e[:5]}')
        print('4. autoplay:', 'OK' if not [x for x in bad if x.startswith('autoplay')] else 'PROBLEMS', f'({n} cases)')
    print('\n'.join(bad) if bad else 'ALL CHECKS PASSED'); sys.exit(1 if bad else 0)

if __name__ == '__main__':
    main()
