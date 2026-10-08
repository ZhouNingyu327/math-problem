"""Base odd k x k grid + lazily added D4-orbits of points from gaps of realized/polished near-covers."""
import fps, numpy as np, math, json, time, sys
from lazy_util import realize, polish, uncovered, new_points
a = float(sys.argv[1]); K = int(sys.argv[2]); k = int(sys.argv[3]); maxit = int(sys.argv[4]) if len(sys.argv) > 4 else 100
out = f"lazysym_{a}_{K}_{k}.json"
def orbit(p):
    x, y = p; pts = set()
    for (u, v) in [(x, y), (y, x)]:
        for (s, t) in [(u, v), (a-u, v), (u, a-v), (a-u, a-v)]:
            pts.add((round(s, 12), round(t, 12)))
    return list(pts)
g = np.linspace(0, a, k)
P = [(float(x), float(y)) for x in g for y in g]
log = []; t0 = time.time(); rng = np.random.default_rng(0)
for it in range(maxit):
    Pa = np.array(P)
    S, s = fps.family(Pa, K=K); M = fps.members(S, len(Pa))
    r, obj, db = fps.cover_status(M, 6, tl=3600)
    rec = dict(it=it, n=len(P), nsets=int(S.shape[0]), t=round(time.time()-t0, 1), lb=round(db, 3))
    if r == 'CERT' or r == 'unknown':
        rec['status'] = r; log.append(rec); print(rec, flush=True)
        json.dump(dict(a=a, K=K, s=s, P=P, log=log, status=r), open(out, 'w')); break
    poses = [realize(Pa[M[i]], K, a)[0] for i in r]
    while len(poses) < 6: poses.append((rng.uniform(0, a), rng.uniform(0, a), 0.3))
    U0 = uncovered(poses, a, side=s)
    pol, ar = polish(poses, a, iters=1500)
    U1 = uncovered(pol, a)
    newp = new_points(U1, 2) + new_points(U0, 2)
    rec.update(status='feasible', unc_raw=round(U0.area, 6), unc_pol=round(float(ar), 6)); log.append(rec); print(rec, flush=True)
    have = set((round(x, 12), round(y, 12)) for x, y in P)
    for q in newp:
        for o in orbit(q):
            if o not in have: P.append(o); have.add(o)
    json.dump(dict(a=a, K=K, s=s, P=P, log=log, status='running'), open(out, 'w'))
