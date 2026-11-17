#!/usr/bin/env python3
"""Mnemo Hooks: put mnemo/mnemo.js and mnemo/mnemo.css into the game and wire it in (idempotent).

Usage: python3 mnemo/inject.py [game.html]     (then python3 mnemo/mnemo_build.py for the data)
The code lives between /*MNEMO-JS*/…/*MNEMO-JS-END*/ and /*MNEMO-CSS*/…/*MNEMO-CSS-END*/; re-running replaces it.
The small hooks into the engine (PATCHES) are applied once; each must match exactly once, or the script stops.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
GAME = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', 'game', 'gorsaf-abercastell.html')

# (marker that shows the patch is in, old text, new text)
PATCHES = [
    # 1. a Mnemo Hooks drawer in every unit (and the exam unit), after the flashcard drawer
    ("body.append(k)}\n    if(DATA.news&&DATA.news[u]){const L=DATA.news[u],rd=",
     "body.append(k)}\n    {const mb=mnDrawerBtn(u);if(mb)body.append(mb)}\n    if(DATA.news&&DATA.news[u]){const L=DATA.news[u],rd=",
     "{const mb=mnDrawerBtn(u);if(mb)body.append(mb)}"),
    # 2. all words, at the end of the unit list (before "Any time")
    ("{const cur=units.find(u=>!uDone(u));if(cur)setOpen(String(cur),true)}\n  list.append(h('p','sub','Any time'));",
     "{const cur=units.find(u=>!uDone(u));if(cur)setOpen(String(cur),true)}\n  {const ma=mnAllBtn();if(ma)list.append(ma)}\n  list.append(h('p','sub','Any time'));",
     "{const ma=mnAllBtn();if(ma)list.append(ma)}"),
    # 3. load the Mnemo document next to the main save
    ("const id=await user.id();if(!id)return;const ref=db.doc('data/users/'+id+'/save');",
     "const id=await user.id();if(!id)return;await mhInit(db,id);const ref=db.doc('data/users/'+id+'/save');",
     "await mhInit(db,id);"),
    # 4. backup code carries Mnemo progress (field mh; the main save document does not)
    ("function encodeSave(){const d=snapshot();d.at=today();",
     "function encodeSave(){const d=snapshot();if(S.mh&&Object.keys(S.mh.c||{}).length)d.mh=S.mh;d.at=today();",
     "if(S.mh&&Object.keys(S.mh.c||{}).length)d.mh=S.mh;"),
    # 5. restore: a code with mh replaces Mnemo progress; a code without it leaves Mnemo progress alone
    ("S.reads=d.reads&&typeof d.reads==='object'?d.reads:{};",
     "S.reads=d.reads&&typeof d.reads==='object'?d.reads:{};if(d.mh&&typeof d.mh==='object'&&d.mh.c&&typeof d.mh.c==='object')S.mh={c:d.mh.c};",
     "if(d.mh&&typeof d.mh==='object'&&d.mh.c"),
    ("go.onclick=()=>{applySave(d);if(isDay(d.at))S.lastBackup=d.at;save();",
     "go.onclick=()=>{applySave(d);if(isDay(d.at))S.lastBackup=d.at;save();mhSave();",
     "save();mhSave();paintCredQuiet();home()};out.append(go)"),
    ("<b>${kn}</b> cards known both ways.",
     "<b>${kn}</b> cards known both ways${d.mh&&d.mh.c?`, <b>${Object.keys(d.mh.c).filter(x=>/r$/.test(x)).length}</b> Mnemo Hooks words started`:''}.",
     "Mnemo Hooks words started"),
    # 6. "Reset progress" wipes Mnemo progress too
    ("S.reads={};save();paintCredQuiet();home()}}))};",
     "S.reads={};S.mh={c:{}};save();mhSave();paintCredQuiet();home()}}))};",
     "S.mh={c:{}};save();mhSave();"),
    # 7. leaving a screen stops a Mnemo sheet left open
    ("function show(...nodes){audStop();",
     "function show(...nodes){audStop();{const p=$('#mhpeek');if(p){p.hidden=true;p.innerHTML=''}}",
     "{const p=$('#mhpeek');if(p){p.hidden=true;p.innerHTML=''}}"),
]


def main():
    html = open(GAME, encoding='utf-8').read()
    js = open(os.path.join(HERE, 'mnemo.js'), encoding='utf-8').read().strip()
    css = open(os.path.join(HERE, 'mnemo.css'), encoding='utf-8').read().strip()
    jsb, cssb = '/*MNEMO-JS*/\n' + js + '\n/*MNEMO-JS-END*/', '/*MNEMO-CSS*/\n' + css + '\n/*MNEMO-CSS-END*/'
    if '/*MNEMO-JS*/' in html:
        html = re.sub(r'/\*MNEMO-JS\*/.*?/\*MNEMO-JS-END\*/', lambda _: jsb, html, flags=re.S)
    else:
        i = html.index('const newsAll=')
        html = html[:i] + jsb + '\n' + html[i:]
    if '/*MNEMO-CSS*/' in html:
        html = re.sub(r'/\*MNEMO-CSS\*/.*?/\*MNEMO-CSS-END\*/', lambda _: cssb, html, flags=re.S)
    else:
        i = html.index('</style>')
        html = html[:i] + cssb + '\n' + html[i:]
    for old, new, mark in PATCHES:
        if mark in html:
            continue
        n = html.count(old)
        if n != 1:
            sys.exit(f'patch does not match exactly once ({n}x): {old[:70]}…')
        html = html.replace(old, new)
    open(GAME, 'w', encoding='utf-8').write(html)
    print('Mnemo Hooks code in place')


if __name__ == '__main__':
    main()
