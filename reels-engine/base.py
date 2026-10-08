BASE = r'''<!doctype html><html><head><meta charset="utf-8"><style>
*{box-sizing:border-box;margin:0;padding:0}
body{width:1080px;height:1920px;overflow:hidden;background:#0f1f3a;font-family:Inter;color:#f4ecd8}
#navy,#cream{position:absolute;inset:0}
#cream{background:#f3ead7;color:#1c2a44}
.ep{position:absolute;top:120px;left:90px;font:600 30px Inter;letter-spacing:8px;text-transform:uppercase;color:#c9a24a}
.rule{position:absolute;top:180px;left:90px;height:4px;background:#c9a24a}
#cream .ep{color:#8a6a1f}#cream .rule{background:#8a6a1f}
#stage{position:absolute;top:260px;left:0}
#count{position:absolute;top:1190px;left:0;right:0;text-align:center;font:600 34px Inter;letter-spacing:6px;color:#c9a24a}
#cap{position:absolute;top:1300px;left:90px;right:90px;font:500 76px/1.2 Lora;text-align:center}
#cap span{display:inline-block;white-space:pre}
#cap .g{color:#e3bb5c;font-weight:700}
.wm{position:absolute;bottom:90px;left:0;right:0;text-align:center;font:500 28px Inter;letter-spacing:3px;opacity:.55}
#c1{position:absolute;top:560px;left:90px;right:90px;font:500 96px/1.2 Lora}
#c2{position:absolute;top:900px;left:90px;font:700 104px/1.2 Lora}
#hl{position:absolute;left:-18px;top:6px;bottom:2px;background:#e9c869;z-index:-1;border-radius:4px}
#c2w{position:relative;display:inline-block;z-index:1}
#ref{position:absolute;top:1130px;left:94px;font:600 32px Inter;letter-spacing:7px;color:#8a6a1f}
svg text{font-family:Inter}
__CSS__
</style></head><body>
<div id="navy">
 <div class="ep" id="ep">Parable No. __NUM__</div><div class="rule" id="rule"></div>
 <svg id="stage" width="1080" height="920" viewBox="0 0 1080 920"></svg>
 <div id="count"></div><div id="cap"></div>
 <div class="wm">@talentsandtitles</div>
</div>
<div id="cream">
 <div class="ep">Parable No. __NUM__</div><div class="rule" style="width:120px"></div>
 <div id="c1">__C1__</div>
 <div id="c2"><span id="c2w"><span id="hl"></span>__C2__</span></div>
 <div id="ref">__REF__</div>
 <div class="wm">@talentsandtitles</div>
</div>
<script>
const NS='http://www.w3.org/2000/svg';const st=document.getElementById('stage');
function el(n,a,p){const e=document.createElementNS(NS,n);for(const k in a)e.setAttribute(k,a[k]);(p||st).appendChild(e);return e}
const $=id=>document.getElementById(id);
const cl=(x,a=0,b=1)=>Math.max(a,Math.min(b,x));
const pr=(t,s,d)=>cl((t-s)/d);
const eo=x=>1-Math.pow(1-x,3);
const eio=x=>x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2;
const bounce=x=>{const n=7.5625,d=2.75;if(x<1/d)return n*x*x;if(x<2/d)return n*(x-=1.5/d)*x+.75;if(x<2.5/d)return n*(x-=2.25/d)*x+.9375;return n*(x-=2.625/d)*x+.984375};
const GOLD='#c9a24a',BR='#e3bb5c',CR='#f4ecd8';
const CAP=__CAP__;const CAPT=__CAPT__;const END=__END__;
// optional: per-word caption times and cream-page cues, e.g. from voiceover timestamps
const CAPW=__CAPW__;const CUE=Object.assign({c1:END+0.6,c2:END+1.9,hl:END+2.2,ref:END+3.0},__CUE__);
const cap=$('cap');const ws=CAP.map(([w,g,br])=>{const s=document.createElement('span');s.textContent=w;if(g)s.className='g';cap.appendChild(s);if(br)cap.appendChild(document.createElement('br'));return s});
__SCENE__
window.render=function(t){
 $('ep').style.opacity=eo(pr(t,0.1,0.5));$('rule').style.width=120*eo(pr(t,0.2,0.6))+'px';
 scene(t);
 ws.forEach((s,i)=>{const a=eo(pr(t,CAPW?CAPW[i]:CAPT+i*0.16,0.4));s.style.opacity=a;s.style.transform=`translateY(${(1-a)*24}px)`});
 const w=eio(pr(t,END,0.7));$('cream').style.clipPath=`inset(${(1-w)*100}% 0 0 0)`;
 const a1=eo(pr(t,CUE.c1,0.6));$('c1').style.opacity=a1;$('c1').style.transform=`translateY(${(1-a1)*30}px)`;
 $('c2').style.opacity=eo(pr(t,CUE.c2,0.5));
 const h=eio(pr(t,CUE.hl,0.6));$('hl').style.width=`calc(${h*100}% + ${36*h}px)`;
 $('ref').style.opacity=eo(pr(t,CUE.ref,0.5));
};
render(0);
</script></body></html>'''
def build(path,num,c1,c2,ref,cap,capt,end,scene,css='',capw=None,cue=None):
    import json
    h=BASE.replace('__NUM__',str(num)).replace('__C1__',c1).replace('__C2__',c2).replace('__REF__',ref).replace('__CAP__',json.dumps(cap)).replace('__CAPT__',str(capt)).replace('__END__',str(end)).replace('__CSS__',css).replace('__CAPW__',json.dumps(capw)).replace('__CUE__',json.dumps(cue or {})).replace('__SCENE__',scene)
    open(path,'w').write(h)
