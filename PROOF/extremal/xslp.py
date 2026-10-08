"""Exchange-SLP local maximization of exact min covering depth (=> coverable side a/(1-2t)).
Floating point exploration only."""
import numpy as np, sys, json
from scipy.optimize import linprog
from exact import min_depth, mdepth, candidates

def lp_step(P, X, tr):
    m, am = mdepth(P, X)
    rows = []; rhs = []; tags = []
    for j in range(len(X)):
        i = am[j]; cx, cy, th = P[i]; x, y = X[j]
        for k in range(4):
            ang = th + k*np.pi/2; nx, ny = np.cos(ang), np.sin(ang)
            val = nx*(x-cx) + ny*(y-cy)
            if 0.5 - val - m[j] > 0.2: continue
            r = np.zeros(19)
            r[3*i] = -nx; r[3*i+1] = -ny; r[3*i+2] = -np.sin(ang)*(x-cx) + np.cos(ang)*(y-cy); r[18] = 1
            rows.append(r); rhs.append(0.5 - val); tags.append((j, i, k))
    c = np.zeros(19); c[18] = -1
    res = linprog(c, A_ub=np.array(rows), b_ub=np.array(rhs), bounds=[(-tr, tr)]*18 + [(None, None)], method='highs')
    return res, tags

def optimize(P, a, iters=300, tr=0.05, verbose=False):
    g = np.linspace(0, a, 21); G = np.array([(x, y) for x in g for y in g])
    pool = np.zeros((0, 2))
    t, _, _ = min_depth(P, a)
    for it in range(iters):
        _, Xc, mc = min_depth(P, a, k=60)
        pool = np.concatenate([pool, Xc])[-1500:]
        X = np.concatenate([G, pool])
        res, tags = lp_step(P, X, tr)
        if res.status != 0: tr *= 0.5; continue
        Pn = P + res.x[:18].reshape(6, 3)
        tn, _, _ = min_depth(Pn, a)
        if tn > t + 1e-13:
            P, t = Pn, tn; tr = min(tr*1.6, 0.1)
        else:
            tr *= 0.4
        if tr < 1e-9: break
    return P, t, a/(1-2*t)

if __name__ == '__main__':
    seed, nstart = int(sys.argv[1]), int(sys.argv[2]); a = 2.0
    rng = np.random.default_rng(seed); out = []
    for s in range(nstart):
        P0 = np.zeros((6, 3)); P0[:, :2] = rng.uniform(0.4, a-0.4, (6, 2)); P0[:, 2] = rng.uniform(0, np.pi/2, 6)
        P, t, side = optimize(P0, a)
        out.append(dict(P=P.tolist(), t=float(t), side=float(side)))
        print(s, round(side, 6), flush=True)
        json.dump(out, open(f'xslp_{seed}.json', 'w'))
