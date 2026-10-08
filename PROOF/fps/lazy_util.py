import numpy as np, math
from shapely.geometry import Polygon, box as sbox
from shapely.ops import unary_union, polylabel
from scipy.optimize import minimize
def sqpoly(cx, cy, th, side=1.0):
    c, s = math.cos(th), math.sin(th); h = side/2
    return Polygon([(cx + c*dx - s*dy, cy + s*dx + c*dy) for dx, dy in [(-h,-h),(h,-h),(h,h),(-h,h)]])
def uncovered(poses, a, side=1.0):
    return sbox(0, 0, a, a).difference(unary_union([sqpoly(*p, side=side) for p in poses]))
def realize(Pts, K, a=None):
    D = (math.pi/2)/K; ths = (np.arange(K)+0.5)*D
    c, s = np.cos(ths)[:, None], np.sin(ths)[:, None]
    u = Pts[:, 0][None]*c + Pts[:, 1][None]*s; v = -Pts[:, 0][None]*s + Pts[:, 1][None]*c
    w = np.maximum(u.max(1)-u.min(1), v.max(1)-v.min(1)); k = int(np.argmin(w)); th = ths[k]
    uc = (u[k].max()+u[k].min())/2; vc = (v[k].max()+v[k].min())/2
    return (uc*math.cos(th) - vc*math.sin(th), uc*math.sin(th) + vc*math.cos(th), th), w[k]
def polish(poses, a, iters=1500):
    f = lambda x: uncovered(x.reshape(-1, 3), a).area
    r = minimize(f, np.array(poses).ravel(), method='Powell', options={'maxfev': iters, 'xtol': 1e-5, 'ftol': 1e-10})
    return r.x.reshape(-1, 3), r.fun
def new_points(U, k=3):
    geoms = [g for g in getattr(U, 'geoms', [U]) if g.geom_type == 'Polygon' and g.area > 1e-14]
    geoms.sort(key=lambda g: -g.area); pts = []
    for g in geoms[:k]:
        try: p = polylabel(g, tolerance=1e-4)
        except Exception: p = g.representative_point()
        if not g.contains(p): p = g.representative_point()
        pts.append((p.x, p.y))
    return pts
