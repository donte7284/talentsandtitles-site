from mk import page
# front-view office SVG shared by paper + watercolor
OFFICE_SVG='''
<g id="room">
 <rect class="wall" x="0" y="0" width="1080" height="1500"/>
 <rect class="floor" x="0" y="1380" width="1080" height="540"/>
 <g id="win"><rect class="winf" x="560" y="260" width="400" height="460" rx="10"/><rect class="sky" x="585" y="285" width="350" height="410"/>
  <g id="clouds"><ellipse class="cloud" cx="680" cy="400" rx="80" ry="34"/><ellipse class="cloud" cx="840" cy="520" rx="70" ry="28"/></g>
  <rect class="winf" x="752" y="285" width="16" height="410"/></g>
 <g id="shelf"><rect class="shelf" x="110" y="420" width="330" height="22"/><rect class="b1" x="140" y="320" width="40" height="100"/><rect class="b2" x="185" y="340" width="40" height="80"/><rect class="b3" x="230" y="310" width="40" height="110"/><rect class="b1" x="290" y="350" width="40" height="70" transform="rotate(-14 310 420)"/></g>
 <g id="clock"><circle class="clockf" cx="350" cy="620" r="70"/><line id="hand" class="hand" x1="350" y1="620" x2="350" y2="570"/><line class="hand" x1="350" y1="620" x2="380" y2="620"/></g>
 <g id="plant"><path class="leaf" d="M190 1180 C120 1050 120 980 170 930 C200 1010 210 1100 190 1180Z"/><path class="leaf2" d="M200 1180 C230 1040 290 980 340 970 C310 1060 260 1130 200 1180Z"/><path class="leaf" d="M195 1180 C170 1080 200 990 250 940 C255 1040 230 1120 195 1180Z"/><path class="pot" d="M130 1180 H270 L250 1380 H150Z"/></g>
 <g id="desk"><rect class="desk" x="330" y="1120" width="680" height="40" rx="6"/><rect class="deskl" x="360" y="1160" width="26" height="240"/><rect class="deskl" x="950" y="1160" width="26" height="240"/><rect class="drawer" x="780" y="1160" width="190" height="150"/><rect class="knob" x="850" y="1225" width="50" height="10" rx="5"/></g>
 <g id="mon"><rect class="mon" x="460" y="770" width="420" height="270" rx="14"/><rect class="scr" x="482" y="790" width="376" height="226" rx="6"/>
  <rect class="bar a" x="520" y="900" width="50" height="96"/><rect class="bar b" x="600" y="870" width="50" height="126"/><rect class="bar c" x="680" y="830" width="50" height="166"/><rect class="bar a" x="760" y="810" width="50" height="186"/>
  <rect class="mon" x="650" y="1040" width="40" height="60"/><rect class="mon" x="590" y="1096" width="160" height="24" rx="6"/></g>
 <g id="lamp"><path class="lampsh" d="M920 900 L1000 900 L1030 980 L890 980Z"/><rect class="mon" x="955" y="980" width="10" height="130"/><rect class="mon" x="915" y="1105" width="90" height="16" rx="6"/></g>
 <g id="mug"><rect class="mug" x="400" y="1050" width="56" height="70" rx="8"/><path class="mugh" d="M456 1065 q28 0 28 22 q0 22 -28 22" fill="none"/></g>
 <g id="chair"><rect class="chair" x="560" y="1180" width="230" height="250" rx="40"/><rect class="chair2" x="540" y="1400" width="270" height="44" rx="20"/><rect class="deskl" x="662" y="1444" width="26" height="150"/><rect class="chair2" x="560" y="1590" width="230" height="22" rx="10"/></g>
</g>'''
# ---------- PAPER CUTOUT ----------
page('paper_cutout','#e9dcc9','''
const order=['win','shelf','clock','plant','desk','mon','lamp','mug','chair'];window.DUR=4;
window.render=t=>{order.forEach((id,i)=>{const e=document.getElementById(id);const p=eob(pr(t,.15+i*.12,.55));e.style.transform=`translateY(${(1-p)*-260}px) rotate(${(1-p)*(i%2?6:-6)}deg)`;e.style.opacity=Math.min(1,p*3);e.style.transformOrigin='center';e.style.transformBox='fill-box'});
 document.getElementById('hand').setAttribute('transform',`rotate(${t*60} 350 620)`);document.getElementById('clouds').setAttribute('transform',`translate(${Math.sin(t)*20} 0)`);
 document.querySelectorAll('.bar').forEach((b,i)=>{const p=eob(pr(t,1.8+i*.15,.5));b.style.transform=`scaleY(${Math.max(.01,p)})`});
 document.getElementById('plant').querySelectorAll('.leaf,.leaf2').forEach((l,i)=>l.setAttribute('transform',`rotate(${Math.sin(t*2+i)*2} 200 1180)`))};
''',css='''svg{position:absolute;inset:0}
.wall{fill:#f2c6b4}.floor{fill:#c98a6b}.winf{fill:#fffaf0}.sky{fill:#a9d6e5}.cloud{fill:#fffaf0}.shelf{fill:#8c5a3c}.b1{fill:#e76f51}.b2{fill:#2a9d8f}.b3{fill:#e9c46a}
.clockf{fill:#fffaf0}.hand{stroke:#264653;stroke-width:8;stroke-linecap:round}.leaf{fill:#2a9d8f}.leaf2{fill:#52b788}.pot{fill:#e76f51}.desk{fill:#fffaf0}.deskl{fill:#8c5a3c}.drawer{fill:#f4e3c7}.knob{fill:#8c5a3c}
.mon{fill:#264653}.scr{fill:#e8f4f8}.bar{transform-box:fill-box;transform-origin:bottom}.bar.a{fill:#e76f51}.bar.b{fill:#e9c46a}.bar.c{fill:#2a9d8f}.lampsh{fill:#e9c46a}.mug{fill:#e76f51}.mugh{stroke:#e76f51;stroke-width:10}.chair{fill:#2a9d8f}.chair2{fill:#264653}
#room>g,#room>rect{filter:url(#paper)}
#grain{position:absolute;inset:0;mix-blend-mode:multiply;opacity:.35}''',
html='''<svg width="1080" height="1920" viewBox="0 0 1080 1920"><defs>
<filter id="paper" x="-10%" y="-10%" width="120%" height="130%"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="3" result="n"/><feColorMatrix in="n" type="saturate" values="0" result="g"/>
<feComposite in="SourceGraphic" in2="g" operator="arithmetic" k1="0" k2="1" k3="-.08" k4="0" result="tex"/><feDropShadow in="tex" dx="6" dy="12" stdDeviation="7" flood-color="#3a2416" flood-opacity=".35"/></filter></defs>'''+OFFICE_SVG+'</svg>')
# ---------- WATERCOLOR ----------
page('watercolor','#f7f1e3','''
window.DUR=4.5;const m=document.getElementById('maskc');
window.render=t=>{const p=eio(pr(t,0,3));m.setAttribute('r',80+p*1500);document.getElementById('dsp').setAttribute('seed',1+Math.floor(t*4)%3);
 document.getElementById('hand').setAttribute('transform',`rotate(${t*40} 350 620)`);document.getElementById('clouds').setAttribute('transform',`translate(${Math.sin(t*.8)*25} 0)`)};
''',css='''svg{position:absolute;inset:0}
.wall{fill:#f3d5c0;opacity:.55}.floor{fill:#c99a7a;opacity:.6}.winf{fill:#fff;opacity:.7}.sky{fill:#8ec5df;opacity:.75}.cloud{fill:#fff}.shelf{fill:#8a6a50;opacity:.8}.b1{fill:#d1495b;opacity:.75}.b2{fill:#2e86ab;opacity:.75}.b3{fill:#edae49;opacity:.8}
.clockf{fill:#fff;opacity:.8}.hand{stroke:#3d405b;stroke-width:6;stroke-linecap:round}.leaf{fill:#5c9e6e;opacity:.8}.leaf2{fill:#8bc49a;opacity:.8}.pot{fill:#d1495b;opacity:.75}.desk{fill:#e8d7c3;opacity:.9}.deskl{fill:#8a6a50;opacity:.75}.drawer{fill:#e8d7c3;opacity:.8}.knob{fill:#8a6a50}
.mon{fill:#3d405b;opacity:.85}.scr{fill:#dff1f7;opacity:.9}.bar.a{fill:#d1495b;opacity:.75}.bar.b{fill:#edae49;opacity:.8}.bar.c{fill:#2e86ab;opacity:.75}.lampsh{fill:#edae49;opacity:.85}.mug{fill:#d1495b;opacity:.75}.mugh{stroke:#d1495b;stroke-width:8;opacity:.75}.chair{fill:#2e86ab;opacity:.7}.chair2{fill:#3d405b;opacity:.75}
#room{filter:url(#wc)}#paperbg{position:absolute;inset:0;mix-blend-mode:multiply}''',
html='''<svg width="1080" height="1920" viewBox="0 0 1080 1920"><defs>
<filter id="wc" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence type="fractalNoise" baseFrequency=".022" numOctaves="3" seed="2" id="dsp" result="t"/><feDisplacementMap in="SourceGraphic" in2="t" scale="18" result="d"/>
<feTurbulence type="fractalNoise" baseFrequency=".6" numOctaves="3" seed="8" result="g"/><feColorMatrix in="g" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -1.6 1.3" result="ga"/>
<feComposite in="d" in2="ga" operator="in" result="p"/><feGaussianBlur in="d" stdDeviation="2.2" result="bl"/><feComposite in="bl" in2="p" operator="arithmetic" k2=".55" k3=".6"/></filter>
<filter id="rough"><feTurbulence type="fractalNoise" baseFrequency=".04" numOctaves="4" seed="5"/><feDisplacementMap in="SourceGraphic" scale="120"/></filter>
<mask id="mk"><rect width="1080" height="1920" fill="#000"/><circle id="maskc" cx="560" cy="960" r="80" fill="#fff" filter="url(#rough)"/></mask>
<filter id="pp"><feTurbulence type="fractalNoise" baseFrequency=".8" numOctaves="3" seed="1"/><feColorMatrix type="matrix" values="0 0 0 0 .96  0 0 0 0 .93  0 0 0 0 .86  0 0 0 -.9 1"/></filter></defs>
<rect width="1080" height="1920" fill="#f7f1e3"/><rect width="1080" height="1920" filter="url(#pp)" opacity=".5"/><g mask="url(#mk)">'''+OFFICE_SVG+'</g></svg>')
# ---------- INK WASH ----------
page('ink_wash','#efe8d8','''
const cv=document.createElement('canvas');cv.width=1080;cv.height=1920;document.body.prepend(cv);const X=cv.getContext('2d');
const r=rng(9);const ridge=(seed,base,amp,fr)=>{const rr=rng(seed);const ph=[rr()*6,rr()*6,rr()*6];return x=>base-amp*(Math.abs(Math.sin(x*fr+ph[0]))*.6+Math.sin(x*fr*2.3+ph[1])*.25+Math.sin(x*fr*5.1+ph[2])*.1)};
const layers=[[ridge(1,900,420,.004),.18,0.15],[ridge(2,1050,360,.006),.32,0.3],[ridge(3,1200,300,.008),.5,0.5],[ridge(4,1380,260,.011),.78,0.8]];
const birds=[...Array(5)].map((_,i)=>({x:200+i*60,y:420+r()*80,p:r()*6}));
window.DUR=4.5;
window.render=t=>{X.fillStyle='#efe8d8';X.fillRect(0,0,1080,1920);
 // sun
 X.fillStyle='#c8102e';X.globalAlpha=eo(pr(t,.2,.8));X.beginPath();X.arc(760,520,110,0,7);X.fill();X.globalAlpha=1;
 layers.forEach(([f,dark,par],i)=>{const rev=eio(pr(t,i*.35,1.2));const off=t*14*par;
  for(let x=0;x<1080;x+=3){const top=f(x+off);const g=X.createLinearGradient(0,top,0,top+520);g.addColorStop(0,`rgba(20,20,22,${dark*rev})`);g.addColorStop(.35,`rgba(20,20,22,${dark*.35*rev})`);g.addColorStop(1,'rgba(20,20,22,0)');X.fillStyle=g;X.fillRect(x,top,3,520)}
  // mist band
  const mg=X.createLinearGradient(0,0,0,1920);X.fillStyle=`rgba(239,232,216,${.35})`;X.fillRect(0,f(540+off)+160,1080,120)});
 // water
 X.fillStyle='#efe8d8';X.fillRect(0,1500,1080,420);for(let i=0;i<14;i++){X.strokeStyle=`rgba(20,20,22,${.15+.1*(i%3)})`;X.lineWidth=2;X.beginPath();const y=1530+i*26;X.moveTo(120+((i*97+t*30)%300),y);X.lineTo(320+((i*97+t*30)%300)+i*20,y);X.stroke()}
 // boat
 const bx=300+t*40,by=1600+Math.sin(t*2)*4;X.fillStyle='#141416';X.beginPath();X.moveTo(bx-90,by);X.quadraticCurveTo(bx,by+34,bx+90,by-6);X.lineTo(bx+60,by+6);X.quadraticCurveTo(bx,by+22,bx-70,by+6);X.fill();X.fillRect(bx-6,by-40,10,40);X.beginPath();X.arc(bx-1,by-48,14,Math.PI,0);X.fill();
 X.strokeStyle='#141416';X.lineWidth=3;X.beginPath();X.moveTo(bx+20,by-30);X.lineTo(bx+110,by+30);X.stroke();
 // birds
 X.strokeStyle='#141416';X.lineWidth=4;birds.forEach(b=>{const x=b.x+t*50,y=b.y+Math.sin(t*3+b.p)*8,w=Math.sin(t*10+b.p)*8;X.beginPath();X.moveTo(x-16,y-w);X.quadraticCurveTo(x-6,y-4,x,y);X.quadraticCurveTo(x+6,y-4,x+16,y-w);X.stroke()});
 // calligraphy column + seal
 X.fillStyle=`rgba(20,20,22,${eo(pr(t,1.8,.8))})`;X.font='600 58px Lora';['T','H','E',' ','R','I','V','E','R'].forEach((c,i)=>X.fillText(c,110,240+i*66));
 X.fillStyle=`rgba(200,16,46,${eo(pr(t,2.6,.5))})`;X.fillRect(96,860,70,70);X.fillStyle=`rgba(239,232,216,${eo(pr(t,2.6,.5))})`;X.font='700 30px Inter';X.fillText('T&T',103,906);
 X.fillStyle=`rgba(20,20,22,${eo(pr(t,2.2,.8))})`;X.font='italic 500 44px Lora';X.textAlign='center';X.fillText('The river keeps no name.',540,1820);X.textAlign='left'};
''')
# ---------- UKIYO-E ----------
page('ukiyo_e','#efe0bd','''
const cv=document.createElement('canvas');cv.width=1080;cv.height=1920;document.body.prepend(cv);const X=cv.getContext('2d');
const P='#1f3a68',P2='#3d6a9e',FOAM='#f6efdc',INK='#1b1b1b';
// paper fibers
const pc=document.createElement('canvas');pc.width=1080;pc.height=1920;const PX=pc.getContext('2d');const rr=rng(2);PX.fillStyle='#efe0bd';PX.fillRect(0,0,1080,1920);for(let i=0;i<9000;i++){PX.fillStyle=`rgba(120,90,40,${rr()*.08})`;PX.fillRect(rr()*1080,rr()*1920,rr()*30,1)}
window.DUR=4.5;
function wave(t,cx,base,H,ph){// big curling wave silhouette
 const pts=[];for(let i=0;i<=60;i++){const u=i/60;const x=cx-520+u*1040;const y=base-H*Math.pow(Math.sin(u*Math.PI*.95),1.6)*(1+.04*Math.sin(t*2+ph))+Math.sin(u*18+t*3+ph)*8;pts.push([x,y])}return pts}
window.render=t=>{X.drawImage(pc,0,0);
 // sky band & Fuji
 X.fillStyle='#d9c79c';X.fillRect(0,0,1080,140);
 X.fillStyle=P;X.beginPath();X.moveTo(640,1180);X.lineTo(760,1060);X.lineTo(800,1060);X.lineTo(930,1180);X.fill();X.fillStyle=FOAM;X.beginPath();X.moveTo(737,1083);X.lineTo(760,1060);X.lineTo(800,1060);X.lineTo(825,1085);X.lineTo(800,1078);X.lineTo(780,1090);X.lineTo(760,1078);X.fill();
 // big wave: body + hooked curl with hollow
 const s=Math.sin(t*1.1);const cx=420+s*20,cy=470-s*15;
 X.fillStyle=P;X.beginPath();X.moveTo(-60,1500);X.bezierCurveTo(-20,1100,60,760,cx-120,cy+40);
 X.bezierCurveTo(cx-40,cy-120,cx+260,cy-150,cx+420,cy-20);X.bezierCurveTo(cx+500,cy+60,cx+470,cy+200,cx+380,cy+230);
 X.bezierCurveTo(cx+430,cy+150,cx+380,cy+80,cx+300,cy+80);X.bezierCurveTo(cx+160,cy+80,cx+100,cy+220,cx+160,cy+380);
 X.bezierCurveTo(cx+220,cy+560,560,1050,720,1250);X.lineTo(760,1500);X.closePath();X.fill();
 // hollow of curl (paper shows through, lighter wash)
 X.fillStyle='#e6d3a6';X.beginPath();X.moveTo(cx+300,cy+95);X.bezierCurveTo(cx+190,cy+100,cx+150,cy+220,cx+190,cy+330);X.bezierCurveTo(cx+220,cy+250,cx+260,cy+170,cx+330,cy+150);X.closePath();X.fill();
 // stripes following the face
 X.strokeStyle=P2;X.lineWidth=12;for(let k=0;k<7;k++){X.beginPath();X.moveTo(-10+k*34,1500);X.bezierCurveTo(30+k*30,1150,110+k*20,850,cx-100+k*30,cy+90+k*22);X.bezierCurveTo(cx-40+k*20,cy-40+k*20,cx+150,cy-90+k*24,cx+300-k*10,cy-30+k*26);X.stroke()}
 // white foam crest line + claws hanging from curl lip
 X.strokeStyle=FOAM;X.lineWidth=16;X.lineCap='round';X.beginPath();X.moveTo(cx-120,cy+40);X.bezierCurveTo(cx-40,cy-120,cx+260,cy-150,cx+420,cy-20);X.bezierCurveTo(cx+500,cy+60,cx+470,cy+200,cx+380,cy+230);X.stroke();
 X.fillStyle=FOAM;for(let k=0;k<18;k++){const a=k/17;const ang=-2.6+a*3.3;const bx=cx+290+Math.cos(ang)*170,by=cy+60+Math.sin(ang)*150;const L=40+18*Math.sin(t*5+k);
  X.beginPath();X.moveTo(bx-9,by);X.quadraticCurveTo(bx+Math.cos(ang+1.7)*L*.6,by+Math.sin(ang+1.7)*L*.6+L*.5,bx+Math.cos(ang+1.2)*L,by+L);X.quadraticCurveTo(bx+6,by+L*.4,bx+9,by);X.fill();
  X.beginPath();X.arc(bx+Math.cos(ang+1.2)*L,by+L,6,0,7);X.fill()}
 // spray
 for(let k=0;k<40;k++){const a=(k*0.6180339)%1;const sx=cx-60+a*520,sy=cy-120-((k*37)%90)-Math.sin(t*3+k)*12;X.beginPath();X.arc(sx,sy,4+(k%3)*2,0,7);X.fill()}
 // foreground small waves
 for(let r=0;r<4;r++){const y=1420+r*110;X.fillStyle=r%2?P:P2;X.beginPath();X.moveTo(0,1920);for(let x=0;x<=1080;x+=20)X.lineTo(x,y+Math.sin(x/70+t*2.4+r)*24);X.lineTo(1080,1920);X.fill();
  X.fillStyle=FOAM;for(let x=0;x<1080;x+=70){const yy=y+Math.sin(x/70+t*2.4+r)*24;X.beginPath();X.arc(x+10,yy-4,8,0,7);X.fill()}}
 // boat
 const bx=640+Math.sin(t*1.3)*30,by=1360+Math.cos(t*1.3)*30;X.save();X.translate(bx,by);X.rotate(-.35+Math.sin(t*1.3)*.08);X.fillStyle='#e8d9b0';X.beginPath();X.moveTo(-200,0);X.quadraticCurveTo(0,40,200,-30);X.lineTo(190,-10);X.quadraticCurveTo(0,60,-200,20);X.fill();X.strokeStyle=INK;X.lineWidth=3;X.stroke();
 X.fillStyle=INK;for(let i=0;i<7;i++){X.beginPath();X.arc(-140+i*45,-4+i*-3,10,0,7);X.fill()}X.restore();
 // cartouche
 X.fillStyle='#e8d9b0';X.fillRect(890,640,120,380);X.strokeStyle=INK;X.lineWidth=4;X.strokeRect(890,640,120,380);X.fillStyle=INK;X.font='700 42px Lora';['T','A','L','E','N','T'].forEach((c,i)=>X.fillText(c,935,700+i*58));
 X.fillStyle='#b5121b';X.fillRect(910,1035,80,80);};
''',css='')
