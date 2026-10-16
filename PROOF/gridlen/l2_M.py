import numpy as np
from scipy.optimize import minimize
from shapely.geometry import box, LineString
from shapely import affinity
n=4;a=4.001;q=a/n;S=box(0,0,a,a)
H=[LineString([(0,k*q),(a,k*q)]) for k in range(n+1)];Vv=[LineString([(k*q,0),(k*q,a)]) for k in range(n+1)]
sides=[H[0],H[n],Vv[0],Vv[n]]
def f(x,lam):
    cx,cy,th=x
    T=affinity.rotate(box(cx-.5,cy-.5,cx+.5,cy+.5),th,origin=(cx,cy),use_radians=True)
    if sum(T.intersects(s) for s in sides)!=1 or not T.intersects(H[0]): return 0
    TS=T.intersection(S); return -(sum(TS.intersection(l).length for l in H+Vv)+lam*TS.intersection(H[0]).length)
rng=np.random.default_rng(3)
for lam in [0.0,0.1]:
    best=0
    for k in range(400):
        x0=[q+rng.uniform(-.6,.6),rng.uniform(-.2,.75),rng.uniform(0,np.pi/2)] if k else [q,np.sqrt(2)/2-1e-6,np.pi/4]
        r=minimize(f,x0,args=(lam,),method="Nelder-Mead",options={"xatol":1e-9,"fatol":1e-11})
        best=min(best,r.fun)
    print("lam",lam,"M approx",-best,flush=True)
