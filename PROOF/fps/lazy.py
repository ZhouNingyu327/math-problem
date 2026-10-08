"""Lazy point generation: grow P until no 6 sets of the (superset) family cover P."""
import fps, numpy as np, math, json, time, sys
from shapely.geometry import Polygon, box as sbox
from shapely.ops import unary_union, polylabel
from scipy.optimize import minimize

a = float(sys.argv[1]); K = int(sys.argv[2]); tag = sys.argv[3] if len(sys.argv) > 3 else ''
maxit = int(sys.argv[4]) if len(sys.argv) > 4 else 400
rng = np.random.default_rng(0)
out = f"lazy_{a}_{K}{tag}.json"
Sq = sbox(0, 0, a, a)

def sqpoly(cx, cy, th, side=1.0):
    c, s = math.cos(th), math.sin(th); h = side / 2
    pts = [(cx + c*dx - s*dy, cy + s*dx + c*dy) for dx, dy in [(-h,-h),(h,-h),(h,h),(-h,h)]]
    return Polygon(pts)

def uncovered(poses, side=1.0):
    U = unary_union([sqpoly(*p, side=side) for p in poses])
    return Sq.difference(U)

def realize(Pts, K):
    D = (math.pi/2)/K
    ths = (np.arange(K)+0.5)*D
    c, s = np.cos(ths)[:, None], np.sin(ths)[:, None]
    u = Pts[:, 0][None]*c + Pts[:, 1][None]*s
    v = -Pts[:, 0][None]*s + Pts[:, 1][None]*c
    w = np.maximum(u.max(1)-u.min(1), v.max(1)-v.min(1))
    k = int(np.argmin(w)); th = ths[k]
    uc = (u[k].max()+u[k].min())/2; vc = (v[k].max()+v[k].min())/2
    return (uc*math.cos(th) - vc*math.sin(th), uc*math.sin(th) + vc*math.cos(th), th), w[k]

def polish(poses, iters=1500):
    x0 = np.array(poses).ravel()
    f = lambda x: uncovered(x.reshape(-1, 3)).area
    r = minimize(f, x0, method='Powell', options={'maxfev': iters, 'xtol': 1e-5, 'ftol': 1e-10})
    return r.x.reshape(-1, 3), r.fun

def new_points(U, k=3):
    geoms = [g for g in getattr(U, 'geoms', [U]) if g.area > 1e-14 and g.geom_type == 'Polygon']
    geoms.sort(key=lambda g: -g.area)
    pts = []
    for g in geoms[:k]:
        try:
            p = polylabel(g, tolerance=1e-4)
        except Exception:
            p = g.representative_point()
        if not g.contains(p):
            p = g.representative_point()
        pts.append((p.x, p.y))
    return pts

g = np.linspace(0, a, 5)
P = [(x, y) for x in g for y in g]
log = []
t0 = time.time()
for it in range(maxit):
    Pa = np.array(P)
    S, s = fps.family(Pa, K=K)
    M = fps.members(S, len(Pa))
    r, obj, db = fps.cover_status(M, 6, tl=1200)
    rec = dict(it=it, n=len(P), nsets=int(S.shape[0]), t=round(time.time()-t0, 1), lb=round(db,3))
    if r == 'CERT':
        rec['status'] = 'INFEASIBLE'; log.append(rec); print(rec, flush=True)
        json.dump(dict(a=a, K=K, s=s, P=P, log=log, status='CERT'), open(out, 'w'))
        break
    if r == 'unknown':
        rec['status'] = 'timeout'; log.append(rec); print(rec, flush=True)
        json.dump(dict(a=a, K=K, s=s, P=P, log=log, status='timeout'), open(out, 'w'))
        break
    poses = []; ws = []
    for i in r:
        pp, w = realize(Pa[M[i]], K); poses.append(pp); ws.append(w)
    while len(poses) < 6:
        poses.append((rng.uniform(0, a), rng.uniform(0, a), rng.uniform(0, 1.5)))
    U0 = uncovered(poses)
    pol, ar = polish(poses, iters=600 if it % 5 else 2000)
    U1 = uncovered(pol)
    newp = new_points(U1, 3) + new_points(U0, 1)
    rec.update(status='feasible', unc_raw=round(U0.area, 6), unc_pol=float(ar), maxw=round(max(ws), 4), added=len(newp))
    log.append(rec); print(rec, flush=True)
    if ar < 1e-12:
        print('POSSIBLE COVER', pol.tolist()); json.dump(dict(a=a, poses=pol.tolist()), open('POSSIBLE_COVER.json', 'w'))
    for q in newp:
        if min(math.hypot(q[0]-p[0], q[1]-p[1]) for p in P) > 1e-4:
            P.append((float(q[0]), float(q[1])))
    json.dump(dict(a=a, K=K, s=s, P=P, log=log, status='running'), open(out, 'w'))
