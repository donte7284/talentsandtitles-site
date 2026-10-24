"""Parable No. 9, Ruth gleaning, timed to a voiceover.

usage: python ep09_ruth_gleaning.py <voice audio> <word timestamps json> <out.mp4>
Ruth 2:2-17: "Let me now go to the field, and glean" (2), she gleans after the reapers in Boaz's field (3),
continues from the morning until now (7), Boaz has handfuls let fall on purpose (16), gleans until even,
about an ephah of barley (17).
"""
import json,os,sys
from base import build
from episode import Voice,HERE

v=Voice(*sys.argv[1:3]);out=sys.argv[3];at=v.at
T=dict(
 field=at('let me now go'),glean=at('and glean'),reapers=at('the reapers'),boaz=at('a man named boaz'),
 morning=at('from the morning'),handfuls=at('let some handfuls'),leave=at('leave them for her'),
 evening=at('until evening'),ephah=at('about an ephah'),
)
punch=at('she showed up');c2=at('and she worked it')

SCENE=r'''
const T=__T__,RED='#d9735a';
const N=9,X=i=>150+i*100;
const gl=el('line',{x1:60,y1:700,x2:1020,y2:700,stroke:GOLD,'stroke-width':5,'stroke-linecap':'round',opacity:.6});
const fence=el('path',{d:'M60 700 V640 M60 660 H110 M110 640 V700',fill:'none',stroke:GOLD,'stroke-width':5,opacity:.6});
// stalks of grain: stem and ear
const stalks=[...Array(N)].map((_,i)=>{const g=el('g',{transform:`translate(${X(i)},700)`});
 el('path',{d:'M0 0 V-230',stroke:GOLD,'stroke-width':6,'stroke-linecap':'round'},g);
 const ear=el('g',{transform:'translate(0,-230)'},g);
 [0,1,2,3].forEach(k=>{el('ellipse',{cx:-14,cy:-k*28,rx:16,ry:9,fill:BR,transform:`rotate(-35 -14 ${-k*28})`},ear);el('ellipse',{cx:14,cy:-k*28,rx:16,ry:9,fill:BR,transform:`rotate(35 14 ${-k*28})`},ear)});
 return{g,i}});
const lab=el('text',{x:540,y:790,'text-anchor':'middle','font-size':30,'font-weight':600,'letter-spacing':7,fill:GOLD});
// sickle for the reapers, sun, basket, handfuls dropped on purpose
const sk=el('path',{d:'M0 0 Q90 -30 80 -110 M0 0 L-40 40',fill:'none',stroke:CR,'stroke-width':8,'stroke-linecap':'round'});
const sun=el('circle',{r:48,fill:'none',stroke:BR,'stroke-width':7});
const drops=[0,1,2].map(i=>el('g',{}));
drops.forEach((g,i)=>{el('path',{d:'M0 0 V-60',stroke:BR,'stroke-width':6,'stroke-linecap':'round'},g);el('ellipse',{cx:0,cy:-70,rx:12,ry:22,fill:BR},g)});
const sack=el('g',{transform:'translate(540,560)'});
el('path',{d:'M-110 -90 Q-150 20 -90 120 H90 Q150 20 110 -90 Z',fill:'#0f1f3a',stroke:GOLD,'stroke-width':8,'stroke-linejoin':'round'},sack);
const sfill=el('path',{d:'',fill:BR,opacity:.85},sack);
el('path',{d:'M-110 -90 Q0 -50 110 -90',fill:'none',stroke:GOLD,'stroke-width':6},sack);
const ept=el('text',{x:0,y:20,'text-anchor':'middle','font-size':44,'font-weight':700,fill:'#0f1f3a','font-family':'Lora'},sack);ept.textContent='EPHAH';
function scene(t){
 const edge=eo(pr(t,0.3,0.8));
 gl.setAttribute('opacity',.6*edge);fence.setAttribute('opacity',.6*edge);
 const reap=pr(t,T.reapers,0.5);
 stalks.forEach(({g,i})=>{
  const grow=eo(pr(t,0.3+i*0.07,0.6));
  // the first stalks are taken by the reapers; Ruth gleans the leftovers at the edge
  const cutT=T.reapers+0.2+i*0.12,cut=i>=2&&i<N-1?eio(pr(t,cutT,0.5)):0;
  const gl2=i<2?eio(pr(t,T.glean+0.2*i,0.6)):0;
  g.setAttribute('transform',`translate(${X(i)},700) rotate(${-cut*80+(i<2?-gl2*12:0)})`);
  g.setAttribute('opacity',grow*(1-cut*0.9)*(1-(gl2*0.0)));
  g.children[0].setAttribute('stroke',i<2&&t>T.glean?BR:GOLD);
 });
 // sun arc: morning to evening
 const sp=pr(t,T.morning,T.evening-T.morning+0.6);const sx=130+800*sp,sy=240-Math.sin(sp*Math.PI)*170;
 sun.setAttribute('cx',sx);sun.setAttribute('cy',sy);sun.setAttribute('opacity',eo(pr(t,T.morning,0.4))*(1-eo(pr(t,T.evening+0.7,0.5))));
 sun.setAttribute('stroke',sp>0.75?RED:BR);
 sk.setAttribute('transform',`translate(${560+(1-reap)*400},${520+Math.sin(t*8)*10}) rotate(${-20+Math.sin(t*6)*14})`);sk.setAttribute('opacity',reap*(1-eo(pr(t,T.boaz,0.5))));
 // handfuls fall on purpose
 drops.forEach((g,i)=>{const p=bounce(pr(t,T.handfuls+0.3+i*0.35,0.6));g.setAttribute('transform',`translate(${300+i*150},${700-(1-p)*260}) rotate(${-25+i*25})`);g.setAttribute('opacity',(t>T.handfuls+0.3+i*0.35?1:0)*(1-eo(pr(t,T.evening,0.4))))});
 // the sack fills
 const f=eio(pr(t,T.evening+0.4,T.ephah-T.evening+0.8));sack.setAttribute('opacity',eo(pr(t,T.evening,0.5)));
 const y=120-210*f;sfill.setAttribute('d',`M-100 ${y} H100 L${90-10*(1-f)} 120 H${-90+10*(1-f)} Z`);
 const c=t>=T.ephah?'ABOUT AN EPHAH OF BARLEY':t>=T.evening?'UNTIL EVENING':t>=T.handfuls?'LEFT ON PURPOSE':t>=T.morning?'FROM THE MORNING':t>=T.glean?'GLEANING THE EDGE':t>=T.field?'LET ME GO TO THE FIELD':'';
 $('count').textContent=c;$('count').style.opacity=c?1:0;
}
'''
CAPS=[["Let ",0,0],["me ",0,0],["now ",0,0],["go ",1,0],["to ",0,0],["the ",0,0],["field,",1,1],["and ",0,0],["glean.",1,0]]
capw=v.capw(CAPS)
html=os.path.join(HERE,'ep09_ruth_gleaning.html')
build(html,9,'Show up at the edge,','and work it.','RUTH 2 : 1–17',CAPS,capw[0],punch-0.1,SCENE.replace('__T__',json.dumps(T)),
      capw=capw,cue=dict(c1=punch+0.1,c2=c2,hl=c2+0.25,ref=c2+0.9))
v.finish('ep09',html,out)
