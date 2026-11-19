# render_fast.py name [name ...] [--workers N] [--fps F] [--scale S]
# Faster renderer: splits each video into chunks rendered in parallel worker processes, and grabs frames
# straight from the page's drawing canvas (window.CAPTURE) instead of taking full-page screenshots.
# Pages without window.CAPTURE fall back to screenshots. Chunks are joined without re-encoding.
import sys, os, subprocess, time, base64, argparse
from multiprocessing import Process
from playwright.sync_api import sync_playwright
base = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser()
ap.add_argument('names', nargs='+')
ap.add_argument('--workers', type=int, default=os.cpu_count() or 2)
ap.add_argument('--fps', type=int, default=30)
ap.add_argument('--scale', type=float, default=1.0, help='0.5 = half-size draft')
A = ap.parse_args()
ARGS = ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist']

def open_page(b, n):
    pg = b.new_page(viewport={'width': 1080, 'height': 1920})
    pg.on('pageerror', lambda e: print('  PAGEERROR', n, e, flush=True))
    pg.goto(f'http://localhost:8765/s/{n}.html')
    pg.wait_for_function('window.READY===true', timeout=120000)
    return pg

GRAB = '''([t,s])=>{window.render(t);const c=window.CAPTURE;let src=c;
 if(s!=1){if(!window._sc){window._sc=document.createElement('canvas')}const o=window._sc;o.width=Math.round(c.width*s);o.height=Math.round(c.height*s);o.getContext('2d').drawImage(c,0,0,o.width,o.height);src=o}
 return src.toDataURL('image/jpeg',0.92).slice(23)}'''

def worker(n, i0, i1, part):
    w, h = int(1080 * A.scale) // 2 * 2, int(1920 * A.scale) // 2 * 2
    with sync_playwright() as pw:
        b = pw.chromium.launch(args=ARGS)
        pg = open_page(b, n)
        canvas = pg.evaluate('!!window.CAPTURE')
        ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', str(A.fps), '-i', '-',
                               '-vf', f'scale={w}:{h}', '-c:v', 'libx264', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', '-crf', '20', part], stdin=subprocess.PIPE)
        for i in range(i0, i1):
            t = i / A.fps
            if canvas:
                ff.stdin.write(base64.b64decode(pg.evaluate(GRAB, [t, A.scale])))
            else:
                pg.evaluate(f'window.render({t})')
                ff.stdin.write(pg.screenshot(type='jpeg', quality=90))
        ff.stdin.close(); ff.wait(); b.close()

if __name__ == '__main__':
    os.makedirs(f'{base}/out/parts', exist_ok=True)
    with sync_playwright() as pw:
        b = pw.chromium.launch(args=ARGS)
        durs = {}
        for n in A.names:
            pg = open_page(b, n); durs[n] = pg.evaluate('window.DUR||4'); pg.close()
        b.close()
    t0 = time.time()
    # one queue of chunks across all videos, run W at a time
    jobs = []
    for n in A.names:
        nf = int(durs[n] * A.fps); k = A.workers
        cuts = [nf * j // k for j in range(k + 1)]
        for j in range(k):
            jobs.append((n, cuts[j], cuts[j + 1], f'{base}/out/parts/{n}_{j:02d}.mp4'))
    running = []
    while jobs or running:
        while jobs and len(running) < A.workers:
            p = Process(target=worker, args=jobs.pop(0)); p.start(); running.append(p)
        running[0].join(); running.pop(0)
    suffix = '' if A.scale == 1 else '_draft'
    for n in A.names:
        parts = sorted(f for f in os.listdir(f'{base}/out/parts') if f.startswith(n + '_') and f[len(n) + 1:-4].isdigit())
        lst = f'{base}/out/parts/{n}.txt'
        open(lst, 'w').write(''.join(f"file '{base}/out/parts/{f}'\n" for f in parts))
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', '-movflags', '+faststart', f'{base}/out/{n}{suffix}.mp4'], check=True)
        for f in parts: os.remove(f'{base}/out/parts/{f}')
        os.remove(lst)
    print(f'{len(A.names)} video(s) in {time.time()-t0:.0f}s with {A.workers} workers', flush=True)
