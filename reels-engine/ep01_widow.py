"""Parable No. 1, the widow's oil, timed to a voiceover.

usage: python ep01_widow.py <voice.m4a> <stt.json> <out.mp4>
stt.json is ElevenLabs speech-to-text output with word timestamps for that recording.
Every animation cue below is a word from the recording, so a re-record only needs a new stt.json.
"""
import json,os,re,subprocess,sys
from base import build
OIL_CSS='#count{top:1170px}#cap{top:1290px}#c2{font-size:110px}'  # same layout as the approved No. 1 test

voice,stt,out=sys.argv[1:4]
here=os.path.dirname(os.path.abspath(__file__))
words=[w for w in json.load(open(stt))['words'] if w['type']=='word']
# speech-to-text can start a word at the end of the previous one when a pause sits between them;
# move any word start that falls inside a detected silence to where the voice actually begins
sd=subprocess.run(['ffmpeg','-hide_banner','-i',voice,'-af','silencedetect=n=-40dB:d=0.15','-f','null','-'],capture_output=True,text=True).stderr
sil=list(zip(map(float,re.findall(r'silence_start: ([\d.]+)',sd)),map(float,re.findall(r'silence_end: ([\d.]+)',sd))))
for w in words:
    for s0,s1 in sil:
        if s0-0.1<=w['start']<s1-0.05 and s1<w['end']:print(f"snap {w['text']!r} {w['start']:.2f} -> {s1:.2f}");w['start']=s1
norm=lambda s:re.sub(r"[^a-z']",'',s.lower())
toks=[norm(w['text']) for w in words]

LEAD,TAIL=0.35,0.9
OFF=max(0,words[0]['start']-LEAD)
END_AUDIO=words[-1]['end']+TAIL-OFF

def at(phrase,nth=1,end=False):
    """time (s, trimmed) of the nth occurrence of a phrase; its first word's start, or last word's end"""
    p=[norm(x) for x in phrase.split()];n=0
    for i in range(len(toks)-len(p)+1):
        if toks[i:i+len(p)]==p:
            n+=1
            if n==nth:return round((words[i+len(p)-1]['end'] if end else words[i]['start'])-OFF,3)
    raise SystemExit(f'phrase not in recording: {phrase!r} #{nth}')

T=dict(
 widow=at('widow'),debt=at('debt'),sons=at('two sons'),
 house=at('your house',1,end=True),nothing=at('nothing',1),jar=at('one jar of oil'),
 borrow=at('borrow'),b1=at('every empty'),b2=at('empty jar'),b3=at('jar your'),b4=at('neighbors'),
 then=at('then shut'),pours=at('she pours'),runs=at('runs out of jars'),
)
span=T['runs']-T['pours']-0.1;per=span/5;T['fd']=per*0.88;T['gap']=per*0.12
supply=at('the supply');jarswere=at('the jars were')

