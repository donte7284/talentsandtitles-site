"""Parable No. 10, manna, timed to a voiceover.

usage: python ep10_manna.py <voice audio> <word timestamps json> <out.mp4>
Exodus 16:14-21: small round thing fine as frost (14), "It is manna" (15), an omer for every man (16),
some more, some less, nothing over and no lack (17-18), "Let no man leave of it till the morning" (19),
some did; it bred worms and stank (20).
"""
import json,os,sys
from base import build
from episode import Voice,HERE

v=Voice(*sys.argv[1:3]);out=sys.argv[3];at=v.at
T=dict(
 morning=at('morning in the wilderness'),small=at('small and round'),frost=at('fine as frost'),manna=at('it is manna'),
 bread=at('the bread'),omer=at('an omer'),more=at('some gather more'),nobody=at('nobody has'),
 leave=at('leave none'),anyway=at('some do anyway'),worms=at('it breeds worms'),stinks=at('it stinks'),
)
punch=at('enough for today');c2=at('what are you holding')

SCENE=r'''
const T=__T__,RED='#d9735a';
const gr=el('line',{x1:60,y1:700,x2:1020,y2:700,stroke:GOLD,'stroke-width':5,'stroke-linecap':'round',opacity:.6});
// flakes falling like frost
const fl=[...Array(36)].map((_,i)=>el('circle',{r:7+(i%3)*3,fill:i%4?CR:BR}));
// jars: one omer each
const J=[0,1,2].map(i=>{const g=el('g',{transform:`translate(${240+i*300},700)`});
 el('path',{d:'M-70 -190 H70 L90 -150 Q100 -60 70 0 H-70 Q-100 -60 -90 -150 Z',fill:'#0f1f3a',stroke:GOLD,'stroke-width':8,'stroke-linejoin':'round'},g);
 const f=el('path',{d:'',fill:CR,opacity:.85},g);return{g,f}});
const wm=[0,1,2].map(i=>{const g=el('g',{});for(let k=0;k<3;k++)el('path',{d:`M${-20+k*20} 0 q-10 -14 0 -28 q10 -14 0 -28`,fill:'none',stroke:RED,'stroke-width':5,'stroke-linecap':'round'},g);return g});
const mound=el('path',{d:'',fill:'none',stroke:BR,'stroke-width':7,'stroke-linecap':'round'});
const worm=[0,1,2,3,4].map(i=>el('path',{d:'',fill:'none',stroke:RED,'stroke-width':6,'stroke-linecap':'round'}));
function scene(t){
 gr.setAttribute('opacity',.6*eo(pr(t,0.3,0.7)));
 fl.forEach((c,i)=>{const s=T.small+i*0.07,p=pr(t,s,1.6);const x=110+((i*97)%860),y=120+eo(p)*(540+(i%5)*10);
  c.setAttribute('cx',x+Math.sin(t*2+i)*8);c.setAttribute('cy',y);c.setAttribute('opacity',(t>s?1:0)*(p>=1?0.9:1)*(1-eo(pr(t,T.omer-0.3,0.6))*0.0))});
 // flakes settle into a frosty line, then jars take their place
 const ja=eo(pr(t,T.omer,0.6));
 J.forEach(({g,f},i)=>{
  g.setAttribute('opacity',ja);
  const fi=eo(pr(t,T.omer+0.2+i*0.25,0.7));const y=-10-fi*150;
  const rot=t>T.worms+i*0.15;
  f.setAttribute('d',`M-76 ${y} H76 L88 -10 H-88 Z`);
  const keep=(i==2&&t>T.leave);
  f.setAttribute('fill',keep&&t>T.worms?RED:CR);
  g.children[0].setAttribute('stroke',keep&&t>T.worms?RED:GOLD);
 });
 // the jar left till morning spoils
 const w=eio(pr(t,T.worms,0.7));
 wm.forEach((g,i)=>{g.setAttribute('transform',`translate(${240+2*300-60+i*60},${480-w*60+Math.sin(t*3+i)*10}) scale(${1})`);g.setAttribute('opacity',w*(i%2?1:.8)*(t>=T.stinks-0.3?1:0)*0+w*(t>=T.stinks?1:0))});
 worm.forEach((p,i)=>{const o=eo(pr(t,T.worms+i*0.12,0.4));const x=780+i*20-40,y=690-i*20;let d='M'+x+' '+y;for(let k=1;k<=6;k++)d+=' L'+(x+k*14)+' '+(y+Math.sin(t*8+k+i)*8);p.setAttribute('d',d);p.setAttribute('opacity',o)});
 const c=t>=T.worms?'WORMS · STINK':t>=T.leave?'LEAVE NONE TILL MORNING':t>=T.omer?'ONE OMER EACH':t>=T.manna?'MANNA':t>=T.small?'SMALL · ROUND · FINE AS FROST':'';
 $('count').textContent=c;$('count').style.color=t>=T.worms?RED:'#c9a24a';$('count').style.opacity=c?1:0;
}
'''
CAPS=[["Leave ",0,0],["none ",1,0],["of ",0,0],["it ",0,0],["till ",0,0],["the ",0,0],["morning.",1,0]]
capw=v.capw(CAPS)
html=os.path.join(HERE,'ep10_manna.html')
build(html,10,'Enough','for today.','EXODUS 16 : 14–21',CAPS,capw[0],punch-0.1,SCENE.replace('__T__',json.dumps(T)),
      capw=capw,cue=dict(c1=punch+0.1,c2=c2,hl=c2+0.25,ref=c2+0.9))
v.finish('ep10',html,out)
