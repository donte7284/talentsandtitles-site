# World War II, Europe & North Africa, month by month, in the three map styles (fantasy, simple, modern).
import json, sys
import os
_B=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _B)
from mk import page
from build_mapset import CORE, FONTS

WW = r'''
const GW=270,GH=311,NC=GW*GH,Y0=250,SC=GEO.sc,LON0=GEO.lon0;
const myc=l=>Math.log(Math.tan(Math.PI/4+l*Math.PI/360))*180/Math.PI;const TOPM=myc(GEO.top);
const PX=(lon,lat)=>[(lon-LON0)*SC,Y0+(TOPM-myc(lat))*SC];
const c01=v=>v<0?0:v>1?1:v;
const CN=Uint8Array.from(atob(GEO.cells),ch=>ch.charCodeAt(0));
const C={};GEO.names.forEach((n,i)=>C[n]=i);
const LAND=new Path2D(GEO.land);
const LON=new Float32Array(NC),LAT=new Float32Array(NC),NX=new Float32Array(NC),NY=new Float32Array(NC),ROW=new Int16Array(NC);
for(let j=0;j<GH;j++)for(let i=0;i<GW;i++){const c=j*GW+i,x=i*4+2,y=Y0+j*4+2,lon=x/SC+LON0,lat=FR.rowlat[j];LON[c]=lon;LAT[c]=lat;ROW[c]=j;
 const nz=.17*(Math.sin(x/37+1.3)+.6*Math.sin(y/23+.7)+.4*Math.sin((x+y)/13));NX[c]=lon+nz;NY[c]=lat+.6*(Math.sin(x/29+.4)+.5*Math.sin(y/17+2.1))*.2;
}
// sea cells borrow the nearest land cell (4 steps) so fills and borders run cleanly under the coastline clip
const NEAR=new Int32Array(NC).fill(-1);{let q=[];for(let c=0;c<NC;c++)if(CN[c]){NEAR[c]=c;q.push(c)}
 for(let s=0;s<4;s++){const nq=[];for(const c of q){const i=c%GW,j=(c/GW)|0;[[1,0],[-1,0],[0,1],[0,-1]].forEach(([a,b])=>{const ii=i+a,jj=j+b;if(ii<0||jj<0||ii>=GW||jj>=GH)return;const d=jj*GW+ii;if(NEAR[d]<0){NEAR[d]=NEAR[c];nq.push(d)}})}q=nq}}
const k1=(K,m)=>{if(m<=K[0][0])return K[0][1];for(let i=1;i<K.length;i++)if(m<=K[i][0]){const f=eio((m-K[i-1][0])/(K[i][0]-K[i-1][0]));return K[i-1][1]+(K[i][1]-K[i-1][1])*f}return K[K.length-1][1]};
const toRows=K=>K.map(([m,r])=>[m,Float32Array.from(r,v=>v==null?NaN:v)]);
function rowsAt(K,m,out){if(m<=K[0][0]){out.set(K[0][1]);return}let i=1;while(i<K.length&&m>K[i][0])i++;if(i>=K.length){out.set(K[K.length-1][1]);return}
 const f=eio((m-K[i-1][0])/(K[i][0]-K[i-1][0])),A=K[i-1][1],B=K[i][1];for(let j=0;j<GH;j++){const a=A[j],b=B[j];out[j]=a!==a?b:b!==b?a:a+(b-a)*f}}
const Gc=0,Ac=1,Lc=2,Sc=3,Vc=4,Nc=5;
const sw=(m,m0,d,v)=>m>=m0+d*c01(v);
const ell=(y,x,la,lo,rl,ro)=>((y-la)/rl)**2+((x-lo)/ro)**2<1;
%THEATRE%
// ---------- time ----------
const STT=ST.st;const mOf=t=>{if(t<=STT[0])return -1;for(let i=1;i<STT.length;i++)if(t<STT[i])return i-2+(t-STT[i-1])/(STT[i]-STT[i-1]);return ST.nm-1.001};
const tOf=m=>{const i=Math.max(0,Math.min(STT.length-2,Math.floor(m)+1));return STT[i]+(m-Math.floor(m))*(STT[i+1]-STT[i])};
const MON=['January','February','March','April','May','June','July','August','September','October','November','December'];
const dateOf=mi=>{const a=mi+ST.epoch;return MON[a%12]+' '+Math.floor(a/12)};
// ---------- theme colours ----------
const PAL={fantasy:{fill:['rgba(60,30,12,.45)','rgba(165,115,20,.36)','rgba(40,85,170,.34)','rgba(150,25,20,.32)','rgba(110,80,140,.34)','rgba(120,100,70,.08)'],str:['#8a1f12','#a5731a','#1f3d70','#8a1f12','#5e3f7a','#6b5a40']},
 simple:{fill:['#4a3326','#f5d887','#a7c8f3','#f3aaa2','#d3c3e6','#e6e4da'],str:['#c0471c','#d39a12','#2f6fdc','#e0453a','#7d5ba6','#9a9a90']},
 modern:{fill:['rgba(255,90,20,.12)','rgba(255,200,80,.24)','rgba(79,179,255,.26)','rgba(255,77,94,.27)','rgba(190,150,255,.22)','rgba(207,232,239,.05)'],str:['#ff7a1a','#ffc850','#4fb3ff','#ff4d5e','#be96ff','#5f7a86']}}[TH];
const parseC=s=>{if(s[0]=='#'){const n=parseInt(s.slice(1),16);return[n>>16,n>>8&255,n&255,1]}const q=s.match(/[\d.]+/g).map(Number);return[q[0],q[1],q[2],q[3]??1]};
const FILLC=PAL.fill.map(parseC);
// ---------- static layers ----------
Q=M.getContext('2d');seaBg();Q.save();Q.beginPath();Q.rect(0,Y0,1080,GH*4);Q.clip();
if(TH=='fantasy'){for(let k=1;k<=6;k++){Q.save();Q.translate(-k*5,k*2.5);Q.strokeStyle=inkA(.2-k*.026);Q.lineWidth=1;Q.setLineDash([18+k*3,5+k*2]);Q.stroke(LAND);Q.restore()}Q.setLineDash([]);Q.fillStyle='rgba(239,224,184,.5)';Q.fill(LAND,'evenodd')}
else if(TH=='simple'){Q.strokeStyle='#c4e3f5';Q.lineWidth=26;Q.lineJoin='round';Q.stroke(LAND);Q.fillStyle='#eef0e2';Q.fill(LAND,'evenodd')}
else{Q.fillStyle='#101b24';Q.fill(LAND,'evenodd');Q.save();Q.clip(LAND,'evenodd');Q.strokeStyle='rgba(90,140,170,.12)';Q.lineWidth=1;for(let x=0;x<=1080;x+=60){Q.beginPath();Q.moveTo(x,0);Q.lineTo(x,1920);Q.stroke()}for(let y=0;y<=1920;y+=60){Q.beginPath();Q.moveTo(0,y);Q.lineTo(1080,y);Q.stroke()}Q.restore()}
Q.restore();const COAST=mkC();{const q=COAST.getContext('2d');q.beginPath();q.rect(0,Y0,1080,GH*4);q.clip();q.lineJoin='round';if(TH=='fantasy'){q.strokeStyle=INK;q.lineWidth=2;q.stroke(LAND)}else if(TH=='simple'){q.strokeStyle='#7fb07a';q.lineWidth=2.6;q.stroke(LAND)}else{q.shadowColor='#78dcd2';q.shadowBlur=10;q.strokeStyle='#78dcd2';q.lineWidth=1.8;q.stroke(LAND)}}
// labels: countries, seas, cities
const LBc=mkC();{const q=LBc.getContext('2d');
 const lab=(t,lo,la,s,col,sp,rot=0)=>{const[x,y]=PX(lo,la);spaced(t,x,y,s,col,rot,sp,q)};
 const cf=TH=='fantasy'?(s=>`${s}px 'Uncial Antiqua'`):TT.L;const cc=TH=='modern'?'rgba(207,232,239,.75)':inkA(.72);
 ST.labels.forEach(([t,lo,la])=>lab(t,lo,la,cf(ST.big.includes(t)?30:21),cc,TH=='fantasy'?3:2));
 const sf=TT.I;const sc=TH=='modern'?'rgba(120,200,220,.6)':TH=='simple'?'rgba(60,110,150,.75)':inkA(.6);
 ST.seas.forEach(([t,lo,la])=>lab(t,lo,la,sf(24),sc,TH=='fantasy'?3:2));
 window.CITIES=ST.cities;
 CITIES.forEach(([n,lo,la])=>{const[x,y]=PX(lo,la);q.fillStyle=TH=='modern'?'#cfe8ef':INK;q.strokeStyle=TT.halo;q.lineWidth=3;q.beginPath();q.arc(x,y,5,0,7);q.stroke();q.fill();
  spaced(n,x,y-12,TT.I(TH=='fantasy'?21:19),TH=='modern'?'#cfe8ef':INK,0,0,q)})}
// ---------- per-frame state ----------
const own=new Int8Array(NC),IND=new Float32Array(NC),TMPB=new Float32Array(NC);
function blur(a,r){for(let pass=0;pass<2;pass++){for(let j=0;j<GH;j++){let s=0;const o=j*GW;for(let i=-r;i<=r;i++)s+=a[o+Math.max(0,Math.min(GW-1,i))];for(let i=0;i<GW;i++){TMPB[o+i]=s/(2*r+1);s+=a[o+Math.min(GW-1,i+r+1)]-a[o+Math.max(0,i-r)]}}
 for(let i=0;i<GW;i++){let s=0;for(let j=-r;j<=r;j++)s+=TMPB[Math.max(0,Math.min(GH-1,j))*GW+i];for(let j=0;j<GH;j++){a[j*GW+i]=s/(2*r+1);s+=TMPB[Math.min(GH-1,j+r+1)*GW+i]-TMPB[Math.max(0,j-r)*GW+i]}}}}
const low=document.createElement('canvas');low.width=GW;low.height=GH;const LX=low.getContext('2d');const img=LX.createImageData(GW,GH);
function contour(a,lv,p){for(let j=0;j<GH-1;j++)for(let i=0;i<GW-1;i++){const c=j*GW+i;const A=a[c]-lv,B=a[c+1]-lv,D=a[c+GW]-lv,E=a[c+GW+1]-lv;const idx=(A>0)|((B>0)<<1)|((E>0)<<2)|((D>0)<<3);if(idx==0||idx==15)continue;const x=i*4+2,y=Y0+j*4+2;
 const T=[A>0!=B>0?[x+4*A/(A-B),y]:null,B>0!=E>0?[x+4,y+4*B/(B-E)]:null,D>0!=E>0?[x+4*D/(D-E),y+4]:null,A>0!=D>0?[x,y+4*A/(A-D)]:null].filter(Boolean);for(let n=0;n+1<T.length;n+=2){p.moveTo(...T[n]);p.lineTo(...T[n+1])}}}
const GI=new Float32Array(NC),IA=new Float32Array(NC);
function solve(m){frameVals(m);const raw=new Int8Array(NC);for(let c=0;c<NC;c++)raw[c]=CN[c]?ctrl(c,m):-1;for(let c=0;c<NC;c++){const n=NEAR[c];own[c]=n<0?-1:raw[n]}}
function paintFill(){for(let c=0;c<NC;c++){const o=own[c],q=c*4;if(o<0){img.data[q+3]=0;continue}const f=FILLC[o];img.data[q]=f[0];img.data[q+1]=f[1];img.data[q+2]=f[2];img.data[q+3]=f[3]*255}LX.putImageData(img,0,0)}
function borders(){const p=new Path2D();for(let k=1;k<6;k++){for(let c=0;c<NC;c++)IND[c]=own[c]==k?1:0;blur(IND,1);contour(IND,.5,p)}return p}
// ---------- fire (Germany and what it holds) ----------
const CH=mkC();{const C2=CH.getContext('2d');const r=rng(5);C2.fillStyle='#160c06';C2.fillRect(0,0,1080,1920);
 for(let i=0;i<2600;i++){const x=r()*1080,y=r()*1920,rr=8+r()*60;const g=C2.createRadialGradient(x,y,0,x,y,rr);const v=r();g.addColorStop(0,v<.5?'rgba(60,32,14,.55)':v<.85?'rgba(0,0,0,.6)':'rgba(110,40,10,.4)');g.addColorStop(1,'rgba(0,0,0,0)');C2.fillStyle=g;C2.fillRect(x-rr,y-rr,2*rr,2*rr)}
 for(let i=0;i<1500;i++){C2.fillStyle=`rgba(255,${80+r()*90|0},20,${r()*.5})`;C2.fillRect(r()*1080,r()*1920,1.6,1.6)}}
const mk2=()=>{const c=document.createElement('canvas');c.width=GW;c.height=GH;return c};
const bm=mk2(),BX=bm.getContext('2d'),bi=BX.createImageData(GW,GH),gl=mk2(),GX=gl.getContext('2d'),gi=GX.createImageData(GW,GH),scm=mk2(),SX=scm.getContext('2d'),si=SX.createImageData(GW,GH);
const nzc=new Float32Array(NC);for(let c=0;c<NC;c++){const x=(c%GW)*4,y=Math.floor(c/GW)*4;nzc[c]=Math.sin(x/23+y/31)*.5+Math.sin(x/11-y/17)*.3+Math.sin(x/5+y/7)*.2}
const MH=GH*4;const mkL=()=>{const c=document.createElement('canvas');c.width=1080;c.height=MH;return c};const LMASK=mkL();{const q=LMASK.getContext('2d');q.translate(0,-Y0);q.fillStyle='#fff';q.fill(LAND,'evenodd')}
const tmp=mkL(),TX=tmp.getContext('2d');const FLY=mkL(),FX=FLY.getContext('2d');const MAPL=mkL(),MX=MAPL.getContext('2d');const gl2=mk2(),G2=gl2.getContext('2d');
const sparks=[];{const sr=rng(11);let n=0;while(sparks.length<650&&n<99999){n++;const c=(sr()*NC)|0;if(!CN[c])continue;sparks.push({c,x:(c%GW)*4+2,y:Y0+Math.floor(c/GW)*4+2,ph:sr()*1.6,sp:30+sr()*60,dr:(sr()-.5)*24,sz:1.4+sr()*2.2})}}
function fire(t){for(let c=0;c<NC;c++)GI[c]=own[c]==0?1:0;blur(GI,2);const fl=.8+.2*Math.sin(t*13)*Math.sin(t*7.3);
 for(let c=0;c<NC;c++){const q=c*4;const s=(GI[c]-.5)*.6+nzc[c]*.05;bi.data[q]=bi.data[q+1]=bi.data[q+2]=255;bi.data[q+3]=255*c01((s+.02)/.14);
  si.data[q]=95;si.data[q+1]=52;si.data[q+2]=18;si.data[q+3]=s<.04?255*.5*c01((s+.2)/.18):0;const g=Math.exp(-(((s-.02)/.07)**2))*fl;gi.data[q]=255;gi.data[q+1]=120+90*g;gi.data[q+2]=30;gi.data[q+3]=255*Math.min(1,g*1.3)}
 BX.putImageData(bi,0,0);GX.putImageData(gi,0,0);SX.putImageData(si,0,0);
 FX.globalCompositeOperation='source-over';FX.clearRect(0,0,1080,MH);FX.drawImage(scm,0,0,1080,MH);TX.globalCompositeOperation='source-over';TX.clearRect(0,0,1080,MH);TX.drawImage(CH,0,-Y0);TX.globalCompositeOperation='destination-in';TX.drawImage(bm,0,0,1080,MH);FX.globalAlpha=.92;FX.drawImage(tmp,0,0);FX.globalAlpha=1;FX.globalCompositeOperation='lighter';G2.clearRect(0,0,GW,GH);G2.filter='blur(1.3px)';G2.drawImage(gl,0,0);G2.filter='none';FX.drawImage(gl2,0,0,1080,MH);FX.globalAlpha=.85;FX.drawImage(gl,0,0,1080,MH);FX.globalAlpha=1;FX.globalCompositeOperation='destination-in';FX.drawImage(LMASK,0,0);FX.globalCompositeOperation='source-over';X.drawImage(FLY,0,Y0);X.save();X.globalCompositeOperation='lighter';sparks.forEach(s=>{const per=1.6,age=(t+s.ph)%per;if(GI[s.c]<.3||GI[s.c]>.95)return;const a=1-age/per;X.fillStyle=`rgba(255,${150+80*a|0},60,${a*.9})`;X.beginPath();X.arc(s.x+Math.sin(age*3+s.ph)*5+s.dr*age,s.y-age*s.sp,s.sz*a+.4,0,7);X.fill()});
 X.restore();
 CITIES.forEach(([n,lo,la])=>{const[x,y]=PX(lo,la);const c=Math.min(GH-1,Math.max(0,Math.floor((y-Y0)/4)))*GW+Math.min(GW-1,Math.floor(x/4));if(own[c]!=0)return;
  X.save();X.globalCompositeOperation='lighter';const f2=.7+.3*Math.sin(t*17+x);const g=X.createRadialGradient(x,y-6,0,x,y-6,26);g.addColorStop(0,`rgba(255,170,60,${.75*f2})`);g.addColorStop(1,'rgba(255,60,0,0)');X.fillStyle=g;X.fillRect(x-30,y-36,60,60);X.restore();
  for(let k=0;k<4;k++){const age=(t*.6+k*.25)%1;X.fillStyle=`rgba(30,22,16,${.3*(1-age)})`;X.beginPath();X.arc(x+Math.sin(k+t)*5+age*14,y-20-age*55,6+age*18,0,7);X.fill()}})}
// ---------- flags ----------
function drawFlag(q,f,w,h){const st=(cols,vert)=>cols.forEach((c,i)=>{q.fillStyle=c;vert?q.fillRect(i*w/cols.length,0,w/cols.length+.5,h):q.fillRect(0,i*h/cols.length,w,h/cols.length+.5)});
 if(f=='de')st(['#111','#fff','#d21f1f']);else if(f=='fr')st(['#1f3c99','#fff','#e0293a'],1);else if(f=='pl')st(['#fff','#dc143c']);else if(f=='ro')st(['#1d3c9b','#fcd116','#ce1126'],1);else if(f=='hu')st(['#cd2a3e','#fff','#43704b']);else if(f=='yu')st(['#1d3c9b','#fff','#d0262c']);
 else if(f=='yp'){st(['#1d3c9b','#fff','#d0262c']);star(q,w/2,h/2,h*.32,'#d0262c','#fff')}
 else if(f=='it'){st(['#079246','#fff','#d1232a'],1);q.fillStyle='#1f3c99';q.fillRect(w/2-h*.2,h*.25,h*.4,h*.5);q.fillStyle='#d1232a';q.fillRect(w/2-h*.16,h*.29,h*.32,h*.42);q.fillStyle='#fff';q.fillRect(w/2-h*.04,h*.29,h*.08,h*.42);q.fillRect(w/2-h*.16,h*.46,h*.32,h*.08)}
 else if(f=='fi'){q.fillStyle='#fff';q.fillRect(0,0,w,h);q.fillStyle='#16357a';q.fillRect(w*.28,0,h*.24,h);q.fillRect(0,h*.38,w,h*.24)}
 else if(f=='gr'){for(let i=0;i<9;i++){q.fillStyle=i%2?'#fff':'#0d5eaf';q.fillRect(0,i*h/9,w,h/9+.5)}q.fillStyle='#0d5eaf';q.fillRect(0,0,h*5/9,h*5/9);q.fillStyle='#fff';q.fillRect(h*2/9,0,h/9,h*5/9);q.fillRect(0,h*2/9,h*5/9,h/9)}
 else if(f=='us'){for(let i=0;i<13;i++){q.fillStyle=i%2?'#fff':'#b22234';q.fillRect(0,i*h/13,w,h/13+.5)}q.fillStyle='#3c3b6e';q.fillRect(0,0,w*.42,h*7/13);q.fillStyle='#fff';for(let a=0;a<6;a++)for(let b=0;b<8;b++){q.beginPath();q.arc(w*.42*(b+.5)/8,h*7/13*(a+.5)/6,.9*w/100+.6,0,7);q.fill()}}
 else if(f=='su'){q.fillStyle='#cc0000';q.fillRect(0,0,w,h);const s=h/30;q.save();q.translate(h*.36,h*.42);q.strokeStyle='#ffd700';q.fillStyle='#ffd700';q.lineWidth=2.2*s;q.beginPath();q.arc(0,0,5.2*s,Math.PI*.15,Math.PI*1.25);q.stroke();q.beginPath();q.moveTo(-4*s,4*s);q.lineTo(4*s,-4*s);q.stroke();q.fillRect(1.6*s,-6.4*s,4.4*s,2.4*s);q.restore();star(q,h*.36,h*.12,h*.08,'#ffd700',null)}
 else if(f=='jp'){q.fillStyle='#fff';q.fillRect(0,0,w,h);q.fillStyle='#bc002d';q.beginPath();q.arc(w/2,h/2,h*.3,0,7);q.fill()}
 else if(f=='nl')st(['#ae1c28','#fff','#21468b']);else if(f=='th')st(['#a51931','#f4f5f8','#2d2a4a','#2d2a4a','#f4f5f8','#a51931']);
 else if(f=='cn'){q.fillStyle='#fe0000';q.fillRect(0,0,w,h);q.fillStyle='#000095';q.fillRect(0,0,w/2,h/2);sun(q,w/4,h/4,h*.17)}
 else if(f=='au'){q.fillStyle='#012169';q.fillRect(0,0,w,h);q.save();q.scale(.5,.5);drawFlag(q,'gb',w,h);q.restore();star(q,w/4,h*.76,h*.13,'#fff',null);[[.75,.78],[.62,.42],[.75,.18],[.87,.36]].forEach(([a,b])=>star(q,w*a,h*b,h*.07,'#fff',null))}
 else if(f=='gb'){q.fillStyle='#012169';q.fillRect(0,0,w,h);q.save();q.beginPath();q.rect(0,0,w,h);q.clip();q.strokeStyle='#fff';q.lineWidth=h*.2;q.beginPath();q.moveTo(0,0);q.lineTo(w,h);q.moveTo(w,0);q.lineTo(0,h);q.stroke();q.strokeStyle='#c8102e';q.lineWidth=h*.07;q.beginPath();q.moveTo(0,0);q.lineTo(w,h);q.moveTo(w,0);q.lineTo(0,h);q.stroke();q.restore();
  q.fillStyle='#fff';q.fillRect(w/2-h*.17,0,h*.34,h);q.fillRect(0,h/2-h*.17,w,h*.34);q.fillStyle='#c8102e';q.fillRect(w/2-h*.1,0,h*.2,h);q.fillRect(0,h/2-h*.1,w,h*.2)}}
function sun(q,x,y,r){q.fillStyle='#fff';q.beginPath();for(let i=0;i<24;i++){const a=i*Math.PI/12,rr=i%2?r*.6:r*1.25;q.lineTo(x+Math.cos(a)*rr,y+Math.sin(a)*rr)}q.fill();q.fillStyle='#000095';q.beginPath();q.arc(x,y,r*.55,0,7);q.fill();q.fillStyle='#fff';q.beginPath();q.arc(x,y,r*.45,0,7);q.fill()}
function star(q,x,y,r,f,s){q.beginPath();for(let i=0;i<10;i++){const a=-Math.PI/2+i*Math.PI/5,rr=i%2?r*.42:r;q.lineTo(x+Math.cos(a)*rr,y+Math.sin(a)*rr)}q.closePath();if(s){q.strokeStyle=s;q.lineWidth=1.5;q.stroke()}q.fillStyle=f;q.fill()}
const FW=50,FH=33;const FLAGI={};['de','gb','us','su','fr','pl','it','gr','ro','hu','fi','yu','yp','jp','cn','au','nl','th'].forEach(f=>{const c=document.createElement('canvas');c.width=FW*2;c.height=FH*2;const q=c.getContext('2d');q.scale(2,2);drawFlag(q,f,FW,FH);FLAGI[f]=c});
const ARM=ST.flags.map((a,i)=>({...a,i,t0:tOf(a.k[0][0]),t1:tOf(a.k[a.k.length-1][0])}));
function armyPos(a,m){const K=a.k;if(m<=K[0][0])return[K[0][1],K[0][2]];for(let i=1;i<K.length;i++)if(m<=K[i][0]){const f=eio((m-K[i-1][0])/(K[i][0]-K[i-1][0]));return[K[i-1][1]+(K[i][1]-K[i-1][1])*f,K[i-1][2]+(K[i][2]-K[i-1][2])*f]}const n=K.length-1;return[K[n][1],K[n][2]]}
function flagAt(x,y,f,t,ph,al,sc=1){X.save();X.globalAlpha=al;X.translate(x,y);X.scale(sc,sc);
 X.fillStyle='rgba(0,0,0,.28)';X.beginPath();X.ellipse(0,1,9,3.5,0,0,7);X.fill();
 X.strokeStyle=TH=='modern'?'#cfe8ef':TH=='simple'?'#33363d':'#3a2a16';X.lineWidth=3;X.beginPath();X.moveTo(0,0);X.lineTo(0,-60);X.stroke();X.fillStyle=X.strokeStyle;X.beginPath();X.arc(0,-61,3,0,7);X.fill();
 const im=FLAGI[f];const N=10;for(let s=0;s<N;s++){const u=s/N;const dy=Math.sin(t*5.5+ph-u*4)*3*u;X.drawImage(im,s*im.width/N,0,im.width/N,im.height,u*FW,-58+dy,FW/N+.6,FH)}
 X.strokeStyle='rgba(0,0,0,.35)';X.lineWidth=1;X.strokeRect(.5,-58,FW,FH);X.restore()}
function armies(t,m){ARM.forEach(a=>{if(t<a.t0-.01)return;let al=c01((t-a.t0)/.35),sc=1;if(t>a.t1){const dt=t-a.t1;if(a.end=='die'){if(dt>.7)return;al*=1-dt/.7;sc=1-dt/.7*.6;if(dt<.5)burst(...PX(...armyPos(a,m)).map((v,i)=>v+(i?-30:0)),.4+dt*.6,t,TT.mark)}else{if(dt>.4)return;al*=1-dt/.4}}
 const[x,y]=PX(...armyPos(a,Math.min(m,a.k[a.k.length-1][0])));flagAt(x,y,a.f,t,a.i*1.7,al,sc)})}
// ---------- battles ----------
const CLS=ST.clash.map(([a,b,lo,la,n])=>{const ta=tOf(a);return{ta,tb:Math.max(tOf(b),ta+1.5),lo,la,n}});
function battles(t){CLS.forEach(B=>{if(t<B.ta||t>B.tb+.4)return;const u=c01((t-B.ta)/.3)*(1-c01((t-B.tb)/.4));const[x,y]=PX(B.lo,B.la);X.save();X.globalAlpha=u;
  const lk=ST.ring.includes(B.n),fl=ST.flash.includes(B.n);if(fl){const g=X.createRadialGradient(x,y,0,x,y,70);g.addColorStop(0,'rgba(255,255,240,.95)');g.addColorStop(.4,'rgba(255,220,150,.6)');g.addColorStop(1,'rgba(255,150,60,0)');X.fillStyle=g;X.beginPath();X.arc(x,y,70,0,7);X.fill()}else if(!lk)burst(x,y,.34+.05*Math.sin(t*9),t,TT.mark);else{X.strokeStyle=PAL.str[2];X.lineWidth=4;X.beginPath();X.arc(x,y,26+4*Math.sin(t*5),0,7);X.stroke()}
  X.restore();X.globalAlpha=u;spaced(B.n,x,lk?y+70:y+46,TT.L(TH=='fantasy'?25:23),TH=='modern'?'#ffc850':TH=='simple'?'#c0392b':'#7a1a0e',0,TH=='fantasy'?2:1,X);X.globalAlpha=1})}
// ---------- HUD ----------
const HUD=mkC();{Q=HUD.getContext('2d');panel(Q,40,36,1000,200);panel(Q,40,1508,1000,92);panel(Q,40,1614,1000,266);
 Q.fillStyle=INK;Q.textAlign='center';Q.font=TH=='fantasy'?TT.I(30):TT.L(24);Q.fillText(TH=='fantasy'?ST.title[0]:(TT.up?ST.title[1].toUpperCase():ST.title[1]),540,84);Q.textAlign='left';
 const LG=ST.legend;
 LG.forEach(([n,k],i)=>{const y=1668+i*(LG.length>5?36:42);if(k==0){Q.fillStyle='#1a0d06';Q.fillRect(78,y-20,36,24);const g=Q.createLinearGradient(78,0,114,0);g.addColorStop(0,'#ff7a1a');g.addColorStop(1,'#ffcf60');Q.fillStyle=g;Q.fillRect(78,y-5,36,4)}
  else{Q.fillStyle=PAL.fill[k];Q.fillRect(78,y-20,36,24);Q.strokeStyle=PAL.str[k];Q.lineWidth=2;Q.strokeRect(78,y-20,36,24)}Q.fillStyle=INK;Q.font=TT.L(TH=='fantasy'?21:20);Q.fillText(TT.up?n.toUpperCase():n,128,y)});
 const FK=ST.flagkey;
 FK.forEach(([f,n],i)=>{const x=480+(i%2)*270,y=1660+Math.floor(i/2)*(FK.length>8?36:42);Q.drawImage(FLAGI[f],x,y-20,36,24);Q.strokeStyle='rgba(0,0,0,.35)';Q.lineWidth=1;Q.strokeRect(x,y-20,36,24);Q.fillStyle=INK;Q.font=TT.L(TH=='fantasy'?21:20);Q.fillText(TT.up?n.toUpperCase():n,x+48,y)});
 Q.font=TT.I(17);Q.fillStyle=inkA(.75);if(ST.foot)Q.fillText(TT.up?ST.foot.toUpperCase():ST.foot,480,1868)}
const capOf=mi=>{let c=null,k=-9;for(const key in ST.cap){const v=+key;if(v<=mi&&v>k){k=v;c=ST.cap[key]}}return[c,k]};
function hud(t,m){X.drawImage(HUD,0,0);const mi=Math.max(-1,Math.min(ST.nm-2,Math.floor(m)));const ds=dateOf(mi);const pop=c01((t-tOf(mi))/.18);
 X.save();X.textAlign='center';X.fillStyle=INK;X.font=TT.T(TH=='fantasy'?70:72);X.globalAlpha=.4+.6*pop;X.fillText(TT.up?ds.toUpperCase():ds,540,168+(1-pop)*8);X.restore();
 // timeline bar
 const x0=110,x1=970,ty=206;X.strokeStyle=inkA(.35);X.lineWidth=3;X.beginPath();X.moveTo(x0,ty);X.lineTo(x1,ty);X.stroke();X.font=TT.I(16);X.textAlign='center';
 for(let y=Math.ceil((ST.epoch-1)/12);y<=Math.floor((ST.epoch+ST.nm-2)/12);y++){const mm=y*12-ST.epoch;const xx=x0+(mm+1)/ST.nm*(x1-x0);X.fillStyle=inkA(.6);X.fillRect(xx-1,ty-7,2,14);X.fillText(String(y),xx,ty+26)}
 const px=x0+c01((m+1)/ST.nm)*(x1-x0);X.strokeStyle=PAL.str[0];X.lineWidth=5;X.beginPath();X.moveTo(x0,ty);X.lineTo(px,ty);X.stroke();X.fillStyle=PAL.str[0];X.beginPath();X.arc(px,ty,8,0,7);X.fill();X.textAlign='left';
 const[cap,ck]=capOf(mi);if(cap){const a=c01((t-tOf(ck))/.3);let fs=TH=='fantasy'?30:31;X.font=TT.I(fs);while(X.measureText(cap).width>950&&fs>18){fs--;X.font=TT.I(fs)}X.globalAlpha=a;X.fillStyle=INK;X.textAlign='center';X.fillText(TT.up?cap.toUpperCase():cap,540,1566);X.textAlign='left';X.globalAlpha=1}}
window.DUR=ST.dur;window.CAPTURE=cv;window._F={solve,paintFill,borders,fire,armies,hud,battles};
window.render=t=>{const m=mOf(t);X.fillStyle=BGC;X.fillRect(0,0,1080,1920);const rv=c01(t/.8);X.globalAlpha=rv;X.drawImage(M,0,0);
 solve(m);paintFill();MX.globalCompositeOperation='source-over';MX.clearRect(0,0,1080,MH);MX.imageSmoothingEnabled=true;MX.imageSmoothingQuality='high';MX.drawImage(low,0,0,1080,MH);MX.save();MX.translate(0,-Y0);const X0=X;{const X=MX;
 const bp=borders();X.lineJoin='round';X.lineCap='round';if(TH=='simple'){X.strokeStyle='#fff';X.lineWidth=5;X.stroke(bp);X.strokeStyle='#33363d';X.lineWidth=1.8;X.stroke(bp)}else if(TH=='fantasy'){X.strokeStyle=inkA(.85);X.lineWidth=2.4;X.stroke(bp)}else{X.shadowColor='#cfe8ef';X.shadowBlur=6;X.strokeStyle='rgba(207,232,239,.85)';X.lineWidth=1.8;X.stroke(bp)}}MX.restore();MX.shadowBlur=0;MX.globalCompositeOperation='destination-in';MX.drawImage(LMASK,0,0);X.drawImage(MAPL,0,Y0);
 X.drawImage(COAST,0,0);fire(t);X.drawImage(LBc,0,0);battles(t);armies(t,m);hud(t,m);if(TH=='fantasy'){Q=X;frameEdge()}X.globalAlpha=1};
'''
BG = {'fantasy': '#7d5a2c', 'simple': '#a9d4ef', 'modern': '#070b10'}
def build(name, d):
    geo = open(f'{_B}/{d}/geo.json').read(); fronts = open(f'{_B}/{d}/fronts.json').read(); story = open(f'{_B}/{d}/story.json').read()
    th_js = open(f'{_B}/{d}/theatre.js').read()
    for th in ['fantasy', 'simple', 'modern']:
        js = f"const TH='{th}';const GEO={geo};const FR={fronts};const ST={story};" + CORE + WW.replace('%THEATRE%', th_js)
        page(f'{name}_{th}', BG[th], js, css=FONTS)
if __name__ == '__main__':
    build('map_ww2', 'ww2')
    build('map_pac', 'pac')
    print('ok')
