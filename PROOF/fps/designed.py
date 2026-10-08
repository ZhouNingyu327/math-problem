"""Designed point set: odd k grid + rows hugging the midlines (offset d) + corner-diagonal points; D4-symmetric.
usage: designed.py a K k d1,d2 t1,t2,..   -> HiGHS min set cover; writes designed_<a>_<K>_<k>.json"""
import fps, numpy as np, json, sys, time
a = float(sys.argv[1]); K = int(sys.argv[2]); k = int(sys.argv[3])
ds = [float(v) for v in sys.argv[4].split(',')] if sys.argv[4] != '-' else []
tc = [float(v) for v in sys.argv[5].split(',')] if sys.argv[5] != '-' else []
g = np.linspace(0, a, k); pts = set()
def add(x, y):
    for (u, v) in [(x, y), (y, x)]:
        for (s, t) in [(u, v), (a-u, v), (u, a-v), (a-u, a-v)]:
            pts.add((round(s, 12), round(t, 12)))
for x in g:
    for y in g: add(x, y)
for d in ds:
    for x in g: add(x, a/2 - d)
for t in tc: add(t, t)
P = sorted(pts); Pa = np.array(P)
t0 = time.time(); S, s = fps.family(Pa, K=K); M = fps.members(S, len(Pa))
print(f"a={a} K={K} k={k} ds={ds} tc={tc} n={len(P)} |F|={len(S)} family {time.time()-t0:.0f}s", flush=True)
r, obj, db = fps.cover_status(M, 6, tl=float(sys.argv[6]) if len(sys.argv) > 6 else 2400)
res = 'CERT' if r == 'CERT' else ('cover' if isinstance(r, list) else 'unknown')
print(f"RESULT {res} obj={obj} lb={db} {time.time()-t0:.0f}s", flush=True)
json.dump(dict(a=a, K=K, s=s, P=P, status=res, ds=ds, tc=tc), open(f"designed_{a}_{K}_{k}.json", 'w'))
