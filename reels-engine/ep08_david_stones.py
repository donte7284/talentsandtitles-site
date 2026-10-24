"""Parable No. 8, David's five stones, timed to a voiceover.

usage: python ep08_david_stones.py <voice audio> <word timestamps json> <out.mp4>
1 Samuel 17:38-50: Saul's armour (helmet of brass, coat of mail), "I cannot go with these; for I have
not proved them" (39), staff, five smooth stones from the brook in the shepherd's bag, sling in hand (40),
a stone slung, the Philistine falls, "there was no sword in the hand of David" (49-50).
"""
import json,os,sys
from base import build
from episode import Voice,HERE

v=Voice(*sys.argv[1:3]);out=sys.argv[3];at=v.at
T=dict(
 armour=at('saul puts'),helmet=at('a helmet'),mail=at('coat of mail'),walk=at('tries to walk'),
 cannot=at('i cannot'),off=at('takes them off'),staff=at('his staff'),five=at('five smooth stones'),
 bag=at("shepherd's bag"),sling=at('his sling'),wins=at('david wins'),nosword=at('no sword'),
)
punch=at('use the tools');c2=at('you have proved')

SCENE=r'''
const T=__T__,RED='#d9735a';
const dr=(p,a)=>el('path',Object.assign({fill:'none',stroke:GOLD,'stroke-width':8,'stroke-linecap':'round','stroke-linejoin':'round',pathLength:1,'stroke-dasharray':1},a||{}),p);
// Saul's armour: helmet and coat of mail
const arm=el('g',{});
const hg=el('g',{transform:'translate(300,250)'},arm);
const h1=dr(hg,{d:'M-90 50 Q-90 -90 0 -90 Q90 -90 90 50 Z'}),h2=dr(hg,{d:'M-100 50 H100 M0 -90 V-130 M-30 -50 H30',opacity:.9});
const mg=el('g',{transform:'translate(300,560)'},arm);
const m1=dr(mg,{d:'M-90 -80 L-40 -100 Q0 -70 40 -100 L90 -80 L140 -20 L88 14 L74 -10 V130 H-74 V-10 L-88 14 L-140 -20 Z'});
const m2=dr(mg,{d:'M-50 -20 H50 M-50 20 H50 M-50 60 H50 M-50 100 H50','stroke-width':3,opacity:.5});
const lab1=el('text',{x:300,y:790,'text-anchor':'middle','font-size':30,'font-weight':600,'letter-spacing':7,fill:GOLD});lab1.textContent="SAUL'S ARMOUR";
// brook, stones, bag, sling
const brook=dr(st,{'stroke-width':5,opacity:.6});
const stones=[0,1,2,3,4].map(i=>el('ellipse',{rx:30,ry:24,fill:BR,stroke:CR,'stroke-width':4}));
const bag=el('g',{transform:'translate(300,470)'});
const bg1=el('path',{d:'M-90 -70 Q-120 60 -60 120 H60 Q120 60 90 -70 Z',fill:'#0f1f3a',stroke:GOLD,'stroke-width':8,'stroke-linejoin':'round'},bag);
el('path',{d:'M-90 -70 Q0 -30 90 -70',fill:'none',stroke:GOLD,'stroke-width':6},bag);
stones.forEach(s=>st.appendChild(s));
const staff=dr(st,{d:'M120 160 L120 780','stroke-width':10});
const sl=dr(st,{d:'M640 560 Q690 640 740 640 Q790 640 840 560 M640 560 L600 470 M840 560 L880 470 M740 640 m-34 0 a34 24 0 1 0 68 0 a34 24 0 1 0 -68 0','stroke-width':7});
// the stone in flight, the target
const shot=el('ellipse',{rx:26,ry:22,fill:BR,stroke:CR,'stroke-width':4});
const tg=el('g',{transform:'translate(880,330)'});
const tp=el('path',{d:'M-70 -120 H70 V30 Q70 130 0 170 Q-70 130 -70 30 Z',fill:'none',stroke:GOLD,'stroke-width':8,'stroke-linejoin':'round'},tg);
const crack=el('path',{d:'M0 -120 L-18 -40 L20 20 L-10 100',fill:'none',stroke:RED,'stroke-width':7,'stroke-linecap':'round',pathLength:1,'stroke-dasharray':1,'stroke-dashoffset':1},tg);
const sw=el('g',{transform:'translate(540,360)'});
const sw1=el('path',{d:'M-170 120 L170 -120 M110 -120 L170 -60 M-150 140 L-190 100',fill:'none',stroke:GOLD,'stroke-width':10,'stroke-linecap':'round'},sw);
const nosw=el('path',{d:'M-230 180 L230 -180',stroke:RED,'stroke-width':12,'stroke-linecap':'round'},sw);
const lab2=el('text',{x:540,y:790,'text-anchor':'middle','font-size':30,'font-weight':600,'letter-spacing':7,fill:GOLD});
function scene(t){
 const a=pr(t,T.armour,0.9);
 h1.setAttribute('stroke-dashoffset',1-eo(pr(t,T.helmet-0.2,0.8)));h2.setAttribute('stroke-dashoffset',1-eo(pr(t,T.helmet,0.8)));
 m1.setAttribute('stroke-dashoffset',1-eo(pr(t,T.mail-0.2,0.9)));m2.setAttribute('stroke-dashoffset',1-eo(pr(t,T.mail+0.2,0.8)));
 const wob=Math.sin(t*14)*5*(t>T.walk&&t<T.cannot+0.6?1:0);
 const red=t>=T.cannot, slide=eio(pr(t,T.off,0.9));
 [h1,h2,m1,m2].forEach(p=>p.setAttribute('stroke',red?RED:GOLD));
 arm.setAttribute('transform',`translate(${-slide*700+wob},0)`);
 lab1.setAttribute('opacity',eo(pr(t,T.helmet,0.4))*(1-eo(pr(t,T.off+0.4,0.4))));
 // brook line + stones
 const bp=eo(pr(t,T.staff,0.8));let d='';for(let x=420;x<=420+520*bp;x+=20)d+=(d?'L':'M')+x+' '+(790+Math.sin(x/50+t*2)*8);
 brook.setAttribute('d',d||'M0 0');brook.setAttribute('opacity',(t>T.staff?.6:0));
 staff.setAttribute('stroke-dashoffset',1-eio(pr(t,T.staff,0.7)));
 stones.forEach((s,i)=>{const ap=eo(pr(t,T.five+i*0.16,0.35)),gp=eio(pr(t,T.bag+0.1*i,0.7));
  const x0=470+i*85,y0=745,x1=300+(i-2)*34,y1=395;
  s.setAttribute('cx',x0+(x1-x0)*gp);s.setAttribute('cy',y0+(y1-y0)*gp-Math.sin(gp*Math.PI)*60);s.setAttribute('opacity',ap)});
 bag.setAttribute('opacity',eo(pr(t,T.bag-0.2,0.5)));
 sl.setAttribute('stroke-dashoffset',1-eio(pr(t,T.sling,0.8)));
 // shot
 const sp=eio(pr(t,T.wins,0.7));
 shot.setAttribute('cx',740+(880-740)*sp);shot.setAttribute('cy',640+(380-640)*sp-Math.sin(sp*Math.PI)*60);shot.setAttribute('opacity',t>=T.wins&&sp<1?1:0);
 const hit=pr(t,T.wins+0.7,0.5);
 tg.setAttribute('opacity',eo(pr(t,T.sling,0.6))*(1-eo(pr(t,T.nosword,0.5))));
 tg.setAttribute('transform',`translate(${880+hit*20},${330+hit*hit*320}) rotate(${hit*60})`);
 crack.setAttribute('stroke-dashoffset',1-hit);tp.setAttribute('stroke',hit>0?RED:GOLD);
 sw.setAttribute('opacity',eo(pr(t,T.nosword,0.5)));nosw.setAttribute('stroke-dasharray','1');nosw.setAttribute('stroke-dasharray',`${400*eio(pr(t,T.nosword+0.4,0.5))} 800`);
 const c=t>=T.nosword?'NO SWORD':t>=T.wins?'ONE STONE':t>=T.five?'FIVE SMOOTH STONES':t>=T.cannot?'NOT PROVED':t>=T.armour?'BORROWED ARMOUR':'';
 $('count').textContent=c;$('count').style.color=(t>=T.cannot&&t<T.staff)||t>=T.nosword?RED:'#c9a24a';$('count').style.opacity=c?1:0;
 lab2.setAttribute('opacity',0);
}
'''
CAPS=[["I ",0,0],["have ",0,0],["not ",1,0],["proved ",1,0],["them.",0,0]]
capw=v.capw(CAPS)
html=os.path.join(HERE,'ep08_david_stones.html')
build(html,8,'Use the tools','you have proved.','1 SAMUEL 17 : 38–50',CAPS,capw[0],punch-0.1,SCENE.replace('__T__',json.dumps(T)),
      capw=capw,cue=dict(c1=punch+0.1,c2=c2,hl=c2+0.25,ref=c2+0.9))
v.finish('ep08',html,out)
