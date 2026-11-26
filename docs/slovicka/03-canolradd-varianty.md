# Canolradd – systém variant (jih → sever, spisovná)

Platí pro všechny balíčky Canolradd. Hlavní pole karty = jižní hovorová velština (jazyk učebnice).

## Kdy kartě přidat "varianty"
1. **Liší se samo slovo** (allwedd / goriad): "varianty.sever" přepíše "slovo", případně "rod", "plural", "priklad", "priklad_cs". Audio: `<id>-sever.mp3` + `<id>-sever-p.mp3`.
2. **Slovo je stejné, ale příkladová věta obsahuje jižní gramatiku nebo slovo** (dych, Beth yw, gyda chi, arian…): "varianty.sever" přepíše jen "priklad", "priklad_cs" a přidá "pozn". Audio: jen `<id>-sever-p.mp3`.
3. **Neliší se nic** → pole "varianty" vynech.
4. Každá "pozn" uvádí, co se liší, a zdroj: číslo lekce (rámeček Y De a'r Gogledd), nebo „mimo učebnici“.
5. Když si severním tvarem nejsem jistý, variantu nepřidávám (lepší žádná než vymyšlená). Při pochybnosti "overit": true.

## Převodní tabulka jih → sever
| jih | sever | zdroj |
|---|---|---|
| gyda (s) | efo | L2 |
| mas | allan | L3 |
| arian (peníze) | pres | L4 |
| Beth yw e? | Be ydy o? | L5 |
| Mae car gyda fi / gyda chi | Mae gen i gar / gynnoch chi | L6 |
| Mae … gyda ni | Mae gynnon ni … (předmět měkce mutuje) | odvozeno z L6; schváleno 12. 11. 2026 |
| gallu | medru | L7 |
| brwnt | budr | L7 |
| llaeth | llefrith | L8 |
| Beth? | Be? | L9 |
| eisiau | isio | L10 |
| dych chi | dach chi | L11 |
| nawr | rŵan | L12 |
| crac | blin | L13 |
| cwympo | syrthio | L14, L15 |
| taw | mai | L14 |
| tost | sâl | L15 |
| allwedd | goriad | L16 |
| tad-cu, mam-gu | taid, nain | L17 |
| edrych (ar) = dívat se (na) | sbio (ar) | L18; jen ve významu „dívat se“, ne „vypadat“ (edrych yn…), edrych dros, edrych ymlaen; schváleno 12. 11. 2026 |
| cer! | dos! | L18 |
| dere! | tyrd! | L19 |
| fe / e (on) | fo / o | L1 |
| dyw … ddim | dydy … ddim | mimo učebnici; věty z učebnice s dydy: v hlavní větě dyw, dydy do varianty (schváleno 12. 11. 2026) |
| ysgrifennu / sgrifennu | sgwennu | mimo učebnici |
| twymo (ohřát) | cynhesu | mimo učebnici (cynhesu L2, twymo L12); schváleno 12. 11. 2026 |
| lawr llawr (dole) | lawr grisiau | mimo učebnici (lawr llawr L16); schváleno 12. 11. 2026 |
| bant (pryč) | i ffwrdd | mimo učebnici; schváleno 12. 11. 2026 |
| gartre (doma) | adra | mimo učebnici; schváleno 12. 11. 2026 |
| ces i (dostal jsem) | ges i | mimo učebnici; schváleno 12. 11. 2026 |
| i fi | i mi | mimo učebnici; schváleno 12. 11. 2026 |
| dweud, dwedodd | deud, deudodd | mimo učebnici; schváleno 12. 11. 2026 |
| 'te (tak, tedy) | 'ta | mimo učebnici; schváleno 12. 11. 2026 |
| cwrdd (â) | cyfarfod (â) | mimo učebnici; schváleno 12. 11. 2026 |

Tvary s Faswn i / Faset ti zatím nepřevádím (severní tvary kolísají: faswn / fyswn, fasat / fysat).

## Spisovná velština ("varianty.spisovna")
Motor zná jen klíče "sever" a "spisovna"; jiné varianty (např. Patagonie) by vyžadovaly změnu motoru.
Spisovné tvary se do karet doplňují jen na pokyn uživatele. Typické převody: dych chi → ydych chi, dw i → rydw i / yr wyf, dyw … ddim → nid yw, faswn i byth → ni fyddwn byth, mae'n flin gyda fi → mae'n ddrwg gennyf.
