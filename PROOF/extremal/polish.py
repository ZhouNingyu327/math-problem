"""Basin-hopping polish of xslp results: perturb + re-optimize; keep improvements. Tests whether stalls are true local maxima."""
import numpy as np, json, sys, glob
from xslp import optimize
from exact import min_depth
a = 2.0
rng = np.random.default_rng(int(sys.argv[1]))
files = sys.argv[2:]
res = []
for f in files:
    res += json.load(open(f))
res.sort(key=lambda r: -r['side'])
out = []
for r in res[:int(6)]:
    P = np.array(r['P']); best = r['side']; hist = [best]
    for hop in range(6):
        sc = 0.02 if hop % 2 == 0 else 0.005
        Q = P + rng.normal(0, sc, P.shape)
        Q, t, side = optimize(Q, a, iters=200, tr=0.01)
        if side > best + 1e-9:
            P, best = Q, side
        hist.append(round(best, 6))
    out.append(dict(P=P.tolist(), side=best, hist=hist))
    print(round(r['side'], 6), '->', round(best, 6), flush=True)
    json.dump(out, open(f'polish_{sys.argv[1]}.json', 'w'))
