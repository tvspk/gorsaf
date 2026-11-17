#!/usr/bin/env python3
"""Builds the listening page listen/index.html (all clips, play + flag) from the game.
Run after any re-pack:  python3 listen/make_rows.py
Publish listen/index.html as its own artifact with capabilities {db:{}, user:{}} and files audio/<pack>.mp3 -> game/audio-packs/<pack>.mp3
(or copy them server side from the main artifact). Flags land in db collection `flags` (doc id = clip key)."""
import sys, json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'audio')); import make_audio as M
src = M.GAME.read_text(encoding='utf8')
I = json.loads(re.search(r'const AUDIO_INDEX=(\{.*?\});', src).group(1))
rows = [[l['key'], l['text'], str(l['where']), l['unit'], 1 if l.get('card') else 0, l['voice']] + I[l['key']]
        for l in M.lines_for('all') if l['key'] in I]
page = (ROOT / 'listen' / 'zvuky.html').read_text(encoding='utf8')
data = json.dumps(rows, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
(ROOT / 'listen' / 'index.html').write_text(page.replace('__ROWS__', data), encoding='utf8')
print(len(rows), 'clips -> listen/index.html')
