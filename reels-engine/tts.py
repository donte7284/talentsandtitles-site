"""Clone narration with word timestamps, ready for an episode script.

usage: python tts.py <voice_id> <text.txt> <out.wav> <out.stt.json>
Calls ElevenLabs text-to-speech "with timestamps" (the API key is added by the environment),
pads 0.35 s of lead-in to match a trimmed phone take, and writes word timings in the same
shape as speech-to-text output so ep01_widow.py etc. can use either.
"""
import base64,json,subprocess,sys,tempfile
voice_id,txt,wav,stt=sys.argv[1:5]
LEAD=0.35
text=open(txt).read().strip()
with tempfile.TemporaryDirectory() as d:
    open(f'{d}/req.json','w').write(json.dumps({'text':text,'model_id':'eleven_multilingual_v2'}))
    # mp3_44100_128: higher bitrates need the Creator tier
    code=subprocess.run(['curl','-sS','-o',f'{d}/resp.json','-w','%{http_code}','-X','POST',
        f'https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/with-timestamps?output_format=mp3_44100_128',
        '-H','Content-Type: application/json','--data-binary',f'@{d}/req.json'],capture_output=True,text=True,check=True).stdout
    r=json.load(open(f'{d}/resp.json'))
    if code!='200':raise SystemExit(f'HTTP {code}: {json.dumps(r)[:400]}')
    open(f'{d}/a.mp3','wb').write(base64.b64decode(r['audio_base64']))
    subprocess.run(['ffmpeg','-y','-loglevel','error','-i',f'{d}/a.mp3','-af',f'adelay={int(LEAD*1000)}:all=1','-ar','48000',wav],check=True)
a=r['alignment'];words=[];cur=None
for c,s,e in zip(a['characters'],a['character_start_times_seconds'],a['character_end_times_seconds']):
    if c.isspace():
        if cur:words.append(cur);cur=None
        continue
    if cur is None:cur={'text':'','start':s+LEAD,'end':e+LEAD,'type':'word'}
    cur['text']+=c;cur['end']=e+LEAD
if cur:words.append(cur)
json.dump({'text':text,'words':words,'source':'tts-with-timestamps'},open(stt,'w'))
print(len(words),'words,',round(words[-1]['end'],2),'s')
