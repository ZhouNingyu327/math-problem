"""pardfs + rigorous mirror reduction at the root + resume.
Root point p0 (a corner) is fixed by the diagonal reflection sigma:(x,y)->(y,x). We check that sigma maps P onto P (exactly, as
index permutation) and the family F onto F (exact bitset equality). Then a 6-cover using candidate T exists iff one using sigma(T)
exists, so only one of {T, sigma(T)} needs to be searched. Branches already finished in an earlier log are skipped (resume).
usage: pardfs_sym.py cert.json K slack nproc [previous_log ...]"""
import fps, exactdfs, numpy as np, json, sys, time, re
from multiprocessing import Pool
G = {}
def work(j):
    S, indptr, idx, compat, order, n, W = G['S'], G['indptr'], G['idx'], G['compat'], G['order'], G['n'], G['W']
    st = np.zeros(2, np.int64); t = time.time()
    found = exactdfs._dfs(S, indptr, idx, compat, order, S[j].copy(), 1, 6, n, W, st)
    return j, bool(found), int(st[0]), round(time.time() - t, 1)
if __name__ == '__main__':
    d = json.load(open(sys.argv[1])); K = int(sys.argv[2]); sl = float(sys.argv[3]); npr = int(sys.argv[4])
    P = np.array(d['P'], float); n = len(P)
    S, s = fps.family(P, K=K, slack=sl); W = S.shape[1]
    bits = fps.members(S, n); cnt = bits.sum(0)
    key = {(round(x, 9), round(y, 9)): i for i, (x, y) in enumerate(P)}
    perm = np.array([key.get((round(y, 9), round(x, 9)), -1) for x, y in P])
    sym = (perm >= 0).all() and len(set(perm)) == n
    rows = {bits[i].tobytes(): i for i in range(len(S))}
    mirror = None
    if sym:
        mb = bits[:, perm]   # mirrored set: point q in sigma(T) iff perm[q] in T
        mirror = np.array([rows.get(mb[i].tobytes(), -1) for i in range(len(S))])
        sym = (mirror >= 0).all()
    print(f"a={d['a']} n={n} |F|={len(S)} s={s:.9f} mirror-closed={sym}", flush=True)
    indptr = np.zeros(n + 1, np.int64); indptr[1:] = np.cumsum(cnt)
    idx = np.concatenate([np.nonzero(bits[:, p])[0] for p in range(n)]).astype(np.int64)
    B = bits.astype(np.float32); compat = (B.T @ B) > 0.5
    order = np.argsort(cnt, kind='stable').astype(np.int64)
    G.update(S=S, indptr=indptr, idx=idx, compat=compat, order=order, n=n, W=W)
    p = int(order[0]); cands = [int(j) for j in idx[indptr[p]:indptr[p+1]]]
    assert (not sym) or perm[p] == p, "root point not fixed by sigma"
    done = set()
    for lg in sys.argv[5:]:
        for line in open(lg):
            m = re.search(r"set (\d+): no cover", line)
            if m: done.add(int(m.group(1)))
    todo = []; seen = set()
    for j in cands:
        rep = min(j, int(mirror[j])) if sym else j
        if rep in seen: continue
        seen.add(rep)
        if j in done or (sym and int(mirror[j]) in done): continue
        todo.append(j)
    print(f"root point {p} {P[p]}: {len(cands)} candidates, {len(seen)} mirror classes, {len(todo)} still to search (skipped {len(seen)-len(todo)} done)", flush=True)
    t0 = time.time(); tot = 0; anyfound = False
    with Pool(npr) as pool:
        for k, (j, f, nodes, dt) in enumerate(pool.imap_unordered(work, todo)):
            tot += nodes; anyfound |= f
            print(f"  [{k+1}/{len(todo)}] set {j}: {'COVER FOUND' if f else 'no cover'} nodes={nodes} {dt}s", flush=True)
    print("EXACT PARALLEL DFS (mirror-reduced, resumed):", "A 6-COVER OF P EXISTS" if anyfound else "NO 6 SETS COVER P", f"nodes {tot}, wall {time.time()-t0:.1f}s", flush=True)
