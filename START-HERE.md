# Gorsaf Abercastell: START HERE (for any AI assistant or developer)

State: **26 November 2026**. This file is tool-neutral: it does not assume Claude or any particular AI.
`HANDOFF.md` is the long, binding history and rulebook. Read this file first, then `HANDOFF.md` §000 (English
variant + sync), §2 (the user and the hard rules), §3–§7 (files, code map, audio, publishing).

## 1. What it is
A single-file HTML game for learning Welsh (course *Dysgu Cymraeg Canolradd, South*, units 1–19 + exam unit): cases
on a space station, flashcards with spaced repetition, a mutation trainer, a mock exam, a newsletter, **Mnemo Hooks**
(899 cards with memory hooks) and 4208 recorded Welsh audio clips (Piper CY-EN voice, Bangor University, CC BY 4.0:
the attribution line in the game must stay).

Two apps are built from the same game:

| | Czech-Mnemo app (original) | **English app (active)** |
|---|---|---|
| Source | `game/gorsaf-abercastell.html` (hand-edited) | `game-en/gorsaf-abercastell-en.html` (**derived**, never edit by hand) |
| Mnemo texts | Czech (`mnemo/decks/`) | British English (`mnemo/decks-en/`, from `mnemo/en-src/*.txt`) |
| Android id / label | `cymru.gorsaf.abercastell` / Gorsaf Abercastell | `cymru.gorsaf.abercastell.en` / Gorsaf Abercastell EN |
| Signing key | `apk/signing/gorsaf.jks` | `apk/signing-en/gorsaf-en.jks` (alias `gorsafen`, cert SHA-256 `89e9d208…e136c2`) |
| Last version | 3.4, versionCode 16 (built locally) | **3.13-en, versionCode 10** (GitHub release; next ≥ 11) |
| Sync between devices | no | **yes** (phone, tablet, web) |
| Where it runs | APK; claude.ai artifact | APK + web https://tvspk.github.io/gorsaf/ (+ a claude.ai artifact, without sync) |

## 1a. Releases since 17 Nov 2026 (all English app, all in the shared game file)
- **3.11-en (vc 8):** app version on the last line of the desk footnote (`#appver`; APK from `GorsafAndroid.version()`,
  web from `window.GORSAF_WEB_VER`, written by `build_web.py` from `apk/verze-en.txt`).
- **3.12-en (vc 9):** Lost property plays a short Web Audio chime (right) / thud (wrong), `sfx(ok)` in the game file.
- **3.13-en (vc 10):** "Voice speed" button in the desk footnote (1 → 0.9 → 0.8 → 0.7), per device in
  `localStorage['gorsaf-voice-rate']`, not synced, applied in `audPlay` to every Welsh recording.
- The Czech app (3.4) and its claude.ai artifact do NOT have 3.12/3.13 yet: they get them with the next local Czech build.
Details: HANDOFF §000 (end of the section).

## 2. Where everything is
- **Code repository (public):** https://github.com/tvspk/gorsaf . Everything in this ZIP except the keys, the notes for
  the user and the audio clips (the repository has the clips as `audio/<key>.mp3`). Push to `main` → GitHub Actions
  (`.github/workflows/apk.yml`) checks, builds the English APK and, when `apk/verze-en.txt` has a new version, publishes
  release `v<versionName>` with `gorsaf-en.apk`. GitHub Pages serves the repository root (`index.html`).
- **Sync mailbox (private):** `tvspk/gorsaf-en-sync`. Holds only encrypted data. Never needed for development; never
  write to it by hand.
- **GitHub Secrets** of `tvspk/gorsaf`: `GORSAF_EN_KEYSTORE` (base64 of `gorsaf-en.jks`), `GORSAF_EN_KEYSTORE_PASSWORD`.
- **Keys in this ZIP:** `apk/signing/` (Czech app) and `apk/signing-en/` (English app), each with `KEYSTORE.txt`
  (password). Losing a key = that app can never be updated in place again (users would have to uninstall and lose
  progress). Never put them in the repository or send them anywhere.
- **NOT in this ZIP and never needed by a developer:** the user's GitHub token for sync and the 8-word pairing code
  (they stay in the user's password manager), backup codes `GORSAF1.…` (the user's progress).
