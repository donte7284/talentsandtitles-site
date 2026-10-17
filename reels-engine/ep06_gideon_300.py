"""Parable No. 6, Gideon's three hundred, timed to a voiceover.

usage: python ep06_gideon_300.py <voice audio> <word timestamps json> <out.mp4>
Judges 7:2-8: the army is too many; the fearful leave (22,000), 10,000 remain; at the water
three hundred are set apart (7:5-7) and the rest sent to their tents.
"""
import json,os,sys
from base import build
from episode import Voice,HERE

v=Voice(*sys.argv[1:3]);out=sys.argv[3];at=v.at
T=dict(
 army=at('army'),many=at('too many'),leave=at('twenty-two thousand'),ten=at('ten thousand'),
 still=at('still too many'),water=at('at the water'),three=at('only three hundred'),kept=at('are kept'),
)
punch=at('not everyone');c2=at('is meant to go')

SCENE=r'''
const T=__T__,RED='#d9735a';
const N=40,R=[],K=[9,21,33];
for(let i=0;i<N;i++)if(i%4==1)R.push(i);
const shields=[...Array(N)].map((_,i)=>{const g=el('g',{});
 el('path',{d:'M-36 -42 H36 V10 Q36 42 0 58 Q-36 42 -36 10Z',fill:BR,opacity:.25},g);
 el('path',{d:'M-36 -42 H36 V10 Q36 42 0 58 Q-36 42 -36 10Z',fill:'none',stroke:GOLD,'stroke-width':5,'stroke-linejoin':'round'},g);
 el('path',{d:'M0 -26 V34 M-20 -4 H20',stroke:GOLD,'stroke-width':3,opacity:.5,fill:'none'},g);return g});
const pos=i=>[110+(i%8)*123,150+Math.floor(i/8)*115];
const sea=el('path',{fill:'none',stroke:BR,'stroke-width':6,'stroke-linecap':'round'});
const sea2=el('path',{fill:'none',stroke:GOLD,'stroke-width':4,'stroke-linecap':'round'});
const n300=el('text',{x:540,y:630,'text-anchor':'middle','font-size':120,'font-weight':700,fill:BR,'font-family':'Lora'});n300.textContent='300';
function scene(t){
 shields.forEach((g,i)=>{
  const [x,y]=pos(i);const app=eo(pr(t,T.army+i*0.025,0.4));
  let a=app,dx=0,dy=0,sc=1,tx=x,ty=y;
  const inR=i%4==1,inK=K.includes(i);
  if(!inR){const p=eio(pr(t,T.leave+(i%7)*0.05,1.2));a*=1-p;dx=(x<540?-1:1)*140*p;dy=90*p}
  else if(!inK){const p=eio(pr(t,T.three+(i%5)*0.06,1.2));a*=1-p;dx=(x<540?-1:1)*140*p;dy=90*p}
  else{const p=eio(pr(t,T.three+0.3,1.1));const k=K.indexOf(i);tx=x+(270+k*270-x)*p;ty=y+(380-y)*p;sc=1+0.7*p}
  g.setAttribute('transform',`translate(${tx+dx},${ty+dy}) scale(${sc*(0.8+0.2*app)})`);g.setAttribute('opacity',a);
  const edge=g.children[1];edge.setAttribute('stroke',(!inR&&t>=T.leave)||(inR&&!inK&&t>=T.three)?RED:GOLD);
 });
 const sp=eio(pr(t,T.water,0.8));
 [sea,sea2].forEach((w,k)=>{let d='';for(let x=60;x<=60+960*sp;x+=20)d+=(d?'L':'M')+x+' '+(740+k*34+Math.sin(x/80+t*2+k)*12);w.setAttribute('d',d);w.setAttribute('opacity',k?.5:1)});
 n300.setAttribute('opacity',eo(pr(t,T.kept,0.5)));n300.setAttribute('y',620+ (1-eo(pr(t,T.kept,0.5)))*30);
 const c=t>=T.kept?'THREE HUNDRED KEPT':t>=T.still?'STILL TOO MANY':t>=T.ten?'10,000 REMAIN':t>=T.leave?'22,000 GO HOME':t>=T.many?'TOO MANY':'';
 $('count').textContent=c;$('count').style.color=(t>=T.leave&&t<T.ten)||(t>=T.still&&t<T.kept)||(t>=T.many&&t<T.leave)?RED:'#c9a24a';$('count').style.opacity=c?1:0;
}
'''
CAPS=[["By ",0,0],["the ",0,0],["three ",1,0],["hundred",1,1],["men ",0,0],["that ",0,0],["lapped",0,1],["will ",0,0],["I ",0,0],["save ",1,0],["you.",1,0]]
capw=v.capw(CAPS)
html=os.path.join(HERE,'ep06_gideon_300.html')
build(html,6,'Not everyone you gather','is meant to go.','JUDGES 7 : 2–8',CAPS,capw[0],punch-0.1,SCENE.replace('__T__',json.dumps(T)),
      capw=capw,cue=dict(c1=punch+0.1,c2=c2,hl=c2+0.25,ref=c2+0.9))
v.finish('ep06',html,out)
