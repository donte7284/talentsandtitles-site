from mk import page
COMMON_CAM='''
const R=new THREE.WebGLRenderer({antialias:true,preserveDrawingBuffer:true});R.setSize(1080,1920);document.body.prepend(R.domElement);
const sc=new THREE.Scene();const cam=new THREE.PerspectiveCamera(42,1080/1920,0.1,100);
function camAt(t,rad=11.5,h=5.2){const a=0.55+t*0.06;cam.position.set(Math.sin(a)*rad,h,Math.cos(a)*rad*0.95);cam.lookAt(0,1.9,-1.2);}
'''
# ---------- THERMAL ----------
page('thermal','#000',COMMON_CAM+'''
const HEAT={monitor:.75,screen:.95,bar1:.9,bar2:.9,bar3:.9,lamp:.6,lampShade:1.0,mug:1.0,keyboard:.55,chair:.35,chairSeat:.45,plant:.25,pot:.2,window:.05,frame:.1,floor:.15,wall:.12,desk:.3,deskLeg:.2,cabinet:.18,cabinetLine:.2,shelf:.15,book0:.2,book1:.2,book2:.2,clock:.25,clockHand:.3};
const vs=`varying vec3 vN;varying vec3 vW;void main(){vN=normalize(normalMatrix*normal);vec4 w=modelMatrix*vec4(position,1.);vW=w.xyz;gl_Position=projectionMatrix*viewMatrix*w;}`;
const fs=`uniform float heat;uniform float time;varying vec3 vN;varying vec3 vW;
vec3 pal(float x){x=clamp(x,0.,1.);vec3 c0=vec3(.02,.0,.08),c1=vec3(.28,.0,.5),c2=vec3(.75,.05,.45),c3=vec3(.98,.35,.05),c4=vec3(1.,.85,.1),c5=vec3(1.,1.,.9);
 if(x<.2)return mix(c0,c1,x/.2);if(x<.4)return mix(c1,c2,(x-.2)/.2);if(x<.6)return mix(c2,c3,(x-.4)/.2);if(x<.8)return mix(c3,c4,(x-.6)/.2);return mix(c4,c5,(x-.8)/.2);}
float h(vec3 p){return fract(sin(dot(p,vec3(12.9,78.2,37.7)))*43758.5);}
void main(){float l=.55+.45*max(dot(vN,normalize(vec3(.3,1.,.6))),0.);float x=(heat*1.1+.05)*l+.08*sin(vW.y*3.+time*2.)*heat+ (h(floor(vW*40.)+floor(time*12.))-.5)*.05;gl_FragColor=vec4(pal(x),1.);}`;
const mats=[];const mat=n=>{const m=new THREE.ShaderMaterial({vertexShader:vs,fragmentShader:fs,uniforms:{heat:{value:HEAT[n]??.3},time:{value:0}}});mats.push(m);return m};
const o=buildOffice(THREE,mat);sc.add(o.group);
window.DUR=4;
window.render=t=>{camAt(t,10.5,4.6);mats.forEach(m=>m.uniforms.time.value=t);o.hand.rotation.z=-t;
 document.getElementById('temp').textContent=(36.4+Math.sin(t*3)*0.6).toFixed(1)+'°C';
 document.getElementById('tc').textContent=String(Math.floor(t*30)).padStart(5,'0');R.render(sc,cam)};
''',css='''.hud{position:absolute;color:#fff;font:600 30px 'DejaVu Sans Mono',monospace;letter-spacing:3px;text-shadow:0 0 6px #000}
#cross{position:absolute;left:490px;top:910px;width:100px;height:100px;border:3px solid rgba(255,255,255,.8)}
#cross:before,#cross:after{content:'';position:absolute;background:#fff;left:48px;top:-40px;width:3px;height:180px}#cross:after{left:-40px;top:48px;width:180px;height:3px}
.scale{position:absolute;right:60px;top:520px;width:36px;height:880px;background:linear-gradient(#fffbe6,#ffd91a,#fa5a0d,#bf0d73,#470080,#050014);border:2px solid #fff}''',
html='''<div class="hud" style="left:60px;top:80px">● REC  THERMAL · IR-7</div><div class="hud" id="tc" style="right:60px;top:80px">00000</div>
<div id="cross"></div><div class="hud" id="temp" style="left:610px;top:860px;font-size:40px">36.4°C</div>
<div class="scale"></div><div class="hud" style="right:110px;top:505px">42°</div><div class="hud" style="right:110px;top:1380px">18°</div>''')

