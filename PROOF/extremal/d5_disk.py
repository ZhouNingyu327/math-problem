"""Can 5 unit squares + one disk of diameter sqrt2 cover S_a (a>2)? If yes, 'Lemma D(5)' (uncovered set of any 5 tiles has diam>sqrt2) is FALSE.
Powell on uncovered area (shapely). Float only."""
import numpy as np, sys
from scipy.optimize import minimize
from shapely.geometry import Point, box
from shapely.ops import unary_union
from d5_test import sq
a = float(sys.argv[1]); r = 2**.5/2 * float(sys.argv[2]) if len(sys.argv) > 2 else 2**.5/2
S = box(0, 0, a, a); Dq = Point(0, 0).buffer(1, 256)
def unc(z):
    T = [sq(*z[3*i:3*i+3]) for i in range(5)]
    D = Point(z[15], z[16]).buffer(r, 128)
    return S.difference(unary_union(T + [D])).area
rng = np.random.default_rng(1); best = 9
starts = []
# brick-like start: bottom row grid, top row grid, disk at top-right gap + spare
for k in range(12):
    z = np.concatenate([np.array([[.5, .5, 0], [1.5, .5, 0], [.5, 1.5, 0], [1.5, 1.5, 0], [1., 1., .4]]).ravel(), [a-.5, a-.5]])
    z = z*np.r_[np.tile([a/2, a/2, 1], 5), [1, 1]] + rng.normal(0, .15, 17)
    starts.append(z)
for z0 in starts:
    res = minimize(unc, z0, method='Powell', options=dict(maxiter=20000, xtol=1e-7, ftol=1e-12))
    res = minimize(unc, res.x, method='Powell', options=dict(maxiter=20000, xtol=1e-8, ftol=1e-14))
    best = min(best, res.fun); print(round(res.fun, 9), flush=True)
    if res.fun < 1e-10:
        print('COVER FOUND', list(res.x)); break
print('best', best)
