// Visits every side screen and reports script errors and sideways scroll (run by run_checks.py)
async ()=>{const sleep=ms=>new Promise(r=>setTimeout(r,ms));const out={over:[],errs:[]};window.addEventListener('error',e=>out.errs.push(String(e.message)));
const chk=name=>{const W=document.documentElement.scrollWidth,iw=innerWidth;if(W>iw+1){const wide=[...document.querySelectorAll('#main *')].filter(el=>{const r=el.getBoundingClientRect();return r.right>iw+1}).slice(0,3).map(el=>el.tagName+'.'+el.className+':'+el.textContent.slice(0,30));out.over.push(name+' '+W+' '+JSON.stringify(wide))}};
const M=()=>document.querySelector('#main');
S.done=new Set(DATA.chapters.map(c=>c.id));S.credits=5000;S.exam.n=1;S.exam.best=88;S.trophies=new Set(DATA.chapters.map(c=>c.trophy).concat(['tystysgrif']));
newsAll().forEach(a=>S.reads[a.id]={best:2,at:today()});
home();await sleep(30);chk('home');document.querySelector('.bonussep').click();await sleep(30);chk('home+bonus');
for(const g of document.querySelectorAll('.uhead')){g.click();await sleep(5)}chk('home all units');
for(const u of Object.keys(DATA.words)){mnemo(+u);await sleep(5);chk('mnemo'+u);mnRound(mnQueue(mnCards(+u)));await sleep(5);for(let k=0;k<4;k++){const fc=M().querySelector('.mhfc');if(!fc)break;fc.click();await sleep(2);chk('mnback'+u);const b=M().querySelector('.mhg'+(k%3+1));if(!b)break;b.click();await sleep(2)}}
for(const u of Object.keys(DATA.words)){drill(+u);await sleep(5);chk('drill'+u)}
for(const u of Object.keys(DATA.news)){papurList(+u);await sleep(5);chk('plist'+u);for(const a of DATA.news[u]){papur(a.id);await sleep(5);chk('papur '+a.id);for(let q=0;q<a.qs.length;q++){const o=M().querySelector('.pqbox .opt');o.click();await sleep(2);M().querySelector('.pqbox .fb .btn').click();await sleep(2)}chk('papurEnd '+a.id);const g=M().querySelector('.gl');if(g){g.click()}}}
exam();await sleep(5);chk('exam intro');M().querySelector('.btn').click();await sleep(5);
for(let i=0;i<60;i++){const c=M();const o=c.querySelector('.opts .opt');if(o){chk('exam q'+i);o.click();await sleep(2);continue}const inp=c.querySelector('input.txt');if(inp){chk('exam gap'+i);inp.value='test';c.querySelector('form').requestSubmit();await sleep(2);continue}break}
chk('exam result');out.examResult=M().querySelector('h2')&&M().querySelector('h2').textContent;
treig();await sleep(5);chk('treig');shop();await sleep(5);chk('shop');backup();await sleep(5);chk('backup');restore();await sleep(5);chk('restore');
S.round={};R={maint:true,earned:0,retry:0};runStation(()=>{});await sleep(5);chk('maint');
revise();await sleep(5);chk('revise');
// grammar notes for every unit
for(const u of Object.keys(DATA.notes)){const n=notesEl(u);M().replaceChildren(n);chk('notes'+u)}
home();return out}
