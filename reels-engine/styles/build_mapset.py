# Map set: 3 map types (campaign, bridge, territory) x 3 themes (fantasy, simple, modern)
from mk import page
FONTS="@font-face{font-family:'Uncial Antiqua';src:url(fonts/uncial-antiqua-latin-400-normal.woff2)}@font-face{font-family:'IM Fell';font-style:italic;src:url(fonts/im-fell-english-latin-400-italic.woff2)}@font-face{font-family:'IM Fell';font-style:normal;src:url(fonts/im-fell-english-latin-400-normal.woff2)}"
CORE=r'''
await document.fonts.load("40px 'Uncial Antiqua'");await document.fonts.load("italic 24px 'IM Fell'");
const THEMES={
 fantasy:{ink:[46,34,20],A:'#1f3d70',B:'#8a1f12',mark:'#8a1f12',halo:'rgba(236,220,178,.85)',panel:'rgba(236,220,178,.93)',
  T:s=>`${s}px 'Uncial Antiqua'`,L:s=>`${s}px 'Uncial Antiqua'`,I:s=>`italic ${s}px 'IM Fell'`,up:false,
  nat:['rgba(40,85,170,.34)','rgba(138,31,18,.30)','rgba(55,105,35,.32)','rgba(165,115,20,.34)'],natS:['#1f3d70','#8a1f12','#376923','#a5731a']},
 simple:{ink:[51,54,61],A:'#2f6fdc',B:'#e0453a',mark:'#e0453a',halo:'rgba(255,255,255,.92)',panel:'rgba(255,255,255,.95)',
  T:s=>`800 ${s}px Inter`,L:s=>`700 ${s}px Inter`,I:s=>`italic 600 ${s}px Lora`,up:false,
  nat:['#a7c8f3','#f3aaa2','#b2dca4','#f5d887'],natS:['#2f6fdc','#e0453a','#3f9a3a','#d39a12']},
 modern:{ink:[207,232,239],A:'#4fb3ff',B:'#ff4d5e',mark:'#ffc850',halo:'rgba(7,11,16,.92)',panel:'rgba(7,11,16,.9)',
  T:s=>`800 ${s}px Inter`,L:s=>`600 ${s}px "DejaVu Sans Mono"`,I:s=>`500 ${s}px "DejaVu Sans Mono"`,up:true,
  nat:['rgba(79,179,255,.26)','rgba(255,77,94,.26)','rgba(80,230,160,.22)','rgba(255,200,80,.22)'],natS:['#4fb3ff','#ff4d5e','#50e6a0','#ffc850']}};
const TT=THEMES[TH];const inkA=(a=1)=>`rgba(${TT.ink.join(',')},${a})`;const INK=inkA(1);const BLUE=TT.A,RED=TT.B;
const cv=document.createElement('canvas');cv.width=1080;cv.height=1920;document.body.prepend(cv);const X=cv.getContext('2d');
let R=rng(29);
const mkC=()=>{const c=document.createElement('canvas');c.width=1080;c.height=1920;return c};
const M=mkC();let Q=M.getContext('2d');
// ---------- backgrounds ----------
function parchment(){const g=Q.createRadialGradient(540,980,250,540,980,1180);g.addColorStop(0,'#efdfb4');g.addColorStop(.55,'#e2c993');g.addColorStop(.85,'#c9a565');g.addColorStop(1,'#7d5a2c');Q.fillStyle=g;Q.fillRect(0,0,1080,1920);
 const r=rng(3);for(let i=0;i<22000;i++){Q.fillStyle=`rgba(80,52,20,${r()*.05})`;Q.fillRect(r()*1080,r()*1920,1+r()*28,1)}
 for(let i=0;i<70;i++){const x=r()*1080,y=r()*1920,rr=30+r()*140;const gg=Q.createRadialGradient(x,y,0,x,y,rr);gg.addColorStop(0,'rgba(120,80,35,.07)');gg.addColorStop(1,'rgba(120,80,35,0)');Q.fillStyle=gg;Q.fillRect(x-rr,y-rr,2*rr,2*rr)}}
function grid(base){Q.fillStyle=base;Q.fillRect(0,0,1080,1920);Q.strokeStyle='rgba(90,140,170,.12)';Q.lineWidth=1;for(let x=0;x<=1080;x+=60){Q.beginPath();Q.moveTo(x,0);Q.lineTo(x,1920);Q.stroke()}for(let y=0;y<=1920;y+=60){Q.beginPath();Q.moveTo(0,y);Q.lineTo(1080,y);Q.stroke()}}
function seaBg(){if(TH=='fantasy')parchment();else if(TH=='simple'){Q.fillStyle='#a9d4ef';Q.fillRect(0,0,1080,1920)}else grid('#070b10')}
function groundBg(){if(TH=='fantasy')parchment();else if(TH=='simple'){Q.fillStyle='#e8eed1';Q.fillRect(0,0,1080,1920)}else grid('#0e1820')}
// ---------- coast ----------
function coastFill(fillTrace,lineTrace){
 if(TH=='fantasy'){for(let k=1;k<=7;k++){Q.save();Q.translate(-k*7,k*3);Q.beginPath();lineTrace(Q);Q.strokeStyle=inkA(.2-k*.022);Q.lineWidth=1.1;Q.setLineDash([22+k*3,6+k*2]);Q.stroke();Q.restore()}Q.setLineDash([]);Q.beginPath();fillTrace(Q);Q.fillStyle='rgba(239,224,184,.45)';Q.fill()}
 else if(TH=='simple'){Q.beginPath();lineTrace(Q);Q.strokeStyle='#c4e3f5';Q.lineWidth=70;Q.lineJoin='round';Q.stroke();Q.beginPath();fillTrace(Q);Q.fillStyle='#e8eed1';Q.fill()}
 else{Q.beginPath();fillTrace(Q);Q.fillStyle='#101b24';Q.fill();Q.save();Q.beginPath();fillTrace(Q);Q.clip();Q.strokeStyle='rgba(90,140,170,.12)';Q.lineWidth=1;for(let x=0;x<=1080;x+=60){Q.beginPath();Q.moveTo(x,0);Q.lineTo(x,1920);Q.stroke()}for(let y=0;y<=1920;y+=60){Q.beginPath();Q.moveTo(0,y);Q.lineTo(1080,y);Q.stroke()}Q.restore()}}
function coastLine(lineTrace){Q.beginPath();lineTrace(Q);if(TH=='fantasy'){Q.strokeStyle=INK;Q.lineWidth=2.6;Q.stroke()}else if(TH=='simple'){Q.strokeStyle='#7fb07a';Q.lineWidth=5;Q.stroke()}else{Q.save();Q.shadowColor='#78dcd2';Q.shadowBlur=14;Q.strokeStyle='#78dcd2';Q.lineWidth=3;Q.stroke();Q.restore()}}
function island(x,y,r){const tr=c=>{for(let i=0;i<=40;i++){const a=i/40*Math.PI*2;const rr=r*(1+.25*Math.sin(a*3+x)+.12*Math.sin(a*7+y));i?c.lineTo(x+Math.cos(a)*rr,y+Math.sin(a)*rr*.7):c.moveTo(x+rr,y)}c.closePath()};
 Q.beginPath();tr(Q);if(TH=='fantasy'){Q.fillStyle='rgba(236,220,178,.6)';Q.fill();Q.strokeStyle=INK;Q.lineWidth=1.8;Q.stroke()}else if(TH=='simple'){Q.fillStyle='#e8eed1';Q.fill();Q.strokeStyle='#7fb07a';Q.lineWidth=3;Q.stroke()}else{Q.fillStyle='#101b24';Q.fill();Q.strokeStyle='#78dcd2';Q.lineWidth=2;Q.stroke()}}
// ---------- terrain ----------
function peak(x,y,s){const h=s*1.25;
 if(TH=='fantasy'){Q.fillStyle='#ecd9ab';Q.beginPath();Q.moveTo(x-s,y);Q.lineTo(x-s*.1,y-h);Q.lineTo(x+s*.15,y-h*.92);Q.lineTo(x+s,y);Q.closePath();Q.fill();Q.strokeStyle=inkA(.85);Q.lineWidth=1;for(let k=1;k<8;k++){const u=k/8;Q.beginPath();Q.moveTo(x+s*.15*u-s*.1*(1-u),y-h*(1-u));Q.lineTo(x+s*u*.95,y);Q.stroke()}Q.lineWidth=2;Q.strokeStyle=INK;Q.beginPath();Q.moveTo(x-s,y);Q.lineTo(x-s*.1,y-h);Q.lineTo(x+s*.15,y-h*.92);Q.lineTo(x+s,y);Q.stroke()}
 else if(TH=='simple'){Q.fillStyle='#b9ab95';Q.beginPath();Q.moveTo(x-s,y);Q.lineTo(x,y-h);Q.lineTo(x+s,y);Q.fill();Q.fillStyle='#a0927c';Q.beginPath();Q.moveTo(x,y-h);Q.lineTo(x+s,y);Q.lineTo(x+s*.25,y);Q.fill();Q.fillStyle='#fff';Q.beginPath();Q.moveTo(x-s*.28,y-h*.72);Q.lineTo(x,y-h);Q.lineTo(x+s*.28,y-h*.72);Q.fill()}
 else{Q.strokeStyle='rgba(120,220,210,.55)';Q.lineWidth=1.4;[1,.62,.3].forEach(k=>{Q.beginPath();Q.moveTo(x-s*k,y-h*(1-k)*.6);Q.lineTo(x,y-h*(1-(1-k)*.4));Q.lineTo(x+s*k,y-h*(1-k)*.6);Q.stroke()})}}
function treeAt(x,y,s){if(TH=='fantasy'){Q.fillStyle='#e6d2a2';Q.strokeStyle=inkA(.85);Q.lineWidth=1.1;Q.beginPath();Q.arc(x,y,s,Math.PI,0);Q.quadraticCurveTo(x+s,y+s*.6,x,y+s*.5);Q.quadraticCurveTo(x-s,y+s*.6,x-s,y);Q.fill();Q.stroke()}
 else if(TH=='simple'){Q.fillStyle='#8cc27e';Q.beginPath();Q.arc(x,y,s*1.5,0,7);Q.fill();Q.fillStyle='#6fa863';Q.beginPath();Q.arc(x+s*.4,y+s*.3,s*.7,0,7);Q.fill()}
 else{Q.fillStyle='rgba(80,200,150,.35)';Q.beginPath();Q.arc(x,y,s*.55,0,7);Q.fill()}}
function forest(cx,cy,rx,ry,n,s0=5){const T=[];for(let i=0;i<n;i++){const a=R()*Math.PI*2,r=Math.sqrt(R());T.push([cx+Math.cos(a)*rx*r,cy+Math.sin(a)*ry*r])}T.sort((a,b)=>a[1]-b[1]).forEach(([x,y])=>treeAt(x,y,s0+R()*3))}
function hill(x,y,s){if(TH=='fantasy'){Q.strokeStyle=inkA(.7);Q.lineWidth=1.4;Q.beginPath();Q.arc(x,y,s,Math.PI*1.08,Math.PI*1.92);Q.stroke();for(let k=0;k<3;k++){Q.beginPath();Q.moveTo(x+s*(.15+k*.22),y-s*(.75-k*.18));Q.lineTo(x+s*(.25+k*.22),y-s*(.25-k*.1));Q.lineWidth=1;Q.stroke()}}
 else if(TH=='simple'){Q.strokeStyle='rgba(120,160,90,.45)';Q.lineWidth=2;Q.beginPath();Q.arc(x,y,s,Math.PI*1.1,Math.PI*1.9);Q.stroke()}
 else{Q.strokeStyle='rgba(120,220,210,.18)';Q.lineWidth=1;Q.beginPath();Q.arc(x,y,s*1.4,Math.PI*1.1,Math.PI*1.9);Q.stroke();Q.beginPath();Q.arc(x,y,s*.8,Math.PI*1.1,Math.PI*1.9);Q.stroke()}}
const chain=(pts,n,sz,wd=70)=>{const out=[];for(let i=0;i<n;i++){const u=i/(n-1);const f=u*(pts.length-1),j=Math.min(pts.length-2,Math.floor(f)),w=f-j;const dx=pts[j+1][0]-pts[j][0],dy=pts[j+1][1]-pts[j][1],L=Math.hypot(dx,dy);const lat=(R()-.5)*wd*(1-Math.abs(u-.5));out.push([pts[j][0]+dx*w-dy/L*lat+(R()-.5)*14,pts[j][1]+dy*w+dx/L*lat+(R()-.5)*10,sz*(.55+R()*.6)*(1.1-.6*Math.abs(u-.5))])}return out};
const wig=(pts,a=6)=>{const o=[];for(let i=0;i<pts.length-1;i++){for(let k=0;k<6;k++){const u=k/6;o.push([pts[i][0]+(pts[i+1][0]-pts[i][0])*u+Math.sin((i*6+k)*1.9)*a,pts[i][1]+(pts[i+1][1]-pts[i][1])*u+Math.cos((i*6+k)*1.3)*a*.8])}}o.push(pts[pts.length-1]);return o};
function river(pts,w){const col=TH=='fantasy'?INK:TH=='simple'?'#6fb6e2':'#50aaff';const mul=TH=='simple'?1.8:1;if(TH=='modern'){Q.save();Q.shadowColor='#50aaff';Q.shadowBlur=8}
 for(let i=1;i<pts.length;i++){Q.strokeStyle=col;Q.lineWidth=w*mul*(.35+.65*i/pts.length);Q.lineCap='round';Q.beginPath();Q.moveTo(...pts[i-1]);Q.lineTo(...pts[i]);Q.stroke()}if(TH=='modern')Q.restore()}
// ---------- settlements ----------
function castleIcon(x,y,big){if(TH=='fantasy'){Q.fillStyle='#ecd9ab';Q.strokeStyle=INK;Q.lineWidth=1.8;const w=big?34:18;Q.beginPath();Q.rect(x-w/2,y-12,w,12);Q.fill();Q.stroke();for(let k=0;k<(big?3:2);k++){const tx=x-w/2+3+k*((w-6)/((big?3:2)-1));Q.beginPath();Q.rect(tx-4,y-24,8,12);Q.fill();Q.stroke();Q.beginPath();Q.moveTo(tx-5,y-24);Q.lineTo(tx,y-32);Q.lineTo(tx+5,y-24);Q.stroke()}}
 else if(TH=='simple'){Q.fillStyle='#fff';Q.beginPath();Q.arc(x,y-8,big?16:11,0,7);Q.fill();Q.lineWidth=big?6:5;Q.strokeStyle='#33363d';Q.stroke();if(big){Q.fillStyle='#33363d';Q.beginPath();Q.arc(x,y-8,6,0,7);Q.fill()}}
 else{Q.strokeStyle='#cfe8ef';Q.lineWidth=3;const s=big?12:8;Q.strokeRect(x-s,y-8-s,2*s,2*s);if(big){Q.fillStyle='#cfe8ef';Q.fillRect(x-4,y-12,8,8)}}}
function house(x,y,s){if(TH=='fantasy'){Q.fillStyle='#ecd9ab';Q.strokeStyle=INK;Q.lineWidth=1.5;Q.beginPath();Q.rect(x-s,y-s*.7,2*s,s*1.4);Q.fill();Q.stroke();Q.beginPath();Q.moveTo(x-s-3,y-s*.7);Q.lineTo(x,y-s*1.6);Q.lineTo(x+s+3,y-s*.7);Q.closePath();Q.fill();Q.stroke()}
 else if(TH=='simple'){Q.fillStyle='#fbf6ec';Q.strokeStyle='#8a7f70';Q.lineWidth=1.5;Q.beginPath();Q.rect(x-s,y-s*.7,2*s,s*1.4);Q.fill();Q.stroke();Q.fillStyle='#d77a5a';Q.beginPath();Q.moveTo(x-s-3,y-s*.7);Q.lineTo(x,y-s*1.6);Q.lineTo(x+s+3,y-s*.7);Q.closePath();Q.fill()}
 else{Q.fillStyle='rgba(207,232,239,.18)';Q.strokeStyle='rgba(207,232,239,.75)';Q.lineWidth=1.4;Q.beginPath();Q.rect(x-s,y-s,2*s,2*s);Q.fill();Q.stroke()}}
function tower(x,y){if(TH=='modern'){Q.strokeStyle='#cfe8ef';Q.lineWidth=3;Q.strokeRect(x-12,y-24,24,24);Q.beginPath();Q.moveTo(x-12,y-24);Q.lineTo(x+12,y);Q.moveTo(x+12,y-24);Q.lineTo(x-12,y);Q.stroke();return}
 Q.fillStyle=TH=='fantasy'?'#ecd9ab':'#fbf6ec';Q.strokeStyle=TH=='fantasy'?INK:'#8a7f70';Q.lineWidth=1.8;Q.beginPath();Q.rect(x-9,y-40,18,40);Q.fill();Q.stroke();Q.fillStyle=TH=='fantasy'?'#ecd9ab':'#b45a40';Q.beginPath();Q.moveTo(x-12,y-40);Q.lineTo(x,y-62);Q.lineTo(x+12,y-40);Q.closePath();Q.fill();Q.stroke()}
// ---------- text & furniture ----------
function spaced(txt,x,y,font,col,rot=0,sp=0,ctx=Q){if(TT.up)txt=txt.toUpperCase();ctx.save();ctx.translate(x,y);ctx.rotate(rot);ctx.font=font;ctx.fillStyle=col;const ch=[...txt];const w=ch.reduce((s,c)=>s+ctx.measureText(c).width+sp,0)-sp;let cx=-w/2;ctx.lineWidth=7;ctx.lineJoin='round';ctx.strokeStyle=TT.halo;let hx=cx;ch.forEach(c=>{ctx.strokeText(c,hx,0);hx+=ctx.measureText(c).width+sp});ch.forEach(c=>{ctx.fillText(c,cx,0);cx+=ctx.measureText(c).width+sp});ctx.restore()}
function compass(x,y,r){Q.save();Q.translate(x,y);
 if(TH=='fantasy'){Q.strokeStyle=INK;Q.lineWidth=1.6;[1,.86,.3].forEach(k=>{Q.beginPath();Q.arc(0,0,r*k,0,7);Q.stroke()});for(let k=0;k<8;k++){const a=k*Math.PI/4-Math.PI/2,L=k%2?r*.6:r*1.12;[1,-1].forEach(s=>{Q.fillStyle=s>0?INK:'#ecd9ab';Q.beginPath();Q.moveTo(Math.cos(a)*L,Math.sin(a)*L);Q.lineTo(Math.cos(a+s*Math.PI/2)*r*.11,Math.sin(a+s*Math.PI/2)*r*.11);Q.lineTo(0,0);Q.closePath();Q.fill();Q.stroke()})}}
 else if(TH=='simple'){Q.fillStyle='#fff';Q.beginPath();Q.arc(0,0,r*.8,0,7);Q.fill();Q.fillStyle='#e0453a';Q.beginPath();Q.moveTo(0,-r*.6);Q.lineTo(r*.22,0);Q.lineTo(-r*.22,0);Q.fill();Q.fillStyle='#33363d';Q.beginPath();Q.moveTo(0,r*.6);Q.lineTo(r*.22,0);Q.lineTo(-r*.22,0);Q.fill()}
 else{Q.strokeStyle='#cfe8ef';Q.lineWidth=2;Q.beginPath();Q.arc(0,0,r*.7,0,7);Q.stroke();Q.beginPath();Q.moveTo(0,-r);Q.lineTo(0,r);Q.moveTo(-r,0);Q.lineTo(r,0);Q.stroke()}
 Q.restore();Q.fillStyle=INK;Q.font=TT.L(TH=='fantasy'?30:24);Q.textAlign='center';Q.fillText('N',x,y-r-(TH=='simple'?2:18));Q.textAlign='left'}
function titleBox(x,y,w,h,l1,l2){
 if(TH=='fantasy'){Q.fillStyle='rgba(236,220,178,.94)';Q.strokeStyle=INK;Q.lineWidth=2.4;Q.beginPath();Q.roundRect(x,y,w,h,20);Q.fill();Q.stroke();Q.strokeRect(x+12,y+12,w-24,h-24);[[x,y],[x+w,y],[x,y+h],[x+w,y+h]].forEach(([cx,cy])=>{Q.beginPath();Q.arc(cx,cy,16,0,7);Q.fillStyle='#ecd9ab';Q.fill();Q.stroke();Q.beginPath();Q.arc(cx,cy,7,0,7);Q.stroke()});
  Q.fillStyle=INK;Q.textAlign='center';Q.font=TT.T(44);Q.fillText(l1,x+w/2,y+h/2-8);Q.font=TT.I(26);Q.fillText(l2,x+w/2,y+h/2+32);Q.textAlign='left'}
 else if(TH=='simple'){Q.fillStyle='#fff';Q.beginPath();Q.roundRect(x,y,w,h,30);Q.fill();Q.fillStyle='#33363d';Q.font=TT.T(56);Q.fillText(l1,x+40,y+h/2+6);Q.fillStyle='#7a8190';Q.font='500 30px Inter';Q.fillText(l2,x+40,y+h/2+48)}
 else{Q.fillStyle='rgba(7,11,16,.9)';Q.fillRect(x,y,w,h);Q.strokeStyle='#4fb3ff';Q.lineWidth=3;[[x,y,1,1],[x+w,y,-1,1],[x,y+h,1,-1],[x+w,y+h,-1,-1]].forEach(([cx,cy,a,b])=>{Q.beginPath();Q.moveTo(cx,cy+30*b);Q.lineTo(cx,cy);Q.lineTo(cx+30*a,cy);Q.stroke()});Q.fillStyle='#cfe8ef';Q.font=TT.T(48);Q.fillText(l1.toUpperCase(),x+34,y+h/2+4);Q.fillStyle='#7fa3b4';Q.font=TT.I(22);Q.fillText(l2.toUpperCase(),x+34,y+h/2+44)}}
function frameEdge(){if(TH=='fantasy'){const g=Q.createRadialGradient(540,960,700,540,960,1120);g.addColorStop(0,'rgba(60,35,10,0)');g.addColorStop(1,'rgba(60,35,10,.55)');Q.fillStyle=g;Q.fillRect(0,0,1080,1920);Q.strokeStyle=INK;Q.lineWidth=5;Q.strokeRect(22,22,1036,1876);Q.lineWidth=1.4;Q.strokeRect(36,36,1008,1848)}
 else if(TH=='modern'){Q.strokeStyle='#4fb3ff';Q.lineWidth=4;[[30,30,1,1],[1050,30,-1,1],[30,1890,1,-1],[1050,1890,-1,-1]].forEach(([x,y,a,b])=>{Q.beginPath();Q.moveTo(x,y+60*b);Q.lineTo(x,y);Q.lineTo(x+60*a,y);Q.stroke()})}}
function panel(ctx,x,y,w,h){ctx.fillStyle=TT.panel;if(TH=='simple'){ctx.beginPath();ctx.roundRect(x,y,w,h,24);ctx.fill();return}ctx.fillRect(x,y,w,h);ctx.strokeStyle=TH=='fantasy'?INK:'rgba(79,179,255,.8)';ctx.lineWidth=1.6;ctx.strokeRect(x,y,w,h);if(TH=='fantasy')ctx.strokeRect(x+6,y+6,w-12,h-12)}
// ---------- troops ----------
function shape(ctx,type,x,y,ang,s){ctx.beginPath();if(type=='inf'||type=='gen'){ctx.save();ctx.translate(x,y);ctx.rotate(ang);ctx.rect(-s,-s*(type=='gen'?.7:1),2*s,2*s*(type=='gen'?.7:1));ctx.restore()}
 else if(type=='arc'){ctx.arc(x,y,s,0,7)}else{const c=Math.cos(ang),sn=Math.sin(ang);const P=[[s*1.35,0],[-s*.9,-s*1.05],[-s*.9,s*1.05]].map(([u,v])=>[x+u*c-v*sn,y+u*sn+v*c]);ctx.moveTo(...P[0]);ctx.lineTo(...P[1]);ctx.lineTo(...P[2]);ctx.closePath()}}
function troop(u,c,s,t){const dt=u.die==null?-1:t-u.die;if(dt>.55)return;const k=dt>=0?1-dt/.55:1;const ga=X.globalAlpha;X.globalAlpha=ga*k;const ss=s*Math.max(.05,k);
 if(TH=='fantasy'){shape(X,u.type,u.x,u.y,u.ang,ss);X.fillStyle='rgba(239,224,184,.95)';X.fill();X.lineWidth=2.6;X.strokeStyle=c;X.stroke();shape(X,u.type,u.x,u.y,u.ang,ss*.42);X.fillStyle=c;X.fill()}
 else if(TH=='simple'){shape(X,u.type,u.x,u.y,u.ang,ss);X.fillStyle=c;X.fill();X.lineWidth=2.6;X.strokeStyle='#fff';X.stroke()}
 else{X.save();X.shadowColor=c;X.shadowBlur=10;shape(X,u.type,u.x,u.y,u.ang,ss);X.fillStyle='rgba(7,11,16,.85)';X.fill();X.lineWidth=3;X.strokeStyle=c;X.stroke();X.restore()}
 if(dt>=0){X.globalAlpha=ga*k;X.strokeStyle=TH=='fantasy'?INK:TH=='simple'?'#33363d':c;X.lineWidth=2;for(let i=0;i<6;i++){const a=i/6*Math.PI*2+u.x;const r1=s*.6+dt*30,r2=s*1.1+dt*46;X.beginPath();X.moveTo(u.x+Math.cos(a)*r1,u.y+Math.sin(a)*r1);X.lineTo(u.x+Math.cos(a)*r2,u.y+Math.sin(a)*r2);X.stroke()}}
 X.globalAlpha=ga}
function burst(x,y,s,t,col=TT.mark){X.save();X.translate(x,y);X.scale(s,s);X.strokeStyle=col;X.lineWidth=TH=='fantasy'?2:3;for(let i=0;i<16;i++){const a=i/16*Math.PI*2+(TH=='modern'?t:0);X.beginPath();X.moveTo(Math.cos(a)*44,Math.sin(a)*44);X.lineTo(Math.cos(a)*(80+(i%2)*26),Math.sin(a)*(80+(i%2)*26));X.stroke()}X.restore()}
const lerp2=(a,b,f)=>[a[0]+(b[0]-a[0])*f,a[1]+(b[1]-a[1])*f];
function kf(K,t){if(t<=K[0][0])return[K[0][1],K[0][2],Math.atan2(K[1][2]-K[0][2],K[1][1]-K[0][1])];for(let i=1;i<K.length;i++){if(t<=K[i][0]){const f=eio((t-K[i-1][0])/(K[i][0]-K[i-1][0]));return[K[i-1][1]+(K[i][1]-K[i-1][1])*f,K[i-1][2]+(K[i][2]-K[i-1][2])*f,Math.atan2(K[i][2]-K[i-1][2],K[i][1]-K[i-1][1])]}}const n=K.length-1;return[K[n][1],K[n][2],Math.atan2(K[n][2]-K[n-1][2],K[n][1]-K[n-1][1])]}
const BGC={fantasy:'#7d5a2c',simple:'#a9d4ef',modern:'#070b10'}[TH];
'''

