#!/usr/bin/env python3
"""Records the Welsh lines of Gorsaf Abercastell with Piper and registers them in the game.

Usage:   python3 audio/make_audio.py 1            # Uned 1
         python3 audio/make_audio.py 1 2 3        # several units
         python3 audio/make_audio.py all [--prune]   # --prune deletes clips no longer used
Needs:   pip install piper-tts techiaith-g2p onnxruntime numpy ; node ; ffmpeg
         The voice model in audio/voices/ (see audio/README.md for where to get it).

What gets recorded is decided by the game itself: the /*AUDIO-BEGIN*/ block (audioLines) is run in Node,
so file names always match what the game asks for. Existing MP3s are kept; only missing ones are made.
At the end the list of available clips is written into the game (/*AUDIO-HAVE*/ line), so the 🔊 button
only appears where a recording exists.
"""
import json, os, re, subprocess, sys, tempfile, wave
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GAME = ROOT / 'game' / 'gorsaf-abercastell.html'
OUT = ROOT / 'game' / 'audio'
PACKS = ROOT / 'game' / 'audio-packs'
VOICES = ROOT / 'audio' / 'voices'
MODEL = 'cy_GB-bu_tts-medium'                 # Piper, eSpeak pronunciation (has the only southern MALE voice)
CYEN = 'cy_en_GB-bu_tts-bangor-medium'        # Piper CY-EN, Bangor pronouncing dictionary (better Welsh)
# voice names used in the game -> (engine, speaker)
CYEN_SPK = {'cyen-benyw-de': 0, 'cyen-benyw-gogledd': 1, 'cyen-gwryw-gogledd': 2}
GAP = 0.5      # seconds of silence between the two parts of a card headword (bare form … form with the article)
FORCE_CY = {'dawn', 'man'}   # single-word cards the G2P would otherwise read as English (talent, place)
SPEED = 1.08   # >1 = slower; learners like it a touch slower than native pace

NODE = r'''
const fs=require('fs'),vm=require('vm');const src=fs.readFileSync(process.argv[1],'utf8');
const data=src.slice(src.indexOf('const DATA = {'),src.indexOf('/* ============================ END OF CONTENT'));
const aud=src.slice(src.indexOf('/*AUDIO-BEGIN*/'),src.indexOf('/*AUDIO-END*/'));
const ctx={};vm.createContext(ctx);vm.runInContext(data+aud+';this.DATA=DATA;this.audioLines=audioLines;this.audioNewsLines=audioNewsLines;this.cardsOf=cardsOf;this.audioCardLines=audioCardLines;this.audioMnemoLines=audioMnemoLines;',ctx);
const want=process.argv[2]==='all'?null:process.argv[2].split(',').map(Number);
const out=[];for(const ch of ctx.DATA.chapters){if(want&&!want.includes(ch.unit))continue;
  for(const ex of [...(ch.story||[]),...(ch.puzzle||[])]){const L=ctx.audioLines(ex);for(const k in L)out.push({...L[k],where:ch.id,unit:ch.unit})}}
for(const u in (ctx.DATA.news||{})){if(want&&!want.includes(+u))continue;
  for(const a of ctx.DATA.news[u])for(const l of ctx.audioNewsLines(a))if(l)out.push({...l,where:a.id,unit:+u})}
// flashcards (words, phrases, example sentences) go to their own packs k<N>, fetched only when the card drawer plays one
for(const u in ctx.DATA.words){if(want&&!want.includes(+u))continue;
  for(const c of ctx.cardsOf(+u)){const ex=ctx.DATA.examples[c.key],L=ctx.audioCardLines(c,ex&&ex[0]);for(const k of ['word','ex'])if(L[k])out.push({...L[k],where:c.key,unit:+u,card:1})}}
// Mnemo Hooks cards (headword + example) go to packs m<N>; a text that already has a clip elsewhere keeps it
const MN=(ctx.DATA.mnemo&&ctx.DATA.mnemo.units)||{};
for(const u in MN){if(want&&!want.includes(+u))continue;
  for(const k of MN[u]){const L=ctx.audioMnemoLines(k);for(const x of ['word','ex','nword','nex'])if(L[x])out.push({...L[x],where:k.id.replace('cy-canolradd-','mn'),unit:+u,card:2})}}
console.log(JSON.stringify(out));
'''


class Cyen:
    """Piper CY-EN voice driven by the Bangor G2P (pip install techiaith-g2p onnxruntime numpy)."""
    def __init__(self):
        import json as _j, onnxruntime as ort
        from techiaith.g2p import BangorG2P
        onnx = next(VOICES.rglob(CYEN + '.onnx'))
        cfg = _j.load(open(str(onnx) + '.json'))
        self.g = BangorG2P(english_mode=cfg['phonemizer']['english_mode'])
        if self.g.data_version() != cfg['phonemizer']['data_version']:
            sys.exit(f"techiaith-g2p data_version {self.g.data_version()} != model {cfg['phonemizer']['data_version']}: install the matching techiaith-g2p")
        self.sess = ort.InferenceSession(str(onnx), providers=['CPUExecutionProvider'])
        self.sr = cfg['audio']['sample_rate']

    def synth(self, text, sid):
        import numpy as np
        ids = np.array([self.g.text_to_ids(text, lang='cy' if text.strip().lower() in FORCE_CY else None)], dtype=np.int64)
        return self.sess.run(None, {'input': ids, 'input_lengths': np.array([ids.shape[1]], dtype=np.int64),
                                    'scales': np.array([0.667, SPEED, 0.8], dtype=np.float32),
                                    'sid': np.array([sid], dtype=np.int64)})[0].squeeze()

    def wav(self, text, sid, path, parts=None):
        import numpy as np
        if parts:   # each part synthesised alone, its own silence trimmed, joined by exactly GAP seconds
            segs = []
            for t in parts:
                x = self.synth(t, sid); m = float(np.abs(x).max()) or 1e-6; on = np.where(np.abs(x) > 0.02 * m)[0]
                segs.append(x[on[0]:on[-1] + 1] / m if len(on) else x)
            gap = np.zeros(int(GAP * self.sr), dtype=np.float32); a = segs[0]
            for x in segs[1:]:
                a = np.concatenate([a, gap, x])
        else:
            a = self.synth(text, sid)
        a = (a / max(1e-6, float(np.abs(a).max())) * 0.9 * 32767).astype(np.int16)
        with wave.open(path, 'wb') as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(self.sr); w.writeframes(a.tobytes())


