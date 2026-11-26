# Gorsaf Abercastell – HANDOFF (binding)

> **This file is the single binding source of truth.** It replaces every earlier version of HANDOFF.md and any older
> notes. If a chat message, an old prompt or your own idea disagrees with this file, this file wins unless the user
> says otherwise in the current chat. §000 updated 17 Nov 2026 (Chat EN-9: sync between devices, APK 3.8-en vc 5, repo tvspk/gorsaf; Chat EN-8: double review + fixes, APK 3.6-en vc 3, EN artifact; Chat EN-7: review fixes, 187 new hooks, EN icon, APK 3.5-en vc 2; before that Chat EN-6: EN line merged into 3.4, English APK 3.4-en vc 1, new key signing-en). §00 last updated 13 Nov 2026 (Chat E: counts checked, Mnemo audio recorded, packs m1–m20). Rest last updated: 12 Oct 2026 (audio for cases, newsletter and flashcards; card headwords = bare form only; main artifact version 15).

## 000. ENGLISH MNEMO VARIANT: WORK IN PROGRESS (13 Nov 2026), READ THIS FIRST
Goal: a variant of the game/app with **no Czech at all in Mnemo Hooks** (new British-English hooks, English meanings,
example translations and notes) and its own app with a **new signing key + new applicationId** (done, see the end of this section). Czech decks in `mnemo/decks/` stay
untouched (the original app keeps them). Reply in Czech.
- Source per deck: `mnemo/en-src/NN.txt` (format and rules in `mnemo/en-src/STYLE.md`, binding: gender code
  feminine = hot/red, masculine = cold/blue, rotate images). Output: `mnemo/decks-en/cy-canolradd-NN.json`, same schema
  (keys stay, values English; `cs` holds the English meaning, `en` removed, `vyklad:"en-GB"`).
- Workflow per deck: `python3 -I mnemo/extract.py mnemo/decks/cy-canolradd-NN.json` (compact view: id|word|pos/gender|
  en|cs|ex|ex_cs|hook + extras JSON incl. `famN` = family entries with glosses) → write `mnemo/en-src/NN.txt` →
  `python3 -I mnemo/merge_en.py mnemo/decks/cy-canolradd-NN.json mnemo/en-src/NN.txt mnemo/decks-en/cy-canolradd-NN.json`
  (refuses to write if a card/note is missing or Czech remains). Cards with no Czech hook stay without a hook.