# ---------------- campaign geography (shared with territory) ----------------
CGEO=r'''
const coast=[];for(let i=0;i<=900;i++){const u=i/900;const y=40+u*1840;const x=150+70*Math.sin(u*9+.5)+40*Math.sin(u*23+1.1)+16*Math.sin(u*61)+(u>.78?(u-.78)*900:0);coast.push([x,y])}
const coastX=y=>{const i=Math.max(0,Math.min(900,Math.round((y-40)/1840*900)));return coast[i][0]};
const lineTrace=c=>{coast.forEach((p,i)=>i?c.lineTo(...p):c.moveTo(...p))};
const fillTrace=c=>{c.moveTo(1080,40);c.lineTo(coast[0][0],coast[0][1]);coast.forEach(p=>c.lineTo(...p));c.lineTo(1080,1880);c.closePath()};
const TOWNS=[['Aldmere',560,330,1],['Westwatch',300,620,0],['Highcairn',720,780,0],['Ravensford',930,520,0],['Tollbridge',480,900,0],
 ['Karth',640,1680,1],['Saltmoor',300,1420,0],['Dunhallow',840,1500,0],['Greyfen',480,1230,0],['Embers',940,1150,0]];
let PK=[];
function drawCampaignLand(){seaBg();coastFill(fillTrace,lineTrace);[[80,400,20],[95,450,11],[70,1150,24],[300,1820,30],[420,1850,16]].forEach(i=>island(...i))}
function drawCampaignFeatures(opts={}){R=rng(29);
 river(wig([[700,300],[660,420],[600,520],[560,640],[470,760],[380,880],[300,960],[230,1010]]),5);
 river(wig([[900,1000],[860,1080],[820,1180],[720,1260],[640,1340],[600,1440],[560,1560],[520,1700],[500,1800]]),5);
 river(wig([[420,1180],[480,1250],[560,1300],[640,1340]]),2.5);
 PK=[...chain([[260,160],[380,190],[520,170],[660,200]],60,20,60),...chain([[760,560],[850,700],[900,860]],60,24,80),...chain([[300,1300],[340,1420],[330,1560]],40,18,50),...chain([[700,1560],[820,1620],[960,1600]],38,17,40)];
 forest(400,520,110,70,TH=='simple'?120:260);forest(860,380,110,90,TH=='simple'?120:260);forest(600,1060,120,70,TH=='simple'?120:260);forest(260,1560,70,90,TH=='simple'?70:140);forest(880,1380,90,70,TH=='simple'?80:160);
 const HL=[];for(let i=0;i<220;i++)HL.push([200+R()*840,120+R()*1700,8+R()*6]);
 HL.forEach(h=>{if(PK.every(([a,b])=>Math.hypot(h[0]-a,h[1]-b)>24)&&h[0]>coastX(h[1])+20)hill(...h)});
 PK.slice().sort((a,b)=>a[1]-b[1]).forEach(p=>peak(...p));
 coastLine(lineTrace);
 if(opts.border){const pts=[[170,1000],[330,960],[480,980],[640,940],[760,990],[900,960],[1050,980]];Q.setLineDash([3,9]);Q.strokeStyle=TH=='modern'?'rgba(207,232,239,.6)':inkA(.75);Q.lineWidth=3;Q.beginPath();pts.forEach((p,i)=>i?Q.lineTo(...p):Q.moveTo(...p));Q.stroke();Q.setLineDash([])}
 TOWNS.forEach(([n,x,y,b])=>castleIcon(x,y,b));if(opts.labels!==false)drawCampaignLabels();}
function drawCampaignLabels(){TOWNS.forEach(([n,x,y,b])=>spaced(n,x,y+30,TT.L(b?28:22),INK));
 spaced('the Iron Teeth',870,840,TT.L(22),inkA(.8),1.1,TH=='fantasy'?6:2);spaced('the Ashwood',600,1150,TT.I(24),INK);spaced('Mirkenwood',860,300,TT.L(24),INK);
 spaced('The Sundered Sea',110,780,TT.L(30),inkA(TH=='simple'?.5:.55),-1.5,TH=='fantasy'?10:6);}
'''