# ---------- HOLOGRAM ----------
page('hologram','#020a14',COMMON_CAM+'''
import {EffectComposer} from 'three/addons/postprocessing/EffectComposer.js';import {RenderPass} from 'three/addons/postprocessing/RenderPass.js';import {UnrealBloomPass} from 'three/addons/postprocessing/UnrealBloomPass.js';
const fill=new THREE.MeshBasicMaterial({color:0x0aa6ff,transparent:true,opacity:.025,depthWrite:false,blending:THREE.AdditiveBlending});
const mat=n=>fill;
const o=buildOffice(THREE,mat);
o.group.children.forEach(m=>{if(m.geometry){const e=new THREE.LineSegments(new THREE.EdgesGeometry(m.geometry,25),new THREE.LineBasicMaterial({color:0x5fe3ff,transparent:true,opacity:.9}));m.add(e);}});
const floorGrid=new THREE.GridHelper(14,28,0x2ad0ff,0x0b5a8a);floorGrid.position.y=0.01;sc.add(floorGrid);
sc.add(o.group);
// projector ring
const ring=new THREE.Mesh(new THREE.RingGeometry(4.3,4.4,96),new THREE.MeshBasicMaterial({color:0x5fe3ff,side:2,transparent:true,opacity:.7}));ring.rotation.x=-Math.PI/2;ring.position.y=.02;sc.add(ring);
const ring2=ring.clone();ring2.scale.setScalar(.8);sc.add(ring2);
const comp=new EffectComposer(R);comp.addPass(new RenderPass(sc,cam));comp.addPass(new UnrealBloomPass(new THREE.Vector2(1080,1920),.7,.4,.1));
const scan=new THREE.Mesh(new THREE.PlaneGeometry(9,.06),new THREE.MeshBasicMaterial({color:0x9ff3ff,transparent:true,opacity:.8}));scan.rotation.x=-Math.PI/2;sc.add(scan);
window.DUR=4;
window.render=t=>{camAt(t,9.4,4.6);const rev=eio(pr(t,0,2.2));
 o.group.children.forEach(m=>{const y=m.position.y;m.visible=y<rev*5.2;});
 scan.position.set(0,rev*5.2,-0.5);scan.visible=rev<1;
 ring.rotation.z=t;ring2.rotation.z=-t*1.4;
 const fl=0.85+0.15*Math.sin(t*37)*Math.sin(t*13);R.domElement.style.opacity=fl;
 o.hand.rotation.z=-t;comp.render()};
''',css='''#scan{position:absolute;inset:0;background:repeating-linear-gradient(0deg,rgba(0,0,0,.25) 0 2px,transparent 2px 6px);pointer-events:none}
.t{position:absolute;color:#7fe9ff;font:600 28px 'DejaVu Sans Mono',monospace;letter-spacing:4px;text-shadow:0 0 12px #0af}''',
html='''<div id="scan"></div><div class="t" style="left:70px;top:90px">OFFICE // FLOOR 12</div><div class="t" style="right:70px;top:90px">PROJECTION 98%</div><div class="t" style="left:70px;bottom:120px">EMPLOYEE_842 · ACTIVE</div>''')

