#!/usr/bin/env python3
"""Sync between devices through a FAKE GitHub (no real network). Each device = its own browser context (own localStorage).
Real time (no fake clock), so "last changed wins" is tested with real, different times.
Checks: first device (new code), next devices (code by its first 4 letters, wrong code, public repository, bad token),
encryption (only ciphertext on "GitHub", decrypted here with the same HKDF/AES-GCM), credyd earned AND spent summed over
3 devices (also when changed at the same time), sync again changes nothing and uploads nothing, last changed wins per card
(srs, Mnemo), station part repaired vs stale broken, weak spots removed, cases/souvenirs/shop union, streak, join with own
progress (take / add), new token after 401, damaged data of another device, reset progress turns sync off on that device only,
restore from a backup wins everywhere, upload by itself after a change, footer link, no Czech, no sideways scroll at 375 px,
no script errors, new-version bar (fake GorsafAndroid). Run:  python3 testy/test_sync.py   (needs index.html: build_web.py)"""
import os, sys, asyncio, json, base64, hashlib, gzip, datetime as dt, threading, functools, http.server, re
from playwright.async_api import async_playwright
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
fails = []
def ok(n, c, x=''):
    print(('OK  ' if c else 'FAIL') + ' ' + n + (' | ' + str(x) if x != '' else ''), flush=True)
    if not c: fails.append(n)

class GH:
    """Just enough of the GitHub REST API (as used by sync.js)."""
    REPO = 'tvspk/gorsaf-en-sync'
    def __init__(s):
        s.tokens = {'github_pat_' + 'a' * 30, 'github_pat_' + 'b' * 30, 'github_pat_' + 'c' * 30}
        s.private = True; s.n = 0; s.log = []; s.latest = 'v3.8-en'
        s.contents = {'README.md': b'# sync'}; s.blobs = {}; s.trees = {}; s.commits = {}; s.refs = {'main': 'f' * 40}
    def sha(s, b=b''):
        s.n += 1; return hashlib.sha1(b + str(s.n).encode()).hexdigest()
    async def handle(s, r):
        req = r.request; u = req.url.split('api.github.com', 1)[1]; m = req.method
        H = {'access-control-allow-origin': '*', 'content-type': 'application/json'}
        def J(o, st=200): return r.fulfill(status=st, headers=H, body=json.dumps(o))
        if m == 'OPTIONS': return await r.fulfill(status=204, headers={**H, 'access-control-allow-headers': '*', 'access-control-allow-methods': '*'})
        if u == '/repos/tvspk/gorsaf/releases/latest': return await J({'tag_name': s.latest})
        auth = (await req.all_headers()).get('authorization', '')
        if auth.replace('Bearer ', '') not in s.tokens: return await J({'message': 'Bad credentials'}, 401)
        s.log.append((m, u))
        body = json.loads(req.post_data) if req.post_data else None
        P = '/repos/' + s.REPO
        if u == '/user': return await J({'login': 'tvspk'})
        if u == P: return await J({'full_name': s.REPO, 'private': s.private})
        if not u.startswith(P): return await J({'message': 'Not Found'}, 404)
        u = u[len(P):]
        if u.startswith('/contents/'):
            f = u[len('/contents/'):]
            if m == 'GET': return await (J({'content': base64.b64encode(s.contents[f]).decode()}) if f in s.contents else J({'message': 'Not Found'}, 404))
            if m == 'PUT':
                if f in s.contents: return await J({'message': 'sha wasn’t supplied'}, 422)
                s.contents[f] = base64.b64decode(body['content']); return await J({'content': {}}, 201)
        if u.startswith('/git/matching-refs/heads/'):
            pre = u.split('/heads/', 1)[1]
            return await J([{'ref': 'refs/heads/' + k, 'object': {'sha': v}} for k, v in s.refs.items() if k.startswith(pre)])
        if u.startswith('/git/commits/') and m == 'GET':
            c = s.commits.get(u.split('/')[-1]); return await (J(c) if c else J({'message': 'Not Found'}, 404))
        if u.startswith('/git/trees/') and m == 'GET': return await J({'tree': s.trees[u.split('/')[-1]]})
        if u.startswith('/git/blobs/') and m == 'GET':
            return await r.fulfill(status=200, headers={**H, 'content-type': 'application/octet-stream'}, body=s.blobs[u.split('/')[-1]])
        if u == '/git/blobs' and m == 'POST':
            b = base64.b64decode(body['content']); h = s.sha(b); s.blobs[h] = b; return await J({'sha': h}, 201)
        if u == '/git/trees' and m == 'POST':
            h = s.sha(); s.trees[h] = [{**e, 'type': 'blob'} for e in body['tree']]; return await J({'sha': h}, 201)
        if u == '/git/commits' and m == 'POST':
            h = s.sha(); c = {'sha': h, 'tree': {'sha': body['tree']}, 'parents': body['parents'],
                              'committer': {'date': dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}}
            s.commits[h] = c; return await J(c, 201)
        if u == '/git/refs' and m == 'POST':
            k = body['ref'].replace('refs/heads/', '')
            if k in s.refs: return await J({'message': 'Reference already exists'}, 422)
            s.refs[k] = body['sha']; return await J({}, 201)
        if u.startswith('/git/refs/heads/') and m == 'PATCH':
            k = u.split('/heads/', 1)[1]
            if k not in s.refs: return await J({'message': 'Not Found'}, 422)
            s.refs[k] = body['sha']; return await J({})
        return await J({'message': 'Not Found ' + u}, 404)
    def state_of(s, br, code):
        c = s.commits[s.refs[br]]; e = [x for x in s.trees[c['tree']['sha']] if x['path'] == 'state'][0]; raw = s.blobs[e['sha']]
        key = HKDF(algorithm=hashes.SHA256(), length=32, salt=b'Gorsaf EN sync v1', info=b'state').derive(code.encode())
        return json.loads(gzip.decompress(AESGCM(key).decrypt(raw[:12], raw[12:], b'state')))
    def uploads(s): return sum(1 for m, u in s.log if m == 'POST' and u.endswith('/git/blobs'))

