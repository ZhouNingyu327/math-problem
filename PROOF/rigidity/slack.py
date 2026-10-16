# Local search: minimize uncovered area of [0,a]^2 for a slightly >2, starting near a=2 families.
import numpy as np, sys
from shapely.geometry import box
from shapely import affinity
from shapely.ops import unary_union
from scipy.optimize import minimize
def sq(cx,cy,t): return affinity.rotate(box(cx-.5,cy-.5,cx+.5,cy+.5),t,origin=(cx,cy),use_radians=True)
def unc(x,a):
    P=x.reshape(6,3); return box(0,0,a,a).difference(unary_union([sq(*p) for p in P])).area
grid=np.array([[.5,.5,0],[1.5,.5,0],[.5,1.5,0],[1.5,1.5,0],[1,1,.785],[1,1,0]])
tilt=np.array([[.5,.5,0],[1.5,.5,0],[.3,1.7,.349],[1.5,1.5,0],[.55,1.5,0],[-.4,1.4,0]])
if __name__=="__main__":
 rng=np.random.default_rng(0)
 for name,x0 in [("grid",grid),("tilt",tilt)]:
   for a in [2.001,2.01,2.03]:
     best=9
     for k in range(6):
       x=(x0*[a/2,a/2,1]).ravel()+rng.normal(0,.02,18)
       r=minimize(unc,x,args=(a,),method="Powell",options={"maxiter":4000,"xtol":1e-7,"ftol":1e-12})
       best=min(best,r.fun)
     print(name,a,"min uncovered",best,"ratio/(a-2)",best/(a-2),flush=True)