# ---------- CYBERPUNK ----------
page('cyberpunk','#07020f',COMMON_CAM+'''
import {EffectComposer} from 'three/addons/postprocessing/EffectComposer.js';import {RenderPass} from 'three/addons/postprocessing/RenderPass.js';import {UnrealBloomPass} from 'three/addons/postprocessing/UnrealBloomPass.js';
const NE={screen:0x00f0ff,bar1:0xff2bd6,bar2:0x00f0ff,bar3:0xffe600,lampShade:0xff2bd6,window:0x5a0fa0,keyboard:0x00f0ff,clock:0xff2bd6};
const mat=n=>NE[n]!==undefined?new THREE.MeshBasicMaterial({color:NE[n]}):new THREE.MeshStandardMaterial({color:0x1a1030,roughness:.35,metalness:.6});
const o=buildOffice(THREE,mat);sc.add(o.group);
o.group.children.forEach((m,i)=>{if(m.geometry&&!NE[Object.keys(o.parts).find(k=>o.parts[k].includes(m))]){const e=new THREE.LineSegments(new THREE.EdgesGeometry(m.geometry,30),new THREE.LineBasicMaterial({color:i%2?0xff2bd6:0x00f0ff,transparent:true,opacity:.55}));m.add(e)}});
sc.add(new THREE.AmbientLight(0x30104a,1.5));
const p1=new THREE.PointLight(0xff2bd6,40,12);p1.position.set(-2,3.5,1);sc.add(p1);const p2=new THREE.PointLight(0x00f0ff,40,12);p2.position.set(2.5,2.5,0);sc.add(p2);
// neon strip on wall
const strip=new THREE.Mesh(new THREE.BoxGeometry(7.6,.06,.06),new THREE.MeshBasicMaterial({color:0xff2bd6}));strip.position.set(0,4.6,-2.85);sc.add(strip);
const strip2=new THREE.Mesh(new THREE.BoxGeometry(.06,4.6,.06),new THREE.MeshBasicMaterial({color:0x00f0ff}));strip2.position.set(-3.85,2.4,-2.85);sc.add(strip2);
// city skyline through window
const city=new THREE.Group();const r=rng(7);for(let i=0;i<14;i++){const h=.3+r()*1.3;const b=new THREE.Mesh(new THREE.BoxGeometry(.15,h,.02),new THREE.MeshBasicMaterial({color:r()>.5?0xff2bd6:0x7a2cff}));b.position.set(0.5+i*.16,2.1+h/2,-2.86);city.add(b)}sc.add(city);
const comp=new EffectComposer(R);comp.addPass(new RenderPass(sc,cam));comp.addPass(new UnrealBloomPass(new THREE.Vector2(1080,1920),1.3,.5,.15));
// rain
const rg=new THREE.BufferGeometry();const N=500;const pos=new Float32Array(N*6);const rr=rng(3);const seeds=[];for(let i=0;i<N;i++){seeds.push([rr()*10-5,rr()*8,rr()*6-2])}
rg.setAttribute('position',new THREE.BufferAttribute(pos,3));const rain=new THREE.LineSegments(rg,new THREE.LineBasicMaterial({color:0x8a6cff,transparent:true,opacity:.35}));sc.add(rain);
window.DUR=4;
window.render=t=>{camAt(t,9.6,4.2);seeds.forEach((s,i)=>{const y=((s[1]-t*9)%8+8)%8;pos.set([s[0],y,s[2],s[0]-.05,y+.4,s[2]],i*6)});rg.attributes.position.needsUpdate=true;
 const fl=t%1.3<0.06?0.2:1;strip.material.color.setHex(fl<1?0x3a0a30:0xff2bd6);
 o.parts.bar1.concat(o.parts.bar2,o.parts.bar3).forEach((b,i)=>{b.scale.y=.6+.4*Math.abs(Math.sin(t*2+i))});o.hand.rotation.z=-t;comp.render()};
''',css='''.n{position:absolute;font:800 64px Inter;letter-spacing:4px;color:#fff;text-shadow:0 0 10px #ff2bd6,0 0 30px #ff2bd6,0 0 60px #ff2bd6}''',
html='''<div class="n" style="left:70px;top:110px">NIGHT SHIFT</div><div class="n" style="left:72px;top:190px;font-size:32px;text-shadow:0 0 10px #00f0ff,0 0 30px #00f0ff">// DISTRICT 9 · 02:47</div>''')

