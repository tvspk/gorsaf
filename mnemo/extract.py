import json,sys
d=json.load(open(sys.argv[1]))
print(d['zdroj'])
for c in d['karty']:
    if c['vyrazeno']: continue
    e=c['extra']
    row=[c['id'][-4:],c['slovo'],c['slovni_druh']+('/'+e['rod'] if e.get('rod') else ''),c['en'],c['cs'],c['priklad'],c['priklad_cs'],c['mnemo']]
    ex={k:v for k,v in e.items() if k in('pozn','puvod','rod_pozn','tvary','zensky_tvar')}
    if c.get('cs_upresneni'): ex['cs_upr']=c['cs_upresneni']
    for j,r in enumerate(c['rodina']):
        if '(' in r or '=' in r:ex['fam%d'%j]=r
    if 'varianty' in c: ex['sever']=c['varianty']['sever']
    print('|'.join(map(str,row)),json.dumps(ex,ensure_ascii=False) if ex else '')
