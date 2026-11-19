# geo.py <outdir> <lon0> <lon1> <toplat> : project world-atlas coastlines/countries into a 1080-wide map frame
# starting at y=250, and rasterize a country grid (270 x 311 cells of 4px). Longitudes are unwrapped so maps
# can cross the date line (e.g. the Pacific: lon0=95, lon1=205).
import json, math, base64, sys, os
from PIL import Image, ImageDraw
import numpy as np
OUT=sys.argv[1] if len(sys.argv)>1 else os.path.dirname(os.path.abspath(__file__))
LON0=float(sys.argv[2]) if len(sys.argv)>2 else -12; LON1=float(sys.argv[3]) if len(sys.argv)>3 else 48; TOPLAT=float(sys.argv[4]) if len(sys.argv)>4 else 68
S=1080/(LON1-LON0); Y0=250; CEN=(LON0+LON1)/2
def my(lat): return math.degrees(math.log(math.tan(math.pi/4+math.radians(lat)/2)))
TOP=my(TOPLAT)
def P(lon,lat): return ((lon-LON0)*S, Y0+(TOP-my(lat))*S)
GW,GH=270,311
BOT=TOP-(GH*4)/S;BOTLAT=math.degrees(2*math.atan(math.exp(math.radians(BOT)))-math.pi/2)
def topo_polys(path,obj):
    d=json.load(open(path));tr=d['transform'];sx,sy=tr['scale'];tx,ty=tr['translate']
    arcs=[]
    for a in d['arcs']:
        x=y=0;pts=[]
        for dx,dy in a:x+=dx;y+=dy;pts.append((x*sx+tx,y*sy+ty))
        arcs.append(pts)
    def ring(ix):
        out=[]
        for i in ix:
            a=arcs[i] if i>=0 else arcs[~i][::-1]
            out+=a[1:] if out else a
        # unwrap, then move the ring next to the map centre
        u=[out[0]]
        for x,y in out[1:]:
            px=u[-1][0]
            while x-px>180:x-=360
            while x-px<-180:x+=360
            u.append((x,y))
        mx=sum(x for x,_ in u)/len(u);k=round((CEN-mx)/360)
        return [(x+360*k,y) for x,y in u]
    res=[]
    for g in d['objects'][obj]['geometries']:
        polys=[]
        if g['type']=='Polygon':polys=[[ring(r) for r in g['arcs']]]
        elif g['type']=='MultiPolygon':polys=[[ring(r) for r in p] for p in g['arcs']]
        res.append((g.get('properties',{}).get('name',''),polys))
    return res
NM=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'node_modules','world-atlas')+'/'
inb=lambda r:any(LON0-4<x<LON1+4 and BOTLAT-4<y<TOPLAT+4 for x,y in r)
parts=[]
for _,polys in topo_polys(NM+'land-50m.json','land'):
    for p in polys:
        for r in p:
            if not inb(r):continue
            r=[(max(LON0-40,min(LON1+40,x)),max(-85,min(85,y))) for x,y in r]
            pts=[P(*q) for q in r];out=[pts[0]]
            for q in pts[1:]:
                if abs(q[0]-out[-1][0])+abs(q[1]-out[-1][1])>1.4:out.append(q)
            if len(out)<3:
                if len(pts)>=3:out=pts[::max(1,len(pts)//4)]
                if len(out)<3:continue
            parts.append('M'+'L'.join(f'{x:.1f},{y:.1f}' for x,y in out)+'Z')
land=''.join(parts)
names=['']
img=Image.new('I',(GW*2,GH*2),0);dr=ImageDraw.Draw(img)
small=[]
for name,polys in topo_polys(NM+'countries-50m.json','countries'):
    if not any(inb(r) for p in polys for r in p):continue
    names.append(name);k=len(names)-1
    for p in polys:
        for i,r in enumerate(p):
            pts=[(P(x,y)[0]/2,(P(x,y)[1]-Y0)/2) for x,y in r]
            if len(pts)>2:dr.polygon(pts,fill=k if i==0 else 0)
            if i==0:small.append((k,pts))
a=np.array(img,dtype=np.int32)
cells=np.zeros((GH,GW),np.uint8)
for j in range(GH):
    for i in range(GW):
        b=a[2*j:2*j+2,2*i:2*i+2].ravel();nz=b[b>0]
        if len(nz)>=2: cells[j,i]=np.bincount(nz).argmax()
# keep small islands: any ring whose cells all vanished gets its centre cell
for k,pts in small:
    xs=[p[0]/2 for p in pts];ys=[p[1]/2 for p in pts]
    if max(xs)-min(xs)>3 or max(ys)-min(ys)>3:continue
    i=int(sum(xs)/len(xs));j=int(sum(ys)/len(ys))
    if 0<=i<GW and 0<=j<GH and cells[j,i]==0:cells[j,i]=k
assert len(names)<256
json.dump({'names':names,'cells':base64.b64encode(cells.tobytes()).decode(),'land':land,'sc':S,'lon0':LON0,'top':TOPLAT},open(os.path.join(OUT,'geo.json'),'w'))
print(len(names),'countries;',len(land)//1024,'KB land path; land cells',int((cells>0).sum()),'; bottom lat %.1f'%BOTLAT)
