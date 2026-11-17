#!/usr/bin/env python3
"""The APK page (apk/build-en/project/assets/index.html, opened from file:// like the WebView does) with a fake
GorsafAndroid bridge: sync set-up and a sync against the fake GitHub work from the file:// origin, the new-version
bar appears for an older versionName, no script errors.  Run after apk/build_en.sh:  python3 testy/test_apk_page.py"""
import os, sys, asyncio, json
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'test_sync.py'), encoding='utf-8').read().replace('asyncio.run(main())', '')
T = {'__file__': os.path.join(HERE, 'test_sync.py')}; exec(compile(src, 'test_sync', 'exec'), T)
ok, wait, setup_first, TOK, G = T['ok'], T['wait'], T['setup_first'], T['TOK'], T['G']
from playwright.async_api import async_playwright
PAGE = os.path.join(os.path.dirname(HERE), 'apk', 'build-en', 'project', 'assets', 'index.html')

async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        ctx = await b.new_context(viewport={'width': 375, 'height': 800})
        await ctx.route('https://api.github.com/**', G.handle)
        await ctx.add_init_script("window.GorsafAndroid={version:()=>'3.7-en',open:u=>{window.__opened=u},copy:()=>{},paste:()=>'',share:()=>{},bars:()=>{}}")
        p = await ctx.new_page(); p.errs = []; p.name = 'APK'
        p.on('pageerror', lambda e: p.errs.append(str(e)))
        await p.goto('file://' + PAGE); await wait(p, 'ready===true')
        ok('APK page: local storage mode', await p.evaluate('window.GORSAF_LOCAL===true'))
        await p.wait_for_selector('#upbar', timeout=10000); ok('APK page: new version bar', True)
        await p.evaluate('S.credits=12;save()')
        code = await setup_first(p, TOK[0])
        ok('APK page: sync set up from file://', len(code.split()) == 8 and any(k.startswith('ge-') for k in G.refs))
        ok('APK page: audio path is local', await p.evaluate("audUrl(Object.keys(AUDIO_INDEX)[0]).then(u=>u.startsWith('audio/'))"))
        ok('APK page: no script errors', not p.errs, p.errs[:3])
        await b.close()
    print('\n' + ('APK PAGE OK' if not T['fails'] else 'FAILED: ' + ', '.join(T['fails'])))
    sys.exit(1 if T['fails'] else 0)

asyncio.run(main())
