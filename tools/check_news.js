// Y Papur Bro checker. Loads DATA from the game the same way audio/make_audio.py does.
// usage: node check_news.js game.html [units…]
// Uned 1–19: two pieces each. Uned 20 (Arholiad): one special issue {special, parts:[{title,by,byEn,genre,mail?,form?,text}], qs with 5 Welsh options and part}.
const fs=require('fs'),vm=require('vm');
const src=fs.readFileSync(process.argv[2],'utf8');
const data=src.slice(src.indexOf('const DATA = {'),src.indexOf('/* ============================ END OF CONTENT'));
const ctx={};vm.createContext(ctx);vm.runInContext(data+';this.DATA=DATA;',ctx);const D=ctx.DATA;
const want=process.argv.slice(3).map(Number);
let err=0;const E=m=>{err++;console.log('  ERROR '+m)};
const news=D.news||{},units=Object.keys(news).map(Number).sort((a,b)=>a-b);
const lw=s=>s.toLowerCase().normalize('NFC');
const words=s=>lw(s.replace(/\{([^|}]+)\|[^}]+\}/g,' ').replace(/<[^>]+>/g,' ')).replace(/[’‘]/g,"'").split(/[^a-zâêîôûŵŷäëïöüÿáéíóúẁýàèìòùẃỳ'-]+/).map(w=>w.replace(/^'+|'+$/g,'')).filter(Boolean);
// word stock for units 1..N: vocabulary, phrases, examples, notes, game texts of those units' chapters
function strings(o,out){if(typeof o==='string')out.push(o);else if(Array.isArray(o))o.forEach(x=>strings(x,out));else if(o&&typeof o==='object')Object.values(o).forEach(x=>strings(x,out));return out}
function stock(N){const st=new Set(),add=s=>words(s).forEach(w=>{st.add(w);w.split("'").forEach(x=>x&&st.add(x))});
  for(let u=1;u<=N;u++){strings(D.words[u]||[],[]).forEach(add);strings(D.phrases[u]||[],[]).forEach(add);strings(D.cardsExtra[u]||[],[]).forEach(add);strings(D.notes[u]||[],[]).forEach(add);
    Object.entries(D.examples).filter(([k])=>k.slice(1).split(':')[0]==u).forEach(([,v])=>add(v[0]));
    D.chapters.filter(c=>c.unit===u).forEach(c=>strings([c.story,c.puzzle],[]).forEach(add));
    (news[u]||[]).forEach(a=>Object.keys(a.gloss).forEach(add))}
  if(N>=1)strings(D.nasal,[]).forEach(add);return st}
// undo an initial mutation: soft, nasal, aspirate, h- before a vowel
function radicals(w){const out=new Set([w]),m=[['ngh','c'],['mh','p'],['nh','t'],['ng','g'],['ph','p'],['th','t'],['ch','c'],['dd','d'],['b','p'],['d','t'],['g','c'],['f','b'],['f','m'],['l','ll'],['r','rh'],['m','b'],['n','d']];
  for(const [a,b] of m)if(w.startsWith(a))out.add(b+w.slice(a.length));if(/^[aeiouwyâêîôûŵŷ]/.test(w))out.add('g'+w);if(/^h[aeiouwyâêîôûŵŷ]/.test(w))out.add(w.slice(1));return [...out]}
const NAMES=new Set(['seren']),ids=new Set(),EN=/\b(the|and|is|of|to|you|it|that|with|this|was|for|on|are|be|have|what|why|yes|no|but|she|he|they|we)\b(?!['’])/i;
let prevAuthor=null;
for(const u of units){const L=news[u];if(want.length&&!want.includes(u)){prevAuthor=L.length?L[L.length-1].by:prevAuthor;continue}
  console.log(`Uned ${u}`);if(u<1||u>20)E(`unit ${u} is outside 1–20`);if(u===20){if(L.length!==1||!L[0].special)E(`Uned 20 wants one special issue`)}else if(L.length!==2)E(`${L.length} pieces, want 2`);
  const st=stock(u);
  for(const a of L){if(a.special){a.text=a.parts.flatMap(p=>p.text.map(t=>[t[0],t[1]]));console.log(` ${a.id} · special · ${a.parts.map(p=>p.by).join(' / ')} · ${a.text.length} lines`)}
    else console.log(` ${a.id} · ${a.by} · ${a.genre} · ${a.text.length} sentences`);
    for(const k of ['id','unit','title','by','byEn','genre','tags','intro','text','gloss','qs','clip'])if(a[k]==null)E(`${a.id}: missing ${k}`);
    if(ids.has(a.id))E(`duplicate id ${a.id}`);ids.add(a.id);if(a.unit!==u)E(`${a.id}: unit ${a.unit} filed under ${u}`);
    if(!a.special){if(a.by===prevAuthor)E(`${a.id}: ${a.by} writes twice in a row`);prevAuthor=a.by;
    if(a.text.length<8||a.text.length>12)E(`${a.id}: ${a.text.length} sentences (8–12)`)}
    else{if(a.parts.length<3||a.parts.length>5)E(`${a.id}: ${a.parts.length} parts (3–5)`);if(a.text.length>40)E(`${a.id}: ${a.text.length} lines (max 40)`)}
    a.text.forEach((t,i)=>{if(a.chat&&!t[2])E(`${a.id} line ${i+1}: chat line without speaker`);if(!a.chat&&t[2])E(`${a.id} line ${i+1}: speaker outside a chat`);if(!t[1])E(`${a.id} line ${i+1}: no translation`);
      const bare=t[0].replace(/\{[^}]+\}/g,'');if(EN.test(bare))E(`${a.id} line ${i+1}: unmarked English word? "${bare.match(EN)[0]}"`)});
    const marked=new Set();a.text.forEach(t=>{for(const m of t[0].matchAll(/\{([^|}]+)\|([^}]+)\}/g))marked.add(m[2])});
    for(const l of marked)if(!a.gloss[l])E(`${a.id}: {…|${l}} has no gloss`);for(const l of Object.keys(a.gloss))if(!marked.has(l))E(`${a.id}: gloss "${l}" is not marked in the text`);
    if(marked.size>(a.special?10:6))E(`${a.id}: ${marked.size} words outside the syllabus (max ${a.special?10:6})`);
    if(!a.special){for(const t of a.tags)if(!(D.unitTags[u]||[]).includes(t))E(`${a.id}: tag ${t} not in unitTags[${u}]`);if(a.tags.length<2)E(`${a.id}: fewer than 2 tags`)}
    if(a.special?(a.qs.length<6||a.qs.length>10):a.qs.length!==3)E(`${a.id}: ${a.qs.length} questions`);
    a.qs.forEach((q,i)=>{if(q.opts.length!==(a.special?5:4))E(`${a.id} q${i+1}: ${q.opts.length} options`);if(a.special&&!(q.part>=0&&q.part<a.parts.length))E(`${a.id} q${i+1}: bad part`);if(a.special&&i&&q.part<a.qs[i-1].part)E(`${a.id} q${i+1}: questions out of order`);if(new Set(q.opts).size!==q.opts.length)E(`${a.id} q${i+1}: duplicate options`);if(!q.why)E(`${a.id} q${i+1}: no why`);
      const ls=q.opts.map(o=>o.length);if(Math.max(...ls)>2.2*Math.min(...ls))console.log(`  note ${a.id} q${i+1}: option lengths ${ls.join('/')}`)});
    // duplicates of sentences already in the game (outside DATA.news)
    const game=new Set(strings([D.chapters,D.examples,D.exam,D.bank,D.phrases],[]).map(s=>lw(s).replace(/[^a-zâêîôûŵŷ' ]/g,'').trim()));
    a.text.forEach((t,i)=>{const k=lw(t[0].replace(/\{([^|}]+)\|[^}]+\}/g,'$1')).replace(/[^a-zâêîôûŵŷ' ]/g,'').trim();if(k.split(' ').length>2&&game.has(k))E(`${a.id} line ${i+1}: sentence already in the game`)});
    const out=new Set();a.text.forEach(t=>words(t[0]).forEach(w=>{if(NAMES.has(w)||radicals(w).some(r=>st.has(r)))return;const parts=w.split("'").filter(Boolean);if(parts.length>1&&parts.every(p=>radicals(p).some(r=>st.has(r))))return;out.add(w)}));
    console.log(out.size?`  not in units 1–${u} (check by hand): ${[...out].join(', ')}`:`  every word is in units 1–${u}`)}}
console.log(err?`${err} error(s)`:'OK');process.exit(err?1:0)
