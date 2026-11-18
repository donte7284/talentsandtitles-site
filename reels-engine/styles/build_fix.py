from mk import page
# ---------- ASCII v2: custom renderer, readable glyphs ----------
page('ascii','#000',r'''
const COLS=72,ROWS=104,CW=15,CH=1920/ROWS*0.9;// ~16.6px rows over 1728px
const R=new THREE.WebGLRenderer({antialias:false,preserveDrawingBuffer:true});R.setSize(COLS*2,ROWS*2);R.setPixelRatio(1);
const sc=new THREE.Scene();sc.background=new THREE.Color(0x000000);
const cam=new THREE.PerspectiveCamera(42,(COLS*CW)/(ROWS*CH),0.1,100);
const bright={screen:1,window:.9,lampShade:1,bar1:.15,bar2:.15,bar3:.15,wall:.0,floor:.14,frame:.7,mug:.95,keyboard:.8,plant:.6,pot:.75,desk:.85,chair:.55,chairSeat:.7,clock:.9,book0:.7,book1:.5,book2:.8,shelf:.6,cabinet:.65,monitor:.35};
const mat=n=>new THREE.MeshLambertMaterial({color:new THREE.Color().setScalar(bright[n]??.6)});
const o=buildOffice(THREE,mat);sc.add(o.group);
const dl=new THREE.DirectionalLight(0xffffff,2.2);dl.position.set(4,9,7);sc.add(dl);sc.add(new THREE.AmbientLight(0xffffff,.55));
const rt=new THREE.WebGLRenderTarget(COLS,ROWS);const buf=new Uint8Array(COLS*ROWS*4);
const cv=document.createElement('canvas');cv.width=1080;cv.height=1920;document.body.prepend(cv);const X=cv.getContext('2d');
const RAMP=' .,:;-=+*cox%#@';
window.DUR=4.5;
const lines=['$ claude render --style ascii office.scene','> mesh: desk monitor chair plant lamp ...... ok','> cols 72  rows 104  fps 30'];
window.render=t=>{const a=0.55+t*.07;cam.position.set(Math.sin(a)*8.2,4.2,Math.cos(a)*7.8);cam.lookAt(-.2,1.7,-1.3);o.hand.rotation.z=-t;
 o.parts.bar1.concat(o.parts.bar2,o.parts.bar3).forEach((b,i)=>{b.scale.y=.4+.6*Math.abs(Math.sin(t*1.5+i))});
 R.setRenderTarget(rt);R.render(sc,cam);R.readRenderTargetPixels(rt,0,0,COLS,ROWS,buf);R.setRenderTarget(null);
 X.fillStyle='#000';X.fillRect(0,0,1080,1920);X.font='bold 22px "DejaVu Sans Mono"';X.textBaseline='top';
 const top=150;const reveal=eio(pr(t,0,1.4))*ROWS;
 for(let r=0;r<ROWS;r++){if(r>reveal)break;for(let c=0;c<COLS;c++){const i=((ROWS-1-r)*COLS+c)*4;let l=(buf[i]*.3+buf[i+1]*.59+buf[i+2]*.11)/255;l=Math.pow(l,.85);
  if(l<.04)continue;const ch=RAMP[Math.min(RAMP.length-1,Math.floor(l*RAMP.length))];const g=Math.floor(160+95*l);
  X.fillStyle=`rgb(${Math.floor(40*l)},${g},${Math.floor(70+60*l)})`;X.fillText(ch,c*CW,top+r*CH)}}
 // scan cursor line
 if(reveal<ROWS){X.fillStyle='rgba(80,255,140,.35)';X.fillRect(0,top+reveal*CH,1080,CH)}
 // terminal header
 X.font='500 26px "DejaVu Sans Mono"';X.fillStyle='#4dff88';const n=Math.floor(t*30);let k=n;lines.forEach((l,i)=>{X.fillText(l.slice(0,Math.max(0,k)),40,24+i*38);k-=l.length});
 X.fillText('[ ASCII TERMINAL ]   mem 64K   frame '+String(Math.floor(t*30)).padStart(4,'0')+(Math.floor(t*3)%2?' █':''),40,1860)};
''',css='''canvas{position:absolute;top:0;left:0;filter:drop-shadow(0 0 4px rgba(60,255,130,.55))}
#crt{position:absolute;inset:0;background:repeating-linear-gradient(0deg,rgba(0,0,0,.28) 0 2px,transparent 2px 5px),radial-gradient(ellipse at center,transparent 62%,rgba(0,0,0,.75));pointer-events:none;z-index:9}''',html='<div id="crt"></div>')
# ---------- CRYSTAL GLASS v2 ----------
page('crystal_glass','#04040a',r'''
import {EffectComposer} from 'three/addons/postprocessing/EffectComposer.js';import {RenderPass} from 'three/addons/postprocessing/RenderPass.js';import {UnrealBloomPass} from 'three/addons/postprocessing/UnrealBloomPass.js';
const R=new THREE.WebGLRenderer({antialias:true});R.setSize(1080,1920);document.body.prepend(R.domElement);R.toneMapping=THREE.ACESFilmicToneMapping;R.toneMappingExposure=1.1;
const sc=new THREE.Scene();sc.background=new THREE.Color(0x04040a);
// --- environment scene for reflections/refractions ---
const env=new THREE.Scene();env.background=new THREE.Color(0x020205);
const panel=(w,h,c,i,x,y,z)=>{const m=new THREE.Mesh(new THREE.PlaneGeometry(w,h),new THREE.MeshBasicMaterial({color:new THREE.Color(c).multiplyScalar(i),side:2}));m.position.set(x,y,z);m.lookAt(0,0,0);env.add(m)};
panel(6,1.2,0xffffff,6,0,8,2);panel(1.2,6,0xffffff,4,-8,1,-2);panel(1.2,6,0xffffff,4,8,1,-2);panel(5,.6,0xffffff,5,0,-3,8);
[[0xff2d6f,-6,4,6],[0xffb400,6,5,5],[0x29e3a0,-5,-4,-6],[0x2ea8ff,5,-3,-7],[0x9b5cff,0,6,-8],[0xff7a00,7,-1,6]].forEach(([c,x,y,z])=>{const s=new THREE.Mesh(new THREE.SphereGeometry(1.4,16,12),new THREE.MeshBasicMaterial({color:new THREE.Color(c).multiplyScalar(2.5)}));s.position.set(x,y,z);env.add(s)});
const crt=new THREE.WebGLCubeRenderTarget(512,{type:THREE.HalfFloatType});const cc=new THREE.CubeCamera(.1,50,crt);env.add(cc);cc.update(R,env);
// --- brilliant-cut geometry ---
const ring=(n,r,y,off)=>[...Array(n)].map((_,i)=>{const a=(i/n+off)*Math.PI*2;return new THREE.Vector3(Math.cos(a)*r,y,Math.sin(a)*r)});
const ang=v=>{let a=Math.atan2(v.z,v.x);return a<0?a+Math.PI*2:a};
const tris=[];
function stitch(A,B,flip){// connect two closed rings by angle merge
 let i=0,j=0;const na=A.length,nb=B.length;const ea=A.map(ang),eb=B.map(ang);
 // rotate so both start near angle 0
 while(i<na+0&&j<nb+0||i<na||j<nb){const a0=A[i%na],b0=B[j%nb];const an=(ea[(i+1)%na]+(i+1>=na?Math.PI*2:0)),bn=(eb[(j+1)%nb]+(j+1>=nb?Math.PI*2:0));
  if((i<na&&an<=bn)||j>=nb){tris.push(flip?[a0,A[(i+1)%na],b0]:[a0,b0,A[(i+1)%na]]);i++}else{tris.push(flip?[a0,B[(j+1)%nb],b0]:[a0,b0,B[(j+1)%nb]]);j++}}}
const TOP=.43;const table=ring(8,.56,TOP,1/16),star=ring(8,.8,.24,0),girU=ring(16,1,.03,1/32),girL=ring(16,1,-.03,1/32),pav=ring(8,.55,-.5,0),cul=new THREE.Vector3(0,-.88,0),cen=new THREE.Vector3(0,TOP,0);
table.forEach((p,i)=>tris.push([cen,table[(i+1)%8],p]));
stitch(table,star,false);stitch(star,girU,false);stitch(girU,girL,false);stitch(girL,pav,false);pav.forEach((p,i)=>tris.push([p,pav[(i+1)%8],cul]));
const pos=[];tris.forEach(t=>t.forEach(v=>pos.push(v.x,v.y,v.z)));const geo=new THREE.BufferGeometry();geo.setAttribute('position',new THREE.Float32BufferAttribute(pos,3));geo.computeVertexNormals();
const gm=new THREE.ShaderMaterial({side:THREE.DoubleSide,uniforms:{env:{value:crt.texture},t:{value:0}},
vertexShader:'varying vec3 wp;void main(){vec4 w=modelMatrix*vec4(position,1.);wp=w.xyz;gl_Position=projectionMatrix*viewMatrix*w;}',
fragmentShader:`uniform samplerCube env;uniform float t;varying vec3 wp;
vec3 hue(float h){return clamp(abs(mod(h*6.+vec3(0,4,2),6.)-3.)-1.,0.,1.);}
float h1(vec3 p){return fract(sin(dot(p,vec3(12.9898,78.233,37.719)))*43758.5453);}
vec3 S(vec3 d){d=normalize(d);float a=atan(d.z,d.x)/6.2832+.5;float y=d.y;
 vec3 c=vec3(.02,.02,.035);
 c+=vec3(1.)*(1.-smoothstep(0.,.03,abs(fract(a*7.)-.5)-.44))*smoothstep(-.3,.5,y)*1.3;c+=vec3(.35,.38,.45)*smoothstep(0.,1.,y)*.12;
 c+=hue(fract(a*3.+y*.5))*(1.-smoothstep(0.,.02,abs(fract(a*13.+y)-.5)-.47))*1.3;
 c+=vec3(.9)*smoothstep(.93,.98,y)*.8;return c;}
void main(){vec3 N=normalize(cross(dFdx(wp),dFdy(wp)));vec3 V=normalize(cameraPosition-wp);if(dot(N,V)<0.)N=-N;
 float k=h1(floor(N*9.+.5));float F=.06+.94*pow(1.-max(dot(N,V),0.),4.);
 vec3 refl=S(reflect(-V,N));
 float rot=k*6.2832+t*.3;mat2 m=mat2(cos(rot),-sin(rot),sin(rot),cos(rot));
 vec3 col;float io[3];io[0]=.405;io[1]=.415;io[2]=.428;
 for(int c=0;c<3;c++){vec3 r=refract(-V,N,io[c]);r.xz=m*r.xz;r.y=-r.y*.6+ (k-.5);vec3 s=S(r)*1.1+S(r.zyx*vec3(1.,-1.,1.))*.5;col[c]=s[c];}
 vec3 c=mix(col,refl,F)*(.25+1.2*k*k);float g=dot(c,vec3(.33));c=mix(vec3(g),c,.75);
 float sp=pow(max(dot(reflect(-V,N),normalize(vec3(.2,1.,.5))),0.),220.);c+=vec3(sp)*2.;
 gl_FragColor=vec4(pow(c/(1.+c*.35),vec3(2.0)),1.);}`});
const gem=new THREE.Mesh(geo,gm);gem.scale.setScalar(1.25);sc.add(gem);gem.add(new THREE.LineSegments(new THREE.EdgesGeometry(geo,1),new THREE.LineBasicMaterial({color:0xffffff,transparent:true,opacity:.35})));
// floor caustic + bokeh
const cv=document.createElement('canvas');cv.width=512;cv.height=512;const cx=cv.getContext('2d');for(let k=0;k<7;k++){const g=cx.createRadialGradient(256,256,0,256,256,256);const col=['#ff0040','#ff8a00','#ffe600','#2bff88','#00c8ff','#5a4bff','#d400ff'][k];g.addColorStop(0,col+'99');g.addColorStop(1,col+'00');cx.save();cx.translate(256,256);cx.rotate(k/7*Math.PI*2);cx.scale(1,.18);cx.translate(-256,-256);cx.fillStyle=g;cx.fillRect(0,0,512,512);cx.restore()}
const caus=new THREE.Mesh(new THREE.PlaneGeometry(4.2,4.2),new THREE.MeshBasicMaterial({map:new THREE.CanvasTexture(cv),transparent:true,opacity:.6,blending:THREE.AdditiveBlending,depthWrite:false}));caus.rotation.x=-Math.PI/2;caus.position.y=-1.9;sc.add(caus);
const sp=document.createElement('canvas');sp.width=sp.height=128;const sx=sp.getContext('2d');const rg=sx.createRadialGradient(64,64,0,64,64,64);rg.addColorStop(0,'rgba(255,255,255,1)');rg.addColorStop(.4,'rgba(255,255,255,.3)');rg.addColorStop(1,'rgba(255,255,255,0)');sx.fillStyle=rg;sx.fillRect(0,0,128,128);const stx=new THREE.CanvasTexture(sp);
const bk=rng(4);['#ff2d6f','#ffb400','#29e3a0','#2ea8ff','#9b5cff'].forEach(c=>{for(let k=0;k<3;k++){const s=new THREE.Sprite(new THREE.SpriteMaterial({map:stx,color:c,transparent:true,opacity:.14,blending:THREE.AdditiveBlending,depthWrite:false}));const z=bk();s.scale.setScalar(2+z*3);s.position.set(bk()*10-5,bk()*9-3,-6-z*6);sc.add(s)}});
// star glints
const glints=[...Array(5)].map((_,i)=>{const s=new THREE.Sprite(new THREE.SpriteMaterial({map:(()=>{const c=document.createElement('canvas');c.width=c.height=256;const x=c.getContext('2d');x.translate(128,128);[0,Math.PI/2,Math.PI/4,-Math.PI/4].forEach((a,k)=>{x.save();x.rotate(a);const g=x.createLinearGradient(-128,0,128,0);g.addColorStop(0,'rgba(255,255,255,0)');g.addColorStop(.5,'rgba(255,255,255,1)');g.addColorStop(1,'rgba(255,255,255,0)');x.fillStyle=g;x.fillRect(-128,k<2?-3:-1.5,256,k<2?6:3);x.restore()});return new THREE.CanvasTexture(c)})(),transparent:true,blending:THREE.AdditiveBlending,depthWrite:false}));sc.add(s);return s});
const cam=new THREE.PerspectiveCamera(30,1080/1920,.1,100);cam.position.set(0,1.6,12);cam.lookAt(0,-.2,0);
const comp=new EffectComposer(R);comp.addPass(new RenderPass(sc,cam));comp.addPass(new UnrealBloomPass(new THREE.Vector2(1080,1920),.18,.25,.97));
const gp=[[.3,.6,.2],[-.6,.35,.4],[.7,.1,.6],[-.2,.5,-.5],[.5,-.3,.6]];
window.DUR=4.5;
window.render=t=>{gem.rotation.set(.32+Math.sin(t*.8)*.06,t*.7,.08*Math.sin(t*.6));gem.position.y=Math.sin(t*1.3)*.08;gm.uniforms.t.value=t;caus.rotation.z=t*.4;caus.material.opacity=.3+.12*Math.sin(t*2);
 glints.forEach((g,i)=>{const ph=(t*1.1+i*.37)%1.6;const a=Math.max(0,Math.sin(Math.min(ph/.5,1)*Math.PI));g.material.opacity=a;g.scale.setScalar(.2+1.4*a);const v=new THREE.Vector3(...gp[i]).multiplyScalar(1.25).applyEuler(gem.rotation);g.position.copy(v).add(gem.position);g.material.rotation=t*.5});
 comp.render()};
''')
# ---------- INK WASH v2: shader-based soft brush mountains ----------
page('ink_wash','#efe8d8',r'''
const R=new THREE.WebGLRenderer({antialias:true,alpha:true});R.setSize(1080,1920);document.body.prepend(R.domElement);
const sc=new THREE.Scene();const cam=new THREE.OrthographicCamera(-1,1,1,-1,0,1);
const m=new THREE.ShaderMaterial({uniforms:{t:{value:0}},vertexShader:'varying vec2 vUv;void main(){vUv=uv;gl_Position=vec4(position,1.);}',
fragmentShader:`uniform float t;varying vec2 vUv;
float h(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);}
float n(vec2 p){vec2 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);return mix(mix(h(i),h(i+vec2(1,0)),f.x),mix(h(i+vec2(0,1)),h(i+vec2(1,1)),f.x),f.y);}
float fbm(vec2 p){float s=0.,a=.5;for(int i=0;i<6;i++){s+=a*n(p);p=p*2.03+vec2(1.7,9.2);a*=.5;}return s;}
float ridge(float x,float seed,float sharp){float v=0.;v+=pow(abs(sin(x*1.3+seed)),sharp)*.55;v+=fbm(vec2(x*2.2,seed))*.55;v+=pow(abs(sin(x*3.1+seed*2.)),sharp*1.4)*.18;return v;}
void main(){vec2 uv=vUv;uv.x*=1080./1920.;float y=uv.y;
 vec3 paper=vec3(.94,.91,.85)-fbm(uv*vec2(60.,6.))*.04-fbm(uv*14.)*.05;
 float ink=0.;
 // 4 layers far->near
 for(int L=0;L<4;L++){float fl=float(L);float sp=.006+fl*.012;float x=uv.x*(1.1+fl*.35)+t*sp+fl*3.7;
  float base=.62-fl*.13;float H=.28+fl*.04;float top=base+ridge(x,fl*5.3,2.+fl)*H;
  float d=top-y; // >0 inside mountain
  float edge=smoothstep(-.004,.004,d);
  float wet=fbm(vec2(x*4.,y*3.+fl));
  float body=exp(-d*(6.-fl*1.2))*(.75+.4*wet); // dark at ridge, fading down = ink wash
  float dens=(.18+fl*.2)*edge*clamp(body,0.,1.);
  // dry-brush texture on near layers
  dens*=mix(1.,.55+.9*fbm(vec2(x*30.,y*90.)),.35+fl*.1);
  // mist band at mountain foot
  float mist=smoothstep(.0,.09,base+.02-y)*smoothstep(.22,.05,base+.02-y);
  dens*=1.-mist*.85;
  ink=ink+(1.-ink)*dens;}
 // water area below
 float wl=.21;ink*=mix(.0,1.,smoothstep(wl-.05,wl+.07,y))+ (1.-smoothstep(wl-.05,wl+.07,y))*.18*fbm(vec2(uv.x*3.,y*40.));
 // red sun
 vec2 sp=vec2(.38,.84);float sd=length((uv-sp)*vec2(1.,1.));float sun=smoothstep(.062,.058,sd)*(.85+.15*fbm(uv*40.));
 vec3 bg=mix(paper,vec3(.78,.1,.13),sun*smoothstep(0.,.8,t));vec3 col=mix(bg,vec3(.07,.07,.08),ink);
 gl_FragColor=vec4(col,1.);}`});
sc.add(new THREE.Mesh(new THREE.PlaneGeometry(2,2),m));
const cv=document.createElement('canvas');cv.width=1080;cv.height=1920;document.body.appendChild(cv);cv.style.cssText='position:absolute;inset:0';const X=cv.getContext('2d');
const r=rng(9);const birds=[...Array(5)].map((_,i)=>({x:180+i*55,y:330+r()*90,p:r()*6}));
// brush stroke helper: tapered line
function stroke(pts,w,a){for(let i=1;i<pts.length;i++){const u=i/pts.length;X.lineWidth=w*Math.sin(u*Math.PI)+.5;X.strokeStyle=`rgba(18,18,20,${a})`;X.beginPath();X.moveTo(...pts[i-1]);X.lineTo(...pts[i]);X.stroke()}}
window.DUR=4.5;
window.render=t=>{m.uniforms.t.value=t;R.render(sc,cam);X.clearRect(0,0,1080,1920);X.lineCap='round';
 // water ripples
 for(let i=0;i<12;i++){const y=1560+i*28;const x0=150+((i*131+t*25)%420);const pts=[];for(let k=0;k<12;k++)pts.push([x0+k*18,y+Math.sin(k*.6+t+i)*1.5]);stroke(pts,4,.35)}
 // boat + figure
 const bx=330+t*35,by=1590+Math.sin(t*2)*3;X.fillStyle='#141416';X.beginPath();X.moveTo(bx-95,by-4);X.quadraticCurveTo(bx,by+30,bx+95,by-12);X.quadraticCurveTo(bx,by+12,bx-95,by-4);X.fill();
 X.beginPath();X.ellipse(bx-8,by-34,13,22,0,0,7);X.fill();X.beginPath();X.moveTo(bx-38,by-48);X.lineTo(bx+22,by-48);X.lineTo(bx-8,by-66);X.fill();
 stroke([[bx+12,by-40],[bx+60,by-5],[bx+110,by+30]],5,.9);
 // reflection
 X.globalAlpha=.18;X.save();X.translate(0,2*by+14);X.scale(1,-1);X.beginPath();X.ellipse(bx-8,by-34,13,22,0,0,7);X.fill();X.restore();X.globalAlpha=1;
 // birds
 birds.forEach(b=>{const x=b.x+t*45,y=b.y+Math.sin(t*3+b.p)*6,w=Math.sin(t*9+b.p)*9;stroke([[x-18,y-w],[x-8,y-3],[x,y]],5,.9);stroke([[x,y],[x+8,y-3],[x+18,y-w]],5,.9)});
 // calligraphy + seal
 const a1=eo(pr(t,1.6,.9));X.fillStyle=`rgba(20,20,22,${a1})`;X.font='600 60px Lora';['T','H','E',' ','R','I','V','E','R'].forEach((c,i)=>X.fillText(c,90,230+i*68));
 const a2=eo(pr(t,2.4,.5));X.fillStyle=`rgba(190,20,40,${a2})`;X.fillRect(80,860,72,72);X.fillStyle=`rgba(239,232,216,${a2})`;X.font='700 28px Inter';X.fillText('T&T',89,906);
 X.fillStyle=`rgba(20,20,22,${eo(pr(t,2.0,.8))})`;X.font='italic 500 46px Lora';X.textAlign='center';X.fillText('The river keeps no name.',540,1840);X.textAlign='left'};
''')
# ---------- UKIYO-E v2 ----------
page('ukiyo_e','#ecdcb6',r'''
const cv=document.createElement('canvas');cv.width=1080;cv.height=1920;document.body.prepend(cv);const X=cv.getContext('2d');
const PR='#1d3557',PR2='#2f5d8a',PR3='#6f95b8',FOAM='#f3ead3',KEY='#14243a',SKY='#e9d9b0',SKY2='#cbb88f';
// paper texture
const pc=document.createElement('canvas');pc.width=1080;pc.height=1920;const P=pc.getContext('2d');const rr=rng(2);P.fillStyle='#ecdcb6';P.fillRect(0,0,1080,1920);
for(let i=0;i<14000;i++){P.fillStyle=`rgba(110,80,40,${rr()*.07})`;P.fillRect(rr()*1080,rr()*1920,2+rr()*40,1)}for(let i=0;i<3000;i++){P.fillStyle=`rgba(255,255,255,${rr()*.12})`;P.fillRect(rr()*1080,rr()*1920,1,1+rr()*3)}
const grain=document.createElement('canvas');grain.width=1080;grain.height=1920;const G=grain.getContext('2d');const gr=rng(5);for(let i=0;i<40000;i++){G.fillStyle=`rgba(60,40,20,${gr()*.06})`;G.fillRect(gr()*1080,gr()*1920,1.5,1.5)}
// recursive foam claw: branching fingers
function claw(x,y,ang,len,depth,w){if(depth==0||len<6)return;const x2=x+Math.cos(ang)*len,y2=y+Math.sin(ang)*len;
 X.beginPath();X.moveTo(x+Math.cos(ang+1.57)*w,y+Math.sin(ang+1.57)*w);X.quadraticCurveTo(x+Math.cos(ang)*len*.6+Math.cos(ang+1.57)*w*.4,y+Math.sin(ang)*len*.6+Math.sin(ang+1.57)*w*.4,x2,y2);
 X.quadraticCurveTo(x+Math.cos(ang)*len*.6-Math.cos(ang+1.57)*w*.4,y+Math.sin(ang)*len*.6-Math.sin(ang+1.57)*w*.4,x-Math.cos(ang+1.57)*w,y-Math.sin(ang+1.57)*w);X.fill();if(w>3){X.lineWidth=1.4;X.strokeStyle=KEY;X.stroke()}
 for(const da of [-.55,.45])claw(x2,y2,ang+da+.35,len*.55,depth-1,w*.55)}
function waveShape(cx,cy,s,ph){// big wave path with curl, returns key points
 X.beginPath();X.moveTo(cx-560*s,cy+1100*s);
 X.bezierCurveTo(cx-520*s,cy+700*s,cx-420*s,cy+300*s,cx-200*s,cy+60*s+ph*10);
 X.bezierCurveTo(cx-60*s,cy-60*s,cx+200*s,cy-110*s+ph*8,cx+360*s,cy-20*s);
 X.bezierCurveTo(cx+470*s,cy+50*s,cx+470*s,cy+190*s,cx+380*s,cy+240*s);
 X.bezierCurveTo(cx+400*s,cy+150*s,cx+330*s,cy+90*s,cx+250*s,cy+110*s);
 X.bezierCurveTo(cx+120*s,cy+140*s,cx+60*s,cy+300*s,cx+120*s,cy+470*s);
 X.bezierCurveTo(cx+180*s,cy+640*s,cx+300*s,cy+820*s,cx+420*s,cy+1100*s);X.closePath()}
function boat(x,y,rot,sc){X.save();X.translate(x,y);X.rotate(rot);X.scale(sc,sc);X.fillStyle='#f1e4c2';X.strokeStyle=KEY;X.lineWidth=3;
 X.beginPath();X.moveTo(-230,0);X.quadraticCurveTo(-40,46,230,-26);X.lineTo(222,-6);X.quadraticCurveTo(-30,70,-232,22);X.closePath();X.fill();X.stroke();
 X.fillStyle='#3b3b3b';for(let i=0;i<8;i++){X.beginPath();X.ellipse(-170+i*46,2-i*2.5,12,15,0,0,7);X.fill()}X.fillStyle='#7a2e22';for(let i=0;i<8;i++){X.fillRect(-180+i*46,-10-i*2.5,22,8)}X.restore()}
window.DUR=4.5;
window.render=t=>{X.drawImage(pc,0,0);
 // sky band + clouds
 const sk=X.createLinearGradient(0,0,0,700);sk.addColorStop(0,SKY2);sk.addColorStop(.25,SKY);sk.addColorStop(1,'rgba(236,220,182,0)');X.fillStyle=sk;X.fillRect(0,0,1080,700);
 X.fillStyle='rgba(120,110,90,.18)';for(let i=0;i<3;i++){X.beginPath();X.ellipse(200+i*330+((t*12)%60),150+i*40,190,22,0,0,7);X.fill()}
 // Fuji in distance
 X.fillStyle=PR;X.strokeStyle=KEY;X.lineWidth=3;X.beginPath();X.moveTo(560,1235);X.lineTo(690,1115);X.lineTo(735,1112);X.lineTo(870,1235);X.closePath();X.fill();X.stroke();
 X.fillStyle=FOAM;X.beginPath();X.moveTo(662,1141);X.lineTo(690,1115);X.lineTo(735,1112);X.lineTo(765,1140);X.lineTo(744,1132);X.lineTo(726,1146);X.lineTo(706,1133);X.lineTo(686,1148);X.closePath();X.fill();
 // back swell
 X.fillStyle=PR2;X.strokeStyle=KEY;X.lineWidth=4;X.beginPath();X.moveTo(380,1400);X.quadraticCurveTo(700,1150+Math.sin(t*1.4)*20,1100,1240);X.lineTo(1100,1500);X.lineTo(380,1500);X.closePath();X.fill();X.stroke();
 boat(820,1270+Math.sin(t*1.4+1)*14,-.12+Math.sin(t*1.4)*.05,.7);
 // big wave
 const s=1, sw=Math.sin(t*1.1), cx=470+sw*18, cy=500-sw*14;
 const wg=X.createLinearGradient(0,cy,0,cy+1100);wg.addColorStop(0,PR2);wg.addColorStop(.35,PR);wg.addColorStop(1,'#13243d');
 waveShape(cx,cy,s,sw);X.fillStyle=wg;X.fill();X.lineWidth=6;X.strokeStyle=KEY;X.stroke();
 // inner wash stripes (clipped)
 X.save();waveShape(cx,cy,s,sw);X.clip();X.lineWidth=10;
 for(let k=0;k<9;k++){X.strokeStyle=k%2?PR3:'rgba(111,149,184,.55)';X.beginPath();X.moveTo(cx-560+k*30,cy+1100);X.bezierCurveTo(cx-500+k*28,cy+700,cx-380+k*24,cy+330+k*12,cx-170+k*14,cy+120+k*22);X.bezierCurveTo(cx-40+k*10,cy+20+k*22,cx+180,cy-40+k*24,cx+320-k*8,cy+30+k*20);X.stroke()}
 // hollow of curl in paper colour with wash
 X.fillStyle='#e3d1a5';X.beginPath();X.moveTo(cx+250,cy+125);X.bezierCurveTo(cx+130,cy+150,cx+80,cy+300,cx+125,cy+440);X.bezierCurveTo(cx+160,cy+330,cx+210,cy+220,cx+300,cy+185);X.closePath();X.fill();X.restore();
 // foam lip band
 X.fillStyle=FOAM;X.strokeStyle=KEY;X.lineWidth=3;
 X.beginPath();X.moveTo(cx-205,cy+50+sw*10);X.bezierCurveTo(cx-60,cy-75,cx+200,cy-125+sw*8,cx+362,cy-32);X.bezierCurveTo(cx+480,cy+40,cx+485,cy+200,cx+385,cy+246);
 X.bezierCurveTo(cx+450,cy+190,cx+450,cy+60,cx+350,cy+4);X.bezierCurveTo(cx+200,cy-80,cx-40,cy-40,cx-205,cy+50+sw*10);X.fill();X.stroke();
 // fractal claws hanging from the curl lip
 const N=20;for(let k=0;k<N;k++){const a=k/(N-1);const ang=-2.2+a*3.6;const bx=cx+250+Math.cos(ang)*205,by=cy+95+Math.sin(ang)*190;
  const wob=Math.sin(t*4+k*1.3)*.12;X.fillStyle=FOAM;claw(bx,by,ang+1.35+wob,62+16*Math.sin(k*2.1),4,13)}
 // spray dots
 X.fillStyle=FOAM;for(let k=0;k<70;k++){const a=(k*.6180339)%1;const sx=cx-120+a*560,sy=cy-110-((k*53)%140)+Math.sin(t*2.5+k)*16-t*6*((k%3)+1)%60;X.beginPath();X.arc(sx,sy,3+(k%4)*2,0,7);X.fill()}
 // front wave with boat
 boat(360,1500+Math.sin(t*1.6)*18,-.32+Math.sin(t*1.6)*.06,.85);
 for(let r=0;r<4;r++){const y=1560+r*95;X.fillStyle=r%2?PR:PR2;X.strokeStyle=KEY;X.lineWidth=4;X.beginPath();X.moveTo(-10,1930);
  const pts=[];for(let x=-10;x<=1100;x+=15){const yy=y+Math.sin(x/90+t*2.2+r*1.7)*30;pts.push([x,yy]);X.lineTo(x,yy)}X.lineTo(1100,1930);X.closePath();X.fill();X.stroke();
  X.fillStyle=FOAM;X.strokeStyle=KEY;X.lineWidth=2;for(let i=0;i<pts.length;i+=5){const[x,yy]=pts[i];const crest=Math.cos(x/90+t*2.2+r*1.7);if(crest>.55){X.beginPath();X.ellipse(x,yy+4,16,7,0,0,7);X.fill();claw(x+6,yy,-1.0,20,2,6)}}}
 // cartouche + seal
 X.fillStyle='#efe2bf';X.strokeStyle=KEY;X.lineWidth=4;X.fillRect(70,120,120,400);X.strokeRect(70,120,120,400);X.fillStyle=KEY;X.font='700 46px Lora';['T','A','L','E','N','T'].forEach((c,i)=>X.fillText(c,114,188+i*60));
 X.fillStyle='#b5121b';X.fillRect(92,540,76,76);X.fillStyle='#efe2bf';X.font='700 26px Inter';X.fillText('T&T',103,587);
 X.drawImage(grain,0,0)};
''')
