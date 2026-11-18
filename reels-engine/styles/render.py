import sys, subprocess, os, time
from playwright.sync_api import sync_playwright
FPS=30
names=sys.argv[1:]
base=os.path.dirname(os.path.abspath(__file__))
with sync_playwright() as pw:
    b=pw.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
    for n in names:
        t0=time.time()
        pg=b.new_page(viewport={'width':1080,'height':1920})
        pg.on('console', lambda m: print('  console:',m.text) if m.type in ('error','warning') and 'GL Driver' not in m.text else None)
        pg.on('pageerror', lambda e: print('  PAGEERROR',e))
        pg.goto(f'http://localhost:8765/s/{n}.html')
        pg.wait_for_function('window.READY===true', timeout=60000)
        dur=pg.evaluate('window.DUR||4')
        nf=int(dur*FPS)
        ff=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','image2pipe','-framerate',str(FPS),'-i','-','-c:v','libx264','-preset','veryfast','-pix_fmt','yuv420p','-crf','20','-movflags','+faststart',f'{base}/out/{n}.mp4'],stdin=subprocess.PIPE)
        for i in range(nf):
            pg.evaluate(f'window.render({i/FPS})')
            ff.stdin.write(pg.screenshot(type='jpeg',quality=90))
        ff.stdin.close(); ff.wait()
        pg.close()
        print(f'{n}: {nf} frames in {time.time()-t0:.0f}s', flush=True)
    b.close()
