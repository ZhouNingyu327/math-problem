"""Extremal / jammed-configuration search for 6 unit squares covering [0,a]^2.
Max-min depth formulation: maximize t such that every sample x in S_a lies in some tile shrunk by t
(i.e. at depth >= t). Exact identity: mu*(a) = (1 - a/S(6))/2, so the coverable side of a configuration
with depth t at side a is a/(1-2t). Local method: SLP with tile assignment = argmax depth, linearized
rotation, trust region. LP duals = stress (KKT multipliers) on sample points.
Floating point exploration only (NOT a certificate)."""
import numpy as np, sys, json
from scipy.optimize import linprog

def depth(P, X):
    # P: (6,3) cx,cy,th ; X: (N,2). returns (6,N) depth = min over 4 edges of 1/2 - |proj|
    D = []
    for cx, cy, th in P:
        c, s = np.cos(th), np.sin(th)
        dx, dy = X[:, 0] - cx, X[:, 1] - cy
        u = c * dx + s * dy; v = -s * dx + c * dy
        D.append(0.5 - np.maximum(np.abs(u), np.abs(v)))
    return np.array(D)

def samples(a, n):
    g = np.linspace(0, a, n)
    X = np.array([(x, y) for x in g for y in g])
    return X

def slp(P, a, n=41, iters=200, tr=0.05, X=None, verbose=False):
    if X is None: X = samples(a, n)
    P = P.copy(); hist = []
    for it in range(iters):
        D = depth(P, X)
        # assign each sample to best tile; also include near-ties (within 0.02) to allow switching
        best = D.max(0)
        t0 = best.min()
        rows = []; rhs = []
        nv = 19
        for i in range(6):
            mask = D[i] >= best - 0.03
            idx = np.where(mask)[0]
            if len(idx) == 0: continue
            cx, cy, th = P[i]
            for k in range(4):
                ang = th + k * np.pi / 2
                nx, ny = np.cos(ang), np.sin(ang)
                dnx, dny = -np.sin(ang), np.cos(ang)
                # constraint: n.(x-c) <= 1/2 - t  -> linearize in (dc, dth)
                for j in idx:
                    x, y = X[j]
                    val = nx * (x - cx) + ny * (y - cy)
                    # d/dcx = -nx, d/dcy=-ny, d/dth = dnx*(x-cx)+dny*(y-cy)
                    r = np.zeros(nv)
                    r[3*i] = -nx; r[3*i+1] = -ny; r[3*i+2] = dnx*(x-cx)+dny*(y-cy)
                    r[18] = 1.0
                    rows.append(r); rhs.append(0.5 - val)
        # only keep points: each point must be satisfied by at least one tile -> with fixed assignment
        # we require it for argmax tile only (others are optional). Rebuild with argmax only:
        rows = []; rhs = []; owner = []
        am = D.argmax(0)
        for j in range(len(X)):
            i = am[j]; cx, cy, th = P[i]; x, y = X[j]
            for k in range(4):
                ang = th + k*np.pi/2
                nx, ny = np.cos(ang), np.sin(ang)
                val = nx*(x-cx)+ny*(y-cy)
                if 0.5 - val - best[j] > 0.25:  # far from binding: skip
                    continue
                r = np.zeros(nv)
                r[3*i] = -nx; r[3*i+1] = -ny; r[3*i+2] = -np.sin(ang)*(x-cx)+np.cos(ang)*(y-cy)
                r[18] = 1.0
                rows.append(r); rhs.append(0.5 - val); owner.append((j, i, k))
        A = np.array(rows); b = np.array(rhs)
        bounds = [(-tr, tr)] * 18 + [(None, None)]
        cobj = np.zeros(nv); cobj[18] = -1
        res = linprog(cobj, A_ub=A, b_ub=b, bounds=bounds, method='highs')
        if res.status != 0:
            tr *= 0.5; continue
        dP = res.x[:18].reshape(6, 3)
        Pn = P + dP
        tn = depth(Pn, X).max(0).min()
        if tn > t0 + 1e-12:
            P = Pn; tr = min(tr * 1.5, 0.1)
        else:
            tr *= 0.5
        hist.append(max(t0, tn))
        if tr < 1e-7: break
    D = depth(P, X); t = D.max(0).min()
    # stress from final LP
    duals = None
    try:
        duals = -res.ineqlin.marginals
    except Exception:
        pass
    return P, t, a / (1 - 2 * t), dict(owner=owner, duals=duals, X=X)

def random_start(a, rng):
    P = np.zeros((6, 3))
    P[:, :2] = rng.uniform(0.5, a - 0.5, (6, 2))
    P[:, 2] = rng.uniform(0, np.pi / 2, 6)
    return P

if __name__ == '__main__':
    seed = int(sys.argv[1]); nstart = int(sys.argv[2]); a = 2.0
    rng = np.random.default_rng(seed)
    out = []
    for s in range(nstart):
        P0 = random_start(a, rng)
        P, t, side, info = slp(P0, a, n=31, iters=150)
        P, t, side, info = slp(P, a, n=61, iters=150, tr=0.01)
        out.append(dict(P=P.tolist(), t=t, side=side))
        print(s, round(side, 5), flush=True)
    json.dump(out, open(f'slp_{seed}.json', 'w'))
