"""merge_en.py deck.json en.txt out.json
en.txt: card lines  NNNN|meaning|example translation|hook   (hook may be empty)
        option lines  +key=value  (cu, pozn, rod_pozn, puvod, kmen, alt, ov, s.pozn, s.exc; alt = extra accepted Welsh answers, comma-separated, added to the deck's alternativy;
        ov=0 clears the 'to check' flag (overit) after the point was checked in the EN review) apply to the previous card."""
import json,sys,re
TEMA={'obecné':'general','komunikace':'communication','tělo a zdraví':'body and health','práce':'work',
'příroda a počasí':'nature and weather','vlastnosti a popis':'qualities and description','kultura a zábava':'culture and leisure',
'kriminalita a nehody':'crime and accidents','společnost a politika':'society and politics','domov':'home',
'čas a čísla':'time and numbers','lidé a vztahy':'people and relationships','pocity':'feelings','místa':'places',
'sport':'sport','cestování a doprava':'travel and transport','jídlo':'food','obchod a peníze':'shopping and money',
'vzdělání a věda':'education and science','média':'media','oblečení':'clothes','jazyk':'language'}
PUV={'anglický':'English','latinský':'Latin'}
CZ=re.compile(r'[ěščřžůťďňĚŠČŘŽŮ]|\b(nebo|místo|jen|také|osoba|jako|ženský|mužský|rod|pojí|učebnic\w*|sever:|sloveso|škola|nepravideln\w*|viz)\b')
src,txt,out=sys.argv[1:4]
d=json.load(open(src));by={c['id'][-4:]:c for c in d['karty']}
en={};cur=None
for ln in open(txt,encoding='utf-8'):
    ln=ln.rstrip('\n')
    if not ln.strip() or ln.startswith('#'):continue
    if ln.startswith('+'):
        k,v=ln[1:].split('=',1);en[cur][k.strip()]=v.strip();continue
    p=ln.split('|');assert len(p)==4,ln
    cur=p[0];en[cur]={'cs':p[1],'exc':p[2],'hook':p[3]}
err=[]
for i,c in by.items():
    if c['vyrazeno']:continue
    if i not in en:err.append('missing '+i);continue
    e=en.pop(i);x=c['extra']
    c['cs']=e['cs'];old_exc=c['priklad_cs'];c['priklad_cs']=e['exc'];c['mnemo']=e['hook']
    for k,v in e.items():
        if k.startswith('fam'):c['rodina'][int(k[3:])]=v
    for j,r in enumerate(c['rodina']):
        if re.search(r'[(=]',r) and 'fam%d'%j not in e:err.append(f'{i} check +fam{j}= {r}')
    c.pop('en',None);c['tema']=TEMA[c['tema']]
    if 'cs_upresneni' in c:
        if 'cu' in e:c['cs_upresneni']=e['cu']
        else:err.append(i+' needs +cu')
    for k in('pozn','rod_pozn'):
        if k in x:
            if k in e:x[k]=e[k]
            else:err.append(f'{i} needs +{k}')
    if 'kmen' in e:x['kmen']=e['kmen']
    if e.get('ov')=='0':c['overit']=False
    if 'alt' in e:c['alternativy']=list(dict.fromkeys((c.get('alternativy') or [])+[a.strip() for a in e['alt'].split(',') if a.strip()]))
    if 'puvod' in x:x['puvod']=e.get('puvod',PUV.get(x['puvod'],x['puvod']))
    s=c.get('varianty',{}).get('sever')
    if s:
        if 'priklad_cs' in s:
            if s['priklad_cs']==old_exc and 's.exc' not in e:s['priklad_cs']=e['exc']
            elif 's.exc' in e:s['priklad_cs']=e['s.exc']
            else:err.append(i+' needs +s.exc')
        if 'pozn' in s:
            if 's.pozn' in e:s['pozn']=e['s.pozn']
            else:err.append(i+' needs +s.pozn')
err+=['unknown id '+k for k in en]
d['vyklad']='en-GB'
def vals(o):
    if isinstance(o,dict):
        for k,v in o.items():
            if k!='slovni_druh':yield from vals(v)
    elif isinstance(o,list):
        for v in o:yield from vals(v)
    elif isinstance(o,str):yield o
for v in vals(d):
    if CZ.search(v):err.append('czech? '+v)
if err:print('\n'.join(err));sys.exit(1)
with open(out,'w',encoding='utf-8') as f:
    f.write('{'+json.dumps({k:v for k,v in d.items() if k!='karty'},ensure_ascii=False)[1:-1]+',"karty":[\n'
            +',\n'.join(json.dumps(c,ensure_ascii=False) for c in d['karty'])+'\n]}\n')
print('OK',out,len(d['karty']))
