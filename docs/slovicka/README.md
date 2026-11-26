# Slovíčka Canolradd (zdroj karet Mnemo Hooks): předání

Stav: **26. 11. 2026**. Psáno pro libovolnou AI nebo vývojáře, nepředpokládá Claude.
Ověřeno proti claude.ai projektu „Canolradd gORSAF 26112026“ a proti GitHubu `tvspk/gorsaf` (poslední commit
26. 11. 2026 11:01 UTC, „3.13-en: voice speed for every Welsh recording“).

## 0. Jak začít v nové AI (zkopíruj jako první zprávu)

> Jsi můj lektor velštiny a správce mých flashcards. Odpovídej česky, stručně a věcně. Pravidla jsou v souboru
> `docs/slovicka/01-instrukce-projektu.md`, stav a rozhodnutí v `docs/slovicka/README.md`, mapa učebnice v `02-canolradd-rozcestnik.md`,
> severní tvary v `03-canolradd-varianty.md`, data v `mnemo/decks/cy-canolradd-01.json` až `-40.json` (v tomto repozitáři).
> Neměň id karet, karty nemaž (jen "vyrazeno": true), nevymýšlej tvary ani rod (při pochybnosti "overit": true).
> Dnes chci: …

Pro práci s aplikací (kód): nejdřív `START-HERE.md`, `CLAUDE.md` a `HANDOFF.md` (§000) v kořeni repozitáře.

## 1. Co projekt je (dvě vrstvy)

1. **Slovníková továrna (claude.ai projekt „Canolradd gORSAF“).** Z učebnice *Dysgu Cymraeg – Canolradd (B1), jižní
   verze*, 20 lekcí (PDF jsou u uživatele), vznikly flashcards: **899 karet ve 40 balíčcích JSON**
   (`cy-canolradd-01.json` … `-40.json`, id `cy-canolradd-0001` … `0899`). Ke každé kartě: jižní tvar, český a anglický
   význam, příkladová věta (většinou z učebnice), česká mnemotechnika s barvou rodu, příbuzná slova, rod/plurál/kmen,
   severní varianta (168 karet), mutace.
2. **Aplikace Gorsaf Abercastell (GitHub `tvspk/gorsaf`).** Hra na učení velštiny (vesmírná stanice, případy, mutace,
   zkouška, 4208 velšských nahrávek). Balíčky z bodu 1 jsou v ní jako sekce **Mnemo Hooks** (SRS: rozpoznání,
   psaní, poslech). Dvě aplikace ze stejného kódu:

| | Česká Mnemo aplikace (původní) | **Anglická aplikace (aktivní)** |
|---|---|---|
| Zdroj | `game/gorsaf-abercastell.html` (ruční úpravy) | `game-en/gorsaf-abercastell-en.html` (**odvozený**, nikdy ručně) |
| Texty Mnemo | česky (`mnemo/decks/`) | britská angličtina (`mnemo/decks-en/`, ze zdrojů `mnemo/en-src/NN.txt`) |
| Android | `cymru.gorsaf.abercastell`, 3.4 (versionCode 16), buildí se jen lokálně | `cymru.gorsaf.abercastell.en`, **3.13-en (versionCode 10)**, buildí GitHub Actions |
| Web | claude.ai artefakt AbSoWLbaanut3eBz7yNa51 | https://tvspk.github.io/gorsaf/ (+ artefakt VvLiuefz5QgFQP91qwDMYx bez synchronizace) |
| Synchronizace | ne | ano, šifrovaně přes soukromý repozitář `tvspk/gorsaf-en-sync` |

Stažení EN aplikace: https://github.com/tvspk/gorsaf/releases/latest/download/gorsaf-en.apk

## 2. Stav k 26. 11. 2026

**Data (balíčky):**
- Učebnice zpracovaná **celá** (lekce 1–20). Nic nečeká na zpracování.
- Revize všech 40 balíčků 12.–13. 11. 2026 (14 závažných, 163 drobných, 171 stylistických nálezů, vše opraveno).
- Mnemotechniky přebarveny 13. 11. 2026 (202 podstatných jmen, 183 změněno; pestré střídání motivů, viz oddíl 6).
- **Balíčky = `mnemo/decks/` v tomto repozitáři.** Čísla "verze" všech 40 balíčků odpovídají konečnému stavu
  z projektu (01: 5, 02: 6, 16: 6, 29: 5, 37: 5 …); obsah karty 0001–0026 porovnán ručně, shodný.
  V repozitáři jsou zapsané kompaktně (jedna karta na řádek), obsah je stejný.
- Statistika: 423 podstatných jmen, 177 sloves, 123 přídavných jmen, 91 ostatní, 85 frází; 168 karet se severní
  variantou (16 z nich s jiným slovem); 0 vyřazených; 212 karet bez české mnemotechniky (hlavně věty a fráze).