# ---------- ASCII ----------
page('ascii','#000',COMMON_CAM.replace("document.body.prepend(R.domElement);","")+'''
import {AsciiEffect} from 'three/addons/effects/AsciiEffect.js';
const mat=n=>new THREE.MeshLambertMaterial({color:({screen:0xffffff,window:0xffffff,lampShade:0xffffff,bar1:0x222222,bar2:0x222222,bar3:0x222222,floor:0x555555,wall:0x333333})[n]??0xaaaaaa});
const o=buildOffice(THREE,mat);sc.add(o.group);
const dl=new THREE.DirectionalLight(0xffffff,2.5);dl.position.set(3,8,6);sc.add(dl);sc.add(new THREE.AmbientLight(0xffffff,.9));
const fx=new AsciiEffect(R,' .:-=+*#%@',{invert:true,resolution:.085});fx.setSize(1080,1460);fx.domElement.style.color='#33ff66';fx.domElement.style.backgroundColor='#000';
fx.domElement.style.position='absolute';fx.domElement.style.top='300px';document.body.appendChild(fx.domElement);
window.DUR=4;
const lines=['$ claude render --style ascii office.scene','> loading mesh: desk, monitor, chair, plant ......... ok','> frame 0042  rows:96  cols:120  fps:30'];
window.render=t=>{camAt(t,10.5,4.6);o.hand.rotation.z=-t;fx.render(sc,cam);
 const n=Math.floor(t*28);let s='';let k=n;for(const l of lines){s+=l.slice(0,Math.max(0,k))+'\\n';k-=l.length;if(k<0)break}document.getElementById('term').textContent=s+(Math.floor(t*3)%2?'█':' ')};
''',css='''#term{position:absolute;left:50px;top:70px;right:50px;color:#33ff66;font:500 26px/1.5 'DejaVu Sans Mono',monospace;white-space:pre;text-shadow:0 0 8px #1f9}
#bot{position:absolute;left:50px;bottom:110px;color:#33ff66;font:500 26px 'DejaVu Sans Mono',monospace;opacity:.8}
#crt{position:absolute;inset:0;background:repeating-linear-gradient(0deg,rgba(0,0,0,.35) 0 2px,transparent 2px 5px),radial-gradient(ellipse at center,transparent 60%,rgba(0,0,0,.7));pointer-events:none;z-index:9}
table,td,pre{text-shadow:0 0 6px rgba(51,255,102,.7)}''',html='<div id="term"></div><div id="bot">[ ASCII TERMINAL ]   mem 64K   ok</div><div id="crt"></div>')

# ---------- CLAYMATION ----------
page('claymation','#f2c98a',COMMON_CAM+'''
import {RoundedBoxGeometry} from 'three/addons/geometries/RoundedBoxGeometry.js';
R.shadowMap.enabled=true;R.shadowMap.type=THREE.PCFSoftShadowMap;R.toneMapping=THREE.ACESFilmicToneMapping;
const C={floor:0xd98e4a,wall:0xf2c98a,desk:0xb5651d,deskLeg:0x8a4b16,monitor:0x3b3b58,screen:0x9fe3d4,bar1:0xe94f37,bar2:0xf6c90e,bar3:0x3f88c5,keyboard:0xf1f1e6,mug:0xe94f37,lamp:0x3f88c5,lampShade:0xf6c90e,chair:0xe94f37,chairSeat:0xe94f37,plant:0x5bb153,pot:0xc8553d,window:0xa8dadc,frame:0xf1f1e6,shelf:0x8a4b16,book0:0x3f88c5,book1:0xe94f37,book2:0x5bb153,clock:0xf1f1e6,clockHand:0x222222,cabinet:0x9fe3d4,cabinetLine:0x5c9e92};
// fingerprint-ish bump via noise texture
const cv=document.createElement('canvas');cv.width=cv.height=256;const cx=cv.getContext('2d');const rr=rng(5);for(let i=0;i<4000;i++){cx.fillStyle=`rgba(${rr()>.5?255:0},${rr()>.5?255:0},0,.05)`;cx.beginPath();cx.arc(rr()*256,rr()*256,1+rr()*4,0,7);cx.fill()}
const bump=new THREE.CanvasTexture(cv);bump.wrapS=bump.wrapT=THREE.RepeatWrapping;
const mat=n=>new THREE.MeshStandardMaterial({color:C[n]??0xffffff,roughness:.95,bumpMap:bump,bumpScale:1.5});
const o=buildOffice(THREE,mat,{boxGeo:(w,h,d)=>new RoundedBoxGeometry(w,h,d,4,Math.min(w,h,d)*.3)});sc.add(o.group);
sc.add(new THREE.HemisphereLight(0xfff1d6,0x8a4b16,1.1));const dl=new THREE.DirectionalLight(0xffe2b0,2.6);dl.position.set(5,9,7);dl.castShadow=true;dl.shadow.mapSize.set(2048,2048);Object.assign(dl.shadow.camera,{left:-8,right:8,top:8,bottom:-8});dl.shadow.radius=6;sc.add(dl);
window.DUR=4;
window.render=t=>{const tq=Math.floor(t*12)/12;const j=rng(Math.floor(t*12)+1);camAt(tq,10.8,4.8);cam.position.x+=(j()-.5)*.03;cam.position.y+=(j()-.5)*.03;cam.lookAt(0,1.9,-1.2);
 o.hand.rotation.z=-Math.floor(tq*2)*0.5;o.parts.plant.forEach((p,i)=>p.rotation.z=Math.sin(tq*3+i)*.08);
 o.parts.bar1.concat(o.parts.bar2,o.parts.bar3).forEach((b,i)=>{const p=Math.min(1,Math.floor(Math.max(0,tq-.6-i*.3)*6)/4);b.scale.y=Math.max(.05,p);b.position.y=2+b.userData.h*b.scale.y/2});
 o.parts.mug[0].position.y=1.69+Math.abs(Math.sin(tq*4))*.08;R.render(sc,cam)};
''')

