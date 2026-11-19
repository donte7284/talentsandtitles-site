import os
_B=os.path.dirname(os.path.abspath(__file__))
# World War II, Europe & North Africa, month by month, in the three map styles (fantasy, simple, modern).
import json, sys
sys.path.insert(0, _B)
from mk import page
from build_mapset import CORE, FONTS
geo = open(_B+'/ww2/geo.json').read()
fronts = open(_B+'/ww2/fronts.json').read()
story = open(_B+'/ww2/story.json').read()

WW = r'''
const GW=270,GH=311,NC=GW*GH,Y0=250,SC=18;
const myc=l=>Math.log(Math.tan(Math.PI/4+l*Math.PI/360))*180/Math.PI;const TOPM=myc(68);
const PX=(lon,lat)=>[(lon+12)*SC,Y0+(TOPM-myc(lat))*SC];
const c01=v=>v<0?0:v>1?1:v;
const CN=Uint8Array.from(atob(GEO.cells),ch=>ch.charCodeAt(0));
const C={};GEO.names.forEach((n,i)=>C[n]=i);
const LAND=new Path2D(GEO.land);
const LON=new Float32Array(NC),LAT=new Float32Array(NC),NX=new Float32Array(NC),NY=new Float32Array(NC),ROW=new Int16Array(NC),SIT=new Float32Array(NC);
const EZ=new Uint8Array(NC),WZ=new Uint8Array(NC),AOCC=new Uint8Array(NC);
const SOVH=new Set(['Russia','Ukraine','Belarus','Moldova','Lithuania','Latvia','Estonia'].map(n=>C[n]));
const YU=new Set(['Serbia','Croatia','Bosnia and Herz.','Slovenia','Montenegro','Kosovo','Macedonia'].map(n=>C[n]));
const EZC=new Set([...SOVH,...['Poland','Hungary','Slovakia','Czechia','Austria','Germany','Serbia','Croatia','Bosnia and Herz.','Slovenia','Montenegro','Kosovo'].map(n=>C[n])]);
const WZC=new Set(['France','Belgium','Netherlands','Luxembourg','Germany','Austria','Czechia'].map(n=>C[n]));
const NEU=new Set(['Spain','Portugal','Andorra','Switzerland','Liechtenstein','Sweden','Turkey','Saudi Arabia','Ireland','W. Sahara'].map(n=>C[n]));
const SOVX=new Set(['Kazakhstan','Georgia','Armenia','Azerbaijan','Turkmenistan'].map(n=>C[n]));
for(let j=0;j<GH;j++)for(let i=0;i<GW;i++){const c=j*GW+i,x=i*4+2,y=Y0+j*4+2,lon=x/SC-12,lat=FR.rowlat[j];LON[c]=lon;LAT[c]=lat;ROW[c]=j;
 const nz=.17*(Math.sin(x/37+1.3)+.6*Math.sin(y/23+.7)+.4*Math.sin((x+y)/13));NX[c]=lon+nz;NY[c]=lat+.6*(Math.sin(x/29+.4)+.5*Math.sin(y/17+2.1))*.2;
 let s=((lat-38.1)*7.36+(lon-15.65)*(-6.46))/95.9;if(lat>43)s-=.06*c01((12-lon)/1.6);SIT[c]=s+nz*.02;
 const k=CN[c];const rx=(k==C.Romania&&((lat>46.35&&lon<25)||(lat>45.95&&lon>=24.4&&lon<26.3)));EZ[c]=(EZC.has(k)||rx)?1:0;WZ[c]=WZC.has(k)?1:0;
 AOCC[c]=(k==C.Moldova||(k==C.Ukraine&&((lat<48.4&&lat>47.7&&lon>24.9&&lon<27.4)||(lat<46.65&&lon>28.2&&lon<30.6)||(lat<48.6&&lat>46.3&&lon>28.2&&lon<31.3))))?1:0}
// sea cells borrow the nearest land cell (4 steps) so fills and borders run cleanly under the coastline clip
const NEAR=new Int32Array(NC).fill(-1);{let q=[];for(let c=0;c<NC;c++)if(CN[c]){NEAR[c]=c;q.push(c)}
 for(let s=0;s<4;s++){const nq=[];for(const c of q){const i=c%GW,j=(c/GW)|0;[[1,0],[-1,0],[0,1],[0,-1]].forEach(([a,b])=>{const ii=i+a,jj=j+b;if(ii<0||jj<0||ii>=GW||jj>=GH)return;const d=jj*GW+ii;if(NEAR[d]<0){NEAR[d]=NEAR[c];nq.push(d)}})}q=nq}}
const k1=(K,m)=>{if(m<=K[0][0])return K[0][1];for(let i=1;i<K.length;i++)if(m<=K[i][0]){const f=eio((m-K[i-1][0])/(K[i][0]-K[i-1][0]));return K[i-1][1]+(K[i][1]-K[i-1][1])*f}return K[K.length-1][1]};
const toRows=K=>K.map(([m,r])=>[m,Float32Array.from(r,v=>v==null?NaN:v)]);const EK=toRows(FR.E),WK=toRows(FR.W);
function rowsAt(K,m,out){if(m<=K[0][0]){out.set(K[0][1]);return}let i=1;while(i<K.length&&m>K[i][0])i++;if(i>=K.length){out.set(K[K.length-1][1]);return}
 const f=eio((m-K[i-1][0])/(K[i][0]-K[i-1][0])),A=K[i-1][1],B=K[i][1];for(let j=0;j<GH;j++){const a=A[j],b=B[j];out[j]=a!==a?b:b!==b?a:a+(b-a)*f}}
const ER=new Float32Array(GH),WR=new Float32Array(GH);
const Gc=0,Ac=1,Lc=2,Sc=3,Vc=4,Nc=5;
const sw=(m,m0,d,v)=>m>=m0+d*c01(v);
const ell=(y,x,la,lo,rl,ro)=>((y-la)/rl)**2+((x-lo)/ro)**2<1;
const ro_=m=>m<14.73?Nc:m<59.73?Ac:Sc, hun=m=>m<14.63?Nc:m<54.6?Ac:Gc;
const DEMK=[[-0.3,46.6],[0.5,46.4],[2.0,47.2],[3.3,46.6],[4.8,46.8],[5.5,47.0],[6.1,46.25]];
const DEM=x=>{if(x<=DEMK[0][0])return DEMK[0][1];for(let i=1;i<DEMK.length;i++)if(x<=DEMK[i][0])return DEMK[i-1][1]+(DEMK[i][1]-DEMK[i-1][1])*(x-DEMK[i-1][0])/(DEMK[i][0]-DEMK[i-1][0]);return DEMK[DEMK.length-1][1]};
let PFv,SFv,FLv,NAv,TWv,TMv,ITv,DRv,ECv,CAv=new Float32Array(10);
function frameVals(m){PFv=k1(FR.PF,m);SFv=k1(FR.SF,m);FLv=k1(FR.FL,m);NAv=k1(FR.NA,m);TWv=k1(FR.TW,m);TMv=k1(FR.TM,m);ITv=k1(FR.IT,m);DRv=k1(FR.DR,m);ECv=k1(FR.EC,m);
 for(let n=0;n<10;n++)CAv[n]=k1(FR.C.map(([mm,a])=>[mm,a[n]]),m);if(m>=21.7)rowsAt(EK,m,ER);if(m>=57.1)rowsAt(WK,m,WR)}
const cAt=x=>{const N=FR.Cn;if(x<=N[0])return CAv[0];for(let n=1;n<N.length;n++)if(x<=N[n])return CAv[n-1]+(CAv[n]-CAv[n-1])*(x-N[n-1]);return CAv[9]};
function yug(k,x,y,m){if(m<19.17)return Nc;if(!sw(m,19.17,.4,(46.6-y)/4.8))return Lc;
 if(k==C.Slovenia)return y>46.1?Gc:(m<48.23?Ac:Gc);if(k==C.Croatia||k==C['Bosnia and Herz.'])return Ac;
 if(k==C.Serbia)return(y>45.25&&x<20.25)?hun(m):Gc;if(k==C.Montenegro)return m<48.23?Ac:m<63.4?Gc:Lc;if(k==C.Kosovo)return m<48.23?Ac:Gc;
 if(k==C.Macedonia)return m<60.27?Ac:m<62.4?Gc:Lc;return Gc}
function base(k,x,y,xn,yn,m,c){
 switch(k){
 case C.Germany:case C.Austria:case C.Czechia:return Gc;
 case C.Slovakia:return Ac;
 case C.Poland:{if(xn<15.8||(y>53.15&&xn<17.0)||(y<51.35&&xn<17.9)||(y>53.35&&xn>19.35&&xn<22.75)||(y>54.15&&x>18.3&&x<19.4))return Gc;
  if(m<0)return Lc;const dem=y<50.4?22.6:23.75;if(m<0.9&&ell(y,x,52.23,21.0,.12,.2))return Lc;
  if(xn<Math.min(PFv,dem))return Gc;if(m>=0.55&&xn>Math.max(SFv,dem))return Sc;return m<1.15?Lc:(xn<dem?Gc:Sc)}
 case C.Belarus:return xn<27?((m<0.55||xn<SFv)?Lc:Sc):Sc;
 case C.Ukraine:{if(y>47.9&&y<48.95&&x<24.65)return hun(m);if((y<48.4&&y>47.7&&x>24.9&&x<27.4)||(y<46.65&&x>28.2&&x<30.6))return m<9.9?ro_(m):Sc;
  if(y>48.4&&xn<26.2)return(m<0.55||xn<SFv)?Lc:Sc;return Sc}
 case C.Lithuania:if(y>55.25&&x<21.95)return Gc;if(x>24.5&&y<55.4)return m<0.55?Lc:m<1.3?Sc:m<9.5?Nc:Sc;return m<9.5?Nc:Sc;
 case C.Latvia:case C.Estonia:return m<9.5?Nc:Sc;
 case C.Moldova:return m<9.9?ro_(m):Sc;
 case C.Russia:{if(x<23&&x>19&&y>54&&y<55.5)return Gc;
  if(y>60.15&&y<62.3&&x<33&&x<30+(y-60.15)*1.6){if(m<6.43)return Nc;if(m<22.9+.6*c01((62.2-y)/2))return Sc;if(m<57.6+.5*c01((y-60.15)/2))return Ac;return Sc}
  if(y>60.15&&y<64.5&&x<35.5){if(m<23+1.5*c01((x-30)/5))return Sc;if(m<57.6+.8*c01((y-60.15)/4))return Ac;return Sc}return Sc}
 case C.Finland:case C['Åland']:if(m<21.73)return Nc;if(m<60.6)return Ac;if(y>65.6&&m<61+2.2*c01((y-65.6)/2.4))return Gc;return Nc;
 case C.Romania:{const ntr=(y>46.35&&x<25)||(y>45.95&&x>=24.4&&x<26.3);if(ntr&&m>=11.97)return hun(m);return ro_(m)}
 case C.Hungary:return hun(m);
 case C.Bulgaria:return m<18?Nc:m<60.27?Ac:Sc;
 case C.Albania:if(m>=62.5+.4*c01((y-39.6)/3.1))return Lc;if(m>=48.23)return Gc;if(y<40.55&&m<19.45&&sw(m,14.5,.8,(y-39.6)/.95))return Lc;return Ac;
 case C.Greece:{if(y<35.75){if(m<13.9)return Nc;if(m<20.63+.37*c01((x-23.5)/2.8))return Lc;return m<68.27?Gc:Lc}
  if(x>26.5&&y<37.1)return m<48.23?Ac:m<68.27?Gc:Lc;if(m<13.9)return Nc;
  if(m<19.2||!sw(m,19.2,.75,(41.75-y)/4))return Lc;if(sw(m,61,.9,(y-36.4)/5.3))return Lc;return Gc}
 case C.Italy:case C.Vatican:case C['San Marino']:{if(x<10&&y<41.35&&y>38.8)return m<48.55?Ac:Lc;
  if(y<38.35&&y>36.5&&x<15.7&&x>12.3)return m<46.3+1.23*c01(.65*(x-12.4)/3.3+.35*(y-36.6)/1.7)?Ac:Lc;
  if(m>=67.95)return Lc;if(SIT[c]<ITv)return Lc;if(m<48.23)return Ac;
  if(m>=52.73&&m<56.8&&ell(y,x,41.47,12.65,.15,.25))return Lc;if(m>=48.27&&m<48.8&&ell(y,x,40.55,14.95,.2,.3))return Lc;return Gc}
 case C.France:case C.Monaco:{if(x>8.5&&y<43.1)return m<9.7?Lc:m<38.33?Vc:m<48.23?Ac:m<49.1?Gc:Lc;if(m<8.3)return Lc;let r;
  if(m<9.7){r=yn>FLv?Gc:Lc;if(m<9.1&&ell(y,x,51.0,2.4,.12,.35))r=Lc}
  else{const occ=x<(y<45.5?-0.3:0.3)||yn>DEM(xn)||(y>48.6&&x>6.0)||(y>47.4&&x>6.85);
   if(occ)r=Gc;else if(m<38.33)r=Vc;else if(m<48.23&&x>4.85&&y<46.4)r=Ac;else r=sw(m,38.33,.2,(46.6-y)/4.3)?Gc:Vc}
  if(m>=59.47&&x>4.4&&x<7.8&&yn<DRv)r=Lc;if(m>=68.27)r=Lc;return r}
 case C.Jersey:case C.Guernsey:return(m<9.97||m>=68.27)?Lc:Gc;
 case C.Belgium:if(m<8.3)return Nc;return sw(m,8.3,.6,(6.4-x)/3.9)?(m>=68.27?Lc:Gc):Lc;
 case C.Netherlands:if(m<8.3)return Nc;return sw(m,8.3,.17,(7.2-x)/3.8)?(m>=68.27?Lc:Gc):Lc;
 case C.Luxembourg:return m<8.3?Nc:m>=68.27?Lc:Gc;
 case C.Denmark:return m<7.27?Nc:m>=68.27?Lc:Gc;
 case C.Norway:if(m<7.27)return Nc;if(m>=68.27)return Lc;return sw(m,7.27,2,(y-58)/9.5)?Gc:Lc;
 case C['United Kingdom']:case C['Isle of Man']:return Lc;
 case C.Iceland:case C['Faeroe Is.']:return m<7.3?Nc:Lc;
 case C.Morocco:if(y>34.85&&x>-6.3&&x<-2.3)return Nc;return m<9.7?Lc:sw(m,38.23,.15,(x+9)/8)?Lc:Vc;
 case C.Algeria:return m<9.7?Lc:sw(m,38.23,.25,(x+2)/10)?Lc:Vc;
 case C.Mauritania:case C.Mali:case C.Niger:return m<9.7?Lc:m<38.3?Vc:Lc;
 case C.Tunisia:if(m<9.7||m>=44.4)return Lc;if(!sw(m,38.33,.3,(37.3-y)/4))return Vc;return(xn<TWv||yn<TMv)?Lc:Gc;
 case C.Libya:if(m>=41.33)return Lc;if(m>=40.1&&y<28&&x<17)return Lc;if(m>=19.3&&m<27.3&&ell(y,x,32.05,23.95,.25,.4))return Lc;return xn<NAv?Ac:Lc;
 case C.Egypt:return(m<41.33&&xn<NAv)?Ac:Lc;
 case C.Syria:case C.Lebanon:return m<9.7?Lc:sw(m,21.23,1.2,(y-33)/4.3)?Lc:Vc;
 case C.Iraq:return(m>=19&&m<20)?Ac:Lc;
 case C.Iran:return m<23.8?Nc:(y>35.6?Sc:Lc);}
 if(SOVX.has(k))return Sc;if(NEU.has(k))return Nc;if(YU.has(k))return yug(k,x,y,m);return Lc}
function crimea(x,y,m){if(m<25.83+.8*c01((46.15-y)/1.9))return Sc;if(m<34.1&&ell(y,x,44.6,33.55,.15,.3))return Sc;if(x>35.35&&m>=28&&m<32.4)return Sc;
 if(m<55.23+1.1*c01(.6*(46.15-y)/1.9+.4*(36.6-x)/4.2))return Gc;return Sc}
const POCK=FR.POCK;
function ctrl(c,m){const k=CN[c];if(!k)return -1;const x=LON[c],y=LAT[c],xn=NX[c],yn=NY[c],j=ROW[c];
 const b=base(k,x,y,xn,yn,m,c);let r=b;
 if(m>=21.7){const cri=y<46.15&&y>44.3&&x>32.4&&x<36.7&&(k==C.Ukraine||k==C.Russia);const cau=k==C.Russia&&y<46.2&&x>36.5;
  if(cri)r=crimea(x,y,m);else if(cau)r=(xn<ECv&&yn>cAt(xn))?Gc:Sc;
  else if(EZ[c]&&!(k==C.Russia&&y>60.15)){const e=ER[j];if(e===e){if(xn>e){if(!(b==Gc&&m<55))r=YU.has(k)?Lc:Sc}else if(b==Sc&&SOVH.has(k)||(b==Sc&&k==C.Poland))r=AOCC[c]?Ac:Gc}}}
 if(m>=57.13&&WZ[c]&&r!=Sc){const w=WR[j];if(w===w&&xn<w)r=Lc;if(k==C.Netherlands&&y>51.95&&x<5.6&&m<68.2)r=Gc}
 for(let p=0;p<POCK.length;p++){const P=POCK[p];if(m<P[5]||m>=P[6])continue;const s=P[7]?1-.65*((m-P[5])/(P[6]-P[5]))**2:1;if(ell(y,x,P[0],P[1],P[2]*s,P[3]*s))r=P[4]}
 if(r==Ac)r=Gc;if(m>=68.27&&r==Gc)r=Lc;return r}
// ---------- time ----------
const STT=ST.st;const mOf=t=>{if(t<=STT[0])return -1;for(let i=1;i<STT.length;i++)if(t<STT[i])return i-2+(t-STT[i-1])/(STT[i]-STT[i-1]);return 68.999};
const tOf=m=>{const i=Math.max(0,Math.min(STT.length-2,Math.floor(m)+1));return STT[i]+(m-Math.floor(m))*(STT[i+1]-STT[i])};
const MON=['January','February','March','April','May','June','July','August','September','October','November','December'];
const dateOf=mi=>{const a=mi+8+1939*12;return MON[a%12]+' '+Math.floor(a/12)};
// ---------- theme colours ----------
const PAL={fantasy:{fill:['rgba(60,30,12,.45)','rgba(165,115,20,.36)','rgba(40,85,170,.34)','rgba(150,25,20,.32)','rgba(110,80,140,.34)','rgba(120,100,70,.08)'],str:['#8a1f12','#a5731a','#1f3d70','#8a1f12','#5e3f7a','#6b5a40']},
 simple:{fill:['#4a3326','#f5d887','#a7c8f3','#f3aaa2','#d3c3e6','#e6e4da'],str:['#c0471c','#d39a12','#2f6fdc','#e0453a','#7d5ba6','#9a9a90']},
 modern:{fill:['rgba(255,90,20,.12)','rgba(255,200,80,.24)','rgba(79,179,255,.26)','rgba(255,77,94,.27)','rgba(190,150,255,.22)','rgba(207,232,239,.05)'],str:['#ff7a1a','#ffc850','#4fb3ff','#ff4d5e','#be96ff','#5f7a86']}}[TH];
const parseC=s=>{if(s[0]=='#'){const n=parseInt(s.slice(1),16);return[n>>16,n>>8&255,n&255,1]}const q=s.match(/[\d.]+/g).map(Number);return[q[0],q[1],q[2],q[3]??1]};
const FILLC=PAL.fill.map(parseC);
// ---------- static layers ----------
Q=M.getContext('2d');seaBg();
if(TH=='fantasy'){for(let k=1;k<=6;k++){Q.save();Q.translate(-k*5,k*2.5);Q.strokeStyle=inkA(.2-k*.026);Q.lineWidth=1;Q.setLineDash([18+k*3,5+k*2]);Q.stroke(LAND);Q.restore()}Q.setLineDash([]);Q.fillStyle='rgba(239,224,184,.5)';Q.fill(LAND,'evenodd')}
else if(TH=='simple'){Q.strokeStyle='#c4e3f5';Q.lineWidth=26;Q.lineJoin='round';Q.stroke(LAND);Q.fillStyle='#eef0e2';Q.fill(LAND,'evenodd')}
else{Q.fillStyle='#101b24';Q.fill(LAND,'evenodd');Q.save();Q.clip(LAND,'evenodd');Q.strokeStyle='rgba(90,140,170,.12)';Q.lineWidth=1;for(let x=0;x<=1080;x+=60){Q.beginPath();Q.moveTo(x,0);Q.lineTo(x,1920);Q.stroke()}for(let y=0;y<=1920;y+=60){Q.beginPath();Q.moveTo(0,y);Q.lineTo(1080,y);Q.stroke()}Q.restore()}
const COAST=mkC();{const q=COAST.getContext('2d');q.lineJoin='round';if(TH=='fantasy'){q.strokeStyle=INK;q.lineWidth=2;q.stroke(LAND)}else if(TH=='simple'){q.strokeStyle='#7fb07a';q.lineWidth=2.6;q.stroke(LAND)}else{q.shadowColor='#78dcd2';q.shadowBlur=10;q.strokeStyle='#78dcd2';q.lineWidth=1.8;q.stroke(LAND)}}
// labels: countries, seas, cities
const LBc=mkC();{const q=LBc.getContext('2d');
 const lab=(t,lo,la,s,col,sp,rot=0)=>{const[x,y]=PX(lo,la);spaced(t,x,y,s,col,rot,sp,q)};
 const cf=TH=='fantasy'?(s=>`${s}px 'Uncial Antiqua'`):TT.L;const cc=TH=='modern'?'rgba(207,232,239,.75)':inkA(.72);
 [['Great Britain',-2.2,53.6],['France',2.4,46.4],['Spain',-3.6,39.6],['Italy',13.6,43.0],['Germany',10.2,50.6],['Poland',18.6,51.3],['Soviet Union',38.5,58.6],['Sweden',15.2,63.2],['Norway',9.2,61.6],['Finland',26.6,63.6],['Turkey',34.5,39.0],['Egypt',29.6,26.6],['Libya',17.5,27.2],['Algeria',3.0,29.0],['Romania',25.0,45.4],['Yugoslavia',18.6,43.9],['Greece',21.9,39.3],['Hungary',19.4,47.0]].forEach(([t,lo,la])=>lab(t,lo,la,cf(t=='Soviet Union'?30:21),cc,TH=='fantasy'?3:2));
 const sf=TT.I;const sc=TH=='modern'?'rgba(120,200,220,.6)':TH=='simple'?'rgba(60,110,150,.75)':inkA(.6);
 [['Atlantic Ocean',-8.6,47.0],['Mediterranean Sea',18.5,35.0],['Black Sea',34.4,43.3],['North Sea',3.4,56.2],['Baltic Sea',19.6,57.3]].forEach(([t,lo,la])=>lab(t,lo,la,sf(24),sc,TH=='fantasy'?3:2));
 window.CITIES=[['London',-0.12,51.5],['Paris',2.35,48.86],['Berlin',13.4,52.52],['Rome',12.5,41.9],['Moscow',37.62,55.75],['Leningrad',30.3,59.94],['Stalingrad',44.5,48.7],['Warsaw',21.0,52.23],['Cairo',31.24,30.04],['Athens',23.73,37.98],['Madrid',-3.7,40.42],['Kiev',30.52,50.45],['Vienna',16.37,48.21],['Tunis',10.18,36.8],['Belgrade',20.46,44.8]];
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
function fire(t){for(let c=0;c<NC;c++){GI[c]=own[c]==0?1:0;IA[c]=own[c]==1?1:0}blur(GI,2);blur(IA,2);const fl=.8+.2*Math.sin(t*13)*Math.sin(t*7.3);
 for(let c=0;c<NC;c++){const q=c*4;const s=(GI[c]-.5)*.6+nzc[c]*.05;bi.data[q]=bi.data[q+1]=bi.data[q+2]=255;bi.data[q+3]=255*c01((s+.02)/.14);
  si.data[q]=95;si.data[q+1]=52;si.data[q+2]=18;si.data[q+3]=s<.04?255*.5*c01((s+.2)/.18):0;const g=Math.exp(-(((s-.02)/.07)**2))*fl*(1-.8*IA[c]);gi.data[q]=255;gi.data[q+1]=120+90*g;gi.data[q+2]=30;gi.data[q+3]=255*Math.min(1,g*1.3)}
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
 else if(f=='gb'){q.fillStyle='#012169';q.fillRect(0,0,w,h);q.save();q.beginPath();q.rect(0,0,w,h);q.clip();q.strokeStyle='#fff';q.lineWidth=h*.2;q.beginPath();q.moveTo(0,0);q.lineTo(w,h);q.moveTo(w,0);q.lineTo(0,h);q.stroke();q.strokeStyle='#c8102e';q.lineWidth=h*.07;q.beginPath();q.moveTo(0,0);q.lineTo(w,h);q.moveTo(w,0);q.lineTo(0,h);q.stroke();q.restore();
  q.fillStyle='#fff';q.fillRect(w/2-h*.17,0,h*.34,h);q.fillRect(0,h/2-h*.17,w,h*.34);q.fillStyle='#c8102e';q.fillRect(w/2-h*.1,0,h*.2,h);q.fillRect(0,h/2-h*.1,w,h*.2)}}
function star(q,x,y,r,f,s){q.beginPath();for(let i=0;i<10;i++){const a=-Math.PI/2+i*Math.PI/5,rr=i%2?r*.42:r;q.lineTo(x+Math.cos(a)*rr,y+Math.sin(a)*rr)}q.closePath();if(s){q.strokeStyle=s;q.lineWidth=1.5;q.stroke()}q.fillStyle=f;q.fill()}
const FW=50,FH=33;const FLAGI={};['de','gb','us','su','fr','pl','it','gr','ro','hu','fi','yu','yp'].forEach(f=>{const c=document.createElement('canvas');c.width=FW*2;c.height=FH*2;const q=c.getContext('2d');q.scale(2,2);drawFlag(q,f,FW,FH);FLAGI[f]=c});
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
  const lk=B.n=='Elbe link-up';if(!lk)burst(x,y,.34+.05*Math.sin(t*9),t,TT.mark);else{X.strokeStyle=PAL.str[2];X.lineWidth=4;X.beginPath();X.arc(x,y,26+4*Math.sin(t*5),0,7);X.stroke()}
  X.restore();X.globalAlpha=u;spaced(B.n,x,lk?y+70:y+46,TT.L(TH=='fantasy'?25:23),TH=='modern'?'#ffc850':TH=='simple'?'#c0392b':'#7a1a0e',0,TH=='fantasy'?2:1,X);X.globalAlpha=1})}
// ---------- HUD ----------
const HUD=mkC();{Q=HUD.getContext('2d');panel(Q,40,36,1000,200);panel(Q,40,1508,1000,92);panel(Q,40,1614,1000,266);
 Q.fillStyle=INK;Q.textAlign='center';Q.font=TH=='fantasy'?TT.I(30):TT.L(24);Q.fillText(TH=='fantasy'?'The Second World War in Europe & North Africa':(TT.up?'WORLD WAR II · EUROPE & NORTH AFRICA':'World War II · Europe & North Africa'),540,84);Q.textAlign='left';
 const LG=[['Axis & occupied lands',0],['Allies',2],['Soviet Union',3],['Vichy France',4],['Neutral',5]];
 LG.forEach(([n,k],i)=>{const y=1668+i*42;if(k==0){Q.fillStyle='#1a0d06';Q.fillRect(78,y-20,36,24);const g=Q.createLinearGradient(78,0,114,0);g.addColorStop(0,'#ff7a1a');g.addColorStop(1,'#ffcf60');Q.fillStyle=g;Q.fillRect(78,y-5,36,4)}
  else{Q.fillStyle=PAL.fill[k];Q.fillRect(78,y-20,36,24);Q.strokeStyle=PAL.str[k];Q.lineWidth=2;Q.strokeRect(78,y-20,36,24)}Q.fillStyle=INK;Q.font=TT.L(TH=='fantasy'?21:20);Q.fillText(TT.up?n.toUpperCase():n,128,y)});
 const FK=[['de','Germany*'],['it','Italy'],['gb','Britain'],['us','United States'],['fr','France'],['su','Soviet Union'],['pl','Poland'],['gr','Greece'],['ro','Romania'],['hu','Hungary'],['fi','Finland'],['yp','Yugoslavia']];
 FK.forEach(([f,n],i)=>{const x=480+(i%2)*270,y=1660+Math.floor(i/2)*36;Q.drawImage(FLAGI[f],x,y-20,36,24);Q.strokeStyle='rgba(0,0,0,.35)';Q.lineWidth=1;Q.strokeRect(x,y-20,36,24);Q.fillStyle=INK;Q.font=TT.L(TH=='fantasy'?21:20);Q.fillText(TT.up?n.toUpperCase():n,x+48,y)});
 Q.font=TT.I(17);Q.fillStyle=inkA(.75);Q.fillText(TT.up?'*GERMANY IN ITS OLD IMPERIAL COLOURS':'*Germany is shown in its old imperial colours',480,1868)}
const capOf=mi=>{let c=null,k=-9;for(const key in ST.cap){const v=+key;if(v<=mi&&v>k){k=v;c=ST.cap[key]}}return[c,k]};
function hud(t,m){X.drawImage(HUD,0,0);const mi=Math.max(-1,Math.min(68,Math.floor(m)));const ds=dateOf(mi);const pop=c01((t-tOf(mi))/.18);
 X.save();X.textAlign='center';X.fillStyle=INK;X.font=TT.T(TH=='fantasy'?70:72);X.globalAlpha=.4+.6*pop;X.fillText(TT.up?ds.toUpperCase():ds,540,168+(1-pop)*8);X.restore();
 // timeline bar
 const x0=110,x1=970,ty=206;X.strokeStyle=inkA(.35);X.lineWidth=3;X.beginPath();X.moveTo(x0,ty);X.lineTo(x1,ty);X.stroke();X.font=TT.I(16);X.textAlign='center';
 for(let y=1939;y<=1945;y++){const mm=(y-1939)*12-8;const xx=x0+(mm+1)/70*(x1-x0);X.fillStyle=inkA(.6);X.fillRect(xx-1,ty-7,2,14);X.fillText(String(y),xx,ty+26)}
 const px=x0+c01((m+1)/70)*(x1-x0);X.strokeStyle=PAL.str[0];X.lineWidth=5;X.beginPath();X.moveTo(x0,ty);X.lineTo(px,ty);X.stroke();X.fillStyle=PAL.str[0];X.beginPath();X.arc(px,ty,8,0,7);X.fill();X.textAlign='left';
 const[cap,ck]=capOf(mi);if(cap){const a=c01((t-tOf(ck))/.3);let fs=TH=='fantasy'?30:31;X.font=TT.I(fs);while(X.measureText(cap).width>950&&fs>18){fs--;X.font=TT.I(fs)}X.globalAlpha=a;X.fillStyle=INK;X.textAlign='center';X.fillText(TT.up?cap.toUpperCase():cap,540,1566);X.textAlign='left';X.globalAlpha=1}}
window.DUR=ST.dur;window.CAPTURE=cv;window._F={solve,paintFill,borders,fire,armies,hud,battles};
window.render=t=>{const m=mOf(t);X.fillStyle=BGC;X.fillRect(0,0,1080,1920);const rv=c01(t/.8);X.globalAlpha=rv;X.drawImage(M,0,0);
 solve(m);paintFill();MX.globalCompositeOperation='source-over';MX.clearRect(0,0,1080,MH);MX.imageSmoothingEnabled=true;MX.imageSmoothingQuality='high';MX.drawImage(low,0,0,1080,MH);MX.save();MX.translate(0,-Y0);const X0=X;{const X=MX;
 const bp=borders();X.lineJoin='round';X.lineCap='round';if(TH=='simple'){X.strokeStyle='#fff';X.lineWidth=5;X.stroke(bp);X.strokeStyle='#33363d';X.lineWidth=1.8;X.stroke(bp)}else if(TH=='fantasy'){X.strokeStyle=inkA(.85);X.lineWidth=2.4;X.stroke(bp)}else{X.shadowColor='#cfe8ef';X.shadowBlur=6;X.strokeStyle='rgba(207,232,239,.85)';X.lineWidth=1.8;X.stroke(bp)}}MX.restore();MX.shadowBlur=0;MX.globalCompositeOperation='destination-in';MX.drawImage(LMASK,0,0);X.drawImage(MAPL,0,Y0);
 X.drawImage(COAST,0,0);fire(t);X.drawImage(LBc,0,0);battles(t);armies(t,m);hud(t,m);if(TH=='fantasy'){Q=X;frameEdge()}X.globalAlpha=1};
'''
BG = {'fantasy': '#7d5a2c', 'simple': '#a9d4ef', 'modern': '#070b10'}
for th in ['fantasy', 'simple', 'modern']:
    js = f"const TH='{th}';const GEO={geo};const FR={fronts};const ST={story};" + CORE + WW
    page(f'map_ww2_{th}', BG[th], js, css=FONTS)
print('ok')
