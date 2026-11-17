#!/usr/bin/env python3
"""Puts sync (sync/sync.js) and the QR library (sync/qr.js) into the ENGLISH game file.

Usage:  python3 -I sync/inject_sync.py game-en/gorsaf-abercastell-en.html
Called by mnemo/make_en.py after the Mnemo data, so game-en is always derived. The Czech game never gets it.
Idempotent: an earlier copy between the markers is replaced.
- qr.js + sync.js go just before the game's last line `home();initStore();` (same <script>, so they can wrap
  save / mhSave / show / home / initStore and use S, store, snapshot …).
- "Reset progress" turns sync off on this device first (syReset), so a wipe never spreads to the other devices.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
LAST = '\nhome();initStore();\n</script>'
RESET_OLD = 'S.reads={};S.mh={c:{}};save();mhSave();'
RESET_NEW = 'S.reads={};S.mh={c:{}};syReset();save();mhSave();'


def main():
    path = sys.argv[1]
    html = open(path, encoding='utf-8').read()
    html = re.sub(r'/\*GSQR-BEGIN\*/.*?/\*GSQR-END\*/\n', '', html, flags=re.S)
    html = re.sub(r'/\*SYNC-BEGIN\*/.*?/\*SYNC-END\*/\n', '', html, flags=re.S)
    qr = open(os.path.join(HERE, 'qr.js'), encoding='utf-8').read().strip()
    sy = open(os.path.join(HERE, 'sync.js'), encoding='utf-8').read().strip()
    assert sy.startswith('/*SYNC-BEGIN*/') and sy.endswith('/*SYNC-END*/')
    if html.count(LAST) != 1:
        sys.exit('inject_sync: the game does not end with "home();initStore();" + </script>')
    block = '/*GSQR-BEGIN*/\n' + qr + '\n/*GSQR-END*/\n' + sy + '\n'
    html = html.replace(LAST, '\n' + block + 'home();initStore();\n</script>')
    if RESET_NEW not in html:
        if html.count(RESET_OLD) != 1:
            sys.exit('inject_sync: "Reset progress" code not found (the game changed: update RESET_OLD)')
        html = html.replace(RESET_OLD, RESET_NEW)
    open(path, 'w', encoding='utf-8').write(html)
    print(f'{os.path.relpath(path)}: sync + QR injected ({len(sy) // 1024} kB + {len(qr) // 1024} kB)')


if __name__ == '__main__':
    main()
