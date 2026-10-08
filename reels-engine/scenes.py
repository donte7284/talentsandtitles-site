from base import build
TOWER=r'''
const GY=800;
el('line',{x1:80,y1:GY,x2:1000,y2:GY,stroke:GOLD,'stroke-width':6,'stroke-linecap':'round',pathLength:1,'stroke-dasharray':1,id:'ground'});
// ghost plan
const ghost=el('g',{id:'ghost'});
const GP="M340 710 V200 H400 V150 H470 V200 H505 V150 H575 V200 H610 V150 H680 V200 H740 V710";
const gp=el('path',{d:GP,fill:'none',stroke:CR,'stroke-width':5,'stroke-dasharray':'18 16','stroke-linejoin':'round'},ghost);
const glen=2200;const gmask=el('clipPath',{id:'gm'});const gmr=el('rect',{x:300,y:710,width:480,height:0},gmask);ghost.setAttribute('clip-path','url(#gm)');
[590,470,350].forEach(y=>el('line',{x1:340,y1:y,x2:740,y2:y,stroke:CR,'stroke-width':3,'stroke-dasharray':'10 14',opacity:.6},ghost));
const plan=el('text',{x:540,y:110,'text-anchor':'middle','font-size':30,'font-weight':600,'letter-spacing':7,fill:CR});plan.textContent='THE PLAN';
// funds bar
const fb=el('g',{});
const ft=el('text',{x:90,y:40,'font-size':30,'font-weight':600,'letter-spacing':7,fill:GOLD},fb);ft.textContent='FUNDS';
el('rect',{x:240,y:14,width:750,height:30,rx:15,fill:'none',stroke:GOLD,'stroke-width':4},fb);
const fbar=el('rect',{x:246,y:20,width:738,height:18,rx:9,fill:BR},fb);
// foundation blocks
const blocks=[0,1,2,3].map(i=>{const g=el('g',{});el('rect',{x:-96,y:-86,width:192,height:86,rx:8,fill:BR},g);el('rect',{x:-96,y:-86,width:192,height:86,rx:8,fill:'none',stroke:GOLD,'stroke-width':5},g);el('line',{x1:-60,y1:-43,x2:60,y2:-43,stroke:'#0f1f3a','stroke-width':4,opacity:.25},g);return g});
const b5=el('g',{});el('rect',{x:-96,y:-86,width:192,height:86,rx:8,fill:'none',stroke:BR,'stroke-width':5},b5);
const B0=2.6,BD=0.75,BG=0.55;
function scene(t){
 $('ground').setAttribute('stroke-dashoffset',1-eo(pr(t,0.3,0.8)));
 const gh=eio(pr(t,0.9,1.4))*600;gmr.setAttribute('y',710-gh);gmr.setAttribute('height',gh+20);
 const dim=1-0.55*eo(pr(t,B0+4*(BD+BG)+0.9,0.8));
 const pulse=t>9.2?0.75+0.25*Math.sin((t-9.2)*4):1;
 ghost.setAttribute('opacity',dim*pulse);
 plan.setAttribute('opacity',eo(pr(t,1.6,0.5))*dim);
 fb.setAttribute('opacity',eo(pr(t,1.9,0.5)));
 let spent=0;
 blocks.forEach((g,i)=>{const s=B0+i*(BD+BG);const p=pr(t,s,BD);const y=-140+(GY+140-3)*bounce(p);
  g.setAttribute('transform',`translate(${240+i*200},${y})`);g.setAttribute('opacity',p>0?1:0);spent+=eio(pr(t,s+0.25,0.5));});
 const left=1-spent/4;fbar.setAttribute('width',Math.max(0,738*left));
 const empty=pr(t,B0+4*(BD+BG)-0.3,0.4);fbar.setAttribute('fill',left<0.3?'#d9735a':BR);
 ft.setAttribute('fill',empty>=1?'#d9735a':GOLD);
 // fifth block hovers, shakes, falls away
 const s5=B0+4*(BD+BG)+0.2;const a=pr(t,s5,0.5),hold=pr(t,s5+0.5,1.0),drop=pr(t,s5+1.5,0.7);
 const shake=hold>0&&drop<=0?Math.sin(t*40)*6*hold:0;
 b5.setAttribute('transform',`translate(${440+shake},${420+ (1-eo(a))*-120 + eio(drop)*40}) rotate(${drop*14})`);
 b5.setAttribute('opacity',eo(a)*(1-eo(drop)));
 $('count').textContent=t>B0+4*(BD+BG)+1.2?'1 LEVEL BUILT · 5 PLANNED · FUNDS 0':'';$('count').style.opacity=eo(pr(t,B0+4*(BD+BG)+1.2,0.5));
}
'''
SHIP=r'''
const chips=['NO SHIPYARD','NO CREW','NO TOOLS'].map((s,i)=>{const g=el('g',{transform:`translate(${190+i*350},60)`});const tx=el('text',{x:0,y:10,'text-anchor':'middle','font-size':32,'font-weight':600,'letter-spacing':5,fill:CR},g);tx.textContent=s;return g});
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
 chips.forEach((g,i)=>{const a=eo(pr(t,1.9+i*0.55,0.4));const fade=1-0.7*eo(pr(t,4.4,0.6));g.setAttribute('opacity',a*fade);g.setAttribute('transform',`translate(${190+i*350},${60+(1-a)*20})`)});
 const WY=600;
 waves.forEach((w,i)=>{let d='';for(let x=-20;x<=1100;x+=20){const y=WY+i*34+Math.sin(x/90+t*(1.6-i*0.3)+i*2)*(14-i*3);d+=(x==-20?'M':'L')+x+' '+y}w.setAttribute('d',d);w.setAttribute('opacity',[1,.6,.35][i]*eo(pr(t,0.3+i*0.15,0.8)))});
 let d='M-20 720';for(let x=-20;x<=1100;x+=20){d+=` L${x} ${WY+Math.sin(x/90+t*1.6)*14}`}sea.setAttribute('d',d+' L1100 720Z');
 const bob=Math.sin(540/90+t*1.6)*12, tilt=Math.cos(540/90+t*1.6)*1.6;
 ship.setAttribute('transform',`translate(540,${WY-96+bob}) rotate(${tilt})`);
 const build=t=>eio(pr(t,8.3,2.2));const b=build(t);
 ghost.setAttribute('opacity',eo(pr(t,0.9,0.9))*(0.55+0.2*Math.sin(t*3))*(1-b));
 strokes.forEach((s,i)=>s.setAttribute('stroke-dashoffset',1-cl(b*1.6-i*0.25)));
 mast.setAttribute('stroke-dashoffset',1-cl(b*1.6-0.2));
 hf.setAttribute('opacity',cl(b*2-0.6));s1f.setAttribute('opacity',cl(b*2-0.9)*0.95);s2f.setAttribute('opacity',cl(b*2-1.0)*0.85);
 planks.forEach((p,i)=>p.setAttribute('stroke-dashoffset',1-cl(b*2-1+i*-0.1)));
 // ore drops
 const od=pr(t,5.0,0.7);ore.setAttribute('transform',`translate(200,${-100+(800+100)*bounce(od)}) scale(${1+0.06*Math.sin(Math.PI*pr(t,5.7,0.4))})`);ore.setAttribute('opacity',od>0?1:0);
 oreT.setAttribute('opacity',eo(pr(t,5.6,0.4)));
 arrow.setAttribute('stroke-dashoffset',1-eio(pr(t,6.2,0.5)));arrow.setAttribute('opacity',t>6.2?1:0);
 const ha=eo(pr(t,6.7,0.5));const swing=t>7.2&&t<8.4?Math.sin((t-7.2)*10)*18*(1-pr(t,7.2,1.2)):0;
 ham.setAttribute('transform',`translate(540,800) rotate(${-25+swing}) scale(${0.6+0.4*ha})`);ham.setAttribute('opacity',ha);
 hamT.setAttribute('opacity',eo(pr(t,7.0,0.4)));
 arrow2.setAttribute('stroke-dashoffset',1-eio(pr(t,7.7,0.5)));arrow2.setAttribute('opacity',t>7.7?1:0);
 shipT.setAttribute('opacity',eo(pr(t,8.2,0.4)));
 $('count').textContent='';
}
'''
OIL=r'''
// drawn on a 960x860 stage originally placed at (60,300); base stage sits at (0,260)
const ofr=el('clipPath',{id:'oilframe'},el('defs',{}));el('rect',{x:0,y:0,width:960,height:860},ofr);
const W=el('g',{transform:'translate(60,40)','clip-path':'url(#oilframe)'});
const JAR="M-55 -150 h110 v28 q0 14 14 22 q46 30 46 110 v120 q0 50 -50 50 h-130 q-50 0 -50 -50 v-120 q0 -80 46 -110 q14 -8 14 -22z";
const INNER="M-104 -30 q10 -40 40 -62 h128 q30 22 40 62 v158 q0 44 -44 44 h-120 q-44 0 -44 -44z";
const pos=[[160,190],[480,190],[800,190],[160,610],[480,610],[800,610]];
const defs=el('defs',{},W);const cp=el('clipPath',{id:'cp'},defs);el('path',{d:INNER},cp);
const jars=pos.map((p,i)=>{const g=el('g',{transform:`translate(${p[0]},${p[1]})`},W);
 const o={g};
 if(i<5){o.stream=el('rect',{x:-7,y:-330,width:14,height:0,rx:7,fill:BR},g);
  const c=el('g',{'clip-path':'url(#cp)'},g);o.liq=el('path',{fill:BR},c);
  o.out=el('path',{d:JAR,fill:'none',stroke:GOLD,'stroke-width':7,'stroke-linejoin':'round',pathLength:1,'stroke-dasharray':1},g);
 }else{o.box=el('rect',{x:-120,y:-170,width:240,height:360,rx:24,fill:'none',stroke:CR,'stroke-width':5,'stroke-dasharray':'18 16'},g);
  o.q=el('text',{x:0,y:50,'text-anchor':'middle',style:'font-family:Lora','font-size':150,fill:CR},g);o.q.textContent='?';}
 return o});
const F0=1.5,FD=0.95,GAP=0.12;
function scene(t){
 let full=0;
 jars.forEach((j,i)=>{
  if(i<5){
   const a=eo(pr(t,0.3+i*0.12,0.8));
   j.out.setAttribute('stroke-dashoffset',1-a);j.g.setAttribute('opacity',a>0?1:0);
   const s=F0+i*(FD+GAP);const p=eio(pr(t,s,FD));if(p>=0.999)full++;
   const lvl=172-p*250;const amp=(p>0&&p<1)?7*Math.sin(Math.PI*p):1.5*Math.max(0,1-(t-s-FD)/1.2)*(p>=1?1:0);
   let d=`M-130 ${lvl}`;for(let x=-130;x<=130;x+=10){d+=` L${x} ${lvl+amp*Math.sin(x/22+t*9+i)}`}d+=' L130 200 L-130 200Z';
   j.liq.setAttribute('d',p>0?d:'');
   // stream: descends, holds, then tail falls
   const raw=pr(t,s-0.12,FD+0.12);let top=-330,bot=-330;
   if(raw>0&&raw<1){const head=cl(raw/0.14);const tail=cl((raw-0.82)/0.18);bot=-330+(lvl+330)*eo(head);top=-330+(lvl+330)*eio(tail);}
   j.stream.setAttribute('y',top);j.stream.setAttribute('height',Math.max(0,bot-top));
   const sc=1+0.04*Math.sin(Math.PI*pr(t,s+FD-0.05,0.35));
   j.g.setAttribute('transform',`translate(${pos[i][0]},${pos[i][1]}) scale(${sc})`);
  }else{
   const a=eo(pr(t,6.9,0.5));const pulse=0.45+0.3*Math.sin(Math.max(0,t-7.4)*5)*(t>7.4?1:0);
   j.g.setAttribute('opacity',a*cl(pulse,0.2,0.8));
   j.g.setAttribute('transform',`translate(${pos[i][0]},${pos[i][1]}) scale(${0.9+0.1*a})`);
  }});
 $('count').textContent=t>6.9?'5 FULL · NO JARS LEFT':t>F0?`${full} FULL`:'';$('count').style.opacity=eo(pr(t,F0,0.4));
}
'''
# keeps the approved No. 1 layout, which predates base.py
OIL_CSS='#count{top:1170px}#cap{top:1290px}#c2{font-size:110px}'
build('oil.html',1,'The supply was never the limit.','The jars were.','2 KINGS 4 : 1–7',[["The ",0,0],["oil ",0,0],["stops ",0,0],["when ",0,0],["she ",0,1],["runs ",1,0],["out ",1,0],["of ",1,0],["jars.",1,0]],7.0,9.6,OIL,OIL_CSS)
build('tower.html',2,'Everybody starts.','Count the cost.','LUKE 14 : 28–30',[["He ",0,0],["started, ",0,0],["and",0,1],["couldn't ",1,0],["finish.",1,0]],8.9,11.4,TOWER)
build('ship.html',3,"You don't need the ship yet.",'You need the ore.','1 NEPHI 17 : 8–18',[["His ",0,0],["first ",0,0],["question:",0,1],["where ",1,0],["do ",1,0],["I ",1,0],["find ",1,0],["ore?",1,0]],9.6,12.6,SHIP)
