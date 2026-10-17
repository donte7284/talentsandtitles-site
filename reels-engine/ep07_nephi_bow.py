"""Parable No. 7, Nephi's broken bow, timed to a voiceover.

usage: python ep07_nephi_bow.py <voice audio> <word timestamps json> <out.mp4>
1 Nephi 16:18-32: the steel bow breaks (18), no food, brothers' bows lost their springs (21),
a bow of wood and an arrow from a straight stick (23), "Whither shall I go to obtain food?",
the ball's directions to the top of the mountain (26-30), food brought home (31-32).
"""
import json,os,sys
from base import build
from episode import Voice,HERE

v=Voice(*sys.argv[1:3]);out=sys.argv[3];at=v.at
T=dict(
 breaks=at('breaks'),steel=at('fine steel'),nofood=at('no food'),brothers=at('their own bows'),
 spring=at('lost their spring'),makes=at('nephi makes'),newbow=at('new bow'),stick=at('straight stick'),
 asks=at('asks his father'),where=at('where should'),lord=at('the lord answers'),climbs=at('climbs'),
 brings=at('brings home'),
)
punch=at('he made it');c2=at('then he asked')

SCENE=r'''
const T=__T__,RED='#d9735a';
const UP='M0 -200 Q85 -100 85 0',LO='M85 0 Q85 100 0 200';
// steel bow, two halves and a string
const bow=el('g',{});
const up=el('path',{d:UP,fill:'none',stroke:GOLD,'stroke-width':10,'stroke-linecap':'round',pathLength:1,'stroke-dasharray':1},bow);
const lo=el('path',{d:LO,fill:'none',stroke:GOLD,'stroke-width':10,'stroke-linecap':'round',pathLength:1,'stroke-dasharray':1},bow);
const s1=el('line',{x1:0,y1:-200,x2:0,y2:0,stroke:CR,'stroke-width':3},bow),s2=el('line',{x1:0,y1:0,x2:0,y2:200,stroke:CR,'stroke-width':3},bow);
const steel=el('text',{x:400,y:870,'text-anchor':'middle','font-size':30,'font-weight':600,'letter-spacing':7,fill:GOLD});steel.textContent='FINE STEEL';
// brothers' bows
const bro=[0,1,2].map(i=>{const g=el('g',{transform:`translate(${700+i*140},330)`});
 const p=el('path',{fill:'none',stroke:GOLD,'stroke-width':7,'stroke-linecap':'round'},g);el('line',{x1:-62,y1:0,x2:62,y2:0,stroke:CR,'stroke-width':2.5,opacity:.8},g);return{g,p}});
const nos=el('text',{x:840,y:430,'text-anchor':'middle','font-size':28,'font-weight':600,'letter-spacing':7,fill:RED});nos.textContent='NO SPRING';
// wood bow and stick arrow
const wb=el('g',{transform:'translate(480,430)'});
el('path',{d:'M0 -190 Q160 0 0 190',fill:'none',stroke:BR,'stroke-width':12,'stroke-linecap':'round',pathLength:1,'stroke-dasharray':1,id:'wbp'},wb);
const wstr=el('line',{x1:0,y1:-190,x2:0,y2:190,stroke:CR,'stroke-width':3,pathLength:1,'stroke-dasharray':1},wb);
const arrow=el('path',{d:'M-90 0 H300 M270 -22 L304 0 L270 22',fill:'none',stroke:CR,'stroke-width':8,'stroke-linecap':'round','stroke-linejoin':'round',pathLength:1,'stroke-dasharray':1,transform:'translate(480,430)'});
// the question, then the ball with its pointers
const q=el('text',{x:540,y:300,'text-anchor':'middle','font-size':260,'font-weight':700,fill:BR,'font-family':'Lora'});q.textContent='?';
const ball=el('g',{transform:'translate(240,300)'});
el('circle',{r:100,fill:'#0f1f3a',stroke:GOLD,'stroke-width':8},ball);el('circle',{r:80,fill:'none',stroke:GOLD,'stroke-width':3,opacity:.5},ball);
const n1=el('path',{d:'M0 0 L0 -78',stroke:BR,'stroke-width':9,'stroke-linecap':'round'},ball);
const n2=el('path',{d:'M0 0 L0 -52',stroke:CR,'stroke-width':6,'stroke-linecap':'round'},ball);
const dot=el('circle',{r:9,fill:GOLD},ball);
// mountain and climber, food
const mt=el('path',{d:'M430 790 L740 430 L1040 790',fill:'none',stroke:GOLD,'stroke-width':8,'stroke-linejoin':'round',pathLength:1,'stroke-dasharray':1});
const gr=el('line',{x1:60,y1:790,x2:1040,y2:790,stroke:GOLD,'stroke-width':5,'stroke-linecap':'round',opacity:.5});
const me=el('circle',{r:16,fill:BR,stroke:CR,'stroke-width':4});
const food=el('g',{});el('ellipse',{cx:0,cy:0,rx:56,ry:34,fill:BR,stroke:GOLD,'stroke-width':5},food);
el('line',{x1:40,y1:0,x2:96,y2:0,stroke:CR,'stroke-width':8,'stroke-linecap':'round'},food);el('circle',{cx:100,cy:-6,r:10,fill:CR},food);el('circle',{cx:100,cy:8,r:10,fill:CR},food);
function scene(t){
 const inB=eo(pr(t,0.2,0.8));
 const brk=pr(t,T.breaks,0.9),gone=1-eo(pr(t,T.makes,0.6));
 up.setAttribute('stroke-dashoffset',1-inB);lo.setAttribute('stroke-dashoffset',1-inB);
 bow.setAttribute('transform',`translate(400,430)`);
 up.setAttribute('transform',`translate(${-brk*60},${-brk*40}) rotate(${-brk*34} 85 0)`);
 lo.setAttribute('transform',`translate(${-brk*40},${bounce(pr(t,T.breaks,0.9))*150*(brk>0?1:0)}) rotate(${brk*40} 85 0)`);
 up.setAttribute('stroke',t>=T.breaks?RED:GOLD);lo.setAttribute('stroke',t>=T.breaks?RED:GOLD);
 const sn=1-eo(pr(t,T.breaks,0.15));s1.setAttribute('opacity',sn*inB);s2.setAttribute('opacity',sn*inB);
 bow.setAttribute('opacity',gone);
 steel.setAttribute('opacity',eo(pr(t,T.steel,0.4))*gone);
 bro.forEach((b,i)=>{const sag=eo(pr(t,T.spring+i*0.2,0.5));const h=46*(1-sag)+4;
  b.p.setAttribute('d',`M-62 0 Q0 ${-h*2} 62 0`);b.p.setAttribute('stroke',sag>0.5?RED:GOLD);
  b.g.setAttribute('opacity',eo(pr(t,T.brothers+i*0.15,0.4))*gone)});
 nos.setAttribute('opacity',eo(pr(t,T.spring+0.3,0.4))*gone);
 // wood bow + arrow
 const wp=eio(pr(t,T.newbow-0.3,0.8)),ap=eio(pr(t,T.stick-0.2,0.7)),wfade=1-eo(pr(t,T.asks,0.6));
 $('wbp').setAttribute('stroke-dashoffset',1-wp);wstr.setAttribute('stroke-dashoffset',1-cl(wp*2-1));
 arrow.setAttribute('stroke-dashoffset',1-ap);wb.setAttribute('opacity',wfade);arrow.setAttribute('opacity',wfade);
 // the question, then the ball answers
 const qa=bounce(pr(t,T.where-0.2,0.6));q.setAttribute('opacity',(t>T.where-0.2?1:0)*(1-eo(pr(t,T.lord,0.4))));q.setAttribute('transform',`translate(0,${(1-qa)*-120})`);
 const ba=eo(pr(t,T.lord,0.5));ball.setAttribute('opacity',ba);
 const settle=1-eo(pr(t,T.lord,1.4)),ang=11+settle*(520+Math.sin(t*9)*10);
 n1.setAttribute('transform',`rotate(${ang+90})`);n2.setAttribute('transform',`rotate(${ang+90+180-settle*60})`);
 // mountain, climb, food home
 mt.setAttribute('stroke-dashoffset',1-eio(pr(t,T.lord+0.8,1.0)));
 const cp=eio(pr(t,T.climbs,Math.max(1,T.brings-T.climbs-0.2)));
 me.setAttribute('cx',430+310*cp);me.setAttribute('cy',790-360*cp);me.setAttribute('opacity',t>T.climbs?1:0);
 const fa=bounce(pr(t,T.brings,0.7));food.setAttribute('transform',`translate(${160+0*fa},${160+(780-160)*fa-40})`);food.setAttribute('opacity',t>T.brings?1:0);
 gr.setAttribute('opacity',t>T.lord?.5:0);
 const c=t>=T.brings?'FOOD FOR THE FAMILY':t>=T.lord?'THE LORD ANSWERS':t>=T.where?'WHERE SHOULD I GO?':t>=T.newbow?'WOOD BOW · STICK ARROW':t>=T.nofood?'NO BOW · NO FOOD':'';
 $('count').textContent=c;$('count').style.color=t>=T.newbow?'#c9a24a':RED;$('count').style.opacity=c?1:0;
}
'''
CAPS=[["Nephi ",0,0],["makes ",0,0],["a ",0,0],["new ",1,0],["bow",1,1],["out ",0,0],["of ",0,0],["wood.",1,0]]
capw=v.capw(CAPS)
html=os.path.join(HERE,'ep07_nephi_bow.html')
build(html,7,'He made it from what he had.','Then he asked.','1 NEPHI 16 : 18–32',CAPS,capw[0],punch-0.1,SCENE.replace('__T__',json.dumps(T)),
      capw=capw,cue=dict(c1=punch+0.1,c2=c2,hl=c2+0.25,ref=c2+0.9))
v.finish('ep07',html,out)
