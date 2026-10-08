"""Shared steps for an episode timed to a voiceover.

An episode script loads a Voice (audio + word timestamps), reads cue times with v.at(...),
builds its scene HTML with base.build(), then calls v.finish(...) to clean the audio, render
and mux. Word timestamps come from speech-to-text (a real take) or tts.py (the clone).
"""
import json,os,re,subprocess,sys
HERE=os.path.dirname(os.path.abspath(__file__))
norm=lambda s:re.sub(r"[^a-z']",'',s.lower())

class Voice:
    LEAD,TAIL=0.35,0.9
    def __init__(self,voice,stt):
        self.voice=voice
        self.words=[w for w in json.load(open(stt))['words'] if w['type']=='word']
        # speech-to-text can start a word at the end of the previous one when a pause sits between them;
        # move any word start that falls inside a detected silence to where the voice actually begins
        sd=subprocess.run(['ffmpeg','-hide_banner','-i',voice,'-af','silencedetect=n=-40dB:d=0.15','-f','null','-'],capture_output=True,text=True).stderr
        sil=list(zip(map(float,re.findall(r'silence_start: ([\d.]+)',sd)),map(float,re.findall(r'silence_end: ([\d.]+)',sd))))
        for w in self.words:
            for s0,s1 in sil:
                if s0-0.1<=w['start']<s1-0.05 and s1<w['end']:w['start']=s1
        self.toks=[norm(w['text']) for w in self.words]
        self.off=max(0,self.words[0]['start']-self.LEAD)
        self.dur=self.words[-1]['end']+self.TAIL-self.off

    def at(self,phrase,nth=1,end=False):
        """time (s, trimmed) of the nth occurrence of a phrase; its first word's start, or last word's end"""
        p=[norm(x) for x in phrase.split()];n=0
        for i in range(len(self.toks)-len(p)+1):
            if self.toks[i:i+len(p)]==p:
                n+=1
                if n==nth:return round((self.words[i+len(p)-1]['end'] if end else self.words[i]['start'])-self.off,3)
        raise SystemExit(f'phrase not in recording: {phrase!r} #{nth}')

    def capw(self,cap):
        """per-word caption times: anchored where the caption's first two words are spoken together,
        then each caption word at its next spoken occurrence (spoken extras are skipped)"""
        p=[norm(w[0]) for w in cap]
        i=next((i for i in range(len(self.toks)) if self.toks[i:i+2]==p[:2]),None)
        if i is None:raise SystemExit(f'caption start not in recording: {p[:2]}')
        out=[]
        for w in p:
            while self.toks[i]!=w:i+=1
            out.append(round(self.words[i]['start']-self.off-0.08,3));i+=1
        return out

    def finish(self,tag,html,out):
        """voice: trim, high-pass, two-pass loudness normalise to -14 LUFS, pad, fades; then render and mux"""
        os.makedirs(os.path.join(HERE,'out'),exist_ok=True)
        wav=os.path.join(HERE,'out',f'{tag}_voice.wav')
        pre=f"atrim={self.off}:{self.off+self.dur},asetpts=PTS-STARTPTS,aformat=channel_layouts=mono,highpass=f=80"
        m=subprocess.run(['ffmpeg','-hide_banner','-i',self.voice,'-af',pre+',loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True).stderr
        L=json.loads(m[m.rindex('{'):m.rindex('}')+1])
        ln=f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={L['input_i']}:measured_TP={L['input_tp']}:measured_LRA={L['input_lra']}:measured_thresh={L['input_thresh']}:offset={L['target_offset']}:linear=true"
        subprocess.run(['ffmpeg','-y','-loglevel','error','-i',self.voice,'-af',f"{pre},{ln},apad=whole_dur={self.dur},afade=t=in:d=0.05,afade=t=out:st={self.dur-0.4}:d=0.4",'-ar','48000',wav],check=True)
        silent=os.path.join(HERE,'out',f'{tag}_silent.mp4')
        subprocess.run([sys.executable,os.path.join(HERE,'render.py'),str(round(self.dur,2)),silent,os.path.basename(html)],check=True)
        subprocess.run(['ffmpeg','-y','-loglevel','error','-i',silent,'-i',wav,'-c:v','copy','-c:a','aac','-b:a','192k','-ac','2','-shortest','-movflags','+faststart',out],check=True)
        print('wrote',out,f'({self.dur:.2f}s)')
