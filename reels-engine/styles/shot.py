# shot.py name t1 t2 ... -> frames/<name>_t<t>.png straight from the page (no video), with timing
import sys,time,os
from playwright.sync_api import sync_playwright
n=sys.argv[1];ts=[float(x) for x in sys.argv[2:]]
with sync_playwright() as pw:
    b=pw.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
    pg=b.new_page(viewport={'width':1080,'height':1920})
    pg.on('pageerror',lambda e:print('PAGEERROR',e));pg.on('console',lambda m:print('console:',m.text) if m.type=='error' else None)
    t0=time.time();pg.goto(f'http://localhost:8765/s/{n}.html');pg.wait_for_function('window.READY===true',timeout=120000);print('load',round(time.time()-t0,1))
    for t in ts:
        t1=time.time();pg.evaluate(f'window.render({t})');r=time.time()-t1
        pg.screenshot(path=os.path.dirname(os.path.abspath(__file__))+f'/frames/{n}_t{t}.png');print(t,'render',round(r,2))
    b.close()
