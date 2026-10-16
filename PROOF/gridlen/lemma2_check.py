# Counter-check of Lemma 2 (single-sided tile covers <=1.5*sqrt2 of grid) for n=2.
from shapely.geometry import box, LineString
from shapely import affinity
import numpy as np
def tile(cx,cy,t): return affinity.rotate(box(cx-.5,cy-.5,cx+.5,cy+.5),t,origin=(cx,cy),use_radians=True)
def cov(T,a):
    S=box(0,0,a,a); m=a/2
    L=[LineString([(0,0),(a,0)]),LineString([(0,a),(a,a)]),LineString([(0,0),(0,a)]),LineString([(a,0),(a,a)]),
       LineString([(0,m),(a,m)]),LineString([(m,0),(m,a)])]
    sides=sum(1 for l in L[:4] if T.intersects(l))
    return sides,sum(T.intersection(S).intersection(l).length for l in L)
if __name__=="__main__":
    a=2.001
    
    T=tile(a/2,np.sqrt(2)/2-1e-9,np.pi/4)
    print("example 45deg tile at (a/2,0.7071):",cov(T,a),"vs 1.5sqrt2=",1.5*np.sqrt(2))
    best=(0,None);rng=np.random.default_rng(1)
    for _ in range(200000):
        cx,cy,t=rng.uniform(0,a),rng.uniform(-.7,1.5),rng.uniform(0,np.pi/2)
        T=tile(cx,cy,t); s,c=cov(T,a)
        if s==1 and c>best[0]: best=(c,(cx,cy,t))
    print("random max single-sided grid coverage",best)