CAMPAIGN=r'''
drawCampaignLand();drawCampaignFeatures({border:true});
spaced('Kingdom of Aldmere',640,700,TT.L(38),inkA(.5),-.05,TH=='fantasy'?10:4);spaced('Realm of Karth',700,1430,TT.L(38),inkA(.5),-.05,TH=='fantasy'?10:4);
compass(130,1700,62);titleBox(500,60,520,150,'The Two Crowns','the campaign of the Year of Ash');frameEdge();
const BLOCK=[];for(let r=0;r<3;r++)for(let c=0;c<4;c++)BLOCK.push([-r*24,(c-1.5)*24]);
const ARMIES=[[0,BLUE,[[1.2,560,360],[2.6,500,640],[4.4,470,975]]],[0,BLUE,[[1.4,300,650],[3.2,290,840],[4.6,330,990]]],[0,BLUE,[[1.2,720,800],[2.8,790,960],[4.3,840,1110]]],
 [1,RED,[[1.2,480,1240],[3.0,430,1130],[4.5,400,1060]]],[1,RED,[[1.2,960,1170],[2.6,950,1160],[4.3,925,1150]]],[1,RED,[[1.4,840,1500],[3.0,800,1330],[4.7,800,1185]]]];
const SITES=[[400,1025],[860,1140]];const LOSS=[4,4,11,10,4,4];const r2=rng(7);
const UNITS=ARMIES.map((A,ai)=>{const [side,c,K]=A;const nl=LOSS[ai];const order=BLOCK.map((b,i)=>i).sort((a,b)=>BLOCK[a][0]===BLOCK[b][0]?r2()-.5:BLOCK[b][0]-BLOCK[a][0]);const die={};order.slice(0,nl).forEach((i,k)=>die[i]=5.0+k*(3.4/nl)+r2()*.2);return{side,c,K,die}});
window.DUR=10;
window.render=t=>{X.fillStyle=BGC;X.fillRect(0,0,1080,1920);X.globalAlpha=Math.min(1,eio(pr(t,0,1))*1.4);X.drawImage(M,0,0);X.globalAlpha=1;
 SITES.forEach(([x,y])=>{const cp=pr(t,4.8,.6);if(cp>0)burst(x,y,eob(Math.min(1,cp)),t)});
 UNITS.forEach(A=>{const [x,y,ang]=kf(A.K,t);const fight=pr(t,4.8,4);
  X.setLineDash([3,10]);X.strokeStyle=A.c;X.globalAlpha=.55;X.lineWidth=3;X.beginPath();A.K.forEach(([kt,kx,ky],i)=>{if(kt<=t||i==0){i?X.lineTo(kx,ky):X.moveTo(kx,ky)}});X.lineTo(x,y);X.stroke();X.setLineDash([]);X.globalAlpha=1;
  if(t<A.K[0][0]-.3)return;X.globalAlpha=eo(pr(t,A.K[0][0]-.3,.4));
  BLOCK.forEach(([bx,by],i)=>{const c=Math.cos(ang),s=Math.sin(ang);let ux=x+bx*c-by*s,uy=y+bx*s+by*c;if(fight>0){ux+=Math.sin(t*8+i*1.9)*4*Math.min(1,fight*3);uy+=Math.cos(t*7+i*1.3)*4*Math.min(1,fight*3)}troop({x:ux,y:uy,ang,type:'gen',die:A.die[i]},A.c,11,t)});X.globalAlpha=1});
 const ra=eo(pr(t,8.6,.6));if(ra>0){X.globalAlpha=ra;spaced('Aldmere holds the West',400,1180,TT.L(30),BLUE,0,0,X);spaced('Karth breaks the East',840,1280,TT.L(30),RED,0,0,X);X.globalAlpha=1}
 panel(X,60,250,330,150);[[BLUE,'Aldmere',300],[RED,'Karth',350]].forEach(([c,n,y])=>{troop({x:95,y:y-9,ang:0,type:'gen'},c,13,t);X.fillStyle=INK;X.font=TT.L(26);X.fillText(TT.up?n.toUpperCase():n,125,y)});
 X.font=TT.I(20);X.fillStyle=INK;X.fillText(TT.up?'EACH MARK = 1 COMPANY':'each mark, one company',95,385)};
'''

