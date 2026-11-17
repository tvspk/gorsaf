#!/usr/bin/env python3
"""English variant of the game: Mnemo Hooks with British-English hooks and an English UI, no Czech.

Usage:  python3 -I mnemo/make_en.py [game.html] [out.html]
        defaults: game/gorsaf-abercastell.html  game-en/gorsaf-abercastell-en.html

The variant is always DERIVED from the main game, never edited by hand: copy the game, put the current
mnemo/mnemo.js + mnemo.css in (inject.py), then replace the Mnemo data with mnemo/decks-en (mnemo_build.py,
which sets DATA.mnemo.lang='en'), then add sync between devices (sync/inject_sync.py: sync.js + qr.js). Re-run it after any change to the game, mnemo.js or decks-en.
Finally it checks that no Czech letters are left anywhere in the variant (outside the Welsh text).
"""
import os, re, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..')
GAME = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'game', 'gorsaf-abercastell.html')
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, 'game-en', 'gorsaf-abercastell-en.html')
CZ = re.compile(r'[ěščřžůťďňĚŠČŘŽŮ]|\b(?:Dobr[éá]|Snadn[éá]|Znovu|Těžk)\w*')
# Czech words in the shared game text that the English app must say in English (exact, each must be found once)
EN_FIX = [('(Dobré or Snadné)', '(Good or Easy)')]   # station part ysgol: the Mnemo buttons are Good / Easy in English


def run(*a):
    r = subprocess.run([sys.executable, '-I', *a], capture_output=True, text=True)
    print(r.stdout.strip())
    if r.returncode or 'Mixed' in r.stderr:
        sys.exit(r.stderr or f'{a[0]} failed')


def main():
    os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True)
    shutil.copyfile(GAME, OUT)
    run(os.path.join(HERE, 'inject.py'), OUT)
    run(os.path.join(HERE, 'mnemo_build.py'), os.path.join(HERE, 'decks-en'), OUT)
    run(os.path.join(ROOT, 'sync', 'inject_sync.py'), OUT)   # sync between devices: English app + web only
    html = open(OUT, encoding='utf-8').read()
    for a, b in EN_FIX:
        if html.count(a) != 1:
            sys.exit(f'EN_FIX: {a!r} found {html.count(a)}x (the game changed: update EN_FIX)')
        html = html.replace(a, b)
    open(OUT, 'w', encoding='utf-8').write(html)
    if "DATA.mnemo={\"lang\":\"en\"" not in html:
        sys.exit('the variant has no English Mnemo data')
    # the Czech half of the string table in mnemo.js is code shared with the original game; the variant never shows it
    i, j = html.index('cs:{kind:'), html.index('\nen:{kind:')
    rest = html[:i] + html[j:]
    bad = [rest[max(0, m.start() - 40):m.end() + 40] for m in CZ.finditer(rest)]
    print(f'{os.path.relpath(OUT)}: Czech letters outside the shared Czech string table: {len(bad)}')
    for ctx in bad[:20]:
        print(f'  ! …{ctx}…')
    if bad:
        sys.exit(1)


if __name__ == '__main__':
    main()
