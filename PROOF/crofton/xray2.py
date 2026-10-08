import numpy as np, math, sys
from xray import deficit
from scipy.optimize import minimize
a=float(sys.argv[1]); rng=np.random.default_rng(int(sys.argv[2]))
q=a/4
starts=[]
for sp in [[(a/2,a/2-0.45,math.pi/4),(a/2,a/2+0.45,math.pi/4)],[(a/2-0.45,a/2,math.pi/4),(a/2+0.45,a/2,math.pi/4)],
           [(a/2,a/2,math.pi/4),(a/2,a/2,0.0)],[(a/2-0.3,a/2-0.3,0.3),(a/2+0.3,a/2+0.3,1.2)]]:
    x=[q,q,0,3*q,q,0,q,3*q,0,3*q,3*q,0]+[v for p in sp for v in p]
    starts.append(np.array(x))
best=None
for x0 in starts+[s+rng.normal(0,0.05,18) for s in starts]:
    f=lambda x: deficit(x,a)
    r=minimize(f,x0,method='Powell',options={'maxfev':8000,'xtol':1e-8,'ftol':1e-15})
    r=minimize(f,r.x,method='Nelder-Mead',options={'maxfev':8000,'xatol':1e-9,'fatol':1e-16,'adaptive':True})
    tot,mx=deficit(r.x,a,True); print(f"a={a} sumsq={tot:.3e} max={mx:.3e}",flush=True)
    if best is None or tot<best[0]: best=(tot,mx,r.x)
    if mx<1e-9: break
print("BEST",best[0],best[1],best[2].round(6).tolist())
