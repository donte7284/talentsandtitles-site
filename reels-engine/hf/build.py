"""Build and render a Parables episode with HyperFrames, timed to the clone narration.

usage: python hf/build.py <episode> <voice.wav> <stt.json> <out.mp4> [--snap 1,5,9]
  episode   name of the scene file in hf/, e.g. ep08_david_stones (hf/ep08_david_stones.html)
  voice/stt from tts.py (the clone, with word timestamps) or hf/fake_stt.py (layout checks only)
  --snap    write a contact sheet of those seconds instead of rendering the MP4

The scene file has four parts, each after a marker comment:
  <!-- @config --> JSON: no, hook_kick, hook_html, turn_at, turn_html, turn_size, turn_hl,
                   question_at, question, ref, send, theme (optional CSS colour overrides)
  <!-- @css -->    the episode's own styles
  <!-- @html -->   the episode's objects (inside #stage)
  <!-- @js -->     K.run(function(tl, K){ ...beats cued with K.at("spoken words")... })
Shared look: kit.css, kit.js, template.html. Setup once per container: bash hf/setup.sh
"""
import json,os,re,shutil,subprocess,sys
HF=os.path.dirname(os.path.abspath(__file__)); ENG=os.path.dirname(HF)
sys.path.insert(0,ENG)
from episode import Voice

args=sys.argv[1:]; snap=None
if '--snap' in args: i=args.index('--snap'); snap=args[i+1]; del args[i:i+2]
name,voice,stt,out=args
src=open(os.path.join(HF,name+'.html')).read()
parts=dict(re.findall(r'<!-- @(\w+) -->\n(.*?)(?=\n<!-- @\w+ -->|\Z)',src,re.S))
cfg=json.loads(parts['config'])

v=Voice(voice,stt)
words=[{'t':w['text'],'s':round(w['start']-v.off,3),'e':round(w['end']-v.off,3)} for w in v.words]
dur=round(v.dur,2)
first_stop=next(w for w in words if re.search(r'[.?!]["”]?$',w['t']))
paper=round(v.at(cfg['turn_at'])-0.45,3)
ep={'words':words,'dur':dur,'paper':paper,'hookOff':round(first_stop['e']+0.6,3),
    'cues':{'turnHl':v.at(cfg['turn_hl']),'q':v.at(cfg['question_at'])-0.1,'send':v.at('Send this')-0.1},
    'theme':cfg.get('theme')}

work=os.path.join(ENG,'work','hf',name); shutil.rmtree(work,ignore_errors=True)
os.makedirs(os.path.join(work,'assets','fonts'))
nm=os.path.join(HF,'node_modules')
shutil.copy(os.path.join(nm,'gsap','dist','gsap.min.js'),os.path.join(work,'assets'))
for f in ['lora-latin-500-normal','lora-latin-600-normal','lora-latin-700-normal','lora-latin-500-italic']:
    shutil.copy(os.path.join(nm,'@fontsource','lora','files',f+'.woff2'),os.path.join(work,'assets','fonts'))
for f in ['inter-latin-500-normal','inter-latin-600-normal','inter-latin-800-normal']:
    shutil.copy(os.path.join(nm,'@fontsource','inter','files',f+'.woff2'),os.path.join(work,'assets','fonts'))
for f in ['kit.css','kit.js']: shutil.copy(os.path.join(HF,f),work)

html=open(os.path.join(HF,'template.html')).read()
fill={'SCENE_CSS':parts['css'],'SCENE_HTML':parts['html'],'SCENE_JS':parts['js'],'EP_JSON':json.dumps(ep),
      'DUR':str(dur),'NO':str(cfg['no']),'HOOK_KICK':cfg.get('hook_kick','PARABLE FOR BUILDERS'),'HOOK_HTML':cfg['hook_html'],
      'PAPER_START':str(paper),'PAPER_DUR':str(round(dur-paper,2)),'TURN_HTML':cfg['turn_html'],'TURN_SIZE':str(cfg.get('turn_size',104)),
      'QUESTION':cfg['question'],'REF':cfg['ref'],'SEND':cfg['send']}
for k,val in fill.items(): html=html.replace('{{'+k+'}}',val)
open(os.path.join(work,'index.html'),'w').write(html)
json.dump({'name':name},open(os.path.join(work,'meta.json'),'w'))

# voice: same clean-up as episode.py (trim, high-pass, -14 LUFS, fades)
pre=f"atrim={v.off}:{v.off+v.dur},asetpts=PTS-STARTPTS,aformat=channel_layouts=mono,highpass=f=80"
m=subprocess.run(['ffmpeg','-hide_banner','-i',voice,'-af',pre+',loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True).stderr
L=json.loads(m[m.rindex('{'):m.rindex('}')+1])
ln=('anull' if L['input_i'] in ('-inf','inf') else f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={L['input_i']}:measured_TP={L['input_tp']}:measured_LRA={L['input_lra']}:measured_thresh={L['input_thresh']}:offset={L['target_offset']}:linear=true")
subprocess.run(['ffmpeg','-y','-loglevel','error','-i',voice,'-af',f"{pre},{ln},apad=whole_dur={v.dur},afade=t=in:d=0.05,afade=t=out:st={v.dur-0.4}:d=0.4",'-ar','48000','-ac','2',os.path.join(work,'voice.wav')],check=True)

env=dict(os.environ,HYPERFRAMES_SKIP_SKILLS='1',HYPERFRAMES_NO_TELEMETRY='1')
if 'HYPERFRAMES_BROWSER_PATH' not in env:
    p=open(os.path.join(HF,'.chrome')).read().strip() if os.path.exists(os.path.join(HF,'.chrome')) else ''
    if p: env['HYPERFRAMES_BROWSER_PATH']=p
hf=os.path.join(nm,'.bin','hyperframes')
lint=subprocess.run([hf,'lint',work],capture_output=True,text=True,env=env)
errs=[l for l in lint.stdout.splitlines() if l.strip().startswith('✗')]
if errs: print('\n'.join(errs)); raise SystemExit('lint errors: fix the scene file')
if snap:
    r=subprocess.run([hf,'snapshot',work,'--at',snap],capture_output=True,text=True,env=env)
    print('\n'.join(l for l in r.stdout.splitlines() if 'contact-sheet' in l or 'rror' in l))
else:
    os.makedirs(os.path.dirname(os.path.abspath(out)),exist_ok=True)
    subprocess.run([hf,'render',work,'-o',os.path.abspath(out),'-q','delivery','--quiet'],check=True,env=env)
    print('wrote',out,f'({dur:.2f}s)')