def lines_for(units):
    r = subprocess.run(['node', '-e', NODE, str(GAME), units], capture_output=True, text=True, check=True)
    seen, out = {}, []
    for l in json.loads(r.stdout):
        if l['key'] not in seen:
            l['pack'] = (l.get('card') or 0, l['unit']); seen[l['key']] = l; out.append(l)
        else:   # a clip used in several places goes to u, then k, then m packs, then the lowest unit
            seen[l['key']]['pack'] = min(seen[l['key']]['pack'], (l.get('card') or 0, l['unit']))
    return out


def main():
    args = sys.argv[1:] or ['1']
    prune = '--prune' in args
    args = [a for a in args if a != '--prune']
    if prune and args != ['all']:
        sys.exit('--prune only together with: all')
    units = 'all' if args == ['all'] else ','.join(args)
    todo = lines_for(units)
    OUT.mkdir(parents=True, exist_ok=True)
    piper_voice = cyen = None
    made = 0
    for l in todo:
        mp3 = OUT / (l['key'] + '.mp3')
        if mp3.exists():
            continue
        with tempfile.NamedTemporaryFile(suffix='.wav') as tmp:
            if l['voice'] in CYEN_SPK:
                cyen = cyen or Cyen()
                cyen.wav(l['text'], CYEN_SPK[l['voice']], tmp.name, l.get('parts'))
            else:
                if piper_voice is None:
                    from piper import PiperVoice
                    onnx = next(VOICES.rglob(MODEL + '.onnx'))
                    piper_voice = PiperVoice.load(onnx, config_path=str(onnx) + '.json')
                from piper import SynthesisConfig
                cfg = SynthesisConfig(speaker_id=piper_voice.config.speaker_id_map[l['voice']], length_scale=SPEED)
                with wave.open(tmp.name, 'wb') as w:
                    piper_voice.synthesize_wav(l['text'], w, syn_config=cfg)
            # mono MP3, quiet lead-in trimmed, plays everywhere (Android WebView, iOS, desktop)
            subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', tmp.name,
                            '-af', 'silenceremove=start_periods=1:start_threshold=-50dB,apad=pad_dur=0.15',
                            '-ac', '1', '-b:a', '48k', str(mp3)], check=True)
        made += 1
        print(f"{l['where']:12} {l['voice']:16} {l['text']}")
    if prune:   # drop clips the game no longer asks for (only safe with 'all')
        need = {l['key'] for l in todo}
        for p in OUT.glob('*.mp3'):
            if p.stem not in need:
                p.unlink(); print('removed', p.name)
    # packs for the artifact: game/audio-packs/u<N>.mp3 (cases + newsletter), k<N>.mp3 (flashcards) and m<N>.mp3 (Mnemo Hooks) = MP3s concatenated; the game gets
    # AUDIO_INDEX = {key: [unit, offset, length]} (loose MP3s in game/audio stay for the APK)
    allines = todo if units == 'all' else lines_for('all')
    # safety: the packs are rebuilt from the loose clips, so every clip already in the game must be here first
    old = json.loads(re.search(r'const AUDIO_INDEX=(\{.*?\});', GAME.read_text(encoding='utf8'), re.S).group(1))
    lost = [k for k in old if k in {l['key'] for l in allines} and not (OUT / (k + '.mp3')).exists()]
    if lost:
        sys.exit(f'{len(lost)} recorded clips are missing from game/audio (e.g. {lost[0]}). Run python3 audio/unpack_packs.py first; nothing was changed.')
    PACKS.mkdir(parents=True, exist_ok=True)
    for p in PACKS.glob('[ukm]*.mp3'):
        p.unlink()
    index, packs = {}, {}
    for l in sorted(allines, key=lambda l: (l['pack'], l['key'])):
        mp3 = OUT / (l['key'] + '.mp3')
        if mp3.exists():
            name = 'ukm'[l['pack'][0]] + str(l['pack'][1])
            buf = packs.setdefault(name, bytearray())
            index[l['key']] = [name, len(buf), mp3.stat().st_size]
            buf += mp3.read_bytes()
    for u, buf in packs.items():
        (PACKS / f'{u}.mp3').write_bytes(bytes(buf))
    src = GAME.read_text(encoding='utf8')
    src = re.sub(r'/\*AUDIO-HAVE\*/.*?/\*AUDIO-HAVE-END\*/', lambda m:
                 '/*AUDIO-HAVE*/const AUDIO_INDEX=' + json.dumps(index, separators=(',', ':')) +
                 ';const AUDIO_HAVE=new Set(Object.keys(AUDIO_INDEX));/*AUDIO-HAVE-END*/', src, flags=re.S)
    GAME.write_text(src, encoding='utf8')
    size = sum(len(b) for b in packs.values())
    print(f'\n{made} new, {len(todo)} needed for units {units}; {len(index)} clips in {len(packs)} packs ({size/1048576:.1f} MB)')


if __name__ == '__main__':
    main()