BRIDGE=r'''
groundBg();R=rng(29);
const RY=x=>960+50*Math.sin((x-540)/170)+8*Math.sin(x/37);const RW=x=>34+6*Math.sin(x/90);
const field=(x,y,w,h,a)=>{Q.save();Q.translate(x,y);Q.rotate(a);if(TH=='simple'){Q.fillStyle='#f1e7b4';Q.fillRect(-w/2,-h/2,w,h);Q.strokeStyle='#d8c98a';Q.lineWidth=2;Q.strokeRect(-w/2,-h/2,w,h);Q.strokeStyle='rgba(200,180,110,.6)';Q.lineWidth=1.5;for(let k=-w/2+10;k<w/2;k+=12){Q.beginPath();Q.moveTo(k,-h/2);Q.lineTo(k,h/2);Q.stroke()}}
 else if(TH=='fantasy'){Q.strokeStyle=inkA(.55);Q.lineWidth=1.4;Q.strokeRect(-w/2,-h/2,w,h);Q.lineWidth=.9;Q.strokeStyle=inkA(.3);for(let k=-w/2+8;k<w/2;k+=9){Q.beginPath();Q.moveTo(k,-h/2);Q.lineTo(k,h/2);Q.stroke()}}
 else{Q.setLineDash([6,6]);Q.strokeStyle='rgba(120,200,190,.35)';Q.lineWidth=1.5;Q.strokeRect(-w/2,-h/2,w,h);Q.setLineDash([])}Q.restore()};
[[260,520,170,110,.1],[820,540,180,120,-.08],[820,700,140,90,.15],[250,1420,180,110,-.1],[820,1380,170,120,.12],[830,1560,140,100,-.05],[300,1250,120,80,.2]].forEach(f=>field(...f));
const road=(pts)=>{if(TH=='simple'){Q.strokeStyle='#d5d0bd';Q.lineWidth=14;Q.lineCap='round';Q.lineJoin='round';Q.beginPath();pts.forEach((p,i)=>i?Q.lineTo(...p):Q.moveTo(...p));Q.stroke();Q.strokeStyle='#fff';Q.lineWidth=9;Q.stroke()}
 else if(TH=='fantasy'){[-7,7].forEach(o=>{Q.strokeStyle=inkA(.55);Q.lineWidth=1.4;Q.beginPath();pts.forEach(([x,y],i)=>i?Q.lineTo(x+o,y):Q.moveTo(x+o,y));Q.stroke()})}
 else{Q.setLineDash([10,10]);Q.strokeStyle='rgba(200,210,220,.4)';Q.lineWidth=3;Q.beginPath();pts.forEach((p,i)=>i?Q.lineTo(...p):Q.moveTo(...p));Q.stroke();Q.setLineDash([])}};
road([[540,380],[545,560],[535,760],[540,900]]);road([[540,1020],[530,1200],[548,1380],[540,1540]]);road([[540,560],[380,600],[230,640]]);road([[540,1380],[700,1340],[860,1300]]);
// river band
Q.beginPath();for(let x=40;x<=1040;x+=6)Q.lineTo(x,RY(x)-RW(x));for(let x=1040;x>=40;x-=6)Q.lineTo(x,RY(x)+RW(x));Q.closePath();Q.fillStyle=TH=='fantasy'?'rgba(150,160,150,.28)':TH=='simple'?'#a9d4ef':'rgba(40,110,180,.35)';Q.fill();
[-1,1].forEach(s=>{Q.beginPath();for(let x=40;x<=1040;x+=6){const y=RY(x)+s*RW(x);x==40?Q.moveTo(x,y):Q.lineTo(x,y)}Q.strokeStyle=TH=='fantasy'?INK:TH=='simple'?'#6fb6e2':'#50aaff';Q.lineWidth=TH=='simple'?4:2.6;Q.stroke()});
for(let k=-2;k<=2;k++){Q.setLineDash([18,14]);Q.strokeStyle=TH=='fantasy'?inkA(.28):TH=='simple'?'rgba(255,255,255,.6)':'rgba(80,170,255,.35)';Q.lineWidth=1;Q.beginPath();for(let x=40;x<=1040;x+=6){const y=RY(x)+k*11;x==40?Q.moveTo(x,y):Q.lineTo(x,y)}Q.stroke()}Q.setLineDash([]);
const FX=230;for(let k=0;k<7;k++){Q.fillStyle=TH=='modern'?'#1b2a36':TH=='simple'?'#d9d4c4':'#ecd9ab';Q.strokeStyle=TH=='modern'?'#cfe8ef':TH=='simple'?'#8a7f70':INK;Q.lineWidth=1.4;Q.beginPath();Q.ellipse(FX-20+((k%2)*30),RY(FX)-RW(FX)+8+k*10,9,5,0,0,7);Q.fill();Q.stroke()}
{const x0=505,x1=575,y0=RY(540)-RW(540)-14,y1=RY(540)+RW(540)+14;Q.fillStyle=TH=='modern'?'#1b2a36':TH=='simple'?'#cfc7b4':'#ecd9ab';Q.fillRect(x0,y0,x1-x0,y1-y0);Q.strokeStyle=TH=='modern'?'#cfe8ef':TH=='simple'?'#7a6f60':INK;Q.lineWidth=3;Q.strokeRect(x0,y0,x1-x0,y1-y0);
 Q.lineWidth=1;Q.strokeStyle=TH=='modern'?'rgba(207,232,239,.4)':TH=='simple'?'rgba(122,111,96,.5)':inkA(.6);for(let y=y0+8;y<y1;y+=9){Q.beginPath();Q.moveTo(x0+4,y);Q.lineTo(x1-4,y);Q.stroke()}
 [x0,x1].forEach(x=>{Q.lineWidth=5;Q.strokeStyle=TH=='modern'?'#cfe8ef':TH=='simple'?'#7a6f60':INK;Q.beginPath();Q.moveTo(x,y0-10);Q.lineTo(x,y1+10);Q.stroke();[y0-10,y1+10].forEach(y=>{Q.fillStyle=Q.strokeStyle;Q.fillRect(x-6,y-6,12,12)})})}
const near=(x,y)=>Math.abs(y-RY(x))<RW(x)+30||Math.abs(x-540)<60;
for(let i=0;i<120;i++){const x=70+R()*940,y=120+R()*1700;if(!near(x,y)&&Math.abs(y-960)>90&&Math.abs(x-540)>90)treeAt(x,y,6+R()*3)}
forest(170,330,90,70,TH=='simple'?60:120,6);forest(900,300,100,70,TH=='simple'?60:130,6);forest(900,1700,90,70,TH=='simple'?60:120,6);forest(160,1650,80,80,TH=='simple'?55:110,6);
for(let i=0;i<60;i++){const x=80+R()*920,y=180+R()*1600;if(!near(x,y)&&Math.abs(x-540)>140&&Math.abs(y-960)>150)hill(x,y,8+R()*5)}
function town(cx,cy,seed){const r=rng(seed);const H=[];for(let i=0;i<26;i++){const a=r()*Math.PI*2,d=30+r()*110;H.push([cx+Math.cos(a)*d*1.3,cy+Math.sin(a)*d*.7,9+r()*5])}H.sort((a,b)=>a[1]-b[1]).forEach(h=>house(...h));tower(cx,cy+10);
 Q.setLineDash([2,5]);Q.strokeStyle=TH=='modern'?'rgba(207,232,239,.5)':TH=='simple'?'rgba(122,111,96,.6)':inkA(.6);Q.lineWidth=2;Q.beginPath();Q.ellipse(cx,cy,185,105,0,0,7);Q.stroke();Q.setLineDash([])}
town(540,300,4);town(540,1620,9);
spaced('Ashford',540,440,TT.T(40),INK,0,TH=='fantasy'?6:2);spaced('Harrowmere',540,1500,TT.T(40),INK,0,TH=='fantasy'?6:2);
spaced('the Stillwater',830,RY(830)+8,TT.I(28),INK,.15);spaced("Fowler's Ford",FX-80,RY(FX)+80,TT.I(24),INK);spaced('Old Bridge',650,RY(650)-52,TT.I(24),INK);
compass(950,1760,50);titleBox(70,60,600,150,'Ashford Bridge','the battle at the river crossing');frameEdge();
const SZ=13;const U=[];const mir=([x,y])=>[x,1920-y];
for(let side=0;side<2;side++){const Mf=side?mir:(p=>p);
 for(let r=0;r<3;r++)for(let c=0;c<5;c++)U.push({side,type:'inf',dep:Mf([540+(c-2)*32,820-r*32]),row:r,col:c});
 for(let r=0;r<2;r++)for(let c=0;c<5;c++)U.push({side,type:'arc',dep:Mf([540+(c-2)*40,700-r*34]),row:r,col:c});
 for(let k=0;k<6;k++)U.push({side,type:'cav',dep:Mf([230+(k%3-1)*34,780-Math.floor(k/3)*34]),idx:k})}
const colOrder=[2,1,3,0,4];U.forEach(u=>{if(u.type=='inf'&&u.row<2)u.colIdx=u.row*5+colOrder.indexOf(u.col)});
const sched=(list,times)=>list.forEach((u,i)=>{if(times[i]!=null)u.die=times[i]});
const col=s=>U.filter(u=>u.side==s&&u.colIdx!=null).sort((a,b)=>a.colIdx-b.colIdx);
sched(col(0),[5.9,6.8,7.7,8.5]);sched(col(1),[5.6,6.1,6.5,6.95,7.35,7.8,8.2,8.6,9.0]);
const arcs=s=>U.filter(u=>u.side==s&&u.type=='arc');sched(arcs(0),[null,null,4.3,null,null,null,7.1]);sched(arcs(1),[null,4.0,null,null,4.7,null,null,6.4,null,9.9]);
const res=s=>U.filter(u=>u.side==s&&u.type=='inf'&&u.row==2);sched(res(1),[3.8,null,9.7,null,10.2]);
const cav=s=>U.filter(u=>u.side==s&&u.type=='cav');sched(cav(1),[7.6,7.9,8.2,8.5,8.8,9.1]);sched(cav(0),[null,8.0,null,null,8.6]);
const BY=RY(540);
function pos(u,t){const s=u.side,sg=s?-1:1,Mf=s?mir:(p=>p);const town=Mf([540+(u.dep[0]-540)*.3,420]);const d=eio(pr(t,1.0+(u.type=='cav'?.2:0),2.0));let [x,y]=lerp2(town,u.dep,d);let ang=s?-Math.PI/2:Math.PI/2;
 if(u.colIdx!=null){let slot=u.colIdx;col(s).forEach(v=>{if(v.colIdx<u.colIdx&&v.die!=null)slot-=eo(pr(t,v.die,.6))});let front=BY-sg*14;if(s==0)front+=eio(pr(t,9.3,1.3))*190;
  const tgt=[540+(Math.round(slot)%2?16:-16),front-sg*Math.floor(slot/2+.001)*30];const k=eio(pr(t,4.6+u.colIdx*.05,1.2));[x,y]=lerp2([x,y],tgt,k);
  if(t>5.5&&slot<2){x+=Math.sin(t*11+u.colIdx)*3;y+=Math.cos(t*9+u.colIdx)*3}if(s==1&&u.die==null){const r=eio(pr(t,9.3,1.4));[x,y]=lerp2([x,y],[600,1300],r);ang=Math.PI/2}}
 if(u.type=='cav'){const ford=[FX,RY(FX)];if(s==1){const k=eio(pr(t,6.0,1.5));[x,y]=lerp2([x,y],[ford[0]+(u.idx%3-1)*28,ford[1]-10-Math.floor(u.idx/3)*26],k)}
  else{const k=eio(pr(t,6.1,1.3));[x,y]=lerp2([x,y],[ford[0]+(u.idx%3-1)*30,ford[1]-80-Math.floor(u.idx/3)*28],k);const k2=eio(pr(t,9.3,1.4));[x,y]=lerp2([x,y],[300+(u.idx%3)*34,1130+Math.floor(u.idx/3)*30],k2);if(k2>0&&k2<1)ang=Math.atan2(1130-ford[1],70)}
  if(t>7.4&&t<9.2){x+=Math.sin(t*10+u.idx)*4;y+=Math.cos(t*8+u.idx)*4}}
 if(s==1&&(u.type=='arc'||(u.type=='inf'&&u.row==2))){const r=eio(pr(t,9.4,1.6));y+=r*240;x+=(u.dep[0]-540)*r*.4}
 return[x,y,ang]}
const ARR=[];const ra=rng(41);[3.0,3.8,4.6,5.6,6.4,7.2,8.0].forEach(T0=>{[0,1].forEach(s=>{for(let k=0;k<10;k++)ARR.push({s,t0:T0+ra()*.25+(s?.35:0),k,tx:540+(ra()-.5)*200,ty:s?760+ra()*80:1100+ra()*90})})});
window.DUR=12;
window.render=t=>{X.fillStyle=BGC;X.fillRect(0,0,1080,1920);X.globalAlpha=Math.min(1,eio(pr(t,0,1))*1.4);X.drawImage(M,0,0);X.globalAlpha=1;
 ARR.forEach(a=>{const p=(t-a.t0)/.7;if(p<0||p>1)return;const sh=arcs(a.s)[a.k];if(!sh||(sh.die!=null&&sh.die<a.t0))return;const [sx,sy]=pos(sh,a.t0);const x=sx+(a.tx-sx)*p,y=sy+(a.ty-sy)*p;const dx=a.tx-sx,dy=a.ty-sy,L=Math.hypot(dx,dy);X.strokeStyle=a.s?RED:BLUE;X.lineWidth=2.6;X.globalAlpha=.9;X.beginPath();X.moveTo(x,y);X.lineTo(x-dx/L*24,y-dy/L*24);X.stroke();X.globalAlpha=1});
 [[540,BY,5.4,9.3],[FX,RY(FX)-45,7.4,9.2]].forEach(([x,y,a,b])=>{if(t<a||t>b+.4)return;X.globalAlpha=Math.min(1,(t-a)*3)*Math.min(1,(b+.4-t)*3);X.strokeStyle=TT.mark;X.lineWidth=TH=='fantasy'?2:3;for(let i=0;i<12;i++){const an=i/12*Math.PI*2+t*2;const r1=26,r2=46+((i+Math.floor(t*6))%2)*12;X.beginPath();X.moveTo(x+Math.cos(an)*r1,y+Math.sin(an)*r1);X.lineTo(x+Math.cos(an)*r2,y+Math.sin(an)*r2);X.stroke()}X.globalAlpha=1});
 X.globalAlpha=eo(pr(t,.9,.5));U.forEach(u=>{const [x,y,ang]=pos(u,t);troop({x,y,ang,type:u.type,die:u.die},u.side?RED:BLUE,SZ,t)});X.globalAlpha=1;
 const dead=s=>U.filter(u=>u.side==s&&u.die!=null&&u.die<=t).length;
 panel(X,60,1640,560,220);[['cav','Horsemen',1690],['inf','Footmen',1735],['arc','Bowmen',1780]].forEach(([ty,n,y])=>{troop({x:95,y:y-9,ang:0,type:ty},TH=='modern'?'#cfe8ef':TH=='simple'?'#6b7280':INK,12,t);X.fillStyle=INK;X.font=TT.L(TH=='fantasy'?24:22);X.fillText(TT.up?n.toUpperCase():n,125,y)});
 X.font=TT.I(TH=='fantasy'?28:22);X.fillStyle=BLUE;X.fillText((TT.up?'ASHFORD LOST: ':'Ashford fallen: ')+dead(0),300,1692);X.fillStyle=RED;X.fillText((TT.up?'HARROWMERE LOST: ':'Harrowmere fallen: ')+dead(1),300,1740);
 const fa=eo(pr(t,10.4,.6));if(fa>0){X.globalAlpha=fa;spaced('The bridge is taken',720,1240,TT.L(TH=='fantasy'?40:36),BLUE,0,0,X);X.globalAlpha=1}};
'''

