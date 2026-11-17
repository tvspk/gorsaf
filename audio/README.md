# Audio for Gorsaf Abercastell

Welsh lines are recorded in advance with **Piper** (offline neural TTS) and shipped as MP3 files in `game/audio/`.
The game shows a 🔊 button only where a recording exists, so units without audio keep working as before.

## What is recorded
Decided in the game itself, in the `/*AUDIO-BEGIN*/ … /*AUDIO-END*/` block (`audioLines(ex)`):
- `line`: a character's Welsh line (`ex.cy`), played from the button on the paper slip, in that character's voice;
- `full`: the complete correct Welsh sentence after answering (gap filled with `opts[0]` / `answers[0]`, or the `type`/`build` answer), button "Hear it", narrator voice.
File name = `<voice>-<FNV-1a hash of "voice|text">.mp3`. Change a sentence, and it simply gets a new file on the next run.

## Voices (binding: see HANDOFF.md §6.1)
Only **Piper CY-EN** `cy_en_GB-bu_tts-bangor-medium` (Bangor University, CC BY 4.0, credit shown in the game).
Pronunciation from the Bangor pronouncing dictionary (`techiaith-g2p`, must match the model's `data_version`).
- `cyen-benyw-de` = speaker 0, southern woman: narrator, correct sentences, women.
- `cyen-gwryw-gogledd` = speaker 2, northern man: all men.
- (`cyen-benyw-gogledd` = speaker 1, northern woman: unused.)
Model files go to `audio/voices/cyen/` (download from https://huggingface.co/techiaith/cy_en_GB-bu_tts).
The older `cy_GB-bu_tts` (eSpeak) path in the script is legacy and not used.

## Make / update recordings
```
pip install techiaith-g2p onnxruntime numpy   # + node, ffmpeg
python3 audio/make_audio.py 1          # Uned 1   (or: 2 3 …, or: all)
```
Only missing clips are made; then the list of clips is written into the game (`AUDIO_HAVE`).
Size: about 0.5 MB per unit (MP3 48 kbps mono).

## Publishing
- Artifact: publish the game with `files` = every `game/audio/*.mp3` at path `audio/<name>.mp3`.
- APK: `apk/build.sh` copies `game/audio/` into the app's assets automatically.

## Not verified
The Welsh pronunciation of the synthetic voices has **not** been checked by a native speaker. Mutated forms and names (Treorci, Pontypridd) are the usual weak spots.
