"""a=2 cover with the closed G2 incidences in which bd(Q4) is NOT covered by V4 ∪ C (F essential on bd Q4).
V1=[0,1]^2 ∋ v1,m1;  V2=[1,2]x[0,1] ∋ v2;  V3=[1,2]^2 ∋ v3,m2;  C=[0,1]x[0.4,1.4] ∋ c=(1,1), m4=(0,1);
V4 tilted by th, containing v4=(0,2), m3=(1,2);  F free (must contain no midpoint).  Search over V4, F; report uncovered area."""
import numpy as np, math, json
from shapely.geometry import Polygon, box, LineString, Point
from shapely.ops import unary_union
from scipy.optimize import minimize
def sq(cx, cy, th):
    co, si = math.cos(th), math.sin(th)
    return Polygon([(cx + co*dx - si*dy, cy + si*dx + co*dy) for dx, dy in [(-.5,-.5),(.5,-.5),(.5,.5),(-.5,.5)]])
def cheb(p, cx, cy, th):
    dx, dy = p[0]-cx, p[1]-cy; co, si = math.cos(th), math.sin(th)
    return max(abs(co*dx + si*dy), abs(-si*dx + co*dy)) - 0.5
S = box(0, 0, 2, 2); V1 = box(0, 0, 1, 1); V2 = box(1, 0, 2, 1); V3 = box(1, 1, 2, 2); C = box(0, 0.4, 1, 1.4)
mids = [(1, 0), (2, 1), (1, 2), (0, 1)]
bdQ4 = LineString([(0, 1), (1, 1), (1, 2), (0, 2), (0, 1)])
def f(x):
    v4, F = x[:3], x[3:]
    pen = sum(max(0, cheb(p, *v4) + 1e-6)**2 for p in [(0, 2), (1, 2)]) * 1e4
    pen += sum(max(0, 1e-3 - cheb(p, *F))**2 for p in mids) * 1e4
    U = S.difference(unary_union([V1, V2, V3, C, sq(*v4), sq(*F)]))
    return U.area + pen
best = None
for th in [0.15, 0.25, 0.35, -0.2, -0.3]:
    for Fc in [(0.3, 1.6, 0.0), (0.2, 1.7, 0.3), (0.5, 1.9, 0.6)]:
        x0 = np.array([0.5 + 0.0, 1.5, th] + list(Fc))
        r = minimize(f, x0, method='Powell', options={'maxfev': 20000, 'xtol': 1e-10, 'ftol': 1e-15})
        if best is None or r.fun < best.fun: best = r
v4, F = best.x[:3], best.x[3:]
P4, PF = sq(*v4), sq(*F)
U = S.difference(unary_union([V1, V2, V3, C, P4, PF]))
resid = bdQ4.difference(unary_union([P4, C]))
rep = dict(V4=[float(t) for t in v4], F=[float(t) for t in F], th_V4_deg=math.degrees(v4[2]), uncovered_area=U.area,
           V4_has_v4_m3=[cheb(p, *v4) <= 1e-9 for p in [(0, 2), (1, 2)]], F_min_cheb_to_midpoints=min(cheb(p, *F) for p in mids),
           bdQ4_not_in_V4_or_C=resid.length, bdQ4_not_in_any=bdQ4.difference(unary_union([V1, V2, V3, C, P4, PF])).length)
print(json.dumps(rep, default=lambda o: bool(o) if isinstance(o, (bool, np.bool_)) else float(o)))
json.dump(rep, open('a2_G2.json', 'w'), default=lambda o: bool(o) if isinstance(o, (bool, np.bool_)) else float(o))
