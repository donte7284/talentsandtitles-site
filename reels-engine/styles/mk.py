# mk.py: wrap a JS module body into a page. usage from python: page(name,bg,js)
HEAD='''<!doctype html><html><head><meta charset="utf-8"><style>
*{margin:0;padding:0;box-sizing:border-box}body{width:1080px;height:1920px;overflow:hidden;background:%s;font-family:Inter}
%s</style></head><body>%s
<script type="importmap">{"imports":{"three":"/node_modules/three/build/three.module.js","three/addons/":"/node_modules/three/examples/jsm/"}}</script>
<script type="module">
import * as THREE from 'three';import {buildOffice} from './office.js';import {cl,pr,eo,eio,eob,rng,lerp} from './lib.js';
%s
window.READY=true;
</script></body></html>'''
def page(name,bg,js,css='',html=''):
    import os; open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'s',f'{name}.html'),'w').write(HEAD%(bg,css,html,js))
