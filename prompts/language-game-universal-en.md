# Language-practice game — universal build prompt

> **How to use this prompt.** Paste the whole file into a new Claude chat. Fill in what you know in the `[brackets]` of
> §1; anything you leave as `[ ]` Claude will ask you about once, in one short message, with a sensible default for each.
> Then send your first chapter (or say "no textbook").
>
> Derived from *Gorsaf Abercastell*, a Welsh course game built with Claude in 2026 (20 units, ~4000 lines, 3130 audio clips,
> Android app). Everything Welsh-specific has been turned into a choice or a rule that works for any language.

---

## 0. Your role and the goal

You are building, and then maintaining over many sessions, **one interactive game** that teaches me a language. It must be
something I come back to because I want to, not a school exercise. It is published as a claude.ai **artifact** (one HTML
file, progress saved to my account) and, if I choose the module, also as an offline **Android app**.

You are the game designer, the course writer, the engineer and the proofreader. Work carefully. I can't check the
language myself, so a wrong sentence in the game teaches me a mistake.

---

## 1. Setup (fill in, or leave `[ ]` and Claude will ask)

**Me**
- Target language and variety: `[e.g. Welsh, southern]` — one variety, used consistently (spelling, vocabulary, forms).
- My level: `[e.g. A2 / "second year evening class"]`
- My native language: `[ ]` — Claude talks to me in it, briefly.
- Language of the game's interface and narration: `[English / my native language / the target language]`. Exercises are always in the target language.

**Material**
- Textbook / course: `[name, or "none"]`
  - *With a textbook:* I send chapters (PDF/photos) and worksheets one at a time; the game follows them chapter by chapter.
  - *Without:* propose a syllabus of `[N, default 12]` units for my level (topic + grammar + ~40 words each), wait for my OK, then build unit by unit.
- Does the course end with an exam? `[yes: name / no]`

**World**
- Setting: `[default: an ordinary municipal help desk on an orbital space station]` — any place works (a lighthouse, a hotel
  on the Moon, a village post office, a submarine…). Rule: **the situations stay everyday** (forms, shopping, neighbours,
  work, weather), only the circumstances are fantastical, so the vocabulary stays useful.
- My role in the world: `[default: a new clerk who solves residents' "cases"]`
- Tone and humour: `[default: dry, ironic; the narrator is mildly weary of the world and teases me and itself; praise is sparse; no cute mascots]`
- Content limits: `[e.g. family-friendly]`
- Running motif for the daily streak: `[default: something from the target culture, e.g. a row of leeks for Welsh]`
- In-game currency name: `[default: the target-language word for "credit"]`

**Modules** (the core game is always built; tick the rest)
- `[x]` Core game (§3), always
- `[ ]` A. Community newsletter with reading comprehension (§5A)
- `[ ]` B. Recorded audio in the target language (§5B)
- `[ ]` C. Listening page for reviewing and flagging the recordings (§5C), needs B
- `[ ]` D. Offline Android app (APK) (§5D)
- `[ ]` E. Mock exam (§3.8), only if the course has an exam

**Working style**
- Pace: `[default: one chapter at a time; wait for my "ok" before the next]`
- Token budget: `[default: careful. Don't reread the big file whole, test once, publish once.]`

**Rules for the setup questions:** ask only about unfilled fields, all in **one** message, each with your proposed default,
so I can answer "defaults are fine". Then start. Never ask again about something I already answered.

---

## 2. Material rules (binding)

1. **Never reuse sentences or answers from homework/worksheets.** Practise the same grammar and words with different
   sentences. Examples from the textbook itself are fine. Also never duplicate a sentence already in the game. Check before adding.
2. Stick to the chapter's grammar and vocabulary. If material is thin, write your own sentences at the same level, but
   **no grammar from later chapters**. Words from earlier chapters are allowed.
3. Several chapters sent at once → still build them **one by one, in order**, with the full check after each, and tell me where you are.
4. The last chapter may be special (exam preparation). Treat it on its own terms, decide what fits and explain why.
5. Before writing exercises for a chapter, list for yourself: its grammar points (as skill tags with a one-sentence rule),
   its full word list, and the "tricky features" this language has at this level (see §4).

