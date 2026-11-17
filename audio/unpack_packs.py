#!/usr/bin/env python3
"""Rebuilds the loose clips game/audio/<key>.mp3 from the packs game/audio-packs/{u,k,m}<N>.mp3 using AUDIO_INDEX in the game.
The packs are the files published with the main artifact (audio/u1.mp3 … audio/k20.mp3, audio/m1.mp3 … audio/m20.mp3): download them into game/audio-packs/
(e.g. Claude: Artifact read with path "audio/u1.mp3" …), then run:  python3 audio/unpack_packs.py
Needed for the APK (apk/build.sh copies game/audio/) and before re-recording (make_audio.py only records missing clips)."""
import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
src = (ROOT / 'game' / 'gorsaf-abercastell.html').read_text(encoding='utf8')
index = json.loads(re.search(r'const AUDIO_INDEX=(\{.*?\});const AUDIO_HAVE', src, re.S).group(1))
out = ROOT / 'game' / 'audio'; out.mkdir(exist_ok=True); packs = {}; n = 0
for key, (pack, off, ln) in index.items():
    if pack not in packs:
        packs[pack] = (ROOT / 'game' / 'audio-packs' / f'{pack}.mp3').read_bytes()
    (out / f'{key}.mp3').write_bytes(packs[pack][off:off + ln]); n += 1
print(f'{n} clips written to game/audio from {len(packs)} packs')
