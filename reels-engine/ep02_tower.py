"""Parable No. 2, the unfinished tower, timed to a voiceover.

usage: python ep02_tower.py <voice audio> <word timestamps json> <out.mp4>
The approved tower drawing from scenes.py, with each beat cued to a spoken word.
"""
import json,os,sys
from base import build
from episode import Voice,HERE

v=Voice(*sys.argv[1:3]);out=sys.argv[3];at=v.at
T=dict(
 starts=at('starts building'),building=at('building'),tower=at('a tower'),
 lays=at('lays the foundation'),runs=at('runs out'),outend=at('runs out',end=True),sees=at('sees it'),
 nothing=at('nothing on it'),foundation2=at('a foundation with'),laugh=at('laugh'),
 count=at('count the cost'),
)
# four foundation blocks land between "lays" and just after "runs out"; funds drain as they land
T['bd']=0.6;T['bs']=max(0.25,(T['runs']+0.25-T['lays']-T['bd'])/3)
punch=at('starting is cheap');everybody=at('everybody starts');count2=at('the count is')

SCENE=r'''
const T=__T__;
const GY=800;
el('line',{x1:80,y1:GY,x2:1000,y2:GY,stroke:GOLD,'stroke-width':6,'stroke-linecap':'round',pathLength:1,'stroke-dasharray':1,id:'ground'});
// ghost plan
const ghost=el('g',{id:'ghost'});
const GP="M340 710 V200 H400 V150 H470 V200 H505 V150 H575 V200 H610 V150 H680 V200 H740 V710";
el('path',{d:GP,fill:'none',stroke:CR,'stroke-width':5,'stroke-dasharray':'18 16','stroke-linejoin':'round'},ghost);
const gmask=el('clipPath',{id:'gm'});const gmr=el('rect',{x:300,y:710,width:480,height:0},gmask);ghost.setAttribute('clip-path','url(#gm)');
[590,470,350].forEach(y=>el('line',{x1:340,y1:y,x2:740,y2:y,stroke:CR,'stroke-width':3,'stroke-dasharray':'10 14',opacity:.6},ghost));
const plan=el('text',{x:540,y:110,'text-anchor':'middle','font-size':30,'font-weight':600,'letter-spacing':7,fill:CR});plan.textContent='THE PLAN';
// counting the cost: the five planned levels get numbered on "count the cost"
const nums=[650,530,410,275,175].map((y,i)=>{const n=el('text',{x:790,y:y+12,'text-anchor':'middle','font-size':36,'font-weight':600,fill:BR});n.textContent=String(i+1);return n});
// funds bar
const fb=el('g',{});
const ft=el('text',{x:90,y:40,'font-size':30,'font-weight':600,'letter-spacing':7,fill:GOLD},fb);ft.textContent='FUNDS';
el('rect',{x:240,y:14,width:750,height:30,rx:15,fill:'none',stroke:GOLD,'stroke-width':4},fb);
const fbar=el('rect',{x:246,y:20,width:738,height:18,rx:9,fill:BR},fb);
// foundation blocks
const blocks=[0,1,2,3].map(i=>{const g=el('g',{});el('rect',{x:-96,y:-86,width:192,height:86,rx:8,fill:BR},g);el('rect',{x:-96,y:-86,width:192,height:86,rx:8,fill:'none',stroke:GOLD,'stroke-width':5},g);el('line',{x1:-60,y1:-43,x2:60,y2:-43,stroke:'#0f1f3a','stroke-width':4,opacity:.25},g);return g});
const b5=el('g',{});el('rect',{x:-96,y:-86,width:192,height:86,rx:8,fill:'none',stroke:BR,'stroke-width':5},b5);
function scene(t){
 $('ground').setAttribute('stroke-dashoffset',1-eo(pr(t,T.starts,0.8)));
 const gh=eio(pr(t,T.tower,1.2))*600;gmr.setAttribute('y',710-gh);gmr.setAttribute('height',gh+20);
 const dim=1-0.55*eo(pr(t,T.nothing,0.8));
 const pulse=t>T.laugh?0.75+0.25*Math.sin((t-T.laugh)*4):1;
 ghost.setAttribute('opacity',dim*pulse);
 plan.setAttribute('opacity',eo(pr(t,T.tower+0.5,0.5))*dim);
 fb.setAttribute('opacity',eo(pr(t,T.building,0.5)));
 let spent=0;
 blocks.forEach((g,i)=>{const s=T.lays+i*T.bs;const p=pr(t,s,T.bd);const y=-140+(GY+140-3)*bounce(p);
  g.setAttribute('transform',`translate(${240+i*200},${y})`);g.setAttribute('opacity',p>0?1:0);spent+=eio(pr(t,s+T.bd*0.33,T.bd*0.67));});
 const left=1-spent/4;fbar.setAttribute('width',Math.max(0,738*left));
 fbar.setAttribute('fill',left<0.3?'#d9735a':BR);
 ft.setAttribute('fill',t>=T.outend?'#d9735a':GOLD);
 // fifth block hovers after the money runs out, shakes, falls away on "sees it"
 const s5=T.outend+0.1;const a=pr(t,s5,0.5),hold=pr(t,s5+0.5,Math.max(0.3,T.sees-s5-0.5)),drop=pr(t,T.sees,0.7);
 const shake=hold>0&&drop<=0?Math.sin(t*40)*6*hold:0;
 b5.setAttribute('transform',`translate(${440+shake},${420+(1-eo(a))*-120+eio(drop)*40}) rotate(${drop*14})`);
 b5.setAttribute('opacity',eo(a)*(1-eo(drop)));
 nums.forEach((n,i)=>n.setAttribute('opacity',eo(pr(t,T.count+i*0.15,0.3))));
 $('count').textContent=t>T.foundation2?'1 LEVEL BUILT · 5 PLANNED · FUNDS 0':'';$('count').style.opacity=eo(pr(t,T.foundation2,0.5));
}
'''
CAPS=[["He ",0,0],["started, ",0,0],["and",0,1],["couldn't ",1,0],["finish.",1,0]]
capw=v.capw(CAPS)
html=os.path.join(HERE,'ep02_tower.html')
build(html,2,'Everybody starts.','Count the cost.','LUKE 14 : 28–30',CAPS,capw[0],punch-0.1,SCENE.replace('__T__',json.dumps(T)),
      capw=capw,cue=dict(c1=everybody,c2=count2,hl=count2+0.25,ref=count2+0.9))
v.finish('ep02',html,out)
