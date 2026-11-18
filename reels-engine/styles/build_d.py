from mk import page
REND='const R=new THREE.WebGLRenderer({antialias:true});R.setSize(1080,1920);document.body.prepend(R.domElement);R.toneMapping=THREE.ACESFilmicToneMapping;\nconst sc=new THREE.Scene();\n'
FMT='const fmt=n=>Math.round(n).toLocaleString("en-US");\n'
# 1 MAP ROUTE
page('map_route','#eef1f5',REND+r'''
R.shadowMap.enabled=true;sc.background=new THREE.Color(0xeef1f5);
const cam=new THREE.PerspectiveCamera(38,1080/1920,.1,300);
const g=new THREE.Mesh(new THREE.PlaneGeometry(200,200),new THREE.MeshStandardMaterial({color:0xe6e9ef}));g.rotation.x=-Math.PI/2;g.receiveShadow=true;sc.add(g);
const r=rng(3);const wm=new THREE.MeshStandardMaterial({color:0xffffff,roughness:.9});
for(let x=-40;x<40;x+=4)for(let z=-60;z<20;z+=4){if(r()<.15)continue;const h=.4+r()*(r()<.1?2.4:1.2);const b=new THREE.Mesh(new THREE.BoxGeometry(3,h,3),wm);b.position.set(x,h/2,z);b.castShadow=b.receiveShadow=true;sc.add(b)}
const park=new THREE.Mesh(new THREE.BoxGeometry(7,.1,7),new THREE.MeshStandardMaterial({color:0xbfe3c0}));park.position.set(-10,.05,-14);sc.add(park);
const river=new THREE.Mesh(new THREE.PlaneGeometry(200,5),new THREE.MeshStandardMaterial({color:0xbcdcf5}));river.rotation.x=-Math.PI/2;river.rotation.z=.3;river.position.set(0,.03,-30);sc.add(river);
const pts=[[2,0,10],[2,0,2],[-6,0,2],[-6,0,-10],[6,0,-10],[6,0,-22],[-2,0,-22],[-2,0,-38]].map(p=>new THREE.Vector3(p[0],.15,p[2]));
const curve=new THREE.CatmullRomCurve3(pts,false,'catmullrom',.02);const tg=new THREE.TubeGeometry(curve,400,.42,10);const tube=new THREE.Mesh(tg,new THREE.MeshStandardMaterial({color:0x2f7cf6,emissive:0x1050c0,emissiveIntensity:.4}));sc.add(tube);
const dot=new THREE.Mesh(new THREE.SphereGeometry(.8,24,16),new THREE.MeshStandardMaterial({color:0x2f7cf6,emissive:0x2f7cf6,emissiveIntensity:.6}));sc.add(dot);
const halo=new THREE.Mesh(new THREE.RingGeometry(1,1.6,40),new THREE.MeshBasicMaterial({color:0x2f7cf6,transparent:true,opacity:.3,side:2}));halo.rotation.x=-Math.PI/2;sc.add(halo);
const pin=new THREE.Group();const ph=new THREE.Mesh(new THREE.SphereGeometry(1,24,16),new THREE.MeshStandardMaterial({color:0xe5484d}));ph.position.y=3;pin.add(ph);const pc=new THREE.Mesh(new THREE.ConeGeometry(.6,2.2,20),new THREE.MeshStandardMaterial({color:0xe5484d}));pc.rotation.x=Math.PI;pc.position.y=1.4;pin.add(pc);pin.position.copy(pts[pts.length-1]);sc.add(pin);
sc.add(new THREE.HemisphereLight(0xffffff,0xdde3ea,1.6));const dl=new THREE.DirectionalLight(0xffffff,1.8);dl.position.set(-10,25,15);dl.castShadow=true;dl.shadow.mapSize.set(2048,2048);Object.assign(dl.shadow.camera,{left:-40,right:40,top:40,bottom:-40});sc.add(dl);
const total=tg.index.count;window.DUR=4.5;
window.render=t=>{const p=eio(pr(t,.3,3));tg.setDrawRange(0,Math.floor(total*p/6)*6);const q=curve.getPointAt(Math.max(.001,p));dot.position.copy(q);halo.position.set(q.x,.1,q.z);halo.scale.setScalar(1+.3*Math.sin(t*6));
 cam.position.set(q.x+8,62-p*8,q.z+26);cam.lookAt(q.x,0,q.z-6);pin.scale.setScalar(Math.max(.001,eob(pr(t,3.2,.5))));pin.rotation.y=t;R.render(sc,cam);
 document.getElementById('km').textContent=(4.2*p).toFixed(1)+' km';document.getElementById('eta').textContent=Math.round(12-12*p)+' min'};
''',css='''#card{position:absolute;left:60px;right:60px;bottom:120px;background:#fff;border-radius:36px;padding:40px 46px;box-shadow:0 20px 60px rgba(30,40,60,.18);font-family:Inter}
#card .a{font:500 30px Inter;color:#6b7280}#card .b{font:800 64px Inter;color:#111827;margin-top:8px}#card .row{display:flex;gap:30px;margin-top:22px;font:700 40px Inter;color:#2f7cf6}#card .row span{color:#6b7280;font-weight:500}''',
html='<div id="card"><div class="a">Route to</div><div class="b">The Studio</div><div class="row"><div id="km">0.0 km</div><span>·</span><div id="eta">12 min</div></div></div>')
# 2 STAT CHART
page('stat_chart','#0d0f14',FMT+r'''
const svg=document.getElementById('ch');const path=document.getElementById('ln');const area=document.getElementById('ar');const L=path.getTotalLength();path.style.strokeDasharray=L;
window.DUR=4.5;
window.render=t=>{const p=eio(pr(t,.3,3));document.getElementById('num').textContent='$'+(4.2*p).toFixed(1);path.style.strokeDashoffset=L*(1-p);area.style.clipPath=`inset(0 ${100-p*100}% 0 0)`;
 const pt=path.getPointAtLength(L*p);const d=document.getElementById('dt');d.setAttribute('cx',pt.x);d.setAttribute('cy',pt.y);
 document.getElementById('ann').style.opacity=eo(pr(t,2.4,.5));document.getElementById('tag').style.opacity=eo(pr(t,.8,.5))};
''',css='''#grid{position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.05) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.05) 1px,transparent 1px);background-size:60px 60px}
#lbl{position:absolute;left:80px;top:300px;color:#9aa3b2;font:600 32px Inter;letter-spacing:6px}
#num{position:absolute;left:70px;top:350px;color:#fff;font:800 300px/1 Inter;letter-spacing:-10px}#unit{position:absolute;left:80px;top:660px;color:#fff;font:700 70px Inter}
#tag{position:absolute;left:80px;top:770px;background:#ff6a2b;color:#fff;font:700 30px Inter;padding:10px 20px;border-radius:10px;opacity:0}#tag2{position:absolute;left:300px;top:780px;color:#9aa3b2;font:500 30px Inter}
svg{position:absolute;left:0;top:900px}#ann{opacity:0}''',
html='''<div id="grid"></div><div id="lbl">PORTFOLIO VALUE</div><div id="num">$0.0</div><div id="unit">million</div><div id="tag">▲ 312%</div><div id="tag2">since first rental · 2019</div>
<svg width="1080" height="800" viewBox="0 0 1080 800"><defs><linearGradient id="gr" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ff6a2b" stop-opacity=".45"/><stop offset="1" stop-color="#ff6a2b" stop-opacity="0"/></linearGradient></defs>
<path id="ar" d="M80 700 L80 640 C200 630 260 610 340 600 S480 560 560 540 S680 420 760 330 S900 160 1000 110 L1000 700Z" fill="url(#gr)"/>
<path id="ln" d="M80 640 C200 630 260 610 340 600 S480 560 560 540 S680 420 760 330 S900 160 1000 110" fill="none" stroke="#ff6a2b" stroke-width="8" stroke-linecap="round"/>
<circle id="dt" r="16" fill="#fff" stroke="#ff6a2b" stroke-width="6"/>
<g id="ann"><line x1="560" y1="540" x2="560" y2="700" stroke="#fff" stroke-dasharray="6 8" stroke-width="2"/><text x="580" y="660" fill="#fff" font-family="Inter" font-weight="700" font-size="30">Unit #4 bought</text><text x="580" y="700" fill="#9aa3b2" font-family="Inter" font-size="26">cash flow turns positive</text></g>
<g fill="#5b6475" font-family="Inter" font-size="24"><text x="80" y="760">2019</text><text x="380" y="760">2021</text><text x="680" y="760">2023</text><text x="940" y="760">2026</text></g></svg>''')
# 3 HEADLINE
page('headline','#1c1d22','''
window.DUR=4.5;window.render=t=>{const p=eo(pr(t,0,1.2));document.getElementById('paper').style.transform=`perspective(1600px) rotateX(${(1-p)*25+8}deg) rotateZ(${-4+p*2}deg) translateY(${(1-p)*400}px) scale(${.9+t*.03})`;
 document.getElementById('hl').style.width=eio(pr(t,1.6,1.1))*100+'%';document.getElementById('hl2').style.width=eio(pr(t,2.5,.9))*100+'%'};''',
css='''#paper{position:absolute;left:90px;top:300px;width:900px;height:1250px;background:#f4efe4;box-shadow:0 60px 120px rgba(0,0,0,.6);padding:60px 56px;font-family:Lora;color:#1a1a1a;transform-origin:center 70%}
#mast{text-align:center;font:700 92px/1 Lora;border-bottom:4px double #1a1a1a;padding-bottom:20px}#dl{display:flex;justify-content:space-between;font:500 20px Inter;letter-spacing:3px;border-bottom:2px solid #1a1a1a;padding:12px 0;text-transform:uppercase}
#h{font:700 62px/1.12 Lora;margin:34px 0 20px}#dek{font:italic 400 30px/1.4 Lora;color:#444;margin-bottom:24px}
.cols{column-count:2;column-gap:36px;font:400 23px/1.55 Lora;color:#333;text-align:justify}.mk{position:relative;z-index:1}.mk i{position:absolute;left:-4px;top:4px;bottom:0;background:#f7e463;z-index:-1;width:0}
#ph{height:230px;background:linear-gradient(135deg,#b9b2a3,#8d8676);margin-bottom:24px;filter:grayscale(1)}''',
html='''<div id="paper"><div id="mast">The Morrow Ledger</div><div id="dl"><span>Vol. CXII · No. 41</span><span>Thursday, November 12, 2026</span><span>Price 2.00</span></div>
<div id="h">A local landlord quietly <span class="mk"><i id="hl"></i>paid off four houses</span> with one rule.</div><div id="dek">He never bought a property he couldn't explain on a napkin.</div><div id="ph"></div>
<div class="cols">When Marcus Bell bought his first duplex in 2014, the numbers were simple. <span class="mk"><i id="hl2"></i>Every rent check went to the next down payment.</span> Ten years later the method hasn't changed: buy small, fix what tenants notice, and keep reserves for the roof nobody plans for. Neighbours call it boring. His lender calls it the cleanest file on the desk. The rule, he says, is older than any of it.</div></div>''')
# 4 PAPER DESK
page('paper_desk','#2f6b4f','''
const p=document.getElementById('cv');const L=p.getTotalLength();p.style.strokeDasharray=L;const c=document.getElementById('circ');const LC=c.getTotalLength();c.style.strokeDasharray=LC;
window.DUR=4.5;window.render=t=>{const a=eo(pr(t,0,.8));document.getElementById('sheet').style.transform=`translateY(${(1-a)*-500}px) rotate(${-3+(1-a)*-8}deg)`;
 p.style.strokeDashoffset=L*(1-eio(pr(t,.7,1.4)));c.style.strokeDashoffset=LC*(1-eio(pr(t,2.1,.7)));
 const b=eob(pr(t,2.7,.6));document.getElementById('note').style.transform=`translateX(${(1-b)*700}px) rotate(${2+(1-b)*10}deg)`;const k=eob(pr(t,3.1,.5));document.getElementById('lbl').style.transform=`scale(${k}) rotate(-6deg)`};''',
css='''#mat{position:absolute;inset:0;background-color:#2f6b4f;background-image:linear-gradient(rgba(255,255,255,.18) 2px,transparent 2px),linear-gradient(90deg,rgba(255,255,255,.18) 2px,transparent 2px),linear-gradient(rgba(255,255,255,.07) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.07) 1px,transparent 1px);background-size:180px 180px,180px 180px,36px 36px,36px 36px}
.tape{position:absolute;width:150px;height:46px;background:rgba(240,225,180,.8);box-shadow:0 2px 4px rgba(0,0,0,.15)}
#sheet{position:absolute;left:110px;top:330px;width:860px;height:760px;background:#fbf8f0;box-shadow:0 20px 40px rgba(0,0,0,.35);padding:46px;font-family:Lora;color:#222}
#sheet .k{font:600 20px Inter;letter-spacing:4px;color:#888}#sheet h2{font:700 50px/1.1 Lora;margin:12px 0 24px}
#note{position:absolute;left:470px;top:1180px;width:520px;background:#fffdf6;box-shadow:0 18px 36px rgba(0,0,0,.35);padding:40px;font:400 30px/1.45 Lora;color:#333}#note .k{font:600 20px Inter;letter-spacing:4px;color:#888;margin-bottom:10px}
#lbl{position:absolute;left:110px;top:1210px;background:#fff;color:#111;font:900 70px Inter;padding:14px 30px;border:5px solid #111;box-shadow:8px 8px 0 #111}''',
html='''<div id="mat"></div><div id="sheet"><div class="tape" style="left:-30px;top:-14px;transform:rotate(-30deg)"></div><div class="tape" style="right:-30px;top:-14px;transform:rotate(28deg)"></div>
<div class="k">FIG. 2 — TENANT INQUIRIES, FIRST 30 DAYS</div><h2>Most leads decide in the first week</h2>
<svg width="768" height="460"><line x1="40" y1="410" x2="740" y2="410" stroke="#222" stroke-width="3"/><line x1="40" y1="20" x2="40" y2="410" stroke="#222" stroke-width="3"/>
<path id="cv" d="M50 60 C90 70 120 250 170 300 S260 340 330 350 S500 365 600 372 S700 378 735 380" fill="none" stroke="#222" stroke-width="5"/>
<path id="circ" d="M120 120 C60 150 70 330 160 345 C260 360 260 160 190 110 C160 90 130 100 112 128" fill="none" stroke="#e03131" stroke-width="7" stroke-linecap="round"/>
<text x="40" y="445" font-family="Inter" font-size="20" fill="#666">day 1</text><text x="680" y="445" font-family="Inter" font-size="20" fill="#666">day 30</text></svg></div>
<div id="note"><div class="k">FROM THE NOTES · P. 14</div>Across our last 40 listings, the steepest drop came in week one. Leads who toured in the first 7 days mostly signed.</div><div id="lbl">THE HOOK</div>''')
# 5 BEFORE AFTER
page('before_after','#e9ecef','''
window.DUR=4.5;window.render=t=>{const p=eio(pr(t,1.2,1.8));document.getElementById('after').style.clipPath=`inset(0 0 0 ${100-p*100}%)`;document.getElementById('bar').style.left=(60+ (1-p)*960)+'px';document.getElementById('bar').style.opacity=p>0&&p<1?1:0;
 const s=eo(pr(t,0,.6));document.getElementById('frame').style.transform=`translateY(${(1-s)*100}px)`;document.getElementById('frame').style.opacity=s};''',
css='''#ttl{position:absolute;left:0;right:0;top:170px;text-align:center;font:800 84px/1.05 Inter;color:#111;letter-spacing:-2px}#ttl span{color:#ff5a36}
#frame{position:absolute;left:60px;top:470px;width:960px;height:1200px;border-radius:30px;overflow:hidden;box-shadow:0 30px 80px rgba(0,0,0,.25);background:#fff}
.pg{position:absolute;inset:0}.bar{position:absolute;top:0;height:46px;left:0;right:0;background:#ddd;display:flex;gap:10px;align-items:center;padding-left:20px}.bar i{width:14px;height:14px;border-radius:50%;background:#bbb}
#before{background:#f5f0dc;font-family:'DejaVu Serif',serif;color:#1a3d8f}#before .h{background:#1a3d8f;color:#ff0;font:700 46px 'DejaVu Serif';padding:30px;margin-top:46px;text-align:center}
#before .img{margin:30px;height:330px;background:linear-gradient(#9aa,#776);border:6px ridge #c90}#before p{margin:0 34px;font:400 30px/1.4 'DejaVu Serif';color:#222}#before .cta{margin:30px 34px;color:#00f;text-decoration:underline;font:700 34px 'DejaVu Serif'}#before .mar{background:#f00;color:#fff;font:700 28px 'DejaVu Sans';padding:8px 30px;margin:20px 34px}
#after{background:#fffaf5;font-family:Inter}#after .nav{margin-top:46px;display:flex;justify-content:space-between;padding:30px 44px;font:700 32px Inter}#after .nav span{font:500 26px Inter;color:#777}
#after .hero{margin:0 44px;height:520px;border-radius:26px;background:linear-gradient(160deg,#f7c59f 0%,#e07a5f 55%,#3d405b 100%);position:relative}#after .hero:after{content:'';position:absolute;left:250px;top:170px;width:360px;height:260px;background:#fffaf5;clip-path:polygon(50% 0,100% 40%,100% 100%,0 100%,0 40%);opacity:.95}
#after h1{margin:40px 44px 10px;font:800 70px/1.02 Inter;letter-spacing:-2px;color:#1d1d1f}#after p{margin:0 44px;font:400 30px/1.4 Inter;color:#666}#after .btn{margin:34px 44px;display:inline-block;background:#1d1d1f;color:#fff;font:600 32px Inter;padding:24px 40px;border-radius:40px}
#bar{position:absolute;top:470px;width:8px;height:1200px;background:#fff;box-shadow:0 0 20px rgba(0,0,0,.4)}
.tg{position:absolute;top:1700px;font:700 30px Inter;letter-spacing:6px;color:#888}''',
html='''<div id="ttl">Same house.<br><span>New listing.</span></div><div id="frame"><div class="pg" id="before"><div class="bar"><i></i><i></i><i></i></div><div class="h">!!! HOUSE 4 RENT !!!</div><div class="mar">★ CALL NOW ★ WONT LAST ★</div><div class="img"></div><p>3bd 2ba. nice area. no pets no smoking. 1st+last+deposit. serious inquirys only!!!</p><div class="cta">click here for more info</div></div>
<div class="pg" id="after"><div class="bar"><i></i><i></i><i></i></div><div class="nav">Willow Row<span>Tour · Apply · Contact</span></div><div class="hero"></div><h1>Room to grow,<br>minutes from town.</h1><p>3 bed · 2 bath · fenced yard · $1,850/mo</p><div class="btn">Book a tour</div></div></div><div id="bar"></div><div class="tg" style="left:90px">BEFORE</div><div class="tg" style="right:90px">AFTER</div>''')
# 6 ISO FLOW
page('iso_flow','#f4f6fb',REND+r'''
R.shadowMap.enabled=true;R.setClearColor(0xf4f6fb);
const S=9.5,asp=1080/1920;const cam=new THREE.OrthographicCamera(-S*asp,S*asp,S,-S,.1,100);cam.position.set(12,12,12);cam.lookAt(0,0,0);
const M=c=>new THREE.MeshStandardMaterial({color:c,roughness:.8});
const add=(geo,c,x,y,z)=>{const m=new THREE.Mesh(geo,M(c));m.position.set(x,y,z);m.castShadow=m.receiveShadow=true;sc.add(m);return m};
const plat=add(new THREE.BoxGeometry(10,.6,10),0xffffff,0,-.3,0);
// road S-curve
const road=new THREE.CatmullRomCurve3([[-4.5,0,3.5],[-1.5,0,3.5],[0,0,0],[1.5,0,-3.5],[4.5,0,-3.5]].map(p=>new THREE.Vector3(...p)));
const rp=road.getSpacedPoints(80);rp.forEach((p,i)=>{if(i%1==0)add(new THREE.BoxGeometry(.9,.05,.9),0x4a4e69,p.x,.03,p.z)});
// buildings: house, bank, home office
const house=new THREE.Group();const hb=new THREE.Mesh(new THREE.BoxGeometry(1.8,1.3,1.8),M(0xffd6a5));hb.position.y=.65;house.add(hb);const roof=new THREE.Mesh(new THREE.ConeGeometry(1.5,1,4),M(0xe07a5f));roof.position.y=1.8;roof.rotation.y=Math.PI/4;house.add(roof);house.position.set(-3.5,0,1.5);sc.add(house);
const bank=new THREE.Group();const bb=new THREE.Mesh(new THREE.BoxGeometry(2.2,1.6,1.6),M(0xa0c4ff));bb.position.y=.8;bank.add(bb);for(let i=0;i<4;i++){const c=new THREE.Mesh(new THREE.CylinderGeometry(.12,.12,1.4,10),M(0xffffff));c.position.set(-.8+i*.53,.7,.9);bank.add(c)}const br=new THREE.Mesh(new THREE.BoxGeometry(2.5,.3,1.9),M(0x5a7bd8));br.position.y=1.75;bank.add(br);bank.position.set(1.2,0,1.5);sc.add(bank);
const off=new THREE.Group();const ob=new THREE.Mesh(new THREE.BoxGeometry(1.4,2.6,1.4),M(0xcaffbf));ob.position.y=1.3;off.add(ob);for(let y=.5;y<2.5;y+=.55){const w=new THREE.Mesh(new THREE.BoxGeometry(1,.25,.05),M(0x6c8ebf));w.position.set(0,y,.72);off.add(w)}off.position.set(3.2,0,-1.6);sc.add(off);
const r=rng(9);for(let i=0;i<12;i++){const x=r()*9-4.5,z=r()*9-4.5;if(Math.abs(x+z)<2.5)continue;add(new THREE.SphereGeometry(.35,10,8),0x52b788,x,.45,z)}
const coin=add(new THREE.CylinderGeometry(.35,.35,.12,24),0xffc300,0,.5,0);coin.rotation.x=Math.PI/2;
sc.add(new THREE.HemisphereLight(0xffffff,0xd0d6e6,1.5));const dl=new THREE.DirectionalLight(0xffffff,2);dl.position.set(6,10,3);dl.castShadow=true;dl.shadow.mapSize.set(2048,2048);Object.assign(dl.shadow.camera,{left:-8,right:8,top:8,bottom:-8});sc.add(dl);
const pins=[...document.querySelectorAll('.pin')];const tgt=[house,bank,off];const v=new THREE.Vector3();
window.DUR=4.5;
window.render=t=>{sc.children.forEach(o=>{});const e=eob(pr(t,0,.7));plat.scale.set(e,1,e);[house,bank,off].forEach((b,i)=>b.scale.setScalar(Math.max(.001,eob(pr(t,.3+i*.15,.5)))));
 const cp=pr(t,1.4,2.6);const q=road.getPointAt(cp);coin.position.set(q.x,.55+Math.abs(Math.sin(t*8))*.25,q.z);coin.rotation.z=t*6;coin.visible=t>1.3;
 cam.zoom=1+t*.02;cam.updateProjectionMatrix();R.render(sc,cam);
 pins.forEach((p,i)=>{v.copy(tgt[i].position);v.y+=3.2;v.project(cam);p.style.left=((v.x*.5+.5)*1080-150)+'px';p.style.top=((-v.y*.5+.5)*1920-70)+'px';p.style.transform=`scale(${eob(pr(t,1.0+i*.9,.4))})`})};
''',css='''#ttl{position:absolute;left:0;right:0;top:220px;text-align:center;font:800 76px/1.08 Inter;color:#1d2433;letter-spacing:-2px}
.pin{position:absolute;width:300px;display:flex;align-items:center;gap:14px;background:#fff;border-radius:60px;padding:14px 24px;box-shadow:0 10px 30px rgba(20,30,60,.15);font:700 30px Inter;color:#1d2433;transform:scale(0)}
.pin b{width:50px;height:50px;border-radius:50%;background:#2f6bff;color:#fff;display:flex;align-items:center;justify-content:center;font:800 28px Inter}.pin span{display:block;font:500 22px Inter;color:#7a8296}''',
html='<div id="ttl">How rent<br>reaches you</div><div class="pin"><b>1</b><div>Tenant pays<span>autopay, 1st</span></div></div><div class="pin"><b>2</b><div>Bank clears<span>1–2 days</span></div></div><div class="pin"><b>3</b><div>You get paid<span>minus reserves</span></div></div>')
# 7 NOTIFICATIONS
page('notifications','#000',FMT+r'''
const items=[['Rent received','Unit 2B · Jordan M.','+$1,450'],['Rent received','Unit 1A · Priya K.','+$1,320'],['Lease signed','Willow Row · 12 months',''],['Rent received','Unit 3C · Sam T.','+$1,610'],['Rent received','Unit 2A · Lee R.','+$1,275']];
const list=document.getElementById('list');const els=items.map(([a,b,c])=>{const d=document.createElement('div');d.className='n';d.innerHTML=`<div class="ic">T&amp;T</div><div class="tx"><div class="r1"><b>${a}</b><span>now</span></div><div class="r2">${b}</div></div><div class="amt">${c}</div>`;list.appendChild(d);return d});
window.DUR=5;
const SLOT=170,ST=i=>.6+i*.7;
window.render=t=>{let tot=0;els.forEach((e,i)=>{const p=eob(pr(t,ST(i),.5));
 let down=0;for(let j=i+1;j<els.length;j++)down+=eio(pr(t,ST(j),.5));
 e.style.top=(down*SLOT)+'px';e.style.transform=`translateY(${(1-p)*-90}px) scale(${.92+.08*Math.min(1,p)})`;e.style.opacity=Math.min(1,p*1.6);e.style.zIndex=10+i;
 const age=t-ST(i);e.querySelector('.r1 span').textContent=age<1.2?'now':(Math.round(age)+'m ago');
 if(t>ST(i)+.25){const v=items[i][2];if(v)tot+=parseInt(v.replace(/[^0-9]/g,''))}});
 document.getElementById('tot').textContent='$'+fmt(4717+tot);};
''',css='''#wall{position:absolute;inset:0;background:radial-gradient(circle at 30% 20%,#3a4a8a,#141a33 50%,#05060d)}
#time{position:absolute;top:220px;left:0;right:0;text-align:center;color:#fff;font:600 230px/1 Inter;letter-spacing:-6px}#date{position:absolute;top:180px;left:0;right:0;text-align:center;color:#dfe6ff;font:500 42px Inter}
#wid{position:absolute;left:80px;right:80px;top:520px;display:flex;justify-content:space-between;align-items:center;background:rgba(255,255,255,.14);backdrop-filter:blur(20px);border-radius:36px;padding:26px 36px;color:#fff;font:600 32px Inter}#tot{font:800 48px Inter}
#list{position:absolute;left:50px;right:50px;top:690px;height:900px}
.n{position:absolute;left:0;right:0;display:flex;align-items:center;gap:22px;box-shadow:0 10px 30px rgba(0,0,0,.25);background:rgba(245,245,250,.82);border-radius:40px;padding:26px 30px;opacity:0}.ic{width:84px;height:84px;border-radius:20px;background:#0f1f3a;color:#e3bb5c;font:800 26px Inter;display:flex;align-items:center;justify-content:center;flex:none}
.tx{flex:1}.r1{display:flex;justify-content:space-between;font:700 32px Inter;color:#111}.r1 span{font:400 26px Inter;color:#666}.r2{font:400 30px Inter;color:#333;margin-top:4px}.amt{font:800 36px Inter;color:#16a34a}
#bot{position:absolute;bottom:60px;left:380px;width:320px;height:12px;border-radius:6px;background:#fff}
.btn{position:absolute;bottom:130px;width:110px;height:110px;border-radius:50%;background:rgba(255,255,255,.18)}''',
html='<div id="wall"></div><div id="date">Friday, 1 March</div><div id="time">9:41</div><div id="wid"><span>Collected today</span><span id="tot">$4,717</span></div><div id="list"></div><div class="btn" style="left:90px"></div><div class="btn" style="right:90px"></div><div id="bot"></div>')
# 8 DAY COUNTER
page('day_counter','#f2f2ef',r'''
const cal=document.getElementById('cal');for(let i=0;i<5;i++){const e=document.createElement('div');e.className='e';cal.appendChild(e)}
const cells=[];for(let d=1;d<=30;d++){const e=document.createElement('div');e.className='c';e.innerHTML=`<span>${d}</span><svg viewBox="0 0 40 40"><path d="M9 21 L17 29 L32 11" fill="none" stroke="#e8432e" stroke-width="5" stroke-linecap="round" stroke-linejoin="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/></svg>`;cal.appendChild(e);cells.push(e)}
window.DUR=4.5;
window.render=t=>{const p=eio(pr(t,.3,3.3));const day=Math.max(1,Math.round(1+p*29));const dn=document.getElementById('dn');dn.textContent=day;dn.style.transform=`translateY(${(day!==window._d?-10:0)}px)`;window._d=day;
 cells.forEach((c,i)=>{const on=i<day;c.classList.toggle('on',on);c.querySelector('path').setAttribute('stroke-dashoffset',on?Math.max(0,1-(p*29-i+1)*1.5):1)});
 document.getElementById('st').style.opacity=eo(pr(t,3.7,.4));};
''',css='''#k{position:absolute;top:200px;left:0;right:0;text-align:center;font:600 34px Inter;letter-spacing:12px;color:#888}#k:before,#k:after{content:'';display:inline-block;width:140px;height:2px;background:#bbb;vertical-align:middle;margin:0 20px}
#big{position:absolute;top:270px;left:0;right:0;text-align:center;font:900 300px/1 Inter;letter-spacing:-10px;color:#e8432e}#dn{display:inline-block;color:#111;min-width:340px;text-align:left}
#calw{position:absolute;left:110px;right:110px;top:720px;background:#fff;border-radius:30px;box-shadow:0 30px 70px rgba(0,0,0,.12);padding:50px 40px 40px}
#calw h3{font:800 50px Inter;margin:0 0 20px 10px}#hd{display:grid;grid-template-columns:repeat(7,1fr);font:600 24px Inter;color:#999;text-align:center;margin-bottom:10px}
#cal{display:grid;grid-template-columns:repeat(7,1fr);gap:10px}.c,.e{aspect-ratio:1;border-radius:14px;background:#f2f2f2;position:relative}.c span{position:absolute;left:10px;top:6px;font:600 22px Inter;color:#888}.c.on{background:#fde3df}.c svg{position:absolute;inset:14px}
.ring{position:absolute;top:705px;width:22px;height:60px;border-radius:11px;background:#222}
#st{position:absolute;top:1560px;left:0;right:0;text-align:center;font:700 44px Inter;color:#111;opacity:0}''',
html='<div id="k">POSTING EVERY DAY</div><div id="big">DAY <span id="dn">1</span></div><div id="calw"><h3>November</h3><div id="hd"><span>S</span><span>M</span><span>T</span><span>W</span><span>T</span><span>F</span><span>S</span></div><div id="cal"></div></div><div class="ring" style="left:280px"></div><div class="ring" style="right:280px"></div><div id="st">30 days. 30 parables. 0 missed.</div>')
# 9 RENT VS BUY
page('rent_vs_buy','#0f1f3a',FMT+r'''
const rows=[['Monthly cost',2100,2650],['Equity after 5 yrs',0,61400],['Tax benefits',0,4200],['Total cost, 5 yrs',126000,98300]];
window.DUR=4.5;
window.render=t=>{document.querySelectorAll('.row').forEach((r,i)=>{const p=eo(pr(t,.6+i*.45,.7));r.style.opacity=p;r.style.transform=`translateY(${(1-p)*30}px)`;
 const [a,b]=[rows[i][1],rows[i][2]];const mx=Math.max(a,b);r.querySelector('.ba').style.width=(a/mx*100*p)+'%';r.querySelector('.bb').style.width=(b/mx*100*p)+'%';r.querySelector('.va').textContent='$'+fmt(a*p);r.querySelector('.vb').textContent='$'+fmt(b*p)});
 const v=eob(pr(t,3.1,.5));document.getElementById('ver').style.transform=`scale(${v})`};
''',css='''#ttl{position:absolute;top:170px;left:0;right:0;text-align:center;font:900 150px/1 Inter;color:#f4ecd8;letter-spacing:-4px}#ttl i{font-style:normal;display:inline-block;background:#e3bb5c;color:#0f1f3a;border-radius:50%;width:110px;height:110px;font:800 44px/110px Inter;vertical-align:middle;margin:0 18px;letter-spacing:0}
#sub{position:absolute;top:350px;left:0;right:0;text-align:center;font:500 32px Inter;color:#9fb0cc}
#leg{position:absolute;top:450px;left:90px;display:flex;gap:40px;font:600 30px Inter;color:#f4ecd8}#leg span:before{content:'';display:inline-block;width:26px;height:26px;border-radius:6px;margin-right:12px;vertical-align:-4px;background:var(--c)}
#rows{position:absolute;top:540px;left:90px;right:90px;display:flex;flex-direction:column;gap:46px}.row{opacity:0}.row h4{font:600 34px Inter;color:#f4ecd8;margin:0 0 14px}
.l{display:flex;align-items:center;gap:20px;margin-bottom:12px}.bar{height:44px;border-radius:10px}.ba{background:#7f93b5}.bb{background:#e3bb5c}.va,.vb{font:700 32px Inter;color:#f4ecd8;white-space:nowrap}
#ver{position:absolute;left:90px;right:90px;bottom:200px;background:#f3ead7;color:#0f1f3a;border-radius:24px;padding:34px 40px;font:700 40px/1.3 Lora;transform:scale(0)}#ver small{display:block;font:500 24px Inter;color:#6b5a2f;margin-top:10px}''',
html='<div id="ttl">RENT<i>or</i>BUY</div><div id="sub">$350k home · 10% down · 6.4% rate</div><div id="leg"><span style="--c:#7f93b5">Rent</span><span style="--c:#e3bb5c">Buy</span></div><div id="rows">'+''.join(f'<div class="row"><h4>{n}</h4><div class="l"><div class="bar ba"></div><div class="va"></div></div><div class="l"><div class="bar bb"></div><div class="vb"></div></div></div>' for n in ['Monthly cost','Equity after 5 yrs','Tax benefits','Total cost, 5 yrs'])+'</div><div id="ver">Buying costs more each month and less over five years.<small>Illustrative numbers · not financial advice</small></div>')
# 10 BAR CHART
page('bar_chart','#fbfaf7',r'''
const d=[['Zillow / Trulia',38,'#2f6bff'],['Facebook Marketplace',24,'#7b61ff'],['Referrals',17,'#ff7a3d'],['Yard sign',12,'#16a34a'],['Craigslist',6,'#9aa3b2'],['Instagram',3,'#e1306c']];
const wrap=document.getElementById('bars');const els=d.map(([n,v,c])=>{const e=document.createElement('div');e.className='b';e.innerHTML=`<div class="n">${n}</div><div class="tr"><div class="f" style="background:${c}"></div><div class="v">0%</div></div>`;wrap.appendChild(e);return e});
window.DUR=4.5;
window.render=t=>{els.forEach((e,i)=>{const p=eo(pr(t,.6+i*.25,1.1));e.style.opacity=Math.min(1,p*3);e.querySelector('.f').style.width=(d[i][1]/40*100*p)+'%';e.querySelector('.v').textContent=Math.round(d[i][1]*p)+'%'});
 document.getElementById('yr').style.opacity=.08+.04*Math.sin(t)};
''',css='''#k{position:absolute;top:220px;left:90px;font:600 30px Inter;letter-spacing:6px;color:#ff7a3d}#ttl{position:absolute;top:270px;left:90px;right:90px;font:800 88px/1.02 Inter;letter-spacing:-3px;color:#111}
#yr{position:absolute;bottom:120px;right:40px;font:900 340px/1 Inter;color:#111;opacity:.08;letter-spacing:-12px}
#bars{position:absolute;top:620px;left:90px;right:90px;display:flex;flex-direction:column;gap:44px}.b{opacity:0}.n{font:600 34px Inter;color:#333;margin-bottom:12px}.tr{display:flex;align-items:center;gap:20px}.f{height:64px;border-radius:12px}.v{font:800 40px Inter;color:#111}
#src{position:absolute;bottom:90px;left:90px;font:400 24px Inter;color:#999}''',
html='<div id="k">2026 · 214 LEADS</div><div id="ttl">Where new tenants come from</div><div id="bars"></div><div id="yr">2026</div><div id="src">Sample data for illustration</div>')
# 11 SOCIAL CARD
page('social_card','#e7ecf3',FMT+r'''
window.DUR=4.5;window.render=t=>{const p=eob(pr(t,0,.7));document.getElementById('card').style.transform=`translateY(${(1-p)*300}px) scale(${.85+.15*p}) rotate(${(1-p)*-4}deg)`;document.getElementById('card').style.opacity=Math.min(1,p*2);
 const k=eio(pr(t,1,3));document.getElementById('lk').textContent=fmt(12840*k);document.getElementById('rp').textContent=fmt(2310*k);document.getElementById('cm').textContent=fmt(486*k);document.getElementById('vw').textContent=(1.4*k).toFixed(1)+'M';
 const h=document.getElementById('heart');const pop=pr(t,1.5,.4);h.style.transform=`scale(${1+Math.sin(pop*Math.PI)*.5})`;h.style.color=t>1.5?'#f91880':'#536471'};
''',css='''#card{position:absolute;left:70px;right:70px;top:520px;background:#fff;border-radius:40px;padding:50px;box-shadow:0 30px 80px rgba(20,30,50,.18);font-family:Inter;color:#0f1419}
.top{display:flex;gap:24px;align-items:center}.av{width:110px;height:110px;border-radius:50%;background:#0f1f3a;color:#e3bb5c;font:800 34px Inter;display:flex;align-items:center;justify-content:center}.nm{font:800 40px Inter}.nm i{display:inline-block;width:34px;height:34px;border-radius:50%;background:#1d9bf0;vertical-align:-4px;margin-left:8px}.hd{font:400 32px Inter;color:#536471}
.tx{font:400 46px/1.35 Inter;margin:36px 0}.tx b{font-weight:800}.meta{font:400 30px Inter;color:#536471;padding-bottom:28px;border-bottom:2px solid #eff3f4}
.acts{display:flex;justify-content:space-between;margin-top:28px;font:600 32px Inter;color:#536471}#heart{display:inline-block}''',
html='''<div id="card"><div class="top"><div class="av">T&amp;T</div><div><div class="nm">Talents &amp; Titles<i></i></div><div class="hd">@talentsandtitles</div></div></div>
<div class="tx">The widow didn't need more oil.<br><br>She needed <b>more jars.</b><br><br>Your supply was never the limit. Your capacity was.</div>
<div class="meta">9:41 AM · Nov 12, 2026 · <b style="color:#0f1419" id="vw">0</b> views</div>
<div class="acts"><span>💬 <span id="cm">0</span></span><span>🔁 <span id="rp">0</span></span><span><span id="heart">♥</span> <span id="lk">0</span></span><span>🔖</span></div></div>''')
# 12 APP MOCKUP
page('app_mockup','#dfe7f1',FMT+r'''
window.DUR=4.5;window.render=t=>{const ph=eob(pr(t,0,.7));document.getElementById('ph').style.transform=`translateY(${(1-ph)*500}px) rotate(${(1-ph)*8}deg)`;
 document.querySelectorAll('.anim').forEach((e,i)=>{const p=eo(pr(t,.7+i*.18,.5));e.style.opacity=p;e.style.transform=`translateY(${(1-p)*40}px)`});
 const k=eio(pr(t,1,1.8));document.getElementById('bal').textContent='$'+fmt(8740*k);document.getElementById('ring').style.strokeDashoffset=1-.92*k;document.getElementById('pc').textContent=Math.round(92*k)+'%';
 document.querySelectorAll('.mb').forEach((b,i)=>b.style.height=([.55,.7,.62,.85,.78,.95][i]*180*eio(pr(t,1.4+i*.08,.6)))+'px')};
''',css='''#ph{position:absolute;left:190px;top:200px;width:700px;height:1480px;background:#111;border-radius:100px;padding:22px;box-shadow:0 50px 120px rgba(20,40,80,.35)}
#sc{width:100%;height:100%;background:#f7f8fb;border-radius:80px;overflow:hidden;font-family:Inter;color:#111;position:relative;padding:90px 44px 0}
#isl{position:absolute;left:50%;top:22px;width:200px;height:56px;margin-left:-100px;background:#111;border-radius:30px}
.hi{font:500 28px Inter;color:#777}.h1{font:800 54px Inter;margin:4px 0 30px}
.card{background:#0f1f3a;color:#f4ecd8;border-radius:36px;padding:36px;position:relative}.card .l{font:500 26px Inter;opacity:.7}#bal{font:800 76px Inter;margin:6px 0}.card .s{font:500 24px Inter;color:#e3bb5c}
.card svg{position:absolute;right:30px;top:30px}#pc{position:absolute;right:62px;top:92px;font:800 30px Inter;color:#e3bb5c;width:90px;text-align:center}
.sec{font:700 32px Inter;margin:36px 0 18px}.chart{display:flex;align-items:flex-end;gap:18px;height:200px;background:#fff;border-radius:30px;padding:10px 28px 10px}.mb{flex:1;background:#e3bb5c;border-radius:10px 10px 4px 4px}
.u{display:flex;align-items:center;gap:20px;background:#fff;border-radius:26px;padding:22px 26px;margin-bottom:14px;font:600 28px Inter}.u i{width:60px;height:60px;border-radius:16px;background:#e8eefc;flex:none}.u span{margin-left:auto;font:700 28px Inter}.u .ok{color:#16a34a}.u .late{color:#e8432e}''',
html='''<div id="ph"><div id="sc"><div id="isl"></div><div class="hi anim">Good morning, Donte</div><div class="h1 anim">March rent</div>
<div class="card anim"><div class="l">Collected</div><div id="bal">$0</div><div class="s">of $9,500 · 6 units</div><svg width="130" height="130" viewBox="0 0 36 36"><circle cx="18" cy="18" r="15.9" fill="none" stroke="rgba(255,255,255,.15)" stroke-width="3.4"/><circle id="ring" cx="18" cy="18" r="15.9" fill="none" stroke="#e3bb5c" stroke-width="3.4" stroke-linecap="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" transform="rotate(-90 18 18)"/></svg><div id="pc">0%</div></div>
<div class="sec anim">Last 6 months</div><div class="chart anim"><div class="mb"></div><div class="mb"></div><div class="mb"></div><div class="mb"></div><div class="mb"></div><div class="mb"></div></div>
<div class="sec anim">Units</div><div class="u anim"><i></i>Unit 1A<span class="ok">Paid</span></div><div class="u anim"><i></i>Unit 2B<span class="ok">Paid</span></div><div class="u anim"><i></i>Unit 3C<span class="late">2 days late</span></div></div></div>''')
# 13 GLOBE ARCS
page('globe_arcs','#05070d',REND+r'''
import {EffectComposer} from 'three/addons/postprocessing/EffectComposer.js';import {RenderPass} from 'three/addons/postprocessing/RenderPass.js';import {UnrealBloomPass} from 'three/addons/postprocessing/UnrealBloomPass.js';
R.setClearColor(0x05070d);const cam=new THREE.PerspectiveCamera(35,1080/1920,.1,100);cam.position.set(0,-1.2,15.5);
const G=new THREE.Group();G.position.y=-1.3;sc.add(G);const RAD=2.4;
// land mask from rough continent blobs
const ll=(lat,lon,r=RAD)=>{const p=(90-lat)*Math.PI/180,th=(lon+180)*Math.PI/180;return new THREE.Vector3(-r*Math.sin(p)*Math.cos(th),r*Math.cos(p),r*Math.sin(p)*Math.sin(th))};
await new Promise(r=>{const s=document.createElement('script');s.src='/node_modules/topojson-client/dist/topojson-client.min.js';s.onload=r;document.head.appendChild(s)});
const topo=await (await fetch('/node_modules/world-atlas/land-110m.json')).json();const geoj=topojson.feature(topo,topo.objects.land);
const lc=document.createElement('canvas');lc.width=1440;lc.height=720;const lx=lc.getContext('2d',{willReadFrequently:true});lx.fillStyle='#fff';
const prj=([lo,la])=>[(lo+180)*4,(90-la)*4];geoj.features.forEach(f=>{const polys=f.geometry.type==='Polygon'?[f.geometry.coordinates]:f.geometry.coordinates;polys.forEach(poly=>{lx.beginPath();poly.forEach(ring=>{let pl=null;ring.forEach((c,i)=>{const [x,y]=prj(c);(i&&Math.abs(c[0]-pl)<180)?lx.lineTo(x,y):lx.moveTo(x,y);pl=c[0]});lx.closePath()});lx.fill('evenodd')})});
const LD=lx.getImageData(0,0,1440,720).data;const land=(lat,lon)=>{const x=Math.floor((lon+180)*4)%1440,y=Math.min(719,Math.floor((90-lat)*4));return LD[(y*1440+x)*4]>128};
const pos=[];for(let i=0;i<60000;i++){const y=1-2*(i+.5)/60000;const r=Math.sqrt(1-y*y);const th=i*2.39996;const lat=Math.asin(y)*180/Math.PI;const lon=-(((th*180/Math.PI)%360)-180);
 if(land(lat,lon)){const v=ll(lat,lon);pos.push(v.x,v.y,v.z)}}
const pg=new THREE.BufferGeometry();pg.setAttribute('position',new THREE.Float32BufferAttribute(pos,3));G.add(new THREE.Points(pg,new THREE.PointsMaterial({color:0x8fb0ff,size:.032})));
G.add(new THREE.Mesh(new THREE.SphereGeometry(RAD*.995,64,48),new THREE.MeshBasicMaterial({color:0x0a1226})));
const atm=new THREE.Mesh(new THREE.SphereGeometry(RAD*1.08,64,48),new THREE.ShaderMaterial({transparent:true,side:THREE.BackSide,blending:THREE.AdditiveBlending,vertexShader:'varying vec3 n;void main(){n=normalize(normalMatrix*normal);gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}',fragmentShader:'varying vec3 n;void main(){float i=pow(.75-dot(n,vec3(0,0,1.)),3.);gl_FragColor=vec4(.25,.45,1.,1.)*i*.7;}'}));atm.position.y=-1.3;sc.add(atm);

const src=[36.2,-115.1];const dst=[[40.7,-74],[51.5,-.1],[-23.5,-46.6],[35.7,139.7],[-33.9,151.2],[19.4,-99.1],[48.9,2.3],[6.5,3.4],[1.35,103.8],[55.7,37.6],[-26.2,28],[43.7,-79.4],[25.2,55.3],[28.6,77.2]];
const arcs=dst.map(d=>{const a=ll(...src),b=ll(...d);const m=a.clone().add(b).multiplyScalar(.5);m.normalize().multiplyScalar(RAD+a.distanceTo(b)*.45);const c=new THREE.QuadraticBezierCurve3(a,m,b);const g=new THREE.TubeGeometry(c,80,.012,6);const mesh=new THREE.Mesh(g,new THREE.MeshBasicMaterial({color:0xff8a3d}));G.add(mesh);const dotm=new THREE.Mesh(new THREE.SphereGeometry(.045,10,8),new THREE.MeshBasicMaterial({color:0xffc08a}));dotm.position.copy(b);G.add(dotm);return{g,mesh,dot:dotm}});
const home=new THREE.Mesh(new THREE.SphereGeometry(.07,12,10),new THREE.MeshBasicMaterial({color:0xffffff}));home.position.copy(ll(...src));G.add(home);
const comp=new EffectComposer(R);comp.addPass(new RenderPass(sc,cam));comp.addPass(new UnrealBloomPass(new THREE.Vector2(1080,1920),.9,.5,.2));
window.DUR=4.5;
window.render=t=>{G.rotation.y=-0.9+t*.18;G.rotation.x=.35;let n=0;arcs.forEach((a,i)=>{const p=eio(pr(t,.4+i*.18,.9));a.g.setDrawRange(0,Math.floor(a.g.index.count*p/3)*3);a.dot.visible=p>=1;if(p>=1)n++});
 document.getElementById('cnt').textContent=Math.round(24+n);comp.render()};
''',css='''#k{position:absolute;top:230px;left:0;right:0;text-align:center;font:600 32px Inter;letter-spacing:10px;color:#8aa0d6}#n{position:absolute;top:280px;left:0;right:0;text-align:center;color:#fff;font:800 200px/1 Inter}#n span{font:500 64px Inter;color:#ff8a3d;margin-left:16px}
#f{position:absolute;bottom:150px;left:0;right:0;text-align:center;color:#8aa0d6;font:500 30px Inter}''',
html='<div id="k">PACKS DOWNLOADED IN</div><div id="n"><b id="cnt">24</b><span>countries</span></div><div id="f">from Las Vegas, NV</div>')
# 14 LAPTOP REVEAL
page('laptop_reveal','#e9e6e1',REND+r'''
import {RoundedBoxGeometry} from 'three/addons/geometries/RoundedBoxGeometry.js';import {RoomEnvironment} from 'three/addons/environments/RoomEnvironment.js';
const pm=new THREE.PMREMGenerator(R);sc.environment=pm.fromScene(new RoomEnvironment(),.04).texture;R.setClearColor(0xe9e6e1);R.shadowMap.enabled=true;R.shadowMap.type=THREE.PCFSoftShadowMap;
const cam=new THREE.PerspectiveCamera(28,1080/1920,.1,100);
const al=new THREE.MeshStandardMaterial({color:0xc9ccd2,metalness:.9,roughness:.32});
const base=new THREE.Mesh(new RoundedBoxGeometry(4.4,.16,3,4,.08),al);base.castShadow=true;sc.add(base);
const kb=new THREE.Mesh(new THREE.BoxGeometry(3.7,.02,1.3),new THREE.MeshStandardMaterial({color:0x222428,roughness:.6}));kb.position.set(0,.085,-.35);sc.add(kb);
const tp=new THREE.Mesh(new THREE.BoxGeometry(1.5,.01,.9),new THREE.MeshStandardMaterial({color:0xb5b8bf,metalness:.6,roughness:.4}));tp.position.set(0,.085,.85);sc.add(tp);
const hinge=new THREE.Group();hinge.position.set(0,.08,-1.48);sc.add(hinge);
const lid=new THREE.Mesh(new RoundedBoxGeometry(4.4,3,.1,4,.05),al);lid.position.set(0,1.5,0);lid.castShadow=true;hinge.add(lid);
// screen texture
const cv=document.createElement('canvas');cv.width=1600;cv.height=1050;const x=cv.getContext('2d');
x.fillStyle='#f3ead7';x.fillRect(0,0,1600,1050);x.fillStyle='#0f1f3a';x.fillRect(0,0,1600,90);x.fillStyle='#e3bb5c';x.font='700 36px Inter';x.fillText('TALENTS & TITLES',60,58);x.fillStyle='#f4ecd8';x.font='500 28px Inter';x.fillText('Packs     Parables     About',1080,58);
x.fillStyle='#0f1f3a';x.font='800 96px Lora';x.fillText('Your lease,',90,330);x.fillText('done right.',90,440);x.fillStyle='#555';x.font='400 36px Inter';x.fillText('State-specific landlord document packs.',90,520);
x.fillStyle='#0f1f3a';x.beginPath();x.roundRect(90,580,330,90,45);x.fill();x.fillStyle='#fff';x.font='600 34px Inter';x.fillText('Get your pack',140,638);
x.fillStyle='#0f1f3a';x.beginPath();x.roundRect(900,180,600,760,30);x.fill();x.fillStyle='#e3bb5c';for(let i=0;i<6;i++){x.fillRect(960,260+i*100,480,14);x.fillStyle=i%2?'#e3bb5c':'#7f93b5'}x.fillStyle='#f4ecd8';x.font='700 44px Lora';x.fillText('Texas Pack',960,880);
const scr=new THREE.Mesh(new THREE.PlaneGeometry(4.1,2.7),new THREE.MeshBasicMaterial({map:new THREE.CanvasTexture(cv),toneMapped:false}));scr.position.set(0,1.5,.052);hinge.add(scr);
const shadow=new THREE.Mesh(new THREE.PlaneGeometry(30,30),new THREE.ShadowMaterial({opacity:.18}));shadow.rotation.x=-Math.PI/2;shadow.position.y=-.08;shadow.receiveShadow=true;sc.add(shadow);
const dl=new THREE.DirectionalLight(0xffffff,1.5);dl.position.set(3,8,5);dl.castShadow=true;dl.shadow.mapSize.set(2048,2048);dl.shadow.radius=8;sc.add(dl);
window.DUR=4.5;
window.render=t=>{const o=eio(pr(t,.4,2));hinge.rotation.x=Math.PI/2*(1-o)-.18*o;scr.material.color.setScalar(eo(pr(t,1.8,.8)));
 const a=-.5+t*.12;cam.position.set(Math.sin(a)*17,5.5+2*(1-o),Math.cos(a)*17);cam.lookAt(0,1.3*o-1.4,0);R.render(sc,cam)};
''',css='#cap{position:absolute;bottom:260px;left:0;right:0;text-align:center;font:800 76px/1.1 Inter;color:#1d1d1f;letter-spacing:-2px}#cap span{display:block;font:500 34px Inter;color:#777;letter-spacing:0;margin-top:14px}',
html='<div id="cap">The Texas pack<br>is live.<span>talentsandtitles.com</span></div>')
