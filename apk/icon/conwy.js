const {chromium}=require('playwright');const fs=require('fs');
const DRAIG=fs.readFileSync('draig.svgfrag','utf8');
const stars=(n,seed)=>{let r=seed,o='';const R=()=>(r=(r*9301+49297)%233280)/233280;for(let i=0;i<n;i++){const x=R()*100,y=R()*62;o+=`<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="${(R()*.55+.2).toFixed(2)}" fill="#e6efff" opacity="${(R()*.55+.35).toFixed(2)}"/>`}return o};
const S='#b9b1a3',SD='#8f877a',SL='#d4cdbf';
const cren=(x,y,w,c)=>{let o='';const n=Math.max(2,Math.round(w/3));const mw=w/(n*2-1);for(let i=0;i<n;i++)o+=`<rect x="${(x+i*2*mw).toFixed(2)}" y="${y-2}" width="${mw.toFixed(2)}" height="2.2" fill="${c}"/>`;return o};
const tower=(cx,top,w,turret)=>{let o=`<rect x="${cx-w/2}" y="${top}" width="${w}" height="${76-top}" fill="${S}"/><rect x="${cx-w/2}" y="${top}" width="${w*0.32}" height="${76-top}" fill="${SL}" opacity=".55"/><rect x="${cx+w/2-w*0.25}" y="${top}" width="${w*0.25}" height="${76-top}" fill="${SD}" opacity=".7"/>`+cren(cx-w/2,top,w,S)
 +`<rect x="${cx-0.8}" y="${top+6}" width="1.6" height="3" rx=".8" fill="#f0a83a"/>`;
 if(turret)o+=`<rect x="${cx+w*0.05}" y="${top-8}" width="${w*0.32}" height="8" fill="${S}"/>`+cren(cx+w*0.05,top-8,w*0.32,S);return o};
const flag=(x,y)=>`<path d="M${x} ${y}v-13" stroke="#d4cdbf" stroke-width=".8"/><svg x="${x}" y="${y-13}" width="14" height="10.5" viewBox="0 0 640 480"><rect width="640" height="240" fill="#fff"/><rect y="240" width="640" height="240" fill="#00ab39"/>${DRAIG}</svg>`;
const castle=`<g>
 <path d="M6 76 L14 74 L30 75 L52 74 L72 75 L88 73 L95 77 L90 84 L80 88 L74 95 L60 93 L48 99 L38 93 L24 94 L16 87 L9 83 Z" fill="#3d4250"/>
 <path d="M6 76 L14 74 L30 75 L52 74 L72 75 L88 73 L95 77 L91 80 L70 79 L50 80 L28 79 L10 80 Z" fill="#5a6070"/>
 <circle cx="30" cy="86" r="2.2" fill="#2e323d"/><circle cx="64" cy="88" r="1.6" fill="#2e323d"/><circle cx="78" cy="83" r="1.2" fill="#2e323d"/>
 <rect x="8" y="56" width="84" height="20" fill="${SD}"/>${cren(8,56,84,SD)}
 <path d="M47 76v-8a3 3 0 0 1 6 0v8z" fill="#1b1f27"/>
 ${tower(16,44,13,false)}${tower(38,43,13,false)}${tower(62,43,13,true)}${tower(84,44,13,true)}
 ${flag(62+13*0.21,35)}
</g>`;
const svg=(px,round)=>`<svg xmlns="http://www.w3.org/2000/svg" width="${px}" height="${px}" viewBox="0 0 100 100"><defs><clipPath id="r"><rect width="100" height="100" rx="${round?22:0}"/></clipPath><radialGradient id="g" cx=".7" cy=".25" r=".9"><stop offset="0" stop-color="#1f2d4a"/><stop offset="1" stop-color="#0a0f1a"/></radialGradient></defs><g clip-path="url(#r)"><rect width="100" height="100" fill="url(#g)"/>${stars(45,3)}<circle cx="80" cy="16" r="5" fill="#cfd8e6" opacity=".9"/><circle cx="78.5" cy="14.5" r="5" fill="#0f1626" opacity=".55"/>${castle}</g></svg>`;
(async()=>{const br=await chromium.launch();const pg=await br.newPage({viewport:{width:512,height:512}});await pg.setContent(`<body style="margin:0;background:transparent">${svg(512,true)}</body>`);await pg.screenshot({path:'conwy-icon.png',omitBackground:true});
await pg.setViewportSize({width:280,height:120});await pg.setContent(`<body style="margin:0;background:#2b2b2b;display:flex;gap:24px;align-items:center;padding:14px">${[96,64,44].map(s=>svg(s,true)).join('')}</body>`);await pg.screenshot({path:'conwy-sizes.png'});await br.close()})();

// ---- export app icon set ----
(async()=>{const br=await chromium.launch();const pg=await br.newPage();
const defs=`<defs><radialGradient id="g" cx=".7" cy=".25" r=".9"><stop offset="0" stop-color="#1f2d4a"/><stop offset="1" stop-color="#0a0f1a"/></radialGradient></defs>`;
const fg=`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 108 108"><g transform="translate(54 56) scale(.62) translate(-50 -64)">${castle}</g></svg>`;
const bg=`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 108 108">${defs}<rect width="108" height="108" fill="url(#g)"/><g transform="translate(4 4)">${stars(45,3)}</g><circle cx="36" cy="34" r="4" fill="#cfd8e6" opacity=".9"/><circle cx="34.8" cy="32.8" r="4" fill="#0f1626" opacity=".55"/></svg>`;
const shot=async(svg,px,file,transp)=>{await pg.setViewportSize({width:px,height:px});await pg.setContent(`<html><body style="margin:0;background:transparent">${svg.replace('<svg ',`<svg width="${px}" height="${px}" `)}</body></html>`);await pg.screenshot({path:file,omitBackground:!!transp,clip:{x:0,y:0,width:px,height:px}})};
const D={mdpi:1,hdpi:1.5,xhdpi:2,xxhdpi:3,xxxhdpi:4};
for(const [d,f] of Object.entries(D)){await shot(svg(48*f,true).replace(/ width="\d+(\.\d+)?" height="\d+(\.\d+)?"/,''),48*f,`c_launcher-${d}.png`,true);await shot(fg,108*f,`c_fg-${d}.png`,true);await shot(bg,108*f,`c_bg-${d}.png`,false)}
const b64=f=>'data:image/png;base64,'+fs.readFileSync(f).toString('base64');
await pg.setViewportSize({width:520,height:260});await pg.setContent(`<html><body style="margin:0;background:#777;display:flex;gap:30px;padding:20px">${['50%','18%'].map(rad=>`<div style="width:216px;height:216px;border-radius:${rad};overflow:hidden;position:relative"><img src="${b64('c_bg-xxxhdpi.png')}" style="position:absolute;width:324px;left:-54px;top:-54px"><img src="${b64('c_fg-xxxhdpi.png')}" style="position:absolute;width:324px;left:-54px;top:-54px"></div>`).join('')}</body></html>`);
await pg.waitForTimeout(200);await pg.screenshot({path:'c-adaptive-preview.png'});await br.close()})();
