import numpy as np
from scipy.optimize import minimize
def chord(x,zx,zy,th):
    # vertical line at x: interval of y with |u|,|v|<=.5
    c,s=np.cos(th),np.sin(th); dx=x-zx
    lo,hi=-1e9,1e9
    # u=dx*c+dy*s, v=-dx*s+dy*c  (dy=y-zy)
    for (k0,k1) in [(dx*c,s),(-dx*s,c)]:
        if abs(k1)<1e-12:
            if abs(k0)>.5: return None
            continue
        a1,a2=(-.5-k0)/k1,(.5-k0)/k1
        lo=max(lo,min(a1,a2)); hi=min(hi,max(a1,a2))
    if lo>hi: return None
    return zy+lo,zy+hi
def neg(p,w):
    zx,zy,th=p
    c0=chord(0,zx,zy,th); c1=chord(w,zx,zy,th)
    if c0 is None or c1 is None: return 10
    pen=max(0,c0[0])+max(0,c1[0])   # need y=0 inside chord at both ends => lo<=0<=hi
    if c0[1]<0 or c1[1]<0: return 10
    return -(c0[1]+c1[1])/2+100*pen
def T(w):
    best=0;rng=np.random.default_rng(0)
    for _ in range(300):
        p0=[rng.uniform(-.5,w+.5),rng.uniform(0,1),rng.uniform(0,np.pi/2)]
        r=minimize(neg,p0,args=(w,),method="Nelder-Mead",options={"xatol":1e-10,"fatol":1e-12,"maxiter":4000})
        if r.fun<0 and neg(r.x,w)<=0: best=max(best,-neg(r.x,w))
    return best
for w in [0.40,0.45,0.48,0.5,0.52,0.55,0.6,0.7]: print(w,T(w),flush=True)
