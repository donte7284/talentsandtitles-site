from mk import page
REND='const R=new THREE.WebGLRenderer({antialias:true});R.setSize(1080,1920);document.body.prepend(R.domElement);R.toneMapping=THREE.ACESFilmicToneMapping;\nconst sc=new THREE.Scene();\n'
ENV='import {RoomEnvironment} from "three/addons/environments/RoomEnvironment.js";const pm=new THREE.PMREMGenerator(R);sc.environment=pm.fromScene(new RoomEnvironment(),.04).texture;\n'
# ---------- LIQUID CHROME ----------
page('liquid_chrome','#0b0b12',REND+ENV+r'''
import {MarchingCubes} from 'three/addons/objects/MarchingCubes.js';
import {EffectComposer} from 'three/addons/postprocessing/EffectComposer.js';import {RenderPass} from 'three/addons/postprocessing/RenderPass.js';import {UnrealBloomPass} from 'three/addons/postprocessing/UnrealBloomPass.js';
R.setClearColor(0x0b0b12);
const mat=new THREE.MeshPhysicalMaterial({color:0xffffff,metalness:1,roughness:.04,iridescence:.8,iridescenceIOR:1.8,clearcoat:1});
const mc=new MarchingCubes(90,mat,true,false,200000);mc.scale.setScalar(1.55);sc.add(mc);
const cam=new THREE.PerspectiveCamera(35,1080/1920,.1,100);cam.position.set(0,0,10);
const l1=new THREE.PointLight(0xff3ea5,80,20);l1.position.set(-4,3,3);sc.add(l1);const l2=new THREE.PointLight(0x3ec6ff,80,20);l2.position.set(4,-3,3);sc.add(l2);
const comp=new EffectComposer(R);comp.addPass(new RenderPass(sc,cam));comp.addPass(new UnrealBloomPass(new THREE.Vector2(1080,1920),.35,.4,.85));
window.DUR=4;
window.render=t=>{mc.reset();const N=8;mc.addBall(.5,.5,.5,1.0,12);
 for(let i=0;i<N;i++){const a=i/N*Math.PI*2+t*.5;const ext=.17+.04*Math.sin(t*2.2+i*1.3);const z=.5+.08*Math.sin(t*1.7+i);
  mc.addBall(.5+Math.cos(a)*ext,.5+Math.sin(a)*ext,z,.45,12);mc.addBall(.5+Math.cos(a)*ext*1.55,.5+Math.sin(a)*ext*1.55,z,.3,12);mc.addBall(.5+Math.cos(a)*ext*2.0,.5+Math.sin(a)*ext*2.0,z,.2,12)}
 mc.update();mc.rotation.set(Math.sin(t*.6)*.3,Math.sin(t*.5)*.45,t*.35);comp.render()};
''')
# ---------- TOY MINIATURE ----------
page('toy_miniature','#9fd6f2',REND+r'''
import {EffectComposer} from 'three/addons/postprocessing/EffectComposer.js';import {RenderPass} from 'three/addons/postprocessing/RenderPass.js';import {ShaderPass} from 'three/addons/postprocessing/ShaderPass.js';import {OutputPass} from 'three/addons/postprocessing/OutputPass.js';
R.shadowMap.enabled=true;R.shadowMap.type=THREE.PCFSoftShadowMap;sc.background=new THREE.Color(0x9fd6f2);
const cam=new THREE.PerspectiveCamera(30,1080/1920,.1,200);
const ground=new THREE.Mesh(new THREE.BoxGeometry(40,.4,60),new THREE.MeshStandardMaterial({color:0x8fcf6a,roughness:1}));ground.position.y=-.2;ground.receiveShadow=true;sc.add(ground);
const road=new THREE.MeshStandardMaterial({color:0x5b5f66,roughness:.9});const dash=new THREE.MeshStandardMaterial({color:0xffffff});
const roadsX=[-8,0,8],roadsZ=[-20,-10,0,10,20];
roadsX.forEach(x=>{const m=new THREE.Mesh(new THREE.BoxGeometry(2,.05,60),road);m.position.set(x,.02,0);m.receiveShadow=true;sc.add(m);for(let z=-29;z<30;z+=2){const d=new THREE.Mesh(new THREE.BoxGeometry(.12,.06,.8),dash);d.position.set(x,.03,z);sc.add(d)}});
roadsZ.forEach(z=>{const m=new THREE.Mesh(new THREE.BoxGeometry(40,.05,2),road);m.position.set(0,.025,z);m.receiveShadow=true;sc.add(m)});
const pal=[0xffb4a2,0xffd6a5,0xfdffb6,0xcaffbf,0x9bf6ff,0xa0c4ff,0xbdb2ff,0xffc6ff,0xffffff,0xf4a261];const r=rng(13);
const box=(w,h,d,x,y,z,c)=>{const m=new THREE.Mesh(new THREE.BoxGeometry(w,h,d),new THREE.MeshStandardMaterial({color:c,roughness:.6}));m.position.set(x,y,z);m.castShadow=m.receiveShadow=true;sc.add(m);return m};
for(let bx=-16;bx<16;bx+=8)for(let bz=-25;bz<25;bz+=10){for(let k=0;k<4;k++){const x=bx+1.9+(k%2)*3.2+ (r()-.5)*.4,z=bz+2+Math.floor(k/2)*4.5;if(r()<.25){[0,1,2].forEach(j=>{const tr=new THREE.Mesh(new THREE.SphereGeometry(.55,12,10),new THREE.MeshStandardMaterial({color:0x3d9a50,roughness:.8}));tr.position.set(x+(j-1)*.9,.8,z+(j%2)*.8);tr.castShadow=true;sc.add(tr);box(.15,.4,.15,x+(j-1)*.9,.2,z+(j%2)*.8,0x7a4b2a)});continue}
 const h=1+r()*4.5;const b=box(2.4,h,3.2,x,h/2,z,pal[Math.floor(r()*pal.length)]);
 // windows
 for(let wy=.6;wy<h-.3;wy+=.7)for(let wx=-.8;wx<=.8;wx+=.55){box(.3,.35,.05,x+wx,wy,z+1.62,0x6c8ebf)}
 box(2.5,.15,3.3,x,h+.07,z,0xeeeeee)}}
const cars=[];const cc=[0xe63946,0xf1c40f,0x2a9d8f,0xffffff,0x3a86ff,0xff7f50];for(let i=0;i<14;i++){const g=new THREE.Group();const b=new THREE.Mesh(new THREE.BoxGeometry(.6,.35,1.1),new THREE.MeshStandardMaterial({color:cc[i%6],roughness:.3}));b.position.y=.3;b.castShadow=true;g.add(b);const top=new THREE.Mesh(new THREE.BoxGeometry(.5,.25,.55),new THREE.MeshStandardMaterial({color:0xdde6f0}));top.position.y=.58;g.add(top);sc.add(g);cars.push({g,x:roadsX[i%3]+(i%2?.45:-.45),o:r()*60,v:(i%2?1:-1)*(2+r()*2)})}
sc.add(new THREE.HemisphereLight(0xffffff,0x8fcf6a,1.4));const dl=new THREE.DirectionalLight(0xfff2d8,2.5);dl.position.set(10,20,8);dl.castShadow=true;dl.shadow.mapSize.set(2048,2048);Object.assign(dl.shadow.camera,{left:-25,right:25,top:30,bottom:-30});sc.add(dl);
const TS={uniforms:{tDiffuse:{value:null}},vertexShader:'varying vec2 vUv;void main(){vUv=uv;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}',
fragmentShader:`uniform sampler2D tDiffuse;varying vec2 vUv;void main(){float b=smoothstep(.06,.4,abs(vUv.y-.47))*0.012;vec4 c=vec4(0.);float tot=0.;for(int i=-4;i<=4;i++)for(int j=-4;j<=4;j++){vec2 o=vec2(float(i)*.5625,float(j))*b/4.;float w=1.-length(vec2(i,j))/6.;if(w>0.){c+=texture2D(tDiffuse,vUv+o)*w;tot+=w;}}c/=tot;vec3 g=vec3(dot(c.rgb,vec3(.299,.587,.114)));c.rgb=mix(g,c.rgb,1.35);gl_FragColor=c;}`};
const comp=new EffectComposer(R);comp.addPass(new RenderPass(sc,cam));comp.addPass(new OutputPass());comp.addPass(new ShaderPass(TS));
window.DUR=4;
window.render=t=>{cam.position.set(14-t*.6,24,22-t*1.2);cam.lookAt(0-t*.4,0,-1-t*1.2);cars.forEach(c=>{const z=((c.o+t*c.v)%60+60)%60-30;c.g.position.set(c.x,0,z);c.g.rotation.y=c.v>0?0:Math.PI});comp.render()};
''')
# ---------- BLACK HOLE ----------
page('black_hole','#000',REND+r'''
const cam=new THREE.OrthographicCamera(-1,1,1,-1,0,1);
const m=new THREE.ShaderMaterial({uniforms:{t:{value:0},res:{value:new THREE.Vector2(1080,1920)}},vertexShader:'varying vec2 vUv;void main(){vUv=uv;gl_Position=vec4(position,1.);}',
fragmentShader:`uniform float t;uniform vec2 res;varying vec2 vUv;
float h(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);}
float n(vec2 p){vec2 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);return mix(mix(h(i),h(i+vec2(1,0)),f.x),mix(h(i+vec2(0,1)),h(i+vec2(1,1)),f.x),f.y);}
float fbm(vec2 p){float s=0.,a=.5;for(int i=0;i<5;i++){s+=a*n(p);p*=2.1;a*=.5;}return s;}
vec3 diskCol(float r,float ang,float bright){float k=clamp((r-1.25)/2.4,0.,1.);vec3 c=mix(vec3(1.,.95,.8),vec3(1.,.45,.08),k);c=mix(c,vec3(.5,.08,.02),k*k);float st=fbm(vec2(ang*6.-t*1.4/ (r*.7),r*5.));return c*(.5+st)*bright*(1.-k)*1.8;}
void main(){vec2 p=(vUv-.5)*vec2(res.x/res.y,1.)*2.6;p.y+=.12;
 float rs=.2;float r=length(p);
 // lensed stars
 vec2 q=p*(1.+rs*rs/(r*r+.001)*1.4);vec3 col=vec3(0.);float s=h(floor(q*90.));col+=vec3(step(.996,s))*(.6+.4*sin(t*3.+s*40.));col+=vec3(.25,.18,.35)*fbm(q*2.)*.25;
 float tilt=.18;
 // back disk (lensed over top/bottom): ring around shadow
 float rr=r/rs;float ang=atan(p.y,p.x);
 if(rr>1.02&&rr<1.9){float br=smoothstep(1.9,1.15,rr)*smoothstep(1.02,1.1,rr)*pow(abs(sin(ang)),.7);float dop=1.+.55*cos(ang);col+=diskCol(1.3+(rr-1.)*2.,ang*3.,br*1.2*dop);}
 // photon ring
 col+=vec3(1.,.85,.6)*exp(-pow((rr-1.06)*28.,2.))*1.6;
 // shadow
 if(rr<1.0)col=vec3(0.);
 // front disk: flat ellipse in front, covers lower half of shadow
 vec2 d=vec2(p.x,p.y/tilt);float dr=length(d)/rs;float da=atan(d.y,d.x);
 if(dr>1.25&&dr<5.5&&(p.y<0.||rr>1.)){float br=smoothstep(5.5,2.,dr)*smoothstep(1.25,1.6,dr);float dop=1.+.7*cos(da+1.57);vec3 dc=diskCol(dr,da,br*dop);col=mix(col,dc+col*.3,clamp(br*1.4,0.,1.));}
 col+=vec3(1.,.6,.25)*.02/(abs(p.y)+.03)*smoothstep(1.2,.1,abs(p.x));
 col=1.-exp(-col*1.3);gl_FragColor=vec4(col,1.);}`});
sc.add(new THREE.Mesh(new THREE.PlaneGeometry(2,2),m));
window.DUR=4.5;
window.render=t=>{m.uniforms.t.value=t;R.render(sc,cam);document.querySelectorAll('.lab').forEach((e,i)=>e.style.opacity=eo(pr(t,1+i*.5,.5)))};
''',css='''.lab{position:absolute;color:#fff;font:600 30px Inter;letter-spacing:5px;opacity:0}.lab i{display:block;font:400 24px 'DejaVu Sans Mono',monospace;letter-spacing:2px;color:#ffb36b;font-style:normal;margin-top:6px}
.ln{position:absolute;background:rgba(255,255,255,.7);height:2px;transform-origin:left}
#ttl{position:absolute;left:0;right:0;top:150px;text-align:center;color:#fff;font:300 52px Inter;letter-spacing:18px}''',
html='''<div id="ttl">SAGITTARIUS A*</div>
<div class="lab" style="left:70px;top:500px">PHOTON RING<i>r = 1.5 r_s</i><div class="ln" style="left:240px;top:20px;width:200px;transform:rotate(38deg)"></div></div>
<div class="lab" style="left:640px;top:1250px">ACCRETION DISK<i>T ≈ 10⁷ K</i><div class="ln" style="left:-90px;top:20px;width:110px;transform:rotate(200deg)"></div></div>
<div class="lab" style="left:80px;top:1350px">EVENT HORIZON<i>point of no return</i><div class="ln" style="left:300px;top:-10px;width:170px;transform:rotate(-55deg)"></div></div>''')
# ---------- TEARDOWN ----------
page('teardown','#16171c',REND+ENV+r'''
import {RoundedBoxGeometry} from 'three/addons/geometries/RoundedBoxGeometry.js';
R.setClearColor(0x16171c);
const cam=new THREE.PerspectiveCamera(32,1080/1920,.1,100);
const layers=[];const L=(y)=>{const g=new THREE.Group();g.userData.y=y;sc.add(g);layers.push(g);return g};
const COLS=12,ROWS=5,P=.62;
// base case
const base=L(0);base.add(new THREE.Mesh(new RoundedBoxGeometry(COLS*P+.6,.5,ROWS*P+.6,3,.15),new THREE.MeshStandardMaterial({color:0x2a2d36,metalness:.4,roughness:.5})));
// pcb
const pcb=L(1);const pt=document.createElement('canvas');pt.width=1024;pt.height=512;const px=pt.getContext('2d');px.fillStyle='#0f6b3d';px.fillRect(0,0,1024,512);px.strokeStyle='#d8b65a';px.lineWidth=3;const r=rng(6);for(let i=0;i<120;i++){px.beginPath();let x=r()*1024,y=r()*512;px.moveTo(x,y);for(let k=0;k<3;k++){if(r()>.5)x+=r()*200-100;else y+=r()*120-60;px.lineTo(x,y)}px.stroke()}
for(let i=0;i<60;i++){px.fillStyle='#e8d48a';px.beginPath();px.arc(r()*1024,r()*512,5,0,7);px.fill()}px.fillStyle='#111';px.fillRect(440,200,140,90);
pcb.add(new THREE.Mesh(new THREE.BoxGeometry(COLS*P+.2,.08,ROWS*P+.2),new THREE.MeshStandardMaterial({map:new THREE.CanvasTexture(pt),roughness:.5})));
// plate
const plate=L(2);plate.add(new THREE.Mesh(new THREE.BoxGeometry(COLS*P+.2,.06,ROWS*P+.2),new THREE.MeshStandardMaterial({color:0xb8bcc6,metalness:1,roughness:.25})));
const sw=L(3),caps=L(4);
const swM=new THREE.MeshStandardMaterial({color:0xd7263d,roughness:.4}),swH=new THREE.MeshStandardMaterial({color:0x1b1b1f,roughness:.6}),capW=new THREE.MeshStandardMaterial({color:0xf2f0ea,roughness:.55}),capA=new THREE.MeshStandardMaterial({color:0xff7a3d,roughness:.55}),capG=new THREE.MeshStandardMaterial({color:0x8a8f9c,roughness:.55});
for(let i=0;i<COLS;i++)for(let j=0;j<ROWS;j++){const x=(i-(COLS-1)/2)*P,z=(j-(ROWS-1)/2)*P;
 const hs=new THREE.Mesh(new THREE.BoxGeometry(.42,.22,.42),swH);hs.position.set(x,0,z);sw.add(hs);const st=new THREE.Mesh(new THREE.BoxGeometry(.12,.16,.12),swM);st.position.set(x,.18,z);sw.add(st);
 const cp=new THREE.Mesh(new RoundedBoxGeometry(.54,.3,.54,2,.07),(i==COLS-1&&j==0)?capA:(j==ROWS-1&&i>3&&i<8)?capW:(i==0||i==COLS-1)?capG:capW);cp.position.set(x,0,z);caps.add(cp)}
sc.add(new THREE.HemisphereLight(0xffffff,0x202030,1));const dl=new THREE.DirectionalLight(0xffffff,2.5);dl.position.set(4,8,5);sc.add(dl);const rl=new THREE.PointLight(0xff7a3d,30,15);rl.position.set(-5,2,-3);sc.add(rl);
const labs=[...document.querySelectorAll('.lab')];const v=new THREE.Vector3();
window.DUR=4.5;
window.render=t=>{const e=eio(pr(t,.6,1.8));const gap=[0,.9,1.7,2.6,3.6];
 layers.forEach((g,i)=>{g.position.y=i*.12+e*gap[i]*1.15});
 const a=.7+t*.12;cam.position.set(Math.sin(a)*19,9+e*2,Math.cos(a)*19);cam.lookAt(0,1.9*e-.6,0);R.render(sc,cam);
 labs.forEach((el,i)=>{const L=layers[4-i];v.set(COLS*P/2+.2,L.position.y,0).project(cam);const x=(v.x*.5+.5)*1080,y=(-v.y*.5+.5)*1920;el.style.left='760px';el.style.top=(y-20)+'px';el.style.opacity=eo(pr(t,2.2+i*.18,.4))})};
''',css='''.lab{position:absolute;color:#fff;font:700 34px Inter;opacity:0;white-space:nowrap;background:rgba(22,23,28,.75);padding:8px 16px;border-radius:12px}.lab b{display:inline-block;color:#ff7a3d;font:700 26px 'DejaVu Sans Mono',monospace;margin-right:12px}.lab span{display:block;color:#9aa0ad;font:400 22px Inter;margin-top:2px;margin-left:58px}
#ttl{position:absolute;left:70px;top:110px;color:#fff;font:800 76px/1 Inter}#ttl i{display:block;font:400 30px Inter;color:#9aa0ad;margin-top:16px;font-style:normal}''',
html='''<div id="ttl">60 keys,<br>exploded.<i>What's inside a mechanical keyboard</i></div>
<div class="lab"><b>01</b>Keycaps<span>PBT, doubleshot</span></div><div class="lab"><b>02</b>Switches<span>linear, 45g</span></div><div class="lab"><b>03</b>Plate<span>aluminium</span></div><div class="lab"><b>04</b>PCB<span>hot-swap</span></div><div class="lab"><b>05</b>Case<span>gasket mount</span></div>''')
# ---------- CRYSTAL GLASS ----------
page('crystal_glass','#05050a',REND+ENV+r'''
import {EffectComposer} from 'three/addons/postprocessing/EffectComposer.js';import {RenderPass} from 'three/addons/postprocessing/RenderPass.js';import {UnrealBloomPass} from 'three/addons/postprocessing/UnrealBloomPass.js';
R.setClearColor(0x05050a);sc.background=new THREE.Color(0x05050a);
const cam=new THREE.PerspectiveCamera(30,1080/1920,.1,100);cam.position.set(0,4.2,12);cam.lookAt(0,-.2,0);
// brilliant cut profile (lathe)
const prof=[new THREE.Vector2(0,-1.6),new THREE.Vector2(1.55,-.05),new THREE.Vector2(1.6,0.05),new THREE.Vector2(.95,.7),new THREE.Vector2(0,.72)];
const geo=new THREE.LatheGeometry(prof,16).toNonIndexed();geo.computeVertexNormals();
const gm=new THREE.ShaderMaterial({uniforms:{t:{value:0}},vertexShader:'varying vec3 n;varying vec3 v;void main(){vec4 w=modelMatrix*vec4(position,1.);n=normalize(mat3(modelMatrix)*normal);v=normalize(cameraPosition-w.xyz);gl_Position=projectionMatrix*viewMatrix*w;}',
fragmentShader:'uniform float t;varying vec3 n;varying vec3 v;vec3 hue(float h){return clamp(abs(mod(h*6.+vec3(0,4,2),6.)-3.)-1.,0.,1.);}float hs(vec3 p){return fract(sin(dot(p,vec3(12.9,78.2,37.7)))*43758.5);}void main(){vec3 N=normalize(n);float f=pow(1.-abs(dot(N,v)),2.);float k=hs(floor(N*7.));vec3 rb=hue(fract(dot(N,vec3(.6,.3,.8))*1.4+t*.15+k*.3));float facet=.25+.75*k;vec3 c=mix(vec3(.75,.82,.95)*facet,rb,.55+.3*f);c+=vec3(1.)*pow(max(dot(reflect(-v,N),normalize(vec3(.3,1.,.4))),0.),24.)*1.6;c+=vec3(1.)*f*.6;gl_FragColor=vec4(c,1.);}'});
const gem=new THREE.Mesh(geo,gm);sc.add(gem);const bk=rng(4);const sp=document.createElement('canvas');sp.width=sp.height=128;const sx=sp.getContext('2d');const rg=sx.createRadialGradient(64,64,0,64,64,64);rg.addColorStop(0,'rgba(255,255,255,1)');rg.addColorStop(.5,'rgba(255,255,255,.35)');rg.addColorStop(1,'rgba(255,255,255,0)');sx.fillStyle=rg;sx.fillRect(0,0,128,128);const stx=new THREE.CanvasTexture(sp);
['#ff2d6f','#ffb400','#29e3a0','#2ea8ff','#9b5cff'].forEach((c,i)=>{for(let k=0;k<3;k++){const s=new THREE.Sprite(new THREE.SpriteMaterial({map:stx,color:c,transparent:true,opacity:.55,blending:THREE.AdditiveBlending,depthWrite:false}));const z=bk();s.scale.setScalar(1.5+z*2.5);s.position.set(bk()*9-4.5,bk()*8-3,-5-z*5);sc.add(s)}});

const edges=new THREE.LineSegments(new THREE.EdgesGeometry(geo,10),new THREE.LineBasicMaterial({color:0xffffff,transparent:true,opacity:.18}));gem.add(edges);
// rainbow streak on floor
const cv=document.createElement('canvas');cv.width=1024;cv.height=64;const cx=cv.getContext('2d');const g=cx.createLinearGradient(0,0,1024,0);['#ff0040','#ff8a00','#ffe600','#2bff88','#00c8ff','#5a4bff','#d400ff'].forEach((c,i)=>g.addColorStop(i/6,c));cx.fillStyle=g;cx.fillRect(0,0,1024,64);
const vg=cx.createLinearGradient(0,0,0,64);vg.addColorStop(0,'rgba(0,0,0,1)');vg.addColorStop(.5,'rgba(0,0,0,0)');vg.addColorStop(1,'rgba(0,0,0,1)');cx.fillStyle=vg;cx.fillRect(0,0,1024,64);
const streak=new THREE.Mesh(new THREE.PlaneGeometry(9,.7),new THREE.MeshBasicMaterial({map:new THREE.CanvasTexture(cv),transparent:true,blending:THREE.AdditiveBlending,opacity:.9}));streak.rotation.x=-Math.PI/2;streak.position.y=-1.9;sc.add(streak);
const l1=new THREE.PointLight(0xffffff,60,20);l1.position.set(3,4,4);sc.add(l1);
const comp=new EffectComposer(R);comp.addPass(new RenderPass(sc,cam));comp.addPass(new UnrealBloomPass(new THREE.Vector2(1080,1920),.6,.5,.75));
window.DUR=4;
window.render=t=>{gem.rotation.set(.25+Math.sin(t*.7)*.1,t*.9,.2);gem.position.y=.15+Math.sin(t*1.4)*.08;gm.uniforms.t.value=t;streak.material.opacity=.6+.3*Math.sin(t*2);streak.position.x=Math.sin(t*.9)*.6;comp.render()};
''')
