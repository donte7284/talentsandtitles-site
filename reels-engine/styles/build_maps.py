from mk import page
GEO=r'''
const cv=document.createElement('canvas');cv.width=1080;cv.height=1920;document.body.prepend(cv);const X=cv.getContext('2d');
// ---- shared fictional geography (deterministic) ----
const CX=540,CY=990;
const coastR=a=>1+.10*Math.sin(a*3+.7)+.07*Math.sin(a*5+2.1)+.05*Math.sin(a*9+.3)+.03*Math.sin(a*17+1.3);
const COAST=[];for(let i=0;i<=240;i++){const a=i/240*Math.PI*2;const r=coastR(a);COAST.push([CX+Math.cos(a)*400*r,CY+Math.sin(a)*600*r])}
const landPath=(ctx,sc=1,ox=0,oy=0)=>{ctx.beginPath();COAST.forEach(([x,y],i)=>{const px=CX+(x-CX)*sc+ox,py=CY+(y-CY)*sc+oy;i?ctx.lineTo(px,py):ctx.moveTo(px,py)});ctx.closePath()};
const MOUNTAINS=[];for(let i=0;i<14;i++){const u=i/13;MOUNTAINS.push([270+u*270+Math.sin(i*1.7)*22,560+u*330+Math.cos(i*2.3)*18,38+((i*7)%5)*7])}
const RIVER=[[470,900],[500,980],[470,1060],[540,1130],[620,1170],[660,1260],[740,1330],[790,1430],[850,1530]];
const FOREST=[];for(let i=0;i<46;i++){const a=i*2.39996,r=Math.sqrt(i/46)*120;FOREST.push([700+Math.cos(a)*r*1.3,690+Math.sin(a)*r*.8])}
const FOREST2=[];for(let i=0;i<26;i++){const a=i*2.39996,r=Math.sqrt(i/26)*80;FOREST2.push([330+Math.cos(a)*r*1.2,1190+Math.sin(a)*r*.8])}
const CITIES=[['Northgate',400,470],['Ashford',770,860],['Harrowmere',380,1360],['Coastreach',740,1540],['Fenwick',260,960]];
const CLASH=[600,1120];
const ROUTE_A=[[770,860],[735,940],[690,1010],[640,1070],[600,1120]];
const ROUTE_B=[[380,1360],[430,1300],[480,1240],[545,1170],[600,1120]];
const seg=(pts,p)=>{// point + partial polyline at fraction p
 const L=[];let tot=0;for(let i=1;i<pts.length;i++){const d=Math.hypot(pts[i][0]-pts[i-1][0],pts[i][1]-pts[i-1][1]);L.push(d);tot+=d}
 let want=tot*p;const out=[pts[0]];for(let i=1;i<pts.length;i++){if(want>=L[i-1]){out.push(pts[i]);want-=L[i-1]}else{const f=want/L[i-1];out.push([pts[i-1][0]+(pts[i][0]-pts[i-1][0])*f,pts[i-1][1]+(pts[i][1]-pts[i-1][1])*f]);break}}
 const a=out[out.length-1],b=out[Math.max(0,out.length-2)];return{pts:out,head:a,ang:Math.atan2(a[1]-b[1],a[0]-b[0])}};
const smooth=(ctx,pts)=>{ctx.beginPath();ctx.moveTo(...pts[0]);for(let i=1;i<pts.length-1;i++){const mx=(pts[i][0]+pts[i+1][0])/2,my=(pts[i][1]+pts[i+1][1])/2;ctx.quadraticCurveTo(pts[i][0],pts[i][1],mx,my)}if(pts.length>1)ctx.lineTo(...pts[pts.length-1])};

// ---- armies as formations: cavalry ▲ front, infantry ■ middle, archers ● rear ----
const pathInfo=R=>{const cum=[0];for(let i=1;i<R.length;i++)cum.push(cum[i-1]+Math.hypot(R[i][0]-R[i-1][0],R[i][1]-R[i-1][1]));return{R,cum,L:cum[cum.length-1]}};
const at=(P,d)=>{d=Math.max(0,Math.min(P.L,d));let i=1;while(i<P.R.length-1&&P.cum[i]<d)i++;const a=P.R[i-1],b=P.R[i],f=(d-P.cum[i-1])/(P.cum[i]-P.cum[i-1]||1);return{x:a[0]+(b[0]-a[0])*f,y:a[1]+(b[1]-a[1])*f,ang:Math.atan2(b[1]-a[1],b[0]-a[0])}};
const FORM=[];[-40,0,40].forEach((l,i)=>FORM.push({type:'cav',back:i==1?0:20,lat:l}));[-20,20].forEach(l=>FORM.push({type:'cav',back:42,lat:l}));
[76,118,160].forEach(b=>[-42,0,42].forEach(l=>FORM.push({type:'inf',back:b,lat:l})));
[208,246].forEach(b=>[-42,0,42].forEach(l=>FORM.push({type:'arc',back:b,lat:l})));
function armyUnits(R,p,side,t){const P=pathInfo(R);const head=p*(P.L-26);const clash=pr(t,T.clash[0],1.6);
 return FORM.map((u,i)=>{const d=head-u.back;const q=at(P,d);const nx=-Math.sin(q.ang),ny=Math.cos(q.ang);let x=q.x+nx*u.lat,y=q.y+ny*u.lat;
  // melee: front ranks push in and jostle
  if(clash>0&&u.back<130){const k=Math.sin(t*9+i*1.7)*6*clash;x+=Math.cos(q.ang)*(14*clash)+k;y+=Math.sin(q.ang)*(14*clash)+Math.cos(t*7+i)*5*clash}
  const vis=Math.max(0,Math.min(1,(d+20)/30));const lost=clash>0&&u.back<60&&(i+side)%3==0?1-.6*Math.min(1,clash*1.5):1;
  return{x,y,ang:q.ang,type:u.type,a:vis*lost}})}
function shape(ctx,type,x,y,ang,s){ctx.beginPath();if(type=='inf'){ctx.save();ctx.translate(x,y);ctx.rotate(ang);ctx.rect(-s,-s,2*s,2*s);ctx.restore()}
 else if(type=='arc'){ctx.arc(x,y,s,0,7)}else{const c=Math.cos(ang),sn=Math.sin(ang);const P=[[s*1.35,0],[-s*.9,-s*1.05],[-s*.9,s*1.05]].map(([u,v])=>[x+u*c-v*sn,y+u*sn+v*c]);ctx.moveTo(...P[0]);ctx.lineTo(...P[1]);ctx.lineTo(...P[2]);ctx.closePath()}}
const T={reveal:[0,1.1],labels:[.9,.9],march:[1.6,2.7],clash:[4.3,1.2]};
window.DUR=6.5;
'''
# ---------- 1. SIMPLE MAP ----------
page('map_simple','#a9d4ef',GEO+r'''
window.render=t=>{X.fillStyle='#a9d4ef';X.fillRect(0,0,1080,1920);
 const rv=eio(pr(t,...T.reveal));X.save();X.translate(CX,CY);X.scale(.85+.15*rv,.85+.15*rv);X.translate(-CX,-CY);X.globalAlpha=Math.min(1,rv*1.5);
 // shallow water band + land
 landPath(X,1.05);X.fillStyle='#c4e3f5';X.fill();
 landPath(X);X.fillStyle='#e8eed1';X.fill();X.lineWidth=5;X.strokeStyle='#7fb07a';X.stroke();
 // forests
 X.fillStyle='#8cc27e';[...FOREST,...FOREST2].forEach(([x,y],i)=>{X.beginPath();X.arc(x,y,22+(i%3)*4,0,7);X.fill()});
 X.fillStyle='#6fa863';[...FOREST,...FOREST2].forEach(([x,y],i)=>{if(i%2){X.beginPath();X.arc(x+6,y+4,12,0,7);X.fill()}});
 // mountains
 MOUNTAINS.forEach(([x,y,s])=>{X.fillStyle='#b9ab95';X.beginPath();X.moveTo(x-s,y+s*.6);X.lineTo(x,y-s);X.lineTo(x+s,y+s*.6);X.fill();X.fillStyle='#fff';X.beginPath();X.moveTo(x-s*.3,y-s*.4);X.lineTo(x,y-s);X.lineTo(x+s*.3,y-s*.4);X.fill()});
 // river
 X.strokeStyle='#6fb6e2';X.lineWidth=10;X.lineCap='round';X.lineJoin='round';smooth(X,RIVER);X.stroke();
 X.restore();X.globalAlpha=1;
 // cities + labels
 const la=eo(pr(t,...T.labels));CITIES.forEach(([n,x,y],i)=>{const a=eo(pr(t,T.labels[0]+i*.1,.4));X.globalAlpha=a;X.fillStyle='#fff';X.beginPath();X.arc(x,y,13,0,7);X.fill();X.lineWidth=6;X.strokeStyle='#33363d';X.stroke();
  const L=n=='Harrowmere'?[x-28,y+10,'right']:[x,y-26,'center'];X.font='700 34px Inter';X.textAlign=L[2];X.lineWidth=8;X.strokeStyle='rgba(255,255,255,.9)';X.strokeText(n,L[0],L[1]);X.fillStyle='#33363d';X.fillText(n,L[0],L[1])});X.globalAlpha=1;
 X.font='italic 600 30px Lora';X.fillStyle='rgba(60,110,150,.8)';X.fillText('The Grey Sea',180,380);X.fillText('Bay of Salt',920,1700);X.fillStyle='rgba(110,95,70,.85)';X.fillText('Spine Mountains',330,800);X.textAlign='left';
 // clash
 const cp=pr(t,...T.clash);if(cp>0){const [x,y]=CLASH;const s=eob(Math.min(1,cp*2.2));X.save();X.translate(x,y);X.rotate(t*.6);X.globalAlpha=.85;X.fillStyle='#ffcf33';X.beginPath();for(let k=0;k<24;k++){const r=k%2?40:95;const a=k/24*Math.PI*2;X.lineTo(Math.cos(a)*r*s,Math.sin(a)*r*s)}X.closePath();X.fill();X.lineWidth=6;X.strokeStyle='#e0453a';X.stroke();X.restore();X.globalAlpha=1;}
 // armies (formations)
 const mp=eio(pr(t,...T.march));
 [[ROUTE_A,'#2f6fdc','BLUE',0],[ROUTE_B,'#e0453a','RED',1]].forEach(([R,c,lab,k])=>{
  if(mp>0){const s=seg(R,mp*.96);X.strokeStyle=c+'55';X.lineWidth=8;X.setLineDash([4,14]);X.lineCap='round';smooth(X,s.pts);X.stroke();X.setLineDash([])}
  armyUnits(R,mp,k,t).forEach(u=>{if(u.a<=0)return;X.globalAlpha=u.a;shape(X,u.type,u.x,u.y,u.ang,15);X.fillStyle=c;X.fill();X.lineWidth=3;X.strokeStyle='#fff';X.stroke()});X.globalAlpha=1;
  const [sx,sy]=R[0];X.fillStyle=c;X.beginPath();X.roundRect(sx-88,sy+(k?24:-120),176,48,12);X.fill();X.fillStyle='#fff';X.font='800 26px Inter';X.textAlign='center';X.fillText(lab+' ARMY',sx,sy+(k?57:-87));X.textAlign='left'});
 // legend
 X.fillStyle='rgba(255,255,255,.95)';X.beginPath();X.roundRect(60,1730,960,110,24);X.fill();X.font='600 30px Inter';X.fillStyle='#33363d';
 [['cav','Cavalry',150],['arc','Archers',440],['inf','Infantry',720]].forEach(([ty,n,x])=>{shape(X,ty,x,1785,0,13);X.fillStyle='#6b7280';X.fill();X.fillStyle='#33363d';X.fillText(n,x+30,1796)});
 {const cp2=pr(t,...T.clash);if(cp2>0){const [x,y]=CLASH;X.fillStyle='#33363d';X.font='900 46px Inter';X.textAlign='center';X.globalAlpha=eo(pr(t,4.6,.4));X.lineWidth=10;X.strokeStyle='#fff';X.strokeText('BATTLE',x+170,y-90);X.fillText('BATTLE',x+170,y-90);X.globalAlpha=1;X.textAlign='left'}}
 // title
 X.fillStyle='#fff';X.beginPath();X.roundRect(60,90,960,150,30);X.fill();X.fillStyle='#33363d';X.font='800 64px Inter';X.fillText('The March on Ashford',100,170);X.fillStyle='#7a8190';X.font='500 32px Inter';X.fillText('Two armies meet at the river crossing',100,218)};
''')
# ---------- 2. MODERN TACTICAL MAP ----------
page('map_modern','#070b10',GEO+r'''
// height field for contours
const H=(x,y)=>{const dx=(x-CX)/400,dy=(y-CY)/600;const a=Math.atan2(dy,dx);const r=Math.hypot(dx,dy)/coastR(a);let h=Math.max(0,1-r);
 MOUNTAINS.forEach(([mx,my,s])=>{h+=1.1*Math.exp(-((x-mx)**2+(y-my)**2)/(2*(s*2.2)**2))});h+=.25*Math.sin(x/70)*Math.cos(y/90)*Math.max(0,1-r);return r<1?h:-.1};
const G=10,W=108,HH=192;const field=new Float32Array((W+1)*(HH+1));for(let j=0;j<=HH;j++)for(let i=0;i<=W;i++)field[j*(W+1)+i]=H(i*G,j*G);
const contourCanvas=document.createElement('canvas');contourCanvas.width=1080;contourCanvas.height=1920;const C=contourCanvas.getContext('2d');
C.lineWidth=1.4;for(let lv=.08;lv<2.2;lv+=.12){C.strokeStyle=lv>.9?'rgba(120,200,190,.55)':'rgba(70,150,150,.38)';C.beginPath();
 for(let j=0;j<HH;j++)for(let i=0;i<W;i++){const v=[field[j*(W+1)+i],field[j*(W+1)+i+1],field[(j+1)*(W+1)+i+1],field[(j+1)*(W+1)+i]];const P=[[i*G,j*G],[(i+1)*G,j*G],[(i+1)*G,(j+1)*G],[i*G,(j+1)*G]];const pts=[];
  for(let k=0;k<4;k++){const a=v[k],b=v[(k+1)%4];if((a<lv)!==(b<lv)){const f=(lv-a)/(b-a);pts.push([P[k][0]+(P[(k+1)%4][0]-P[k][0])*f,P[k][1]+(P[(k+1)%4][1]-P[k][1])*f])}}
  if(pts.length>=2){C.moveTo(...pts[0]);C.lineTo(...pts[1])}if(pts.length==4){C.moveTo(...pts[2]);C.lineTo(...pts[3])}}C.stroke()}
const unit=(x,y,c,lab,sub)=>{X.save();X.translate(x,y);X.fillStyle='rgba(7,11,16,.85)';X.fillRect(-46,-30,92,60);X.lineWidth=4;X.strokeStyle=c;X.strokeRect(-46,-30,92,60);X.beginPath();X.moveTo(-46,-30);X.lineTo(46,30);X.moveTo(46,-30);X.lineTo(-46,30);X.lineWidth=3;X.stroke();
 X.fillStyle=c;X.font='700 22px "DejaVu Sans Mono"';X.textAlign='center';X.fillText(lab,0,-42);X.font='500 18px "DejaVu Sans Mono"';X.fillText(sub,0,52);X.restore();X.textAlign='left'};
window.render=t=>{X.fillStyle='#070b10';X.fillRect(0,0,1080,1920);
 // grid
 X.strokeStyle='rgba(90,140,170,.12)';X.lineWidth=1;for(let x=0;x<=1080;x+=60){X.beginPath();X.moveTo(x,0);X.lineTo(x,1920);X.stroke()}for(let y=0;y<=1920;y+=60){X.beginPath();X.moveTo(0,y);X.lineTo(1080,y);X.stroke()}
 const rv=eio(pr(t,...T.reveal));X.save();X.beginPath();X.rect(0,0,1080,1920*rv);X.clip();
 landPath(X);X.fillStyle='#101b24';X.fill();X.drawImage(contourCanvas,0,0);landPath(X);X.lineWidth=3;X.strokeStyle='rgba(120,220,210,.9)';X.stroke();
 X.strokeStyle='rgba(80,170,255,.8)';X.lineWidth=4;smooth(X,RIVER);X.stroke();
 // roads
 X.setLineDash([10,10]);X.strokeStyle='rgba(200,210,220,.35)';X.lineWidth=3;[[CITIES[0],CITIES[4]],[CITIES[4],CITIES[2]],[CITIES[1],CITIES[3]],[CITIES[0],CITIES[1]]].forEach(([a,b])=>{X.beginPath();X.moveTo(a[1],a[2]);X.lineTo(b[1],b[2]);X.stroke()});X.setLineDash([]);
 X.restore();
 // scan line
 if(rv<1){X.fillStyle='rgba(120,240,220,.8)';X.fillRect(0,1920*rv,1080,3)}
 // city markers
 CITIES.forEach(([n,x,y],i)=>{const a=eo(pr(t,T.labels[0]+i*.1,.4));X.globalAlpha=a;X.strokeStyle='#cfe8ef';X.lineWidth=3;X.strokeRect(x-9,y-9,18,18);X.fillStyle='#cfe8ef';X.font='600 24px "DejaVu Sans Mono"';X.fillText(n.toUpperCase(),x+18,y+8)});X.globalAlpha=1;
 // contact
 const cp=pr(t,...T.clash);if(cp>0){const [x,y]=CLASH;for(let k=0;k<3;k++){const r=((cp*2.4+k*.33)%1);X.strokeStyle=`rgba(255,200,80,${1-r})`;X.lineWidth=4;X.beginPath();X.arc(x,y,20+r*160,0,7);X.stroke()}
  X.fillStyle='#ffc850';X.beginPath();X.arc(x,y,12,0,7);X.fill();}
 // formations
 const mp=eio(pr(t,...T.march));
 [[ROUTE_A,'#4fb3ff','1ST BDE · BLUFOR',0],[ROUTE_B,'#ff4d5e','3RD REGT · OPFOR',1]].forEach(([R,c,lab,k])=>{
  if(mp>0){const s=seg(R,mp*.96);X.save();X.strokeStyle=c;X.globalAlpha=.45;X.lineWidth=4;X.setLineDash([16,12]);X.lineDashOffset=-t*60;smooth(X,s.pts);X.stroke();X.restore()}
  X.save();X.shadowColor=c;X.shadowBlur=14;armyUnits(R,mp,k,t).forEach(u=>{if(u.a<=0)return;X.globalAlpha=u.a;shape(X,u.type,u.x,u.y,u.ang,14);X.fillStyle='rgba(7,11,16,.85)';X.fill();X.lineWidth=3.5;X.strokeStyle=c;X.stroke()});X.restore();X.globalAlpha=1;
  const [sx,sy]=R[0];X.fillStyle=c;X.font='700 22px "DejaVu Sans Mono"';X.textAlign='center';X.fillText(lab,sx,sy+(k?62:-48));X.textAlign='left'});
 {const cp2=pr(t,...T.clash);if(cp2>0){const [x0,y0]=CLASH;const x=x0+60,y=y0-60;X.globalAlpha=eo(pr(t,4.5,.3));X.fillStyle='rgba(7,11,16,.85)';X.fillRect(x+40,y-80,300,92);X.strokeStyle='#ffc850';X.lineWidth=2;X.strokeRect(x+40,y-80,300,92);
  X.fillStyle='#ffc850';X.font='700 30px "DejaVu Sans Mono"';X.fillText('▲ CONTACT',x+58,y-40);X.font='500 20px "DejaVu Sans Mono"';X.fillText('GRID 41T 6012 1120',x+58,y-10);X.globalAlpha=1}}
 // HUD
 X.fillStyle='rgba(7,11,16,.9)';X.fillRect(0,0,1080,250);X.fillStyle='#cfe8ef';X.font='800 54px Inter';X.fillText('OPERATION ASHFORD',60,130);X.fillStyle='#7fa3b4';X.font='500 24px "DejaVu Sans Mono"';
 X.fillText('T+'+String(Math.floor(t*60)).padStart(3,'0')+'H   SCALE 1:250,000   SECTOR 7',60,185);
 X.strokeStyle='#4fb3ff';X.lineWidth=4;[[40,40,1,1],[1040,40,-1,1],[40,1880,1,-1],[1040,1880,-1,-1]].forEach(([x,y,a,b])=>{X.beginPath();X.moveTo(x,y+60*b);X.lineTo(x,y);X.lineTo(x+60*a,y);X.stroke()});
 X.font='500 22px "DejaVu Sans Mono"';X.fillStyle='#4fb3ff';X.fillText('■ BLUFOR',60,1790);X.fillStyle='#ff4d5e';X.fillText('■ OPFOR',220,1790);
 X.strokeStyle='#cfe8ef';X.lineWidth=3;[['cav','CAV',90],['arc','ARCH',300],['inf','INF',520]].forEach(([ty,n,x])=>{shape(X,ty,x,1840,0,11);X.stroke();X.fillStyle='#cfe8ef';X.fillText(n,x+24,1848)})};
''')
# ---------- 3. FANTASY (old parchment) MAP ----------
page('map_fantasy','#e9d6ab',GEO+r'''
const INK='#3a2a1a',RED='#8e1f14';
// parchment
const pc=document.createElement('canvas');pc.width=1080;pc.height=1920;const P=pc.getContext('2d');const pr2=rng(3);
const g=P.createRadialGradient(540,960,300,540,960,1150);g.addColorStop(0,'#f1e2bb');g.addColorStop(.7,'#e2c98f');g.addColorStop(1,'#a8834b');P.fillStyle=g;P.fillRect(0,0,1080,1920);
for(let i=0;i<9000;i++){P.fillStyle=`rgba(90,60,25,${pr2()*.06})`;P.fillRect(pr2()*1080,pr2()*1920,2+pr2()*30,1)}for(let i=0;i<40;i++){P.fillStyle=`rgba(110,70,30,${pr2()*.06})`;P.beginPath();P.arc(pr2()*1080,pr2()*1920,20+pr2()*90,0,7);P.fill()}
const ink=(a=1)=>`rgba(58,42,26,${a})`;
function mountain(x,y,s){X.fillStyle='#e8d3a4';X.beginPath();X.moveTo(x-s,y+s*.55);X.quadraticCurveTo(x-s*.35,y-s*.2,x,y-s);X.quadraticCurveTo(x+s*.4,y-s*.1,x+s,y+s*.55);X.closePath();X.fill();
 X.strokeStyle=ink();X.lineWidth=2.6;X.beginPath();X.moveTo(x-s,y+s*.55);X.quadraticCurveTo(x-s*.35,y-s*.2,x,y-s);X.quadraticCurveTo(x+s*.4,y-s*.1,x+s,y+s*.55);X.stroke();
 X.lineWidth=1.4;for(let k=1;k<6;k++){const u=k/6;X.beginPath();X.moveTo(x+s*u*.9,y-s+s*1.55*u*.6);X.lineTo(x+s*u*.55,y+s*.5);X.stroke()}
 X.beginPath();X.moveTo(x,y-s);X.lineTo(x+s*.08,y+s*.3);X.stroke()}
function tree(x,y,s){X.fillStyle='#e3cd99';X.strokeStyle=ink();X.lineWidth=1.8;X.beginPath();X.arc(x,y-s,s*.75,0,7);X.fill();X.stroke();X.beginPath();X.moveTo(x,y-s*.3);X.lineTo(x,y+s*.4);X.stroke()}
function castle(x,y){X.fillStyle='#ead8ac';X.strokeStyle=ink();X.lineWidth=2.4;X.beginPath();X.rect(x-20,y-16,40,22);X.fill();X.stroke();[-20,10].forEach(dx=>{X.beginPath();X.rect(x+dx,y-34,10,18);X.fill();X.stroke()});X.beginPath();X.moveTo(x+15,y-34);X.lineTo(x+15,y-50);X.lineTo(x+28,y-45);X.lineTo(x+15,y-40);X.stroke()}
function compass(x,y,r,rot){X.save();X.translate(x,y);X.rotate(rot);X.strokeStyle=ink();X.lineWidth=2;X.beginPath();X.arc(0,0,r,0,7);X.stroke();X.beginPath();X.arc(0,0,r*.85,0,7);X.stroke();
 for(let k=0;k<8;k++){const a=k*Math.PI/4,L=k%2?r*.55:r;X.fillStyle=k%2?'#e8d3a4':INK;X.beginPath();X.moveTo(Math.cos(a)*L,Math.sin(a)*L);X.lineTo(Math.cos(a+Math.PI/2)*r*.12,Math.sin(a+Math.PI/2)*r*.12);X.lineTo(0,0);X.fill();X.stroke()}
 X.restore();X.fillStyle=INK;X.font='700 34px Lora';X.textAlign='center';X.fillText('N',x,y-r-10);X.textAlign='left'}
function banner(x,y,c,flip){X.save();X.translate(x,y);X.strokeStyle=ink();X.lineWidth=3;X.beginPath();X.moveTo(0,0);X.lineTo(0,-70);X.stroke();X.fillStyle=c;X.beginPath();X.moveTo(0,-70);X.lineTo(flip?-46:46,-60);X.lineTo(flip?-36:36,-48);X.lineTo(flip?-46:46,-36);X.lineTo(0,-40);X.closePath();X.fill();X.stroke();X.restore()}
window.render=t=>{X.drawImage(pc,0,0);
 const rv=eio(pr(t,...T.reveal));X.save();X.beginPath();X.arc(CX,CY,1300*rv,0,7);X.clip();
 // coast ripple lines
 for(let k=4;k>=1;k--){landPath(X,1+k*.022);X.strokeStyle=ink(.12+.05*(4-k));X.lineWidth=1.6;X.stroke()}
 landPath(X);X.fillStyle='rgba(240,225,185,.55)';X.fill();X.strokeStyle=ink();X.lineWidth=3.2;X.stroke();
 // river
 X.strokeStyle=ink(.85);X.lineWidth=3;smooth(X,RIVER);X.stroke();X.lineWidth=1.2;X.save();X.translate(5,3);smooth(X,RIVER);X.stroke();X.restore();
 // forests, mountains (sorted by y for overlap)
 [...FOREST,...FOREST2].sort((a,b)=>a[1]-b[1]).forEach(([x,y],i)=>tree(x,y+18,14+(i%3)*3));
 [...MOUNTAINS].sort((a,b)=>a[1]-b[1]).forEach(([x,y,s])=>mountain(x,y,s*1.05));
 CITIES.forEach(([n,x,y])=>castle(x,y));
 X.restore();
 // labels
 const la=eo(pr(t,...T.labels));X.globalAlpha=la;X.fillStyle=INK;X.textAlign='center';
 CITIES.forEach(([n,x,y])=>{X.font='600 italic 34px Lora';X.fillText(n,x,y+42)});
 X.font='italic 500 44px Lora';X.save();X.translate(300,760);X.rotate(1.1);X.fillText('T h e   S p i n e',0,0);X.restore();
 X.font='italic 500 34px Lora';X.fillText('Greywood',700,600);X.fillText('Fen of Whispers',330,1100);
 X.font='italic 600 40px Lora';X.fillStyle=ink(.6);X.fillText('The Grey Sea',190,350);X.fillText('Bay of Salt',900,1720);X.textAlign='left';X.globalAlpha=1;
 // routes (red ink dotted) + banners
 const mp=eio(pr(t,...T.march));[[ROUTE_A,'#2c4a7a',0],[ROUTE_B,RED,1]].forEach(([R,c,k])=>{if(mp<=0)return;const s=seg(R,mp*.96);X.strokeStyle=c;X.lineWidth=5;X.setLineDash([2,14]);X.lineCap='round';smooth(X,s.pts);X.stroke();X.setLineDash([]);
  const [hx,hy]=s.head;banner(hx,hy,c,k==1);});
 // clash: crossed swords
 const cp=pr(t,...T.clash);if(cp>0){const [x,y]=CLASH;const s=eob(Math.min(1,cp*2));X.save();X.translate(x,y-20);X.scale(s,s);X.strokeStyle=INK;X.lineWidth=5;
  [-1,1].forEach(d=>{X.save();X.rotate(d*.75);X.beginPath();X.moveTo(0,-70);X.lineTo(0,50);X.stroke();X.beginPath();X.moveTo(-20,30);X.lineTo(20,30);X.stroke();X.fillStyle=INK;X.beginPath();X.arc(0,60,7,0,7);X.fill();X.restore()});X.restore();
  X.globalAlpha=eo(pr(t,4.6,.5));X.fillStyle=RED;X.font='italic 700 40px Lora';X.textAlign='center';X.fillText('Battle of the Ford',x,y+90);X.font='italic 500 26px Lora';X.fillStyle=INK;X.fillText('in the Year of Ash',x,y+124);X.textAlign='left';X.globalAlpha=1}
 // cartouche title + compass + border
 X.fillStyle='rgba(240,225,185,.9)';X.strokeStyle=ink();X.lineWidth=3;X.beginPath();X.roundRect(140,90,800,170,20);X.fill();X.stroke();X.beginPath();X.roundRect(152,102,776,146,14);X.stroke();
 X.fillStyle=INK;X.textAlign='center';X.font='700 66px Lora';X.fillText('The Westmarch',540,180);X.font='italic 400 30px Lora';X.fillText('wherein the hosts met at the ford',540,226);X.textAlign='left';
 compass(170,1640,70,Math.sin(t*.6)*.05);
 X.strokeStyle=ink(.9);X.lineWidth=5;X.strokeRect(24,24,1032,1872);X.lineWidth=1.5;X.strokeRect(38,38,1004,1844)};
''')