**Aplikace (z GitHubu, mladší než souhrn v repozitáři):**
- 3.11-en (26. 11.): verze aplikace dole na stole. 3.12-en (26. 11.): zvuk správně/špatně v „Lost property“.
  3.13-en (26. 11.): rychlost velšského hlasu 1× / 0,9× / 0,8× / 0,7× pro všechny nahrávky.
- `apk/verze-en.txt` = `10 3.13-en`, release v3.13-en i build stránek proběhly úspěšně. **Další EN APK musí mít versionCode ≥ 11.**

## 3. Co je v této složce

| Soubor | Obsah |
|---|---|
| `docs/slovicka/README.md` | tento dokument |
| `01-instrukce-projektu.md` | doslovné instrukce claude.ai projektu (role, formát karet, pravidla) |
| `02-canolradd-rozcestnik.md` | mapa učebnice: soubory, strany, gramatika, kde hledat věty; rozsahy id po lekcích |
| `03-canolradd-varianty.md` | převodní tabulka jih → sever (schválené tvary) |
| `mnemo/decks/cy-canolradd-01.json` … `-40.json` | všech 899 karet (zdroj pravdy pro data) |
| `canolradd-namluveni.csv` | seznam k namluvení (soubor;text) vygenerovaný 26. 11. 2026 z aktuálních balíčků; jen přehled, aplikace má vlastní klipy v `audio/` |

**Není tu (a proč):** PDF učebnice (má je uživatel, autorská práva); `canolradd-geirfa.md` (813 položek vytažených
z rámečků Geirfa: vše je už v kartách, rod a druh v nich odpovídá barvám knihy); 40 recenzních zpráv
`claude/recenze/*.md` (historie, opravy jsou v balíčcích); kód aplikace a 4208 nahrávek (jsou na GitHubu);
podpisové klíče APK (jen v předávacím ZIPu u uživatele a v GitHub Secrets; nikdy je nedávej do repozitáře ani AI).

## 4. Závazná rozhodnutí uživatele (nepřepisovat bez jeho souhlasu)

- Jižní hovorová velština je hlavní; severní jen v `varianty.sever`. Spisovná jen na výslovný pokyn.
- **Rámeček arall:** víceslovné položky (i podstatná jména jako cyfnod clo, ffurflen gais, drws ffrynt) = "ostatni"
  (fialová), idiomy a ustálená spojení = "fraze" (oranžová). Rod a plurál jen v `extra.pozn` („rod m podle cyfnod; pl. …“).
  Položky z barevných rámečků (m/f) zůstávají podstatnými jmény.
- **dydy v učebnicových větách:** v hlavní větě jižní dyw, dydy do severní varianty („tvar učebnice, s. X“).
- Schválené severní tvary mimo učebnici: bant → i ffwrdd, gartre → adra, ces i → ges i, i fi → i mi, dweud → deud,
  'te → 'ta, cwrdd → cyfarfod, edrych → sbio (jen „dívat se na“), twymo → cynhesu, lawr llawr → lawr grisiau,
  Mae … gyda ni → Mae gynnon ni …
- Faswn/fyswn, fasat/fysat se nepřevádějí. Nejistý severní tvar = žádná varianta.
- Rod tin (0098) a economi (0399) zůstává podle učebnice (m) s "overit".
- Severní varianty v aplikaci namlouvá severní mužský hlas, jižní text ženský hlas.
- Aplikace: v „Lost property“ se nepíše, jen vybírá; Mnemo produkce se píše. Y Drôr Cardiau zrušené (nahradil ho Mnemo).
  Anglická aplikace nesmí obsahovat žádnou češtinu.
- Nikdy nepoužívat věty z pracovních listů (Taflen Waith); příklady z učebnice jsou v pořádku.
- Nikdy neztratit uložený postup: id karet se nemění, karty se nemažou, změna ukládaných dat potřebuje migraci.

## 5. Kde se instrukce projektu rozcházejí se skutečností

1. **„Motor engine.html v projektu, společný s Korejštinou“** v projektu není. Skutečný motor pro tyto balíčky je
   sekce Mnemo Hooks v aplikaci Gorsaf (`mnemo/mnemo.js`, `mnemo/mnemo.css`, sestavení `mnemo/mnemo_build.py`).
   Korejská obdoba je samostatná aplikace Gamgol (repozitář `tvspk/gamgol`).
2. **Zvuk:** instrukce počítají se soubory `audio/<id>.mp3`. Aplikace ve skutečnosti nahrává hlasem Piper CY-EN
   (Bangor University, CC BY 4.0) přes `audio/make_audio.py` a ukládá klipy pod vlastními klíči (`audio/<klíč>.mp3`,
   balíky m1–m20 pro Mnemo). Všech 899 slov + příkladů + 168 severních variant je namluveno (13. 11. 2026, z aktuálních
   textů). Seznam `canolradd-namluveni.csv` slouží jen jako přehled / pro jiný přehrávač.
3. **Úspora tokenů / „jeden chat = jedna lekce“** platí pro claude.ai; v jiné AI je to jen doporučení.
4. Pravidlo „Po každé schválené dávce uprav rozcestník v projektu“: mimo claude.ai uprav
   `docs/slovicka/02-canolradd-rozcestnik.md` (poslední id) a commitni.