- **Audio packs:** `gorsaf-audio-1.zip` (u1–u20: cases + newsletter), `-2.zip` (k1–k20: flashcards), `-3.zip`
  (m1–m20: Mnemo), 60 packs. Unzip into `game/audio-packs/`, run `python3 audio/unpack_packs.py` → 4208 loose clips in
  `game/audio/` (identical to `audio/*.mp3` in the repository). New recordings need the voice model (see HANDOFF §6.3).

- **Vocabulary source (the 899 Mnemo cards):** made in a separate claude.ai project (Czech, data only, no code).
  Its rules, textbook map and north/south table are copied to `docs/slovicka/` (see its README). The decks themselves
  live here: `mnemo/decks/` (Czech, source of truth) and `mnemo/decks-en/` (English, from `mnemo/en-src/`).
- **Handover ZIP from 17 Nov 2026 (`gorsaf-handoff-en-10.zip`) is still the one that carries the keys;** the keys have not
  changed since. Everything else in it is older than this repository: take code and docs from GitHub.

## 3. Everyday work
```
python3 -I mnemo/make_en.py                 # game + mnemo.js/css + decks-en + sync → game-en (checks: no Czech left)
python3 -I scripts/build_web.py             # game-en → index.html, sw.js, manifest (GitHub Pages)
python3 tools/run_checks.py game-en/gorsaf-abercastell-en.html      # integrity, screens, saves
python3 testy/test_sync.py                  # sync with a fake GitHub, 4 devices (Playwright + cryptography, ~3 min)
python3 testy/test_qr.py                    # QR pairing with a fake camera (needs ffmpeg)
```
New English release: raise `apk/verze-en.txt` (`<versionCode+1> <X.Y-en>`, e.g. `8 3.11-en`), commit, push to `main`.
The installed app offers the update by itself (checks `releases/latest` once in 20 h). Local build instead:
`cd apk && GORSAF_AUDIO_DIR=../game/audio ./build_en.sh <vc> <name>` (JDK 17+, python3, npm; key from `signing-en/`).
Czech app: `cd apk && ./build.sh <vc ≥ 17> <name>` locally only (HANDOFF §7.2); it is not in the workflow.

Any change to the game: edit `game/gorsaf-abercastell.html` (or `mnemo/`, `sync/`), then the three commands above.
The workflow fails if `game-en` or `index.html` is out of date. Saved progress must never be lost: a change of saved
data needs a migration in `applySave()` and a decision how sync merges it (see §4).

## 4. Sync between devices (English app + web)
Code: `sync/sync.js` (logic + English texts), `sync/qr.js` (QR encoder/decoder), `sync/inject_sync.py` (puts both into
game-en and wraps the game's `save`, `mhSave`, `show`, `home`, `initStore`; the Czech game never gets it).
No server: each device talks to `https://api.github.com` with the user's fine-grained token (only the mailbox,
Contents read/write). Each device has its own branch `ge-<12 hex>` with one file `state` = AES-256-GCM(gzip(JSON)),
key = HKDF-SHA-256 of the 8-word code (salt `Gorsaf EN sync v1`). Merge rules (binding, details in HANDOFF §000 "SYNC"):
counters summed through each device's own contribution (credyd can go down), sets united, records = maximum, streak =
later day wins, spaced-repetition items = last changed wins per item. When: start, every minute, 3 s after a change at
the desk, quick upload on leaving the app, button "Sync now". Verified by the user on 3 real devices on 17 Nov 2026.

## 5. Working with the user (important)
- The user is Czech, learns Welsh, is **not a programmer**. Reply in **Czech**, briefly and factually. Steps on GitHub
  or the phone: one at a time, exactly where to click, wait for "hotovo".
- Game UI is English with Welsh exercises. The English app must contain **no Czech** at all.
- Never copy sentences from the course worksheets (Taflen Waith). Textbook examples are fine.
- Always say what you checked and what you could not check (Welsh is not native-checked; phones are not available
  to an AI: ask the user to test).
- Bigger changes: propose options, let the user choose, then implement → test → release.
- The repository is public: no personal data, no keys, tokens, codes.

## 6. Open points (26 Nov 2026)
- The new-version offer inside the app has not been confirmed on a phone yet (it appears within 20 h of a new release;
  3.11-en, 3.12-en and 3.13-en were all released on 26 Nov 2026).
- Welsh "to check" cards (list in HANDOFF §000, EN-8). Any Welsh text change needs new audio.
- Czech app: answer checking of headwords with a bracketed preposition is fixed only in the English app (HANDOFF §000).
