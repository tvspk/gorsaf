#!/usr/bin/env python3
"""Mnemo Hooks: turn the Mnemo Welsh project decks (cy-canolradd-NN.json) into game data.

Usage:  python3 mnemo/mnemo_build.py [decks_dir] [game.html]
        defaults: mnemo/decks  game/gorsaf-abercastell.html

Writes one line between the markers /*MNEMO-DATA*/ ... /*MNEMO-DATA-END*/ in the game
(inserted just before END OF CONTENT the first time):  DATA.mnemo={...};
Decks with "vyklad": "en-GB" (mnemo/decks-en, the English variant) get English labels and DATA.mnemo.lang='en',
which switches the Mnemo UI (mnemo.js MN_T) to English. Czech decks give exactly the same output as before (no lang).
Retired cards ("vyrazeno": true) are left out. Card ids never change, so saved progress stays.
Prints problems in the data (missing unit, broken viz_tez links, duplicates).
"""
import json, re, sys, glob, os

HERE = os.path.dirname(os.path.abspath(__file__))
DECKS = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'decks')
GAME = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, '..', 'game', 'gorsaf-abercastell.html')

MUT = {'mekka': 'měkkou', 'nosova': 'nosovou', 'aspirovana': 'aspirovanou'}
# card-back labels per explanation language (the key of each is the deck field it comes from)
LAB = {
    'cs': {'kmen': 'Kmen', 'zensky_tvar': 'Ženský tvar', 'stupnovani': 'Stupňování', 'tvary': 'Tvary', 'mutace': 'Mutace',
           'puvod': 'Původ', 'pozn': 'Pozn.'},
    'en': {'kmen': 'Stem', 'zensky_tvar': 'Feminine form', 'stupnovani': 'Comparison', 'tvary': 'Forms', 'mutace': 'Mutation',
           'puvod': 'Origin', 'pozn': 'Note'},
}
MUT_TXT = {
    'cs': lambda m: 'po tomto slově následuje mutace ' + MUT.get(m, m),
    'en': lambda m: {'mekka': 'soft', 'nosova': 'nasal', 'aspirovana': 'aspirate'}.get(m, m) + ' mutation follows this word',
}
LANG = 'cs'


def kind(c):
    p, x = c.get('slovni_druh'), c.get('extra') or {}
    if p == 'podstatne_jmeno':
        r = x.get('rod')
        return 'b' if r == 'f' else 'g' if r in ('m', 'm/f') else 'n'
    return {'pridavne_jmeno': 'a', 'sloveso': 'v', 'fraze': 'f'}.get(p, 'x')


def extras(c):
    """Lines worth showing on the card back, in the deck's language: [label, text]."""
    x, out, L = c.get('extra') or {}, [], LAB[LANG]
    if x.get('kmen'): out.append([L['kmen'], x['kmen']])
    if x.get('zensky_tvar'): out.append([L['zensky_tvar'], x['zensky_tvar']])
    if x.get('stupnovani'):
        s = x['stupnovani']
        out.append([L['stupnovani'], ', '.join(s) if isinstance(s, list) else ', '.join(f'{k} {v}' for k, v in s.items()) if isinstance(s, dict) else str(s)])
    if x.get('tvary'):
        t = x['tvary']
        out.append([L['tvary'], ', '.join(t) if isinstance(t, list) else ', '.join(f'{v}' for v in t.values()) if isinstance(t, dict) else str(t)])
    if x.get('zpusobuje_mutaci'):
        m = x['zpusobuje_mutaci']
        out.append([L['mutace'], MUT_TXT[LANG](m)])
    if x.get('puvod'): out.append([L['puvod'], x['puvod']])
    if x.get('pozn'): out.append([L['pozn'], x['pozn']])
    return out


def card(c, unit):
    x = c.get('extra') or {}
    n = int(re.search(r'(\d+)$', c['id']).group(1))
    k = {'id': c['id'], 'n': n, 'u': unit, 'w': c['slovo'].strip(), 'cs': c.get('cs', ''), 'k': kind(c)}
    def put(key, val):
        if val not in (None, '', [], {}): k[key] = val
    put('alt', c.get('alternativy'))
    put('en', c.get('en'))
    put('cu', c.get('cs_upresneni'))
    put('g', x.get('rod') if c.get('slovni_druh') == 'podstatne_jmeno' else None)
    put('gp', x.get('rod_pozn'))
    put('pl', x.get('plural'))
    put('t', c.get('tema'))
    put('f', c.get('frekvence'))
    put('ex', c.get('priklad'))
    put('exc', c.get('priklad_cs'))
    put('m', (c.get('mnemo') or '').strip())
    put('fam', c.get('rodina'))
    put('x', extras(c))
    put('vz', c.get('viz_tez'))
    if c.get('overit'): k['ov'] = 1
    sev = (c.get('varianty') or {}).get('sever')
    if sev:
        k['nv'] = {kk: sev[kk] for kk in ('slovo', 'priklad', 'priklad_cs', 'rod', 'plural', 'pozn') if sev.get(kk)}
    return k


def main():
    files = sorted(glob.glob(os.path.join(DECKS, 'cy-canolradd-*.json')))
    if not files:
        sys.exit(f'No decks in {DECKS}')
    global LANG
    decks = [(f, json.load(open(f, encoding='utf-8'))) for f in files]
    langs = {'en' if d.get('vyklad') == 'en-GB' else 'cs' for _, d in decks}
    if len(langs) != 1:
        sys.exit(f'Mixed Czech and English decks in {DECKS}')
    LANG = langs.pop()
    units, seen, probs, n_out, n_ret = {}, {}, [], 0, 0
    for f, d in decks:
        m = re.search(r'Uned\s+(\d+)', d.get('zdroj', ''))
        if not m:
            probs.append(f'{os.path.basename(f)}: no "Uned N" in zdroj'); continue
        u = int(m.group(1))
        for c in d.get('karty', []):
            if c.get('vyrazeno'):
                n_ret += 1; continue
            if c['id'] in seen:
                probs.append(f'duplicate id {c["id"]} ({seen[c["id"]]} and {os.path.basename(f)})'); continue
            seen[c['id']] = os.path.basename(f)
            units.setdefault(u, []).append(card(c, u)); n_out += 1
    ids = {k['id'] for L in units.values() for k in L}
    for L in units.values():
        for k in L:
            if k.get('vz') and k['vz'] not in ids:
                probs.append(f'{k["id"]}: viz_tez {k["vz"]} not found'); del k['vz']
    data = {'units': {str(u): units[u] for u in sorted(units)}}
    if LANG != 'cs':
        data = {'lang': LANG, **data}
    js = 'DATA.mnemo=' + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + ';'
    js = js.replace('</', '<\\/')
    html = open(GAME, encoding='utf-8').read()
    block = '/*MNEMO-DATA*/' + js + '/*MNEMO-DATA-END*/'
    if '/*MNEMO-DATA*/' in html:
        html = re.sub(r'/\*MNEMO-DATA\*/.*?/\*MNEMO-DATA-END\*/', lambda _: block, html, flags=re.S)
    else:
        mark = '/* ============================ END OF CONTENT'
        i = html.index(mark)
        html = html[:i] + block + '\n' + html[i:]
    open(GAME, 'w', encoding='utf-8').write(html)
    print(f'{len(files)} decks ({LANG}), {n_out} cards in {len(units)} units ({n_ret} retired left out), {len(js)//1024} KB')
    for p in probs:
        print('  !', p)


if __name__ == '__main__':
    main()
