"""Parable No. 6, Gideon's three hundred, timed to a voiceover.

usage: python ep06_gideon.py <voice audio> <word timestamps json> <out.mp4>
Judges 7:2-8: 22,000 leave, 10,000 remain, the water test sorts out 300; the rest go home.
Dots stand for the men (objects and symbols only); the afraid, the many, the three hundred are marked by colour.
"""
import json,os,sys
from base import build
from episode import Voice,HERE
from kit import KIT

v=Voice(*sys.argv[1:3]);out=sys.argv[3];at=v.at
T=dict(
 army=at('an army'),many=at('too many'),twenty=at('twenty-two thousand'),afraid=at('afraid'),ten=at('ten thousand'),still=at('still too many'),
 water=at('at the water'),hundred=at('three hundred'),bow=at('bow down'),by=at('by the three hundred'),home=at('go home'),
)
punch=at('a bigger team');right=at('the right team')

SCENE=KIT+r'''
const T=__T__;
const COLS=16,ROWS=10,N=COLS*ROWS;
const hash=i=>((i*2654435761)>>>0)%1000/1000;
const dots=Array.from({length:N},(_,i)=>{const c=i%COLS,r=Math.floor(i/COLS);
 const gx=100+c*58,gy=110+r*52;
 // which men stay: about a third; of those, three are the chosen
 const stay=hash(i)<0.33;const chosen=stay&&(i%7==3)&&hash(i+9)<0.45;
 const e=el('circle',{r:15,fill:BR,'fill-opacity':.3,stroke:GOLD,'stroke-width':4});return{e,gx,gy,stay,chosen,i}});
// force exactly three chosen among the stayers
let stayers=dots.filter(d=>d.stay);dots.forEach(d=>d.chosen=false);[1,Math.floor(stayers.length/2),stayers.length-2].forEach(k=>stayers[k].chosen=true);
stayers.forEach((d,k)=>{d.cx=360+(k%9)*50;d.cy=420+Math.floor(k/9)*50});
const wave=el('path',{fill:'none',stroke:BR,'stroke-width':5,'stroke-linecap':'round',opacity:0});
const wave2=el('path',{fill:'none',stroke:GOLD,'stroke-width':4,'stroke-linecap':'round',opacity:0});
function scene(t){
 const toWater=eio(pr(t,T.water,0.9)),leave=eio(pr(t,T.twenty,1.8)),gone=eo(pr(t,T.home,0.8));
 dots.forEach(d=>{let x=d.gx,y=d.gy,o=eo(pr(t,0.3+(d.i%COLS)*0.03+Math.floor(d.i/COLS)*0.02,0.4)),fill=BR,stroke=GOLD,sc=1;
  if(!d.stay){ // the afraid walk off and turn red
   const dirx=d.gx<540?-1:1;x+=dirx*leave*700;o*=1-leave;if(leave>0.05){stroke=RED;fill=RED}}
  else{x=d.gx+(d.cx-d.gx)*toWater;y=d.gy+(d.cy-d.gy)*toWater;
   if(!d.chosen){const bow=eio(pr(t,T.bow,0.5));sc=1-0.45*bow;y+=bow*12;o*=1-gone;if(bow>0.1)stroke=RED;if(bow>0.1)fill=RED}
   else{const hl=eo(pr(t,T.hundred,0.5));stroke=BR;sc=1+0.5*hl;y-=hl*10;}}
  d.e.setAttribute('cx',x);d.e.setAttribute('cy',y);d.e.setAttribute('r',15*sc);d.e.setAttribute('opacity',o);d.e.setAttribute('stroke',stroke);d.e.setAttribute('fill',fill);
  d.e.setAttribute('fill-opacity',d.chosen&&t>T.hundred?0.9:0.3);
  if(d.stay&&!d.chosen&&t>T.still&&t<T.water){d.e.setAttribute('stroke-width',4+2*Math.sin(t*8))}else d.e.setAttribute('stroke-width',4)});
 const w=eo(pr(t,T.water,0.6));
 [wave,wave2].forEach((e,k)=>{let d='';for(let x=40;x<=1040;x+=20){d+=(x==40?'M':'L')+x+' '+(690+k*34+Math.sin(x/70+t*2+k)*10)}e.setAttribute('d',d);op(e,w*[1,.6][k])});
 const c=$('count');let s='',col=GOLD,a=0;
 if(t>=T.many&&t<T.twenty-0.1){s='TOO MANY';col=RED;a=eo(pr(t,T.many,0.4))}
 else if(t>=T.twenty&&t<T.ten){s='22,000 AFRAID · GO HOME';col=RED;a=eo(pr(t,T.twenty,0.4))}
 else if(t>=T.ten&&t<T.water){s='10,000 REMAIN · STILL TOO MANY';col=GOLD;a=eo(pr(t,T.ten,0.4))}
 else if(t>=T.water&&t<T.by){s='AT THE WATER';col=GOLD;a=eo(pr(t,T.water,0.4))}
 else if(t>=T.by){s='300';col=BR;a=eo(pr(t,T.by,0.4));}
 c.textContent=s;c.style.color=col;c.style.opacity=a;
}
'''
CAPS=[["Three ",0,0],["hundred ",1,0],["men.",0,0]]
capw=v.capw(CAPS)
html=os.path.join(HERE,'ep06_gideon.html')
build(html,6,'A bigger team was never the plan.','The right team.','JUDGES 7 : 2–8',CAPS,capw[0],punch-0.1,SCENE.replace('__T__',json.dumps(T)),
      capw=capw,cue=dict(c1=punch,c2=right,hl=right+0.25,ref=right+0.9))
v.finish('ep06',html,out)
