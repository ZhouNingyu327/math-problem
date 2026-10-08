"""Relaxation: 5 unit squares + K, K = (disk of diameter sqrt2) ∩ (strip of width 1), rotatable, i.e. the largest
convex set with diameter <= sqrt2 and width <= 1 containing a unit square. Does it cover S_a (a>2)?
If yes, no argument that uses only the diameter and width of one tile can work. Powell on uncovered area (shapely). Float only."""
import numpy as np, sys
from scipy.optimize import minimize
from shapely.geometry import Point, box, Polygon
from shapely.ops import unary_union
from shapely import affinity
def sq(cx, cy, th):
    c, s = np.cos(th), np.sin(th)
    return Polygon([(cx + c*u - s*v, cy + s*u + c*v) for u, v in [(-.5,-.5),(.5,-.5),(.5,.5),(-.5,.5)]])
a = float(sys.argv[1]); r = 2**.5/2
S = box(0, 0, a, a)
K0 = Point(0, 0).buffer(r, 128).intersection(box(-1, -.5, 1, .5))
def unc(z):
    T = [sq(*z[3*i:3*i+3]) for i in range(5)]
    K = affinity.translate(affinity.rotate(K0, z[17], use_radians=True, origin=(0, 0)), z[15], z[16])
    return S.difference(unary_union(T + [K])).area
rng = np.random.default_rng(2); best = 9
for k in range(16):
    z = np.concatenate([np.array([[.5,.5,0],[1.5,.5,0],[.5,1.5,0],[1.5,1.5,0],[1.,1.,.4]]).ravel(), [a-.5, a-.5, 0.]])
    z = z*np.r_[np.tile([a/2, a/2, 1], 5), [1, 1, 1]] + rng.normal(0, .15, 18)
    res = minimize(unc, z, method='Powell', options=dict(maxiter=30000, xtol=1e-7, ftol=1e-12))
    res = minimize(unc, res.x, method='Powell', options=dict(maxiter=30000, xtol=1e-8, ftol=1e-14))
    best = min(best, res.fun); print(round(res.fun, 9), flush=True)
    if res.fun < 1e-10:
        print('COVER FOUND', list(map(float, res.x))); break
print('best', best)
