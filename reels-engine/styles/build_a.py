from mk import page
CANVAS='const cv=document.createElement("canvas");cv.width=1080;cv.height=1920;document.body.prepend(cv);const X=cv.getContext("2d");\n'
# ---------- PARTICLE ART ----------
page('particle','#05040c',CANVAS+r'''
// target points from text
const tc=document.createElement('canvas');tc.width=1080;tc.height=1920;const tx=tc.getContext('2d');
tx.fillStyle='#fff';tx.font='900 250px Inter';tx.textAlign='center';tx.fillText('BUILD',540,1010);
const d=tx.getImageData(0,0,1080,1920).data;const pts=[];for(let y=0;y<1920;y+=7)for(let x=0;x<1080;x+=7)if(d[(y*1080+x)*4+3]>128)pts.push([x,y]);
const r=rng(11);const N=7000;const P=[];
for(let i=0;i<N;i++){const tg=pts[i%pts.length];P.push({u:r(),v:r(),s:r(),tx:tg[0]+(r()-.5)*4,ty:tg[1]+(r()-.5)*4,c:r()})}
const col=c=>c<.33?[90,220,255]:c<.66?[255,110,200]:[255,214,110];
window.DUR=4.5;
window.render=t=>{X.fillStyle='#05040c';X.fillRect(0,0,1080,1920);X.globalCompositeOperation='lighter';
 const m=eio(pr(t,1.6,1.6));
 for(const p of P){const a=p.u*Math.PI*2+t*0.6;const rib=Math.sin(p.u*6.28*2+t*1.2);
  const fx=540+Math.cos(a)*(260+p.v*220)+Math.sin(t+p.s*6)*30, fy=960+rib*240+Math.sin(a*2)*(180+p.v*120);
  const x=lerp(fx,p.tx,m),y=lerp(fy,p.ty,m);const [cr,cg,cb]=col((p.c+t*.05)%1);
  const al=.6+.4*Math.sin(t*3+p.s*20)**2;X.fillStyle=`rgba(${cr},${cg},${cb},${al})`;const sz=1.8+p.s*2.8;X.fillRect(x,y,sz,sz)}
 X.globalCompositeOperation='source-over';
 X.fillStyle=`rgba(255,255,255,${.85*eo(pr(t,3.2,.6))})`;X.font='500 34px Inter';X.textAlign='center';X.fillText('— one particle at a time —',540,1110)};
''')
# ---------- STAINED GLASS ----------
page('stained_glass','#120a06',CANVAS+r'''
const r=rng(21);const jewel=['#c1121f','#1d4ed8','#f4a300','#0f766e','#7c3aed','#e85d04','#2563eb','#15803d'];
const cells=[];const CX=540,CY=640,RAD=400;
const rings=[[0,70,1],[70,150,8],[150,240,16],[240,330,16],[330,400,24]];
rings.forEach(([a,b,n],ri)=>{for(let k=0;k<n;k++){cells.push({r0:a,r1:b,a0:k/n*Math.PI*2,a1:(k+1)/n*Math.PI*2,c:jewel[(k+ri*3)%jewel.length],ph:r()*6})}});
const motes=[...Array(160)].map(()=>({x:r(),y:r(),s:r()}));
window.DUR=4;
window.render=t=>{X.fillStyle='#120a06';X.fillRect(0,0,1080,1920);
 const pulse=.75+.25*Math.sin(t*1.5);
 // rays
 X.save();X.globalCompositeOperation='lighter';
 [['#c1121f',-220],['#1d4ed8',-110],['#f4a300',0],['#0f766e',110],['#7c3aed',220]].forEach(([c,o],i)=>{const g=X.createLinearGradient(0,CY,0,1920);g.addColorStop(0,c+'66');g.addColorStop(1,c+'00');X.fillStyle=g;X.globalAlpha=.55*pulse*eo(pr(t,.8,1));X.beginPath();X.moveTo(CX+o*.6,CY);X.lineTo(CX+o*1.6-120,1920);X.lineTo(CX+o*1.6+120,1920);X.closePath();X.fill()});
 X.globalAlpha=1;motes.forEach(m=>{const y=((m.y*1300+CY+t*40*(.3+m.s))%1300)+CY;X.fillStyle=`rgba(255,230,180,${.5*m.s*eo(pr(t,1,1))})`;X.fillRect(250+m.x*580+(y-CY)*(m.x-.5)*.6,y,2.5,2.5)});X.restore();
 // stone surround
 X.fillStyle='#3b2a20';X.beginPath();X.arc(CX,CY,RAD+46,0,7);X.fill();X.fillStyle='#24180f';X.beginPath();X.arc(CX,CY,RAD+16,0,7);X.fill();
 // glass, lit in sweep
 cells.forEach((c,i)=>{const lit=eo(pr(t,i*.012,.5));X.beginPath();X.arc(CX,CY,c.r1,c.a0,c.a1);X.arc(CX,CY,c.r0,c.a1,c.a0,true);X.closePath();
  const g=X.createRadialGradient(CX,CY,c.r0,CX,CY,c.r1);g.addColorStop(0,c.c);g.addColorStop(1,'#000');X.globalAlpha=.25+.75*lit*(.85+.15*Math.sin(t*2+c.ph));X.fillStyle=c.c;X.fill();X.globalAlpha=.25;X.fillStyle=g;X.fill();X.globalAlpha=1;
  X.strokeStyle='#0d0805';X.lineWidth=9;X.stroke()});
 // petals overlay leading
 X.strokeStyle='#0d0805';X.lineWidth=10;for(let k=0;k<8;k++){const a=k/8*Math.PI*2;X.beginPath();X.ellipse(CX+Math.cos(a)*190,CY+Math.sin(a)*190,90,45,a,0,7);X.stroke()}
 // glow
 X.save();X.globalCompositeOperation='lighter';const gg=X.createRadialGradient(CX,CY,0,CX,CY,RAD*1.3);gg.addColorStop(0,`rgba(255,220,150,${.35*pulse})`);gg.addColorStop(1,'rgba(255,200,120,0)');X.fillStyle=gg;X.fillRect(0,0,1080,1300);X.restore();
 // floor caustics
 for(let i=0;i<5;i++){X.fillStyle=jewel[i]+'40';X.beginPath();X.ellipse(340+i*100,1700+Math.sin(t+i)*10,90,26,0,0,7);X.fill()}
};
''')
# ---------- NEON SIGN ----------
page('neon','#1a0f12',r'''
const s=document.getElementById('sign');window.DUR=4;
const pieces=[...document.querySelectorAll('.tube')];
window.render=t=>{pieces.forEach((p,i)=>{const on=t>.5+i*.35;const fl=on&&!(t>.5+i*.35&&t<.75+i*.35&&Math.floor(t*30)%3==0)&&!(i==1&&t>2.9&&t<3.0);p.classList.toggle('on',fl)});
 document.getElementById('glow').style.opacity=pieces.filter(p=>p.classList.contains('on')).length/pieces.length*(.9+.1*Math.sin(t*20))};
''',css=r'''
#wall{position:absolute;inset:0;background-color:#3a1e1a;background-image:linear-gradient(#25110e 6px,transparent 6px),linear-gradient(90deg,#25110e 6px,transparent 6px);background-size:180px 76px,180px 152px;background-position:0 0,90px 76px}
#wall:after{content:'';position:absolute;inset:0;background:linear-gradient(90deg,transparent 0 174px,#25110e 174px 180px) 0 76px/180px 152px repeat,radial-gradient(ellipse at center,transparent 30%,rgba(0,0,0,.75))}
#glow{position:absolute;left:90px;right:90px;top:560px;height:800px;background:radial-gradient(ellipse at center,rgba(255,60,170,.45),rgba(60,160,255,.15) 50%,transparent 70%);filter:blur(30px);opacity:0}
.tube{position:absolute;left:0;right:0;text-align:center;color:#3b2430;transition:none}
#t1{top:640px;font:italic 700 210px Lora;-webkit-text-stroke:3px #6b4050}
#t2{top:930px;font:800 150px Inter;letter-spacing:10px;-webkit-text-stroke:3px #405070}
#t3{top:1160px;font:600 60px Inter;letter-spacing:22px;-webkit-text-stroke:2px #604a30}
#t1.on{color:#ffe1f2;-webkit-text-stroke:3px #ff5ec4;text-shadow:0 0 8px #ff5ec4,0 0 24px #ff2bb0,0 0 60px #ff2bb0,0 0 120px #ff1493}
#t2.on{color:#e3f4ff;-webkit-text-stroke:3px #57c7ff;text-shadow:0 0 8px #57c7ff,0 0 24px #1aa3ff,0 0 60px #1aa3ff,0 0 120px #0080ff}
#t3.on{color:#fff6dc;-webkit-text-stroke:2px #ffcf5a;text-shadow:0 0 8px #ffcf5a,0 0 30px #ffaa00,0 0 70px #ff9900}
.wire{position:absolute;top:0;width:4px;height:600px;background:#111}''',
html='<div id="wall"></div><div class="wire" style="left:300px"></div><div class="wire" style="left:780px"></div><div id="glow"></div><div class="tube" id="t1">Keep</div><div class="tube" id="t2">BUILDING</div><div class="tube" id="t3">OPEN 24/7</div>')
# ---------- LOW POLY ----------
page('low_poly','#f6b38e',r'''
const R=new THREE.WebGLRenderer({antialias:true});R.setSize(1080,1920);document.body.prepend(R.domElement);
const sc=new THREE.Scene();sc.fog=new THREE.Fog(0xf7c6a3,18,60);
const cam=new THREE.PerspectiveCamera(55,1080/1920,.1,200);
const sky=new THREE.Mesh(new THREE.SphereGeometry(90,16,12),new THREE.ShaderMaterial({side:1,uniforms:{},vertexShader:'varying vec3 p;void main(){p=position;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}',fragmentShader:'varying vec3 p;void main(){float h=normalize(p).y;gl_FragColor=vec4(mix(vec3(.98,.75,.55),vec3(.36,.42,.78),clamp(h*2.2,0.,1.)),1.);}'}));sc.add(sky);
const geo=new THREE.PlaneGeometry(60,120,60,120);geo.rotateX(-Math.PI/2);const pos=geo.attributes.position;
const nz=(x,z)=>Math.sin(x*.35)*Math.cos(z*.3)*1.2+Math.sin(x*.9+z*.4)*.5+Math.sin(z*.15)*.8;
for(let i=0;i<pos.count;i++){const x=pos.getX(i),z=pos.getZ(i);const river=Math.sin(z*.12)*3;const dx=Math.abs(x-river);let h=Math.pow(Math.max(0,dx-2.2),1.35)*.55+nz(x,z)*Math.min(1,dx/6);if(dx<2.2)h=-.6;pos.setY(i,h+(dx>14?(dx-14)*1.2:0))}
const g2=geo.toNonIndexed();g2.computeVertexNormals();const cols=[];const p2=g2.attributes.position;
for(let i=0;i<p2.count;i+=3){const y=(p2.getY(i)+p2.getY(i+1)+p2.getY(i+2))/3;let c=y<-.3?[.35,.55,.4]:y<2?[.42,.68,.36]:y<5?[.33,.55,.32]:y<9?[.55,.47,.4]:[.95,.95,.97];for(let k=0;k<3;k++)cols.push(...c)}
g2.setAttribute('color',new THREE.Float32BufferAttribute(cols,3));
sc.add(new THREE.Mesh(g2,new THREE.MeshLambertMaterial({vertexColors:true,flatShading:true})));
const water=new THREE.Mesh(new THREE.PlaneGeometry(60,120,30,60),new THREE.MeshLambertMaterial({color:0x4fa3d9,flatShading:true,transparent:true,opacity:.92}));water.rotation.x=-Math.PI/2;water.position.y=-.35;sc.add(water);
const r=rng(4);for(let i=0;i<70;i++){const z=-r()*100+20,side=r()>.5?1:-1,x=Math.sin(z*.12)*3+side*(3+r()*6);const tr=new THREE.Mesh(new THREE.ConeGeometry(.45,1.6,5),new THREE.MeshLambertMaterial({color:0x2f6b3a,flatShading:true}));tr.position.set(x,nz(x,z)*.3+.8,z);sc.add(tr)}
const sun=new THREE.Mesh(new THREE.IcosahedronGeometry(4,0),new THREE.MeshBasicMaterial({color:0xffe08a}));sun.position.set(0,9,-70);sc.add(sun);
sc.add(new THREE.HemisphereLight(0xffe6c8,0x5a7a50,1.2));const dl=new THREE.DirectionalLight(0xffd29a,2.2);dl.position.set(-5,6,-10);sc.add(dl);
const wp=water.geometry.attributes.position;const w0=Float32Array.from(wp.array);
window.DUR=4;
window.render=t=>{const z=14-t*2.2;cam.position.set(Math.sin(z*.12)*3+.5,3.2+Math.sin(t*.8)*.2,z);cam.lookAt(Math.sin((z-12)*.12)*3,1.2,z-14);
 for(let i=0;i<wp.count;i++)wp.setZ(i,w0[i*3+2]+Math.sin(w0[i*3]*1.3+t*2+w0[i*3+1])*.08);wp.needsUpdate=true;sun.rotation.z=t*.2;R.render(sc,cam)};
''')
