"""Layout-check timings without a voice: silent audio + word times at the series pace (about 165 wpm).

usage: python hf/fake_stt.py narration/epNN_slug.txt work/epNN_fake.wav work/epNN_fake.stt.json
Use only to look at frames (build.py --snap). Real episodes always use tts.py timings.
"""
import json,re,subprocess,sys
txt,wav,stt=sys.argv[1:4]
text=open(txt).read().strip(); t=0.35; words=[]
for tok in re.split(r'(<break[^>]*>)',text):
    if tok.startswith('<break'):
        t+=float(re.search(r'([\d.]+)s',tok).group(1)); continue
    for w in tok.split():
        d=0.11+0.032*len(re.sub(r'[^A-Za-z]','',w))
        words.append({'text':w,'start':round(t,3),'end':round(t+d,3),'type':'word'}); t+=d+0.03
        if re.search(r'[.?!]["”]?$',w): t+=0.28
        elif re.search(r'[,:;]$',w): t+=0.14
dur=t+0.9
subprocess.run(['ffmpeg','-y','-loglevel','error','-f','lavfi','-i','anoisesrc=a=0.02:c=pink:r=48000','-t',str(dur),wav],check=True)
json.dump({'text':text,'words':words,'source':'fake'},open(stt,'w'))
print(len(words),'words,',round(t,2),'s')
