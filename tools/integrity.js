// Data and generator integrity check for a Gorsaf-engine game (run by run_checks.py, in the page)
()=>{const P=[],add=(k,m)=>{P.push(k+': '+m)};const lc=s=>String(s).toLowerCase().trim();
const tagOK=t=>t&&DATA.tags[t];
// 1 chapters
const ids=new Set();DATA.chapters.forEach((c,ci)=>{if(ids.has(c.id))add('dupId',c.id);ids.add(c.id);if(!DATA.units[c.unit]&&c.unit!==20)add('unit',c.id);
  for(const [k] of c.rush)if(!GEN[k])add('rushGen',c.id+' '+k);
  [...c.story,...c.puzzle].forEach((ex,i)=>{const w=`${c.id}#${i}`;
    if(ex.t!=='narr'&&!tagOK(ex.tag))add('noTag',w+' tag='+ex.tag+' t='+ex.t);
    if(ex.t==='mc'){if(!ex.opts||ex.opts.length<2)add('mcOpts',w);const s=new Set(ex.opts.map(lc));if(s.size!==ex.opts.length)add('mcDup',w+' '+JSON.stringify(ex.opts));if(ex.opts.some(o=>/[<&]/.test(o)))add('mcHtml',w+' '+JSON.stringify(ex.opts));if(!ex.why)add('noWhy',w)}
    if(ex.t==='type'){if(!ex.answers||!ex.answers.length||ex.answers.some(a=>!String(a).trim()))add('typeAns',w);if(!ex.why)add('noWhy',w)}
    if(ex.t==='build'){if(!ex.answer)add('build',w);if(/\s{2,}/.test(ex.answer))add('buildSpaces',w);const ws=ex.answer.split(' ');if((ex.extra||[]).some(x=>ws.includes(x)))add('buildExtraInAnswer',w+' '+ex.extra);if(!ex.why)add('noWhy',w)}
    if(ex.t==='match'){const L=ex.pairs.map(p=>p[0]),R=ex.pairs.map(p=>p[1]);if(new Set(L).size!==L.length)add('matchDupL',w);if(new Set(R).size!==R.length)add('matchDupR',w);if([...L,...R].some(o=>/[<&]/.test(o)))add('matchHtml',w)}
    if(!['narr','mc','type','build','match'].includes(ex.t))add('type?',w+' '+ex.t)})});
// 2 bank
for(const [t,arr] of Object.entries(DATA.bank)){if(!DATA.tags[t])add('bankTag',t);arr.forEach((ex,i)=>{const w=`bank ${t}#${i}`;
  if(ex.t==='mc'){const s=new Set(ex.opts.map(lc));if(s.size!==ex.opts.length)add('mcDup',w+' '+JSON.stringify(ex.opts));if(ex.opts.some(o=>/[<&]/.test(o)))add('mcHtml',w)}
  if(ex.t==='type'&&(!ex.answers||!ex.answers.length))add('typeAns',w);if(ex.t==='build'&&!ex.answer)add('build',w);if(!ex.why)add('noWhy',w);if(ex.tag&&!DATA.tags[ex.tag])add('bankItemTag',w+' '+ex.tag)})}
// 3 unitTags
for(const [u,ts] of Object.entries(DATA.unitTags))for(const t of ts)if(!DATA.tags[t])add('unitTag',u+' '+t);
// tags without bank used in review
// 4 generators fuzz
const gstat={};const all={...GEN};TREIG.forEach((t,i)=>{all['tr'+i]=t[2]});
S.done=new Set(DATA.chapters.map(c=>c.id));
for(const [k,g] of Object.entries(all)){let errs=0,dup=0,miss=0,bad=0,html=0,notag=0,few=0,ex1='';for(let n=0;n<1500;n++){let q;try{q=g()}catch(e){errs++;ex1=ex1||String(e);continue}
  if(!q||!q.opts){bad++;continue}if(q.opts.length<3)few++;const s=new Set(q.opts.map(x=>lc(x)));if(s.size!==q.opts.length){dup++;if(!ex1)ex1='DUP '+JSON.stringify([q.q,q.opts])}
  if(q.opts.some(o=>o==null||/undefined|NaN/.test(String(o)))||/undefined|NaN/.test(q.q+q.why)){miss++;if(!ex1)ex1='UNDEF '+JSON.stringify([q.q,q.opts,q.why])}
  if(q.opts.some(o=>/[<&]/.test(String(o))))html++;if(!tagOK(q.tag))notag++}
  if(errs||dup||miss||bad||html||notag||few)gstat[k]={errs,dup,miss,bad,html,notag,few,ex1:ex1.slice(0,300)}}
// 5 wordQ all units/types
const wq={};for(const u of Object.keys(DATA.words)){for(let n=0;n<600;n++){const q=wordQ(+u,true);if(q.t!=='mc')continue;const s=new Set(q.opts.map(lc));if(s.size!==q.opts.length){wq[u]=(wq[u]||[]);if(wq[u].length<3)wq[u].push(q.opts)}}
  for(let n=0;n<200;n++){const ws=DATA.words[u].filter(genderable);if(!ws.length)break;const q=wordQ(+u,false,8);const s=new Set(q.opts.map(lc));if(s.size!==q.opts.length){wq['g'+u]=(wq['g'+u]||[]);if(wq['g'+u].length<3)wq['g'+u].push(q.opts)}}}
// 6 orderSet sizes
R={maint:true};const os={};for(const m of DATA.station){const units=m.u?[m.u]:null;let mn=9;for(let n=0;n<40;n++){mn=Math.min(mn,orderSet(units).length)}if(mn<3)os[m.id]=mn}
for(const u of Object.keys(DATA.unitTags)){let mn=9;for(let n=0;n<40;n++)mn=Math.min(mn,orderSet([+u]).length);if(mn<3)os['unit'+u]=mn}
R=null;
// 7 examples keys
const ci=cardIndex();const exBad=Object.keys(DATA.examples).filter(k=>!ci[k]);const exNoMark=Object.entries(DATA.examples).filter(([k,v])=>!/\[\[.+?\]\]/.test(v[0])).map(([k])=>k);
// 8 cards dup keys
const ck={};for(const u of Object.keys(DATA.words))for(const c of cardsOf(+u)){ck[c.key]=(ck[c.key]||0)+1}const cardDup=Object.entries(ck).filter(([k,n])=>n>1).map(([k])=>k);
// 9 words shape
const wbad=[];for(const [u,ws] of Object.entries(DATA.words))ws.forEach(w=>{if(!w[0]||!w[1]||!'bgavx'.includes(w[2]))wbad.push(u+':'+w[0])});const wdup=[];for(const [u,ws] of Object.entries(DATA.words)){const s=new Set();ws.forEach(w=>{if(s.has(w[0]))wdup.push(u+':'+w[0]);s.add(w[0])})}
// 10 exam
const exm=[];DATA.exam.papers.forEach((p,pi)=>{p.art.qs.forEach(q=>{if(new Set(q.slice(1).map(lc)).size!==q.length-1)exm.push('art'+pi)});p.mail.qs.forEach(q=>{if(new Set(q.slice(1).map(lc)).size!==q.length-1)exm.push('mail'+pi)});p.gap.gaps.forEach((g,k)=>{if(g[3]&&!DATA.tags[g[3]])exm.push('gaptag'+pi+k);if(!(p.gap.text.includes('{'+(k+1)+'}')))exm.push('gapmissing'+pi+k)})});
DATA.exam.letter.forEach((e,i)=>{if(e.tag&&!DATA.tags[e.tag])exm.push('lettertag'+i);if(e.t==='mc'&&new Set(e.opts.map(lc)).size!==e.opts.length)exm.push('letterdup'+i)});DATA.exam.news.forEach((n,i)=>{if(new Set(n.slice(1).map(lc)).size!==n.length-1)exm.push('newsdup'+i)});
// 11 news qs
const nw=[];newsAll().forEach(a=>a.qs.forEach((q,i)=>{if(new Set(q.opts.map(lc)).size!==q.opts.length)nw.push(a.id+'#'+i)}));
// 12 station tiers
const st=[];DATA.station.forEach(m=>{if(m.lv.length!==3)st.push(m.id)});
// 13 audio index contiguity
const packs={};for(const [k,[n,o,l]] of Object.entries(AUDIO_INDEX)){(packs[n]=packs[n]||[]).push([o,l])}const pk={};for(const [n,a] of Object.entries(packs)){a.sort((x,y)=>x[0]-y[0]);let end=0,gaps=0;for(const [o,l] of a){if(o!==end)gaps++;end=o+l}pk[n]=[a.length,end,gaps]}
// 14 audio referenced but missing
let need=0,miss2=0;for(const c of DATA.chapters)for(const ex of [...c.story,...c.puzzle]){const L=audioLines(ex);for(const x of Object.values(L)){need++;if(!AUDIO_HAVE.has(x.key))miss2++}}
let cneed=0,cmiss=0;for(const u of Object.keys(DATA.words))for(const c of cardsOf(+u)){const L=audioCardLines(c,DATA.examples[c.key]&&DATA.examples[c.key][0]);for(const x of [L.word,L.ex])if(x){cneed++;if(!AUDIO_HAVE.has(x.key))cmiss++}}
let nneed=0,nmiss=0;newsAll().forEach(a=>audioNewsLines(a).forEach(x=>{if(x){nneed++;if(!AUDIO_HAVE.has(x.key))nmiss++}}));
return {problems:P.slice(0,80),nProblems:P.length,gstat,wq,orderSetShort:os,exBad:exBad.slice(0,20),exNoMark:exNoMark.slice(0,20),cardDup,wbad,wdup,exm,nw,st,packs:pk,audio:{need,miss2,cneed,cmiss,nneed,nmiss},examPapers:DATA.exam.papers.length}}
