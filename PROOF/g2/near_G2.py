"""Near-covers at a=2+eps of G2 type (strict: k=1, F holds no midpoint) with and without the requirement that F is essential on bd(Q4).
Start: the a=2 example (a2_G2.json) scaled; penalised Powell; float only. Reports min uncovered area of S found."""
import numpy as np, math, json, sys
from shapely.geometry import Polygon, box, LineString
from shapely.ops import unary_union
from scipy.optimize import minimize
a = float(sys.argv[1]); mode = sys.argv[2]   # 'free' or 'Fess'
mu = a/2
d = json.load(open('a2_G2.json')); s = a/2
x0 = np.array([0.5*s, 0.5*s, 0, 1.5*s, 0.5*s, 0, 1.5*s, 1.5*s, 0] + [d['V4'][0]*s, d['V4'][1]*s, d['V4'][2]] + [0.5*s, 0.9*s, 0] + [d['F'][0]*s, d['F'][1]*s, d['F'][2]])
names = ['V1', 'V2', 'V3', 'V4', 'C', 'F']
v = [(0, 0), (a, 0), (a, a), (0, a)]; m = [(mu, 0), (a, mu), (mu, a), (0, mu)]; c = (mu, mu)
need = {'V1': [v[0], m[0]], 'V2': [v[1]], 'V3': [v[2], m[1]], 'V4': [v[3], m[2]], 'C': [c, m[3]], 'F': []}
S = box(0, 0, a, a); bd = LineString([(0, mu), (mu, mu), (mu, a), (0, a), (0, mu)])
def sq(cx, cy, th):
    co, si = math.cos(th), math.sin(th)
    return Polygon([(cx + co*dx - si*dy, cy + si*dx + co*dy) for dx, dy in [(-.5,-.5),(.5,-.5),(.5,.5),(-.5,.5)]])
def cheb(p, cx, cy, th):
    dx, dy = p[0]-cx, p[1]-cy; co, si = math.cos(th), math.sin(th)
    return max(abs(co*dx + si*dy), abs(-si*dx + co*dy)) - 0.5
def evalx(x):
    P = {n: x[3*i:3*i+3] for i, n in enumerate(names)}
    pen = sum(max(0, cheb(p, *P[n]))**2 for n in names for p in need[n]) * 1e5
    pen += sum(max(0, 1e-3 - cheb(p, *P['F']))**2 for p in m) * 1e5
    polys = {n: sq(*P[n]) for n in names}
    five = unary_union([polys[n] for n in names if n != 'F'])
    unc = S.difference(unary_union([five, polys['F']])).area
    ess = bd.difference(five).length
    if mode == 'Fess': pen += max(0, 0.05 - ess)**2 * 1e3
    return unc, pen, ess
f = lambda x: sum(evalx(x)[:2])
rng = np.random.default_rng(0); best = None
for r in range(6):
    st = x0 if best is None else best.x + rng.normal(0, 0.02, 18)
    res = minimize(f, st, method='Powell', options={'maxfev': 12000, 'xtol': 1e-10, 'ftol': 1e-15})
    if best is None or res.fun < best.fun: best = res
    unc, pen, ess = evalx(best.x)
    print(f"a={a} mode={mode} round {r}: uncovered={unc:.3e} penalty={pen:.1e} F-essential length on bd(Q4)={ess:.3f}", flush=True)
json.dump(dict(a=a, mode=mode, x=best.x.tolist(), unc=unc, pen=pen, ess=ess), open(f'near_G2_{a}_{mode}.json', 'w'))