TERRITORY=r'''
drawCampaignLand();
const F=mkC();Q=F.getContext('2d');drawCampaignFeatures({border:false,labels:false});const LBc=mkC();Q=LBc.getContext('2d');drawCampaignLabels();Q=M.getContext('2d');
// ---- smooth influence fields: each realm's strength falls off from its capital; the highest strength owns the ground ----
const G=4,GW=270,GH=480,NC=GW*GH;
const land=new Uint8Array(NC);for(let j=0;j<GH;j++)for(let i=0;i<GW;i++){const x=i*G+2,y=j*G+2;land[j*GW+i]=(x>=coastX(y)&&y>=40&&y<=1880)?1:0}
const NAT=CFG.nat;const NN=NAT.length;const EV=CFG.evil??-1;
const nz=(x,y,s)=>Math.sin(x/97+s)*.5+Math.sin(y/131+s*2)*.5+Math.sin((x+y)/61+s*3)*.25+Math.sin((x-y)/43+s)*.12;
const base=NAT.map(([n,cx,cy,w],k)=>{const a=new Float32Array(NC);for(let j=0;j<GH;j++)for(let i=0;i<GW;i++){const x=i*G+2,y=j*G+2;a[j*GW+i]=-Math.hypot(x-cx,(y-cy)*.9)/(170*w)+nz(x,y,k*1.7)*.2}return a});
// conquests: each push is a bump of strength that grows in, so the front line moves forward chunk by chunk
const PUSH=[];const addP=(nat,pts,t0,amp=2.6,sig=125)=>pts.forEach((p,i)=>PUSH.push({nat,x:p[0],y:p[1],t0:t0+i*.55,dur:.75,amp,sig,from:i?pts[i-1]:null}));
CFG.pushes.forEach(a=>addP(...a));const PH=CFG.phases;const ARROW_FROM=CFG.arrowFrom;
// ---- cities are anchors: each holds ground around itself for its owner, and only falls when the attacker clearly overwhelms it ----
const CITY=TOWNS.map(([n,x,y,b])=>({n,x,y,big:b,cell:Math.min(GH-1,Math.floor(y/G))*GW+Math.min(GW-1,Math.floor(x/G))}));
const pushAt=(k,x,y,t)=>PUSH.reduce((s,P)=>P.nat!=k?s:s+P.amp*eio(Math.max(0,Math.min(1,(t-P.t0)/P.dur)))*Math.exp(-(((x-P.x)**2+(y-P.y)**2)/(2*P.sig*P.sig))),0);
const HOLD=.6,ANC=1.6,AS=70;
CITY.forEach(c=>{const raw=t=>base.map((b,k)=>b[c.cell]+pushAt(k,c.x,c.y,t));const r0=raw(0);c.hist=[[0,r0.indexOf(Math.max(...r0))]];
 for(let s=1;s<=CFG.dur*30;s++){const tt=s/30;const r=raw(tt);const o=c.hist[c.hist.length-1][1];let b=o,bv=r[o]+HOLD;r.forEach((v,k)=>{if(v>bv){bv=v;b=k}});if(b!=o)c.hist.push([tt,b])}});
const cityOwner=(c,t)=>{let o=c.hist[0][1];c.hist.forEach(([tt,k])=>{if(t>=tt)o=k});return o};
const FALLS=[];CITY.forEach(c=>c.hist.slice(1).forEach(([tt,k],i)=>FALLS.push({c,t:tt,k,prev:c.hist[i][1]})));
const sev=new Float32Array(NC);const f=NAT.map(()=>new Float32Array(NC)),own=new Int8Array(NC),gap=new Float32Array(NC),fl=NAT.map(()=>new Float32Array(NC));
function solve(t){for(let k=0;k<NN;k++){f[k].set(base[k]);fl[k].fill(0)}
 CITY.forEach(c=>{const s2=2*AS*AS;let parts=[];let o=c.hist[0][1];let w=[];c.hist.forEach(([tt,k],i)=>{if(i==0)return;});
  const hs=c.hist;for(let i=0;i<hs.length;i++){const st=hs[i][0],k=hs[i][1],en=i+1<hs.length?hs[i+1][0]:1e9;const a=(i==0?1:eio(Math.min(1,(t-st)/.5)))*(t<en?1:Math.max(0,1-(t-en)/.5));if(t>=st-(i?0:1)&&a>0)parts.push([k,a*ANC])}
  const i0=Math.max(0,Math.floor((c.x-3*AS)/G)),i1=Math.min(GW-1,Math.ceil((c.x+3*AS)/G)),j0=Math.max(0,Math.floor((c.y-3*AS)/G)),j1=Math.min(GH-1,Math.ceil((c.y+3*AS)/G));
  for(let j=j0;j<=j1;j++)for(let i=i0;i<=i1;i++){const dx=i*G+2-c.x,dy=j*G+2-c.y;const e=Math.exp(-(dx*dx+dy*dy)/s2);parts.forEach(([k,a])=>{f[k][j*GW+i]+=a*e})}});
 PUSH.forEach(P=>{const a=P.amp*eio(Math.max(0,Math.min(1,(t-P.t0)/P.dur)));if(a<=0)return;const ff=f[P.nat],s2=2*P.sig*P.sig;const u=(t-P.t0)/(P.dur+.5),pulse=u>0&&u<1?Math.sin(u*Math.PI):0;const FL=fl[P.nat];const i0=Math.max(0,Math.floor((P.x-3*P.sig)/G)),i1=Math.min(GW-1,Math.ceil((P.x+3*P.sig)/G)),j0=Math.max(0,Math.floor((P.y-3*P.sig)/G)),j1=Math.min(GH-1,Math.ceil((P.y+3*P.sig)/G));
  for(let j=j0;j<=j1;j++)for(let i=i0;i<=i1;i++){const dx=i*G+2-P.x,dy=j*G+2-P.y;const e=Math.exp(-(dx*dx+dy*dy)/s2);ff[j*GW+i]+=a*e;if(pulse)FL[j*GW+i]=Math.max(FL[j*GW+i],pulse*e)}});
 for(let c=0;c<NC;c++){if(!land[c]){own[c]=-1;continue}let b=0,bv=-1e9,sv=-1e9;for(let k=0;k<NN;k++){const v=f[k][c];if(v>bv){sv=bv;bv=v;b=k}else if(v>sv)sv=v}own[c]=b;gap[c]=bv-sv;if(EV>=0){let m=-1e9;for(let k=0;k<NN;k++)if(k!=EV)m=Math.max(m,f[k][c]);sev[c]=f[EV][c]-m}}}
const parse=s=>{if(s[0]=='#'){const n=parseInt(s.slice(1),16);return[n>>16,n>>8&255,n&255,1]}const m=s.match(/[\d.]+/g).map(Number);return[m[0],m[1],m[2],m[3]??1]};
const NATC=TT.nat.map(parse),NATS=TT.natS.map(parse);
const low=document.createElement('canvas');low.width=GW;low.height=GH;const LX=low.getContext('2d');const img=LX.createImageData(GW,GH);
function paintFill(t,flash){for(let c=0;c<NC;c++){const o=own[c];const q=c*4;if(o<0||o==EV){img.data[q+3]=0;continue}let [r,g,b,a]=NATC[o];
  if(fl[o][c]>.02){const s=NATS[o];const w=.6*fl[o][c];r+=(s[0]-r)*w;g+=(s[1]-g)*w;b+=(s[2]-b)*w;a=Math.min(1,a+w*.5)}
  img.data[q]=r;img.data[q+1]=g;img.data[q+2]=b;img.data[q+3]=a*255}LX.putImageData(img,0,0)}
// marching squares on (own==k ? gap : -gap) gives smooth, rounded borders
function borderPath(){const p=new Path2D();const val=(c,k)=>own[c]<0?NaN:(own[c]==k?gap[c]:-gap[c]);
 for(let k=0;k<NN;k++)for(let j=0;j<GH-1;j++)for(let i=0;i<GW-1;i++){const c=j*GW+i;const a=val(c,k),b=val(c+1,k),d=val(c+GW,k),e=val(c+GW+1,k);if(a!==a||b!==b||d!==d||e!==e)continue;
  const idx=(a>0)|((b>0)<<1)|((e>0)<<2)|((d>0)<<3);if(idx==0||idx==15)continue;const x=i*G+2,y=j*G+2;
  const T=[a>0!=b>0?[x+G*a/(a-b),y]:null,b>0!=e>0?[x+G,y+G*b/(b-e)]:null,d>0!=e>0?[x+G*d/(d-e),y+G]:null,a>0!=d>0?[x,y+G*a/(a-d)]:null].filter(Boolean);
  for(let m=0;m+1<T.length;m+=2){p.moveTo(...T[m]);p.lineTo(...T[m+1])}}return p}

// ---- burning (evil realm) ----
let burnLayer=()=>{};
if(EV>=0){const CH=mkC(),C=CH.getContext('2d');const r=rng(5);C.fillStyle='#160c06';C.fillRect(0,0,1080,1920);
 for(let i=0;i<2600;i++){const x=r()*1080,y=r()*1920,rr=8+r()*60;const g=C.createRadialGradient(x,y,0,x,y,rr);const v=r();g.addColorStop(0,v<.5?'rgba(60,32,14,.55)':v<.85?'rgba(0,0,0,.6)':'rgba(110,40,10,.4)');g.addColorStop(1,'rgba(0,0,0,0)');C.fillStyle=g;C.fillRect(x-rr,y-rr,2*rr,2*rr)}
 for(let i=0;i<1500;i++){C.fillStyle=`rgba(255,${80+r()*90|0},20,${r()*.5})`;C.fillRect(r()*1080,r()*1920,1.6,1.6)}
 const bm=document.createElement('canvas');bm.width=GW;bm.height=GH;const BX=bm.getContext('2d');const bi=BX.createImageData(GW,GH);
 const gl=document.createElement('canvas');gl.width=GW;gl.height=GH;const GX=gl.getContext('2d');const gi=GX.createImageData(GW,GH);
 const nzc=new Float32Array(NC);for(let c=0;c<NC;c++){const x=(c%GW)*G,y=Math.floor(c/GW)*G;nzc[c]=Math.sin(x/23+y/31)*.5+Math.sin(x/11-y/17)*.3+Math.sin(x/5+y/7)*.2}
 const tmp=mkC(),TX=tmp.getContext('2d');const FO=mkC(),FOX=FO.getContext('2d');FOX.drawImage(F,0,0);FOX.globalCompositeOperation='source-in';FOX.fillStyle='#ff8c2a';FOX.fillRect(0,0,1080,1920);
 const sc=document.createElement('canvas');sc.width=GW;sc.height=GH;const SX=sc.getContext('2d');const si=SX.createImageData(GW,GH);const sparks=[];const sr=rng(11);for(let k=0;k<700;k++){let x,y;do{x=200+sr()*860;y=60+sr()*1800}while(x<coastX(y));sparks.push({x,y,ph:sr()*1.6,sp:40+sr()*70,dr:(sr()-.5)*30,sz:1.5+sr()*2.5})}
 burnLayer=t=>{const fl=.8+.2*Math.sin(t*13)*Math.sin(t*7.3);
  for(let c=0;c<NC;c++){const q=c*4;if(!land[c]){bi.data[q+3]=0;gi.data[q+3]=0;continue}const s=sev[c]+nzc[c]*.12;
   bi.data[q]=bi.data[q+1]=bi.data[q+2]=255;bi.data[q+3]=255*Math.max(0,Math.min(1,(s+.02)/.14));si.data[q]=95;si.data[q+1]=52;si.data[q+2]=18;si.data[q+3]=255*.55*Math.max(0,Math.min(1,(s+.22)/.2))*(s<.05?1:0);
   const g=Math.exp(-(((s-.02)/.07)**2))*fl;gi.data[q]=255;gi.data[q+1]=120+90*g;gi.data[q+2]=30;gi.data[q+3]=255*Math.min(1,g*1.3)}
  BX.putImageData(bi,0,0);GX.putImageData(gi,0,0);SX.putImageData(si,0,0);X.drawImage(sc,0,0,1080,1920);
  TX.globalCompositeOperation='source-over';TX.clearRect(0,0,1080,1920);TX.drawImage(CH,0,0);TX.globalCompositeOperation='destination-in';TX.imageSmoothingEnabled=true;TX.drawImage(bm,0,0,1080,1920);
  X.globalAlpha=.9;X.drawImage(tmp,0,0);TX.globalCompositeOperation='source-over';TX.clearRect(0,0,1080,1920);TX.drawImage(FO,0,0);TX.globalCompositeOperation='destination-in';TX.drawImage(bm,0,0,1080,1920);X.globalAlpha=.42;X.drawImage(tmp,0,0);X.globalAlpha=1;
  X.save();X.globalCompositeOperation='lighter';X.filter='blur(6px)';X.drawImage(gl,0,0,1080,1920);X.filter='none';X.globalAlpha=.9;X.drawImage(gl,0,0,1080,1920);X.restore();
  // rising embers near the burning front
  X.save();X.globalCompositeOperation='lighter';sparks.forEach(s=>{const per=1.6;const age=((t+s.ph)%per);const born=t-age;const c=Math.min(GH-1,Math.floor(s.y/G))*GW+Math.min(GW-1,Math.floor(s.x/G));
   if(sev[c]<-.05||sev[c]>.5)return;const a=1-age/per;X.fillStyle=`rgba(255,${150+80*a|0},60,${a*.9})`;X.beginPath();X.arc(s.x+Math.sin(age*3+s.ph)*6+s.dr*age,s.y-age*s.sp,s.sz*a+.5,0,7);X.fill()});X.restore();
  // smoke over burning towns
  CITY.forEach(c=>{if(cityOwner(c,t)!=EV)return;for(let k=0;k<5;k++){const age=((t*.6+k*.2)%1);X.fillStyle=`rgba(30,22,16,${.35*(1-age)})`;X.beginPath();X.arc(c.x+Math.sin(k+t)*6+age*18,c.y-30-age*70,8+age*22,0,7);X.fill()}})}}
function cityLayer(t){CITY.forEach(c=>{const o=cityOwner(c,t);const col=TT.natS[o];
  if(o==EV){X.save();X.globalCompositeOperation='lighter';const fl=.7+.3*Math.sin(t*17+c.x);const g=X.createRadialGradient(c.x,c.y-10,0,c.x,c.y-10,34);g.addColorStop(0,`rgba(255,170,60,${.8*fl})`);g.addColorStop(1,'rgba(255,60,0,0)');X.fillStyle=g;X.fillRect(c.x-40,c.y-50,80,80);X.restore()}
  else{X.strokeStyle=col;X.fillStyle=col;X.lineWidth=2.5;X.beginPath();X.moveTo(c.x+(c.big?22:14),c.y-6);X.lineTo(c.x+(c.big?22:14),c.y-46);X.stroke();X.beginPath();X.moveTo(c.x+(c.big?22:14),c.y-46);X.lineTo(c.x+(c.big?46:38),c.y-40);X.lineTo(c.x+(c.big?22:14),c.y-32);X.closePath();X.fill()}});
 FALLS.forEach(F=>{const u=(t-F.t)/1.4;if(u<0||u>1)return;const col=TT.natS[F.k];X.globalAlpha=1-u;X.strokeStyle=col;X.lineWidth=4;X.beginPath();X.arc(F.c.x,F.c.y-8,20+u*70,0,7);X.stroke();
  spaced(F.c.n+(TT.up?' FALLS':' falls'),F.c.x,F.c.y+62+u*14,TT.L(TH=='fantasy'?28:26),col,0,0,X);X.globalAlpha=1})}
frameEdge();titleBox(500,60,520,150,CFG.title[0],CFG.title[1]);
const tot=land.reduce((s,v)=>s+v,0);
window.DUR=CFG.dur;
window.render=t=>{X.fillStyle=BGC;X.fillRect(0,0,1080,1920);const rv=Math.min(1,eio(pr(t,0,1))*1.4);X.globalAlpha=rv;X.drawImage(M,0,0);
 solve(t);const flash=NAT.map((n,k)=>Math.max(0,...PUSH.filter(P=>P.nat==k).map(P=>{const u=(t-P.t0)/(P.dur+.4);return u>0&&u<1?Math.sin(u*Math.PI)*.55:0})));
 paintFill(t,flash);X.globalAlpha=rv*eo(pr(t,.9,.8));X.imageSmoothingEnabled=true;X.imageSmoothingQuality='high';X.drawImage(low,0,0,1080,1920);X.globalAlpha=rv;
 const bp=borderPath();X.lineJoin='round';X.lineCap='round';
 if(TH=='simple'){X.strokeStyle='#fff';X.lineWidth=7;X.stroke(bp);X.strokeStyle='#33363d';X.lineWidth=2.6;X.stroke(bp)}
 else if(TH=='fantasy'){X.strokeStyle=INK;X.lineWidth=3.2;X.stroke(bp)}else{X.save();X.shadowColor='#cfe8ef';X.shadowBlur=8;X.strokeStyle='#cfe8ef';X.lineWidth=2.4;X.stroke(bp);X.restore()}
 X.drawImage(F,0,0);
 if(EV>=0)burnLayer(t);
 cityLayer(t);X.drawImage(LBc,0,0);
 // advance arrows while a chunk is being taken
 PUSH.forEach(P=>{const u=(t-P.t0+.2)/(P.dur+.5);if(u<=0||u>=1)return;const a=P.from||ARROW_FROM[P.nat];const q=eio(Math.min(1,u*1.5));const x=a[0]+(P.x-a[0])*q,y=a[1]+(P.y-a[1])*q;
  X.globalAlpha=Math.sin(u*Math.PI);const c=TT.natS[P.nat];X.strokeStyle=c;X.fillStyle=c;X.lineWidth=TH=='fantasy'?5:7;X.beginPath();X.moveTo(...a);X.lineTo(x,y);X.stroke();
  const an=Math.atan2(P.y-a[1],P.x-a[0]);X.save();X.translate(x,y);X.rotate(an);X.beginPath();X.moveTo(20,0);X.lineTo(-11,-15);X.lineTo(-11,15);X.closePath();X.fill();X.restore()});X.globalAlpha=1;
 // realm names at the centre of what each holds, and share of land
 const cnt=new Array(NN).fill(0),sx=new Array(NN).fill(0),sy=new Array(NN).fill(0);for(let c=0;c<NC;c++){const o=own[c];if(o<0)continue;cnt[o]++;sx[o]+=(c%GW)*G;sy[o]+=Math.floor(c/GW)*G}
 NAT.forEach(([n],k)=>{if(!cnt[k])return;let lx=sx[k]/cnt[k],ly=sy[k]/cnt[k]-46;for(let it=0;it<6;it++){const hit=CITY.find(c=>Math.abs(c.x-lx)<190&&Math.abs(c.y+20-ly)<55);if(!hit)break;ly=hit.y+20+(ly<hit.y+20?-60:60)}spaced(n,lx,ly,TT.T(TH=='fantasy'?(n.length>12?34:40):38),k==EV?'#ff8a2a':TT.natS[k],0,TH=='fantasy'?6:2,X)});
 let yr=CFG.year0;PH.forEach(p=>{if(t>=p.t)yr=p.year});panel(X,60,1620,470,250);X.fillStyle=INK;X.font=TT.T(44);X.fillText(TT.up?yr.toUpperCase():yr,90,1680);
 NAT.forEach(([n],k)=>{const y=1725+k*40;X.fillStyle=k==EV?'#1a0d06':TT.natS[k];X.fillRect(90,y-22,28,24);if(k==EV){X.fillStyle='#ff7a1a';X.fillRect(94,y-6,20,4)}X.fillStyle=INK;X.font=TT.L(TH=='fantasy'?(n.length>12?20:26):24);X.fillText(TT.up?n.toUpperCase():n,130,y);X.font=TT.I(24);X.fillText(Math.round(cnt[k]/tot*100)+(TT.up?'% LAND':'% of the land'),350,y)});
 compass(950,1780,46)};
'''
CFG_T="const CFG={dur:11,title:['The Four Realms','who holds the land'],year0:'Year 1',nat:[['Aldmere',560,330,1.0],['Karth',640,1680,1.0],['Ostmark',930,560,.86],['Vell',300,1300,.92]],phases:[{t:3.4,year:'Year 3'},{t:6.6,year:'Year 5'}],arrowFrom:{0:[620,470],1:[620,1480],2:[930,660]},pushes:[[1,[[560,1330],[500,1210],[460,1110]],3.5,3.0],[0,[[780,620],[880,560]],3.8,2.8,110],[1,[[360,1240],[300,1110],[320,980]],6.7,3.0,120],[2,[[880,820],[760,780]],6.9,2.6,105],[1,[[900,1180],[920,1060]],7.6,2.8,110]]};"
CFG_B="const CFG={dur:13,evil:3,title:['The Ember War','the shadow spreads from the south'],year0:'Year 1',nat:[['Aldmere',560,330,1.0],['Vell',300,1250,.95],['Ostmark',930,560,.92],['Ashen Dominion',760,1650,.95]],phases:[{t:3.0,year:'Year 4'},{t:6.4,year:'Year 7'},{t:9.6,year:'Year 10'}],arrowFrom:{3:[760,1560],0:[560,500]},pushes:[[3,[[820,1450],[860,1290],[930,1150]],3.1,3.2,120],[3,[[620,1420],[520,1300],[470,1220]],4.1,3.2,120],[3,[[400,1420],[300,1420],[300,1300]],6.5,3.2,115],[3,[[900,1040],[880,880],[760,790]],7.4,3.2,115],[3,[[600,1120],[480,950],[330,1000],[300,800]],9.7,3.3,120],[0,[[520,660],[600,760]],11.2,1.8,100]]};"
if __name__=='__main__':
    NAMES={'campaign':CAMPAIGN,'bridge':BRIDGE,'territory':CFG_T+TERRITORY}
    for th in ['fantasy','simple','modern']:
        for typ,code in NAMES.items():
            page(f'map_{th}_{typ}',{'fantasy':'#7d5a2c','simple':'#a9d4ef','modern':'#070b10'}[th],f"const TH='{th}';"+CORE+CGEO+code,css=FONTS)
    page('map_fantasy_burning','#7d5a2c',"const TH='fantasy';"+CORE+CGEO+CFG_B+TERRITORY,css=FONTS)