SCENE=r'''
const T=__T__;
const ofr=el('clipPath',{id:'oilframe'},el('defs',{}));el('rect',{x:0,y:0,width:960,height:860},ofr);
const W=el('g',{transform:'translate(60,40)','clip-path':'url(#oilframe)'});
const JAR="M-55 -150 h110 v28 q0 14 14 22 q46 30 46 110 v120 q0 50 -50 50 h-130 q-50 0 -50 -50 v-120 q0 -80 46 -110 q14 -8 14 -22z";
const INNER="M-104 -30 q10 -40 40 -62 h128 q30 22 40 62 v158 q0 44 -44 44 h-120 q-44 0 -44 -44z";
const pos=[[160,190],[480,190],[800,190],[160,610],[480,610],[800,610]];
const defs=el('defs',{},W);const cp=el('clipPath',{id:'cp'},defs);el('path',{d:INNER},cp);
// her house: holds the one jar until the borrowing starts
const house=el('g',{},W);
const HOUSE=['M170 440 L480 190 L790 440','M230 400 V780 H730 V400','M600 780 V650 H680 V780'];
const hp=HOUSE.map(d=>el('path',{d,fill:'none',stroke:GOLD,'stroke-width':7,'stroke-linejoin':'round','stroke-linecap':'round',pathLength:1,'stroke-dasharray':1},house));
const H0=[400,610],HS=0.72;
const jars=pos.map((p,i)=>{const g=el('g',{transform:`translate(${p[0]},${p[1]})`},W);
 const o={g};
 if(i<5){o.stream=el('rect',{x:-7,y:-330,width:14,height:0,rx:7,fill:BR},g);
  const c=el('g',{'clip-path':'url(#cp)'},g);o.liq=el('path',{fill:BR},c);
  o.out=el('path',{d:JAR,fill:'none',stroke:GOLD,'stroke-width':7,'stroke-linejoin':'round',pathLength:1,'stroke-dasharray':1},g);
 }else{o.box=el('rect',{x:-120,y:-170,width:240,height:360,rx:24,fill:'none',stroke:CR,'stroke-width':5,'stroke-dasharray':'18 16'},g);
  o.q=el('text',{x:0,y:50,'text-anchor':'middle',style:'font-family:Lora','font-size':150,fill:CR},g);o.q.textContent='?';}
 return o});
const BASE_OIL=0.22;
const drawAt=[T.jar,T.b1,T.b2,T.b3,T.b4];
// status line: [text, colour, time it appeared]; a pure function of t
function status(t){
 if(t>=T.runs)return['5 FULL · NO JARS LEFT',GOLD,T.runs];
 if(t>=T.pours){let n=0,since=T.pours;for(let i=0;i<5;i++){const f=T.pours+i*(T.fd+T.gap)+T.fd;if(t>=f){n++;since=f}}return[`${n} FULL`,GOLD,since]}
 if(t>=T.then)return['',GOLD,T.then];
 if(t>=T.borrow){const b=drawAt.slice(1).filter(s=>t>=s);return[`1 JAR + ${b.length} BORROWED`,GOLD,b.length?b[b.length-1]:T.borrow]}
 if(t>=T.jar)return['IN THE HOUSE: 1 JAR OF OIL',GOLD,T.jar];
 if(t>=T.nothing)return['IN THE HOUSE: NOTHING','#d9735a',T.nothing];
 if(t>=T.house)return['IN THE HOUSE: ?',CR,T.house];
 if(t>=T.sons)return['DEBT UNPAID · TWO SONS AT STAKE','#d9735a',T.sons];
 if(t>=T.debt)return['DEBT UNPAID','#d9735a',T.debt];
 return['',GOLD,0];
}
function scene(t){
 // house draws in on "widow", fades as the borrowing starts
 hp.forEach((p,i)=>p.setAttribute('stroke-dashoffset',1-eio(pr(t,T.widow+i*0.35,1.0))));
 const hfade=1-eo(pr(t,T.borrow,0.6));
 house.setAttribute('opacity',hfade*(t>T.house&&t<T.borrow?0.85+0.15*Math.sin((t-T.house)*5):1));
 let full=0;
 jars.forEach((j,i)=>{
  if(i<5){
   const a=eo(pr(t,drawAt[i],0.6));
   j.out.setAttribute('stroke-dashoffset',1-a);j.g.setAttribute('opacity',a>0?1:0);
   const s=T.pours+i*(T.fd+T.gap);let p=eio(pr(t,s,T.fd));if(p>=0.999)full++;
   const base=i==0?BASE_OIL*eo(pr(t,T.jar+0.3,0.5)):0;const fill=base+(1-base)*p;
   const lvl=172-fill*250;const amp=(p>0&&p<1)?7*Math.sin(Math.PI*p):1.5*Math.max(0,1-(t-s-T.fd)/1.2)*(p>=1?1:0);
   let d=`M-130 ${lvl}`;for(let x=-130;x<=130;x+=10){d+=` L${x} ${lvl+amp*Math.sin(x/22+t*9+i)}`}d+=' L130 200 L-130 200Z';
   j.liq.setAttribute('d',fill>0?d:'');
   const raw=pr(t,s-0.12,T.fd+0.12);let top=-330,bot=-330;
   if(raw>0&&raw<1){const head=cl(raw/0.14);const tail=cl((raw-0.82)/0.18);bot=-330+(lvl+330)*eo(head);top=-330+(lvl+330)*eio(tail);}
   j.stream.setAttribute('y',top);j.stream.setAttribute('height',Math.max(0,bot-top));
   const sc=1+0.04*Math.sin(Math.PI*pr(t,s+T.fd-0.05,0.35));
   let x=pos[i][0],y=pos[i][1],k=sc;
   if(i==0){const m=eio(pr(t,T.borrow,0.8));x=H0[0]+(x-H0[0])*m;y=H0[1]+(y-H0[1])*m;k=sc*(HS+(1-HS)*m)}
   j.g.setAttribute('transform',`translate(${x},${y}) scale(${k})`);
  }else{
   const a=eo(pr(t,T.runs,0.5));const pulse=0.45+0.3*Math.sin(Math.max(0,t-T.runs-0.5)*5)*(t>T.runs+0.5?1:0);
   j.g.setAttribute('opacity',a*cl(pulse,0.2,0.8));
   j.g.setAttribute('transform',`translate(${pos[i][0]},${pos[i][1]}) scale(${0.9+0.1*a})`);
  }});
 const [txt,col,since]=status(t);
 $('count').textContent=txt;$('count').style.color=col;$('count').style.opacity=txt?eo(pr(t,since,0.3)):0;
}
'''
CAPS=[["The ",0,0],["oil ",0,0],["only ",0,0],["stops ",0,0],["when ",0,1],["she ",0,0],["runs ",1,0],["out ",1,0],["of ",1,0],["jars.",1,0]]
p=['the','oil','only','stops','when','she','runs','out','of','jars']
# each caption word lands as it is spoken
i=next(i for i in range(len(toks)) if toks[i:i+2]==['the','oil']);capw=[]
for w in p:
    while toks[i]!=w:i+=1
    capw.append(round(words[i]['start']-OFF-0.08,3));i+=1
