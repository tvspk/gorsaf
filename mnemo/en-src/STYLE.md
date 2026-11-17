# English Mnemo Hooks – style guide (binding for every deck)
- Audience: native British English speaker. Hooks use British sound-alikes, British words and culture (no Czech anywhere).
- Format per card: `NNNN|meaning|example translation|hook`, options `+cu= +pozn= +rod_pozn= +puvod= +s.pozn= +s.exc= +famN=` (famN replaces family entry N).
  Build: `python3 -I mnemo/merge_en.py mnemo/decks/X.json mnemo/en-src/NN.txt mnemo/decks-en/X.json`.
- Sound-alike in CAPITALS with the Welsh syllables in brackets: `A GORilla (A-GOR-iad)`. Language-neutral
  etymology hooks are fine (`cyf- (together) + gweld (to see)`). Vivid, absurd, concrete images beat clever wordplay.
- Mutation notes in examples: `(claf → [g]laf after ei = his)`. North notes: `north: X instead of Y (L5)`.
- GENDER CODE (nouns only): feminine = HOT / RED, masculine = COLD / BLUE. Rotate the image, never reuse one
  within a deck, and avoid repeating it in the neighbouring deck.
  Feminine pool: roaring bonfire, red lava, chilli, red-hot poker, glowing embers, the red dragon breathing fire,
  pillar box, red double-decker bus, red phone box, poppies, strawberries, ketchup, sunburn, lipstick, rubies,
  ladybird, fire engine, Bonfire Night sparklers, sauna, tomato soup, red kite (bird), postman's red van, toaster.
  Masculine pool: icicles, glacier, snowman, frost, blizzard, penguin, polar bear, igloo, freezer, frozen pond,
  ice skates, blue ice lolly, Arctic, hailstones, frozen fish fingers, sapphire, frostbitten blue nose,
  cold shower, snow globe, blue ice-cream van, slush puppy, ski lift, walrus.
  Pool exhausted? Add new images with the same temperature/colour, avoid characters and brands.
- Nouns of both genders (m/f): a lukewarm or purple image. Plural-only nouns, verbs, adjectives, phrases: no colour.
