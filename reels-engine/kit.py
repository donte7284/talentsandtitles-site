"""Small JS helpers shared by the weekly-run scenes (prepended to each SCENE)."""
KIT=r'''
const txt=(x,y,s,size=32,fill=GOLD,ls=6,w=600)=>{const e=el('text',{x,y,'text-anchor':'middle','font-size':size,'font-weight':w,'letter-spacing':ls,fill});e.textContent=s;e.setAttribute('opacity',0);return e};
const op=(e,v)=>e.setAttribute('opacity',v);
const dash=(e,v)=>e.setAttribute('stroke-dashoffset',1-v);
const line=(d,stroke=GOLD,w=7,extra={})=>el('path',Object.assign({d,fill:'none',stroke,'stroke-width':w,'stroke-linecap':'round','stroke-linejoin':'round',pathLength:1,'stroke-dasharray':1},extra));
const RED='#d9735a',NAVY='#0f1f3a';
'''