## 6. Mnemotechnika s barvou rodu (motivy)

Ženský rod = žár/červená, mužský = chlad/modrá; v jedné lekci se motiv neopakuje; obraz nesmí zopakovat scénu jiné
karty (např. tagfa 0594 = zácpa + hasičské auto). Rod m/f = bez barvy.
- 🔵 m: rampouch · jinovatka · sněhulák · iglú · tučňák · lední medvěd · mrazák · kroupy · ledovec · hluboké moře ·
  obloha · chladicí vložka · kontejner na papír · gumová rukavice · borůvky · džíny · námořnická uniforma ·
  modrý inkoust · safír · sněhová vločka (modrý led jen výjimečně). **Chrpa je vyřazená.**
- 🔴 f: plameny · žhavé uhlí · láva/sopka · krb · pec/výheň · svíčka · drak chrlící oheň · chilli · rajče · jahody ·
  mák · růže · rtěnka · hasičské auto · červený koberec · jiskry · rozpálená plotna (rudý jen jako jeden z motivů).
- Nejméně použité (vhodné pro další úpravy): 🔵 kroupy, obloha, námořnická uniforma, modrý inkoust; 🔴 jahody, chilli,
  rozpálená plotna, žhavé uhlí.

## 7. Otevřené body

- **27 karet s "overit": true** (velština k ověření rodilým mluvčím nebo v PDF): 0098 tin, 0108, 0172 nifer, 0212,
  0226, 0258, 0265, 0275, 0290, 0357, 0399 economi, 0411 gwau, 0472, 0589, 0593 nyth, 0616 gweini, 0618, 0659, 0663 cnoi,
  0731 amrywiaeth, 0808, 0835 cyffroi, 0860 siom, 0878, 0887, 0891 cais, 0896 cenllysg. (V anglických balíčcích jsou 0212,
  0275, 0411 už vyřešené.) Změna velšského textu = nová nahrávka.
- Navržené, **neschválené** severní tvary: llond bol (u llond bola 0189), deffro (u dihuno 0384), 'dan ni (u 'dyn ni 0423).
- Česká aplikace: oprava vyhodnocení hesel s předložkou v závorce („codi ofn (ar)“ ← „codi ofn“) je zatím jen v EN
  aplikaci; do české se dostane s její příští skutečnou změnou (pak znovu `mnemo/inject.py`, build, APK ≥ 17).
- Česká aplikace a artefakt nemají změny 3.12/3.13 (zvuky, rychlost hlasu), dokud se znovu nesestaví.
- Velština ani anglické mnemotechniky nebyly zkontrolovány rodilým mluvčím.

## 8. Běžné úkoly a jak na ně

- **Zkoušení v chatu („zkoušej“):** po jednom slově, aktivní vybavování; zmutovaný tvar uznat, pokud sedí kontextu;
  alternativu a severní tvar uznat a připomenout jižní; u "m/f" uznat oba rody; na konci shrnout chyby.
- **Oprava karty:** vrátit jen změněné karty (celé objekty, stejné id); celý balíček se zvýšenou "verze" až na pokyn
  „finální“. Do aplikace: nahradit `mnemo/decks/cy-canolradd-NN.json`; jde-li o anglické texty, upravit
  `mnemo/en-src/NN.txt` a `python3 -I mnemo/merge_en.py …` (návod v HANDOFF §000); pak
  `python3 -I mnemo/make_en.py`, `python3 -I scripts/build_web.py`, testy `python3 tools/run_checks.py
  game-en/gorsaf-abercastell-en.html`; zvýšit `apk/verze-en.txt` (versionCode +1, název X.Y-en) a pushnout na `main`.
  Změnil-li se velšský text, je potřeba nová nahrávka (hlasový model, HANDOFF §6.3).
- **Nová úroveň (např. Uwch):** nové balíčky s novou předponou id (`cy-uwch-0001`), stejný formát; před tvorbou
  kontrola duplicit proti Canolradd; dávky max. 30 karet; ke každé dávce seznam k namluvení.

## 9. Bezpečnost a co nikdy nedělat

- Repozitář `tvspk/gorsaf` je **veřejný**: žádná osobní data, žádné klíče, hesla, tokeny, párovací kódy ani zálohové
  kódy `GORSAF1.…`.
- Podepisovat EN aplikaci jen klíčem `gorsaf-en.jks` (alias `gorsafen`, certifikát SHA-256 89e9d208…e136c2);
  jiný klíč = aktualizace se nenainstaluje a uživatel přijde o postup.
- Nespouštět `make_audio.py all --prune` bez kontroly, že všechny klíče Mnemo zůstávají v `AUDIO_INDEX`.
- Netestovat proti skutečnému GitHub API synchronizace (testy mají falešný GitHub).
- Uživatel není programátor: kroky na GitHubu nebo v telefonu po jednom, přesně kam kliknout, a počkat na „hotovo“.
  Vždy říct, co bylo ověřeno a co ne.
