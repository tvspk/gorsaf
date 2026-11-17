// Autoplayer: plays cases [a,b) through all four phases, 25% wrong answers (run by run_checks.py --play)
async (rng)=>{const sleep=ms=>new Promise(r=>setTimeout(r,ms));const log=[];const errs=[];window.addEventListener('error',e=>errs.push(String(e.message)));
window.__ex=null;const oStep=step;window.step=function(ex,...a){window.__ex=ex;return oStep(ex,...a)};
const M=()=>document.querySelector('#main');const btn=t=>[...M().querySelectorAll('button')].find(b=>b.textContent.trim().startsWith(t)&&!b.disabled);
let rushAns=0,hscroll=0;window.__toff=0;{const oraf=window.requestAnimationFrame.bind(window);window.requestAnimationFrame=cb=>oraf(t=>cb(t+window.__toff))}
async function answer(wrongP){const ex=window.__ex,c=M();const wrong=Math.random()<wrongP;
  if(ex.t==='mc'){const o=[...c.querySelectorAll('.opts .opt:not([disabled])')];const r=o.find(b=>b.textContent===ex.opts[0]);const pick=wrong?(o.find(b=>b!==r)||r):r;if(!r)log.push('MC no right '+JSON.stringify(ex.q).slice(0,80));(pick||o[0]).click()}
  else if(ex.t==='type'){const i=c.querySelector('input.txt');if(!i||i.disabled){log.push('TYPE no input '+String(ex.q).slice(0,60)+' | '+c.innerText.slice(0,120));return}i.value=wrong?'xyz':ex.answers[0];c.querySelector('form.row').requestSubmit();await sleep(5);if(!c.querySelector('.fb')&&c.querySelector('form.row')){i.value=ex.answers[0];c.querySelector('form.row').requestSubmit()}}
  else if(ex.t==='build'){for(const w of ex.answer.split(' ')){const ch=[...c.querySelectorAll('.tray .chip')].find(b=>b.textContent===w);if(!ch){log.push('BUILD missing '+w);break}ch.click()}c.querySelector('button.btn:not(.chip)').click()}
  else if(ex.t==='match'){for(const [a,b] of ex.pairs){const L=[...c.querySelectorAll('.match .col:not(.ends) .opt')].find(x=>x.textContent===a),R=[...c.querySelectorAll('.match .ends .opt')].find(x=>x.textContent===b);L.click();R.click()}}
}
async function playCase(i,wrongP){startChapter(i);let guard=0;
  while(guard++<4000){await sleep(2);const c=M();if(document.documentElement.scrollWidth>innerWidth+1)hscroll++;
    const h2=c.querySelector('h2');if(h2&&/^(Case closed|Overtime logged)/.test(h2.textContent))return 'ok';
    const fb=c.querySelector('.fb .btn');if(fb){fb.click();continue}
    if(c.querySelector('.hud')){const o=[...c.querySelectorAll('.rushq ~ .opts .opt:not([disabled])')];if(o.length){o[Math.floor(Math.random()*o.length)].click();rushAns++;await sleep(160)}else await sleep(50);
      if(rushAns>=3){window.__toff=(window.__toff||0)+1e6;await sleep(40)}continue}
    let b;if((b=btn('Open the counter'))){rushAns=0;b.click();continue}
    if((b=btn('To maintenance'))){b.click();continue}
    if((b=btn('Clock off'))){const jobs=[...c.querySelectorAll('.chapters .chap:not([disabled])')];if(jobs.length&&Math.random()<.5){jobs[0].click();continue}b.click();continue}
    if(c.querySelector('.fc')){return 'cards?'}
    const cont=btn('Continue');if(cont&&window.__ex&&window.__ex.t==='narr'){cont.click();continue}
    if(window.__ex&&c.querySelector('.q, .opts, form.row, .tray, .match')){await answer(wrongP);continue}
    if(cont){cont.click();continue}
    return 'stuck: '+c.innerText.slice(0,200)}
  return 'guard'}
const res={};const [a,b]=rng;for(let i=a;i<Math.min(b,DATA.chapters.length);i++){S.done=new Set(DATA.chapters.slice(0,i).map(c=>c.id));res[DATA.chapters[i].id]=await playCase(i,.25);console.log('case',i,res[DATA.chapters[i].id])}
const ot=[];if(a===0)for(let k=0;k<2;k++)ot.push(await playCase(-1,.3));
return {notOk:Object.entries(res).filter(([k,v])=>v!=='ok'),ot,log:log.slice(0,20),errs:errs.slice(0,20),hscroll,done:S.done.size,credits:S.credits,broken:[...S.broken],lv:S.lv,trophies:S.trophies.size,review:S.review.length}}
