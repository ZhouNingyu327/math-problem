"""Verify an FPS certificate: P subset of [0,a]^2 such that no 6 unit squares cover P.
1. family F (superset, see fps.py docstring) regenerated with K frames and slack 'sl';
2. sanity: 20000 random unit squares (random orientation/centre near P): each covered subset of P is contained in a member of F;
3. exact DFS (exactdfs.py): no 6 members of F cover P.
usage: verify_cert.py cert.json K slack"""
import fps, exactdfs, numpy as np, json, sys, math, time
d = json.load(open(sys.argv[1])); K = int(sys.argv[2]); sl = float(sys.argv[3])
a = d['a']; P = np.array(d['P'], float); n = len(P)
assert P.min() >= -1e-12 and P.max() <= a + 1e-12
S, s = fps.family(P, K=K, slack=sl)
print(f"a={a} n={n} K={K} side_bound={s:.9f} |F|={len(S)}", flush=True)
B = fps.members(S, n)
rng = np.random.default_rng(1); bad = 0
for _ in range(20000):
    th = rng.uniform(0, math.pi/2); c0 = P[rng.integers(n)] + rng.uniform(-0.6, 0.6, 2)
    u = (P - c0) @ np.array([math.cos(th), math.sin(th)]); v = (P - c0) @ np.array([-math.sin(th), math.cos(th)])
    T = (np.abs(u) <= 0.5) & (np.abs(v) <= 0.5)
    if T.any() and not ((B | ~T[None]).all(1)).any(): bad += 1
print("random-square containment failures:", bad, flush=True)
t = time.time(); ok, st = exactdfs.no_cover(S, n, 6)
print("EXACT DFS:", "NO 6 SETS COVER P" if ok else "A 6-COVER OF P EXISTS", "nodes", st[0], "lb-prunes", st[1], f"{time.time()-t:.1f}s", flush=True)
