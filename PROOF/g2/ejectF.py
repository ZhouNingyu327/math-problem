"""G2 (k=1) eject-F test. S=[0,a]^2, v1=(0,0),v2=(a,0),v3=(a,a),v4=(0,a); m1=(a/2,0) (side v1v2), m2=(a,a/2), m3=(a/2,a), m4=(0,a/2); c=(a/2,a/2).
G2 labelling (ATTEMPT §5): m4 in C, c in C, m3 in V4, m2 in V3, m1 in V1, F holds no midpoint. Q4=[0,a/2]x[a/2,a].
Search: 6 unit squares satisfying all incidences (hard, checked exactly at the end), with
  (i) bd(Q4) covered by V4 ∪ C ∪ F, and (ii) a part of bd(Q4) of length >= Lmin NOT in V4 ∪ C (so F is essential on bd Q4);
objective: uncovered area of S (by all six) + penalties.  Float/shapely; final configuration re-checked."""
import numpy as np, math, json, sys
from shapely.geometry import Polygon, box, LineString, Point
from shapely.ops import unary_union
from scipy.optimize import minimize
a = float(sys.argv[1]); Lmin = float(sys.argv[2]); seed = int(sys.argv[3])
mu = a/2
V = {'v1': (0, 0), 'v2': (a, 0), 'v3': (a, a), 'v4': (0, a)}
M = {'m1': (mu, 0), 'm2': (a, mu), 'm3': (mu, a), 'm4': (0, mu)}
c = (mu, mu)
bdQ4 = LineString([(0, mu), (mu, mu), (mu, a), (0, a), (0, mu)])
S = box(0, 0, a, a)
names = ['V1', 'V2', 'V3', 'V4', 'C', 'F']
need = {'V1': [V['v1'], M['m1']], 'V2': [V['v2']], 'V3': [V['v3'], M['m2']], 'V4': [V['v4'], M['m3']], 'C': [c, M['m4']], 'F': []}
def sq(cx, cy, th, side=1.0):
    co, si = math.cos(th), math.sin(th); h = side/2
    return Polygon([(cx + co*dx - si*dy, cy + si*dx + co*dy) for dx, dy in [(-h,-h),(h,-h),(h,h),(-h,h)]])
def cheb(p, cx, cy, th):
    dx, dy = p[0]-cx, p[1]-cy; co, si = math.cos(th), math.sin(th)
    return max(abs(co*dx + si*dy), abs(-si*dx + co*dy)) - 0.5   # <=0 iff inside
def parts(x):
    return {n: x[3*i:3*i+3] for i, n in enumerate(names)}
def obj(x, w=1.0):
    P = parts(x); pen = 0.0
    for n in names:
        for p in need[n]: pen += max(0, cheb(p, *P[n]) + 1e-4)**2 * 1e3
    for p in M.values(): pen += max(0, -cheb(p, *P['F']) + 1e-4)**2 * 1e3   # F holds no midpoint
    polys = {n: sq(*P[n]) for n in names}
    U2 = unary_union([polys['V4'], polys['C']])
    resid = bdQ4.difference(U2)                    # part of bd Q4 not in V4 ∪ C
    pen += max(0, Lmin - resid.length)**2 * 1e2
    pen += resid.difference(polys['F']).length * 10   # must be covered by F (only F; V1..V3 not allowed to help)
    unc = S.difference(unary_union(list(polys.values()))).area
    return unc + pen
rng = np.random.default_rng(seed)
x0 = np.array([0.5, 0.5, 0, a-0.5, 0.5, 0, a-0.5, a-0.5, 0, 0.5, a-0.5, 0, 0.55, mu, 0, mu, mu+0.3, 0.5]) + rng.normal(0, 0.05, 18)
x0[15:17] = rng.uniform(0.3, a-0.3, 2)
best = None
for rnd in range(4):
    r = minimize(obj, x0 if best is None else best.x + rng.normal(0, 0.01, 18), method='Powell', options={'maxfev': 15000, 'xtol': 1e-9, 'ftol': 1e-14})
    if best is None or r.fun < best.fun: best = r
x = best.x; P = parts(x); polys = {n: sq(*P[n]) for n in names}
U2 = unary_union([polys['V4'], polys['C']]); resid = bdQ4.difference(U2)
rep = dict(a=a, Lmin=Lmin, seed=seed, poses={n: list(map(float, P[n])) for n in names},
    incidences_ok=all(cheb(p, *P[n]) <= 1e-9 for n in names for p in need[n]),
    F_no_midpoint=all(cheb(p, *P['F']) > 0 for p in M.values()), c_in_F=cheb(c, *P['F']) <= 0,
    bdQ4_minus_V4C_len=resid.length, bdQ4_uncovered_by_all6=bdQ4.difference(unary_union(list(polys.values()))).length,
    resid_not_in_F=resid.difference(polys['F']).length, S_uncovered_area=S.difference(unary_union(list(polys.values()))).area, obj=float(best.fun))
print(json.dumps(rep, default=lambda o: bool(o) if isinstance(o, (bool, np.bool_)) else float(o))); json.dump(rep, open(f'ejectF_{a}_{Lmin}_{seed}.json', 'w'), default=lambda o: bool(o) if isinstance(o, (bool, np.bool_)) else float(o))
