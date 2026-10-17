"""Parable No. 4, Joseph's grain, timed to a voiceover.

usage: python ep04_joseph_grain.py <voice audio> <word timestamps json> <out.mp4>
Genesis 41:47-57: seven plenteous years, grain laid up in the cities, famine in all lands,
bread in Egypt, "Go unto Joseph", the storehouses opened.
"""
import json,os,sys
from base import build
from episode import Voice,HERE

v=Voice(*sys.argv[1:3]);out=sys.argv[3];at=v.at
T=dict(
 harvest=at('harvest'),seven=at('seven years'),gathers=at('gathers'),stops=at('stops counting'),
 end=at('good years end'),famine=at('famine'),bread=at('there is bread'),goj=at('go unto joseph'),
 opens=at('opens the storehouses'),opensend=at('opens the storehouses',end=True),
)
punch=at('the famine');c1=at('it only showed');c2=at('store up now')

SCENE=r'''
const T=__T__;
const GY=760,RED='#d9735a';
el('line',{x1:60,y1:GY,x2:1020,y2:GY,stroke:GOLD,'stroke-width':6,'stroke-linecap':'round',pathLength:1,'stroke-dasharray':1,id:'ground'});
// stalks of grain either side of the storehouse
function stalk(x,col){const g=el('g',{});el('line',{x1:0,y1:0,x2:0,y2:-210,stroke:col,'stroke-width':6,'stroke-linecap':'round'},g);
 [-210,-165,-120].forEach(y=>{[-1,1].forEach(s=>el('ellipse',{cx:s*16,cy:y,rx:9,ry:22,transform:`rotate(${s*28} ${s*16} ${y})`,fill:col,opacity:.9},g))});
 el('ellipse',{cx:0,cy:-235,rx:9,ry:22,fill:col},g);return g}
const XS=[90,150,210,270,330,750,810,870,930,990].map(x=>x*1);
const ok=XS.map(x=>stalk(x,BR)),bad=XS.map(x=>stalk(x,RED));
// storehouse
const sh=el('g',{});
el('rect',{x:410,y:520,width:260,height:240,fill:'none',stroke:GOLD,'stroke-width':7,'stroke-linejoin':'round'},sh);
el('path',{d:'M385 525 L540 405 L695 525Z',fill:'none',stroke:GOLD,'stroke-width':7,'stroke-linejoin':'round'},sh);
const grain=el('rect',{x:417,y:753,width:246,height:0,fill:BR,opacity:.9},sh);
const lines=[0,1,2,3].map(i=>el('line',{x1:417,y1:0,x2:663,y2:0,stroke:'#0f1f3a','stroke-width':3,opacity:.25},sh));
const doorGlow=el('rect',{x:495,y:640,width:90,height:120,fill:BR,opacity:0},sh);
const door=el('rect',{x:0,y:0,width:90,height:120,fill:'#0f1f3a',stroke:GOLD,'stroke-width':5},sh);
// seven years
const dots=[0,1,2,3,4,5,6].map(i=>el('circle',{cx:330+i*70,cy:80,r:15,fill:'none',stroke:GOLD,'stroke-width':5}));
const yrs=el('text',{x:540,y:140,'text-anchor':'middle','font-size':28,'font-weight':600,'letter-spacing':7,fill:GOLD});yrs.textContent='SEVEN YEARS';
// bread
const loaf=el('g',{});el('ellipse',{cx:0,cy:0,rx:62,ry:36,fill:BR,stroke:GOLD,'stroke-width':5},loaf);
[-24,0,24].forEach(x=>el('path',{d:`M${x-8} -14 L${x+8} 14`,stroke:'#0f1f3a','stroke-width':4,opacity:.4,'stroke-linecap':'round'},loaf));
const breadT=el('text',{x:540,y:300,'text-anchor':'middle','font-size':30,'font-weight':700,'letter-spacing':7,fill:CR});breadT.textContent='BREAD';
// "Go unto Joseph"
const aL=el('path',{d:'M60 640 H320 M290 618 L322 640 L290 662',fill:'none',stroke:CR,'stroke-width':6,'stroke-linecap':'round','stroke-linejoin':'round',pathLength:1,'stroke-dasharray':1});
const aR=el('path',{d:'M1020 640 H760 M790 618 L758 640 L790 662',fill:'none',stroke:CR,'stroke-width':6,'stroke-linecap':'round','stroke-linejoin':'round',pathLength:1,'stroke-dasharray':1});
function scene(t){
 $('ground').setAttribute('stroke-dashoffset',1-eo(pr(t,0.2,0.8)));
 const w=eio(pr(t,T.end,1.3));
 XS.forEach((x,i)=>{const g=pr(t,T.harvest+i*0.07,0.8);const sw=Math.sin(t*2+i)*2*(1-w);
  const tf=`translate(${x},${GY}) rotate(${sw+w*(i%2?1:-1)*38}) scale(1,${eo(g)*(1-0.5*w)})`;
  ok[i].setAttribute('transform',tf);bad[i].setAttribute('transform',tf);
  ok[i].setAttribute('opacity',g>0?1-w:0);bad[i].setAttribute('opacity',g>0?w:0)});
 // storehouse draws in on "gathers", grain fills until "stops counting"
 sh.setAttribute('opacity',eo(pr(t,T.harvest+0.6,0.7)));
 const lv=eio(pr(t,T.gathers,Math.max(1,T.stops+0.6-T.gathers)));
 grain.setAttribute('y',753-228*lv);grain.setAttribute('height',228*lv);
 lines.forEach((l,i)=>{const y=753-228*(i+1)/5;l.setAttribute('y1',y);l.setAttribute('y2',y);l.setAttribute('opacity',lv>(i+1)/5?.25:0)});
 const o=eio(pr(t,T.opens,0.9));door.setAttribute('transform',`translate(495,640) scale(${1-0.92*o},1)`);doorGlow.setAttribute('opacity',o);
 dots.forEach((d,i)=>{const a=eo(pr(t,T.seven+i*0.13,0.3));d.setAttribute('opacity',a);d.setAttribute('fill',t>=T.end?RED:(a>.5?BR:'none'));d.setAttribute('stroke',t>=T.end?RED:GOLD)});
 yrs.setAttribute('opacity',eo(pr(t,T.seven,0.4)));yrs.setAttribute('fill',t>=T.end?RED:GOLD);
 const b=bounce(pr(t,T.bread-0.2,0.7));loaf.setAttribute('transform',`translate(540,${150+(360-150)*b-0})`);
 loaf.setAttribute('opacity',t>T.bread-0.2?1:0);breadT.setAttribute('opacity',eo(pr(t,T.bread+0.3,0.4)));
 aL.setAttribute('stroke-dashoffset',1-eio(pr(t,T.goj,0.6)));aR.setAttribute('stroke-dashoffset',1-eio(pr(t,T.goj,0.6)));
 aL.setAttribute('opacity',t>T.goj?1:0);aR.setAttribute('opacity',t>T.goj?1:0);
 const c=t>=T.goj?'“GO UNTO JOSEPH”':t>=T.famine?'FAMINE · ALL LANDS':t>=T.stops?'WITHOUT NUMBER':'';
 $('count').textContent=c;$('count').style.color=t>=T.goj?'#f4ecd8':t>=T.famine?RED:'#c9a24a';
 $('count').style.opacity=c?1:0;
}
'''
CAPS=[["Famine ",0,0],["hits ",0,0],["all ",0,0],["lands,",0,1],["but ",0,0],["in ",0,0],["Egypt ",0,0],["there ",0,0],["is ",0,0],["bread.",1,0]]
capw=v.capw(CAPS)
html=os.path.join(HERE,'ep04_joseph_grain.html')
build(html,4,'It only showed who had one.','Store up now.','GENESIS 41 : 47–57',CAPS,capw[0],punch-0.1,SCENE.replace('__T__',json.dumps(T)),
      capw=capw,cue=dict(c1=c1,c2=c2,hl=c2+0.25,ref=c2+0.9))
v.finish('ep04',html,out)