- **DONE: decks 01–10 (222 cards). DONE: decks 11–20 (239 cards, ids 0223–0461; Chat EN-2, 13 Nov 2026) → 461 cards
  in `decks-en/`.** merge_en.py OK for every deck; checked: ids, Welsh headwords and Welsh examples identical to the Czech
  decks, hook present exactly where the Czech deck has one. Gender images rotated per deck; deck 20 used (f) embers, red
  bulb, LED in the red, bonfire, strawberry jam, red banners, red cross; (m) ice pack, sleet, sheet of ice, ice palace,
  frozen border, steaming breath, blue balaclava, ice-cold flood, frosty mug, snowflake, avalanche, ice hole, ice rink,
  tundra – avoid these in deck 21. Not native-checked.
  **DONE: decks 21–30 (227 cards, ids 0462–0688; Chat EN-3, 13 Nov 2026) → 688 cards in `decks-en/`.** merge_en.py OK
  for every deck; checked by script against `decks/` (ids, headwords, Welsh examples, northern Welsh examples identical;
  hook exactly where the Czech deck has one). The script also found two OLDER mismatches, left as they are (decide in a
  later chat): 0023 (deck 01) and 0096 (deck 04) have an English hook although the Czech deck has none. Deck 30 used
  (f) treasure chest like hot coals; (m) blue overalls on a frosty morning, date freezing solid; deck 29 used (f) red
  torches, red belt, red bricks, fiery rocket tail, red double-decker, brazier, red marker, red wax seal, red lanterns;
  (m) blue uniform, blue dart, blue scoreboard, frosty hut, icicles, iceberg, blue-stained virus, frosty leather,
  ice-clear line, blue letters, frozen soil, frozen war, freezer sauce, ice cube down the back, ice-cold coins –
  avoid these in deck 31. Not native-checked.
  **DONE: decks 31–40 (211 cards, ids 0689–0899; Chat EN-4, 13 Nov 2026) → ALL 899 cards in `decks-en/` (40 decks).**
  merge_en.py OK for every deck; script check against `decks/`: ids, headwords, part of speech, Welsh examples, northern
  headwords/examples identical, hook exactly where the Czech deck has one (only the two older mismatches 0023, 0096 remain).
  Test build `mnemo_build.py mnemo/decks-en <copy of game>`: 40 decks, 899 cards, 20 units, no warnings (game itself NOT
  changed). Czech "ověřit" notes became "to be checked" (0731, 0808, 0835, 0896). Not native-checked.
  **DONE: engine step (Chat EN-5, 13 Nov 2026).** The English variant is a separate file
  **`game-en/gorsaf-abercastell-en.html`, always DERIVED, never edited by hand:** `python3 -I mnemo/make_en.py` copies
  `game/gorsaf-abercastell.html`, runs `inject.py` (current mnemo.js/css) and `mnemo_build.py mnemo/decks-en`, then fails
  if any Czech letter is left outside the shared Czech string table. Re-run it after ANY change to the game, mnemo.js or
  decks-en.
  - `mnemo.js`: every UI text is in one table `MN_T = {cs:{…}, en:{…}}[MN_LANG]`; `MN_LANG = 'en'` when
    `DATA.mnemo.lang === 'en'`, otherwise Czech. English wording: Again/Hard/Good/Easy, "Practise: N due, N new",
    "Welsh → English", "English → Welsh", "Back to the desk", Hook, Northern variant, "to check" tag (overit) etc.
    The Czech game got the same code re-injected (inject.py) – **its rendering is unchanged** (73 text snapshots of the
    same scripted run, old vs new file: identical, incl. answer checking). Live artifact NOT republished (no need: same
    behaviour; republish only with the next real change). The Czech game file is now 5632 lines (was 5581).
  - `mnemo_build.py`: decks with `vyklad: en-GB` → English labels (Stem, Feminine form, Comparison, Forms, Mutation
    "soft/nasal/aspirate mutation follows this word", Origin, Note) and `DATA.mnemo={"lang":"en",units:…}`. Mixed decks
    refused. Czech decks: output byte-identical to before.
  - Data fix: 0309 `extra.kmen` was still Czech ("nepravidelné (dod)…") – merge_en.py never touched `kmen`. Now option
    `+kmen=` in en-src (used in 15.txt: "irregular (dod): …"), and the Czech-word check also catches nepravideln*/viz.
    All 40 decks re-merged: only that one line changed.
  - Checks: `run_checks.py` on BOTH files: ALL CHECKS PASSED. Scripted run at 375 px on the variant (unit list, all
    words, search, unit/kind/A–Z filters, peek with see-also/extras/northern variant, a 27-answer round with listening,
    recognition, typed production: exact/typo/hint/I don't know/wrong, end screen, SRS saved + reload, 320 px list): no
    script errors, no sideways scroll, no Czech text. Audio: all 899 headwords + examples and all northern word/sentence
    clips found in AUDIO_INDEX in the variant (same Welsh text as the Czech game, so the same 60 packs serve it).
    Not tested on a phone; English UI wording not checked by a native speaker.
  **DONE: merge with 3.4 + APK of the variant (Chat EN-6, 13 Nov 2026). Release: "Gorsaf Abercastell EN" 3.4-en,
  versionCode 1, applicationId `cymru.gorsaf.abercastell.en`.**
  - The English line (Chats EN-1…EN-5) had branched from the 3.3 handoff, parallel to Chat H (3.4). Merged: base = the 3.4
    handoff (game, Czech decks with the new colour hooks, mnemo.css with the 320 px fix, screens.js); taken from the EN line:
    `decks-en/`, `en-src/`, `extract.py`, `merge_en.py`, `make_en.py`, `mnemo_build.py`, multilingual `mnemo.js`, with Chat H's
    Mnemo change ported into it (Yr ysgol pays credyd on a card's first Good/Easy; end screen text `MN_T.paid`: cs "Škola
    vyplatila +N credyd.", en "The school paid out +N credyd."). So the variant = 3.4 (no Y Drôr Cardiau, header "mnemo X%").
  - `game/gorsaf-abercastell.html` (Czech) NOT changed. Checked that re-injecting the new mnemo.js + mnemo_build.py into a copy
    gives byte-identical Mnemo data and identical rendering (17 text snapshots: lists, peeks, a typed round with ysgol payout).
    Re-inject the Czech game only with its next real change.
  - `game-en/gorsaf-abercastell-en.html` rebuilt by `make_en.py` from the 3.4 game: 899 cards, 689 English hooks (687 where the
    Czech deck has one + 0023, 0096, still open), 0 Czech letters. `run_checks.py`: ALL CHECKS PASSED.
  - **APK: `apk/build_en.sh <versionCode> <versionName>`** (e.g. `./build_en.sh 2 3.5-en`). Builds a private project copy in
    `apk/build-en/project/` (manifest: package `cymru.gorsaf.abercastell.en`, label "Gorsaf Abercastell EN", activity fully
    qualified `cymru.gorsaf.abercastell.MainActivity` — the Java code keeps its package), page = web-header + game-en, the same
    4208 clips from `game/audio/`; signs with the **NEW key `apk/signing-en/gorsaf-en.jks`** (PKCS12, RSA 4096, alias
    `gorsafen`, password in `signing-en/KEYSTORE.txt`, cert SHA-256 89e9d208…e136c2). `build.sh`, `project/` and
    `signing/gorsaf.jks` are not touched. Never mix the two keys.
  - Built 3.4-en: 64.6 MB, SHA-256 4d88988aa2a53c814404c4e6e074bbb83fc307311f2d3d999c6d43164ca550c2, apksigner v2+v3 verified,
    aapt2 badging: package cymru.gorsaf.abercastell.en, versionCode 1, label Gorsaf Abercastell EN. Installs NEXT TO the original
    app (own storage). A backup code from the original app can be restored here (same GORSAF1 format, same card numbers).
  - Tested: the app page (build-en/project/assets/index.html, GORSAF_LOCAL) in Chromium 375 px: English home, all-words button,
    Uned 7 list, peek with hook / northern variant, a 10-card round + end screen, SRS saved to localStorage `.../mnemo`,
    ysgol payout, audio key present, no Czech, no errors, no sideways scroll. **Not installed on a real phone.**
  - (superseded: see Chat EN-7), signed with signing-en. Optional later: an artifact of the variant (not asked).
  **DONE: review + fixes (Chat EN-7, 13 Nov 2026). Release: "Gorsaf Abercastell EN" 3.5-en, versionCode 2 (same key
  signing-en, installs over 3.4-en). SHA-256 38352c85f1b36fcf5efc0bb5868c523bf74f54122e1614e19ceb61f972a4a37d.**
  - Review (script pass + all 899 cards read): no Americanisms; mutation notes OK. User decisions, one by one:
    0275 keeps "i Del" (no mutation of the name); 0154 keeps "Rhoia i"; slush puppy stays; 0023/0096 keep their hooks
    ("as many hooks as make sense"); keys STAY in the handoff ZIP (user's choice, B).
  - Fixed in en-src: 0047 hook (gweinydd < gweini, not gwin); 0865 "Foreign news next..."; new hooks 0116, 0117, 0874.
    Typed English → Welsh: identical prompts split + other word accepted: 0466 bwrw "to hit, to strike (also bwrw glaw =
    to rain)", 0862 taro "to hit, to strike (a blow; of a storm)", 0248 artist "artist (in general)", 0496 arlunydd
    "painter (who paints pictures), artist". New en-src option `+alt=` (merge_en.py) adds accepted Welsh answers.
  - 187 NEW hooks for cards that had none (single words / short expressions; whole sentences left without): now 872 of
    899 cards have a hook (27 without: sentences, a few where no sensible hook). Nouns follow the gender colours.
    Lesson references (Lnn) were deliberately NOT added to new hooks (not verified).
  - mnemo.js EN strings only: "Family" → "Related words" (the field also lists topic words; data unchanged),
    intro "Coursebook words, most of them with a memory hook." Czech strings untouched.
  - Icon: `apk/icon-en/res/` (red "EN" badge inside the adaptive safe circle), made by `apk/icon-en/make_icon_en.py`;
    build_en.sh copies it over the original icons in its private project copy. Original app icons unchanged.
  - Checks: re-merge diff only the intended cards; make_en.py 0 Czech letters; run_checks.py ALL CHECKS PASSED;
    app page at 375 px (round, peek, intro, synonyms accepted both ways, no errors, no sideways scroll); APK badging,
    v2+v3 signature, 4208 clips, EN icon inside. **Not tested on a phone. Hooks not checked by a native speaker.**
  - (superseded by Chat EN-8: next English APK ≥ 4.)
  **DONE: double review IT / British English / Welsh + fixes (Chat EN-8, 13 Nov 2026). Release "Gorsaf Abercastell EN"
  3.6-en, versionCode 3 (key signing-en, installs over 3.5-en), SHA-256 b2174a4c04cc78faabda4bf1bee4a61ad152c31d0801ba6b98bfaeabc0f5c55d.
  NEW ARTIFACT of the variant: https://claude.ai/artifact/VvLiuefz5QgFQP91qwDMYx (slug ea3274ed-00fa-41e7-a6f9-a65775b8b74d,
  capabilities {db:{},user:{}}, all 60 packs as audio/<pack>.mp3, index.html = game-en with `<!DOCTYPE html><meta charset="utf-8">`
  prepended and <title>Gorsaf Abercastell EN</title>; publish copy only, source unchanged). Republish there (only changed files).**
  - Two rounds (round 1: all 899 cards read in full; round 2: pattern scans over all cards + all 872 hooks re-read + tests).
  - 50 cards changed in en-src, ONLY English fields (meanings, translations, hooks, notes): no Welsh text changed (script-checked:
    slovo, priklad, alternativy, northern slovo/priklad identical) → no audio affected. Fixes: false etymologies ("From English
    plaid/TURF/PERIL/effect" → "Sounds like / Like"), Americanism SEDAN (0177), non-words/odd English (0121, 0256, 0896),
    "literally:" in brackets (0490, 0833, 0835, 0858), Mam → Mum (0748), River capitalised (0413, 0470), 10 masculine hooks
    without the cold/blue image got one (0097 0173 0514 0601 0603 0608 0775 0776 0778 0878), internal workflow notes removed
    ("approved 12 Nov", "batch 2/3", ".md", "waiting to be approved"), 0057 DERBY → "A DEAR old BIN", 0014 WINO → "the man with
    the WINE from the LOO? NO?" (user decisions). "to check" resolved (new en-src option `+ov=0` in merge_en.py): 0212 (a question
    → wyt ti), 0275 (a = aspirate only → a llwyddiannus), 0411 (stem gwe- as in GPC).
  - mnemo.js: mnJudge accepts a headword without its bracketed preposition ("codi ofn (ar)" ← "codi ofn"; 5 cards were refusing
    the bare verb); EN labels Kind → Type, Order → Sort. **The Czech game still has the old mnJudge (user: fix Czech only with its
    next real change; then re-run inject.py on game/ and rebuild/publish/APK ≥ 17).**
  - build_en.sh: refuses to build if apk/tools (third-party npm jars, apksigner gets the key) differ from the SHA-256 pinned on
    13 Nov 2026.
  - Checks: run_checks ALL PASSED; 375 px: list labels, typed "codi ofn" = Right, no sideways scroll, no errors; APK: v2+v3,
    badging vc 3 / 3.6-en, 4208 clips, new hooks inside. **Not on a phone; not checked by human native speakers.**
  - Open (Welsh, needs coursebook PDF or a native): remaining "to check" cards 0098 0108 0172 0226 0258 0265 0290 0357 0399 0472
    0589 0593 0616 0618 0659 0663 0731 0808 0835 0860 0878 0887 0891 0896. Any Welsh text change needs new audio (voice model, §6.3).
  - (superseded: next English APK ≥ 5.)
  **15 Nov 2026 (Chat EN-8 cont.): APK 3.7-en, versionCode 4 = 3.6-en content with the ORIGINAL icon (no "EN" badge; user's
  choice). build_en.sh no longer copies icon-en/res (line kept as a comment). Label under the icon is still "Gorsaf Abercastell EN".
  SHA-256 da15375736e42828724819481e475050a489135d3f81a65d8772f301f9c0d4cb. Saved whole on the user's computer.**
  - **Next English APK must be versionCode ≥ 11 (3.8-en = vc 5 has sync, 3.9-en = vc 6, 3.10-en = vc 7, 3.11-en = vc 8, 3.12-en = vc 9, 3.13-en = vc 10, see below)**, signed with signing-en.
  **SYNC BETWEEN DEVICES (Chat EN-9, 17 Nov 2026). English app 3.8-en (versionCode 5) + web on GitHub Pages.**
  - User decisions: English app only (Czech game untouched: sync is injected only into game-en); phone + tablet + computer
    (web); PUBLIC code repository `tvspk/gorsaf` (game, decks, audio clips, scripts; no keys, no notes for the user);
    sync on open / on leaving the app (quick) / every minute while open / 3 s after a change at the desk (15 s in a round) + button "Sync now"; no background job.
  - Mailbox = PRIVATE repository `tvspk/gorsaf-en-sync` (fine-grained token, only that repository, Contents read+write).
    Protocol as in MemoChat / Zelvi sudoku (skill "synchronizace-pres-github"): `gorsaf-en-sync.json` in main (app
    `GorsafEN`, encrypted check), one branch per device `ge-<12 hex>`, file `state` = AES-256-GCM(gzip(JSON)), HKDF salt
    `Gorsaf EN sync v1`, 8 BIP39 words (first 4 letters enough), QR `GORSAF:` + words (camera only when scanning).
  - Code: `sync/sync.js` (all logic + English texts SYT + new-version bar), `sync/qr.js` (GSQR, from MemoChat),
    `sync/inject_sync.py` (called by make_en.py; puts both before the game's last line `home();initStore();` and makes
    "Reset progress" turn sync off on that device first). It wraps the game's save / mhSave / show / home / initStore.
    Runs only when `window.GORSAF_LOCAL` (APK, web); in a claude.ai artifact there is no Sync link and nothing runs.
  - **Merge rules (binding):** counters summed via each device's own contribution: credyd (earned AND spent, a contribution
    may be negative), exam.n, stats ok/bad per tag. Union: done cases, trophies, shop items, worn units, word medals (OR),
    newsletter reads (best). Max: rush record, mutation record, exam best, lastBackup. Streak: later `last` wins, best = max.
    Last changed wins PER ITEM (change time noted in save(), GitHub clock + logical clock, never-filled items weight 0):
    srs, tsrs, Mnemo `mh.c`, each station part [level, broken], each weak spot (review). Not synced: decks (deal order),
    look, bonus panel, legacy S.cards. Joining with own progress asks: "Take the progress from my other devices"
    (recommended after a backup restore, else credyd count twice) / "Add this device's progress".
    Reset progress with sync on = wipe here + sync off here. Restore from a backup with sync on = its cards win everywhere
    (cases/souvenirs earned elsewhere stay).
  - APK: build_en.sh adds INTERNET + CAMERA (+ camera feature not required) to the EN manifest only; Java (shared with the
    Czech app's source, harmless there): CameraClient (camera only for our file:// page, Android permission asked when
    scanning), Bridge.version()/open() (only github.com/tvspk/gorsaf/releases/…), JS timers paused 20 s after leaving.
    New-version bar on the desk: once in 20 h `GET /repos/tvspk/gorsaf/releases/latest`, tag `v3.8-en` style.
  - Web: `scripts/build_web.py` → index.html (web-header + game-en + CSP connect-src api.github.com) + sw.js + manifest +
    icons + .nojekyll; clips in `audio/*.mp3` (also used by CI for the APK: GORSAF_AUDIO_DIR=../audio).
  - CI `.github/workflows/apk.yml`: checks no keys/tokens/backup codes, game-en derived + web up to date, builds with the
    key from Secrets (GORSAF_EN_KEYSTORE base64, GORSAF_EN_KEYSTORE_PASSWORD), checks cert 89e9d208…e136c2, releases
    `v<versionName>` from `apk/verze-en.txt` (now `5 3.8-en`).
  - Tests: `testy/test_sync.py` (fake GitHub, 4 devices), `testy/test_qr.py` (fake camera), `testy/test_apk_page.py`;
    run_checks ALL PASSED. **17 Nov 2026: the user installed 3.8-en from the release and paired 3 devices (phone, tablet,
    web) against the real GitHub; Mnemo progress moved between them. Not yet checked: upload when the app is closed right
    after a round.** 
  - **3.9-en (versionCode 6, 17 Nov 2026):** station part `ysgol` in English says "(Good or Easy)" (was Czech "Dobré or
    Snadné"). Fixed only in the derived EN file: `EN_FIX` table in mnemo/make_en.py (Czech game unchanged); the Czech-word
    check there now also catches Dobré/Snadné/Znovu/Těžk….
  - **3.10-en (versionCode 7, 17 Nov 2026):** on a real phone the first close right after a round did not upload (the app
    was most likely stopped before the 5–8 requests ended; nothing lost: it uploads at the next start). Now: upload 3 s after
    a change at the desk (15 s during a round; an earlier deadline is never pushed back; returning to the desk pulls a
    pending upload in), and on leaving the app a QUICK sync (`syLeave` → `syNow(false,true)`: upload only, no downloads,
    no branch list once this device has uploaded: 4 requests); leaving while a sync runs → quick upload right after it.
    MainActivity.onPause calls `syLeave()`. Next English APK ≥ 8.
  - **3.11-en (versionCode 8, 26 Nov 2026):** app version at the bottom of the desk (last line of the footnote,
    `#appver`, `sync.js` `upFoot`). APK: `Version <versionName>` from `GorsafAndroid.version()`; web: `Version <name> (web)`
    from `window.GORSAF_WEB_VER`, written into index.html by `build_web.py` from `apk/verze-en.txt`. Nothing to edit by
    hand on a release: raise verze-en.txt, run build_web.py, push.
  - **3.12-en (versionCode 9, 26 Nov 2026):** Lost property plays a short sound on every answer (user's wish, as Shelf
    Stocking in Moonlight Mart, own sounds): right = two rising sine chime notes (880 → 1318.5 Hz), wrong = a low
    triangle double thud (196 → 147 Hz, sliding down). `sfx(ok)` next to `audStop` in the game file (Web Audio, made on the
    spot, no file, no mute switch), called from `fin` in `step()` only when `phase===4` (Sorting = Lost property); story,
    puzzle, rush, work order and grammar stay silent. In the shared game file, so the Czech game has it too (not rebuilt:
    Czech APK and live artifact unchanged until the next local build).
  - **3.13-en (versionCode 10, 26 Nov 2026):** voice speed for EVERY Welsh recording (user's wish): button
    "Voice speed: 1×" in the desk footnote (`#voicerate`, above the Welsh voices credit) cycles 1 → 0.9 → 0.8 → 0.7.
    Per device in `localStorage['gorsaf-voice-rate']` like the theme (not in S, not synced). Applied in `audPlay` (the one
    shared player for cases, Lost property, cards, news, Mnemo Hooks): playbackRate with preservesPitch. In the shared game
    file (Czech game too, not rebuilt). Next English APK ≥ 11.
## 00. MNEMO HOOKS: WORK IN PROGRESS (13 Nov 2026), READ THIS FIRST
The user is adding a section **Mnemo Hooks** to this game: the 899 Czech mnemonic word cards of the claude.ai project
**"Mnemo Welsh"** (decks `claude/cy-canolradd-01.json` … `-40.json`, made from the same textbook). Reply in Czech.

**User decisions (13 Nov 2026):**
- A Mnemo Hooks drawer **in every unit** (next to Y Drôr Cardiau) + **"Mnemo Hooks · všechna slovíčka"** at the end of the
  unit list (all 899 cards: search Welsh/Czech, filter by unit/topic/kind, sort by unit or A–Z, practise across units).
- It works as **flashcards like the user's Korean app (Gamgol, Mnemo Hooks)**: recognition Welsh → Czech (flip),
  production Czech → Welsh typed (buttons â ê î ô û ŵ ŷ), listening (only where a recording exists), SRS rated
  Znovu/Těžké/Dobré/Snadné. The section is **in Czech** (the hooks only work in Czech); the rest of the game stays English.
- Production check (project rules): exact; alternative (`alternativy`); northern form (accepted, south reminded); missing
  accent (accepted, warned); mutated form (warned, max Těžké); ≤2 letters off (warned, max Těžké); hint = start of the word
  (max Těžké).
- Cards without a hook are shown without one; `overit` cards carry a small "ověřit" tag.
- **Audio: record what is missing at the very end** (task below). **Publishing: not now** (user: "publikace zatím neřešíme").
- The user **cannot download the JSON decks from the project**. So they are read in this order, a few per chat, with
  `Projects project_read` and saved to `mnemo/decks/` unchanged (Write the JSON as it comes). Each chat ends with a fresh ZIP.

**Done (chat of 13 Nov 2026):** code + styles + build script, tested on a 12-card fixture.
- `mnemo/mnemo.js`, `mnemo/mnemo.css`: the section. `python3 mnemo/inject.py` puts them into the game between
  `/*MNEMO-JS*/…/*MNEMO-JS-END*/` (before `const newsAll=`) and `/*MNEMO-CSS*/…` (before `</style>`) and applies 9 small
  hooks into the engine (listed in inject.py `PATCHES`, see "Engine changes" below). Idempotent: edit the .js/.css, re-run.
- `mnemo/mnemo_build.py [decks_dir] [game]`: decks → one line `DATA.mnemo={units:{u:[card…]}}` between
  `/*MNEMO-DATA*/…/*MNEMO-DATA-END*/` (just before END OF CONTENT). Unit = "Uned N" in the deck's `zdroj`. Leaves out
  `vyrazeno`, reports duplicate ids and broken `viz_tez`. Compact card: id, n (number), u, w, cs, k (b f-noun, g m-noun,
  n plural-only, a, v, x other, f phrase), alt, en, cu, g (rod), gp, pl, t, f, ex, exc, m (hook), fam, x ([label,text]
  extras in Czech), vz, ov, nv (northern variant).
- **Right now the game contains the 12-card TEST data** (`mnemo/test-fixture/`, partly invented: card 0071's Czech and
  card 0032). `mnemo/decks/` is empty. The first real build replaces it all. Never ship the fixture.
- Progress: `S.mh.c[key] = [due day (days since 2026-01-01), interval, ease×100, reps, lapses]`, key = card number +
  r/p/l (`"14r"`). Saved in its **own db document `data/users/<id>/mnemo`** (`mhInit`/`mhSave`), so the main save keeps its
  size and shape (no migration needed). The backup code carries it as field `mh`; a code without `mh` leaves Mnemo progress
  alone; Reset wipes it. The APK shim (`apk/web-header.html`) handles any doc path, so the APK needs no change.
- Audio: uses the game's clips where the text matches (`mnLine` = same key as card headwords: southern woman, bare text).
  Many headwords already have a clip; the decks' example sentences mostly do not.
- Tested (Chromium 375 px, both looks, fixture data): drawer in Uned 1, list + filters + search, card details, a round
  (recognition, production with accents, listening), SRS keys written and saved to its own document, reload keeps it,
  backup code round-trip incl. mh, old code without mh keeps Mnemo progress, no horizontal scroll, no script errors.
  `tools/run_checks.py` (copied from the kit): ALL CHECKS PASSED. Not tested on a phone or the published artifact.

**Chat A DONE (13 Nov 2026): decks 01–10 are in `mnemo/decks/`** (written as compact JSON, one card per line, content
identical to the project; all decks `verze` 3). Real build in the game: **222 cards, ids 0001–0222, Uned 1–6**
(per unit 26 / 57 / 40 / 32 / 40 / 27; Uned 6 probably continues in deck 11). The test fixture is gone from the game.
Build warnings expected until later decks are in: 0079 → viz_tez 0427, 0192 → viz_tez 0554. `overit` cards so far:
0098, 0108, 0172, 0212. `run_checks.py`: ALL CHECKS PASSED (41 s). Screenshot at 375 px: "všechna slovíčka" and Uned 6
list OK (colour bars f red / m blue), no sideways scroll, no script errors.

**Chat B DONE (13 Nov 2026): decks 11–20 are in `mnemo/decks/`** (same compact format, content identical to the project;
`verze` 3 except decks 15 and 19 = `verze` 2, as in the project). Real build: **461 cards, ids 0001–0461, Uned 1–11**
(per unit 26 / 57 / 40 / 32 / 40 / 46 / 47 / 41 / 55 / 47 / 30; Uned 11 probably continues in deck 21). 0079 → 0427 now
resolves. Build warnings expected until later decks are in: 0192 → 0554, 0309 → 0539, 0431 → 0617, 0452 → 0823.
`overit` cards so far: 0098, 0108, 0172, 0212, 0226, 0258, 0265, 0275, 0290, 0357, 0399, 0411. `run_checks.py`: ALL CHECKS
PASSED. Screenshots at 375 px: Uned 10 drawer (47 karet) and "všechna slovíčka" filtered to Uned 11 OK (f red / m blue),
no sideways scroll, no script errors.

**Chat C DONE (13 Nov 2026): decks 21–30 are in `mnemo/decks/`** (same compact format, content identical to the project;
`verze` 3 except deck 21 = `verze` 2 and deck 23 = `verze` 4, as in the project). Real build: **688 cards, ids 0001–0688,
Uned 1–15** (per unit 26 / 57 / 40 / 32 / 40 / 46 / 47 / 41 / 55 / 47 / 54 / 63 / 41 / 47 / 52; Uned 15 may continue in
deck 31). 0192 → 0554, 0309 → 0539, 0431 → 0617 now resolve. Build warning expected until deck 31–40 is in: 0452 → 0823.
New `overit` cards: 0472, 0589, 0593, 0616, 0618, 0659, 0663. `run_checks.py`: ALL CHECKS PASSED. Screenshot at 375 px:
Uned 15 drawer (52 karet, card detail open, f red), "všechna slovíčka" filtered to Uned 14 = 47 z 688, no sideways scroll,
no script errors.

**Chat D DONE (13 Nov 2026): decks 31–40 are in `mnemo/decks/`. ALL 40 DECKS ARE IN.** (same compact format, content
identical to the project; `verze` 3 except deck 32 = `verze` 4 and decks 35, 39 = `verze` 2, as in the project). Real
build: **899 cards, ids 0001–0899, Uned 1–20, no build warnings** (all `viz_tez` resolve, incl. 0452 → 0823). Per unit
26 / 57 / 40 / 32 / 40 / 46 / 47 / 41 / 55 / 47 / 54 / 63 / 41 / 47 / 52 / 42 / 38 / 36 / 13 / 82 (Uned 19 has only 13
cards: deck 37; Uned 20 = decks 38–40 incl. the news glossary; check both against the index in Chat E). New `overit`
cards: 0731, 0808, 0835, 0860, 0878, 0887, 0891, 0896 (0860 siom has rod "m/f"). `run_checks.py`: ALL CHECKS PASSED.
Screenshot at 375 px: "všechna slovíčka" = 899 karet, filtered to Arholiad (Uned 20) = 82 z 899 (f red / m blue), no
sideways scroll, no script errors.

**Chat E DONE (13 Nov 2026): counts checked, 320 px test, Mnemo audio recorded.**
- Counts per unit = id ranges in `claude/canolradd-index.md` §7 exactly (all 899, each deck's `zdroj` = its unit, none
  `vyrazeno`); `mnemo_build.py` rebuild byte-identical to the game.
- "všechna slovíčka" at 320 px, both looks: list renders in 0.45 s (300 rows + "zužte výběr"), search, unit/topic/kind
  filters, A–Z sort, 40 details open, one practice round across units with SRS keys saved: no sideways scroll, no errors.
- Audio code: `audioMnemoLine(t,v)` / `audioMnemoLines(k)` in the AUDIO block (word + ex = southern woman; `nv.slovo` +
  `nv.priklad` = northern man `AUDIO_NORTH`, **user decision 13 Nov 2026: northern variants in the northern male voice**).
  `mnemo.js` `mnLine`/`mnAud` use it (🔊 also in the "Severní varianta" box). `make_audio.py` collects them as `card:2` →
  packs **`m1…m20`** (a text already recorded in a u/k pack keeps that clip). `unpack_packs.py` handles u/k/m.
- Model json: the user uploaded the HF *page* (.htm); the JSON was extracted from it (1504 B, data_version
  718542836d1dcbdd). If uploads come as .htm again, do the same (text between `{"dataset"` and the matching `}`).
- Recording DONE: 1078 new clips (895 southern woman, 183 northern man; the first run was cut off after ~10 min,
  the last half-written MP3 deleted, re-run resumed). Now **4208 clips in 60 packs, 59.5 MB**: u1–u20 and k1–k20
  byte-identical to before, new **m1–m20 = 19 MB** (largest m20 1.7 MB). Every Mnemo card has its headword + example
  clip (headwords already in a k pack keep that clip), and all 168 northern variants (16 words + 168 sentences).
  Headwords like "effeithio (ar)" are read with the bracketed preposition. Spot-checked in the log, **not listened to**.
- Tested (Chromium 375 px, packs served as `audio/*.mp3`): Uned 7 card with a northern variant: 4 buttons (word,
  example, northern word, northern sentence) play from k7/m7, no errors, no sideways scroll. `run_checks.py`: ALL CHECKS
  PASSED. Note for local tests: serve the HTML with `charset=utf-8` (the file has no meta charset; the plain Python
  http.server breaks the script; file:// is fine).
- Handover set now: this ZIP + gorsaf-audio-1.zip (u) + gorsaf-audio-2.zip (k) + **gorsaf-audio-3.zip (m1–m20)**.
  Unzip all three into `game/audio-packs/`, then `python3 audio/unpack_packs.py` → 4208 clips.
- Not published (user: publishing later). When publishing: game + only the 20 m packs are new (u/k already live).

**Chat F DONE (13 Nov 2026): PUBLISHED.** New artifact in this account: **https://claude.ai/artifact/AbSoWLbaanut3eBz7yNa51**
(slug 4db16fe3-1da0-44b1-91a1-9f1a6c5a3754, capabilities `{db:{},user:{}}`, all 60 packs u/k/m as `audio/<pack>.mp3`).
GorZWPpARNxXuHBWHmfB7a is not reachable from this account. Two older single-file "Gorsaf Abercastell" artifacts exist here
(QLVjPSsUXzTKHfJtLU2jQf, 251A9YQgzJKEDf7L16dvd6, no audio) and were left untouched; the user moves progress with Back up → Restore.
The published index.html = game file with `<!DOCTYPE html><meta charset="utf-8">` prepended (source file unchanged, so the APK
line order stays). From now on republish to AbSoWLbaanut3eBz7yNa51 (only changed files; packs already there are kept).
**Lost property without typing (user decision 13 Nov 2026: in Lost property the user never types, only chooses):** the old
typed "write it" question (bit 16 = gold) is now a multiple-choice "gold tag": *Which tag is spelled right? <en>* with the right
headword + 3 near-miss spellings from `fakeSpell(cy)` (ll/l, dd/d, ff/f, u/i/y/w, ae/ai, c/ch, n/nn…; never only an accent away,
never another headword (`ALLCY`), fallback `wrongForms`). Checked: all 813 words get 3 distinct distractors. Gold still pays
double (`ex.gold`), dock perk texts say "gold" instead of "typed". Saves unchanged (same bit 16). Mnemo production stays typed.
Tested: a 10-tag round in Uned 7 at 375 px, no text input, no errors; `run_checks.py` ALL CHECKS PASSED. Not tested on the live page / phone.

**Chat G DONE (13 Nov 2026): APK 3.3, versionCode 15** (= live artifact AbSoWLbaanut3eBz7yNa51: Mnemo Hooks + Lost property
without typing). 4208 loose clips in assets, 64.6 MB, SHA-256 f5274d3b8681aa6e…ef3c, signed with `signing/gorsaf.jks` (cert
8bf56480…341b, same as before, installs over 3.2). Sent in 3 parts (`split -n 3 -d`), join on Windows:
`cmd /c copy /b gorsaf-3.3.apk.part00+gorsaf-3.3.apk.part01+gorsaf-3.3.apk.part02 gorsaf-abercastell-3.3.apk`.
Tested: the app page (project/assets/index.html, GORSAF_LOCAL) in Chromium 375 px: 899 Mnemo cards, "všechna slovíčka" opens,
Mnemo progress saved to its own localStorage doc, no errors, no sideways scroll; every AUDIO_INDEX clip exists in assets.
**Not installed on a real phone.** Next APK must be versionCode ≥ 16.
**Full handover set for another account (13 Nov 2026):** this ZIP + gorsaf-audio-1/2/3.zip + the APK parts + ZACNI-TADY.txt.
New account: unzip, put all 60 packs (u1–u20, k1–k20, m1–m20) into `game/audio-packs/`, `python3 audio/unpack_packs.py`
→ 4208 clips; publish as in §0.1 but with all 60 packs (two publish_files calls of ≤64 MiB, then declare `{db:{},user:{}}`;
prepend `<!DOCTYPE html><meta charset="utf-8">` to a publish copy). The Mnemo decks are already in `mnemo/decks/` (no need
for the Mnemo Welsh project unless the decks change).

**Chat H DONE (13 Nov 2026): new hook colours + Y Drôr Cardiau retired. Live = APK 3.4 (versionCode 16).**
- Mnemo Welsh project plan `claude/mnemo-barvy-plan.md` (7 batches, 202 cards, 183 hooks changed, 19 "beze změny"): only
  the field `mnemo` changed. Patched into `mnemo/decks/` (same compact format, `verze` as in the project: 01:5 02:6 04:4
  06:4 08:4 10:5 12:4 14:4 16:6 18:4 20:4 22:4 25:5 27:4 29:5 31:5 33:4 35:3 37:5 38:5 39:3 40:4); rebuild changed exactly 183 `m`.
- **Y Drôr Cardiau removed (user decision 13 Nov 2026: Mnemo Hooks replace it).** Removed: the drawer button in every unit
  and the exam unit, `function cards()`. Changed: header `cards X%` → `mnemo X%` (`cardPct` = share of the unit's Mnemo
  cards at level "umím", interval ≥ 21 days); Adolygu heddiw = grammar only (`dueLists` returns `cs=[]`, `nextDue` reads
  only `S.tsrs`); shop `Yr ysgol` now pays its credyd for a Mnemo card's first Dobré/Snadné, per direction r/p
  (`mnRate` in mnemo.js), Mnemo round end shows "Škola vyplatila +N credyd". **Kept on purpose** (shared with Mnemo / other
  parts, and so progress can come back): `S.cards`, `S.srs` in the save and backup code, `cardsOf`, `cardIndex`,
  `audioCardLines`, `DATA.words/phrases/examples/cardsExtra`, `yForm`, `audCardBtn`, all packs u/k/m (byte-identical).
  **Never run `make_audio.py all --prune`** without first checking every `audioMnemoLines` key stays in `AUDIO_INDEX`
  (899 Mnemo clips are the k-pack card clips). Checked: all Mnemo audio keys in AUDIO_INDEX.
- `tools/screens.js`: the card loop now visits every unit's Mnemo list + a 3-card round. That found an old 320 px overflow
  (Uned 8 title "cyfarwyddiadau" in the Mnemo list): fixed in mnemo.css (`.mhlistc h2{overflow-wrap:anywhere}`).
- `run_checks.py`: ALL CHECKS PASSED. Published to AbSoWLbaanut3eBz7yNa51 (index.html only). APK 3.4 = versionCode 16,
  SHA-256 6c52816d1439cf67…4a32, 64.6 MB, same key 8bf56480…341b, sent in 3 parts. Next APK ≥ 17. Not tried on a phone.

**Next chats (one step per chat; the user attaches only the newest handoff ZIP):**
1. ~~Chat A: decks 01–10~~ (done). ~~Chat B: 11–20~~ (done). ~~Chat C: 21–30~~ (done). ~~Chat D: 31–40~~ (done).
   In each: `python3 mnemo/mnemo_build.py` (first real build removes the fixture), `python3 tools/run_checks.py
   game/gorsaf-abercastell.html` (≈2 min), one screenshot of a Mnemo list, update this §00 (which decks are in), new ZIP
   (without game/audio), short Czech report + the one-line start message for the next chat.
2. ~~Chat E~~ (done, see above). Was: (after D, 899 cards): check counts per unit against `claude/canolradd-index.md` §4/§7, test "all words" with
   899 cards on 320 px (rendering is capped at 300 rows; filters narrow it). Then audio: add a pure
   `audioMnemoLines()` to the AUDIO block (headword + example per card, voice `AUDIO_VOICES.def`, keys exactly as
   `mnLine`), extend `audio/make_audio.py` to collect them into packs `m1…m20`, record only missing clips (§6), voice model
   per §6.3 (HF may be blocked: ask the user to upload the two files). Needs both audio ZIPs. Northern variants: recorded in the northern male voice (user decision).
3. Publishing / APK only when the user asks (then: a new artifact in this account, see §0.1; the old URL in §0 is from
   another account and is not reachable here).

**Engine changes (for the future merge, §9 of the kit):** all in `mnemo/inject.py` PATCHES: Mnemo drawer button in
`drawerBtns`; "all words" button before "Any time" in `home()`; `await mhInit(db,id)` in `initStore2`; `encodeSave` adds
`mh`; `applySave` takes `mh` if present; restore calls `mhSave()` and shows the Mnemo count; Reset wipes `S.mh`; `show()`
closes the Mnemo peek sheet. No change to the main save format.

## 0. STATE AT A GLANCE (read first)
- **17 Nov 2026: START with `START-HERE.md`** (tool-neutral summary). Active line = English app **3.10-en (vc 7)** with sync,
  built and released by GitHub Actions from https://github.com/tvspk/gorsaf ; web https://tvspk.github.io/gorsaf/ . Handover set:
  gorsaf-handoff-en-10.zip (this tree without audio clips, with both keys) + gorsaf-audio-1/2/3.zip + gorsaf-en-3.10-en.apk.
- **Live game now (13 Nov 2026): https://claude.ai/artifact/AbSoWLbaanut3eBz7yNa51 (see §00 Chat F, H). APK 3.4 = versionCode 16 (Chat H); next ≥ 17.**
- **Earlier state (23 Oct 2026):** the user moved to a NEW Claude account; the main game is now a new artifact
  https://claude.ai/artifact/GorZWPpARNxXuHBWHmfB7a (version 10 = old v21 + Welsh date on the home screen + headword 🔊 to the right of the word, see §9). Old account's artifacts (incl. the listening page) are not reachable here.
  **APK 3.3 (versionCode 15, 13 Nov 2026) = AbSoWLbaanut3eBz7yNa51 with Mnemo Hooks; next ≥ 16.** Earlier: **APK 3.2 (versionCode 14, 26 Oct 2026) = artifact v10** (audit of 23 Oct + the two looks, §9) — next APK must be versionCode ≥ 15.
  A kit for NEW games on this engine (other levels) exists: welsh-game-kit.zip (NEW-PROJECT.md, engine, tools/run_checks.py).
  Handover set sent to the user: this ZIP + gorsaf-audio-1.zip (u1–u20) + gorsaf-audio-2.zip (k1–k20) + APK parts.
- Previous state: main artifact version 21, APK **2.8 (versionCode 10, 14 Oct 2026, = artifact v21)** — next APK must be versionCode ≥ 11.
  Hand-picked audio takes and `credyd` after numbers: see §9.

### 0.1 Starting in a NEW Claude account (the user moved here)
You cannot edit the old account's artifacts; you make new ones. Do this once, in order:
1. Unzip the main ZIP so this file is at `<dir>/HANDOFF.md`. Unzip **both** audio ZIPs into `<dir>/game/audio-packs/`
   (40 files `u1…u20.mp3`, `k1…k20.mp3`). Run `python3 audio/unpack_packs.py` → 3130 loose clips in `game/audio/`.
2. Publish the game as a NEW artifact: `file_path game/gorsaf-abercastell.html`, `capabilities {db:{}, user:{}}`,
   `files {"audio/u1.mp3":"game/audio-packs/u1.mp3", … all 40}` (41.5 MB, fits one publish). Write its URL into §7 and §0
   (replace the old main-artifact URL everywhere in this file) and tell the user.
3. The user's progress: they press **Back up** in the old game, copy the code, then **Restore** in the new one. Saved data
   lives in each artifact's own store; nothing moves by itself.
4. Optional: the listening page (`listen/`, see §9 "Listening page"): `python3 listen/make_rows.py`, publish
   `listen/index.html` as its own artifact with `capabilities {db:{}, user:{}}` and the same 40 `files`.
5. APK: `apk/build.sh 15 3.3` needs JDK 17+, python3, npm (tools fetched from npm on first run). The keystore in
   `apk/signing/` is what lets a new APK install over the old one — never regenerate it. The APK is ~45 MB, over the 30 MB
   send limit: split it (`split -n 2 -d x.apk x.apk.part`) and give the user the Windows join command
   `cmd /c copy /b x.apk.part00+x.apk.part01 x.apk`.
6. Voice model (only for NEW recordings): `audio/voices/cyen/cy_en_GB-bu_tts-bangor-medium.onnx` + `.onnx.json` from
   https://huggingface.co/techiaith/cy_en_GB-bu_tts (the user can upload them). `pip install piper-tts techiaith-g2p onnxruntime
   numpy --break-system-packages`; the G2P `data_version` must match the model's json (make_audio checks it).

- Newsletter "Y Papur Bro": **complete** (Uned 1–19 + Rhifyn Arbennig), live in the main game (§8).
- **Swyddog Bowen has been replaced by Swyddog Rhiannon Llwyd, a woman** (user decision, 12 Oct 2026, final): done and
  **published** (main artifact version 12, together with the audio).
- **Audio: DONE for all cases, all newsletter pieces and all flashcards** (words + phrases, nouns with the article as on the
  bare form only, e.g. "glöwr", plus every example sentence): 3130 clips, 41.5 MB, published as 40 packs (main artifact version 15):
  `audio/u<N>.mp3` = cases + newsletter, `audio/k<N>.mp3` = flashcards (fetched only when a card clip is played). Nothing is pending. Possible next steps only if the
  user asks: APK with audio (§7.2), audio for match pairs / `show` slips / flashcards / exam, native-speaker check.

- **Leek streak** (§9, first entry): published, main artifact version 16. **Card sound switch removed** (version 17, see §6.1).

Read the whole file before touching anything. It is written for a Claude who has never seen this project.

---

## 1. What this is, in three sentences
A single-file HTML game that teaches Welsh (course *Dysgu Cymraeg Canolradd, South*, 19 units + exam unit) through
"cases" on a space station. It runs as a claude.ai artifact (progress saved per user) and as an offline Android app
(APK = the same HTML in a WebView). Since Oct 2026 it can also **play recorded Welsh audio** (trial: Uned 1 only).

## 2. The user and how to work with them
- Czech speaker learning Welsh. **Reply in Czech, briefly and factually.**
- Game UI/narration is English with Welsh exercises. Don't change that unless asked.
- Hard rules:
  - **Never reuse sentences or answers from the homework worksheets (Taflen Waith).** Textbook examples are OK. Also avoid duplicating sentences already in the game.
  - **Never lose saved progress.** Any change to saved data needs a migration in `applySave()`. (The audio feature stores nothing.)
  - Always say what you verified and what you didn't. The Welsh text and the synthetic pronunciation are **not native-checked**.
  - For bigger work: propose options, let the user choose, then implement → test → publish.
- The user supplies course PDFs/worksheets again if content work is needed.

## 3. Files in this package
| Path | What it is |
|---|---|
| `game/gorsaf-abercastell.html` | The whole game (one file, ~4000 lines). **Source of truth for the game.** |
| `game/audio/`, `game/audio-packs/` | **Not in the ZIP** (42 MB, over the 30 MB send limit). The 40 packs `u1…u20.mp3` (cases + newsletter) and `k1…k20.mp3` (flashcards) live in the main artifact as `audio/<pack>.mp3`. To work on audio or build the APK: download them into `game/audio-packs/` (Claude: `Artifact read` with `path: "audio/u1.mp3"` etc.), then `python3 audio/unpack_packs.py` recreates the 3130 loose clips in `game/audio/` (verified byte-identical). |
| `audio/unpack_packs.py` | Packs → loose clips, using `AUDIO_INDEX` in the game. |
| `audio/make_audio.py` | Generates the MP3s for chosen units and registers them in the game. |
| `audio/README.md` | Technical details of the audio pipeline. |
| `audio/voices/` | Voice model goes here. **Not in the ZIP** (77 MB); see §6.3 how to get it. |
| `game-en/gorsaf-abercastell-en.html` | English Mnemo variant, DERIVED by `mnemo/make_en.py` (§000), never edit by hand. |
| `apk/build_en.sh`, `apk/signing-en/` | English variant app: build script + its OWN private key (§000). |
| `sync/`, `scripts/build_web.py`, `testy/`, `.github/` | Sync between devices (English app + web), web build, tests, CI (§000 "SYNC"). |
| `apk/` | Android build: `build.sh`, `align.py`, `web-header.html`, `project/` (manifest, Java, icons), `icon/`, `signing/` (**private** keystore + password). |
| `prompts/` | Generic prompt (CS + EN) for building such a game for any language/course. |
| `news/check_news.js` | Checker for the newsletter Y Papur Bro (§8): `node news/check_news.js game/gorsaf-abercastell.html [units]`. |
| `listen/` | Listening page (all clips, play + flag): `zvuky.html` template + `make_rows.py`. |
| `CTI-MNE.txt` | Czech notes for the user. |

## 4. Code map (inside the single HTML file)
- Line 1 `<title>`, line 2 the Google Fonts `<link>` (the APK build relies on this order), then CSS (tokens on `:root`), then one `<script>`.
- `const DATA = {…}` (top of the script) holds **all language content**, separate from logic:
  - `tags` – skill tags `[label, one-sentence rule]`; `unitTags` – tags per unit.
  - `words[unit]` – `[welsh, english, kind, plural]`, kind `b` fem. noun, `g` masc. noun, `a` adj, `v` verb, `x` other. `cardsExtra`, `phrases[unit]` – extra flashcard items.
  - `examples` – flashcard example sentences, key `c<unit>:<word>` / `p<unit>:<phrase>`, word marked as `[[…]]`.
  - `notes[unit]` – grammar notes; `u5…u19` – tables for generated speed-round questions; `bank[tag]` – question pool for review/overtime/inspections.
  - `chapters[]` – cases `{id, unit, opt?, title, blurb, rush:[[generator,weight]], trophy, story[], puzzle[]}`; exercise types `narr`, `mc` (opts[0] is correct), `type` (answers[]), `build` (answer, extra), `match` (pairs). A character's Welsh line is `cy` + speaker `who`.
  - `exam` (mock exam papers), `streak`, `station` (repair parts with 3 tiers), `wearLines`, `shop`.
  - `news[unit]` – newsletter pieces Y Papur Bro (just before `chapters`), see §8.
- Right after `DATA` (after the line `END OF CONTENT`): the **audio block**, see §6.2.
- State `S` + `snapshot()` / `applySave()` (versioned, with migrations: `srsMigrate`, `renameKeys`, worn units…).
- Newsletter: `papurList(u)`, `papur(id)`, `newsSheet`, `newsFull`, `clipEl`, `clipBoard()` (cabin noticeboard, bonus section), gloss bar `glBar`/`glHide`; inserted before `startChapter()`. Saved as `S.reads[id]={best,at}` (in `snapshot()`/`applySave()`, default `{}`).
- Main screens/functions: `home()`, `startChapter()`, `runSeq()`/`step()` (exercise renderer: `doMC`, `doType`, `doBuild` with drag & drop, `doMatch`), `runRush()`, `runStation()`, `drill()`, `cards()`, `revise()` (spaced repetition 1/3/7/14/30/60 days), `treig()` (mutation trainer), `exam()`, `shop()`, `backup()`/`restore()`.
- `GEN` registry of speed-round generators; `TREIG` mutation-trainer triggers.
- Overtime/review only use units with at least one closed case (`studiedUnits()`).

## 5. Adding or changing content
1. Read the textbook chapter and the worksheet (never copy worksheet sentences).
2. Add/modify data in `DATA` only; keep the existing patterns.
3. Check every Welsh sentence (mutations, gender, prepositions), that questions are unambiguous out of context (state tense/form explicitly), and that word lists are complete.
4. **Re-record audio for that unit** (§6.4). Changed sentences get new files automatically; old files can be deleted.
5. Syntax-check the script and play it through with Playwright at 360–390 px width (no console errors, no horizontal scroll).
6. Publish (§7); report briefly in Czech what changed / what was verified.

## 6. Audio (binding decisions + how it works)

### 6.1 Decisions made by the user – do not change without asking
| Who speaks | Voice | Name in code |
|---|---|---|
| Narrator, the **correct sentence after answering**, all **women** (Swyddog Rhiannon Llwyd, Heulwen Haf, Mrs/Ms …, the woman, the hairdresser) | Piper CY-EN, **southern woman** (speaker id 0) | `cyen-benyw-de` |
| All **men** (Mr Hopcyn, Mr Ifan, Mr Puw, Mr Caradog, Y Pennaeth, the vicar, the caretaker, the shopkeeper) | Piper CY-EN, **northern man** (speaker id 2) – chosen for better pronunciation, accepting the northern accent | `cyen-gwryw-gogledd` |
| Anyone else (Sam, documents, "The programme", …) | narrator = southern woman | `cyen-benyw-de` |

- **Only the Piper CY-EN model is used** (`cy_en_GB-bu_tts-bangor-medium`, Bangor University). The older Piper CY model (`cy_GB-bu_tts`, eSpeak pronunciation) was tried and **rejected**; `make_audio.py` still contains code for it, ignore it.
- Speaker ids were identified by voice-similarity measurement (the model's config only says 0/1/2): **0 = southern woman, 1 = northern woman, 2 = northern man.** There is no southern man in this model.
- Audio is **pre-recorded MP3** (48 kbps mono), not generated on the phone. The game only plays files.
- **Licence CC BY 4.0 → attribution is mandatory.** The home screen footnote shows "Welsh voices: Piper CY-EN, Bangor University (Uned Technolegau Iaith), CC BY 4.0." whenever audio exists. Never remove it.
- Status (12 Oct 2026): 3130 clips (cases + newsletter + flashcards), packs u1–u20 + k1–k20, `AUDIO_INDEX` = `{key:[pack,offset,length]}` with pack names like `"u3"` / `"k3"`. Published in the main game (version 15).
- **Card headword audio (user decision, 12 Oct 2026, FINAL, supersedes the two-part "glöwr … y glöwr" tried in version 14):**
  every headword is spoken in its **bare form only** ("arian", never "yr arian"), for nouns too. The form with the article stays
  written on the card back (yForm) and is not spoken. `audioYForm` was removed; make_audio.py still supports two-part lines
  (`parts`, `GAP`) but nothing uses them now.
- **Article rule (yForm on the card back; written only):** the article is
  chosen AFTER the soft mutation (gyrfa → yr yrfa); `YNOMUT = ['gymnasteg','gêm']` never mutate after y (y gymnasteg); w + vowel
  or w + l/r after the mutation takes y (y wên, y wleidyddiaeth). Displayed forms changed by this fix: only gyrfa and gymnasteg.
- **Flashcards (user decisions, 12 Oct 2026):** a small muted 🔊 (no border, ~55 % opacity, bottom-left of the card) only on the side that shows Welsh (front for Cymraeg→English, back for English→Cymraeg) and a smaller one after the example sentence on the back; never tappable on the hidden face; tapping it does not flip the card. No on/off switch: the card buttons are always there (the switch "Sound on cards" existed in versions 13–16 and was removed at the user's request, 12 Oct 2026; the old localStorage key `gorsaf-cardsnd` is simply ignored). Voice: southern woman. Code: `cardsOf`, `audioYForm`, `audioCardLines` (AUDIO block), `audCardBtn`.
- **Swyddog Rhiannon Llwyd is a woman** and replaces Swyddog Bowen everywhere (user decision, 12 Oct 2026, final; this
  supersedes the earlier "Bowen is a man" decision). In text she is "Swyddog Llwyd" / "Llwyd" (full name "Swyddog Rhiannon
  Llwyd" at her first appearance, case Perthnasau). Her name is not mutated in Welsh (as before with Bowen); after a mutating
  word use "Swyddog Llwyd" (s does not mutate). `AUDIO_VOICES` sends `Swyddog Llwyd` to the southern woman. Her three Uned 1
  lines therefore match the existing female clips again (same text + voice = same file name), so no re-recording is needed.

### 6.2 What the player sees and where it is in the code
- 🔊 button on the paper slip of a character's Welsh line (`ex.cy`), in that character's voice.
- **Hear it** button after answering: the full correct Welsh sentence (gap filled with `opts[0]` / `answers[0]`, or the `type`/`build` answer). Same for right and wrong answers.
- A button appears **only if the MP3 exists** (`AUDIO_HAVE`), so missing audio never breaks anything.
- Code:
  - `/*AUDIO-BEGIN*/ … /*AUDIO-END*/` – pure functions, no DOM: `AUDIO_VOICES` (who → voice, regex on the start of `ex.who`), `audioText`, `audioKey`, `audioLines(ex)`. **`make_audio.py` runs exactly this block in Node**, so the game and the generator always agree on which file to play. Change voice rules only here.
  - `/*AUDIO-HAVE*/const AUDIO_HAVE=new Set([...]);/*AUDIO-HAVE-END*/` – list of existing clips. **Written by the script; never edit by hand.**
  - Player: `audBtn()`, `audPlay()`, `audStop()` (before `/* ---------- helpers */`), used in `step()`. CSS class `.aud`.
- File name = `<voice>-<8-hex FNV-1a hash of "voice|text">.mp3`, in `game/audio/`.

### 6.3 Getting the voice model (needed only to record new audio)
- Download both files from https://huggingface.co/techiaith/cy_en_GB-bu_tts : `cy_en_GB-bu_tts-bangor-medium.onnx` and `cy_en_GB-bu_tts-bangor-medium.onnx.json`, and put them in `audio/voices/cyen/`.
- **Claude's cloud sandbox cannot reach huggingface.co** (blocked by policy, don't try to work around it). Ask the user to upload the two files into the chat (they did this before), or work on the user's computer if it is linked.
- Python packages: `pip install techiaith-g2p onnxruntime numpy` (all on PyPI, reachable). Plus `node` and `ffmpeg`.
- `techiaith-g2p` (Bangor pronouncing dictionary) must match the model: the script stops if `data_version` differs from the model's `.onnx.json` (`718542836d1dcbdd` with g2p 1.4.0).

### 6.4 Recording audio for a unit
```
python3 audio/make_audio.py 2          # Uned 2   (several: 2 3 4 ; everything: all)
```
- Records only missing clips, then rewrites `AUDIO_HAVE` in the game. Prints each line with its voice – check it.
- `python3 audio/make_audio.py all --prune` also deletes clips the game no longer uses (only with `all`).
- ~0.5 MB per unit; the full course will be roughly 10 MB.
- Not covered yet (possible next steps, only if the user asks): `match` pairs, `show` slips, flashcards/vocabulary, rush questions, exam, a listening-only mode.

## 7. Publishing
### 7.1 Artifact
- Publish `game/gorsaf-abercastell.html` **with the runtime capabilities `db` and `user`** (progress is stored per user via `window.claude.use('db')` / `use('user')`, doc `data/users/<id>/save`). Without them the game runs but doesn't save.
- **Audio:** the main game is published WITH audio as 20 per-unit packs: `files` = `{"audio/u1.mp3":"game/audio-packs/u1.mp3", …, "audio/u20.mp3":…}`, never loose MP3s. The artifact host refuses `.bin` (not a served type), so packs are `.mp3` (a concatenation of MP3s is itself a valid MP3; the game slices it by `AUDIO_INDEX` offsets). On any later republish the packs already there are kept; send only packs that changed (after re-recording, all packs are rewritten, so send all 20).
- **The user's main game artifact is https://claude.ai/artifact/GorZWPpARNxXuHBWHmfB7a** (capabilities db + user). Version 12 = audio + Rhiannon Llwyd.
- Always republish to the same artifact (keep its URL). The user moves progress between accounts with **Back up → Restore** (code `GORSAF1.<hash>.<base64>`).
- Test copy with audio (old, unmaintained, loose MP3s, still says Llwyd): artifact "Gorsaf Abercastell Sain", https://claude.ai/artifact/QcJ4aJFbEk7CqZwbTuEawk . Ignore it.

### 7.2 Android APK
- `cd apk && ./build.sh <versionCode> <versionName>` – e.g. `./build.sh 6 2.4`. See the release line below; the next versionCode must be higher.
- The script fetches Android tools from npm the first time (`@drxiaozhi/minapk@0.4.0`, `aaptjs3@2.0.2`), builds `project/assets/index.html` from the game + `web-header.html` (offline fonts + a localStorage shim, `window.GORSAF_LOCAL=true`), **copies `game/audio/` into `project/assets/audio/`**, compiles, aligns and signs with `signing/gorsaf.jks`.
- **Always sign with this key**, otherwise the update won't install over the existing app. Keep the key private.
- The app is a WebView (`MainActivity`) with a JS bridge `GorsafAndroid` (copy / paste / share for backup codes). No network access; audio loads from `file:///android_asset/audio/`.
- Last released: **versionCode 14, 3.2** (26 Oct 2026 = artifact v10; 3130 loose MP3s, SHA-256 1b5c13e42ba66910…, key
  8bf56480…341b; sent split in two parts). Before: 3.1 (vc 13, = v8), 3.0 (vc 12), 2.9 (vc 11).
  `web-header.html` now also embeds Libre Baskerville 700 and Source Serif 4 (400/600/400 italic) for the light look;
  `Bridge.bars(light)` → `BarsTask` colours the Android status/navigation bars to match the look (an anonymous inner
  class broke d8: keep Runnables as named classes). Older: **versionCode 6, 2.4** (12 Oct 2026): first APK with audio, 1090 loose MP3s in assets (stored uncompressed), 19.8 MB, signed with `signing/gorsaf.jks` (cert SHA-256 8bf56480…341b). `MainActivity` now sets `setMediaPlaybackRequiresUserGesture(false)` so "Listen to the column" can play sentence after sentence. The next build must use versionCode ≥ 7.
- Not yet verified: the 2.4 APK has not been installed or played on a real phone.

## 8. Planned work: newsletter "Y Papur Bro"
- Specification: `prompts/prompt-zpravodaj-cs.md` (binding for this feature; in Czech). Work in batches as it says.
- Status: **ALL DONE: Uned 1–19 + Rhifyn Arbennig (Uned 20 = Arholiad), published 12 Oct 2026** (main artifact version 10 after proofreading; Uned 1–15 in version 8). Further work only if the user asks (e.g. a human native proofread, audio for the newsletter).
- Decisions made by the user:
  - The sheep is called **Seren**. She is the same sheep that already appears in the game (Mrs Prydderch's letter about the allotment, the daily streak). She follows Mrs Prydderch around, but nobody, Mrs Prydderch included, knows where she came from.
  - Punchlines are approved first (one sentence each, author + genre), then the texts are written. The user likes the dry humour of the rest of the game; a punchline should be absurd logic taken seriously, not wistful.
- Authors and punchlines so far (nobody twice in a row, across units; keep the running jokes consistent):
  - U1a Mr Hopcyn, column "Fy nheulu i": five relatives with fy, all elsewhere; Seren sleeps in his cabin, isn't related (perthyn), so isn't on the form.
  - U1b Sam, interview "Pum munud gyda Heulwen Haf": four tenses; on a free weekend she'd like to go to Wales, where it rains.
  - U2a Mr Ifan, letter "Dw i byth yn cwyno": six complaints; he has sent it tair gwaith this week.
  - U2b Swyddog Llwyd, questionnaire report: everyone answered "Faswn i byth yn llenwi holiadur" on the questionnaire.
  - U3a Mr Puw, TV column: the new series on Sianel yr Orsaf is dull (the only good character is the sheep); he knows, having watched every episode dwywaith. Ms Lewis is his neighbour.
  - U3b Mr Caradog, advice column (chat: Darllenydd / Mr Caradog): Seren ate a Deck 4 reader's parsnips; she is clever, because she has never eaten his leeks.
  - U4a Swyddog Llwyd, safety notice in the short future; emergency on a Sunday → office closed, ring on Monday.
  - U4b Sam, Deck 4 group chat: helpers for Mrs Prydderch's wardrobe each attach a condition; she lifts it, they make the tea. Mr Caradog never goes anywhere without his spade.
  - U5a Mrs Prydderch, travel: a week on Deck 2 with Seren (past -on ni); next year arhoswn ni gartre, Deck 2 is too far.
  - U5b Y Pennaeth, leave FAQ (chat: Cwestiwn / Y Pennaeth): Cewch / Na chewch; may not take the sheep (not related to you); may not talk to the Pennaeth: he'll be on holiday.
  - U6a Mr Hopcyn, notice "Fy mhen-blwydd i": invites all five relatives (ato fe / ati hi / atyn nhw), five refusals; the only guest is Seren, never invited, already resident; she has looked over (edrych drosti) the cake.
  - U6b Ms Lewis, letter: complaint about Mr Puw's barking "blanket", which she asked Mr Puw to look over (edrych drosto fe); he corrected the grammar; still a complaint about him, now with correct mutations.
  - U7a Swyddog Llwyd, election results: five candidates, one vote each (their own); six votes for Seren, all six voters deny it, so on paper chafodd hi mo'r un bleidlais; she chairs the committee (meets in the allotment).
  - U7b Heulwen Haf, correction: denies Tuesday's rain on Deck 3 (welais i mo'r glaw / mohono fe); a pipe broke in Mr Puw's workshop, water came from the ceiling, not the sky, so it was dry. Take a towel.
  - U8a Mr Caradog, allotment diary: Seren finally eats his leeks (newydd…); "Dw i newydd newid fy marn" (callback to U3b). Consistent with the game case Dianc.
  - U8b Y Pennaeth, directions to his moved office (round the roundabout twice, fourth turning); when you arrive he'll have just left (bydda i newydd adael); next directions in the next rhifyn.
  - U9a Ms Lewis, column: persuaded Mr Puw to swap cabins; he's still her only neighbour. **Ms Lewis now lives in Cabin 3-021, Mr Puw in 3-020** (they swapped).
  - U9b Mr Ifan, letter: Sam persuaded him to look after Seren for one night; should-haves; "Hoffwn i fod wedi cwyno. Ond… dw i byth yn cwyno."
  - U10a Mrs Prydderch, craft night report with tag questions: knitted Seren a jumper from Seren's own wool; she looks exactly as before; taswn i wedi meddwl, baswn i wedi gofyn iddi hi gynta.
  - U10b Sam, minutes of the Pennaeth's speech (chat: Y Pennaeth / Y gynulleidfa): tags answered "Nac ydy"; the new lift is an armchair (case Camgymeriad); the only agreed tag is that the speech was short.
  - U11a Mr Puw, workshop report in the passive: things were done (door, table, cap stolen, easy chair eaten); everything "gan ddafad", only one sheep on the station, but he names nobody.
  - U11b Heulwen Haf, forecast for Deck 3: clouds petryal, streipiog, ail-law; painted on the ceiling by Mr Puw llynedd; a pipe broke one last Tuesday (water, not rain; callback U7b); so dry again.
  - U12a Mr Ifan, letter to the editor in -wyd: noise, light broken, parsnips eaten, a sheep found in his cabin, taken back to Mrs Prydderch; "Cwynwyd… chwe gwaith. Nid gan Mr Ifan" — written "ar ran neb".
  - U12b Y Pennaeth, formal apology: last week's paper printed, folded, taken to the doors, found in the allotment, mostly gone; Seren "yn cael blas arno fe'n barod" (this issue).
  - U13a Swyddog Llwyd, corrections to the fair report (Sam decorated the hall, as in case Ffair; Mr Caradog made the tea, the Pennaeth was on holiday, Llwyd will organise the next fair); the only correct item: Seren chairs the committee (callback U7a), again this year.
  - U13b Ms Lewis, neighbours' evening notice: she does everything (Fi sy… / Fi fydd…); the only guest is Mr Puw, her only neighbour, who brings the music, makes the noise and complains about it at midnight. "Dyn trefnus iawn yw e."
  - U14a Mr Caradog, allotment diary: 30 leeks in a night is too many for one sheep → taw defaid sy'n gyfrifol; there is only Seren → "taw hi yw'r defaid".
  - U14b Mr Puw, opinion: the café queue goes round the round deck, so a round queue has no back; he is last and first, Mrs Prydderch is behind and in front of him; no tea since Monday, but "taw fi sy'n iawn".
  - U15a Mr Hopcyn, family careers (consistent with U1a: brother garage, partner choir, father Treorci, sister Caerphilly keeps an eye on everybody, grandfather plants trees); each is sure taw fe/hi sy'n gweithio galeta; so the postman works hardest.
  - U15b Mrs Prydderch, daily task report: the Council's letter (anfonwyd) gives her cadw golwg ar Seren; Seren is always there first (café, allotment, office queue, home); "taw hi sy'n cadw golwg arna i".
  - Authors so far: Sam ×3, Llwyd ×4, Puw ×3, Ms Lewis ×3, Pennaeth ×3, Ifan ×3, Caradog ×3, Hopcyn ×3, Prydderch ×3, Heulwen ×2. Uned 15 ended with Mrs Prydderch, so **Uned 16 must not start with Mrs Prydderch**; Sam and Heulwen are due.
  - U16a Heulwen Haf, forecast with explanations for the di-Gymraeg inspector (she, as in case Treigladau): every word after yn mutates; "sych" on Deck 3 never mutates, like the weather there.
  - U16b Sam, green-living survey on Deck 4 (clipboard borrowed from Swyddog Llwyd): who shares what (ei raw e a'i thebot hi, a'u cwynion nhw…); Seren shares everybody's food, gyda hi ei hun.
  - U17a Mr Ifan, retirement invitation in the conditional: his third retirement; nobody knows what he retires from; he'd like to start doing it before the fourth.
  - U17b Mr Caradog, allotment calendar with dates in words: Seren never eats leeks on 29 Feb, so he plants then; next leeks ready ymhen pedair blynedd.
  - U18a Y Pennaeth, hall rules notice: Swyddog Llwyd gave permission for "one animal, on a lead, between two and three" (as in case Caniatâd); spade not an animal; the rule says nothing about people, so Mrs Prydderch waits at the door: "Does dim caniatâd gyda hi."
  - U18b Mr Puw, opinion on the lost-property sale: no labels, everyone points (hwn/honna…); he bought his own stolen cap (callback U11a), so it's the best cap on the station: paid for twice.
  - U19a Ms Lewis, witness statement in five tenses on the ghost in Cabin 4-116 (as in case Ysbryd, next door to the player); she'd like to live next to it, it never complains, unlike Mr Puw; she can't move in: "Yr ysbryd sy'n byw yno."
  - U19b Mr Hopcyn, the family's future vs the Council's ten-year plan: brother "will come next year" every year; they'd come if his cabin had a window; both plans are the same, with a window if there's money.
  - U20 Rhifyn Arbennig (user chose option 2: one special issue laid out like the exam reading paper): Part 1 Sam's news bulletin (Seren chair for the third time, half a ball found…), Part 2 two emails (Mr Ifan / Y Pennaeth: the Pennaeth must sign every issue in his office, which nobody finds before Tuesday), Part 3 Mrs Prydderch's "Help Llaw" nomination form nominating Seren (form accepted without the corner, so it counts as signed). 8 questions in Welsh, 5 options a–dd.
  - Authors final tally (16–20 added): Sam ×4 (+bulletin), Llwyd ×4, Puw ×4, Ms Lewis ×4, Pennaeth ×4 (+email), Ifan ×4 (+email), Caradog ×4, Hopcyn ×4, Prydderch ×3 (+form), Heulwen ×3.
  - Cabins on Deck 4: the player lives in **4-117**; Mr Caradog in **4-118** (case Sŵn); the ghost's empty cabin is **4-116**, on the other side (case Ysbryd + n19a; renumbered from 4-118 on 12 Oct 2026, user's decision, to fix a clash with Sŵn).
  - Running facts added: Seren still chairs the committee; Mr Puw painted the Deck 3 "clouds" on the ceiling; Mr Hopcyn's sister is professionally nosy.
- Proofreading pass (Claude in the role of a native speaker, 12 Oct 2026; **still not checked by a human native speaker**) fixed: cymdoges for a woman neighbour (not cymydog); gwlân dafad (sheep have wool, not blew); cwpwrdd dillad = wardrobe; Roedd e'n gyfnod… (cyfnod is masculine); "wedi brifo" for "has been hurt" (anafu needs an object); a natural editor's note ("Nodyn y golygydd"). Watch for these in later batches, and keep prepositions with pronouns (aton ni, arno fe…) out of texts before Uned 6.
- Short-future forms of dod follow the textbook (Uned 4 Help llaw): do(f) i, daw e/hi, down ni, dewch chi, dôn nhw. 3rd person singular uses -iff (caniff, agoriff, arhosiff).
- Special issue format (news[20], one item): `special:true`, `parts:[{title,by,byEn,genre,mail?,form?,text}]`; in a `mail` part `t[2]` is `'head'` (header lines) or `'sign'`; in a `form` part `t[2]` is the field label; `qs` carry `part` (index) and 5 Welsh options (shown a–dd, `lang=cy`). Code: `rhif(u)` (20 → "Arbennig"), `textOf(a)`, `newsSheet`/`newsFull` render parts; checker accepts 3–5 parts, ≤40 lines, ≤10 glosses, 6–10 questions × 5 options.
- How content is added: `DATA.news` lives just before `chapters:`. Words outside the course so far are marked `{form|lemma}` with `gloss`. Basic vocabulary of the earlier levels (Mynediad/Sylfaen: gofyn, teulu, dweud, bwrw glaw…) is treated as known and not marked; the checker lists such words for a manual look.
- Check (the English-word test ignores on'd since 12 Oct 2026): `node news/check_news.js game/gorsaf-abercastell.html` (ids, 2 per unit, gloss ↔ marks, 3 × 4 options, 8–12 sentences, tags in unitTags, author not twice in a row, unmarked English, sentences already in the game, words outside units 1–N after un-mutating).
- The user's main game artifact: **https://claude.ai/artifact/GorZWPpARNxXuHBWHmfB7a** – always update THAT one (read it first;
  publish with `url`, omit `capabilities`). Normally the live artifact is the source of truth for the game file. **Exception
  right now:** the ZIP's game = live version 1791806893-ca2a + the Bowen → Llwyd rename (135 changed lines, nothing else). In §10, diff
  the live file against the ZIP's file; if the only differences are the Bowen → Llwyd lines, build on the ZIP's file.
  Never publish the game as a new artifact by mistake, and make sure the user has a fresh Back up code before the first update.

## 9. Verified / not verified (state on 12 Oct 2026)
- **Two looks (user decision, 26 Oct 2026; artifact v9–v10):** the original dark "station" look and a light "manuscript"
  look (mock-up no. 8 of 10: parchment, dark green, gold, double borders, red initial; fonts Libre Baskerville +
  Source Serif 4). CSS: tokens under `:root[data-theme="rukopis"]` + `[data-theme="rukopis"] …` overrides at the end of
  the style block; JS: `THEMES`, `THEME`, `setTheme()`, `themeSwitch()` (moon/sun icon pill in the footnote's link row,
  after Restore — the user rejected a text line "Look: …"), kept per device in localStorage `gorsaf-theme`; default dark.
  Stars are hidden and not drawn in the light look. Verified: the dark look is pixel-identical to v8; all screens at
  320/375/768 px in both looks without errors or sideways scroll; switch persists over reload. Not checked on a phone.
- **Technical audit, 23 Oct 2026 (artifact v8, APK 3.1).** Checked: ESLint (no undefined names, unreachable code, dupe keys);
  data integrity in the browser (every exercise, bank item, tag, unitTag, example key, card key, exam and newsletter
  question; options unique; generators fuzzed 1500–2000× each incl. Treiglydd; orderSet always ≥3 items; AUDIO_INDEX
  contiguous and = pack sizes; all 3163 clip references present); saves (fresh, reload, migration of an old save,
  corrupted save, backup round-trip, tampered code); every side screen at 320/375/768 px; an autoplayer through all 57
  cases (story → puzzle → rush → station, 25 % wrong answers, repairs bought) + overtime. Fixed:
  1. `wrongForms()` lower-cased the rest of a multi-word phrase, so "Pryna i ____ (llyfr Cymraeg)" offered both
     "lyfr Cymraeg" (right) and "lyfr cymraeg" (marked wrong). Now the rest keeps its case (obj generator + Treiglydd).
  2. Rush: a double tap counted the answer twice and could fire two "next question" timers (a skipped question).
     Now one answer per question (`answered` flag in `ask()`).
  3. `save()`: errors were swallowed silently. Now: unchanged data is not rewritten (`lastSaved`), `unavailable` is
     retried once after a random 0.5–1.2 s, other failures retried 3× (4/8/12 s) and the home footnote warns
     ("The last save did not go through… use Back up now"); also saves on `visibilitychange`(hidden)/`pagehide`, and
     the APK calls `save()` in `MainActivity.onPause()`.
  4. Dates from a pasted backup code (`at`, `lastBackup`) were inserted as HTML: now only YYYY-MM-DD is accepted
     (`isDay`).
  5. Starfield with reduced motion stayed blank after a resize.
  6. Scripts: `make_audio.py` refuses to rebuild the packs if previously recorded clips are missing locally (it used to
     drop them silently); `apk/build.sh` refuses to build without all clips in game/audio and creates project/assets.
  Known, not changed: the save document is ≈186 KiB at 100 % progress (limit 256 KiB per db document) — enough now,
  but adding many more cards would need a compact srs format; last-writer-wins if the game is open on two devices at
  once; in the artifact, played packs stay in memory for the session (≤42 MB if everything is played).
- **New account, 23 Oct 2026 (artifact GorZWPpARNxXuHBWHmfB7a v1, with db+user and all 40 packs):**
  (1) [v3, user's FINAL choice after 10 mock-ups] Today's date in Welsh as an amber mono legend set into the top border
  of the leek-streak box on the home screen, **centred** (v4, user's request) (`.streak.hasdate .sdate`, built in `home()` right after `streakEl()`),
  next to the weekday row whose "today" is highlighted — same local calendar day as `today()`. One line always:
  font-size = min(10px, (min(100vw,680px) − 108px) / (chars × 0.6)) via `--n`, plus `fitDate()` shrinking it further
  if a fallback font is wider. (v1 had a line in the card, v2 a paper tag under the header; both removed.) Example: "dydd Gwener y trydydd ar hugain o Hydref". Days dydd Sul…Sadwrn; ordinals 1–31 (yr ail, y deunawfed,
  y pedwerydd ar bymtheg, **yr ugeinfed** (the user wrote "hugainfed"; standard is ugeinfed), yr unfed ar hugain,
  yr unfed ar ddeg ar hugain); month soft-mutated after "o" (Fawrth, Fai, Fehefin, Orffennaf, Fedi, Dachwedd, Ragfyr).
  Device local date, computed when home() renders. (2) Flashcard headword 🔊 is now inline to the RIGHT of the word
  (class `fcaud hw`, inside `.big`), like the example-sentence button; bottom-left position gone. Supersedes the
  "bottom-left" wording in §6.1. Tested Chromium 375 px: date renders, button plays without flipping, no errors, no
  horizontal scroll. Not tested on the published page or a phone.
  v5 (user's request): the leek box no longer shows the "Rhes o gennin. N correct answers a day…" explanation while
  no row is growing (st.n=0, nothing lost) — box gets class `bare`; tapping the box shows/hides that explanation (also
  its `title`). It was the only place that explains the daily rule; nothing in the code depends on the text. The other
  states (Diwrnod N…, the sheep ate them…) still show their line. The first-visit intro ("You volunteer at the help
  desk…", shown only until the first case is closed) is now 14.5 px (class `home-intro`); its content was checked and
  is accurate (story → puzzle → rush → station for every case), it just doesn't mention the extras (cards, newsletter…).
  v6: the leek box on the home screen is always one centred column at every width (`.streak.hasdate`): date legend,
  leek row (max 320 px, centred), then the state line centred (max 52ch). The old side-by-side desktop layout
  (leeks left, text right) applies only to a streak box without the date, which no screen uses now.
  v7: when the sheep is drawn (st.lost && !st.n) the box gets class `sheep` and the leek row 15 px top margin, so the
  sheep (drawn above the SVG's top edge, scales with the row) keeps 10–13 px from the date at 320–1024 px (was 1–4 px).
  v3 test: every day of 2026 (365) and 2028 (366, incl. 29 Feb) at 320/360/375/390/412/680 px, with the APK page (real
  embedded IBM Plex Mono) and with a fallback font: always one line inside the box, no clipping, no horizontal scroll;
  smallest font 7.1 px at 320 px, 8.4 px at 360 px, 10 px from 412 px. Real home() with a mocked clock (29 Feb 2028,
  1 Jul 00:00:05, 31 Dec 23:59:50, 20 Mar) shows the date matching the highlighted weekday. APK 2.9 built with all
  three changes; not installed on a real phone.
  v2 also fixed an old bug: `.topbar{display:flex}` overrode `hidden`, so "← Leave and go back to the desk" showed on
  the desk itself; added `.topbar[hidden]{display:none}`. APK not rebuilt (2.8 lacks both changes).
- **Count in "Find the intruder" (v21, 14 Oct 2026):** the prompt's number must equal options − 1. Four puzzles said "Three of
  these…" with 5 options (agoriad, swn, pwyllgor, chwedl) → now "Four of these…". Checked every intruder/odd-one-out item in
  chapters and bank: the rest either say "One of these is wrong" or have the right count. Keep this when adding puzzles.
- **Credyd after a number (v20):** Welsh nouns stay singular after numerals, so every counted amount reads „58 credyd“, „+7 credyd“,
  „five hundred credyd“ (also the header counter label). Plural „credydau“ only without a number (Spend credydau…, no credydau).
- **Listening page** https://claude.ai/artifact/LVFTUvgAS6StdmU25Fn9bv (source: rows exported from make_audio `lines_for('all')` +
  AUDIO_INDEX, embedded as JSON; packs copied server-side from the main artifact v19). The user flags bad clips there; read them with
  ArtifactData `list` collection `flags` (doc id = clip key, fields text/unit/where/kind/voice/note). After any re-pack, re-export rows
  and re-copy the changed packs to this page too, or it plays stale slices.
- **Hand-picked clip (v18):** card `p1` „Rhowch groeso i…“ — the user found the original take wrong; a fresh CY-EN take
  ("pokus1") replaced `game/audio/cyen-benyw-de-08bcebe7.mp3`, then `make_audio.py all` repacked (only `k1.mp3` changed).
  make_audio never overwrites an existing MP3, so the choice stays; `--prune` keeps it too (key still used). APK 2.5 has the old takes.
- **More hand-picked clips (v19):** card „hen ffrind coleg“ (k1) and the single-word cards „dawn“ (k7) and „man“ (k12) — chosen takes
  copied over the loose MP3s, repacked. Single words have no context, so the G2P read 10 of them as English; `FORCE_CY` in
  make_audio.py forces Welsh for `dawn`/`man` (the other 8 — set, system, project, camp, cap, medal, symbol, bat — are loanwords, left).
  CY-EN synthesis is random per run: a bad clip is fixed by deleting/replacing that one MP3 and choosing among fresh takes.
- **Daily streak = a row of LEEKS (cennin), not parsnips** (user decision, 13 Oct 2026: matches the course, cenhinen/cennin).
  Changed only the streak and what refers to it: `DATA.streak` comment and the 7-day line ("enough cennin for cawl"), the post
  office perks ("The leeks need…", "leek milestones"), the streak messages ("Cennin watered.", "Rhes o gennin.", "Mae'r ddafad
  wedi bwyta'r cennin."), the drawing in `leekSVG()` (green fanned leaves, white shaft, roots) and the end of case 3201
  ("who has been eating your leeks"). **Parsnips elsewhere stay on purpose** (Mrs Prydderch's, the reader's and Mr Ifan's
  parsnips in letters and the newsletter; the exercise "Faswn i byth yn bwyta pannas"): the running joke is that Seren eats
  other people's parsnips but (until U8a) never Mr Caradog's leeks. No audio is affected (streak texts are not recorded).
- **Bare-form headwords (version 15):** 388 noun headwords re-recorded as the bare form (glöwr 0.81 s, gyrfa 0.81 s, cangen 0.91 s,
  gymnasteg 0.97 s; all in AUDIO_INDEX), the two-part clips pruned; u packs byte-identical, only game + k packs uploaded.
  The yForm display fix from version 14 (yr yrfa, y gymnasteg) stays. Not listened to by ear, not re-tested in the browser.
- **Card headword fix (version 14):** 388 noun headwords re-recorded in two parts, the 388 old one-part clips pruned; u packs
  byte-identical, only game + k packs uploaded. Measured: glöwr 0.45 s + 0.51 s gap + 1.03 s; gyrfa ("Yr yrfa") 0.54 + 0.50 + 0.89 s;
  cangen ("Y gangen") 0.63 + 0.50 + 0.88 s (cath is not a flashcard). **Not listened to by ear** (no audio output here), not
  re-tested in the browser (same player and keys; new keys confirmed in AUDIO_INDEX).
- **Flashcard audio (version 13):** 2040 new clips (820 words with the article for nouns, 398 phrases, 846 example sentences, minus
  duplicates); u packs byte-identical to version 12, so only k packs were uploaded. Tested once in Chromium 375 px (Uned 3 drawer):
  Cymraeg→English front shows the button, it plays and does not flip the card; after flipping, the example button plays (pack k3,
  fetched once); English front shows no button; the switch removes / restores the buttons; no errors, no horizontal scroll. Not
  tested: English→Cymraeg back side (same code path), the review mode, phone, APK. **APK not rebuilt** (2.4 has no card audio):
  with 3130 clips it is ≈43 MB, over the 30 MB send limit — see §7.2.
- **§10 FINAL AUDIO PASS (12 Oct 2026, main artifact version 12):** 1055 new clips recorded + 35 old Uned 1 clips = 1090
  (cases + all 39 newsletter pieces), 17.8 MB in 20 packs (largest u6 1.1 MB). Voices spot-checked in the log (Llwyd, Heulwen,
  Mrs/Ms, chat "Darllenydd", special-issue parts → southern woman; Mr …, Y Pennaeth, the two e-mails → northern man). New code:
  `audioNewsLines` (pure, in the AUDIO block), pack player `audUrl`/`audPlay` (APK = loose files, artifact = fetch pack once per
  unit + Blob slice), "Listen to the column/piece/issue" button in the reading view, 🔊 per sentence in the line-by-line view
  (also on the cabin noticeboard), `show()` stops playback. Tested once in Chromium 375 px with the packs served as
  `audio/u*.mp3`: case Perthnasau (Uned 1) and Y Llys (Uned 7) slip clip plays; n7b column plays and advances to the next
  sentence, pressing again stops it; 12 per-sentence buttons, one plays; each pack fetched once; no script errors (only the
  offline font request), no horizontal scroll. Live artifact diffed before publishing: only the Bowen → Llwyd lines differed.
  **Not verified:** playback on the published claude.ai page itself and on a real phone (iOS/Android), the APK with audio,
  pronunciation by a native speaker. Known quirk: "Maer Trecastell", "The agent", "The stranger" etc. get the default
  (female) voice by the §6.1 rule; lines like "c) Mae eich…" read the letter aloud.
- Rename Bowen → Swyddog Rhiannon Llwyd (woman), 12 Oct 2026, in the ZIP's game file only (not yet published): 169 name
  occurrences replaced, ~60 pronouns about her changed (English he/his/him/himself; Welsh e → hi, ar ei phwys hi, i'w chaban hi,
  o'i gwyliau, gyda'i theulu hi; gap/answer keys adjusted). Remaining he/him near her name were checked and refer to other
  people. Syntax OK; `news/check_news.js` output unchanged except the author name; Chromium 375 px smoke test OK (no errors).
  Lines below that mention Llwyd being male describe the earlier state and no longer apply.
- Proofreading pass Uned 16–20 (Claude as native speaker, 12 Oct 2026; still not a human) → version 10: n17a "Dw i ddim yn siŵr beth dw i'n ymddeol ohono fe" (not the ambiguous "siŵr o beth…"); n17b cyfri'r dyddiau (natural southern, not rhifo); n18b dropped "meddai… wrth y til" (wrth after meddai reads as "said TO the till"). Accepted: "ar yr egwyl" for half-time (the game's own exam text uses it), "yr wythnos diwetha" (the game's usage), "fel bob blwyddyn" (spoken), "dau berson". Bowen's Welsh answers (ar ei bwys e/fe, soft mutation) checked.
- Newsletter Uned 16–19 + Rhifyn Arbennig (version 9): checker OK for all units 1–20 (it now skips lines of ≤2 words in the duplicate test, e.g. "Annwyl Gyfaill,"); all 9 new pieces played in Chromium at 360 px (one wrong answer each, credits 10 per piece, Rhifyn Arbennig 7/8 = +35, S.reads saved, home and list show "Rhifyn Arbennig"), no horizontal scroll, no script errors (only the offline font request fails). Worksheets 16–19 checked: no sentences or answers reused (only generic 5-word phrases overlap). Bowen made male throughout the game (≈20 English/Welsh pronoun fixes in questions, answers and narration; Welsh answers "ar ei bwys e/fe" etc.); all remaining feminine pronouns near Bowen were checked and refer to other people or feminine nouns. Welsh checked by Claude only, **not by a human native speaker**. Audio not touched beyond the voice mapping.
- Newsletter Uned 11–15: checker OK for all units 1–15 (remaining notes are only short name/number options); all 10 new pieces played in Chromium at 360 px via `papur(id)` (every question answered incl. one wrong answer, end screens, S.reads saved, credits 29 × 5 = 145 on first reading, gloss bar), no horizontal scroll, no script errors (only the offline Google Fonts request fails in the sandbox). Worksheets 11–15 checked by hand: no sentences or answers reused. Welsh checked by Claude only (mutations after ei/eu/gan/gyda/fy/yn, gender: cadair, ffair, tasg, pibell fem.; southern forms mas, llynedd, gartre), **not by a human native speaker**. Published to the main artifact as version 7 (no audio, capabilities db + user kept).
- Proofreading pass Uned 11–15 (Claude as native speaker, 12 Oct 2026; still not a human) → version 8: n13a now agrees with the game's fair case (Sam sold the coconuts and decorated the hall, so the correction is about the hall, "ei haddurno hi"); n14b "Does dim cefn i giw crwn" (a part of something takes i, not gyda); n15b Friday: "ac roedd Seren wrth y drws" (not the vague "daeth Seren hefyd"). Accepted as they are: a colloquial "fy … i" inside Mr Ifan's -wyd letter (his own mixed register), the -wyd forms gwnaethpwyd (textbook form), llynedd without y (southern spoken). **Check the game's canon (the chapter texts) before writing a correction or a "who did it" piece.**
- Newsletter Uned 6–10: checker OK for all units 1–10; all 10 new pieces played in Chromium at 360 px via `papur(id)` (every question answered, end screens, S.reads saved, noticeboard shows all 10 new cuttings (fresh save)), no horizontal scroll, no script errors (only the offline Google Fonts request fails in the sandbox). Worksheets 6–10 checked by hand: no sentences or answers reused. Welsh proofread by Claude only, **not by a human native speaker**. Second pass (Claude as native speaker, 12 Oct 2026) fixed: mas / bant for allan / i ffwrdd (southern); blwch (course word) for bocs; un noson (a night's stay), not un nos; consistent past tense with a tag (Roedd hi'n…, on'd oedd hi?); elliptical answer "Un fer iawn" (an adjective standing alone would not soften); "i'r lle dw i'n mynd iddo"; "da gyda gramadeg"; "Noson crefftau" (no mutation of the following noun); "yn ôl pawb" in place of "ar bapur" (the ballots are paper).
- Newsletter Uned 2–5: checker OK; all 10 pieces played through in Chromium at 360 px (every question, end screens, noticeboard with 10 cuttings), no horizontal scroll, no script errors; credits 5 per correct answer on first reading (10 × 3 × 5 = 150 checked). Worksheets 2–5 checked by hand: no sentences reused.
- Newsletter Uned 1: checker OK; played in Chromium at 375 px (list, reading, gloss bar, 3 questions, end screen, chat layout, cabin noticeboard) with no horizontal scroll and no script errors; an old save without `reads` loads unchanged and gets `reads:{}`; credits only on the first reading; Back up carries `reads`. Welsh of the two pieces is **not native-checked**.
- Verified: Uned 1 plays in Chromium at 375 px – all clips of case 1 load (HTTP 200) and play, no console errors, no horizontal scroll; the credit line shows on the home screen; script syntax OK; the Bangor dictionary converts all 667 Welsh lines of the whole game without error.
- **Not verified:** pronunciation by a native speaker; audio inside the APK on a real phone; units 2–19 (not recorded).

## 10. FINAL AUDIO PASS — DONE 12 Oct 2026 (kept as the recipe for re-recording)
Goal: record audio for **all units (cases) and all newsletter pieces**, and publish it to the main game artifact **together
with the Bowen → Rhiannon Llwyd rename** (§0), spending as few tokens as possible. Voices: §6.1, unchanged.

### 10.1 Inputs the user brings
- The latest ZIP of this package (its game file already contains the rename).
- The two voice-model files uploaded into the chat: `cy_en_GB-bu_tts-bangor-medium.onnx` (77 MB) and
  `cy_en_GB-bu_tts-bangor-medium.onnx.json`. Copy them to `audio/voices/cyen/`. (Hugging Face is blocked for you.)
- `pip install techiaith-g2p onnxruntime numpy` (PyPI works; plus node, ffmpeg). The script checks the g2p `data_version`.

### 10.2 Steps
1. **Game file.** Use `game/gorsaf-abercastell.html` from the ZIP. Never read it whole into the conversation: use grep/sed
   and scripts. (Publishing to the artifact later requires reading the live version once – see step 9.)
2. **Newsletter audio lines (pure code inside `/*AUDIO-BEGIN*/…/*AUDIO-END*/`):** add `audioNewsLines(article)` returning one
   line per Welsh sentence: text = sentence with every `{form|lemma}` replaced by `form`, then `audioText`. Voice:
   ordinary pieces → `audioVoice(t[2] || article.by)` (t[2] is the chat speaker when present); special issue (`special:true`,
   `parts`) → per part, `audioVoice(part.by)`; in `mail` parts skip lines with `t[2]==='head'` (e-mail headers), read `'sign'`
   lines; in `form` parts `t[2]` is a field label, not a speaker. Check the real `DATA.news` shape first (see §8; there is a
   helper `textOf(a)`).
3. **Generator:** extend the `NODE` snippet in `audio/make_audio.py` to collect `audioNewsLines` for every article of
   `DATA.news[unit]` of the chosen units, so `all` covers cases + newsletter.
4. **Packs for the artifact:** (DONE; `.mp3`, not `.bin`, see §7.1) after recording, the script writes `game/audio-packs/u<N>.mp3` = the MP3s of unit N
   concatenated (cases + newsletter; a clip used in several units goes to the lowest unit; news[20] = pack u20), and writes
   into the game, between the existing `/*AUDIO-HAVE*/ … /*AUDIO-HAVE-END*/` markers:
   `const AUDIO_INDEX={key:[N,offset,length],…};const AUDIO_HAVE=new Set(Object.keys(AUDIO_INDEX));`
   Keep the loose MP3s in `game/audio/` (the APK uses them).
5. **Player (`audPlay`):** APK (`window.GORSAF_LOCAL`) → loose file `audio/<key>.mp3` as now (Android WebView cannot
   `fetch()` file:// URLs). Artifact → `fetch('audio/u'+N+'.mp3')` once per unit (cache the promise), slice
   `[offset, offset+length]`, `new Blob([...],{type:'audio/mpeg'})`, `URL.createObjectURL` (cache per key), play.
   Any failure: stop quietly.
6. **Newsletter UI:** 🔊 per sentence in the piece's final "sentence by sentence" view, and one "Listen to the column" button
   in the reading view that plays all its sentences in order (press again or leave the screen = stop). Only where clips
   exist. Same `.aud` look.
7. **Record:** `python3 audio/make_audio.py all > /tmp/audio.log 2>&1; tail -3 /tmp/audio.log` – **never print the full
   list**. Spot-check ~10 lines with grep (Llwyd and other women = cyen-benyw-de, men = cyen-gwryw-gogledd).
8. **Test once**, Playwright at 375 px, serving `game/audio-packs/*.bin` as `audio/*.bin`: one case in two different units
   and one newsletter piece – a clip plays, "Listen to the column" plays, no console errors, no horizontal scroll.
9. **Publish once** to `https://claude.ai/artifact/GorZWPpARNxXuHBWHmfB7a`: `Artifact read` it; the tool requires you to Read
   every line of the saved live file before it accepts a publish (~5200 lines; do it once, right before publishing).
   Diff it against the ZIP's original game file: expected differences are only the Bowen → Llwyd lines (§8). If the live
   version has anything else new, merge it. Then publish: `file_path` = the game, `url` = the main artifact,
   `files` = `{"audio/u1.mp3":"game/audio-packs/u1.mp3", …}` (~20 files), **omit `capabilities`** (keeps db + user).
   No loose MP3s. The voice credit line appears by itself.
10. **APK only if the user asks:** `apk/build.sh` copies loose `game/audio/` (not the packs); bump the version (§7.2).
11. Update §0, §6.1 status and §9; rebuild the ZIP (without `audio/voices/`), send it, and report in Czech in a few lines:
    counts and MB recorded, what was tested, what not (native-speaker check, phone).

### 10.3 Size
≈0.5 MB per unit for cases + ≈0.3 MB for its newsletter ≈ 15 MB in total; each pack is far below the 15 MB file limit.
