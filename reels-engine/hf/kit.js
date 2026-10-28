/* Parables for Builders: shared timeline pieces for HyperFrames episodes.
   window.EP = {words:[{t,s,e}], dur, paper, cues:{q,send,turnHl}, theme} is written by build.py from the
   clone's word timestamps, so every cue lands on the spoken word. An episode calls K.run(scene)
   where scene(tl, K) adds its own story beats with K.at("spoken phrase"). */
(function(){
  const EP = window.EP;
  const norm = s => s.toLowerCase().replace(/[^a-z0-9']/g,"");
  const toks = EP.words.map(w => norm(w.t));
  const K = {EP, words:EP.words, dur:EP.dur, E:"power3.out", IO:"power2.inOut"};

  /* time of a spoken phrase: its first word's start (or last word's end), nth occurrence, at or after `from` */
  K.at = function(phrase, opt){
    opt = opt || {}; const p = phrase.split(/\s+/).map(norm); let n = 0;
    for(let i=0;i<=toks.length-p.length;i++){
      if(EP.words[i].s < (opt.from||0) - 0.01) continue;
      let ok = true; for(let j=0;j<p.length;j++) if(toks[i+j]!==p[j]){ok=false;break;}
      if(ok && ++n === (opt.nth||1)) return opt.end ? EP.words[i+p.length-1].e : EP.words[i].s;
    }
    throw new Error("phrase not in narration: "+phrase);
  };
  K.end = (phrase, opt) => K.at(phrase, Object.assign({}, opt||{}, {end:true}));

  /* draw-on helper for SVG strokes */
  K.draw = function(tl, sel, t, d, len){
    tl.set(sel, {strokeDasharray:len, strokeDashoffset:len}, 0);
    tl.to(sel, {strokeDashoffset:0, duration:d||.5, ease:"power3.out"}, t);
  };
  /* show/hide move an object relative to wherever it already sits (CSS position or an earlier gsap.set):
     from {y:40} means "start 40px lower", {scale:.9} means "start at 90% of its size", {rotation:-8} "8 degrees back" */
  const rel = (v, sign) => (sign*v >= 0 ? "+=" : "-=") + Math.abs(v);
  function offsets(o, dir){
    const a = {}, b = {};
    for(const k in o){
      const v = o[k];
      if(k === "x" || k === "y" || k === "rotation"){ a[k] = rel(v, 1); b[k] = rel(v, -1); }
      else if(k === "scale"){ a[k] = rel(v - 1, 1); b[k] = rel(v - 1, -1); }
      else a[k] = v;
    }
    return dir === "in" ? [a, b] : [b, a];
  }
  K.show = function(tl, sel, t, from, d){
    const [a, b] = offsets(from || {y:24}, "in");
    return tl.fromTo(sel, Object.assign({opacity:0}, a), Object.assign({opacity:1, duration:d||.5, ease:K.E, immediateRender:false}, b), t);
  };
  K.hide = function(tl, sel, t, to, d){
    const o = Object.assign({}, to || {}); const a = {};
    for(const k in o){ const v = o[k]; a[k] = (k === "x" || k === "y" || k === "rotation") ? rel(v, 1) : (k === "scale" ? rel(v - 1, 1) : v); }
    return tl.to(sel, Object.assign({opacity:0, duration:d||.4, ease:"power2.in"}, a), t);
  };

  function captions(tl){
    /* phrases: break on punctuation, on pauses, or every 6 words; stop where the cream page starts */
    const cap = document.getElementById("cap"), lines = []; let cur = [];
    EP.words.forEach((w,i) => {
      if(w.s >= EP.paper - 0.05) return;
      cur.push(w);
      const nx = EP.words[i+1], gap = nx ? nx.s - w.e : 9;
      if(/[.,:;?!]["”]?$/.test(w.t) || gap > .45 || cur.length >= 6 || !nx || nx.s >= EP.paper - 0.05){ lines.push(cur); cur = []; }
    });
    lines.forEach((ln, li) => {
      const el = document.createElement("div"); el.className = "line"; el.id = "ln"+li;
      ln.forEach((w, wi) => { const sp = document.createElement("span"); sp.className="w"; sp.id=`w${li}_${wi}`; sp.textContent = w.t; el.appendChild(sp); });
      cap.appendChild(el);
      const s = ln[0].s, e = ln[ln.length-1].e, nxt = lines[li+1] ? lines[li+1][0].s : e + .5;
      tl.fromTo(el, {opacity:0, y:22}, {opacity:1, y:0, duration:.16, ease:K.E, immediateRender:false}, Math.max(0, s - .02));
      const off = lines[li+1] ? Math.min(e + .3, nxt - .1) : e + .3;
      tl.to(el, {opacity:0, y:-12, duration:.08, ease:"power2.in"}, Math.max(s + .1, off));
      ln.forEach((w, wi) => {
        tl.set(`#w${li}_${wi}`, {color:"#e3bb5c"}, w.s);
        tl.set(`#w${li}_${wi}`, {color:"rgba(244,236,216,.94)"}, Math.max(w.s + .05, wi < ln.length-1 ? ln[wi+1].s : w.e + .15));
      });
    });
  }

  function atmosphere(tl){
    tl.fromTo("#beam1", {rotation:16, opacity:.30}, {rotation:11, opacity:.44, duration:EP.paper, ease:"sine.inOut"}, 0);
    tl.fromTo("#beam2", {rotation:-9, opacity:.16}, {rotation:-4, opacity:.28, duration:EP.paper, ease:"sine.inOut"}, 0);
    tl.fromTo("#grain", {x:0, y:0}, {x:60, y:-40, duration:EP.dur, ease:"steps("+Math.round(EP.dur*6)+")"}, 0);
    tl.fromTo("#header,#mark", {opacity:0}, {opacity:1, duration:.4}, .1);
  }

  function hook(tl){
    tl.fromTo("#hook .kick", {opacity:0, y:20}, {opacity:1, y:0, duration:.35, ease:K.E}, .05);
    tl.fromTo("#hook .big", {opacity:0, y:40, filter:"blur(10px)"}, {opacity:1, y:0, filter:"blur(0px)", duration:.55, ease:K.E}, .1);
    tl.to("#hook .rule", {width:520, duration:.7, ease:K.E}, .45);
    tl.to("#hook", {opacity:0, y:-30, duration:.4, ease:"power2.in"}, EP.hookOff);
  }

  function paper(tl){
    const t = EP.paper, c = EP.cues;
    tl.fromTo("#paper", {clipPath:"inset(100% 0 0 0)"}, {clipPath:"inset(0% 0 0 0)", duration:.6, ease:"power3.inOut"}, t);
    tl.to("#chrome", {opacity:0, duration:.2}, t + .25);
    tl.fromTo("#paper .eyebrow,#paper .pm", {opacity:0}, {opacity:1, duration:.4}, t + .35);
    tl.fromTo("#paper .turn", {opacity:0, y:30}, {opacity:1, y:0, duration:.5, ease:K.E}, t + .45);
    tl.fromTo("#paper .turn em", {"--hl":0}, {"--hl":1, duration:.45, ease:K.E}, c.turnHl);
    tl.fromTo("#paper .q", {opacity:0, y:20}, {opacity:1, y:0, duration:.5, ease:K.E}, c.q);
    tl.fromTo("#paper .ref", {opacity:0}, {opacity:1, duration:.5}, c.q + .7);
    tl.fromTo("#paper .send", {opacity:0, y:20}, {opacity:1, y:0, duration:.5, ease:K.E}, c.send);
    tl.fromTo("#paper .col", {scale:1}, {scale:1.025, duration:EP.dur - t, ease:"none"}, t);
  }

  /* camera: a slow push per scene. shots = [[start, end, fromScale, toScale, fromY, toY], ...] */
  K.camera = function(tl, shots){
    shots.forEach((s, i) => tl.fromTo("#stage", {scale:s[2], y:s[4]||0}, {scale:s[3], y:s[5]||0, duration:s[1]-s[0], ease:"none", immediateRender:i===0}, s[0]));
  };

  K.run = function(scene){
    const tl = gsap.timeline({paused:true});
    if(EP.theme){ const r = document.documentElement.style; Object.entries(EP.theme).forEach(([k,v]) => r.setProperty("--"+k, v)); }
    atmosphere(tl); hook(tl); captions(tl);
    scene(tl, K);
    paper(tl);
    K.tl = tl;
  };
  window.K = K;
})();
