# Rules for working on Gorsaf Abercastell (this repository is PUBLIC)

- **HANDOFF.md is the binding description of the project** (read §000 and the section "Sync between devices" first).
  Reply to the user in Czech.
- **No personal data** in the repository: no real names of users, ages, family relations. Never commit a signing key,
  a password, a token, a pairing code or a backup code (`GORSAF1.…`). Keys live in the user's handoff ZIP and in
  GitHub Secrets only (`GORSAF_EN_KEYSTORE` = base64 of `gorsaf-en.jks`, alias `gorsafen`; `GORSAF_EN_KEYSTORE_PASSWORD`).
  Another key = the update does not install and progress on the phone would be lost.
- Sources: `game/gorsaf-abercastell.html` (Czech-Mnemo game, also the base of the English one), `mnemo/`, `sync/`.
  **`game-en/gorsaf-abercastell-en.html` is derived**: after any change run `python3 -I mnemo/make_en.py`, then
  `python3 -I scripts/build_web.py` (index.html, sw.js, manifest for GitHub Pages). The workflow fails when either is stale.
- Sync (`sync/sync.js`, injected only into the English game by `sync/inject_sync.py`): merge rules are in the comment at
  its top and in HANDOFF. New saved field in `S` = decide its rule (counter / union / max / last changed wins per item /
  not synced) and add it to `syCount`/`sySetCount`, `sySets`/`syUnion`, `syItems`/`syNorm`/`syPut`. The progress
  documents and `localStorage['gorsaf-en-sync']` are always written together (`syPersist`). Format in the mailbox has
  `v:1`; raise it on an incompatible change. Texts: `SYT` (English only; the English app must contain no Czech).
- QR pairing: `sync/qr.js` (`window.GSQR`, from MemoChat), QR = `GORSAF:` + 8 words in capitals, no token.
- New English APK: raise `apk/verze-en.txt` ("versionCode versionName", versionCode always +1, name `X.Y-en`), push to
  `main` → Actions builds, checks the certificate (SHA-256 89e9d208…e136c2) and releases `v<versionName>` with
  `gorsaf-en.apk`. The app offers the new version itself (once in 20 h, `releases/latest`).
- Audio for the web and the APK: `audio/<key>.mp3` (4208 clips). The Czech app is built locally only (`apk/build.sh`,
  own key `signing/gorsaf.jks`), never by this workflow.
- Tests: `python3 tools/run_checks.py game-en/gorsaf-abercastell-en.html`, `python3 testy/test_sync.py` (fake GitHub,
  ~2 min), `python3 testy/test_qr.py` (fake camera, needs ffmpeg), `python3 testy/test_apk_page.py` (after build_en.sh).
  Never test against the real GitHub API from the Claude environment.
