"""Parable No. 5, the wise and foolish builders, timed to a voiceover.

usage: python ep05_builders.py <voice audio> <word timestamps json> <out.mp4>
Matthew 7:24-27: one house on a rock, one on sand; rain, floods and wind beat on both; one falls.
"""
import json,os,sys
from base import build
from episode import Voice,HERE
from kit import KIT

v=Voice(*sys.argv[1:3]);out=sys.argv[3];at=v.at
T=dict(
 two=at('two men'),rock=at('on a rock'),sand=at('on sand'),rain=at('the rain descends'),floods=at('the floods come'),
 winds=at('the winds blow'),rockfall=at('does not fall'),sandfalls=at('sand falls'),great=at('great is the fall'),
 same=at('same storm'),weather=at('same weather'),
)
punch=at('the difference');found=at('the foundation')

SCENE=KIT+r'''
const T=__T__;
const GY=640;
// rock (left) and sand (right)
const rockP=line(`M70 ${GY} L110 ${GY-40} L220 ${GY-55} L330 ${GY-45} L400 ${GY-5} L430 ${GY} Z`,GOLD,7);
const rockF=el('path',{d:`M70 ${GY} L110 ${GY-40} L220 ${GY-55} L330 ${GY-45} L400 ${GY-5} L430 ${GY} Z`,fill:BR,opacity:0});
const sandL=line(`M650 ${GY} Q720 ${GY-14} 790 ${GY} T930 ${GY} T1010 ${GY}`,GOLD,6);
const dots=Array.from({length:16},(_,i)=>el('circle',{cx:660+i*22,cy:GY+22+(i%3)*18,r:3.5,fill:GOLD,opacity:0}));
function house(cx,base){const g=el('g',{transform:`translate(${cx},${base})`});
 const w=el('path',{d:'M-110 0 V-190 H110 V0',fill:NAVY,stroke:GOLD,'stroke-width':7,'stroke-linejoin':'round','stroke-linecap':'round',pathLength:1,'stroke-dasharray':1},g);
 const r=el('path',{d:'M-135 -190 L0 -300 L135 -190 Z',fill:NAVY,stroke:GOLD,'stroke-width':7,'stroke-linejoin':'round',pathLength:1,'stroke-dasharray':1},g);
 const d=el('rect',{x:-26,y:-100,width:52,height:100,fill:'none',stroke:GOLD,'stroke-width':5},g);
 return{g,w,r,d}}
const H1=house(250,GY-48),H2=house(830,GY);
const l1=txt(250,GY+90,'ROCK',34,GOLD,10),l2=txt(830,GY+120,'SAND',34,GOLD,10);
// storm
const rain=Array.from({length:46},(_,i)=>el('path',{d:'M0 0 l-14 38',stroke:'#f4ecd8','stroke-width':3,'stroke-linecap':'round',opacity:0}));
const flood=el('path',{fill:'none',stroke:BR,'stroke-width':5,'stroke-linecap':'round',opacity:0});
const wind=[0,1,2].map(i=>line(`M${40} ${150+i*60} H${200+i*40} q40 0 40 -26`,GOLD,5,{opacity:0}));
const same=txt(540,870,'THE SAME STORM',34,RED,9);
const crash=el('g',{opacity:0});[[-70,-30,0],[10,-60,20],[80,-20,-15],[-30,-90,35]].forEach(([x,y,r])=>el('rect',{x:x-26,y:y-18,width:52,height:36,fill:'none',stroke:RED,'stroke-width':4,transform:`rotate(${r} ${x} ${y})`},crash));
function scene(t){
 dash(rockP,eio(pr(t,T.rock-0.2,0.8)));op(rockF,0.25*eo(pr(t,T.rock+0.4,0.5)));dash(sandL,eio(pr(t,T.sand-0.2,0.8)));
 dots.forEach((d,i)=>op(d,eo(pr(t,T.sand+0.2+i*0.03,0.3))*0.7));
 [H1,H2].forEach((H,k)=>{const s=T.two+k*0.4;dash(H.w,eio(pr(t,s,0.9)));dash(H.r,eio(pr(t,s+0.6,0.7)));op(H.d,eo(pr(t,s+0.9,0.4)))});
 op(l1,eo(pr(t,T.rock+0.5,0.4)));op(l2,eo(pr(t,T.sand+0.5,0.4)));
 const storm=eo(pr(t,T.rain,0.6));
 rain.forEach((r,i)=>{const sp=1.1+(i%5)*0.12;const ph=((t*sp+i*0.173)%1);r.setAttribute('transform',`translate(${(i*97)%1160-40+ph*-60},${ph*760-20})`);op(r,storm*0.7)});
 const fl=eo(pr(t,T.floods,0.6));let d='';for(let x=40;x<=1040;x+=20){d+=(x==40?'M':'L')+x+' '+(GY-6+Math.sin(x/50+t*3)*8)}flood.setAttribute('d',d);op(flood,fl*0.9);
 wind.forEach((w,i)=>{dash(w,eio(pr(t,T.winds+i*0.15,0.5)));op(w,t>T.winds?0.8*(1-0.5*eo(pr(t,T.rockfall,0.5))):0);w.setAttribute('transform',`translate(${Math.sin(t*5+i)*14},0)`)});
 // both houses shake in the storm; the rock house holds, the sand house falls
 const shake=(t>T.rain&&t<T.rockfall+0.5)?Math.sin(t*38)*3*storm:0;
 H1.g.setAttribute('transform',`translate(${250+shake},${GY-48})`);
 const f=eio(pr(t,T.sandfalls,0.9));
 H2.g.setAttribute('transform',`translate(${830+(t<T.sandfalls?shake:0)+f*60},${GY+f*40}) rotate(${f*38} 100 0)`);
 op(H2.g,1-0.7*eo(pr(t,T.great+0.3,0.6)));
 crash.setAttribute('transform',`translate(840,${GY-60})`);op(crash,eo(pr(t,T.great,0.5))*0.9);
 op(same,eo(pr(t,T.same,0.4)));
 $('count').textContent='';
}
'''
CAPS=[["On ",0,0],["a ",0,0],["rock. ",0,1],["On ",0,0],["sand.",1,0]]
capw=v.capw(CAPS)
html=os.path.join(HERE,'ep05_builders.html')
build(html,5,'The difference was','the foundation.','MATTHEW 7 : 24–27',CAPS,capw[0],punch-0.1,SCENE.replace('__T__',json.dumps(T)),
      capw=capw,cue=dict(c1=punch,c2=found,hl=found+0.25,ref=found+0.9))
v.finish('ep05',html,out)
