"""Parable No. 7, Nephi's broken bow, timed to a voiceover.

usage: python ep07_bow.py <voice audio> <word timestamps json> <out.mp4>
1 Nephi 16:18-32: the steel bow breaks, the brothers' bows lose their springs, Nephi makes a wooden bow and
an arrow, asks where to go, is directed up the mountain and brings food home.
"""
import json,os,sys
from base import build
from episode import Voice,HERE
from kit import KIT

v=Voice(*sys.argv[1:3]);out=sys.argv[3];at=v.at
T=dict(
 breaks=at('breaks his bow'),steel=at('fine steel'),angry=at('are angry'),springs=at('lost their springs'),murmur=at('is murmuring'),
 makes=at('makes a bow'),wood=at('out of wood'),arrow=at('an arrow'),stick=at('straight stick'),asks=at('asks his father'),
 whither=at('shall i go'),food=at('to obtain food'),dir=at('gives direction'),mount=at('up the mountain'),home=at('food home'),
)
punch=at("the tool broke");whenp=at('what just broke')

SCENE=KIT+r'''
const T=__T__;
const ARC='M600 150 Q330 400 600 650',TOP='M600 150 Q465 275 465 400',BOT='M465 400 Q465 525 600 650';
// steel bow: shown whole, then snaps
const whole=line(ARC,GOLD,10);const string=line('M600 150 V650',CR,4);
const topH=line(TOP,GOLD,10,{opacity:0});const botH=line(BOT,GOLD,10,{opacity:0});
const crack=line('M440 380 l22 14 -24 14 24 14',RED,6);
const steel=txt(540,780,'FINE STEEL',32,GOLD,8),broken=txt(540,780,'BROKEN',36,RED,10);
// the brothers' bows: strings gone slack
function slack(cx){const g=el('g',{transform:`translate(${cx},560) scale(0.38)`});
 el('path',{d:ARC,fill:'none',stroke:RED,'stroke-width':14,'stroke-linecap':'round'},g);
 el('path',{d:'M600 150 Q520 400 600 650',fill:'none',stroke:CR,'stroke-width':6,'stroke-dasharray':'16 14'},g);return g}
const sl=[slack(-30),slack(740)];
const nospring=txt(540,880,'NO SPRING · NO FOOD',32,RED,8);
// new wooden bow + arrow
const wb=el('g',{});el('path',{d:'M180 -230 Q-90 0 180 230',fill:'none',stroke:'#0f1f3a','stroke-width':22,'stroke-linecap':'round'},wb);
const wbow=el('path',{d:'M180 -230 Q-90 0 180 230',fill:'none',stroke:BR,'stroke-width':14,'stroke-linecap':'round',pathLength:1,'stroke-dasharray':1},wb);
const wstr=el('path',{d:'M180 -230 V230',stroke:CR,'stroke-width':4,'stroke-linecap':'round',pathLength:1,'stroke-dasharray':1},wb);
const arr=el('g',{});el('path',{d:'M-300 0 H300',stroke:BR,'stroke-width':9,'stroke-linecap':'round',pathLength:1,'stroke-dasharray':1,id:'sh'},arr);
el('path',{d:'M300 0 l-34 -22 M300 0 l-34 22',stroke:BR,'stroke-width':9,'stroke-linecap':'round'},arr);
const wlab=txt(540,780,'WOOD · A STRAIGHT STICK',32,BR,7);
const q=txt(540,330,'WHITHER SHALL I GO?',40,CR,8,600);
// direction: an arrow up to a mountain, food at the end
const mt=line('M250 760 L470 430 L580 560 L700 400 L860 760',GOLD,8);
const route=line('M300 760 Q420 640 500 560 T700 410',BR,7,{'stroke-dasharray':'1'});
const dirT=txt(540,880,'DIRECTION',34,BR,10),foodT=txt(540,880,'FOOD FOR THE FAMILIES',32,BR,7);
const bowl=el('g',{transform:'translate(540,640)'});el('path',{d:'M-90 0 H90 Q80 70 0 76 Q-80 70 -90 0 Z',fill:BR,'fill-opacity':.5,stroke:GOLD,'stroke-width':7,'stroke-linejoin':'round'},bowl);
function scene(t){
 const br=eio(pr(t,T.breaks,0.5));
 const drawn=eio(pr(t,0.3,1.0));dash(whole,drawn);dash(string,drawn);
 const phaseA=1-eo(pr(t,T.makes-0.4,0.6));
 const hw=t<T.breaks?1:0;
 op(whole,hw*phaseA);op(string,(t<T.breaks+0.1?1:0)*phaseA);
 op(topH,(1-hw)*phaseA);op(botH,(1-hw)*phaseA);
 topH.setAttribute('transform',`rotate(${-38*br} 600 150) translate(${-70*br},${-30*br})`);botH.setAttribute('transform',`rotate(${38*br} 600 650) translate(${-70*br},${30*br})`);
 op(crack,Math.max(0,eo(pr(t,T.breaks,0.2))*(1-eo(pr(t,T.breaks+0.5,0.5))))*phaseA);dash(crack,eo(pr(t,T.breaks,0.3)));
 op(steel,eo(pr(t,T.steel,0.4))*(1-eo(pr(t,T.breaks,0.2))));op(broken,eo(pr(t,T.breaks+0.1,0.4))*phaseA);
 sl.forEach((g,i)=>op(g,eo(pr(t,T.springs+i*0.2,0.5))*phaseA));
 op(nospring,eo(pr(t,T.murmur,0.5))*phaseA);
 // wooden bow and arrow
 const mk=eio(pr(t,T.wood,0.9)),ar=eio(pr(t,T.stick,0.7));const phaseB=1-eo(pr(t,T.dir-0.3,0.5));
 wb.setAttribute('transform','translate(470,430) scale(.9)');dash(wbow,mk);dash(wstr,mk);
 op(wb,(t>T.makes?1:0)*phaseB);
 arr.setAttribute('transform','translate(540,430) scale(.6)');dash($('sh'),ar);op(arr,(t>T.arrow?1:0)*phaseB);
 op(wlab,eo(pr(t,T.wood,0.4))*phaseB);
 const qa=eo(pr(t,T.whither,0.5))*(1-eo(pr(t,T.dir,0.4)));op(q,qa);
 q.setAttribute('y',160);
 dash(mt,eio(pr(t,T.dir+0.2,0.8)));op(mt,t>T.dir?1:0);
 dash(route,eio(pr(t,T.mount,0.9)));op(route,t>T.mount?1:0);
 op(dirT,eo(pr(t,T.dir,0.4))*(1-eo(pr(t,T.home,0.3))));
 const bo=eo(pr(t,T.home,0.5));bowl.setAttribute('transform',`translate(540,${660-(1-bo)*60})`);op(bowl,bo);op(foodT,eo(pr(t,T.home+0.3,0.4)));
 $('count').textContent='';
}
'''
CAPS=[["Nephi ",0,0],["breaks ",0,0],["his ",0,0],["bow.",1,0]]
capw=v.capw(CAPS)
html=os.path.join(HERE,'ep07_bow.html')
build(html,7,'The tool broke.','Make another.','1 NEPHI 16 : 18–32',CAPS,capw[0],punch-0.1,SCENE.replace('__T__',json.dumps(T)),
      capw=capw,cue=dict(c1=punch,c2=at('made another'),hl=at('made another')+0.25,ref=at('made another')+0.9))
v.finish('ep07',html,out)