---

## 3. Core game

### 3.1 Home screen
- Top: course name, a small quiet progress chip ("X/Y cases closed"), the currency counter, the streak row.
- A row of numbered buttons, one per chapter (+ exam), jumps straight to a chapter. A **Continue** button opens the next unfinished required case.
- Chapters are collapsible groups; only one is open (the current one by default). The collapsed header shows completed-case
  dots and "filed X% · cards Y%".
- Inside a chapter: a "Grammar notes" toggle (short summary of the chapter's grammar), its cases, the vocabulary game, the flashcard drawer.
- "Any time" section: Today's review, Overtime, the language-specific trainer (§3.7).
- Everything that is a reward and not learning (repairs, cabin, shop, newsletter noticeboard) sits in a separate, collapsible
  **bonus** section at the bottom, visually set apart (dashed divider + label + subtitle such as "where the credits go").
  Its open/closed state is remembered.
- At the very bottom, in small print: save status, **Back up**, **Restore**, **Reset progress** (with confirmation inside the
  page; dialogs like `confirm()` don't work in artifacts), and the voice licence credit if audio exists.

### 3.2 A chapter = 3 cases (5–10 minutes each)
1. **Recognition** (open from the start).
2. **Production**: actively writing full sentences (opens after case 1).
3. **Optional "a bit of everything"** (opens after case 1, never blocks progress, gives a commendation pin instead of a souvenir).

Each case has four phases, with a phase bar shown only inside cases:
1. **Story and mystery**: short scenes; I answer in the target language (multiple choice, fill the word, write the
   sentence). Characters' lines in the target language appear on "official paper slips". It ends with a reveal or a
   punchline and a **souvenir** that appears in my cabin.
2. **Puzzle**: calm logic built on the language. Work out a rule from examples, build a sentence from tiles (with
   distractor tiles), match pairs, find the odd one out.
3. **Speed round**: 60 seconds, multiple choice, combo multiplier (×2 after 3 right, ×3 after 6, ×4 after 10), personal best.
   Questions are **generated from tables of forms** (not a fixed list), only from this chapter. After a mistake the timer
   pauses and a one-line explanation shows. Within a round nothing I got right comes back; a mistake comes back once, a few
   questions later, marked "back again". If all distinct questions run out early, the round ends with "counter cleared" + a
   bonus point per second left.
4. **Maintenance** (bonus, §3.9).

End of a case: a summary by skill (what I'm good at, what to review, each with its one-sentence rule) and an offer of the next case or Overtime.

### 3.3 Exercises
- Every question belongs to a named **skill tag**. Whatever I get wrong comes back later in a different sentence or task type, also in later cases.
- Immediate feedback; for a mistake, a one- or two-sentence explanation of *why*.
- Written answers: accept every correct variant; tolerate small typos and missing diacritics, **except where they are the
  point of the exercise** (§4), which must be exact. Under every text field in small print: "Accents (…) are optional."
  Distinguish "right words, wrong form" from "wrong".
- Out of its story (review, Overtime, inspections), a question shows "Topic: … · Chapter N" above it. Any prompt whose
  answer depends on tense/form/register states it explicitly ("past tense, type the verb"). Never make it guesswork.
- Tiles: tap moves a tile between tray and sentence; tiles can also be dragged to reorder (mouse and touch).
- Matching: the second group has a subtly different tint so the groups are distinguishable when stacked on a phone.
- **Never ask anything from a chapter I haven't played.** Overtime, review and inspections only use chapters with at least
  one closed case. Clean stale weak spots from unplayed chapters on load.

### 3.4 Vocabulary game ("lost property", or whatever fits the setting)
- **Every word** of the chapter's list, no exceptions. Question types: meaning (target → mine), reverse, and the
  language's key word properties (plural, gender, article, aspect pair, measure word, tone…), plus writing from memory.
- Every word comes up before any word repeats.
- A word is "filed" after correct answers in two different question types, "gold" once written correctly. Home shows "filed X%".
- If you're unsure of a word's gender/form, don't ask about it, and tell me which words they are.

### 3.5 Flashcard drawer (per chapter, open regardless of progress)
- All words of the chapter + useful phrases; both directions, mixed; sessions of 15; buttons "no idea" (comes back this
  session), "later" (to the end), "I know".
- A coloured stripe by word class (e.g. red feminine noun, blue masculine noun, green adjective, grey verb, purple
  other/phrase; adapt to the language's classes), with a legend on the first card. No pictograms.
- The back shows the key forms (article/plural/gender/inflected form, whatever matters in this language). Regional or
  register variants get a small badge.
- **Headword shown in its dictionary form.** Audio (if module B) speaks the bare form only.
- Example sentence on the back for words and short phrases: short, target language, the word highlighted (also when
  inflected), translation hidden behind a small "▸ translation" tap. Stored separately from the cards.

### 3.6 Today's review (spaced repetition)
Known cards and missed skills are scheduled at 1, 3, 7, 14, 30, 60 days; a miss resets to tomorrow. A round = up to 10
grammar items + due cards, max 30; "another round" if more are due. The button shows how many are due or when the next is.

### 3.7 Language-specific trainer
One 60-second drill for **the single hardest systematic feature** of this language at my level, with its own record, only
over finished chapters. Examples: Welsh mutations (modes soft/nasal/aspirate), German case endings, Czech/Polish/Russian
cases, Spanish ser/estar or subjunctive triggers, French gender + agreement, Mandarin measure words or tones, Japanese
particles or verb forms, Arabic broken plurals, Finnish consonant gradation. Propose it once you've seen the first chapters.

### 3.8 Daily streak and exam
- Streak: a small row of the motif (§1) for the last seven days, today on the right, weekday abbreviations in the target
  language. A day counts after 5 correct answers. Milestones 3/7/14/30/50/100 days give bonus currency. On mobile the row
  sits full-width above its text.
- Mock exam (module E): timed, mirrors the real exam's written parts, no hints or marking until the end, alternating papers
  on resits, a certificate in the cabin on passing. Plus vocabulary and flashcards for that chapter.

### 3.9 Bonus economy
- Currency is earned **only by correct answers**, never by time.
- **Maintenance:** parts of the setting (station modules, lighthouse lamp, hotel lift…) can be repaired. Each repair is a
  work order of three questions (two right to pass), paid only on success. Each part changes a rule (longer speed round,
  a forgiven mistake, second attempts, more currency, bonus questions from weak spots, crossed-out wrong options…). Each
  part has 3 tiers at rising prices, tiers 2–3 unlock after later chapters; new parts appear as chapters are finished;
  finishing a chapter can "wear out" a working part, which must be repaired again. A map shows every part's state.
  Calibrate prices for the whole course.
- **Cabin/room:** souvenirs and pins on one wall; a shop of purely cosmetic items for currency on a second wall.
- **Grammar of the currency:** amounts follow the target language's number agreement rules (e.g. Welsh keeps the noun
  singular after numerals: "58 credyd", not "58 credydau"). Apply the same care to every counted noun the game shows.

---

## 4. Adapting to the language (do this explicitly, and tell me your choices)

Before the first chapter, write a short **language profile** into HANDOFF.md and follow it everywhere:
- **Script and direction:** non-Latin script → show romanisation where the course does; right-to-left → `dir="rtl"` on
  target-language text, mirrored layout where needed; a font that has every character (also offline in the app).
- **Input:** what a learner can actually type on a phone. Offer on-screen buttons for special letters, and for non-Latin
  scripts accept the course's romanisation where it makes sense.
- **What must be exact vs tolerated:** the features that carry the grammar (mutations, endings, cases, tones, particles,
  gender agreement) are exact; incidental accents/typos are tolerated. List them.
- **Word properties** for the vocabulary game and cards (gender, plural, article, aspect, measure word, etc.).
- **Number agreement** for every counted noun in the UI (§3.9).
- **Variety:** one regional standard, consistently; other variants only as badged extras.
- **Names and culture:** characters have plausible names from the target culture; small cultural details make the world.
- **Weekday names, dates, numbers** in the target language as the course teaches them.

---

## 5. Optional modules

### 5A. Community newsletter (reading)
- A small in-world newspaper, **2 short pieces per chapter** (8–12 sentences), unlocked with the chapter, readable on the
  cabin noticeboard. Each piece uses the chapter's grammar heavily and is written by a recurring resident: no author twice in a row
  across chapters, authors balanced over the course.
- Genres rotate: column, letter to the editor, notice, interview, forecast, minutes, advice column, report, form, group chat.
- **Punchlines first:** for each batch, propose one-sentence punchlines (author + genre + the joke) and wait for my approval,
  then write. Humour = absurd logic taken seriously; running jokes and recurring facts stay consistent (keep a list in HANDOFF.md).
- Words outside the course so far are marked and glossed (tap to see); basic earlier-level vocabulary is treated as known.
- 3 comprehension questions per piece, 4 options each, in the target language. Currency for the first reading only.
- If the course has an exam: one special issue laid out like the exam's reading paper.
- Write a small checker script (ids, counts, glosses ↔ marks, author rotation, sentences already in the game, unmarked
  foreign words, words beyond the current chapter) and run it on every batch.

### 5B. Audio
- A **local open TTS model** run in your workspace (e.g. a Piper voice with a proper pronunciation dictionary/G2P where
  one exists), not a paid online service. Research the best available voice for the language and variety and tell me
  where to download it. Your workspace usually can't reach model hosts, so I upload the model files to the chat.
  Record a test unit first; I listen and approve before you record the rest.
- Voices by role: narrator, the corrected sentence after answering and female characters → one voice; male characters → another.
  Slightly slower than native pace (e.g. length_scale ≈ 1.08). Keep the licence credit in the game if required.
- What is recorded: characters' lines, the full correct sentence after each answer ("Hear it"), newsletter pieces
  (sentence by sentence, with "listen to the column"), flashcard headwords (bare form) and their example sentences.
- **Architecture:** the game's own code decides what gets recorded. A pure function block (no DOM) maps exercise → lines
  `{voice, text, key}` and the recording script runs **that same block** in Node, so file names always match. Key =
  voice + text hashed (e.g. FNV-1a). Record only missing clips and never overwrite an existing one, so hand-picked takes survive.
- MP3 mono 48 kbps, leading silence trimmed, 0.15 s tail. For the artifact, clips are concatenated into per-chapter **packs**
  (`u<N>.mp3` for cases + newsletter, `k<N>.mp3` for flashcards) plus an index `{key: [pack, offset, length]}` written into
  the game; the game fetches a pack on first use and slices it. Packs must have a `.mp3` extension (`.bin` is not served).
  Keep a script that rebuilds loose clips from packs (ZIPs can't carry 40+ MB).
- A 🔊 button appears only where a clip exists; missing audio never breaks anything. On cards: a small muted button on the
  target-language side only, never flipping the card.
- **Quality:** synthesis is random per run. For a bad clip, generate 2–3 fresh takes, I pick one and it replaces the file.
  Single words without context may be read as English: find them and force the target language for non-loanwords.
  A duration-per-phoneme scan catches truncated/garbled clips (not mispronunciations). You can't hear: say so, and rely on me.

### 5C. Listening page (needs 5B)
A separate artifact listing every clip: filters (chapter, kind, search), play one / play all in sequence with the current
row highlighted, "heard" greying (per-browser), and a **Flag** button with a note field stored in the artifact's database
(capabilities `db` + `user`, collection `flags`, doc id = clip key). When I say "fix the flagged ones", read them, make fresh takes and let me choose.

### 5D. Android app (APK)
- The same HTML in a WebView, fully offline: fonts bundled, a storage shim in place of account saving, a small JS bridge
  for copy/paste/share of backup codes, loose MP3s in assets, `setMediaPlaybackRequiresUserGesture(false)`.
- Build with command-line tools fetched from npm if Google's servers are blocked; sign with **one keystore created once**,
  given to me with its password, and reused forever (otherwise updates won't install over the old app). Raise versionCode every build.
- Files over the 30 MB send limit: split into two parts and give me the join command for my OS
  (Windows: `cmd /c copy /b app.apk.part00+app.apk.part01 app.apk`) plus the first 16 hex chars of the SHA-256 to check.
- Progress moves between the artifact and the app via **Back up / Restore**.

---

## 6. Technical rules

- **One HTML file.** CSS tokens on `:root`, then one `<script>`. All language content in one `DATA` block (tags, words,
  phrases, examples, notes, form tables for generators, review bank, chapters, newsletter, exam, streak, station, shop),
  clearly separated from logic. Any language/audio block that a script must run lives between marker comments.
- Design with the atmosphere of the world (e.g. dark station, target-language lines on paper slips, rubber stamps on
  answers), tasteful animation, works on phone and desktop with no horizontal scroll, readable in light and dark.
- **Saving:** publish with capabilities `db` + `user`, save to the per-user doc `data/users/<id>/save`; the game also runs
  without saving. **Version the save format and migrate** every old save (renamed keys keep progress, new fields get
  defaults). **Never lose my progress.** Browser storage only for tiny conveniences.
- **Backup/restore:** a copyable code (prefix + version + checksum + data). Restore validates it, shows a summary (date,
  cases, currency, cards) and replaces progress only after confirmation inside the page.
- Always republish to the **same artifact URL**. Read the live artifact before publishing if another chat may have changed it.
- Platform limits to plan for: file sent to me ≤ 30 MB; one publish ≤ 64 MB / 255 files; one file in an artifact ≤ 16 MB.

---

## 7. Workflow and quality (every chapter)

1. Read the chapter + worksheet. Draft the skill tags and the word list.
2. Build: 3 cases, notes, vocabulary, flashcards + examples, generator tables, review items (+ newsletter/audio if enabled).
3. Check, and report what you checked:
   - every target-language sentence correct and natural in the chosen variety; agreement, forms and the tricky features of §4;
   - no worksheet sentences, no duplicates of existing game sentences; every listed word present;
   - every question unambiguous out of context; any count in a prompt matches the options ("Four of these…" with 5 options);
   - syntax check of the script, then **one** play-through in a headless browser at phone width (≈375 px): no console errors, no horizontal scroll;
   - save → reload → progress intact; old save migrates.
4. Publish once. Report in my language, briefly: what was added, **what you verified and what you didn't**, what you're
   unsure about in the language, and the reminder that the content is **not checked by a native speaker**.
5. Wait for my "ok" (unless I said to continue).

When I report a language mistake, fix it **everywhere** it occurs (search the whole DATA block), and add the rule to the
language profile so it doesn't come back.

---

## 8. Hand-over and memory

Keep a **HANDOFF.md** written for a Claude who has never seen the project: what it is, my rules and decisions (with dates),
the language profile, code map, how to add content, audio pipeline, publishing (artifact URL), APK build (versionCode of
the last release, keystore location), the running jokes and world facts, and a "verified / not verified" log. Update it
with every change. When I ask, deliver a **ZIP** (game, HANDOFF.md, scripts, APK project + keystore; audio packs as
separate ZIPs under 30 MB) and short instructions in my language for continuing in another chat or account.

---

## 9. How to talk to me

- My native language, short, factual. No step-by-step narration of your work; tell me results, decisions needed and problems.
- For bigger design choices: give 2–3 options with your recommendation, let me choose, then build → test → publish.
- If something essential is missing, ask; otherwise build.

**Start now:** ask the setup questions from §1 that are still open (one message, with defaults). After my answer, write
the language profile, propose the world's recurring cast (6–10 residents with one line each) and the streak motif, and
then build chapter 1.
