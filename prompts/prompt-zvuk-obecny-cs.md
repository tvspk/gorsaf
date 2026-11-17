# ZADÁNÍ: Zvuk pro jazykovou hru (artefakt + Android aplikace)

Místa v [závorkách] doplň. Vychází z postupu u velšské hry Gorsaf Abercastell (říjen 2026).

Mám jazykovou hru v jednom HTML souboru, publikovanou jako artefakt (a případně jako aplikaci pro Android). Chci do ní přidat namluvené věty v jazyce [jazyk, varianta]. Postupuj takhle:

## 1. Hlas
- Použij hlasový model, který běží přímo u tebe v pracovním prostředí, ne placenou online službu. Pro velštinu jsme použili Piper CY-EN z Bangorské univerzity se slovníkem výslovnosti techiaith-g2p, spouštěný přes onnxruntime.
- Pro [jazyk] najdi nejlepší dostupný otevřený model. Řekni mi, odkud ho stáhnout: z pracovního prostředí se na Hugging Face obvykle nedostaneš, takže soubory .onnx a .onnx.json ti nahraju do chatu.
- Ověř, že model je pro daný jazyk opravdu dobrý. Modely, které čtou podle obecných pravidel bez slovníku výslovnosti, bývají slabé.
- Hlasy podle rolí: vyprávění, správné odpovědi a ženské postavy dělá jeden hlas, mužské postavy druhý. Pokud to model umí, drž se jedné nářeční varianty, té, kterou se učím.
- Rychlost mírně pomalejší než přirozená (u nás length_scale 1.08).
- Licence: do hry patří poděkování autorům hlasu, pokud ho licence vyžaduje.

## 2. Co nahrát
- Výpis vět, které se mají nahrát, vytváří kód hry sám, ze stejné funkce, kterou používá i přehrávání. Názvy nahrávek tak vždycky sedí.
- Nahrávají se: vyprávění, věty případů, články, slovíčka a fráze na kartičkách a příklady ke kartičkám.
- U podstatných jmen na kartičkách jen základní tvar, bez členu. Zkoušeli jsme i dvojici „tvar … tvar se členem“, ale zůstali jsme u jednoduchého tvaru.
- Klíč nahrávky = hlas + text, zahashovaný (u nás FNV-1a). Stejná věta se nahraje jen jednou.

## 3. Nahrávací skript
- Nahrává jen chybějící nahrávky a existující nikdy nepřepíše. Ručně vybraný pokus tak přežije i příští přegenerování.
- Formát: MP3 mono, 48 kbit/s, ořezané ticho na začátku, 0,15 s ticha na konci.
- Výstup: jednotlivé MP3 pro aplikaci a „balíky“ pro artefakt, tedy MP3 spojené za sebou po lekcích. Případy a články jsou v balících u1–uN, kartičky v k1–kN. Do hry se zapíše rejstřík {klíč: [balík, posun, délka]}.
- Hra si balík stáhne až při prvním přehrání a nahrávku z něj vyřízne. Balíky kartiček se stahují, jen když si kartičku pustím.
- Přípona balíků musí být .mp3. Soubory .bin artefakt nevydá.
- Přidej i skript, který z balíků obnoví jednotlivé nahrávky, protože ZIP se zvuky by byl moc velký.

## 4. Kontrola kvality
- Model u každého nahrání zní trochu jinak, takže špatnou nahrávku často spraví nový pokus. U sporných nahrávek mi pošli 2–3 pokusy, vyberu si a vybraný pokus nahradí původní soubor.
- Samostatná slova bez kontextu může slovník výslovnosti vzít jako angličtinu. U nás to byly „dawn“ a „man“. Najdi všechny takové případy a u slov, která nejsou přejatá, vynuť správný jazyk.
- Udělej mi poslechovou stránku: samostatný artefakt se všemi nahrávkami, filtrem podle lekce a druhu, přehráváním jedné po druhé a tlačítkem „Nahlásit“ s poznámkou. Nahlášení ukládej do úložiště artefaktu (capabilities db a user), abys je mohl přečíst, když napíšu „oprav nahlášené“.
- Délku nahrávek vůči počtu hlásek můžeš použít jako rychlý test na useknuté nebo zdeformované nahrávky. Špatnou výslovnost ale neodhalí.

## 5. Publikování a limity
- Hlavní hru publikuj jednou: HTML plus jen ty balíky, které se změnily. Soubory, které nepošleš, zůstanou.
- Limity: soubor, který mi pošleš, má nejvýš 30 MB; jedno publikování nejvýš 64 MB a 255 souborů; jeden soubor v artefaktu nejvýš 16 MB.
- Aplikace pro Android: stejné HTML ve WebView a jednotlivé MP3 v aplikaci. Pokud bude nad 30 MB, rozděl ji na dvě části a napiš mi příkaz pro Windows `cmd /c copy /b x.apk.part00+x.apk.part01 x.apk`. Pro kontrolu přidej začátek otisku SHA-256.
- Podpisový klíč aplikace vytvoř jen jednou a dej mi ho, protože bez něj se nová verze nenainstaluje přes starou. Číslo verze se musí pokaždé zvýšit.

## 6. Jak se mnou pracovat
- Odpovídej česky, stručně, a vždycky napiš, co jsi ověřil a co ne. Nahrávky sám neslyšíš, takže kvalitu musím posoudit já.
- Šetři tokeny: velký soubor hry nečti celý, testuj jednou a publikuj jednou.
- Všechno zapisuj do HANDOFF.md (jak to funguje, rozhodnutí, ručně vybrané nahrávky), aby mohl pokračovat jiný chat.

Než začneš, navrhni hlasový model a řekni mi, jaké soubory ti mám poslat. Pak nahraj zkušebně jednu lekci, já si ji poslechnu, a teprve potom nahraj zbytek.