G = GH()
TOK = ['github_pat_' + x * 30 for x in 'abc']

def serve():
    class Q(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a): pass
    h = functools.partial(Q, directory=ROOT)
    srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), h)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return f'http://127.0.0.1:{srv.server_port}/index.html'

async def device(browser, url, name, android=None):
    ctx = await browser.new_context(viewport={'width': 375, 'height': 800}, service_workers='block')
    p = await ctx.new_page(); p.errs = []; p.name = name
    p.on('pageerror', lambda e: p.errs.append(str(e)))
    p.on('console', lambda m: p.errs.append(m.text) if m.type == 'error' and 'Failed to load resource' not in m.text else None)
    await ctx.route('https://api.github.com/**', G.handle)
    if android:
        await ctx.add_init_script("window.GorsafAndroid={version:()=>%s,open:u=>{window.__opened=u},copy:()=>{},paste:()=>'',share:()=>{},bars:()=>{}}" % json.dumps(android))
    await p.goto(url)
    await wait(p, 'ready===true')
    return p

E = lambda p, js: p.evaluate(js)
async def wait(p, js, timeout=15000):
    # polls with evaluate (wait_for_function evaluates a string, which the page's CSP forbids: no 'unsafe-eval')
    t = 0
    while not await p.evaluate(js):
        await asyncio.sleep(0.1); t += 100
        if t > timeout: raise TimeoutError(p.name + ': ' + js)
async def state(p):
    return await E(p, """({cr:S.credits,done:[...S.done].sort(),tr:[...S.trophies].sort(),ow:[...S.owned].sort(),xn:S.exam.n,
      st:S.stats,srs:S.srs,mh:mnS().c,lv:S.lv,br:[...S.broken].sort(),rev:S.review.slice().sort(),sk:S.streak,best:S.best,words:S.words,
      on:!!SY,err:SY&&SY.lastError,dev:SY?Object.keys(SY.dev).length:0})""")

async def open_sync(p):
    await p.evaluate('home()')
    await p.click('#sylink'); await p.wait_for_selector('.card.sync')

