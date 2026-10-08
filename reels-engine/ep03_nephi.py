"""Parable No. 3, Nephi's ship, timed to a voiceover.

usage: python ep03_nephi.py <voice audio> <word timestamps json> <out.mp4>
The approved ship drawing from scenes.py, with each beat cued to a spoken word.
Order follows 1 Nephi 17: the ore question (v9), tools made (v16), "Our brother is a fool" (v17).
"""
import json,os,sys
from base import build
from episode import Voice,HERE

v=Voice(*sys.argv[1:3]);out=sys.argv[3];at=v.at
T=dict(
 ship=at('a ship'),no1=at('no shipyard'),no2=at('no crew'),no3=at('no tools'),
 listen=at('listen'),how=at('ask how'),why=at('why me'),asks=at('he asks'),
 ore=at('find ore'),make=at('make the tools'),tools=at('the tools',1,end=True),
 brothers=at('his brothers'),making=at('making the tools'),toolsdone=at('making the tools',end=True),
 started=at('he started'),
)
youdont=at("you don't need");youneed=at('you need the ore')
T['build']=T['started']-0.3;T['bdur']=max(1.4,youdont-0.35-T['build'])

SCENE=r'''
const T=__T__;
const chips=['NO SHIPYARD','NO CREW','NO TOOLS'].map((s,i)=>{const g=el('g',{transform:`translate(${190+i*350},60)`});const tx=el('text',{x:0,y:10,'text-anchor':'middle','font-size':32,'font-weight':600,'letter-spacing':5,fill:CR},g);tx.textContent=s;return g});
// the questions he doesn't ask: shown, then struck through
const notq=['HOW?','WHY ME?'].map((s,i)=>{const x=[365,715][i];const g=el('g',{transform:`translate(${x},60)`});const tx=el('text',{x:0,y:10,'text-anchor':'middle','font-size':32,'font-weight':600,'letter-spacing':5,fill:CR},g);tx.textContent=s;
 const w=[110,180][i];const ln=el('line',{x1:-w/2-10,y1:-1,x2:w/2+10,y2:-1,stroke:'#d9735a','stroke-width':5,'stroke-linecap':'round',pathLength:1,'stroke-dasharray':1},g);return{g,ln}});
// ship group
const ship=el('g',{});
const HULL="M-300 0 Q-262 112 -150 122 H170 Q272 112 322 -12 Z";
const SAIL1="M14 -318 Q190 -210 160 -52 H14Z",SAIL2="M-14 -286 Q-124 -190 -132 -52 H-14Z";
const ghost=el('g',{},ship);
[HULL,SAIL1,SAIL2].forEach(d=>el('path',{d,fill:'none',stroke:CR,'stroke-width':5,'stroke-dasharray':'16 14','stroke-linejoin':'round'},ghost));
el('line',{x1:0,y1:-10,x2:0,y2:-340,stroke:CR,'stroke-width':5,'stroke-dasharray':'16 14'},ghost);
const solid=el('g',{},ship);
const hf=el('path',{d:HULL,fill:BR},solid);const s1f=el('path',{d:SAIL1,fill:CR},solid);const s2f=el('path',{d:SAIL2,fill:CR},solid);
const strokes=[HULL,SAIL1,SAIL2].map(d=>el('path',{d,fill:'none',stroke:GOLD,'stroke-width':7,'stroke-linejoin':'round',pathLength:1,'stroke-dasharray':1},solid));
const mast=el('line',{x1:0,y1:-10,x2:0,y2:-340,stroke:GOLD,'stroke-width':8,'stroke-linecap':'round',pathLength:1,'stroke-dasharray':1},solid);
const planks=[40,80].map(y=>el('path',{d:`M${-272+y*0.5} ${y} H${292-y*1.1}`,stroke:'#0f1f3a','stroke-width':4,opacity:.3,fill:'none',pathLength:1,'stroke-dasharray':1},solid));
// waves
const waves=[0,1,2].map(i=>el('path',{fill:'none',stroke:i==0?BR:GOLD,'stroke-width':i==0?6:4,'stroke-linecap':'round',opacity:[1,.6,.35][i]}));
const sea=el('path',{fill:'#0f1f3a'});st.insertBefore(sea,waves[0]);
// ore -> tools chain
const ore=el('g',{});el('path',{d:'M-62 30 L-40 -34 L8 -58 L58 -26 L66 28 L20 54 L-34 52Z',fill:BR,stroke:GOLD,'stroke-width':5,'stroke-linejoin':'round'},ore);el('path',{d:'M-40 -34 L-4 4 L8 -58 M-4 4 L66 28 M-4 4 L-34 52',fill:'none',stroke:'#0f1f3a','stroke-width':3,opacity:.35},ore);
const oreT=el('text',{x:200,y:905,'text-anchor':'middle','font-size':28,'font-weight':600,'letter-spacing':6,fill:GOLD});oreT.textContent='ORE';
const arrow=el('path',{d:'M300 800 H430 M408 780 L432 800 L408 820',fill:'none',stroke:CR,'stroke-width':5,'stroke-linecap':'round','stroke-linejoin':'round',pathLength:1,'stroke-dasharray':1});
const ham=el('g',{});el('rect',{x:-9,y:-40,width:18,height:110,rx:6,fill:GOLD},ham);el('rect',{x:-52,y:-70,width:104,height:46,rx:8,fill:BR,stroke:GOLD,'stroke-width':5},ham);
const hamT=el('text',{x:540,y:905,'text-anchor':'middle','font-size':28,'font-weight':600,'letter-spacing':6,fill:GOLD});hamT.textContent='TOOLS';
const arrow2=el('path',{d:'M650 800 H780 M758 780 L782 800 L758 820',fill:'none',stroke:CR,'stroke-width':5,'stroke-linecap':'round','stroke-linejoin':'round',pathLength:1,'stroke-dasharray':1});
const shipT=el('text',{x:880,y:812,'text-anchor':'middle','font-size':34,'font-weight':700,'letter-spacing':6,fill:CR});shipT.textContent='SHIP';
function scene(t){
 const out1=1-eo(pr(t,T.listen,0.5));
 chips.forEach((g,i)=>{const a=eo(pr(t,[T.no1,T.no2,T.no3][i],0.4));g.setAttribute('opacity',a*out1);g.setAttribute('transform',`translate(${190+i*350},${60+(1-a)*20})`)});
 notq.forEach((q,i)=>{const s=[T.how,T.why][i];const a=eo(pr(t,s,0.35));q.g.setAttribute('opacity',a*(1-eo(pr(t,T.asks,0.5))));
  q.ln.setAttribute('stroke-dashoffset',1-eio(pr(t,s+0.45,0.35)))});
 const WY=600;
 waves.forEach((w,i)=>{let d='';for(let x=-20;x<=1100;x+=20){const y=WY+i*34+Math.sin(x/90+t*(1.6-i*0.3)+i*2)*(14-i*3);d+=(x==-20?'M':'L')+x+' '+y}w.setAttribute('d',d);w.setAttribute('opacity',[1,.6,.35][i]*eo(pr(t,0.3+i*0.15,0.8)))});
 let d='M-20 720';for(let x=-20;x<=1100;x+=20){d+=` L${x} ${WY+Math.sin(x/90+t*1.6)*14}`}sea.setAttribute('d',d+' L1100 720Z');
 const bob=Math.sin(540/90+t*1.6)*12, tilt=Math.cos(540/90+t*1.6)*1.6;
 ship.setAttribute('transform',`translate(540,${WY-96+bob}) rotate(${tilt})`);
 const b=eio(pr(t,T.build,T.bdur));
 ghost.setAttribute('opacity',eo(pr(t,T.ship,0.9))*(0.55+0.2*Math.sin(t*3))*(1-b));
 strokes.forEach((s,i)=>s.setAttribute('stroke-dashoffset',1-cl(b*1.6-i*0.25)));
 mast.setAttribute('stroke-dashoffset',1-cl(b*1.6-0.2));
 hf.setAttribute('opacity',cl(b*2-0.6));s1f.setAttribute('opacity',cl(b*2-0.9)*0.95);s2f.setAttribute('opacity',cl(b*2-1.0)*0.85);
 planks.forEach((p,i)=>p.setAttribute('stroke-dashoffset',1-cl(b*2-1+i*-0.1)));
 // ore drops so it lands on "ore"
 const o0=T.ore-0.35;const od=pr(t,o0,0.7);ore.setAttribute('transform',`translate(200,${-100+(800+100)*bounce(od)}) scale(${1+0.06*Math.sin(Math.PI*pr(t,o0+0.7,0.4))})`);ore.setAttribute('opacity',od>0?1:0);
 oreT.setAttribute('opacity',eo(pr(t,o0+0.6,0.4)));
 arrow.setAttribute('stroke-dashoffset',1-eio(pr(t,T.make,0.4)));arrow.setAttribute('opacity',t>T.make?1:0);
 const ha=eo(pr(t,T.tools-0.2,0.5));const swing=t>T.making&&t<T.making+1.2?Math.sin((t-T.making)*10)*18*(1-pr(t,T.making,1.2)):0;
 ham.setAttribute('transform',`translate(540,800) rotate(${-25+swing}) scale(${0.6+0.4*ha})`);ham.setAttribute('opacity',ha);
 hamT.setAttribute('opacity',eo(pr(t,T.tools,0.4)));
 arrow2.setAttribute('stroke-dashoffset',1-eio(pr(t,T.toolsdone,0.5)));arrow2.setAttribute('opacity',t>T.toolsdone?1:0);
 shipT.setAttribute('opacity',eo(pr(t,T.toolsdone+0.4,0.4)));
 // 1 Nephi 17:17
 const fool=t>=T.brothers&&t<T.making+0.6;
 $('count').textContent=fool?'“OUR BROTHER IS A FOOL”':'';$('count').style.color='#d9735a';
 $('count').style.opacity=fool?eo(pr(t,T.brothers,0.3))*(1-eo(pr(t,T.making,0.6))):0;
}
'''
CAPS=[["His ",0,0],["first ",0,0],["question:",0,1],["where ",1,0],["do ",1,0],["I ",1,0],["find ",1,0],["ore?",1,0]]
capw=v.capw(CAPS)
html=os.path.join(HERE,'ep03_nephi.html')
build(html,3,"You don't need the ship yet.",'You need the ore.','1 NEPHI 17 : 8–18',CAPS,capw[0],youdont-0.1,SCENE.replace('__T__',json.dumps(T)),
      capw=capw,cue=dict(c1=youdont+0.15,c2=youneed,hl=youneed+0.25,ref=youneed+0.9))
v.finish('ep03',html,out)
