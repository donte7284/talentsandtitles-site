"""Parable No. 5, the wise and foolish builders, timed to a voiceover.

usage: python ep05_wise_builders.py <voice audio> <word timestamps json> <out.mp4>
Matthew 7:24-27: one house on rock, one on sand; rain, floods and winds beat on both;
the rock house does not fall, the sand house falls.
"""
import json,os,sys
from base import build
from episode import Voice,HERE

v=Voice(*sys.argv[1:3]);out=sys.argv[3];at=v.at
T=dict(
 two=at('each build'),rock=at('builds on rock'),sand=at('builds on sand'),rain=at('the rain'),
 floods=at('floods come'),winds=at('the winds'),holds=at('does not fall'),falls=at('sand falls'),
)
punch=at('same storm');c2=at('different ground')

SCENE=r'''
const T=__T__,RED='#d9735a';
const rockG=el('g',{});
el('path',{d:'M60 720 L110 650 L200 625 L330 635 L430 658 L500 720Z',fill:BR,opacity:.9,stroke:GOLD,'stroke-width':6,'stroke-linejoin':'round'},rockG);
el('path',{d:'M200 625 L230 690 M330 635 L310 700',stroke:'#0f1f3a','stroke-width':4,opacity:.3,fill:'none'},rockG);
const sandG=el('g',{});
el('path',{d:'M570 720 Q680 696 790 708 T1020 720Z',fill:'none',stroke:GOLD,'stroke-width':6,'stroke-dasharray':'4 14','stroke-linecap':'round'},sandG);
const lab1=el('text',{x:280,y:790,'text-anchor':'middle','font-size':30,'font-weight':600,'letter-spacing':7,fill:GOLD});lab1.textContent='ROCK';
const lab2=el('text',{x:800,y:790,'text-anchor':'middle','font-size':30,'font-weight':600,'letter-spacing':7,fill:GOLD});lab2.textContent='SAND';
// water goes behind the houses
const sea=el('path',{fill:'#0f1f3a',stroke:'none'});
const wave=el('path',{fill:'none',stroke:BR,'stroke-width':5,'stroke-linecap':'round'});
function house(cx,by){
 const g=el('g',{});const p=el('path',{d:'M-110 0 V-170 L0 -270 L110 -170 V0 Z',fill:'none',stroke:GOLD,'stroke-width':8,'stroke-linejoin':'round',pathLength:1,'stroke-dasharray':1},g);
 const f=el('path',{d:'M-110 0 V-170 L0 -270 L110 -170 V0 Z',fill:BR,opacity:0},g);
 el('rect',{x:-26,y:-90,width:52,height:90,fill:'#0f1f3a',stroke:GOLD,'stroke-width':5},g);
 return{g,p,f,by,cx}}
const hr=house(280,650),hs=house(800,706);
const rain=[...Array(36)].map((_,i)=>el('line',{x1:0,y1:0,x2:-14,y2:44,stroke:CR,'stroke-width':3,'stroke-linecap':'round'}));
const wind=[0,1,2].map(i=>el('path',{d:'M0 0 q50 -26 100 0 t100 0 t100 0',fill:'none',stroke:CR,'stroke-width':4,'stroke-linecap':'round'}));
function scene(t){
 rockG.setAttribute('opacity',eo(pr(t,T.two,0.7)));sandG.setAttribute('opacity',eo(pr(t,T.two,0.7)));
 lab1.setAttribute('opacity',eo(pr(t,T.rock,0.4)));lab2.setAttribute('opacity',eo(pr(t,T.sand,0.4)));
 // build each house on its ground
 const br=eio(pr(t,T.rock,1.0)),bs=eio(pr(t,T.sand,1.0));
 hr.p.setAttribute('stroke-dashoffset',1-br);hr.f.setAttribute('opacity',cl(br*2-1)*0.9);
 hs.p.setAttribute('stroke-dashoffset',1-bs);hs.f.setAttribute('opacity',cl(bs*2-1)*0.9);
 const storm=pr(t,T.rain,0.5);
 const shk=storm>0?Math.sin(t*37)*2.5*storm:0;
 hr.g.setAttribute('transform',`translate(${hr.cx+(t<T.falls+1?shk:0)},${hr.by})`);
 // the sand house shakes, then falls
 const fp=pr(t,T.falls,1.0),fl=bounce(fp);
 const sx=t<T.falls?shk*1.6:0;
 hs.g.setAttribute('transform',`translate(${hs.cx+sx+fp*70},${hs.by+fl*120}) rotate(${fp*28})`);
 hs.g.setAttribute('opacity',1-0.55*eo(fp));
 rain.forEach((r,i)=>{const x=(i*61+(t*120))%1140-30,y=((t*1000+i*173)%960)-40;r.setAttribute('x1',x);r.setAttribute('y1',y);r.setAttribute('x2',x-14);r.setAttribute('y2',y+44);r.setAttribute('opacity',0.55*eo(storm))});
 const fw=eo(pr(t,T.floods,1.6));const wy=900-205*fw;
 let d='M-20 920';for(let x=-20;x<=1100;x+=20)d+=` L${x} ${wy+Math.sin(x/70+t*3)*10}`;sea.setAttribute('d',d+' L1100 920Z');
 let e='';for(let x=-20;x<=1100;x+=20)e+=(x==-20?'M':'L')+x+' '+(wy+Math.sin(x/70+t*3)*10);wave.setAttribute('d',e);
 sea.setAttribute('opacity',fw>0?1:0);wave.setAttribute('opacity',fw);
 wind.forEach((w,i)=>{const a=eo(pr(t,T.winds,0.4));const x=((t-T.winds)*520+i*380)%1500-300;w.setAttribute('transform',`translate(${x},${250+i*95})`);w.setAttribute('opacity',a*0.6)});
 const c=t>=T.falls?'SAND · FALLS':t>=T.holds?'ROCK · STANDS':t>=T.rain?'THE STORM HITS BOTH':'';
 $('count').textContent=c;$('count').style.color=t>=T.falls?RED:'#c9a24a';$('count').style.opacity=c?1:0;
}
'''
CAPS=[["The ",0,0],["house ",0,0],["on ",0,0],["the ",0,0],["rock",1,1],["does ",0,0],["not ",1,0],["fall.",1,0]]
capw=v.capw(CAPS)
html=os.path.join(HERE,'ep05_wise_builders.html')
build(html,5,'Same storm.','Different ground.','MATTHEW 7 : 24–27',CAPS,capw[0],punch-0.1,SCENE.replace('__T__',json.dumps(T)),
      capw=capw,cue=dict(c1=punch+0.15,c2=c2,hl=c2+0.25,ref=c2+0.9))
v.finish('ep05',html,out)
