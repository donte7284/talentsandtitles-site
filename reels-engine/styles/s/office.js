// Shared office scene. mat(name) -> material. Parts: floor, wall, desk, deskLeg, monitor, screen, bar1..3, chair, chairSeat, plant, pot, window, frame, shelf, book, clock, lamp, mug, keyboard, cabinet
export function buildOffice(THREE, mat, opts={}){
  const BG=opts.boxGeo||((w,h,d)=>new THREE.BoxGeometry(w,h,d));
  const g=new THREE.Group(); const parts={};
  const box=(name,w,h,d,x,y,z,m)=>{const o=new THREE.Mesh(BG(w,h,d),mat(m||name));o.position.set(x,y,z);o.castShadow=o.receiveShadow=true;g.add(o);(parts[name]=parts[name]||[]).push(o);return o};
  const cyl=(name,rt,rb,h,x,y,z,m,seg=24)=>{const o=new THREE.Mesh(new THREE.CylinderGeometry(rt,rb,h,seg),mat(m||name));o.position.set(x,y,z);o.castShadow=o.receiveShadow=true;g.add(o);(parts[name]=parts[name]||[]).push(o);return o};
  box('floor',8,0.2,6,0,-0.1,0);
  box('wall',8,5,0.2,0,2.5,-3);
  box('wall',0.2,5,6,-4,2.5,0);
  // window on back wall
  box('window',2.4,1.8,0.05,1.6,3.0,-2.88);
  box('frame',2.6,0.1,0.12,1.6,3.95,-2.85);box('frame',2.6,0.1,0.12,1.6,2.05,-2.85);
  box('frame',0.1,1.9,0.12,0.35,3.0,-2.85);box('frame',0.1,1.9,0.12,2.85,3.0,-2.85);box('frame',0.06,1.8,0.1,1.6,3.0,-2.84);
  // desk
  box('desk',3.2,0.12,1.4,0,1.5,-1.4);
  [[-1.5,-0.8],[1.5,-0.8],[-1.5,-2.0],[1.5,-2.0]].forEach(([x,z])=>box('deskLeg',0.1,1.45,0.1,x,0.72,z));
  // monitor
  box('monitor',1.7,1.05,0.08,-0.2,2.35,-1.75);box('monitor',0.12,0.5,0.08,-0.2,1.8,-1.78);box('monitor',0.6,0.04,0.35,-0.2,1.58,-1.72);
  const scr=box('screen',1.56,0.92,0.02,-0.2,2.35,-1.7);
  // bars on screen
  [0,1,2,3].forEach(i=>{const b=box('bar'+(i%3+1),0.22,0.3+i*0.15,0.03,-0.75+i*0.36,2.0+(0.3+i*0.15)/2,-1.68);b.userData.h=0.3+i*0.15;});
  box('keyboard',0.9,0.04,0.3,-0.2,1.58,-1.1);
  cyl('mug',0.12,0.1,0.25,0.95,1.69,-1.2);
  // lamp
  cyl('lamp',0.18,0.22,0.05,1.3,1.58,-1.85);cyl('lamp',0.03,0.03,0.7,1.3,1.95,-1.85);
  const shade=cyl('lampShade',0.05,0.25,0.25,1.3,2.35,-1.75);shade.rotation.x=0.4;
  // chair
  box('chairSeat',0.9,0.12,0.9,-0.2,0.95,-0.2);box('chair',0.9,1.0,0.1,-0.2,1.5,0.25);cyl('chair',0.05,0.05,0.8,-0.2,0.5,-0.2);
  cyl('chair',0.45,0.45,0.05,-0.2,0.08,-0.2,undefined,5);
  // plant
  cyl('pot',0.32,0.25,0.6,-3.2,0.3,-2.3);
  for(let i=0;i<7;i++){const l=new THREE.Mesh(new THREE.SphereGeometry(0.35,10,8),mat('plant'));const a=i/7*Math.PI*2;l.position.set(-3.2+Math.cos(a)*0.25,0.95+Math.sin(i*1.7)*0.25+ (i%3)*0.2,-2.3+Math.sin(a)*0.25);l.scale.set(0.8,1.3,0.8);l.castShadow=true;g.add(l);(parts.plant=parts.plant||[]).push(l);}
  // shelf with books
  box('shelf',1.8,0.08,0.4,-2.6,3.2,-2.75);
  [0,1,2,3,4].forEach(i=>box('book',0.15,0.45+(i%2)*0.1,0.3,-3.3+i*0.2,3.48+(i%2)*0.05,-2.75,'book'+(i%3)));
  // clock
  const ck=cyl('clock',0.35,0.35,0.06,-1.6,3.6,-2.86);ck.rotation.x=Math.PI/2;
  const hand=box('clockHand',0.04,0.28,0.02,-1.6,3.68,-2.81);
  // cabinet
  box('cabinet',0.9,1.2,1.0,2.7,0.6,-2.2);box('cabinetLine',0.7,0.03,0.02,2.7,0.85,-1.69);box('cabinetLine',0.7,0.03,0.02,2.7,0.35,-1.69);
  return {group:g,parts,screen:scr,hand};
}
