const EK=toRows(FR.E),WK=toRows(FR.W);const ER=new Float32Array(GH),WR=new Float32Array(GH);
const ro_=m=>m<14.73?Nc:m<59.73?Ac:Sc, hun=m=>m<14.63?Nc:m<54.6?Ac:Gc;
const SIT=new Float32Array(NC);const EZ=new Uint8Array(NC),WZ=new Uint8Array(NC),AOCC=new Uint8Array(NC);
const SOVH=new Set(['Russia','Ukraine','Belarus','Moldova','Lithuania','Latvia','Estonia'].map(n=>C[n]));
const YU=new Set(['Serbia','Croatia','Bosnia and Herz.','Slovenia','Montenegro','Kosovo','Macedonia'].map(n=>C[n]));
const EZC=new Set([...SOVH,...['Poland','Hungary','Slovakia','Czechia','Austria','Germany','Serbia','Croatia','Bosnia and Herz.','Slovenia','Montenegro','Kosovo'].map(n=>C[n])]);
const WZC=new Set(['France','Belgium','Netherlands','Luxembourg','Germany','Austria','Czechia'].map(n=>C[n]));
const NEU=new Set(['Spain','Portugal','Andorra','Switzerland','Liechtenstein','Sweden','Turkey','Saudi Arabia','Ireland','W. Sahara'].map(n=>C[n]));
const SOVX=new Set(['Kazakhstan','Georgia','Armenia','Azerbaijan','Turkmenistan'].map(n=>C[n]));
for(let j=0;j<GH;j++)for(let i=0;i<GW;i++){const c=j*GW+i,x=i*4+2,y=Y0+j*4+2,lon=LON[c],lat=LAT[c];const nz=NX[c]-lon;
 let s=((lat-38.1)*7.36+(lon-15.65)*(-6.46))/95.9;if(lat>43)s-=.06*c01((12-lon)/1.6);SIT[c]=s+nz*.02;
 const k=CN[c];const rx=(k==C.Romania&&((lat>46.35&&lon<25)||(lat>45.95&&lon>=24.4&&lon<26.3)));EZ[c]=(EZC.has(k)||rx)?1:0;WZ[c]=WZC.has(k)?1:0;
 AOCC[c]=(k==C.Moldova||(k==C.Ukraine&&((lat<48.4&&lat>47.7&&lon>24.9&&lon<27.4)||(lat<46.65&&lon>28.2&&lon<30.6)||(lat<48.6&&lat>46.3&&lon>28.2&&lon<31.3))))?1:0}
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
