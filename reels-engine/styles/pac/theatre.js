// Pacific theatre: who holds each cell in month m (0 = Dec 1941). Gc = Japan (fire), Ac = China, Lc = Allies, Sc = USSR, Nc = neutral
const D=s=>{const[y,mo,d]=s.split('-').map(Number);return(y-1941)*12+(mo-12)+(d-1)/30};
const CK=toRows(FR.CF);const CR=new Float32Array(GH);let BLv,BRv,MFv;
function frameVals(m){BLv=k1(FR.BL,m);BRv=k1(FR.BR,m);MFv=k1(FR.MF,m);rowsAt(CK,m,CR)}
const END=D('1945-09-02'),SOVIN=D('1945-08-09'),WAR=D('1941-12-08');
const manch=(x,y)=>(y>39.8&&x>118.5)||(y>41&&x>115.5)||(y>40.3&&x>110);
const hyp=Math.hypot;
function base(k,x,y,xn,yn,m,j){switch(k){
 case C.China:{if(y<20.3&&x>108.4)return m>=END?Ac:Gc;
  if(manch(x,y))return m>=SOVIN+.45*(.5*c01((50-y)/11)+.5*c01(1-Math.abs(x-124)/8))?Sc:Gc;
  if(x<100)return Ac;if(y>24.3&&y<28.3&&x>114.8&&x<118.6)return Ac;
  const e=CR[j];const r=(e===e&&xn>e)?Gc:Ac;return(m>=END&&r==Gc)?Ac:r}
 case C['Hong Kong']:return(m<WAR||!sw(m,WAR,.57,(22.55-y)/.35)||m>=END)?Lc:Gc;
 case C.Macao:return Nc;
 case C.Taiwan:return m>=END?Ac:Gc;
 case C['North Korea']:return m>=D('1945-08-12')+.4*c01((42.5-y)/4.5)?Sc:Gc;
 case C['South Korea']:return Gc;
 case C.Japan:{if(y<27.5&&x>140)return m>=D('1945-02-19')+1.2*c01((141.4-x)/.3)?Lc:Gc;
  if(y<27.2&&y>25.9&&x>127.4&&x<128.5){const v=y>26.4?.25*c01((y-26.4)/.5):.3+.7*c01((26.4-y)/.35);return m>=D('1945-04-01')+2.7*v?Lc:Gc}return Gc}
 case C.Russia:if(x>141.5&&x<144.8&&y<50&&y>45.8)return m>=D('1945-08-11')+.5*c01((50-y)/4)?Sc:Gc;
  if(x>145.4&&y>43.3&&y<51)return m>=D('1945-08-18')+.45*c01((51-y)/7.6)?Sc:Gc;return Sc;
 case C.Mongolia:return Sc;
 case C.Vietnam:case C.Laos:case C.Cambodia:return m>=END?(y>16?Ac:Lc):Gc;
 case C.Thailand:return m<WAR?Nc:Gc;
 case C.Myanmar:return(y<Math.min(BLv,26.8)&&!(y>BRv))?Gc:Lc;
 case C.India:if(x<94&&y<14.5&&y>6.5)return(m>=D('1942-03-23')&&m<END)?Gc:Lc;if(m>=D('1944-03-15')&&m<D('1944-07-05')&&ell(y,x,25.05,94.45,.42,.3))return Gc;return Lc;
 case C.Bhutan:return Nc;
 case C.Malaysia:if(x<105)return(m>=WAR&&y>MFv)?Gc:Lc;return sw(m,D('1941-12-16'),1.3,(7.3-y)/6)?Gc:Lc;
 case C.Singapore:return m>=D('1942-02-15')?Gc:Lc;
 case C.Brunei:return(m>=D('1941-12-16')&&m<D('1945-06-10'))?Gc:Lc;
 case C.Indonesia:{let cap,lib=END;
  if(x>108.5&&x<119.3&&y>-4.5){cap=D('1942-01-11')+1.0*c01((4.3-y)/7.5);if(y>3&&x>117)lib=D('1945-05-01');if(x>115.5&&y<0&&y>-2)lib=D('1945-07-01')}
  else if(x>=119.3&&x<125.4&&y>-6.5&&y<2.5)cap=D('1942-01-11')+1.8*c01((1.5-y)/7);
  else if(x>=125.4&&x<131&&y>-9){cap=D('1942-01-30')+1.2*c01((y+4)/7);if(x>127.8&&x<129&&y>1.9&&y<2.8)lib=D('1944-09-15')}
  else if(x>=131){cap=D('1942-04-01')+1.0*c01((x-131)/10);lib=D('1944-04-22')+3.3*c01((141-x)/10)}
  else if(x<106.5&&y>-6.2)cap=D('1942-02-14')+1.4*c01((y+3.5)/9);
  else if(y<-5.8&&x<114.6)cap=D('1942-03-01')+.27*c01((114.6-x)/9);
  else cap=D('1942-02-19')+.4*c01((x-114.5)/10);
  return(m>=cap&&m<lib)?Gc:Lc}
 case C['Timor-Leste']:return m>=D('1942-02-20')?Gc:Nc;
 case C.Philippines:{if(m<D('1942-04-09')&&ell(y,x,14.6,120.45,.25,.18))return Lc;
  const cap=y>12.5?D('1941-12-10')+.75*c01((18.6-y)/4.2):D('1941-12-20')+4.4*c01(hyp(y-7.07,x-125.6)/6);let lib;
  if(x>124.2&&y>9.9&&y<12.7)lib=D('1944-10-20')+2.1*c01(hyp(y-11,x-125)/1.6);
  else if(y>12.1&&y<13.6&&x>120.3&&x<121.6)lib=D('1944-12-15')+.6;
  else if(y>=12.5)lib=(y>16.6&&x>120.6)?END:D('1945-01-09')+5*c01(hyp(y-16,x-120.3)/3.5);
  else if(x<120)lib=D('1945-02-28')+.3;else lib=D('1945-03-18')+3.5*c01(hyp(y-10.5,x-122.5)/5);
  return(m>=cap&&m<lib)?Gc:Lc}
 case C.Guam:return(m>=D('1941-12-10')&&m<D('1944-07-21')+.65)?Gc:Lc;
 case C['N. Mariana Is.']:{const lib=y>15.35?END:y>15.08?D('1944-06-15')+.8:y>14.4?D('1944-07-24')+.27:END;return m<lib?Gc:Lc}
 case C.Palau:case C.Micronesia:return Gc;
 case C['Marshall Is.']:{const lib=((x>166.6&&x<168.2&&y>8.6&&y<9.5)||(x>170.9&&x<171.5&&y>7&&y<7.3))?D('1944-01-31')+.1:(x<162.6&&y>11.2)?D('1944-02-19'):END;return m<lib?Gc:Lc}
 case C.Kiribati:return(x<177&&m>=D('1941-12-10')&&m<D('1943-11-20')+.1)?Gc:Lc;
 case C.Nauru:return m>=D('1942-08-26')?Gc:Lc;
 case C['United States of America']:if(y>51&&y<53.2&&x>172&&x<178.5){const lib=x<175?D('1943-05-30'):D('1943-08-15');return(m>=D('1942-06-07')&&m<lib)?Gc:Lc}return Lc;
 case C['Papua New Guinea']:{let cap=null,lib=END;
  if(x>148&&x<153.5&&y>-6.6&&y<-2.3){cap=D('1942-01-23')+.4*c01((152.5-x)/4);if(x<150)lib=D('1943-12-26')+2*c01((x-148)/2)}
  else if(x>154&&y>-7&&y<-4.8)cap=D('1942-03-30');
  else if(y>-2.5&&y<-1.7&&x>146&&x<148){cap=D('1942-04-08');lib=D('1944-02-29')+.8}
  else if(y>-9.6&&y<-8&&x>147.3&&x<148.7){cap=D('1942-07-21')+1.8*c01((148.5-x)/1.1);lib=D('1942-09-26')+3.9*c01((x-147.3)/1.2)}
  else if(y>-7.6&&y<-5.4&&x>146.3&&x<148.2){cap=D('1942-03-08');lib=D('1943-09-11')+1.3*c01((x-146.6)/1.5)}
  else if(y>-6&&y<-2.6&&x>141&&x<146.3){cap=D('1942-12-15')+c01((146.3-x)/5);lib=x>145?D('1944-04-24'):x<142.9?D('1944-04-22')+.3:D('1945-05-11')}
  if(cap===null)return Lc;return(m>=cap&&m<lib)?Gc:Lc}
 case C['Solomon Is.']:{if(y>-10&&y<-9&&x>159.5&&x<161){if(m<D('1942-07-06'))return Lc;if(m<D('1942-08-07'))return Gc;return m<D('1942-08-07')+6.1*c01((160.2-x)/.75)?Gc:Lc}
  if(x<158.5&&y>-8.6&&y<-7.6)return(m>=D('1942-10-01')&&m<D('1943-06-30')+1.7)?Gc:Lc;
  if(y>-8.6&&x<159.8)return(m>=D('1942-05-03')&&m<D('1943-10-15')+1)?Gc:Lc;return Lc}}
 return Lc}
function ctrl(c,m){const k=CN[c];if(!k)return -1;let r=base(k,LON[c],LAT[c],NX[c],NY[c],m,ROW[c]);if(m>=END&&r==Gc)r=Lc;return r}
