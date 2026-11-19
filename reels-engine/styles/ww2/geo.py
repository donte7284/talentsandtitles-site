import os
_B=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Projects world-atlas coastlines/countries into the WW2 map frame and rasterizes a country grid.
import json, math, base64
from PIL import Image, ImageDraw
import numpy as np
S=18.0; Y0=250
def my(lat): return math.degrees(math.log(math.tan(math.pi/4+math.radians(lat)/2)))
TOP=my(68)
def P(lon,lat): return ((lon+12)*S, Y0+(TOP-my(lat))*S)
GW,GH,G=270,311,4
def topo_polys(path,obj):
    d=json.load(open(path));tr=d['transform'];sx,sy=tr['scale'];tx,ty=tr['translate']
    arcs=[]
    for a in d['arcs']:
        x=y=0;pts=[]
        for dx,dy in a:x+=dx;y+=dy;pts.append((x*sx+tx,y*sy+ty))
        arcs.append([(x+360 if x<-100 else x,y) for x,y in pts])
    def ring(ix):
        out=[]
        for i in ix:
            a=arcs[i] if i>=0 else arcs[~i][::-1]
            out+=a[1:] if out else a
        return out
    res=[]
    for g in d['objects'][obj]['geometries']:
        polys=[]
        if g['type']=='Polygon':polys=[[ring(r) for r in g['arcs']]]
        elif g['type']=='MultiPolygon':polys=[[ring(r) for r in p] for p in g['arcs']]
        res.append((g.get('properties',{}).get('name',''),polys))
    return res
NM=_B+'/node_modules/world-atlas/'
inb=lambda r:any(-16<x<53 and 19<y<72 for x,y in r)
# land outline as an SVG path (projected, lightly simplified)
parts=[]
for _,polys in topo_polys(NM+'land-50m.json','land'):
    for p in polys:
        for r in p:
            if not inb(r):continue
            r=[(max(-30,min(70,x)),max(10,min(80,y))) for x,y in r]
            pts=[P(*q) for q in r];out=[pts[0]]
            for q in pts[1:]:
                if abs(q[0]-out[-1][0])+abs(q[1]-out[-1][1])>1.4:out.append(q)
            if len(out)<3:continue
            parts.append('M'+'L'.join(f'{x:.1f},{y:.1f}' for x,y in out)+'Z')
land=''.join(parts)
# country raster at 2x then majority-downsample to the 4px grid
names=['']
img=Image.new('I',(GW*2,GH*2),0);dr=ImageDraw.Draw(img)
for name,polys in topo_polys(NM+'countries-50m.json','countries'):
    if not any(inb(r) for p in polys for r in p):continue
    names.append(name);k=len(names)-1
    for p in polys:
        for i,r in enumerate(p):
            pts=[(P(x,y)[0]/2,(P(x,y)[1]-Y0)/2) for x,y in r]
            if len(pts)>2:dr.polygon(pts,fill=k if i==0 else 0)
a=np.array(img,dtype=np.int32)
cells=np.zeros((GH,GW),np.uint8)
for j in range(GH):
    for i in range(GW):
        b=a[2*j:2*j+2,2*i:2*i+2].ravel();nz=b[b>0]
        if len(nz)>=2: cells[j,i]=np.bincount(nz).argmax()
assert len(names)<256
json.dump({'names':names,'cells':base64.b64encode(cells.tobytes()).decode(),'land':land},open(_B+'/ww2/geo.json','w'))
print(len(names),'countries;',len(land)//1024,'KB land path; land cells',int((cells>0).sum()))
print([n for n in names])
