import os,sys,shutil,subprocess
from playwright.sync_api import sync_playwright
# usage: python render.py <seconds> <out.mp4> <scene.html>
D=float(sys.argv[1]);FPS=30
base=os.path.dirname(os.path.abspath(__file__))
frames=f'{base}/frames'
shutil.rmtree(frames,ignore_errors=True);os.makedirs(frames)  # stale frames from a longer render would leak into the video
with sync_playwright() as pw:
    ex='/opt/pw-browsers/chromium'
    b=pw.chromium.launch(executable_path=ex) if os.path.isfile(ex) else pw.chromium.launch()
    pg=b.new_page(viewport={'width':1080,'height':1920})
    pg.goto('file://'+base+'/'+sys.argv[3]);pg.wait_for_timeout(600)
    n=int(D*FPS)
    for i in range(n):
        pg.evaluate(f'render({i/FPS})')
        pg.screenshot(path=f'{frames}/{i:05d}.jpg',type='jpeg',quality=93)
    b.close()
subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate',str(FPS),'-i',f'{frames}/%05d.jpg','-c:v','libx264','-pix_fmt','yuv420p','-crf','18','-movflags','+faststart',sys.argv[2]],check=True)
