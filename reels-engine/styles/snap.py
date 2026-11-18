# snap.py name t1 t2 ... -> contact strip png of frames from mp4
import os; B=os.path.dirname(os.path.abspath(__file__))
import sys,subprocess
n=sys.argv[1]; ts=sys.argv[2:]
fs=[]
for i,t in enumerate(ts):
    f=f'{B}/frames/{n}_{i}.png'
    subprocess.run(['ffmpeg','-y','-loglevel','error','-ss',t,'-i',f'{B}/out/{n}.mp4','-frames:v','1','-vf','scale=360:-1',f],check=True); fs.append(f)
subprocess.run(['ffmpeg','-y','-loglevel','error']+sum([['-i',f] for f in fs],[])+['-filter_complex',f'hstack=inputs={len(fs)}' if len(fs)>1 else 'null',f'{B}/frames/{n}_strip.png'],check=True)