async def setup_first(p, tok):
    await open_sync(p); await p.click('#sy-setup')
    await p.fill('#sy-tok', tok); await p.click('text=Connect')
    await p.wait_for_selector('ol.sy-words')
    words = await p.eval_on_selector_all('ol.sy-words li', 'l=>l.map(x=>x.textContent)')
    await p.click('text=I have written them down')
    await wait(p, 'SY&&SY.joined')
    return ' '.join(words)

async def join(p, tok, code, choice=None):
    await open_sync(p); await p.click('#sy-setup')
    await p.fill('#sy-tok', tok); await p.click('text=Connect')
    await p.wait_for_selector('#sy-code'); await p.fill('#sy-code', code); await p.click('#sy-codego')
    if choice:
        await p.wait_for_selector('#sy-' + choice); await p.click('#sy-' + choice)
    await wait(p, 'SY&&SY.joined')

async def sync(p): return await E(p, 'syNow(true)')

async def nosideways(p, what):
    w = await E(p, 'document.documentElement.scrollWidth')
    ok(f'{p.name}: no sideways scroll ({what})', w <= 376, w)

async def main():
    url = serve()
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        A = await device(b, url, 'A')
        ok('footer has the Sync link', await E(A, "!!document.getElementById('sylink')"))
        await open_sync(A); await nosideways(A, 'sync screen')
        txt = await E(A, 'document.body.innerText')
        ok('no Czech on the sync screen', not re.search('[ěščřžůťďň]', txt))
        # progress on A before sync
        ch = await E(A, 'DATA.chapters.map(c=>c.id)'); parts = await E(A, 'DATA.station.map(m=>m.id)'); shop = await E(A, 'DATA.shop.map(i=>i.id)')
        tags = await E(A, 'Object.keys(DATA.tags)')
        await E(A, f"""S.credits=100;S.done.add({json.dumps(ch[0])});S.trophies.add('llun');S.srs['c1:x#1']={{i:2,due:'2030-01-01'}};
          mnS().c['1r']=[100,3,250,2,0];S.lv[{json.dumps(parts[0])}]=1;S.stats[{json.dumps(tags[0])}]={{ok:5,bad:2}};S.exam.n=1;save();mhSave()""")
        # errors while setting up
        await open_sync(A); await A.click('#sy-setup'); await A.fill('#sy-tok', 'github_pat_' + 'x' * 30); await A.click('text=Connect')
        await A.wait_for_selector('#sy-err:not([hidden])'); ok('bad token: message', 'invalid' in await A.inner_text('#sy-err'))
        G.private = False; await A.fill('#sy-tok', TOK[0]); await A.click('text=Connect')
        await wait(A, "document.getElementById('sy-err').textContent.includes('public')"); ok('public repository refused', True)
        G.private = True
        code = await setup_first(A, TOK[0])
        ok('8 words', len(code.split()) == 8, code)
        ok('meta file in main', 'gorsaf-en-sync.json' in G.contents)
        meta = json.loads(G.contents['gorsaf-en-sync.json']); ok('meta: app + check, no code inside', meta['app'] == 'GorsafEN' and code.split()[0] not in json.dumps(meta))
        brA = [k for k in G.refs if k.startswith('ge-')]; ok('A has its branch', len(brA) == 1, brA)
        raw = b''.join(G.blobs.values()); ok('only ciphertext on GitHub', b'credits' not in raw and b'srs' not in raw and b'GorsafEN' not in raw)
        st = G.state_of(brA[0], code); ok('decrypts with the code; own credyd 100', st['app'] == 'GorsafEN' and st['own'].get('cr') == 100, st['own'])
        ok('commit without parents', all(c['parents'] == [] for c in G.commits.values()))
        ok('token/code not in localStorage of the save', TOK[0] not in await E(A, "localStorage.getItem('gorsaf:data/users/local/save')"))
        bk = await E(A, 'encodeSave()'); ok('backup code has no token nor words', TOK[0] not in base64.b64decode(bk.split('.')[2]).decode() and code not in base64.b64decode(bk.split('.')[2]).decode())

        # B: empty device, joins with a wrong code first, then with the first 4 letters of each word
        B = await device(b, url, 'B')
        await open_sync(B); await B.click('#sy-setup'); await B.fill('#sy-tok', TOK[1]); await B.click('text=Connect')
        await B.wait_for_selector('#sy-code'); await B.fill('#sy-code', 'abandon ' * 8); await B.click('#sy-codego')
        await B.wait_for_selector('#sy-err:not([hidden])'); ok('wrong code refused', 'match' in await B.inner_text('#sy-err'))
        short = ' '.join(w[:4] for w in code.split()).upper()
        await B.fill('#sy-code', short); await B.click('#sy-codego'); await wait(B, 'SY&&SY.joined', timeout=15000)
        sb = await state(B)
        ok('B took A’s progress', sb['cr'] == 100 and sb['done'] == [ch[0]] and sb['srs'].get('c1:x#1', {}).get('i') == 2 and sb['mh'].get('1r') == [100, 3, 250, 2, 0], sb)
        ok('B: station part, stats, exam', sb['lv'].get(parts[0]) == 1 and sb['st'].get(tags[0]) == {'ok': 5, 'bad': 2} and sb['xn'] == 1)
        await nosideways(B, 'after join')

        # concurrent: A earns 50, B earns 30 and spends 20 (buys an item), both change the same card; B later
        await E(A, f"S.credits+=50;S.srs['c1:x#1']={{i:3,due:'2031-01-01'}};save()")
        await asyncio.sleep(0.05)
        await E(B, f"S.credits+=30;S.credits-=20;S.owned.add({json.dumps(shop[0])});S.srs['c1:x#1']={{i:0,due:'2026-11-18'}};mnS().c['2r']=[5,1,250,1,0];save();mhSave()")
        for p in (A, B, A): ok(f'{p.name}: sync ok', await sync(p))
        sa, sb = await state(A), await state(B)
        ok('credyd summed (100+50+30-20 = 160) on both', sa['cr'] == sb['cr'] == 160, (sa['cr'], sb['cr']))
        ok('shop item on both', sa['ow'] == sb['ow'] == [shop[0]])
        ok('card changed later on B wins on both', sa['srs']['c1:x#1'] == sb['srs']['c1:x#1'] == {'i': 0, 'due': '2026-11-18'}, sa['srs']['c1:x#1'])
        ok('Mnemo card from B on A', sa['mh'].get('2r') == [5, 1, 250, 1, 0])
        n = G.uploads()
        for p in (A, B, A, B): await sync(p)
        sa2 = await state(A)
        ok('sync again: nothing changes', sa2['cr'] == 160 and sa2['srs'] == sa['srs'])
        ok('sync again: nothing uploaded', G.uploads() == n, (n, G.uploads()))

        # station: A repairs a broken part; B still has it broken from before → A’s later change wins
        await E(A, f"S.broken.add({json.dumps(parts[0])});save()"); await sync(A); await sync(B)
        ok('broken part reached B', parts[0] in (await state(B))['br'])
        await E(A, f"S.broken.delete({json.dumps(parts[0])});S.lv[{json.dumps(parts[0])}]=2;save()"); await sync(A); await sync(B)
        sb = await state(B); ok('repair + upgrade reached B', parts[0] not in sb['br'] and sb['lv'][parts[0]] == 2, sb['lv'])
        # weak spot added on B, removed on A later
        await E(B, f"S.review.push({json.dumps(tags[1])});save()"); await sync(B); await sync(A)
        ok('weak spot reached A', tags[1] in (await state(A))['rev'])
        await E(A, f"S.review=S.review.filter(t=>t!=={json.dumps(tags[1])});save()"); await sync(A); await sync(B)
        ok('weak spot removed everywhere', tags[1] not in (await state(B))['rev'])
        # streak: later watering wins, best = max
        await E(A, "S.streak={n:3,last:'2026-11-16',best:3,d:'2026-11-16',c:3,lost:0};save()")
        await E(B, "S.streak={n:1,last:'2026-11-10',best:7,d:'2026-11-10',c:3,lost:0};save()")
        for p in (A, B, A): await sync(p)
        sk = (await state(B))['sk']; ok('streak: later wins, best is max', sk['n'] == 3 and sk['last'] == '2026-11-16' and sk['best'] == 7, sk)

        # C with its own progress: "Take the progress from my other devices"
        C = await device(b, url, 'C')
        await E(C, f"S.credits=999;S.done.add({json.dumps(ch[1])});save()")
        await join(C, TOK[2], code, 'adopt')
        sc = await state(C); ok('C took (no 999, no own case)', sc['cr'] == 160 and ch[1] not in sc['done'], (sc['cr'], sc['done']))
        await sync(A); ok('A unchanged by C', (await state(A))['cr'] == 160)
        # D with its own progress: "Add this device’s progress"
        D = await device(b, url, 'D')
        await E(D, f"S.credits=40;S.done.add({json.dumps(ch[1])});S.srs['c2:y#1']={{i:1,due:'2027-01-01'}};save()")
        await join(D, TOK[2], code, 'add')
        for p in (A, B, C, D): await sync(p)
        al = [await state(p) for p in (A, B, C, D)]
        ok('D added: credyd 200 on all four', all(s['cr'] == 200 for s in al), [s['cr'] for s in al])
        ok('D added: its case and card everywhere', all(ch[1] in s['done'] and 'c2:y#1' in s['srs'] for s in al))
        ok('paired devices: 4', (await state(A))['dev'] == 3)
        await open_sync(A); ok('screen shows 4 devices', 'Paired devices: 4' in await A.text_content('.card.sync'))

        # sync by itself ~15 s after a change (no button)
        await E(B, "S.credits+=5;save()")
        await A.wait_for_timeout(500)
        await wait(B, 'SY.lastSync>Date.now()-3000&&S.credits===205', timeout=25000)
        await wait(A, 'S.credits===205', timeout=80000)
        ok('upload after a change + A picks it up within a minute', True)

        # back at the desk: upload ~3 s after a change
        await E(B, "home();S.credits+=1;save()"); t0 = await E(B, 'Date.now()')
        await wait(B, f'SY.lastSync>{t0}', 9000); ok('desk: uploaded within ~3 s', (await E(B, 'SY.lastSync')) - t0 < 7000, (await E(B, 'SY.lastSync')) - t0)
        # leaving the app: quick upload (no downloads, no branch list), A gets it
        await sync(A); await sync(B); n0 = len(G.log)
        await E(A, "S.credits+=7;save()")   # A changed: B must not download it while leaving
        await E(B, "S.credits+=3;save();Object.defineProperty(document,'hidden',{configurable:true,get:()=>true});Object.defineProperty(document,'visibilityState',{configurable:true,get:()=>'hidden'});document.dispatchEvent(new Event('visibilitychange'))")
        await wait(B, '!syBusy&&SY.lastSync>Date.now()-4000', 8000)
        log = G.log[n0:]; bl = [x for x in log if x[1].endswith('/blobs') and x[0] == 'POST']
        ok('leaving: uploaded', len(bl) >= 1, log)
        ok('leaving: no downloads, no branch list', not any(m == 'GET' and ('/git/blobs/' in u or 'matching-refs' in u) for m, u in log), log)
        await E(B, "delete document.hidden;delete document.visibilityState")
        await sync(A); await sync(B); sa, sb = await state(A), await state(B)
        ok('after leaving: both 216', sa['cr'] == sb['cr'] == 216, (sa['cr'], sb['cr']))
        # leaving while a sync is still running: it uploads again right after
        await E(B, "S.credits+=2;save();syNow(false);S.credits+=2;save();Object.defineProperty(document,'hidden',{configurable:true,get:()=>true});document.dispatchEvent(new Event('visibilitychange'))")
        await wait(B, '!syBusy&&!syAgain', 8000); await B.wait_for_timeout(1500); await wait(B, '!syBusy', 8000)
        await E(B, "delete document.hidden"); await sync(A)
        ok('leaving during a sync: the last change arrived', (await state(A))['cr'] == 220, (await state(A))['cr'])
        cr_now = 220

        # bad token on A → message on the screen, new token
        G.tokens.discard(TOK[0]); await sync(A)
        await open_sync(A); ok('expired token shown', 'expired' in await A.inner_text('#sy-st'))
        ok('Enter a new token button', await E(A, "!document.getElementById('sy-tok-btn').hidden"))
        ok('footer link warns', '⚠' in await E(A, "home(),document.getElementById('sylink').textContent"))
        G.tokens.add(TOK[0] + 'z'); await open_sync(A); await A.click('#sy-tok-btn'); await A.fill('#sy-tok', TOK[0] + 'z'); await A.click('text=Continue')
        await wait(A, "SY.token.endsWith('z')&&!SY.lastError", timeout=10000); ok('new token works', True)

        # damaged data from another device: the rest syncs
        G.refs['ge-0000000000aa'] = G.refs[brA[0]]   # A’s data under another name: readable → harmless
        bad = G.sha(); G.blobs[bad] = b'\x00' * 40; t = G.sha(); G.trees[t] = [{'path': 'state', 'type': 'blob', 'sha': bad, 'mode': '100644'}]
        cm = G.sha(); G.commits[cm] = {'sha': cm, 'tree': {'sha': t}}; G.refs['ge-0000000000bb'] = cm
        await sync(B); ok('damaged branch: rest synced, message', (await state(B))['err'] == 'damaged' and (await state(B))['cr'] >= 205)
        del G.refs['ge-0000000000bb']; del G.refs['ge-0000000000aa']; await sync(B)

        # restore a backup on A (with sync on): its cards win everywhere
        await E(A, "S.srs['c1:x#1']={i:5,due:'2032-02-02'};save()"); code_bk = await E(A, 'encodeSave()')
        await E(A, "S.srs['c1:x#1']={i:0,due:'2026-11-20'};save()"); await sync(A); await sync(B)
        await E(A, f"(()=>{{const d=decodeSave({json.dumps(code_bk)});applySave(d);save();mhSave()}})()"); await sync(A); await sync(B)
        ok('restored card wins on B', (await state(B))['srs']['c1:x#1'] == {'i': 5, 'due': '2032-02-02'})

        # reset progress on D: only D wiped, sync off there, others keep everything
        cr_before = (await state(A))['cr']
        await E(D, 'home()'); await D.click('text=Reset progress'); await D.click('text=Yes, start again')
        sd = await state(D); ok('reset on D: wiped, sync off', sd['cr'] == 0 and not sd['on'])
        ok('reset note in the footer', 'turned off' in await D.inner_text('.footnote'))
        await sync(A); ok('A keeps its credyd after D’s reset', (await state(A))['cr'] == cr_before)
        # turn off on C
        await open_sync(C); await C.click('#sy-off'); await C.click('#sy-offyes')
        ok('turn off on C', not (await state(C))['on'] and 'off' in await C.inner_text('.card.sync'))

        # pairing code screen + QR (shown on request, hides itself; content = GORSAF: + words)
        await open_sync(A); await A.click('text=Pairing code'); await A.click('text=Show QR code')
        ok('QR shown', await E(A, "!!document.querySelector('.sy-qrimg svg')"))
        ok('QR text', await E(A, "syQrCode('GORSAF:'+SY.code.toUpperCase())===SY.code"))
        ok('foreign QR refused', await E(A, "syQrCode('MEMOCHAT:'+SY.code)===null"))
        await nosideways(A, 'QR')

        # new-version bar (APK only)
        Z = await device(b, url, 'Z', android='3.7-en')
        await Z.wait_for_selector('#upbar', timeout=10000); ok('new version bar', '3.8-en' in await Z.inner_text('#upbar'))
        await Z.click('#up-get'); ok('download opens the release', await E(Z, 'window.__opened') == 'https://github.com/tvspk/gorsaf/releases/latest/download/gorsaf-en.apk')
        G.latest = 'v3.7-en'; await E(Z, "localStorage.removeItem('gorsaf-en-update');upCheck()"); await Z.wait_for_timeout(800)
        ok('same version: no bar', not await E(Z, "!!document.getElementById('upbar')"))
        W = await device(b, url, 'W')
        await W.wait_for_timeout(4500); ok('web (no app): no bar', not await E(W, "!!document.getElementById('upbar')"))

        for p in (A, B, C, D, Z, W):
            ok(f'{p.name}: no script errors', not p.errs, p.errs[:3])
        await b.close()
    print('\n' + ('ALL SYNC TESTS PASSED' if not fails else f'{len(fails)} FAILED: ' + ', '.join(fails)))
    sys.exit(1 if fails else 0)

asyncio.run(main())
