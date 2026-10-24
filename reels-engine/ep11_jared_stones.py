"""Parable No. 11, the brother of Jared's stones, timed to a voiceover.

usage: python ep11_jared_stones.py <voice audio> <word timestamps json> <out.mp4>
Ether 3:1-6: eight vessels prepared, up the mount Shelem, sixteen small stones molten out of a rock,
white and clear like glass (1); he asks the Lord to touch them that they may shine forth in darkness (4);
the Lord touches the stones one by one (6).
"""
import json,os,sys
from base import build
from episode import Voice,HERE

v=Voice(*sys.argv[1:3]);out=sys.argv[3];at=v.at
T=dict(
 vessels=at('the vessels'),light=at('needs light'),mount=at('up the mount'),melts=at('melts'),sixteen=at('sixteen small stones'),
 clear=at('white and clear'),carries=at('he carries'),prays=at('and prays'),touch=at('touch these stones'),shine=at('shine forth'),
 stretches=at('stretches forth'),one=at('one by one'),
)
punch=at('he did the work');c2=at('then he asked')

SCENE=r'''
const T=__T__,RED='#d9735a';
const dr=(a,p)=>el('path',Object.assign({fill:'none',stroke:GOLD,'stroke-width':8,'stroke-linecap':'round','stroke-linejoin':'round',pathLength:1,'stroke-dasharray':1},a),p);
// the vessel (a covered boat), dark inside
const boat=el('g',{transform:'translate(540,640)'});
const hull=dr({d:'M-330 -40 Q-300 120 -140 130 H140 Q300 120 330 -40 Z'},boat);
const lid=dr({d:'M-250 -40 Q-250 -150 0 -150 Q250 -150 250 -40','stroke-width':6},boat);
const wave=dr({d:'M-420 150 q35 -20 70 0 t70 0 t70 0 t70 0 t70 0 t70 0 t70 0 t70 0 t70 0 t70 0 t70 0 t70 0','stroke-width':5,opacity:.6},boat);
const dark=el('text',{x:0,y:40,'text-anchor':'middle','font-size':34,'font-weight':600,'letter-spacing':8,fill:'#6b7a96'},boat);dark.textContent='DARK';
// the mount, a rock, sixteen stones
const mt=dr({d:'M120 500 L540 120 L960 500'});
const rock=dr({d:'M410 470 Q420 380 520 370 Q640 360 680 470 Z'});
const stones=[...Array(16)].map((_,i)=>el('circle',{r:26,fill:'#0f1f3a',stroke:CR,'stroke-width':4}));
const glow=[...Array(16)].map((_,i)=>el('circle',{r:26,fill:BR,opacity:0}));
const rays=[...Array(16)].map((_,i)=>el('path',{d:'',stroke:BR,'stroke-width':4,'stroke-linecap':'round',opacity:0}));
const pos=i=>[540+((i%4)-1.5)*88,200+Math.floor(i/4)*88];
function scene(t){
 const bp=eio(pr(t,0.2,0.9));
 hull.setAttribute('stroke-dashoffset',1-bp);lid.setAttribute('stroke-dashoffset',1-eio(pr(t,T.vessels,0.9)));wave.setAttribute('stroke-dashoffset',1-eio(pr(t,T.vessels+0.2,1.2)));
 wave.setAttribute('transform',`translate(${Math.sin(t*1.5)*20},0)`);
 const lit=eo(pr(t,T.one,1.0));
 dark.setAttribute('opacity',eo(pr(t,T.light-0.3,0.5))*(1-lit));
 // boat shrinks away when we climb, comes back at the end
 const up=eio(pr(t,T.mount,0.8)),back=eio(pr(t,T.one-0.4,0.8));
 const away=up*(1-back);
 boat.setAttribute('transform',`translate(540,${640+away*340}) scale(${1-away*0.55})`);
 mt.setAttribute('stroke-dashoffset',1-eio(pr(t,T.mount,0.8)));mt.setAttribute('opacity',1-back);
 rock.setAttribute('stroke-dashoffset',1-eio(pr(t,T.mount+0.4,0.8)));rock.setAttribute('opacity',(1-back));
 stones.forEach((s,i)=>{
  const [x,y]=pos(i);const ap=eo(pr(t,T.melts+0.2+i*0.12,0.4));
  // carried from the rock up to the top of the mount, then into the dark boat at the end
  const cp=eio(pr(t,T.carries,0.9)),home=eio(pr(t,T.one-0.4+i*0.03,0.8));
  const bx=540+((i%4)-1.5)*56,by=620+Math.floor(i/4)*26;
  let sx=540+(x-540)*cp+((i%4)-1.5)*(1-cp)*20,sy=420+(y-420)*cp;
  sx=sx+(bx-sx)*home;sy=sy+(by-sy)*home;
  s.setAttribute('cx',sx);s.setAttribute('cy',sy-(i>0?0:0));s.setAttribute('opacity',ap);s.setAttribute('r',26*(1-0.4*home));
  s.setAttribute('stroke',t>=T.clear&&t<T.touch?CR:CR);
  // the Lord touches the stones one by one: each lights in turn
  const g=eo(pr(t,T.stretches+0.1+i*0.15,0.5));
  glow[i].setAttribute('cx',sx);glow[i].setAttribute('cy',sy);glow[i].setAttribute('r',s.getAttribute('r'));glow[i].setAttribute('opacity',g*0.9);
  const rr=g*(30+10*Math.sin(t*5+i));
  rays[i].setAttribute('d',`M${sx} ${sy-s.getAttribute('r')-10} v${-rr}`);rays[i].setAttribute('opacity',g*(1-home)*0.8);
 });
 const c=t>=T.stretches?'TOUCHED ONE BY ONE':t>=T.prays?'ASKS FOR LIGHT':t>=T.clear?'SIXTEEN STONES · CLEAR AS GLASS':t>=T.melts?'MELTED FROM ROCK':t>=T.light?'NO LIGHT FOR THE CROSSING':'';
 $('count').textContent=c;$('count').style.color=t>=T.light&&t<T.melts?RED:'#c9a24a';$('count').style.opacity=c?1:0;
}
'''
CAPS=[["That ",0,0],["they ",0,0],["may ",0,0],["shine ",1,0],["forth ",1,0],["in ",0,0],["darkness.",1,0]]
capw=v.capw(CAPS)
html=os.path.join(HERE,'ep11_jared_stones.html')
build(html,11,'Do what you can.','Then ask.','ETHER 3 : 1–6',CAPS,capw[0],punch-0.1,SCENE.replace('__T__',json.dumps(T)),
      capw=capw,cue=dict(c1=punch+0.1,c2=c2,hl=c2+0.25,ref=c2+0.9))
v.finish('ep11',html,out)
