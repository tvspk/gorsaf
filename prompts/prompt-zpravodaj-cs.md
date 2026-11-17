Přečti si nejdřív HANDOFF.md (je závazný) a pak přidej do hry Gorsaf Abercastell čtecí sekci
„Y Papur Bro“ (zpravodaj stanice) podle těchto pravidel. Hra si musí zachovat svou tvář a atmosféru:
nic stávajícího nepřestavuj, jen přidávej.

APLIKACE: Gorsaf Abercastell, učení velštiny podle kurzu Dysgu Cymraeg Canolradd (South),
19 kapitol (Uned 1–19) + zkoušková kapitola. Zpravodaj jen pro Uned 1–19.
SVĚT: obyčejná přepážka místního úřadu na orbitální vesmírné stanici. Zpravodaj „Y papur bro“
ve hře už existuje (jeden list, velmi formální, strčený pod každé dveře): navaž na něj.
Autoři = stálé obsazení hry. Než začneš, přečti si v DATA, jak jednotlivé postavy mluví a co
dělají, a drž se toho (Swyddog Rhiannon Llwyd a její clipboard, Mr Caradog a jeho pórky, Mr Puw s dílnou
a názory, Mrs Gwen Prydderch, Mr Ifan, Mr Hopcyn a jeho pět příbuzných, Heulwen Haf a její
„Bydd hi'n sych heddiw“, Sam, Ms Lewis, Y Pennaeth…). Nové stálé postavy nevymýšlej, kromě jedné:
OPAKOVANÁ FIGURKA: ovce (dafad), která se jednoho dne objevila na palubě stanice. Nikdo neví, čí je
ani jak se tam dostala, a nikdo to nikdy nevysvětlí. Objevuje se skoro v každém fejetonu, obvykle
jen jednou větou a jako samozřejmost. Jméno jí navrhni v první odpovědi (3 možnosti, vyberu si).
JAZYK ROZHRANÍ: angličtina. Text fejetonu jen velsky. Jižní varianta kurzu (dw i, nawr, mas,
gyda, moyn…); severní tvary jen u postavy, která tak ve hře už mluví, a označit.

OBSAH
- Ke každé kapitole 2 fejetony ze zpravodaje. Každý píše jiná postava ze stálého obsazení,
  autoři se mezi kapitolami střídají (nikdo dvakrát po sobě).
- 8–12 krátkých vět.
- Jen gramatika a slovíčka této kapitoly a všech předchozích (DATA.words[1..N] + co už ve hře
  zaznělo v kapitolách 1..N). Aspoň dvě gramatická témata kapitoly (DATA.unitTags[N]) se v textu
  musí objevit přirozeně; která to jsou, napiš do dat (pole tags).
- Nejvýš 6 slov mimo látku. Každé označ {tvar|lemma} (tvar = jak stojí ve větě, i zmutovaný;
  lemma = základní tvar bez mutace) a dej mu anglický překlad do gloss. Víc slov mimo látku =
  větu přepiš.
- Zdvořilost a styl odpovídají autorovi a žánru (sloupek, chat mezi kamarády, lístek na dveřích,
  oznámení, poradna, recenze, zápis ze schůze). Téma vychází z tématu kapitoly.
- Nikdy nepoužívej věty ani odpovědi z pracovních listů (Taflen Waith); neopakuj věty, které už
  ve hře jsou. Příklady z učebnice jsou v pořádku. Učebnici a pracovní list ti k dané kapitole pošlu.

HUMOR
- Suchý, s kamennou tváří, britský. Text nikdy neříká, že je vtipný.
- Fejeton běží vážně a poslední věta ho shodí.
- Logika dotlačená do absurdna, malý svět braný úplně vážně (stejně jako zbytek hry).
- Pointa má stát na gramatice nebo slovíčku kapitoly: kdo mu nerozumí, vtip nepochopí.
- Hodný humor: smějeme se situacím, ne lidem. Žádní záporáci.
- Stejný suchý hlas mají i anglické úvody, vysvětlení a hlášky (jako vypravěč hry).

OTÁZKY (anglicky)
- Přesně 3, v pořadí textu: 1) fakt, 2) důvod / vztah mezi větami, 3) pointa nebo závěr.
  Hodí se dopočítávací otázka („four relatives, three on Earth: how many in the cabin?“).