# ---------- BLUEPRINT ----------
page('blueprint','#0b3c8c',COMMON_CAM+'''
R.setClearColor(0x000000,0);R.localClippingEnabled=true;
const clip=new THREE.Plane(new THREE.Vector3(-1,0,0),0);
const mat=n=>new THREE.MeshBasicMaterial({color:0x0b3c8c,transparent:true,opacity:0});
const o=buildOffice(THREE,mat);sc.add(o.group);
o.group.children.forEach(m=>{if(m.geometry&&m.position.y>0&&!(m.geometry.parameters&&m.geometry.parameters.width==8)){const e=new THREE.LineSegments(new THREE.EdgesGeometry(m.geometry,20),new THREE.LineBasicMaterial({color:0xe8f1ff,clippingPlanes:[clip]}));m.add(e)}});
const fl=new THREE.LineSegments(new THREE.EdgesGeometry(new THREE.BoxGeometry(8,0.01,6)),new THREE.LineBasicMaterial({color:0x9fc3ff,clippingPlanes:[clip]}));sc.add(fl);
window.DUR=4;
window.render=t=>{camAt(t*.6,11,5);clip.constant=-4.5+eio(pr(t,0.1,2.4))*9.5;o.hand.rotation.z=-t;R.render(sc,cam);
 document.querySelectorAll('.dim').forEach((d,i)=>d.style.opacity=eo(pr(t,2.3+i*.3,.4)))};
''',css='''#grid{position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.08) 2px,transparent 2px),linear-gradient(90deg,rgba(255,255,255,.08) 2px,transparent 2px),linear-gradient(rgba(255,255,255,.05) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.05) 1px,transparent 1px);background-size:120px 120px,120px 120px,24px 24px,24px 24px;z-index:-1}
canvas{position:absolute;top:0;left:0}
.t{position:absolute;color:#e8f1ff;font:500 26px 'DejaVu Sans Mono',monospace;letter-spacing:3px}
.dim{opacity:0}
#tb{position:absolute;right:50px;bottom:90px;width:560px;border:3px solid #e8f1ff;color:#e8f1ff;font:500 24px/1.6 'DejaVu Sans Mono',monospace;padding:14px 20px}''',
html='''<div id="grid"></div><div class="t" style="left:60px;top:80px">SHEET 3 OF 10 · WORKSPACE PLAN</div>
<div class="t dim" style="left:150px;top:1180px">DESK 1600 × 700</div><div class="t dim" style="left:640px;top:700px">MONITOR 27"</div><div class="t dim" style="left:120px;top:560px">SHELF H 2100</div>
<div id="tb">PROJECT: STUDIO OFFICE<br>SCALE 1:25 · DRAWN: T&amp;T<br>REV B · NOV 2026</div>''')