html=os.path.join(here,'ep01_widow.html')
SCENE=SCENE.replace('__T__',json.dumps(T))
build(html,1,'The supply was never the limit.','The jars were.','2 KINGS 4 : 1–7',CAPS,capw[0],supply-0.1,SCENE,OIL_CSS,
      capw=capw,cue=dict(c1=supply+0.15,c2=jarswere,hl=jarswere+0.25,ref=jarswere+0.9))
print('offset',round(OFF,2),'duration',round(END_AUDIO,2),'cues',T,'punchline',supply,jarswere)

# voice: trim, high-pass, two-pass loudness normalise to -14 LUFS, short fades
os.makedirs(os.path.join(here,'out'),exist_ok=True)
wav=os.path.join(here,'out','ep01_voice.wav')
pre=f"atrim={OFF}:{OFF+END_AUDIO},asetpts=PTS-STARTPTS,aformat=channel_layouts=mono,highpass=f=80"
m=subprocess.run(['ffmpeg','-hide_banner','-i',voice,'-af',pre+',loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True).stderr
L=json.loads(m[m.rindex('{'):m.rindex('}')+1])
ln=f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={L['input_i']}:measured_TP={L['input_tp']}:measured_LRA={L['input_lra']}:measured_thresh={L['input_thresh']}:offset={L['target_offset']}:linear=true"
subprocess.run(['ffmpeg','-y','-loglevel','error','-i',voice,'-af',f"{pre},{ln},apad=whole_dur={END_AUDIO},afade=t=in:d=0.05,afade=t=out:st={END_AUDIO-0.4}:d=0.4",'-ar','48000',wav],check=True)

silent=os.path.join(here,'out','ep01_silent.mp4')
subprocess.run([sys.executable,os.path.join(here,'render.py'),str(round(END_AUDIO,2)),silent,'ep01_widow.html'],check=True)
subprocess.run(['ffmpeg','-y','-loglevel','error','-i',silent,'-i',wav,'-c:v','copy','-c:a','aac','-b:a','192k','-ac','2','-shortest','-movflags','+faststart',out],check=True)
print('wrote',out)