- 4 možnosti, správná v datech vždy první (hra míchá). Špatné možnosti používají skutečné údaje
  z textu na špatném místě. Jedna smí být absurdní. Podobná délka možností.
- why: citace věty z textu + krátké vysvětlení klíčového slova nebo gramatiky + suchá poznámka.
  1–3 věty, nikdy poučující.

DATA (uvnitř stávajícího bloku DATA, odděleně od logiky; žádné nové soubory)
DATA.news = { 1: [fejeton, fejeton], 2: […], … }, fejeton:
{ id, unit, title, by, byEn, genre, tags: [tag, tag], chat?, intro,
  text: [[věta, anglický překlad, mluvčí?], …],
  gloss: { lemma: "English meaning" },
  qs: [{ ask, opts: [správná, špatná, špatná, špatná], why } × 3],
  clip: { tag: název, name: "Clipping: Y Papur Bro, Uned N", line: jedna suchá věta } }
(mluvčí jen u chatu. Zvuk zatím NE, ale data drž tak, aby šel později doplnit stávajícím
systémem z HANDOFF §6: mluvčí/autor jednoznačně určený.)

CHOVÁNÍ
- Vstup: v každé kapitole na domovské obrazovce (vedle Lost property a kartiček) položka
  „Y Papur Bro“. Otevřená hned, bez ohledu na postup, stejně jako kartičky.
- Seznam: číslo, název, autor, stav („unread“ / „2 of 3“ / „3 of 3“).
- Čtení: intro (anglicky, hlasem vypravěče), fejeton jako list zpravodaje na papíru
  (stávající papírové tokeny --paper/--paperink: hlavička „Y Papur Bro · Rhifyn N“, název, podpis,
  souvislý text, velké písmo), pod ním jedna otázka. Text zůstává vidět.
- Označená slova: tečkované podtržení, ťuknutí otevře lištu s překladem (lemma → gloss).
- Po odpovědi: zamknout možnosti, ukázat správnou/špatnou, razítko Cywir/Anghywir
  (stávající .stamp), krátkou hlášku a why.
- Závěr: skóre, suchá hláška podle výsledku (3 / 1–2 / 0), odměna v credydau jen při prvním
  čtení (stejná logika jako jinde: jen za správné odpovědi), výstřižek do sbírky v kajutě
  (nástěnka s výstřižky, v sekci bonus), celý text větu po větě s překladem.
- Uložit S.reads[id] = { best, at }. Přidat do snapshot() a do applySave() s výchozí hodnotou {}
  (staré uložení se nesmí ztratit; záloha/obnova to pak nese automaticky).
- Mobil 360–390 px bez vodorovného posouvání; vše ve stávajícím vizuálním stylu.

KONTROLA
Napiš skript (Node, načte DATA ze hry stejně jako audio/make_audio.py), který ověří:
jedinečná id; 2 fejetony na kapitolu; každé {…|lemma} má gloss a naopak; 3 otázky × 4 různé
možnosti; 8–12 vět; tags patří do DATA.unitTags[N]; autor se neopakuje dvakrát po sobě; v textu
nejsou neoznačená anglická slova. A vypíše slova, která nejsou ve slovíčkách kapitol 1–N, v textech
kapitol 1–N ani v gloss; před porovnáním zkus odmutovat počáteční hlásku (měkká, nosová,
přídechová mutace, h- před samohláskou). Pak jazyková korektura (mutace, rod, předložky,
jižní tvary) a zkouška na šířce telefonu, konzole bez chyb.

POSTUP (šetři tokeny)
1. Postav sekci a Uned 1. Nejdřív mi ukaž návrh jmen pro ovci a obě pointy jednou větou anglicky
   (s autorem a žánrem), až potom piš texty. Kód sekce piš jen jednou; velký soubor hry nečti celý,
   hledej v něm (grep) a obsah vkládej skriptem. Publikuj, ať vidím vzhled; doladíme ho.
2. Další kapitoly budou chodit v dávkách (3–5 kapitol, s PDF učebnice a pracovními listy).
   Pointy celé dávky mi ukaž najednou v jedné zprávě, po schválení napiš všechny texty dávky,
   proveď kontrolu skriptem a publikuj jednou za dávku. Odpovídej stručně.
3. Po každé dávce aktualizuj HANDOFF.md (stav: které kapitoly zpravodaj má) a připrav nový ZIP
   balíčku, abych mohl pokračovat v novém chatu.
