# n=4: sample single-sided tiles near the bottom side, record (p = bottom-side coverage, g = total grid coverage).
import numpy as np, json
from shapely.geometry import box, LineString
from shapely import affinity
n=4; a=4.001; q=a/n
S=box(0,0,a,a)
H=[LineString([(0,k*q),(a,k*q)]) for k in range(n+1)]; Vv=[LineString([(k*q,0),(k*q,a)]) for k in range(n+1)]
sides=[H[0],H[n],Vv[0],Vv[n]]
rng=np.random.default_rng(5); pts=[]
for _ in range(300000):
    cx=rng.uniform(.75,a-.75); cy=rng.uniform(-.7,.75); th=rng.uniform(0,np.pi/2)
    T=affinity.rotate(box(cx-.5,cy-.5,cx+.5,cy+.5),th,origin=(cx,cy),use_radians=True)
    if sum(T.intersects(s) for s in sides)!=1 or not T.intersects(H[0]): continue
    TS=T.intersection(S)
    p=TS.intersection(H[0]).length
    g=sum(TS.intersection(l).length for l in H+Vv)
    pts.append((p,g))
P=np.array(pts); print("samples",len(P),"max g",P[:,1].max(),"max p",P[:,0].max())
r2=np.sqrt(2)
res={}
for lam in [0,0.1,0.2,0.3,0.5,0.75,1.0]:
    M=(P[:,1]+lam*P[:,0]).max()
    ok=[]
    for nc in range(5):
        for nd in range(4+nc,18):
            if nc==0 and nd>4: continue
            for ns in range(0,18-nd):
                ni=17-nd-ns
                if 2*(4-nc)+2*r2*nc+r2*ns<=16: continue
                Pneed=16-2*(4-nc)-2*r2*nc   # single-sided tiles must cover at least this much perimeter
                gbound=2*nd+ns*M-lam*max(0,Pneed)+2*r2*ni
                if gbound<=40: continue
                ok.append((nc,nd,ns))
    res[lam]=(M,ok); print("lam",lam,"M(lam)=%.4f"%M,"survivors",ok)
json.dump({str(k):v for k,v in res.items()},open("l2_repair.json","w"))
