# Pacific theatre fronts. m = months since 1 Dec 1941.
import json, math, os, sys
HERE=os.path.dirname(os.path.abspath(__file__))
def M(s):
    y,mo,d=map(int,s.split('-'));return (y-1941)*12+(mo-12)+(d-1)/30
G=json.load(open(os.path.join(HERE,'geo.json')));S=G['sc'];Y0=250
def my(lat): return math.degrees(math.log(math.tan(math.pi/4+math.radians(lat)/2)))
TOP=my(G['top']);GH=311
ROWLAT=[math.degrees(2*math.atan(math.exp(math.radians(TOP-(j*4+2)/S)))-math.pi/2) for j in range(GH)]
def rows(pts,lo,hi):
    ks=sorted(pts.items());out=[]
    for la in ROWLAT:
        if la<lo or la>hi: out.append(None);continue
        if la<=ks[0][0]: out.append(ks[0][1]);continue
        if la>=ks[-1][0]: out.append(ks[-1][1]);continue
        for (a,va),(b,vb) in zip(ks,ks[1:]):
            if a<=la<=b: out.append(round(va+(vb-va)*(la-a)/(b-a),3));break
    return out
# China: Japan holds everything east of this line (lon at each latitude)
N41={18:115,21:115,22:113.6,22.8:113.0,23.5:113.2,23.8:116.4,24.6:117.9,25.5:120.0,27.5:121.2,28.6:116.0,29.4:112.9,30.3:112.6,30.7:111.3,31.5:112.2,32.2:113.8,33.0:114.3,34.0:114.2,34.8:113.8,35.2:112.2,36:111.6,37:111.3,38:111.4,39:111.0,40:110.0,41:109.5,42:111.5}
def upd(base,**k):
    d=dict(base);d.update({float(a.replace('_','.').lstrip('n')):v for a,v in k.items()});return d
H44=dict(N41);H44.update({33.0:112.6,34.0:112.0,34.8:111.6,35.2:111.6})
C44=dict(H44);C44.update({29.4:112.6,28.2:112.4,27.5:113.0,27.0:114.0,26.5:116.0})
A44=dict(H44);A44.update({29.4:112.4,28.2:112.0,27.0:112.3,26.5:112.6,26.0:113.2,25.5:114.0})
N44=dict(H44);N44.update({29.4:112.0,28.2:111.6,27.0:111.2,26.0:110.4,25.3:110.0,24.3:109.0,23.5:108.5,22.8:107.9,22.0:106.8,21.5:107.5,24.6:112.0,25.5:112.5})
J45=dict(N44);J45.update({24.0:113.5,24.6:114.0,25.5:114.5})
M45=dict(J45);M45.update({22.8:108.8,22.0:109.5,21.5:110.0})
L45=dict(M45);L45.update({25.3:111.0,24.3:110.6,23.5:110.6,22.8:110.4,22.0:111.0,21.5:111.0,26.0:111.0,27.0:111.5})
CF=[(M('1941-11-01'),N41),(M('1944-04-17'),N41),(M('1944-05-31'),H44),(M('1944-06-30'),C44),(M('1944-08-31'),A44),(M('1944-11-30'),N44),(M('1945-02-15'),J45),(M('1945-05-31'),M45),(M('1945-07-31'),L45)]
D={'CF':[[m,rows(p,18,42)] for m,p in CF],'rowlat':[round(v,4) for v in ROWLAT],
 # Burma: Japan holds south of BL; Allies retake north of BR
 'BL':[[M('1942-01-20'),9.5],[M('1942-02-20'),15.5],[M('1942-03-08'),17.3],[M('1942-04-15'),20.0],[M('1942-05-01'),22.5],[M('1942-05-20'),28.6]],
 'BR':[[M('1944-03-01'),28.6],[M('1944-08-03'),25.3],[M('1944-12-15'),24.2],[M('1945-01-31'),23.0],[M('1945-03-20'),21.5],[M('1945-04-15'),19.5],[M('1945-05-03'),16.5],[M('1945-06-30'),15.0],[M('1945-08-14'),14.5]],
 # Malaya: Japan holds north of MF
 'MF':[[M('1941-12-08'),6.6],[M('1941-12-20'),5.0],[M('1942-01-11'),3.1],[M('1942-01-31'),1.45],[M('1942-02-15'),1.0]]}
json.dump(D,open(os.path.join(HERE,'fronts.json'),'w'))
print('ok')
