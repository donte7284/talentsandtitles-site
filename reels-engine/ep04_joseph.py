"""Parable No. 4, Joseph's grain, timed to a voiceover.

usage: python ep04_joseph.py <voice audio> <word timestamps json> <out.mp4>
Genesis 41:47-57: seven plenteous years, grain laid up in the cities, famine, "Go unto Joseph", storehouses opened.
"""
import json,os,sys
from base import build
from episode import Voice,HERE
from kit import KIT

v=Voice(*sys.argv[1:3]);out=sys.argv[3];at=v.at
T=dict(
 seven=at('seven good years'),lays=at('lays up'),corn=at('gathers corn'),stops=at('stops counting'),
 end=at('years end'),famine=at('famine comes'),cry=at('cry to pharaoh'),go=at('go unto joseph'),opens=at('opens the storehouses'),
)
punch=at("the famine doesn't");finds=at('it finds out');who=at('who had one')

SCENE=KIT+r'''
const T=__T__;
const GY=780;
const ground=line(`M70 ${GY} H1010`,GOLD,6,{id:'g'});
// seven tally marks: the good years
const tally=[0,1,2,3,4,5,6].map(i=>{const g=el('g',{transform:`translate(${255+i*95},120)`});el('circle',{r:26,fill:BR,'fill-opacity':.25,stroke:GOLD,'stroke-width':5},g);
 el('path',{d:'M0 14 V-14 M0 -2 Q-12 -4 -14 -14 M0 -2 Q12 -4 14 -14 M0 8 Q-12 6 -14 -4 M0 8 Q12 6 14 -4',fill:'none',stroke:GOLD,'stroke-width':4,'stroke-linecap':'round'},g);return g});
const yrs=txt(540,215,'SEVEN YEARS OF PLENTY',30,GOLD,7);
// storehouse
const body=line(`M360 ${GY} V500 H720 V${GY}`,GOLD,7);
const roof=line('M335 505 L540 365 L745 505',GOLD,7);
const clip=el('clipPath',{id:'sc'});el('rect',{x:364,y:500,width:352,height:GY-500},clip);
const fill=el('rect',{x:364,y:GY,width:352,height:0,fill:BR,opacity:.55,'clip-path':'url(#sc)'});
const glow=el('rect',{x:470,y:620,width:140,height:GY-620,fill:BR,opacity:0});
const doorL=el('rect',{x:470,y:620,width:70,height:GY-620,fill:'#0f1f3a',stroke:GOLD,'stroke-width':5});
const doorR=el('rect',{x:540,y:620,width:70,height:GY-620,fill:'#0f1f3a',stroke:GOLD,'stroke-width':5});
// grain falling in
const grains=Array.from({length:28},(_,i)=>el('circle',{r:9,fill:BR,opacity:0}));
// famine cracks
const cracks=['M130 780 l30 40 -20 40 40 50','M300 780 l-20 50 30 40','M760 780 l30 45 -25 40 30 50','M930 780 l-25 40 30 40 -15 40','M60 780 l20 30'].map(d=>line(d,RED,5));
const sun=el('circle',{cx:900,cy:380,r:60,fill:'none',stroke:BR,'stroke-width':6});
const rays=Array.from({length:10},(_,i)=>{const a=i*Math.PI/5;return line(`M${900+Math.cos(a)*80} ${380+Math.sin(a)*80} L${900+Math.cos(a)*108} ${380+Math.sin(a)*108}`,BR,6)});
// loaves for the people crying for bread (objects only)
const loaves=[0,1,2].map(i=>{const g=el('g',{transform:`translate(${130+i*70},${640+(i%2)*30})`});el('path',{d:'M-28 10 Q-30 -22 0 -24 Q30 -22 28 10 Z',fill:'none',stroke:RED,'stroke-width':5,'stroke-linejoin':'round'},g);
 el('path',{d:'M-10 -14 l6 14 M6 -16 l6 14',stroke:RED,'stroke-width':4,'stroke-linecap':'round'},g);return g});
const lab1=txt(540,880,'STOREHOUSES FULL',30,GOLD,7),lab2=txt(540,880,'FAMINE',34,RED,10),lab3=txt(540,880,'“GO UNTO JOSEPH”',30,BR,7),lab4=txt(540,880,'STOREHOUSES OPEN',30,BR,7);
function scene(t){
 dash(ground,eo(pr(t,0.2,0.8)));
 const famine=eo(pr(t,T.end,0.7));
 ground.setAttribute('stroke',famine>0.5?RED:GOLD);
 tally.forEach((g,i)=>{const a=eo(pr(t,T.seven+i*0.12,0.3));const d=eo(pr(t,T.end+0.1*i,0.4));op(g,a*(1-0.65*d))});
 op(yrs,eo(pr(t,T.seven+0.6,0.5))*(1-famine));
 dash(body,eio(pr(t,T.lays,0.8)));dash(roof,eio(pr(t,T.lays+0.5,0.7)));
 grains.forEach((g,i)=>{const s=T.corn+i*(T.stops+0.3-T.corn)/28;const p=pr(t,s,0.5);
  g.setAttribute('cx',480+(i*37%220));g.setAttribute('cy',250+(GY-40-250)*p*p-((i*53)%90)*(1-p)*0);op(g,p>0&&p<1?1:0)});
 const lvl=eio(pr(t,T.corn,T.stops-T.corn+0.6));fill.setAttribute('y',GY-lvl*270);fill.setAttribute('height',lvl*270);
 op(lab1,eo(pr(t,T.stops+0.2,0.5))*(1-famine));
 sun.setAttribute('stroke',famine>0.3?RED:BR);op(sun,eo(pr(t,T.seven,0.6)));
 rays.forEach((r,i)=>{op(r,eo(pr(t,T.seven+0.3,0.5))*(1-famine));r.setAttribute('transform',`rotate(${t*10} 900 380)`)});
 cracks.forEach((c,i)=>{dash(c,eio(pr(t,T.famine+i*0.1,0.5)));op(c,t>T.famine?1:0)});
 op(lab2,eo(pr(t,T.famine,0.4))*(1-eo(pr(t,T.go,0.3))));
 loaves.forEach((g,i)=>op(g,eo(pr(t,T.cry+i*0.15,0.4))));
 op(lab3,eo(pr(t,T.go,0.4))*(1-eo(pr(t,T.opens,0.3))));
 const o=eio(pr(t,T.opens,0.7));
 doorL.setAttribute('x',470-o*70);doorL.setAttribute('width',70-o*55);doorR.setAttribute('x',540+o*55);doorR.setAttribute('width',70-o*55);
 op(glow,o);op(lab4,eo(pr(t,T.opens+0.3,0.4)));
 op(doorL,t>T.lays+0.8?1:0);op(doorR,t>T.lays+0.8?1:0);
 $('count').textContent='';
}
'''
CAPS=[["Seven ",0,0],["good ",0,0],["years, ",0,1],["then ",1,0],["famine.",1,0]]
capw=v.capw(CAPS)
html=os.path.join(HERE,'ep04_joseph.html')
build(html,4,'The famine finds out','Who had one.','GENESIS 41 : 47–57',CAPS,capw[0],punch-0.1,SCENE.replace('__T__',json.dumps(T)),
      capw=capw,cue=dict(c1=punch,c2=who,hl=who+0.25,ref=who+0.9))
v.finish('ep04',html,out)
